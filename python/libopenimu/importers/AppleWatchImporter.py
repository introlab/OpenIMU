"""

    AppleWatchImporter
    @authors Dominic Létourneau, Simon Brière
    @date 30/05/2018

"""

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
import os
import zipfile
import struct

class AppleWatchImporter(BaseImporter):
    HEADER = 0xEAEA
    BATTERY_ID = 0x01
    SENSORIA_ID = 0x02
    HEARTRATE_ID = 0x03
    PROCESSED_MOTION_ID = 0x04
    # LOCATION_ID = 0x05
    BEACONS_ID = 0x06
    COORDINATES_ID = 0x7
    RAW_MOTION_ID = 0x8

    def __init__(self, manager: DBManager, participant: Participant):
        super().__init__(manager, participant)
        # No recordsets when starting
        self.recordsets = []

    def load(self, filename):
        print('AppleWatchImporter.load')
        results = {}

        if 'zip' in filename:
            results = self.load_zip(filename)
        else:
            with open(filename, "rb") as file:
                print('Loading File: ', filename)
                results = self.readDataFile(file)

        #print('results len', len(results))
        return results

    def load_zip(self, filename):
        results = {}
        with zipfile.ZipFile(filename) as myzip:
            # print('zip opened')
            namelist = myzip.namelist()

            # print('zip contains : ', namelist)

            # TODO
            # First find SETTINGS file

            # Then process data files
            for file in namelist:
                if '.data' in file:
                    print('Reading file: ', file)
                    my_file = myzip.open(file)
                    values = self.readDataFile(my_file, False)

                    # Add to global results
                    if values is not None:
                        for timestamp in values:
                            if not results.__contains__(timestamp):
                                results[timestamp] = values[timestamp]
                            else:
                                if len(values[timestamp]['battery']) > 0:
                                    results[timestamp]['battery'] = values[timestamp]['battery']

                                if len(values[timestamp]['beacons']) > 0:
                                    results[timestamp]['beacons'] = values[timestamp]['beacons']

                                if len(values[timestamp]['sensoria']) > 0:
                                    results[timestamp]['sensoria'] = values[timestamp]['sensoria']

                                if len(values[timestamp]['heartrate']) > 0:
                                    results[timestamp]['heartrate'] = values[timestamp]['heartrate']

                                if len(values[timestamp]['motion']) > 0:
                                    results[timestamp]['motion'] = values[timestamp]['motion']

                                # if len(values[timestamp]['location']) > 0:
                                #     results[timestamp]['location'] = values[timestamp]['location']
                                #   pass

                                if len(values[timestamp]['coordinates']) > 0:
                                    results[timestamp]['coordinates'] = values[timestamp]['coordinates']
                else:
                    pass
                    # print('Unknown file : ', file)

        return results

    def get_recordset(self, timestamp):
        try:
            my_time = datetime.datetime.fromtimestamp(timestamp)
        except:
            return

        # Validate timestamp
        if my_time > datetime.datetime.now() or my_time < datetime.datetime(2018,1,1):
            print("Invalid timestamp: " + str(timestamp));
            return

        # Find a record the same day
        for record in self.recordsets:
            # Same date return this record
            if record.start_timestamp.date() == my_time.date():
                return record

        # Return new record
        recordset = self.db.add_recordset(self.participant, str(my_time.date()), my_time, my_time)
        self.recordsets.append(recordset)
        return recordset

    def import_motion_to_database(self, sample_rate, timestamp, recordset, sensors, channels, data: list):

        # print('import_motion_to_database')
        # print('data', data, len(data))

        values = np.array(data, dtype=np.float32)
        # print("Values shape: ", values.shape)
        end_timestamp = timestamp + int(np.floor(len(values) / sample_rate))
        # print("timestamps, ", timestamp, end_timestamp)

        # Calculate last index to remove extra values
        real_size = int(np.floor(len(values) / sample_rate) * sample_rate)
        # print('real size:', real_size)

        # Update end_timestamp if required
        if end_timestamp > recordset.end_timestamp.timestamp():
            recordset.end_timestamp = datetime.datetime.fromtimestamp(end_timestamp)

        if real_size > 0:
            # Acc
            for i in range(len(channels['acc'])):
                self.add_sensor_data_to_db(recordset, sensors['acc'], channels['acc'][i],
                                           datetime.datetime.fromtimestamp(timestamp),
                                           datetime.datetime.fromtimestamp(end_timestamp), values[0:real_size, i])

            # Gyro
            for i in range(len(channels['gyro'])):
                self.add_sensor_data_to_db(recordset, sensors['gyro'], channels['gyro'][i],
                                           datetime.datetime.fromtimestamp(timestamp),
                                           datetime.datetime.fromtimestamp(end_timestamp), values[0:real_size, i + 6])

        #self.db.commit()

    def import_battery_to_database(self, sample_rate, timestamp, recordset, sensors, channels, data: list):

        # print('import_motion_to_database')
        # print('data', data, len(data))

        values = np.array(data, dtype=np.float32)
        # print("Values shape: ", values.shape)
        end_timestamp = timestamp + 1
        # print("timestamps, ", timestamp, end_timestamp)

        # Calculate last index to remove extra values
        real_size = int(np.floor(len(values) / sample_rate) * sample_rate)
        # print('real size:', real_size)

        # Update end_timestamp if required
        if end_timestamp > recordset.end_timestamp.timestamp():
            recordset.end_timestamp = datetime.datetime.fromtimestamp(end_timestamp)

        if real_size > 0:
            # Batt
            self.add_sensor_data_to_db(recordset, sensors['batt'], channels['batt'],
                                       datetime.datetime.fromtimestamp(timestamp),
                                       datetime.datetime.fromtimestamp(end_timestamp), values[0, 0])

        #self.db.commit()

    def import_heartrate_to_database(self, sample_rate, timestamp, recordset, sensors, channels, data: list):

        # print('import_motion_to_database')
        # print('data', data, len(data))

        values = np.array(data, dtype=np.float32)
        # print("Values shape: ", values.shape)
        end_timestamp = timestamp + 1
        # print("timestamps, ", timestamp, end_timestamp)

        # Calculate last index to remove extra values
        real_size = int(np.floor(len(values) / sample_rate) * sample_rate)
        # print('real size:', real_size)

        # Update end_timestamp if required
        if end_timestamp > recordset.end_timestamp.timestamp():
            recordset.end_timestamp = datetime.datetime.fromtimestamp(end_timestamp)

        if real_size > 0:
            # print('heartrate size:', real_size)
            # Heartrate
            self.add_sensor_data_to_db(recordset, sensors['heartrate'], channels['heartrate'],
                                       datetime.datetime.fromtimestamp(timestamp),
                                       datetime.datetime.fromtimestamp(end_timestamp), values[0, 0])

        #self.db.commit()

    def import_coordinates_to_database(self, sample_rate, timestamp, recordset, sensors, channels, data: list):

        # print('import_motion_to_database')
        # print('data', data, len(data))

        values = np.array(data, dtype=np.float32)
        # print("Values shape: ", values.shape)
        end_timestamp = timestamp + 1
        # print("timestamps, ", timestamp, end_timestamp)

        # Calculate last index to remove extra values
        real_size = int(np.floor(len(values) / sample_rate) * sample_rate)
        # print('real size:', real_size)

        # Update end_timestamp if required
        if end_timestamp > recordset.end_timestamp.timestamp():
            recordset.end_timestamp = datetime.datetime.fromtimestamp(end_timestamp)

        if real_size > 0:
            # Coordinates

            # Build gps data
            geo = GPSGeodetic()
            geo.latitude = values[0][0] * 1e7
            geo.longitude = values[0][1] * 1e7

            # Store
            self.add_sensor_data_to_db(recordset, sensors['coordinates'], channels['coordinates'],
                                       datetime.datetime.fromtimestamp(timestamp),
                                       datetime.datetime.fromtimestamp(end_timestamp), geo)

        #self.db.commit()

    def import_sensoria_to_database(self, sample_rate, timestamp, recordset, sensors, channels, data: list):
        # print('import_sensoria_to_database')
        # print('data', data, len(data))

        # Ignore tick (useless for now)
        fsr_values = np.array([val[1:4] for val in data], dtype=np.int16)
        motion_values = np.array([val[4:] for val in data], dtype=np.float32)

        # print("Values shape: ", values.shape)
        end_timestamp = timestamp + int(np.floor(len(motion_values) / sample_rate))
        # print("timestamps, ", timestamp, end_timestamp)

        # Calculate last index to remove extra values
        real_size = int(np.floor(len(motion_values) / sample_rate) * sample_rate)
        # print('real size:', real_size)

        # Update end_timestamp if required
        if end_timestamp > recordset.end_timestamp.timestamp():
            recordset.end_timestamp = datetime.datetime.fromtimestamp(end_timestamp)

        if real_size > 0:
            # Acc
            for i in range(len(channels['sensoria_acc'])):
                self.add_sensor_data_to_db(recordset, sensors['sensoria_acc'], channels['sensoria_acc'][i],
                                           datetime.datetime.fromtimestamp(timestamp),
                                           datetime.datetime.fromtimestamp(end_timestamp), motion_values[0:real_size, i])

            # Gyro
            for i in range(len(channels['sensoria_gyro'])):
                self.add_sensor_data_to_db(recordset, sensors['sensoria_gyro'], channels['sensoria_gyro'][i],
                                           datetime.datetime.fromtimestamp(timestamp),
                                           datetime.datetime.fromtimestamp(end_timestamp), motion_values[0:real_size, i + 3])

            # Magneto
            for i in range(len(channels['sensoria_mag'])):
                self.add_sensor_data_to_db(recordset, sensors['sensoria_mag'], channels['sensoria_mag'][i],
                                           datetime.datetime.fromtimestamp(timestamp),
                                           datetime.datetime.fromtimestamp(end_timestamp),
                                           motion_values[0:real_size, i + 6])

            # FSR
            for i in range(len(channels['sensoria_fsr'])):
                self.add_sensor_data_to_db(recordset, sensors['sensoria_fsr'], channels['sensoria_fsr'][i],
                                           datetime.datetime.fromtimestamp(timestamp),
                                           datetime.datetime.fromtimestamp(end_timestamp),
                                           fsr_values[0:real_size, i])

        #self.db.commit()

    def import_beacons_to_database(self, sample_rate, timestamp, recordset, sensors, channels, data: list):
        namespaces = [val[0:10] for val in data]
        namespaces = [[str(format(x, 'x')).rjust(2, '0') for x in tup] for tup in namespaces]
        print(namespaces)

    def import_to_database(self, result):
        print('AppleWatchImporter.import_to_database')

        # Sample rate is hardcoded for now
        sample_rate = 50

        # Create sensors
        accelerometer_sensor = self.add_sensor_to_db(SensorType.ACCELEROMETER, 'Accelerometer',
                                                     'AppleWatch',
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
                                            'AppleWatch',
                                            'Unknown', sample_rate, 1)

        gyro_channels = list()

        # Create channels
        gyro_channels.append(self.add_channel_to_db(gyro_sensor, Units.DEG_PER_SEC,
                                                    DataFormat.FLOAT32, 'Gyro_X'))

        gyro_channels.append(self.add_channel_to_db(gyro_sensor, Units.DEG_PER_SEC,
                                                    DataFormat.FLOAT32, 'Gyro_Y'))

        gyro_channels.append(self.add_channel_to_db(gyro_sensor, Units.DEG_PER_SEC,
                                                    DataFormat.FLOAT32, 'Gyro_Z'))

        # Battery
        battery_sensor = self.add_sensor_to_db(SensorType.BATTERY, 'Battery', 'AppleWatch', 'Unknown', 1, 1)

        battery_channel = self.add_channel_to_db(battery_sensor, Units.VOLTS, DataFormat.FLOAT32, 'Battery Percentage')

        # Heartrate
        heartrate_sensor = self.add_sensor_to_db(SensorType.HEARTRATE, 'Heartrate', 'AppleWatch', 'Unknown', 1, 1)

        heartrate_channel = self.add_channel_to_db(heartrate_sensor, Units.BPM, DataFormat.FLOAT32, 'Heartrate')

        # Coordinates
        coordinates_sensor = self.add_sensor_to_db(SensorType.GPS, 'Coordinates', 'AppleWatch', 'Unknown', 1, 1)

        coordinates_channel = self.add_channel_to_db(coordinates_sensor, Units.NONE, DataFormat.UINT8, 'Coordinates')

        # Sensoria
        sensoria_acc_sensor = self.add_sensor_to_db(SensorType.ACCELEROMETER, 'Accelerometer', 'Sensoria', 'Foot',
                                                    sample_rate, 1)

        sensoria_acc_channels = list()
        sensoria_acc_channels.append(self.add_channel_to_db(sensoria_acc_sensor, Units.GRAVITY_G,
                                                             DataFormat.FLOAT32, 'Accelerometer_X'))
        sensoria_acc_channels.append(self.add_channel_to_db(sensoria_acc_sensor, Units.GRAVITY_G,
                                                             DataFormat.FLOAT32, 'Accelerometer_Y'))
        sensoria_acc_channels.append(self.add_channel_to_db(sensoria_acc_sensor, Units.GRAVITY_G,
                                                             DataFormat.FLOAT32, 'Accelerometer_Z'))

        sensoria_gyro_sensor = self.add_sensor_to_db(SensorType.GYROMETER, 'Gyrometer', 'Sensoria', 'Foot',
                                                    sample_rate, 1)
        sensoria_gyro_channels = list()
        sensoria_gyro_channels.append(self.add_channel_to_db(sensoria_gyro_sensor, Units.DEG_PER_SEC,
                                                    DataFormat.FLOAT32, 'Gyro_X'))
        sensoria_gyro_channels.append(self.add_channel_to_db(sensoria_gyro_sensor, Units.DEG_PER_SEC,
                                                    DataFormat.FLOAT32, 'Gyro_Y'))
        sensoria_gyro_channels.append(self.add_channel_to_db(sensoria_gyro_sensor, Units.DEG_PER_SEC,
                                                    DataFormat.FLOAT32, 'Gyro_Z'))

        sensoria_mag_sensor = self.add_sensor_to_db(SensorType.MAGNETOMETER, 'Magnetometer', 'Sensoria', 'Foot',
                                                     sample_rate, 1)
        sensoria_mag_channels = list()
        sensoria_mag_channels.append(self.add_channel_to_db(sensoria_mag_sensor, Units.GAUSS,
                                                             DataFormat.FLOAT32, 'Mag_X'))
        sensoria_mag_channels.append(self.add_channel_to_db(sensoria_mag_sensor, Units.GAUSS,
                                                             DataFormat.FLOAT32, 'Mag_Y'))
        sensoria_mag_channels.append(self.add_channel_to_db(sensoria_mag_sensor, Units.GAUSS,
                                                             DataFormat.FLOAT32, 'Mag_Z'))

        sensoria_fsr_sensor = self.add_sensor_to_db(SensorType.FSR, 'FSR', 'Sensoria', 'Foot',
                                                     sample_rate, 1)
        sensoria_fsr_channels = list()
        sensoria_fsr_channels.append(self.add_channel_to_db(sensoria_fsr_sensor, Units.NONE,
                                                            DataFormat.SINT16, 'META-1'))
        sensoria_fsr_channels.append(self.add_channel_to_db(sensoria_fsr_sensor, Units.NONE,
                                                            DataFormat.SINT16, 'META-5'))
        sensoria_fsr_channels.append(self.add_channel_to_db(sensoria_fsr_sensor, Units.NONE,
                                                            DataFormat.SINT16, 'HEEL'))

        #Beacons
        beacons_sensor = self.add_sensor_to_db(SensorType.BEACON, 'Beacons', 'Kontact', 'Environment', 1, 1)


        # Create sensor and channels dict
        sensors = {'acc': accelerometer_sensor,
                   'gyro': gyro_sensor,
                   'batt': battery_sensor,
                   'heartrate': heartrate_sensor,
                   'coordinates': coordinates_sensor,
                   'sensoria_acc': sensoria_acc_sensor,
                   'sensoria_gyro': sensoria_gyro_sensor,
                   'sensoria_mag': sensoria_mag_sensor,
                   'sensoria_fsr': sensoria_fsr_sensor,
                   'beacons_sensor': beacons_sensor}

        channels = {'acc': accelerometer_channels,
                    'gyro': gyro_channels,
                    'batt': battery_channel,
                    'heartrate': heartrate_channel,
                    'coordinates': coordinates_channel,
                    'sensoria_acc': sensoria_acc_channels,
                    'sensoria_gyro': sensoria_gyro_channels,
                    'sensoria_mag': sensoria_mag_channels,
                    'sensoria_fsr': sensoria_fsr_channels
                    }

        if result is None:
            return

        for timestamp in result:
            # Change recordset each day
            recordset = self.get_recordset(timestamp)

            if recordset is None:
                continue

            if result[timestamp].__contains__('battery'):
                # print('battery')
                if result[timestamp]['battery']:
                    self.import_battery_to_database(1, timestamp, recordset, sensors, channels,
                                                result[timestamp]['battery'])

            if result[timestamp].__contains__('beacons'):
                # print('beacons')
                if result[timestamp]['beacons']:
                    self.import_beacons_to_database(sample_rate, timestamp, recordset, sensors, channels,
                                                     result[timestamp]['beacons'])
                pass

            if result[timestamp].__contains__('sensoria'):
                # print('sensoria')
                if result[timestamp]['sensoria']:
                    self.import_sensoria_to_database(sample_rate, timestamp, recordset, sensors, channels,
                                                     result[timestamp]['sensoria'])
                pass

            if result[timestamp].__contains__('heartrate'):
                # print('heartrate')
                if result[timestamp]['heartrate']:
                    self.import_heartrate_to_database(1, timestamp, recordset, sensors, channels,
                                                  result[timestamp]['heartrate'])

            if result[timestamp].__contains__('motion'):
                # print('motion')
                if result[timestamp]['motion']:
                    self.import_motion_to_database(sample_rate, timestamp, recordset, sensors, channels,
                                               result[timestamp]['motion'])

            if result[timestamp].__contains__('coordinates'):
                # print('coordinates')
                if result[timestamp]['coordinates']:
                    self.import_coordinates_to_database(1, timestamp, recordset, sensors, channels,
                                                    result[timestamp]['coordinates'])

        # Commit to DB
        self.db.commit()


    def readDataFile(self, file, debug=False):
        '''
        All binary files have a similar header
        • Two bytes for file identifier (based on Wimu format): 0xEA, 0xEA
        • File Version byte: eg. 0x01
        • 4 bytes (as UInt32) for participantID
        • Byte for sensor identification
        ◦ Battery: 1
        ◦ Sensoria: 2
        ◦ Heartrate: 3
        ◦ Motion: 4
        * Location : 5
        ◦ Beacons: 6
        ◦ Coordinates: 7
        '''

        results = {}

        [file_header_id, version, participant_id, sensor_id] = struct.unpack("<HBIB", file.read(2 + 1 + 4 + 1))

        if file_header_id != self.HEADER:
            return None

        if debug:
            print('reading header : ', hex(file_header_id), hex(version))
            print('participant_id : ', participant_id)
            print('sensor_id : ', hex(sensor_id))

        # if version == 1: Nothing more to do

        if version == 2:
            [json_data_size] = struct.unpack("<I", file.read(4))
            [json_data] = struct.unpack("<{}s".format(json_data_size), file.read(json_data_size))
            settings_json_str = json_data.decode("utf-8")
            if debug:
                print('setting_json : ', settings_json_str)

            [end_header_id] = struct.unpack("<H", file.read(2))
            if end_header_id != self.HEADER:
                if debug:
                    print('Error unpacking file, header not ending with 0xEAEA')
                return None

        try:

            last_timestamp = None

            while file.readable():
                # Read timestamp
                [timestamp_ms] = struct.unpack("<Q", file.read(8))
                timestamp_sec = int(np.round(timestamp_ms / 1000))

                if sensor_id == self.PROCESSED_MOTION_ID:
                    if last_timestamp is None:
                        last_timestamp = timestamp_sec
                    else:
                        if timestamp_sec < last_timestamp:
                            print('error backward timestamp')
                        if timestamp_sec > last_timestamp + 3600:
                            # print('One hour, changing timestamp')
                            last_timestamp = timestamp_sec

                if debug:
                    print('TIMESTAMP (MS): ', timestamp_ms)
                    print('time: ', datetime.datetime.fromtimestamp(timestamp_sec))

                # Initialize data structure at this timestamp if required
                if not results.__contains__(timestamp_sec):
                    # print("init timestamp = ", timestamp_ms)
                    results[timestamp_sec] = {}
                    results[timestamp_sec]['battery'] = []
                    results[timestamp_sec]['sensoria'] = []
                    results[timestamp_sec]['heartrate'] = []
                    results[timestamp_sec]['motion'] = []
                    results[timestamp_sec]['location'] = []
                    results[timestamp_sec]['beacons'] = []
                    results[timestamp_sec]['coordinates'] = []

                if sensor_id == self.BATTERY_ID:
                    # Battery data
                    data = self.read_battery_data(file.read(2), debug)
                    results[timestamp_sec]['battery'].append(data)

                elif sensor_id == self.SENSORIA_ID:
                    # Sensoria data
                    data = self.read_sensoria_data(file.read(46), debug)
                    results[timestamp_sec]['sensoria'].append(data)

                elif sensor_id == self.HEARTRATE_ID:
                    # Heartrate data
                    data = self.read_heartrate_data(file.read(1), debug)
                    results[timestamp_sec]['heartrate'].append(data)

                elif sensor_id == self.PROCESSED_MOTION_ID:
                    # Motion data
                    data = self.read_motion_data(file.read(52), debug)
                    results[last_timestamp]['motion'].append(data)

                elif sensor_id == self.BEACONS_ID:
                    # Beacons data
                    data = self.read_beacons_data(file.read(18), debug)
                    results[timestamp_sec]['beacons'].append(data)

                elif sensor_id == self.COORDINATES_ID:
                    # Coordinates data
                    data = self.read_coordinates_data(file.read(28), debug)
                    results[timestamp_sec]['coordinates'].append(data)

                else:
                    print("unknown sensor_id: ", hex(sensor_id))
                    return None

        except:
            pass

        return results

    def read_battery_data(self, chunk, debug=False):
        """
        • Byte integer for battery level between 0 and 100 (percent)
        ◦ 0 meaning invalid level (eg. where state is .unknown)
        • Byte for battery state
        ◦ unknown: 0
        ◦ unplugged: 1
        ◦ charging: 2
        ◦ full: 3
        :param chunk:
        :return:
        """
        assert (len(chunk) == 2)
        data = struct.unpack("BB", chunk)
        if debug:
            print('BATTERY: ', data)
        return data

    def read_sensoria_data(self, chunk, debug=False):
        """
        46 bytes of received frame (will require further processing)
        This assumes that all socks we have use the F20 streaming protocol, as defined in
        SensoriaCoreData. As of now, the app ignores all other protocol to not pollute the files. In the
        future, it would be the best to deserialize these frames directly upon importation into OpenIMU.
        As this will be more cumbersome, for now the deserialization is made directly on reception.
        * Tick (Int32)
        • 3 Int16 for the 3 channels (pressure sensors)
        • 9 Float32 for inertial sensors
        ◦ accelerometer (x,y,z)
        ◦ gyroscope (x,y,z)
        ◦ magnetometer (x,y,z)

        """
        assert(len(chunk) == 46)
        data = struct.unpack("<1i3h9f", chunk)
        if debug:
            print('SENSORIA: ', data)
        return data

    def read_heartrate_data(self, chunk, debug=False):
        """
        unsigned integer as single Byte for bpm
        ** assumes that bpm cannot go above 255, hence values above are clamped to 255
        :param chunk:
        :return:
        """
        assert (len(chunk) == 1)
        data = struct.unpack("<B", chunk)
        if debug:
            print('HEARTRATE: ', data)
        return data

    def read_motion_data(self, chunk, debug=False):
        """
         13 Float32 values, hence 52 bytes, with following fields
        • acceleration (x,y,z)
        • gravity vector (x,y,z)
        • gyroscope (x,y,z)
        • attitude quaternion (w,x,y,z)
            """
        assert (len(chunk) == 52)
        data = struct.unpack("<13f", chunk)
        if debug:
            print('MOTION: ', data)
        return data

    def read_location_data(self, chunk, debug=False):
        # This is not a log file type
        return []

    def read_beacons_data(self, chunk, debug=False):
        """
        10 Bytes Char for namespace
        6 Bytes Char for instance ID
        1 Int8 for TxPower
        1 Int8 for RSSI
        :param chunk:
        :return:
        """
        assert (len(chunk) == 18)
        data = struct.unpack("<16B2b", chunk)
        if debug:
            print('BEACONS: ', data)
        return data

    def read_coordinates_data(self, chunk, debug=False):
        """
          7 Float32 values, hence 28 bytes
        • latitude
        • longitude
        • accuracy in meters for lat/long
        • altitude in meters from sea level
        • accuracy in meters for altitude
        • speed (meters per second)
        • course (degrees relative to true north)
        :return:
        """
        assert (len(chunk) == 28)
        data = struct.unpack("<7f", chunk)
        if debug:
            print('COORDINATES: ', data)
        return data
