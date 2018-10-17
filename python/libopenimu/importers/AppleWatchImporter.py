"""

    AppleWatchImporter
    @authors Dominic Létourneau, Simon Brière
    @date 30/05/2018

"""

from libopenimu.importers.BaseImporter import BaseImporter
from libopenimu.models.sensor_types import SensorType
from libopenimu.models.SensorTimestamps import SensorTimestamps
from libopenimu.models.units import Units
from libopenimu.models.Recordset import Recordset
from libopenimu.models.data_formats import DataFormat
from libopenimu.tools.timing import timing
from libopenimu.db.DBManager import DBManager
from libopenimu.models.Participant import Participant
from libopenimu.importers.wimu import GPSGeodetic
from libopenimu.importers.importer_types import BeaconData

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
import json # For file header config
import gc

from collections import defaultdict

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
    RAW_ACCELERO_ID = 0x9
    RAW_GYRO_ID = 0x0A

    def __init__(self, manager: DBManager, participant: Participant):
        super().__init__(manager, participant)
        # No recordsets when starting
        self.recordsets = []

    def load(self, filename):
        print('AppleWatchImporter.load')
        results = {}

        # Removed zip loading for now,
        if 'zip' in filename:
            results = self.load_zip(filename)
        else:
            with open(filename, "rb") as file:
                print('Loading File: ', filename)
                results = self.readDataFile(file)

        print('results len', len(results))
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

                    # Merge data
                    if values is not None:
                        results.update(values)
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
        if my_time > datetime.datetime.now() or my_time < datetime.datetime(2018, 1, 1):
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

    def import_raw_motion_to_database(self, sample_rate, timestamp, recordset, sensors, channels, data: list):

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
            for i in range(len(channels['raw_acc'])):
                self.add_sensor_data_to_db(recordset, sensors['raw_acc'], channels['raw_acc'][i],
                                           datetime.datetime.fromtimestamp(timestamp),
                                           datetime.datetime.fromtimestamp(end_timestamp), values[0:real_size, i])

            # Gyro
            for i in range(len(channels['raw_gyro'])):
                self.add_sensor_data_to_db(recordset, sensors['raw_gyro'], channels['raw_gyro'][i],
                                           datetime.datetime.fromtimestamp(timestamp),
                                           datetime.datetime.fromtimestamp(end_timestamp), values[0:real_size, i + 3])

    def import_raw_accelerometer_to_database(self, sample_rate, timestamp, recordset, sensors, channels, data: list):

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
            for i in range(len(channels['raw_acc'])):
                self.add_sensor_data_to_db(recordset, sensors['raw_acc'], channels['raw_acc'][i],
                                           datetime.datetime.fromtimestamp(timestamp),
                                           datetime.datetime.fromtimestamp(end_timestamp), values[0:real_size, i])

        #self.db.commit()

    def import_raw_gyro_to_database(self, sample_rate, timestamp, recordset, sensors, channels, data: list):

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
            # Gyro
            for i in range(len(channels['raw_gyro'])):
                self.add_sensor_data_to_db(recordset, sensors['raw_gyro'], channels['raw_gyro'][i],
                                           datetime.datetime.fromtimestamp(timestamp),
                                           datetime.datetime.fromtimestamp(end_timestamp), values[0:real_size, i])

        #self.db.commit()

    def import_heartrate_to_database(self, sample_rate, heartrate: dict):
        # DL Oct. 17 2018, New import to database
        heartrate_sensor = self.add_sensor_to_db(SensorType.HEARTRATE, 'Heartrate', 'AppleWatch', 'Wrist',
                                                 sample_rate, 1)

        heartrate_channel = self.add_channel_to_db(heartrate_sensor, Units.BPM, DataFormat.UINT8, 'Heartrate')

        for timestamp in heartrate:
            print('heartrate', timestamp, len(heartrate[timestamp]['times']),
                  len(heartrate[timestamp]['values']))

            # Calculate recordset
            recordset = self.get_recordset(timestamp.timestamp())

            # Create time array as float64
            timesarray = np.asarray(heartrate[timestamp]['times'], dtype=np.float64)

            if len(timesarray) is 0:
                print('Empty data, returning')
                return

            # Other values are float32
            valuesarray = np.asarray(heartrate[timestamp]['values'], dtype=np.uint8)

            # Create sensor timestamps first
            sensor_timestamps = SensorTimestamps()
            sensor_timestamps.timestamps = timesarray
            sensor_timestamps.update_timestamps()

            # Update timestamps in recordset
            # This should not happen, recordset is initialized at the beginning of the hour
            if sensor_timestamps.start_timestamp < recordset.start_timestamp:
                recordset.start_timestamp = sensor_timestamps.start_timestamp
            # This can occur though
            if sensor_timestamps.end_timestamp > recordset.end_timestamp:
                recordset.end_timestamp = sensor_timestamps.end_timestamp

            # Store data
            self.add_sensor_data_to_db(recordset, heartrate_sensor, heartrate_channel,
                                       sensor_timestamps, valuesarray[:, 0])

    def import_coordinates_to_database(self, sample_rate, coordinates: dict):
        # DL Oct. 17 2018, New import to database
        coordinates_sensor = self.add_sensor_to_db(SensorType.GPS, 'Coordinates', 'AppleWatch', 'Wrist',
                                                   sample_rate, 1)
        coordinates_channel = self.add_channel_to_db(coordinates_sensor, Units.NONE, DataFormat.UINT8, 'Coordinates')

        for timestamp in coordinates:
            print('coordinates', timestamp, len(coordinates[timestamp]['times']),
                  len(coordinates[timestamp]['values']))

            # Create time array as float64
            timesarray = np.asarray(coordinates[timestamp]['times'], dtype=np.float64)

            if len(timesarray) is 0:
                print('Empty data, returning')
                return

            # Other values are float32
            valuesarray = np.asarray(coordinates[timestamp]['values'], dtype=np.float32)

            # Create one entry per timestamp ?
            # Could we store a vector instead ?
            for i in range(0, len(valuesarray)):
                # Build gps data
                geo = GPSGeodetic()
                geo.latitude = valuesarray[i][0] * 1e7
                geo.longitude = valuesarray[i][1] * 1e7

                # Create sensor timestamps first
                sensor_timestamps = SensorTimestamps()
                sensor_timestamps.timestamps = timesarray[i:i+1]
                sensor_timestamps.update_timestamps()

                # Calculate recordset
                recordset = self.get_recordset(sensor_timestamps.start_timestamp.timestamp())

                # Update timestamps in recordset
                # This should not happen, recordset is initialized at the beginning of the hour
                if sensor_timestamps.start_timestamp < recordset.start_timestamp:
                    recordset.start_timestamp = sensor_timestamps.start_timestamp
                # This can occur though
                if sensor_timestamps.end_timestamp > recordset.end_timestamp:
                    recordset.end_timestamp = sensor_timestamps.end_timestamp

                # Store
                self.add_sensor_data_to_db(recordset, coordinates_sensor, coordinates_channel,
                                           sensor_timestamps, geo)

    def import_sensoria_to_database(self, sample_rate, sensoria: dict):
        # DL Oct. 17 2018, New import to database
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
                                                            DataFormat.FLOAT32, 'META-1'))
        sensoria_fsr_channels.append(self.add_channel_to_db(sensoria_fsr_sensor, Units.NONE,
                                                            DataFormat.FLOAT32, 'META-5'))
        sensoria_fsr_channels.append(self.add_channel_to_db(sensoria_fsr_sensor, Units.NONE,
                                                            DataFormat.FLOAT32, 'HEEL'))
        for timestamp in sensoria:
            print('sensoria', timestamp, len(sensoria[timestamp]['times']),
                  len(sensoria[timestamp]['values']))

            # Calculate recordset
            recordset = self.get_recordset(timestamp.timestamp())

            # Create time array as float64
            timesarray = np.asarray(sensoria[timestamp]['times'], dtype=np.float64)

            if len(timesarray) is 0:
                print('Empty data, returning')
                return

            # Other values are float32
            valuesarray = np.asarray(sensoria[timestamp]['values'], dtype=np.float32)

            # Create sensor timestamps first
            sensor_timestamps = SensorTimestamps()
            sensor_timestamps.timestamps = timesarray
            sensor_timestamps.update_timestamps()

            # Update timestamps in recordset
            # This should not happen, recordset is initialized at the beginning of the hour
            if sensor_timestamps.start_timestamp < recordset.start_timestamp:
                recordset.start_timestamp = sensor_timestamps.start_timestamp
            # This can occur though
            if sensor_timestamps.end_timestamp > recordset.end_timestamp:
                recordset.end_timestamp = sensor_timestamps.end_timestamp

            # Store FSR
            for i in range(len(sensoria_fsr_channels)):
                self.add_sensor_data_to_db(recordset, sensoria_fsr_sensor, sensoria_fsr_channels[i],
                                           sensor_timestamps,
                                           valuesarray[:, i + 1])

            # Store Acc
            for i in range(len(sensoria_acc_channels)):
                self.add_sensor_data_to_db(recordset, sensoria_acc_sensor, sensoria_acc_channels[i],
                                           sensor_timestamps,
                                           valuesarray[:, i + 4])

            # Store Gyro
            for i in range(len(sensoria_gyro_channels)):
                self.add_sensor_data_to_db(recordset, sensoria_gyro_sensor, sensoria_gyro_channels[i],
                                           sensor_timestamps,
                                           valuesarray[:, i + 7])

            # Magneto
            for i in range(len(sensoria_mag_channels)):
                self.add_sensor_data_to_db(recordset, sensoria_mag_sensor, sensoria_mag_channels[i],
                                           sensor_timestamps,
                                           valuesarray[:, i + 10])

    def import_beacons_to_database(self, sample_rate, beacons: dict):
        # DL Oct. 17 2018, New import to database
        beacons_sensor = self.add_sensor_to_db(SensorType.BEACON, 'Beacons', 'Kontact', 'Environment',
                                               sample_rate, 1)
        channel_values = dict()

        # Data is already hour-aligned iterate through hours
        for timestamp in beacons:
            print('beacons', timestamp, len(beacons[timestamp]['times']),
                  len(beacons[timestamp]['values']))

            # Create time array as float64
            timesarray = np.asarray(beacons[timestamp]['times'], dtype=np.float64)

            if len(timesarray) is 0:
                print('Empty data, returning')
                return

            # Other values are int8
            valuesarray = np.asarray(beacons[timestamp]['values'], dtype=np.int8)

            # Iterate through each entry to generate data for each beacon_id
            for i in range(0, len(timesarray)):
                name = [str(format(x, 'x')).rjust(2, '0') for x in beacons[timestamp]['values'][i][0:16]]
                beacon_id = ''.join(name[0:10]) + '_' + ''.join(name[10:])

                # Create channel if it does not exist
                if not channel_values.__contains__(beacon_id):
                    channel_values[beacon_id] = []

                channel_values[beacon_id].append((timesarray[i], valuesarray[i][14], valuesarray[i][15]))

            # Store each beacon_id in separate channels
            for key in channel_values:
                timevect = np.asarray([x[0] for x in channel_values[key]], dtype=np.float64)

                # Create sensor timestamps first
                sensor_timestamps = SensorTimestamps()
                sensor_timestamps.timestamps = timevect
                sensor_timestamps.update_timestamps()

                # Calculate recordset
                recordset = self.get_recordset(sensor_timestamps.start_timestamp.timestamp())

                # Update timestamps in recordset
                # This should not happen, recordset is initialized at the beginning of the hour
                if sensor_timestamps.start_timestamp < recordset.start_timestamp:
                    recordset.start_timestamp = sensor_timestamps.start_timestamp
                # This can occur though
                if sensor_timestamps.end_timestamp > recordset.end_timestamp:
                    recordset.end_timestamp = sensor_timestamps.end_timestamp

                # Create channel
                channel_txPower = self.add_channel_to_db(beacons_sensor, Units.NONE,
                                                 DataFormat.SINT8, key + '_TxPower')

                channel_RSSI = self.add_channel_to_db(beacons_sensor, Units.NONE,
                                                         DataFormat.SINT8, key + '_RSSI')

                tx_power_vect = np.asarray([x[1] for x in channel_values[key]], dtype=np.int8)
                rssi_vect = np.asarray([x[2] for x in channel_values[key]], dtype=np.int8)

                # Add data
                self.add_sensor_data_to_db(recordset, beacons_sensor, channel_txPower,
                                           sensor_timestamps, tx_power_vect)

                self.add_sensor_data_to_db(recordset, beacons_sensor, channel_RSSI,
                                           sensor_timestamps, rssi_vect)

    def import_motion_to_database(self, sampling_rate, motion: dict):
        # DL Oct. 16 2018, New import to database

        # Create channels and sensors
        accelerometer_sensor = self.add_sensor_to_db(SensorType.ACCELEROMETER, 'Accelerometer',
                                                     'AppleWatch',
                                                     'Wrist',
                                                     sampling_rate, 1)

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
                                            'Wrist', sampling_rate, 1)

        gyro_channels = list()

        # Create channels
        gyro_channels.append(self.add_channel_to_db(gyro_sensor, Units.DEG_PER_SEC,
                                                    DataFormat.FLOAT32, 'Gyro_X'))

        gyro_channels.append(self.add_channel_to_db(gyro_sensor, Units.DEG_PER_SEC,
                                                    DataFormat.FLOAT32, 'Gyro_Y'))

        gyro_channels.append(self.add_channel_to_db(gyro_sensor, Units.DEG_PER_SEC,
                                                    DataFormat.FLOAT32, 'Gyro_Z'))

        # Data is already hour-aligned iterate through hours
        for timestamp in motion:
            print('motion', timestamp, len(motion[timestamp]['times']),
                  len(motion[timestamp]['values']))

            # Calculate recordset
            recordset = self.get_recordset(timestamp.timestamp())

            # Add motion data to database

            # Create time array as float64
            timesarray = np.asarray(motion[timestamp]['times'], dtype=np.float64)

            if len(timesarray) is 0:
                print('Empty data, returning')
                return

            # Other values are float32
            valuesarray = np.asarray(motion[timestamp]['values'], dtype=np.float32)

            # Motion contains in this order
            # acceleration(x, y, z)
            # gravity vector(x, y, z)
            # gyroscope(x, y, z)
            # attitude quaternion(w, x, y, z)

            # Create sensor timestamps first
            sensor_timestamps = SensorTimestamps()
            sensor_timestamps.timestamps = timesarray
            sensor_timestamps.update_timestamps()

            # Update timestamps in recordset
            # This should not happen, recordset is initialized at the beginning of the hour
            if sensor_timestamps.start_timestamp < recordset.start_timestamp:
                recordset.start_timestamp = sensor_timestamps.start_timestamp
            # This can occur though
            if sensor_timestamps.end_timestamp > recordset.end_timestamp:
                recordset.end_timestamp = sensor_timestamps.end_timestamp

            # Acc
            for i in range(len(accelerometer_channels)):
                self.add_sensor_data_to_db(recordset, accelerometer_sensor, accelerometer_channels[i],
                                           sensor_timestamps, valuesarray[:, i])

            # Gyro
            for i in range(len(gyro_channels)):
                self.add_sensor_data_to_db(recordset, gyro_sensor, gyro_channels[i],
                                           sensor_timestamps, valuesarray[:, i + 6])

    def import_battery_to_database(self, sampling_rate, battery: dict):
        # DL Oct. 16 2018, New import to database
        battery_sensor = self.add_sensor_to_db(SensorType.BATTERY, 'Battery', 'AppleWatch', 'Wrist',
                                               sampling_rate, 1)

        battery_channel = self.add_channel_to_db(battery_sensor, Units.VOLTS, DataFormat.FLOAT32, 'Battery Percentage')

        # Data is already hour-aligned iterate through hours
        for timestamp in battery:
            print('battery', timestamp, len(battery[timestamp]['times']),
                  len(battery[timestamp]['values']))

            # Calculate recordset
            recordset = self.get_recordset(timestamp.timestamp())

            # Import to database
            # Create time array as float64
            timesarray = np.asarray(battery[timestamp]['times'], dtype=np.float64)

            if len(timesarray) is 0:
                print('Empty data, returning')
                return

            # Other values are float32
            valuesarray = np.asarray(battery[timestamp]['values'], dtype=np.float32)

            # Create sensor timestamps first
            sensor_timestamps = SensorTimestamps()
            sensor_timestamps.timestamps = timesarray
            sensor_timestamps.update_timestamps()

            # Update timestamps in recordset
            # This should not happen, recordset is initialized at the beginning of the hour
            if sensor_timestamps.start_timestamp < recordset.start_timestamp:
                recordset.start_timestamp = sensor_timestamps.start_timestamp
            # This can occur though
            if sensor_timestamps.end_timestamp > recordset.end_timestamp:
                recordset.end_timestamp = sensor_timestamps.end_timestamp

            self.add_sensor_data_to_db(recordset, battery_sensor, battery_channel, sensor_timestamps,
                                       valuesarray[:, 0])

    def import_to_database(self, results):
        # DL Oct. 16 2018, New import to database
        if results.__contains__('motion'):
            sampling_rate = results['motion']['sampling_rate']
            if results['motion']['timestamps']:
                self.import_motion_to_database(sampling_rate, results['motion']['timestamps'])

        if results.__contains__('battery'):
            sampling_rate = results['battery']['sampling_rate']
            if results['battery']['timestamps']:
                self.import_battery_to_database(sampling_rate, results['battery']['timestamps'])

        if results.__contains__('sensoria'):
            sampling_rate = results['sensoria']['sampling_rate']
            if results['sensoria']['timestamps']:
                self.import_sensoria_to_database(sampling_rate, results['sensoria']['timestamps'])

        if results.__contains__('heartrate'):
            sampling_rate = results['heartrate']['sampling_rate']
            if results['heartrate']['timestamps']:
                self.import_heartrate_to_database(sampling_rate, results['heartrate']['timestamps'])

        if results.__contains__('beacons'):
            sampling_rate = results['beacons']['sampling_rate']
            if results['beacons']['timestamps']:
                self.import_beacons_to_database(sampling_rate, results['beacons']['timestamps'])

        if results.__contains__('coordinates'):
            sampling_rate = results['coordinates']['sampling_rate']
            if results['coordinates']['timestamps']:
                self.import_coordinates_to_database(sampling_rate, results['coordinates']['timestamps'])

        if results.__contains__('raw_motion'):
            sampling_rate = results['raw_motion']['sampling_rate']
            if results['raw_motion']['timestamps']:
                # TODO
                pass

        if results.__contains__('raw_accelero'):
            sampling_rate = results['raw_accelero']['sampling_rate']
            if results['raw_accelero']['timestamps']:
                # TODO
                pass

        if results.__contains__('raw_gyro'):
            sampling_rate = results['raw_gyro']['sampling_rate']
            if results['raw_gyro']['timestamps']:
                # TODO
                pass

        # Commit DB
        self.db.commit()

    def import_to_database_old(self, result):
        print('AppleWatchImporter.import_to_database')
        sensors = {}
        channels = {}

        if result is None:
            return

        # Create sensors
        if result['sampling_rate'].__contains__(self.PROCESSED_MOTION_ID):
            accelerometer_sensor = self.add_sensor_to_db(SensorType.ACCELEROMETER, 'Accelerometer',
                                                         'AppleWatch',
                                                         'Unknown', result['sampling_rate'][self.PROCESSED_MOTION_ID], 1)

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
                                                'Unknown', result['sampling_rate'][self.PROCESSED_MOTION_ID], 1)

            gyro_channels = list()

            # Create channels
            gyro_channels.append(self.add_channel_to_db(gyro_sensor, Units.DEG_PER_SEC,
                                                        DataFormat.FLOAT32, 'Gyro_X'))

            gyro_channels.append(self.add_channel_to_db(gyro_sensor, Units.DEG_PER_SEC,
                                                        DataFormat.FLOAT32, 'Gyro_Y'))

            gyro_channels.append(self.add_channel_to_db(gyro_sensor, Units.DEG_PER_SEC,
                                                        DataFormat.FLOAT32, 'Gyro_Z'))

            sensors['acc'] = accelerometer_sensor
            sensors['gyro'] = gyro_sensor
            channels['acc'] = accelerometer_channels
            channels['gyro'] = gyro_channels

        # Battery
        if result['sampling_rate'].__contains__(self.BATTERY_ID):
            battery_sensor = self.add_sensor_to_db(SensorType.BATTERY, 'Battery', 'AppleWatch', 'Unknown', result['sampling_rate'][self.BATTERY_ID], 1)
            battery_channel = self.add_channel_to_db(battery_sensor, Units.VOLTS, DataFormat.FLOAT32, 'Battery Percentage')
            sensors['batt'] = battery_sensor
            channels['batt'] = battery_channel

        # Heartrate
        if result['sampling_rate'].__contains__(self.HEARTRATE_ID):
            heartrate_sensor = self.add_sensor_to_db(SensorType.HEARTRATE, 'Heartrate', 'AppleWatch', 'Unknown', result['sampling_rate'][self.HEARTRATE_ID], 1)
            heartrate_channel = self.add_channel_to_db(heartrate_sensor, Units.BPM, DataFormat.FLOAT32, 'Heartrate')
            sensors['heartrate'] = heartrate_sensor
            channels['heartrate'] = heartrate_channel

        # Coordinates
        if result['sampling_rate'].__contains__(self.COORDINATES_ID):
            coordinates_sensor = self.add_sensor_to_db(SensorType.GPS, 'Coordinates', 'AppleWatch', 'Unknown', result['sampling_rate'][self.COORDINATES_ID], 1)
            coordinates_channel = self.add_channel_to_db(coordinates_sensor, Units.NONE, DataFormat.UINT8, 'Coordinates')
            sensors['coordinates'] = coordinates_sensor
            channels['coordinates'] = coordinates_channel

        # Sensoria
        if result['sampling_rate'].__contains__(self.SENSORIA_ID):
            sensoria_acc_sensor = self.add_sensor_to_db(SensorType.ACCELEROMETER, 'Accelerometer', 'Sensoria', 'Foot',
                                                        result['sampling_rate'][self.SENSORIA_ID], 1)

            sensoria_acc_channels = list()
            sensoria_acc_channels.append(self.add_channel_to_db(sensoria_acc_sensor, Units.GRAVITY_G,
                                                                DataFormat.FLOAT32, 'Accelerometer_X'))
            sensoria_acc_channels.append(self.add_channel_to_db(sensoria_acc_sensor, Units.GRAVITY_G,
                                                                DataFormat.FLOAT32, 'Accelerometer_Y'))
            sensoria_acc_channels.append(self.add_channel_to_db(sensoria_acc_sensor, Units.GRAVITY_G,
                                                                DataFormat.FLOAT32, 'Accelerometer_Z'))

            sensoria_gyro_sensor = self.add_sensor_to_db(SensorType.GYROMETER, 'Gyrometer', 'Sensoria', 'Foot',
                                                         result['sampling_rate'][self.SENSORIA_ID], 1)
            sensoria_gyro_channels = list()
            sensoria_gyro_channels.append(self.add_channel_to_db(sensoria_gyro_sensor, Units.DEG_PER_SEC,
                                                                 DataFormat.FLOAT32, 'Gyro_X'))
            sensoria_gyro_channels.append(self.add_channel_to_db(sensoria_gyro_sensor, Units.DEG_PER_SEC,
                                                                 DataFormat.FLOAT32, 'Gyro_Y'))
            sensoria_gyro_channels.append(self.add_channel_to_db(sensoria_gyro_sensor, Units.DEG_PER_SEC,
                                                                 DataFormat.FLOAT32, 'Gyro_Z'))

            sensoria_mag_sensor = self.add_sensor_to_db(SensorType.MAGNETOMETER, 'Magnetometer', 'Sensoria', 'Foot',
                                                        result['sampling_rate'][self.SENSORIA_ID], 1)
            sensoria_mag_channels = list()
            sensoria_mag_channels.append(self.add_channel_to_db(sensoria_mag_sensor, Units.GAUSS,
                                                                DataFormat.FLOAT32, 'Mag_X'))
            sensoria_mag_channels.append(self.add_channel_to_db(sensoria_mag_sensor, Units.GAUSS,
                                                                DataFormat.FLOAT32, 'Mag_Y'))
            sensoria_mag_channels.append(self.add_channel_to_db(sensoria_mag_sensor, Units.GAUSS,
                                                                DataFormat.FLOAT32, 'Mag_Z'))

            sensoria_fsr_sensor = self.add_sensor_to_db(SensorType.FSR, 'FSR', 'Sensoria', 'Foot',
                                                        result['sampling_rate'][self.SENSORIA_ID], 1)
            sensoria_fsr_channels = list()
            sensoria_fsr_channels.append(self.add_channel_to_db(sensoria_fsr_sensor, Units.NONE,
                                                                DataFormat.SINT16, 'META-1'))
            sensoria_fsr_channels.append(self.add_channel_to_db(sensoria_fsr_sensor, Units.NONE,
                                                                DataFormat.SINT16, 'META-5'))
            sensoria_fsr_channels.append(self.add_channel_to_db(sensoria_fsr_sensor, Units.NONE,
                                                                DataFormat.SINT16, 'HEEL'))

            sensors['sensoria_acc'] = sensoria_acc_sensor
            sensors['sensoria_gyro'] = sensoria_gyro_sensor
            sensors['sensoria_mag'] = sensoria_mag_sensor
            sensors['sensoria_fsr'] = sensoria_fsr_sensor
            channels['sensoria_acc'] = sensoria_acc_channels
            channels['sensoria_gyro'] = sensoria_gyro_channels
            channels['sensoria_mag'] = sensoria_mag_channels
            channels['sensoria_fsr'] = sensoria_fsr_channels

        #Beacons
        if result['sampling_rate'].__contains__(self.BEACONS_ID):
            beacons_sensor = self.add_sensor_to_db(SensorType.BEACON, 'Beacons', 'Kontact', 'Environment', result['sampling_rate'][self.BEACONS_ID], 1)
            beacons_channels = list()
            sensors['beacons'] = beacons_sensor
            channels['beacons'] = beacons_channels

        # Raw Motion
        if result['sampling_rate'].__contains__(self.RAW_MOTION_ID):
            raw_accelerometer_sensor = self.add_sensor_to_db(SensorType.ACCELEROMETER, 'Raw Accelerometer',
                                                             'AppleWatch',
                                                             'Unknown', result['sampling_rate'][self.RAW_MOTION_ID], 1)

            raw_accelerometer_channels = list()

            # Create channels
            raw_accelerometer_channels.append(self.add_channel_to_db(raw_accelerometer_sensor, Units.GRAVITY_G,
                                                                     DataFormat.FLOAT32, 'Accelerometer_X'))

            raw_accelerometer_channels.append(self.add_channel_to_db(raw_accelerometer_sensor, Units.GRAVITY_G,
                                                                     DataFormat.FLOAT32, 'Accelerometer_Y'))

            raw_accelerometer_channels.append(self.add_channel_to_db(raw_accelerometer_sensor, Units.GRAVITY_G,
                                                                     DataFormat.FLOAT32, 'Accelerometer_Z'))

            # Create sensor
            raw_gyro_sensor = self.add_sensor_to_db(SensorType.GYROMETER, 'Raw Gyro',
                                                    'AppleWatch',
                                                    'Unknown', result['sampling_rate'][self.RAW_MOTION_ID], 1)

            raw_gyro_channels = list()

            # Create channels
            raw_gyro_channels.append(self.add_channel_to_db(raw_gyro_sensor, Units.DEG_PER_SEC,
                                                            DataFormat.FLOAT32, 'Gyro_X'))

            raw_gyro_channels.append(self.add_channel_to_db(raw_gyro_sensor, Units.DEG_PER_SEC,
                                                            DataFormat.FLOAT32, 'Gyro_Y'))

            raw_gyro_channels.append(self.add_channel_to_db(raw_gyro_sensor, Units.DEG_PER_SEC,
                                                            DataFormat.FLOAT32, 'Gyro_Z'))

            sensors['raw_acc'] = raw_accelerometer_sensor
            sensors['raw_gyro'] = raw_gyro_sensor
            channels['raw_acc'] = raw_accelerometer_channels
            channels['raw_gyro'] = raw_gyro_channels

        if result['sampling_rate'].__contains__(self.RAW_ACCELERO_ID):

            raw_accelerometer_sensor = self.add_sensor_to_db(SensorType.ACCELEROMETER, 'Raw Accelerometer',
                                                             'AppleWatch',
                                                             'Unknown', result['sampling_rate'][self.RAW_ACCELERO_ID], 1)

            raw_accelerometer_channels = list()

            # Create channels
            raw_accelerometer_channels.append(self.add_channel_to_db(raw_accelerometer_sensor, Units.GRAVITY_G,
                                                                     DataFormat.FLOAT32, 'Accelerometer_X'))

            raw_accelerometer_channels.append(self.add_channel_to_db(raw_accelerometer_sensor, Units.GRAVITY_G,
                                                                     DataFormat.FLOAT32, 'Accelerometer_Y'))

            raw_accelerometer_channels.append(self.add_channel_to_db(raw_accelerometer_sensor, Units.GRAVITY_G,
                                                                     DataFormat.FLOAT32, 'Accelerometer_Z'))

            sensors['raw_acc'] = raw_accelerometer_sensor
            channels['raw_acc'] = raw_accelerometer_channels

        if result['sampling_rate'].__contains__(self.RAW_GYRO_ID):
            # Create sensor
            raw_gyro_sensor = self.add_sensor_to_db(SensorType.GYROMETER, 'Raw Gyro',
                                                 'AppleWatch',
                                                 'Unknown', result['sampling_rate'][self.RAW_GYRO_ID], 1)

            raw_gyro_channels = list()

            # Create channels
            raw_gyro_channels.append(self.add_channel_to_db(raw_gyro_sensor, Units.DEG_PER_SEC,
                                                         DataFormat.FLOAT32, 'Gyro_X'))

            raw_gyro_channels.append(self.add_channel_to_db(raw_gyro_sensor, Units.DEG_PER_SEC,
                                                         DataFormat.FLOAT32, 'Gyro_Y'))

            raw_gyro_channels.append(self.add_channel_to_db(raw_gyro_sensor, Units.DEG_PER_SEC,
                                                                 DataFormat.FLOAT32, 'Gyro_Z'))

            sensors['raw_gyro'] = raw_gyro_sensor
            channels['raw_gyro'] = raw_gyro_channels

        # Create sensor and channels dict
        """sensors = {'acc': accelerometer_sensor,
                   'gyro': gyro_sensor,
                   'batt': battery_sensor,
                   'heartrate': heartrate_sensor,
                   'coordinates': coordinates_sensor,
                   'sensoria_acc': sensoria_acc_sensor,
                   'sensoria_gyro': sensoria_gyro_sensor,
                   'sensoria_mag': sensoria_mag_sensor,
                   'sensoria_fsr': sensoria_fsr_sensor,
                   'beacons': beacons_sensor,
                   'raw_acc': raw_accelerometer_sensor,
                   'raw_gyro': raw_gyro_sensor
                   }

        channels = {'acc': accelerometer_channels,
                    'gyro': gyro_channels,
                    'batt': battery_channel,
                    'heartrate': heartrate_channel,
                    'coordinates': coordinates_channel,
                    'sensoria_acc': sensoria_acc_channels,
                    'sensoria_gyro': sensoria_gyro_channels,
                    'sensoria_mag': sensoria_mag_channels,
                    'sensoria_fsr': sensoria_fsr_channels,
                    'beacons': beacons_channels,
                    'raw_acc': raw_accelerometer_channels,
                    'raw_gyro': raw_gyro_channels
                    }
        """
        for timestamp in result:
            # Change recordset each day
            recordset = self.get_recordset(timestamp)

            if recordset is None:
                continue

            if result[timestamp].__contains__('battery'):
                # print('battery')
                if result[timestamp]['battery']:
                    self.import_battery_to_database(result['sampling_rate'][self.BATTERY_ID], timestamp, recordset, sensors, channels,
                                                result[timestamp]['battery'])
                    if len(result[timestamp]['battery']) != result['sampling_rate'][self.BATTERY_ID]:
                        print(timestamp, ' WARNING Battery does not fit sampling rate : ',
                              len(result[timestamp]['battery']), ' != ',
                              result['sampling_rate'][self.BATTERY_ID])

            if result[timestamp].__contains__('beacons'):
                # print('beacons')
                if result[timestamp]['beacons']:
                    self.import_beacons_to_database(result['sampling_rate'][self.BEACONS_ID], timestamp, recordset, sensors, channels,
                                                    result[timestamp]['beacons'])
                    if len(result[timestamp]['beacons']) != result['sampling_rate'][self.BEACONS_ID]:
                        print(timestamp, ' WARNING Beacons does not fit sampling rate : ',
                              len(result[timestamp]['beacons']), ' != ',
                              result['sampling_rate'][self.BEACONS_ID])

            if result[timestamp].__contains__('sensoria'):
                # print('sensoria')
                if result[timestamp]['sensoria']:
                    self.import_sensoria_to_database(result['sampling_rate'][self.SENSORIA_ID], timestamp, recordset, sensors, channels,
                                                     result[timestamp]['sensoria'])
                    if len(result[timestamp]['sensoria']) != result['sampling_rate'][self.SENSORIA_ID]:
                        print(timestamp, ' WARNING Sensoria does not fit sampling rate : ',
                              len(result[timestamp]['sensoria']), ' != ',
                              result['sampling_rate'][self.SENSORIA_ID])

            if result[timestamp].__contains__('heartrate'):
                # print('heartrate')
                if result[timestamp]['heartrate']:
                    self.import_heartrate_to_database(result['sampling_rate'][self.HEARTRATE_ID], timestamp, recordset, sensors, channels,
                                                      result[timestamp]['heartrate'])
                    if len(result[timestamp]['heartrate']) != result['sampling_rate'][self.HEARTRATE_ID]:
                        print(timestamp, ' WARNING Heartrate does not fit sampling rate : ',
                              len(result[timestamp]['heartrate']), ' != ',
                              result['sampling_rate'][self.HEARTRATE_ID])

            if result[timestamp].__contains__('motion'):
                # print('motion')
                if result[timestamp]['motion']:
                    self.import_motion_to_database(result['sampling_rate'][self.PROCESSED_MOTION_ID], timestamp, recordset, sensors, channels,
                                                   result[timestamp]['motion'])
                    if len(result[timestamp]['motion']) != result['sampling_rate'][self.PROCESSED_MOTION_ID]:
                        print(timestamp, ' WARNING Processed motion does not fit sampling rate : ',
                              len(result[timestamp]['motion']), ' != ',
                              result['sampling_rate'][self.PROCESSED_MOTION_ID])

            if result[timestamp].__contains__('coordinates'):
                # print('coordinates')
                if result[timestamp]['coordinates']:
                    self.import_coordinates_to_database(result['sampling_rate'][self.COORDINATES_ID], timestamp, recordset, sensors, channels,
                                                        result[timestamp]['coordinates'])

                    if len(result[timestamp]['coordinates']) != result['sampling_rate'][self.COORDINATES_ID]:
                        print(timestamp, ' WARNING Coordinates does not fit sampling rate : ',
                              len(result[timestamp]['coordinates']), ' != ',
                              result['sampling_rate'][self.COORDINATES_ID])

            if result[timestamp].__contains__('raw_motion'):
                if result[timestamp]['raw_motion']:
                    self.import_raw_motion_to_database(result['sampling_rate'][self.RAW_MOTION_ID], timestamp, recordset, sensors, channels,
                                                       result[timestamp]['raw_motion'])

            if result[timestamp].__contains__('raw_accelero'):
                if result[timestamp]['raw_accelero']:
                    self.import_raw_accelerometer_to_database(result['sampling_rate'][self.RAW_ACCELERO_ID], timestamp, recordset, sensors, channels,
                                                       result[timestamp]['raw_accelero'])

            if result[timestamp].__contains__('raw_gyro'):
                if result[timestamp]['raw_gyro']:
                    self.import_raw_gyro_to_database(result['sampling_rate'][self.RAW_GYRO_ID], timestamp, recordset, sensors, channels,
                                                       result[timestamp]['raw_gyro'])

        # Commit to DB
        self.db.commit()

    def get_sampling_rate_from_header(self, sensor_id, header): #header = string of json
        sample_rate = 0
        if header != "":
            json_settings = json.loads(header) # converts to json
        else:
            return sample_rate

        if sensor_id == self.BATTERY_ID:
            sample_rate = 1 / 3  # Default value (if file version = 1)
            # Sampling rate
            if header != "":
                interval = json_settings.get('check_interval')
                if interval:
                    sample_rate = 1 / interval

        if sensor_id == self.COORDINATES_ID:
            sample_rate = 1 / 10  # Default value (if file version = 1)
            # Sampling rate
            if header != "":
                interval = json_settings.get('period')
                if interval:
                    sample_rate = 1 / interval

        if sensor_id in [self.RAW_MOTION_ID, self.PROCESSED_MOTION_ID, self.RAW_ACCELERO_ID, self.RAW_GYRO_ID]:
            sample_rate = 50
            interval = json_settings.get('frequency')
            if interval:
                sample_rate = interval

        if sensor_id == self.HEARTRATE_ID:
            sample_rate = 1 / 3  # Default value (if file version = 1)
            # Sampling rate
            if header != "":
                interval = json_settings.get('sampling_interval')
                if interval:
                    sample_rate = 1 / interval

        if sensor_id == self.BEACONS_ID:
            sample_rate = 1 #No sampling rate in beacons config

        if sensor_id == self.SENSORIA_ID:
            sample_rate = json_settings.get('frequency')

        return sample_rate

    def readDataFile(self, file, debug=False):
        """
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
        """

        results = {}

        # results['sampling_rate'] = {}

        settings_json_str = ""

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

        # Get correct sample_rate for data
        # results['sampling_rate'][sensor_id] = self.get_sampling_rate_from_header(sensor_id, settings_json_str)
        # print('sampling rate for sensor_id', sensor_id, ' : ', results['sampling_rate'][sensor_id])

        # prepare for loop by finding right sensor info
        dict_name = ""
        if sensor_id == self.BATTERY_ID:
            read_data_func = self.read_battery_data
            dict_name = "battery"
        elif sensor_id == self.SENSORIA_ID:
            # Sensoria format changed from v1 to v2...
            dict_name = 'sensoria'
            if version == 2:
                read_data_func = self.read_sensoria_data
            else:
                read_data_func = None
        elif sensor_id == self.HEARTRATE_ID:
            read_data_func = self.read_heartrate_data
            dict_name = 'heartrate'
        elif sensor_id == self.PROCESSED_MOTION_ID:
            read_data_func = self.read_motion_data
            dict_name = 'motion'
        elif sensor_id == self.BEACONS_ID:
            read_data_func = self.read_beacons_data
            dict_name = 'beacons'
        elif sensor_id == self.COORDINATES_ID:
            read_data_func = self.read_coordinates_data
            dict_name = 'coordinates'
        # deprecated
        elif sensor_id == self.RAW_MOTION_ID:
            read_data_func = self.read_raw_motion_data
            dict_name = 'raw_motion'
        elif sensor_id == self.RAW_ACCELERO_ID:
            read_data_func = self.read_raw_accelerometer_data
            dict_name = 'raw_accelero'
        elif sensor_id == self.RAW_GYRO_ID:
            read_data_func = self.read_raw_gyro_data
            dict_name = 'raw_gyro'
        else:
            print("unknown sensor_id: ", hex(sensor_id))
            return None

        # DL 16 oct. 2018. New format for results. Will keep all timestamps and group them by hour
        results[dict_name] = {}

        results[dict_name]['timestamps'] = {}

        # Insert sampling rate information
        results[dict_name]['sampling_rate'] = self.get_sampling_rate_from_header(sensor_id, settings_json_str)

        # lists of co-dependant timestamp(ms) and data
        results_ms_ts = []
        results_ms_data = []

        # read the whole file
        try:
            while file.readable() and read_data_func is not None:
                # Read timestamp
                [timestamp_ms] = struct.unpack("<Q", file.read(8))

                results_ms_ts.append(timestamp_ms)
                results_ms_data.append(read_data_func(file, debug))

        except:
            # let's hope it's only eof...
            # Make sure data vectors are of the same size
            min_size = min(len(results_ms_ts), len(results_ms_data))
            results_ms_ts = results_ms_ts[0:min_size]
            results_ms_data = results_ms_data[0:min_size]

        # insertion sort on almost sorted timestamps, tends to O(n)
        for i in range(1, len(results_ms_ts)):
            curr_ts = results_ms_ts[i]
            curr_data = results_ms_data[i]
            j = i - 1
            # compare timestamps
            while j >= 0 and curr_ts < results_ms_ts[j]:
                # drift up and continue looking
                results_ms_ts[j+1] = results_ms_ts[j]
                results_ms_data[j+1] = results_ms_data[j]
                j -= 1
            # only replace if needed
            if j != i - 1:
                results_ms_ts[j+1] = curr_ts
                results_ms_data[j+1] = curr_data

        # Create hour-aligned separated data
        for i in range(0, len(results_ms_ts)):
            hour_lower_limit_sec = np.floor(results_ms_ts[i] / 3600000) * 3600
            mydate = datetime.datetime.utcfromtimestamp(hour_lower_limit_sec)

            # Create hour entry if it does not exist
            if not results[dict_name]['timestamps'].__contains__(mydate):
                results[dict_name]['timestamps'][mydate] = {'times': [], 'values': []}

            # Append data (slow?)
            # ms time to secs
            results[dict_name]['timestamps'][mydate]['times'].append(results_ms_ts[i] / 1000.0)
            # data
            results[dict_name]['timestamps'][mydate]['values'].append(results_ms_data[i])

        print('done processing: ', dict_name)

        # force the gc to clear temporary lists
        results_ms_ts.clear()
        results_ms_data.clear()
        gc.collect()

        return results

    def read_battery_data(self, file, debug=False):
        """
        • Byte integer for battery level between 0 and 100 (percent)
        ◦ 0 meaning invalid level (eg. where state is .unknown)
        • Byte for battery state
        ◦ unknown: 0
        ◦ unplugged: 1
        ◦ charging: 2
        ◦ full: 3
        :return:
        """
        chunk = file.read(2)
        data = struct.unpack("BB", chunk)
        if debug:
            print('BATTERY: ', data)
        return data

    def read_sensoria_data(self, file, debug=False):
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
        chunk = file.read(46)
        data = struct.unpack("<1i3h9f", chunk)
        if debug:
            print('SENSORIA: ', data)
        return data

    def read_heartrate_data(self, file, debug=False):
        """
        unsigned integer as single Byte for bpm
        ** assumes that bpm cannot go above 255, hence values above are clamped to 255
        :param chunk:
        :return:
        """
        chunk = file.read(1)
        data = struct.unpack("<B", chunk)
        if debug:
            print('HEARTRATE: ', data)
        return data

    def read_motion_data(self, file, debug=False):
        """
         13 Float32 values, hence 52 bytes, with following fields
        • acceleration (x,y,z)
        • gravity vector (x,y,z)
        • gyroscope (x,y,z)
        • attitude quaternion (w,x,y,z)
            """
        chunk = file.read(52)
        data = struct.unpack("<13f", chunk)
        if debug:
            print('MOTION: ', data)
        return data

    def read_beacons_data(self, file, debug=False):
        """
        10 Bytes Char for namespace
        6 Bytes Char for instance ID
        1 Int8 for TxPower
        1 Int8 for RSSI
        :param chunk:
        :return:
        """
        chunk = file.read(18)
        data = struct.unpack("<16B2b", chunk)
        if debug:
            print('BEACONS: ', data)
        return data

    def read_coordinates_data(self, file, debug=False):
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
        chunk = file.read(28)
        data = struct.unpack("<7f", chunk)
        if debug:
            print('COORDINATES: ', data)
        return data

    # deprecated, not used anymore, separated into two files
    def read_raw_motion_data(self, file, debug=False):
        """
         6 Float32 values, hence 24 bytes, with following fields
            acceleration (x,y,z)
            gyroscope (x,y,z)
        """
        chunk = file.read(24)
        data = struct.unpack("<6f", chunk)
        if debug:
            print('RAW MOTION: ', data)
        return data

    def read_raw_accelerometer_data(self, file, debug=False):
        """
         3 Float32 values, hence 12 bytes, with following fields
            acceleration (x,y,z)
        """
        chunk = file.read(12)
        data = struct.unpack("<3f", chunk)
        if debug:
            print('RAW ACCELERO: ', data)
        return data

    def read_raw_gyro_data(self, file, debug=False):
        """
         3 Float32 values, hence 12 bytes, with following fields
            gyroscope (x,y,z)
        """
        chunk = file.read(12)
        data = struct.unpack("<3f", chunk)
        if debug:
            print('RAW GYRO: ', data)
        return data
