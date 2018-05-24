from libopenimu.importers.BaseImporter import BaseImporter
from libopenimu.models.sensor_types import SensorType
from libopenimu.models.units import Units
from libopenimu.models.Recordset import Recordset
from libopenimu.models.data_formats import DataFormat
from libopenimu.tools.timing import timing
from libopenimu.db.DBManager import DBManager
from libopenimu.models.Participant import Participant
from libopenimu.importers.wimu import GPSGeodetic

import numpy as np
import math
import datetime

import struct
import sys
import binascii
import datetime
import string


class OpenIMUImporter(BaseImporter):
    def __init__(self, manager: DBManager, participant: Participant):
        super().__init__(manager, participant)
        print('OpenIMU Importer')
        # No recordsets when starting
        self.recordsets = []

    def get_recordset(self, timestamp):
        my_time = datetime.datetime.fromtimestamp(timestamp)

        # Find a record the same day
        for record in self.recordsets:
            # Same date return this record
            if record.start_timestamp.date() == my_time.date():
                return record

        # Return new record
        recordset = self.db.add_recordset(self.participant, str(my_time.date()), my_time, my_time)
        self.recordsets.append(recordset)
        return recordset

    @timing
    def load(self, filename):
        print('OpenIMUImporter.load')
        results = {}
        with open(filename, "rb") as file:
            print('Loading File: ', filename)
            results = self.readDataFile(file)

        print('Done!')
        return results

    @timing
    def import_imu_to_database(self, timestamp, recordset, data: list):

        print('import_imu_to_database')

        # Sample rate is hardcoded for now
        sample_rate = 50

        # Create sensors
        accelerometer_sensor = self.add_sensor_to_db(SensorType.ACCELEROMETER, 'Accelerometer',
                                                     'OpenIMU-HW',
                                                     'Unknown', sample_rate, 1)

        accelerometer_channels = list()

        # Create channels
        accelerometer_channels.append(self.add_channel_to_db(accelerometer_sensor, Units.GRAVITY_G,
                                                             DataFormat.FLOAT32, 'Accelerometer_X'))

        accelerometer_channels.append(self.add_channel_to_db(accelerometer_sensor, Units.GRAVITY_G,
                                                             DataFormat.FLOAT32, 'Accelerometer_Y'))

        accelerometer_channels.append(self.add_channel_to_db(accelerometer_sensor, Units.GRAVITY_G,
                                                             DataFormat.FLOAT32, 'Accelerometer_Z'))

        # Create sensor
        gyro_sensor = self.add_sensor_to_db(SensorType.GYROMETER, 'Gyro',
                                            'OpenIMU-HW',
                                            'Unknown', sample_rate, 1)

        gyro_channels = list()

        # Create channels
        gyro_channels.append(self.add_channel_to_db(gyro_sensor, Units.DEG_PER_SEC,
                                                    DataFormat.FLOAT32, 'Gyro_X'))

        gyro_channels.append(self.add_channel_to_db(gyro_sensor, Units.DEG_PER_SEC,
                                                    DataFormat.FLOAT32, 'Gyro_Y'))

        gyro_channels.append(self.add_channel_to_db(gyro_sensor, Units.DEG_PER_SEC,
                                                    DataFormat.FLOAT32, 'Gyro_Z'))

        # Create sensor
        mag_sensor = self.add_sensor_to_db(SensorType.MAGNETOMETER, 'Magnetometer',
                                            'OpenIMU-HW',
                                            'Unknown', sample_rate, 1)

        mag_channels = list()

        # Create channels
        mag_channels.append(self.add_channel_to_db(mag_sensor, Units.UTESLA,
                                                    DataFormat.FLOAT32, 'Mag_X'))

        mag_channels.append(self.add_channel_to_db(mag_sensor, Units.UTESLA,
                                                    DataFormat.FLOAT32, 'Mag_Y'))

        mag_channels.append(self.add_channel_to_db(mag_sensor, Units.UTESLA,
                                                    DataFormat.FLOAT32, 'Mag_Z'))

        values = np.array(data, dtype=np.float32)
        # print("Values shape: ", values.shape)
        end_timestamp = timestamp + int(np.floor(len(values) / sample_rate))

        # Calculate last index to remove extra values
        real_size = int(np.floor(len(values) / sample_rate) * sample_rate)
        # print('real size:', real_size)

        # Update end_timestamp if required
        if end_timestamp > recordset.end_timestamp.timestamp():
            recordset.end_timestamp = datetime.datetime.fromtimestamp(end_timestamp)

        # Acc
        for i in range(len(accelerometer_channels)):
            self.add_sensor_data_to_db(recordset, accelerometer_sensor, accelerometer_channels[i],
                                       datetime.datetime.fromtimestamp(timestamp),
                                       datetime.datetime.fromtimestamp(end_timestamp), values[0:real_size, i])

        # Gyro
        for i in range(len(gyro_channels)):
            self.add_sensor_data_to_db(recordset, gyro_sensor, gyro_channels[i],
                                       datetime.datetime.fromtimestamp(timestamp),
                                       datetime.datetime.fromtimestamp(end_timestamp), values[0:real_size, i + 3])

        # Magnetometer
        for i in range(len(mag_channels)):
            self.add_sensor_data_to_db(recordset, mag_sensor, mag_channels[i],
                                       datetime.datetime.fromtimestamp(timestamp),
                                       datetime.datetime.fromtimestamp(end_timestamp), values[0:real_size, i + 6])

        self.db.commit()

    @timing
    def import_power_to_database(self, timestamp, recordset, data: list):

        # Create sensors
        battery_sensor = self.add_sensor_to_db(SensorType.BATTERY, 'Battery',
                                                     'OpenIMU-HW',
                                                     'Unknown', 1, 1)

        current_sensor = self.add_sensor_to_db(SensorType.CURRENT, 'Current',
                                                     'OpenIMU-HW',
                                                     'Unknown', 1, 1)

        # Create channels
        battery_channel = self.add_channel_to_db(battery_sensor, Units.VOLTS,
                                                 DataFormat.FLOAT32, 'Voltage')

        current_channel = self.add_channel_to_db(current_sensor, Units.AMPERES,
                                                 DataFormat.FLOAT32, 'Current')

        # Get data in the form of array
        values = np.array(data, dtype=np.float32)
        # print("Values shape: ", values.shape)
        # print(values[:, 0])
        # print(values[:, 1])

        end_timestamp = timestamp + len(values)

        # Update end_timestamp if required
        if end_timestamp > recordset.end_timestamp.timestamp():
            recordset.end_timestamp = datetime.datetime.fromtimestamp(end_timestamp)

        self.add_sensor_data_to_db(recordset, battery_sensor, battery_channel,
                                   datetime.datetime.fromtimestamp(timestamp),
                                   datetime.datetime.fromtimestamp(end_timestamp), values[:, 0])

        self.add_sensor_data_to_db(recordset, current_sensor, current_channel,
                                   datetime.datetime.fromtimestamp(timestamp),
                                   datetime.datetime.fromtimestamp(end_timestamp), values[:, 1])

        self.db.commit()

    @timing
    def import_gps_to_database(self, timestamp, recordset, data: list):

        # Create sensors
        gps_sensor = self.add_sensor_to_db(SensorType.GPS, 'GPS',
                                            'OpenIMU-HW',
                                            'Unknown', 1, 1)

        gps_channel = self.add_channel_to_db(gps_sensor, Units.NONE,
                                              DataFormat.UINT8, 'GPS_SIRF')

        # Get data in the form of array
        values = np.array(data, dtype=np.float32)
        # print("Values shape: ", values.shape)
        # print(values[:, 0])
        # print(values[:, 1])

        end_timestamp = timestamp + len(values)

        # Update end_timestamp if required
        if end_timestamp > recordset.end_timestamp.timestamp():
            recordset.end_timestamp = datetime.datetime.fromtimestamp(end_timestamp)


        # print('GPS DATA ', values)
        # Regenerate GPS data to be stored in the DB as SIRF data
        # TODO Better GPS solution?

        # We have one sample per second of GPS data
        for i in range(len(values)):
            val = values[i]
            geo = GPSGeodetic()
            # Discard invalid data
            if math.isnan(val[1]) or math.isnan(val[2]):
                continue
            geo.latitude = val[1] * 1e7
            geo.longitude = val[2] * 1e7
            #altitude = val[3] * 1e7
            self.add_sensor_data_to_db(recordset, gps_sensor, gps_channel,
                                       datetime.datetime.fromtimestamp(timestamp + i),
                                       datetime.datetime.fromtimestamp(timestamp + i), geo)

        # Commit to file
        self.db.commit()





    @timing
    def import_baro_to_database(self, timestamp, recordset, data: list):
        # Create sensors
        baro_sensor = self.add_sensor_to_db(SensorType.BAROMETER, 'Barometer',
                                               'OpenIMU-HW',
                                               'Unknown', 1, 1)

        baro_channel = self.add_channel_to_db(baro_sensor, Units.KPA,
                                                 DataFormat.FLOAT32, 'Pressure')

        # Get data in the form of array
        values = np.array(data, dtype=np.float32)
        # print("Values shape: ", values.shape)

        end_timestamp = timestamp + len(values)

        # Update end_timestamp if required
        if end_timestamp > recordset.end_timestamp.timestamp():
            recordset.end_timestamp = datetime.datetime.fromtimestamp(end_timestamp)

        self.add_sensor_data_to_db(recordset, baro_sensor, baro_channel,
                                   datetime.datetime.fromtimestamp(timestamp),
                                   datetime.datetime.fromtimestamp(end_timestamp), values[:, 0])

    @timing
    def import_to_database(self, result):
        print('OpenIMUImporter.import_to_database')

        for timestamp in result:

            recordset = self.get_recordset(timestamp)

            if result[timestamp].__contains__('imu'):
                # print('contains imu')
                self.import_imu_to_database(timestamp, recordset, result[timestamp]['imu'])
            if result[timestamp].__contains__('power'):
                # print('contains power')
                self.import_power_to_database(timestamp, recordset, result[timestamp]['power'])
            if result[timestamp].__contains__('gps'):
                # print('contains gps')
                self.import_gps_to_database(timestamp, recordset, result[timestamp]['gps'])
            if result[timestamp].__contains__('baro'):
                # print('contains baro')
                self.import_baro_to_database(timestamp, recordset, result[timestamp]['baro'])

    def processImuChunk(self, chunk, debug=False):
        data = struct.unpack("9f", chunk)

        if debug:
            print("IMU: ", data)

        return data

    def processTimestampChunk(self, chunk, debug=False):
        [timestamp] = struct.unpack("i", chunk)
        if debug:
            print(datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'))
        return timestamp

    def processGPSChunk(self, chunk, debug=False):
        data = struct.unpack("?3f", chunk)
        if debug:
            print("GPS: ", data)
        return data

    def processBarometerChunk(self, chunk, debug=False):
        data = struct.unpack("2f", chunk)
        if debug:
            print("BARO: ", data[0], data[1])
        return data

    def processPowerChunk(self, chunk, debug=False):
        data = struct.unpack("2f", chunk)
        if debug:
            print("POWER: ", data[0], data[1])
        return data

    def readDataFile(self, file, debug=False):
        n = 0
        results = {}
        timestamp = None

        # Todo better than while 1?
        while True:

            chunk = file.read(1)
            if len(chunk) < 1:
                print("Reached end of file")
                break

            (headChar) = struct.unpack("c", chunk)
            # print('headchar ', headChar)

            if headChar[0] == b'h':
                n = n + 1
                print("New log stream")
            elif headChar[0] == b't':
                n = n + 1
                chunk = file.read(struct.calcsize("i"))
                current_timestamp = self.processTimestampChunk(chunk)

                if timestamp is None:
                    timestamp = current_timestamp
                else:
                    if current_timestamp >= timestamp + 3600:  # Max 1 hour of data per timestamp
                        timestamp = current_timestamp

                # Initialize data structure at this timestamp
                if not results.__contains__(timestamp):
                    print("init timestamp = ", timestamp)
                    results[timestamp] = {}
                    results[timestamp]['gps'] = []
                    results[timestamp]['power'] = []
                    results[timestamp]['imu'] = []
                    results[timestamp]['baro'] = []

            elif headChar[0] == b'i':
                n = n + 1
                chunk = file.read(struct.calcsize("9f"))
                data = self.processImuChunk(chunk)
                if timestamp is not None:
                    results[timestamp]['imu'].append(data)

            elif headChar[0] == b'g':
                n = n + 1
                chunk = file.read(struct.calcsize("?3f"))
                data = self.processGPSChunk(chunk)
                if timestamp is not None:
                    results[timestamp]['gps'].append(data)

            elif headChar[0] == b'p':
                n = n + 1
                chunk = file.read(struct.calcsize("2f"))
                data = self.processPowerChunk(chunk)
                if timestamp is not None:
                    results[timestamp]['power'].append(data)

            elif headChar[0] == b'b':
                n = n + 1
                chunk = file.read(struct.calcsize("2f"))
                data = self.processBarometerChunk(chunk)
                if timestamp is not None:
                    results[timestamp]['baro'].append(data)

            else:
                print("Unrecognised chunk :", headChar[0])
                break

        return results
