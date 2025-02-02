"""

    AppleWatchImporter
    @authors Dominic Létourneau, Simon Brière
    @date 30/05/2018

"""

from libopenimu.importers.BaseImporter import BaseImporter
from libopenimu.models.sensor_types import SensorType
from libopenimu.models.SensorTimestamps import SensorTimestamps
from libopenimu.models.units import Units
from libopenimu.models.data_formats import DataFormat
from libopenimu.db.DBManager import DBManager
from libopenimu.models.Participant import Participant
from libopenimu.importers.wimu import GPSGeodetic

import numpy as np

import datetime
import os
import zipfile
import struct
import json  # For file header config
import gc


# from collections import defaultdict


class AppleWatchImporter(BaseImporter):
    HEADER = 0xEAEA
    BATTERY_ID = 1
    SENSORIA_ID = 2
    HEARTRATE_ID = 3
    PROCESSED_MOTION_ID = 4
    # LOCATION_ID = 5
    BEACONS_ID = 6
    COORDINATES_ID = 7
    RAW_MOTION_ID = 8
    RAW_ACCELERO_ID = 9
    RAW_GYRO_ID = 10
    PEDOMETER_ID = 11
    ACTIVITY_ID = 13
    QUESTION_ID = 14
    HEALTH_ID = 15
    HEADINGS_ID = 16
    RAW_MAGNETO_ID = 17
    TREMOR_ID = 18
    DYSKINETIC_ID = 19

    def __init__(self, manager: DBManager, participant: Participant):
        super().__init__(manager, participant)
        self.last_error = None
        self.session_name = str()
        self.current_file_size = 0
        self.device_id = None

    def load(self, filename: str):
        # print('AppleWatchImporter.load')
        results = []
        # Removed zip loading for now,
        if 'zip' in filename:
            results = self.load_zip(filename)
        else:
            if '.data' in filename:
                with open(filename, "rb") as file:

                    # Look for session information in the same directory
                    basename = os.path.basename(filename)
                    session_file_name = filename.replace(basename, 'session.oimi')

                    # Default session name
                    parts = filename.split(os.path.sep)
                    if len(parts) >= 2:
                        self.session_name = parts[-2]

                    # Use .oimi file if present to properly name the session
                    if os.path.exists(session_file_name):
                        with open(session_file_name, 'r') as session_file:
                            # Read JSON information
                            session_info = json.load(session_file)
                            # TODO better session name?
                            if session_info.__contains__('participant') and session_info.__contains__('timestamp'):
                                self.session_name = session_info['timestamp'] + '_' + session_info['participant']
                            if 'deviceID' in session_info:
                                self.device_id = session_info['deviceID']

                    # print('Loading File: ', filename)
                    self.current_file_size = os.stat(filename).st_size

                    values = self.read_data_file(file)
                    if values is not None:
                        results.append(values)

        # print('results len', len(results))
        return results

    def load_zip(self, filename):
        results = []
        with zipfile.ZipFile(filename) as myzip:
            # print('zip opened')
            namelist = myzip.namelist()

            # Process data files
            for file in namelist:
                if '.data' in file:

                    # Try to extract session information if available
                    basename = os.path.basename(file)
                    session_file_name = file.replace(basename, 'session.oimi')

                    if session_file_name in namelist:
                        session_file = myzip.open(session_file_name)
                        # Read JSON information
                        session_info = json.load(session_file)
                        # TODO better session name?
                        if session_info.__contains__('participant') and session_info.__contains__('timestamp'):
                            self.session_name = session_info['timestamp'] + '_' + session_info['participant']
                        else:
                            # Reset session name
                            self.session_name = str()

                    # print('Reading file: ', file)
                    my_file = myzip.open(file)
                    self.current_file_size = myzip.getinfo(my_file.name).file_size
                    values = self.read_data_file(my_file, False)

                    # Append data
                    if values is not None:
                        results.append(values)

        # Returns an array which each element is the result of the import of one file
        return results

    @staticmethod
    def create_sensor_timestamps(times, recordset):
        # Create sensor timestamps first
        sensor_timestamps = SensorTimestamps()
        sensor_timestamps.timestamps = times
        sensor_timestamps.update_timestamps()

        # Update timestamps in recordset
        # This should not happen, recordset is initialized at the beginning of the hour
        if sensor_timestamps.start_timestamp < recordset.start_timestamp:
            recordset.start_timestamp = sensor_timestamps.start_timestamp
        # This can occur though
        if sensor_timestamps.end_timestamp > recordset.end_timestamp:
            recordset.end_timestamp = sensor_timestamps.end_timestamp

        return sensor_timestamps

    def import_activity_to_database(self, settings: str, activity: dict):
        activity_sensor = self.add_sensor_to_db(SensorType.ACTIVITY, 'Activity', 'AppleWatch', 'Wrist',
                                                0, 1, settings, self.device_id)
        confidence_channel = self.add_channel_to_db(activity_sensor, Units.NONE, DataFormat.UINT8, 'Confidence')
        car_channel = self.add_channel_to_db(activity_sensor, Units.NONE, DataFormat.UINT8, 'Automotive')
        cycle_channel = self.add_channel_to_db(activity_sensor, Units.NONE, DataFormat.UINT8, 'Cycling')
        run_channel = self.add_channel_to_db(activity_sensor, Units.NONE, DataFormat.UINT8, 'Running')
        stat_channel = self.add_channel_to_db(activity_sensor, Units.NONE, DataFormat.UINT8, 'Stationnary')
        walk_channel = self.add_channel_to_db(activity_sensor, Units.NONE, DataFormat.UINT8, 'Walking')
        unknown_channel = self.add_channel_to_db(activity_sensor, Units.NONE, DataFormat.UINT8, 'Unknown')

        count = 0
        for timestamp in activity:
            # Filter invalid timestamp if needed
            if timestamp.year < 2000:
                continue

            # Calculate recordset
            recordset = self.get_recordset(timestamp.timestamp(), session_name=self.session_name)

            # Create time array as float64
            timesarray = np.asarray(activity[timestamp]['times'], dtype=np.float64)

            if len(timesarray) == 0:
                self.last_error = "No temporal data"
                return

            # Create sensor timestamps first
            sensor_timestamps = self.create_sensor_timestamps(timesarray, recordset)

            # All stored into one UInt8 value...
            valuesarray = np.asarray(activity[timestamp]['values'], dtype=np.uint8)

            # Extract values
            mask = np.full(valuesarray.shape, fill_value=0x03, dtype=np.uint8)
            masked = np.bitwise_and(valuesarray, mask)
            self.add_sensor_data_to_db(recordset, activity_sensor, confidence_channel, sensor_timestamps, masked[:, 0])

            mask = np.full(valuesarray.shape, fill_value=0x04, dtype=np.uint8)
            masked = np.right_shift(np.bitwise_and(valuesarray, mask), 2)
            self.add_sensor_data_to_db(recordset, activity_sensor, car_channel, sensor_timestamps, masked[:, 0])

            mask = np.full(valuesarray.shape, fill_value=0x08, dtype=np.uint8)
            masked = np.right_shift(np.bitwise_and(valuesarray, mask), 3)
            self.add_sensor_data_to_db(recordset, activity_sensor, cycle_channel, sensor_timestamps, masked[:, 0])

            mask = np.full(valuesarray.shape, fill_value=0x10, dtype=np.uint8)
            masked = np.right_shift(np.bitwise_and(valuesarray, mask), 4)
            self.add_sensor_data_to_db(recordset, activity_sensor, run_channel, sensor_timestamps, masked[:, 0])

            mask = np.full(valuesarray.shape, fill_value=0x20, dtype=np.uint8)
            masked = np.right_shift(np.bitwise_and(valuesarray, mask), 5)
            self.add_sensor_data_to_db(recordset, activity_sensor, stat_channel, sensor_timestamps, masked[:, 0])

            mask = np.full(valuesarray.shape, fill_value=0x40, dtype=np.uint8)
            masked = np.right_shift(np.bitwise_and(valuesarray, mask), 6)
            self.add_sensor_data_to_db(recordset, activity_sensor, walk_channel, sensor_timestamps, masked[:, 0])

            mask = np.full(valuesarray.shape, fill_value=0x80, dtype=np.uint8)
            masked = np.right_shift(np.bitwise_and(valuesarray, mask), 7)
            self.add_sensor_data_to_db(recordset, activity_sensor, unknown_channel, sensor_timestamps, masked[:, 0])

            count += 1
            self.update_progress.emit(50 + np.floor(count / len(activity) / 2 * 100))

    def import_raw_accelerometer_to_database(self, settings: str, sample_rate, raw_accelero: dict):
        # DL Oct. 17 2018, New import to database
        raw_accelerometer_sensor = self.add_sensor_to_db(SensorType.ACCELEROMETER, 'Raw Accelerometer',
                                                         'AppleWatch',
                                                         'Wrist', sample_rate, 1, settings, self.device_id)

        raw_accelerometer_channels = list()

        # Create channels
        raw_accelerometer_channels.append(self.add_channel_to_db(raw_accelerometer_sensor, Units.GRAVITY_G,
                                                                 DataFormat.FLOAT32, 'Accelerometer_X'))

        raw_accelerometer_channels.append(self.add_channel_to_db(raw_accelerometer_sensor, Units.GRAVITY_G,
                                                                 DataFormat.FLOAT32, 'Accelerometer_Y'))

        raw_accelerometer_channels.append(self.add_channel_to_db(raw_accelerometer_sensor, Units.GRAVITY_G,
                                                                 DataFormat.FLOAT32, 'Accelerometer_Z'))

        # Data is already hour-aligned iterate through hours
        count = 0
        for timestamp in raw_accelero:
            # Filter invalid timestamp if needed
            if timestamp.year < 2000:
                continue
            # print('raw_accelero', timestamp, len(raw_accelero[timestamp]['times']),
            #       len(raw_accelero[timestamp]['values']))

            # Calculate recordset
            recordset = self.get_recordset(timestamp.timestamp(), session_name=self.session_name)

            # Add motion data to database

            # Create time array as float64
            timesarray = np.asarray(raw_accelero[timestamp]['times'], dtype=np.float64)

            if len(timesarray) == 0:
                self.last_error = "Aucune données temporelles."
                return

            # Other values are float32
            valuesarray = np.asarray(raw_accelero[timestamp]['values'], dtype=np.float32)

            # raw_accelero contains in this order
            # acceleration(x, y, z)

            sensor_timestamps = self.create_sensor_timestamps(timesarray, recordset)

            # Acc
            # for i in range(len(raw_accelerometer_channels)):
            for i, channel in enumerate(raw_accelerometer_channels):
                self.add_sensor_data_to_db(recordset, raw_accelerometer_sensor, channel,
                                           sensor_timestamps, valuesarray[:, i])
                count += 1
                self.update_progress.emit(
                    50 + np.floor(count / (len(raw_accelero) * len(raw_accelerometer_channels)) / 2
                                  * 100))

    def import_raw_gyro_to_database(self, settings, sample_rate, raw_gyro: dict):
        # DL Oct. 17 2018, New import to database
        # Create sensor
        raw_gyro_sensor = self.add_sensor_to_db(SensorType.GYROMETER, 'Raw Gyro',
                                                'AppleWatch',
                                                'Wrist', sample_rate, 1, settings, self.device_id)

        raw_gyro_channels = list()

        # Create channels
        raw_gyro_channels.append(self.add_channel_to_db(raw_gyro_sensor, Units.DEG_PER_SEC,
                                                        DataFormat.FLOAT32, 'Gyro_X'))

        raw_gyro_channels.append(self.add_channel_to_db(raw_gyro_sensor, Units.DEG_PER_SEC,
                                                        DataFormat.FLOAT32, 'Gyro_Y'))

        raw_gyro_channels.append(self.add_channel_to_db(raw_gyro_sensor, Units.DEG_PER_SEC,
                                                        DataFormat.FLOAT32, 'Gyro_Z'))

        # Data is already hour-aligned iterate through hours
        count = 0
        for timestamp in raw_gyro:
            # Filter invalid timestamp if needed
            if timestamp.year < 2000:
                continue
            # print('raw_gyro', timestamp, len(raw_gyro[timestamp]['times']),
            #       len(raw_gyro[timestamp]['values']))

            # Calculate recordset
            recordset = None
            try:
                recordset = self.get_recordset(timestamp.timestamp(), session_name=self.session_name)
            except OSError as e:
                print(e.filename + ' - ' + str(timestamp) + ' : ' + e.strerror)

            # Create time array as float64
            timesarray = np.asarray(raw_gyro[timestamp]['times'], dtype=np.float64)

            if len(timesarray) == 0:
                self.last_error = "Aucune données temporelles."
                return

            # Other values are float32
            valuesarray = np.asarray(raw_gyro[timestamp]['values'], dtype=np.float32)

            # raw_accelero contains in this order
            # gyro(x, y, z)

            # Create sensor timestamps first
            sensor_timestamps = self.create_sensor_timestamps(timesarray, recordset)

            # Gyro
            # for i in range(len(raw_gyro_channels)):
            for i, channel in enumerate(raw_gyro_channels):
                self.add_sensor_data_to_db(recordset, raw_gyro_sensor, channel,
                                           sensor_timestamps, valuesarray[:, i])

            count += 1
            self.update_progress.emit(50 + np.floor(count / len(raw_gyro) / 2 * 100))

    def import_raw_magneto_to_database(self, settings, sample_rate, raw_data: dict):
        # Create sensor
        raw_magneto_sensor = self.add_sensor_to_db(SensorType.MAGNETOMETER, 'Raw Magneto', 'AppleWatch',
                                                   'Wrist', sample_rate, 1, settings, self.device_id)

        raw_mag_channels = list()

        # Create channels
        raw_mag_channels.append(self.add_channel_to_db(raw_magneto_sensor, Units.UTESLA, DataFormat.FLOAT32, 'Mag_X'))
        raw_mag_channels.append(self.add_channel_to_db(raw_magneto_sensor, Units.UTESLA, DataFormat.FLOAT32, 'Mag_Y'))
        raw_mag_channels.append(self.add_channel_to_db(raw_magneto_sensor, Units.UTESLA, DataFormat.FLOAT32, 'Mag_Z'))

        # Data is already hour-aligned iterate through hours
        count = 0
        for timestamp in raw_data:
            # Filter invalid timestamp if needed
            if timestamp.year < 2000:
                continue

            # Calculate recordset
            recordset = None
            try:
                recordset = self.get_recordset(timestamp.timestamp(), session_name=self.session_name)
            except OSError as e:
                print(e.filename + ' - ' + str(timestamp) + ' : ' + e.strerror)

            # Create time array as float64
            timesarray = np.asarray(raw_data[timestamp]['times'], dtype=np.float64)

            if len(timesarray) == 0:
                self.last_error = "Aucune données temporelles."
                return

            # Other values are float32
            valuesarray = np.asarray(raw_data[timestamp]['values'], dtype=np.float32)

            # Create sensor timestamps first
            sensor_timestamps = self.create_sensor_timestamps(timesarray, recordset)

            for i, channel in enumerate(raw_mag_channels):
                self.add_sensor_data_to_db(recordset, raw_magneto_sensor, channel, sensor_timestamps, valuesarray[:, i])

            count += 1
            self.update_progress.emit(50 + np.floor(count / len(raw_data) / 2 * 100))

    def import_heartrate_to_database(self, settings, sample_rate, heartrate: dict):
        heartrate_sensor = self.add_sensor_to_db(SensorType.HEARTRATE, 'Heartrate', 'AppleWatch', 'Wrist',
                                                 sample_rate, 1, settings, self.device_id)

        heartrate_channel = self.add_channel_to_db(heartrate_sensor, Units.BPM, DataFormat.UINT8, 'Heartrate')
        count = 0
        for timestamp in heartrate:
            # Filter invalid timestamp if needed
            if timestamp.year < 2000:
                continue
            # print('heartrate', timestamp, len(heartrate[timestamp]['times']),
            #       len(heartrate[timestamp]['values']))

            # Calculate recordset
            recordset = self.get_recordset(timestamp.timestamp(), session_name=self.session_name)

            # Create time array as float64
            timesarray = np.asarray(heartrate[timestamp]['times'], dtype=np.float64)

            if len(timesarray) == 0:
                self.last_error = "Aucune données temporelles."
                return

            # Other values are float32
            valuesarray = np.asarray(heartrate[timestamp]['values'], dtype=np.uint8)

            # Create sensor timestamps first
            sensor_timestamps = self.create_sensor_timestamps(timesarray, recordset)

            # Store data
            self.add_sensor_data_to_db(recordset, heartrate_sensor, heartrate_channel,
                                       sensor_timestamps, valuesarray[:, 0])
            count += 1
            self.update_progress.emit(50 + np.floor(count / len(heartrate) / 2 * 100))

    def import_coordinates_to_database(self, settings, sample_rate, coordinates: dict):
        # DL Oct. 17 2018, New import to database
        coordinates_sensor = self.add_sensor_to_db(SensorType.GPS, 'Coordinates', 'AppleWatch', 'Wrist',
                                                   sample_rate, 1, settings, self.device_id)
        coordinates_channel = self.add_channel_to_db(coordinates_sensor, Units.NONE, DataFormat.UINT8, 'Coordinates')

        for timestamp in coordinates:
            # Filter invalid timestamp if needed
            if timestamp.year < 2000:
                continue
            # print('coordinates', timestamp, len(coordinates[timestamp]['times']),
            #      len(coordinates[timestamp]['values']))

            # Create time array as float64
            timesarray = np.asarray(coordinates[timestamp]['times'], dtype=np.float64)

            if len(timesarray) == 0:
                self.last_error = "Aucune données temporelles."
                return

            # Other values are float32
            valuesarray = np.asarray(coordinates[timestamp]['values'], dtype=np.float32)

            # Create one entry per timestamp ?
            # Could we store a vector instead ?
            for i, value in enumerate(valuesarray):
                # Build gps data
                geo = GPSGeodetic()
                geo.nav_valid = 1
                geo.latitude = int(value[0] * 1e7)
                geo.longitude = int(value[1] * 1e7)
                geo.accuracy = np.uint16(value[2]*100)
                geo.altitude_mls = np.uint16(value[3])
                geo.altitude_accuracy = np.uint16(value[4]*100)
                if value[5] < 0:
                    value[5] = 0
                geo.speed_over_ground = np.uint16(value[5]*100)
                if value[6] < 0:
                    value[6] = 0
                geo.course_over_ground = np.uint16(value[6])

                # Create sensor timestamps first
                sensor_timestamps = SensorTimestamps()
                sensor_timestamps.timestamps = timesarray[i:i + 1]
                sensor_timestamps.update_timestamps()

                current_timestamp = datetime.datetime.fromtimestamp(timesarray[i:i + 1][0])
                geo.year = current_timestamp.year
                geo.month = current_timestamp.month
                geo.day = current_timestamp.day
                geo.hour = current_timestamp.hour
                geo.minute = current_timestamp.minute
                geo.second = current_timestamp.second

                # Calculate recordset
                recordset = self.get_recordset(sensor_timestamps.start_timestamp.timestamp(),
                                               session_name=self.session_name)

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
                self.update_progress.emit(50 + np.floor(i / len(valuesarray) / 2 * 100))

    def import_pedometer_to_database(self, settings, pedometer: dict):
        pedometer_sensor = self.add_sensor_to_db(SensorType.STEP, 'Pedometer', 'AppleWatch', 'Wrist',
                                                 0, 1, settings, self.device_id)
        step_channel = self.add_channel_to_db(pedometer_sensor, Units.NONE, DataFormat.UINT32, 'Step count')
        distance_channel = self.add_channel_to_db(pedometer_sensor, Units.METERS, DataFormat.FLOAT32, 'Distance')
        average_pace_channel = self.add_channel_to_db(pedometer_sensor, Units.METERS_PER_SEC, DataFormat.FLOAT32,
                                                      'Average Pace')
        pace_channel = self.add_channel_to_db(pedometer_sensor, Units.METERS_PER_SEC, DataFormat.FLOAT32,
                                              'Pace')
        cadence_channel = self.add_channel_to_db(pedometer_sensor, Units.METERS_PER_SEC, DataFormat.FLOAT32, 'Cadence')
        floors_up_channel = self.add_channel_to_db(pedometer_sensor, Units.NONE, DataFormat.UINT32, 'Floors ascended')
        floors_down_channel = self.add_channel_to_db(pedometer_sensor, Units.NONE, DataFormat.UINT32,
                                                     'Floors descended')

        count = 0
        for timestamp in pedometer:
            # Filter invalid timestamp if needed
            if timestamp.year < 2000:
                continue

            # Calculate recordset
            recordset = self.get_recordset(timestamp.timestamp(), session_name=self.session_name)

            # Create time array as float64
            timesarray = np.asarray(pedometer[timestamp]['times'], dtype=np.float64)

            if len(timesarray) == 0:
                self.last_error = "No temporal data"
                return

            # Create sensor timestamps first
            sensor_timestamps = self.create_sensor_timestamps(timesarray, recordset)

            # Step counts as UInt32
            valuesarray = np.asarray(pedometer[timestamp]['values'], dtype=np.int32)

            # Store counts
            self.add_sensor_data_to_db(recordset, pedometer_sensor, step_channel, sensor_timestamps,
                                       valuesarray[:, 0])

            values = valuesarray[:, 5]
            # if values.min() >= 0 and values.max() >= 0:  # Ignore if not available (all -1)
            self.add_sensor_data_to_db(recordset, pedometer_sensor, floors_up_channel, sensor_timestamps, values)

            values = valuesarray[:, 6]
            # if values.min() >= 0 and values.max() >= 0:
            self.add_sensor_data_to_db(recordset, pedometer_sensor, floors_down_channel, sensor_timestamps, values)

            # Other values are float32
            valuesarray = np.asarray(pedometer[timestamp]['values'], dtype=np.float32)
            values = valuesarray[:, 1]
            # if values.min() >= 0 and values.max() >= 0:  # Ignore if not available (all -1)
            self.add_sensor_data_to_db(recordset, pedometer_sensor, distance_channel, sensor_timestamps, values)

            values = valuesarray[:, 2]
            # if values.min() >= 0 and values.max() >= 0:  # Ignore if not available (all -1)
            self.add_sensor_data_to_db(recordset, pedometer_sensor, average_pace_channel, sensor_timestamps, values)

            values = valuesarray[:, 3]
            # if values.min() >= 0 and values.max() >= 0:  # Ignore if not available (all -1)
            self.add_sensor_data_to_db(recordset, pedometer_sensor, pace_channel, sensor_timestamps, values)

            values = valuesarray[:, 4]
            # if values.min() >= 0 and values.max() >= 0:  # Ignore if not available (all -1)
            self.add_sensor_data_to_db(recordset, pedometer_sensor, cadence_channel, sensor_timestamps, values)

            count += 1
            self.update_progress.emit(50 + np.floor(count / len(pedometer) / 2 * 100))

    def import_sensoria_to_database(self, settings, sample_rate, sensoria: dict):
        # DL Oct. 17 2018, New import to database
        sensoria_acc_sensor = self.add_sensor_to_db(SensorType.ACCELEROMETER, 'Accelerometer', 'Sensoria', 'Foot',
                                                    sample_rate, 1, settings, self.device_id)

        sensoria_acc_channels = list()
        sensoria_acc_channels.append(self.add_channel_to_db(sensoria_acc_sensor, Units.GRAVITY_G,
                                                            DataFormat.FLOAT32, 'Accelerometer_X'))
        sensoria_acc_channels.append(self.add_channel_to_db(sensoria_acc_sensor, Units.GRAVITY_G,
                                                            DataFormat.FLOAT32, 'Accelerometer_Y'))
        sensoria_acc_channels.append(self.add_channel_to_db(sensoria_acc_sensor, Units.GRAVITY_G,
                                                            DataFormat.FLOAT32, 'Accelerometer_Z'))

        sensoria_gyro_sensor = self.add_sensor_to_db(SensorType.GYROMETER, 'Gyroscope', 'Sensoria', 'Foot',
                                                     sample_rate, 1, settings, self.device_id)
        sensoria_gyro_channels = list()
        sensoria_gyro_channels.append(self.add_channel_to_db(sensoria_gyro_sensor, Units.DEG_PER_SEC,
                                                             DataFormat.FLOAT32, 'Gyro_X'))
        sensoria_gyro_channels.append(self.add_channel_to_db(sensoria_gyro_sensor, Units.DEG_PER_SEC,
                                                             DataFormat.FLOAT32, 'Gyro_Y'))
        sensoria_gyro_channels.append(self.add_channel_to_db(sensoria_gyro_sensor, Units.DEG_PER_SEC,
                                                             DataFormat.FLOAT32, 'Gyro_Z'))

        sensoria_mag_sensor = self.add_sensor_to_db(SensorType.MAGNETOMETER, 'Magnetometer', 'Sensoria', 'Foot',
                                                    sample_rate, 1, settings, self.device_id)
        sensoria_mag_channels = list()
        sensoria_mag_channels.append(self.add_channel_to_db(sensoria_mag_sensor, Units.GAUSS,
                                                            DataFormat.FLOAT32, 'Mag_X'))
        sensoria_mag_channels.append(self.add_channel_to_db(sensoria_mag_sensor, Units.GAUSS,
                                                            DataFormat.FLOAT32, 'Mag_Y'))
        sensoria_mag_channels.append(self.add_channel_to_db(sensoria_mag_sensor, Units.GAUSS,
                                                            DataFormat.FLOAT32, 'Mag_Z'))

        sensoria_fsr_sensor = self.add_sensor_to_db(SensorType.FSR, 'FSR', 'Sensoria', 'Foot',
                                                    sample_rate, 1, settings, self.device_id)
        sensoria_fsr_channels = list()
        sensoria_fsr_channels.append(self.add_channel_to_db(sensoria_fsr_sensor, Units.NONE,
                                                            DataFormat.UINT16, 'META-1'))
        sensoria_fsr_channels.append(self.add_channel_to_db(sensoria_fsr_sensor, Units.NONE,
                                                            DataFormat.UINT16, 'META-5'))
        sensoria_fsr_channels.append(self.add_channel_to_db(sensoria_fsr_sensor, Units.NONE,
                                                            DataFormat.UINT16, 'HEEL'))
        count = 0
        for timestamp in sensoria:
            # Filter invalid timestamp if needed
            if timestamp.year < 2000:
                continue
            # print('sensoria', timestamp, len(sensoria[timestamp]['times']),
            #      len(sensoria[timestamp]['values']))

            # Calculate recordset
            recordset = self.get_recordset(timestamp.timestamp(), session_name=self.session_name)

            # Create time array as float64
            timesarray = np.asarray(sensoria[timestamp]['times'], dtype=np.float64)

            if len(timesarray) == 0:
                self.last_error = "Aucune données temporelles."
                return

            # Create sensor timestamps first
            sensor_timestamps = self.create_sensor_timestamps(timesarray, recordset)

            # FSR values are uint16
            valuesarray = np.asarray(sensoria[timestamp]['values'], dtype=np.uint16)

            # Store FSR
            for i, fsr_channel in enumerate(sensoria_fsr_channels):
                self.add_sensor_data_to_db(recordset, sensoria_fsr_sensor, fsr_channel,
                                           sensor_timestamps,
                                           valuesarray[:, i + 1])

            # Other values are float32
            valuesarray = np.asarray(sensoria[timestamp]['values'], dtype=np.float32)
            # Store Acc
            for i, acc_channel in enumerate(sensoria_acc_channels):
                self.add_sensor_data_to_db(recordset, sensoria_acc_sensor, acc_channel,
                                           sensor_timestamps,
                                           valuesarray[:, i + 4])

            # Store Gyro
            for i, gyro_channel in enumerate(sensoria_gyro_channels):
                self.add_sensor_data_to_db(recordset, sensoria_gyro_sensor, gyro_channel,
                                           sensor_timestamps,
                                           valuesarray[:, i + 7])

            # Magneto
            for i, mag_channel in enumerate(sensoria_mag_channels):
                self.add_sensor_data_to_db(recordset, sensoria_mag_sensor, mag_channel,
                                           sensor_timestamps,
                                           valuesarray[:, i + 10])

            count += 1
            self.update_progress.emit(50 + np.floor(count / len(sensoria) / 2 * 100))

    def import_beacons_to_database(self, settings, sample_rate, beacons: dict):
        # DL Oct. 17 2018, New import to database
        beacons_sensor = self.add_sensor_to_db(SensorType.BEACON, 'Beacons', 'Kontact', 'Environment',
                                               sample_rate, 1, settings, self.device_id)
        channel_values = dict()

        # Data is already hour-aligned iterate through hours
        for timestamp in beacons:
            # Filter invalid timestamp if needed
            if timestamp.year < 2000:
                continue
            # print('beacons', timestamp, len(beacons[timestamp]['times']),
            #      len(beacons[timestamp]['values']))

            # Create time array as float64
            timesarray = np.asarray(beacons[timestamp]['times'], dtype=np.float64)

            if len(timesarray) == 0:
                self.last_error = "Aucune données temporelles."
                return

            # Other values are int8
            valuesarray = np.asarray(beacons[timestamp]['values'], dtype=np.int16)

            # Iterate through each entry to generate data for each beacon_id
            for i, timearray in enumerate(timesarray):
                name = [str(format(x, 'x')).rjust(2, '0') for x in beacons[timestamp]['values'][i][0:16]]
                beacon_id = ''.join(name[0:10]) + '_' + ''.join(name[10:])

                # Create channel if it does not exist
                if not channel_values.__contains__(beacon_id):
                    channel_values[beacon_id] = []

                channel_values[beacon_id].append((timearray, valuesarray[i][16], valuesarray[i][17]))

            # Store each beacon_id in separate channels
            count = 0
            for key in channel_values:
                timevect = np.asarray([x[0] for x in channel_values[key]], dtype=np.float64)

                # Create sensor timestamps first
                sensor_timestamps = SensorTimestamps()
                sensor_timestamps.timestamps = timevect
                sensor_timestamps.update_timestamps()

                # Calculate recordset
                recordset = self.get_recordset(sensor_timestamps.start_timestamp.timestamp(),
                                               session_name=self.session_name)

                # Update timestamps in recordset
                # This should not happen, recordset is initialized at the beginning of the hour
                if sensor_timestamps.start_timestamp < recordset.start_timestamp:
                    recordset.start_timestamp = sensor_timestamps.start_timestamp
                # This can occur though
                if sensor_timestamps.end_timestamp > recordset.end_timestamp:
                    recordset.end_timestamp = sensor_timestamps.end_timestamp

                # Create channel
                channel_tx_power = self.add_channel_to_db(beacons_sensor, Units.NONE,
                                                          DataFormat.SINT8, key + '_TxPower')

                channel_rssi = self.add_channel_to_db(beacons_sensor, Units.NONE,
                                                      DataFormat.SINT8, key + '_RSSI')

                tx_power_vect = np.asarray([x[1] for x in channel_values[key]], dtype=np.int8)
                rssi_vect = np.asarray([x[2] for x in channel_values[key]], dtype=np.int8)

                # Add data
                self.add_sensor_data_to_db(recordset, beacons_sensor, channel_tx_power,
                                           sensor_timestamps, tx_power_vect)

                self.add_sensor_data_to_db(recordset, beacons_sensor, channel_rssi,
                                           sensor_timestamps, rssi_vect)
            count += 1
            self.update_progress.emit(50 + np.floor(count / len(beacons) / 2 * 100))

    def import_motion_to_database(self, settings, sampling_rate, motion: dict, version: int):
        # DL Oct. 16 2018, New import to database

        # Create channels and sensors
        accelerometer_sensor = self.add_sensor_to_db(SensorType.ACCELEROMETER, 'Accelerometer',
                                                     'AppleWatch', 'Wrist', sampling_rate, 1, settings, self.device_id)

        accelerometer_channels = list()

        # Create channels
        accelerometer_channels.append(self.add_channel_to_db(accelerometer_sensor, Units.GRAVITY_G,
                                                             DataFormat.FLOAT32, 'Accelerometer_X'))

        accelerometer_channels.append(self.add_channel_to_db(accelerometer_sensor, Units.GRAVITY_G,
                                                             DataFormat.FLOAT32, 'Accelerometer_Y'))

        accelerometer_channels.append(self.add_channel_to_db(accelerometer_sensor, Units.GRAVITY_G,
                                                             DataFormat.FLOAT32, 'Accelerometer_Z'))

        # Create sensor
        gyro_sensor = self.add_sensor_to_db(SensorType.GYROMETER, 'Gyroscope', 'AppleWatch',
                                            'Wrist', sampling_rate, 1, settings, self.device_id)

        gyro_channels = list()

        # Create channels
        gyro_channels.append(self.add_channel_to_db(gyro_sensor, Units.DEG_PER_SEC,
                                                    DataFormat.FLOAT32, 'Gyro_X'))

        gyro_channels.append(self.add_channel_to_db(gyro_sensor, Units.DEG_PER_SEC,
                                                    DataFormat.FLOAT32, 'Gyro_Y'))

        gyro_channels.append(self.add_channel_to_db(gyro_sensor, Units.DEG_PER_SEC,
                                                    DataFormat.FLOAT32, 'Gyro_Z'))

        orientation_sensor = self.add_sensor_to_db(SensorType.ORIENTATION, 'Attitude', 'AppleWatch',
                                                   'Wrist', sampling_rate, 1, settings, self.device_id)

        orientation_channels = list()
        orientation_channels.append(self.add_channel_to_db(orientation_sensor, Units.NONE, DataFormat.FLOAT32, 'q0'))
        orientation_channels.append(self.add_channel_to_db(orientation_sensor, Units.NONE, DataFormat.FLOAT32, 'q1'))
        orientation_channels.append(self.add_channel_to_db(orientation_sensor, Units.NONE, DataFormat.FLOAT32, 'q2'))
        orientation_channels.append(self.add_channel_to_db(orientation_sensor, Units.NONE, DataFormat.FLOAT32, 'q3'))

        mag_channels = list()
        magneto_sensor = None
        if version >= 3:  # Also includes magnetometer values
            # Create sensor
            magneto_sensor = self.add_sensor_to_db(SensorType.MAGNETOMETER, 'Magnetometer', 'AppleWatch',
                                                   'Wrist', sampling_rate, 1, settings, self.device_id)

            # Create channels
            mag_channels.append(self.add_channel_to_db(magneto_sensor, Units.UTESLA, DataFormat.FLOAT32, 'Mag_X'))
            mag_channels.append(self.add_channel_to_db(magneto_sensor, Units.UTESLA, DataFormat.FLOAT32, 'Mag_Y'))
            mag_channels.append(self.add_channel_to_db(magneto_sensor, Units.UTESLA, DataFormat.FLOAT32, 'Mag_Z'))

        # Data is already hour-aligned iterate through hours
        count = 0
        for timestamp in motion:
            # Filter invalid timestamp if needed
            if timestamp.year < 2000:
                continue
            # print('motion', timestamp, len(motion[timestamp]['times']),
            #     len(motion[timestamp]['values']))

            # Calculate recordset
            recordset = self.get_recordset(timestamp.timestamp(), session_name=self.session_name)

            # Add motion data to database

            # Create time array as float64
            timesarray = np.asarray(motion[timestamp]['times'], dtype=np.float64)

            if len(timesarray) == 0:
                self.last_error = "Aucune données temporelles."
                return

            # Other values are float32
            valuesarray = np.asarray(motion[timestamp]['values'], dtype=np.float32)

            # Motion contains in this order
            # acceleration(x, y, z)
            # gravity vector(x, y, z)
            # gyroscope(x, y, z)
            # attitude quaternion(w, x, y, z)

            # Create sensor timestamps first
            sensor_timestamps = self.create_sensor_timestamps(timesarray, recordset)

            # Acc
            for i, acc_channel in enumerate(accelerometer_channels):
                self.add_sensor_data_to_db(recordset, accelerometer_sensor, acc_channel,
                                           sensor_timestamps, valuesarray[:, i])

            # Gyro
            for i, gyro_channel in enumerate(gyro_channels):
                self.add_sensor_data_to_db(recordset, gyro_sensor, gyro_channel,
                                           sensor_timestamps, valuesarray[:, i + 6])

            # Magneto
            current_offset = 9
            if magneto_sensor:
                for i, mag_channel in enumerate(mag_channels):
                    self.add_sensor_data_to_db(recordset, magneto_sensor, mag_channel, sensor_timestamps,
                                               valuesarray[:, i + current_offset])
                current_offset = 12

            # Attitude
            for i, channel in enumerate(orientation_channels):
                self.add_sensor_data_to_db(recordset, orientation_sensor, channel, sensor_timestamps,
                                           valuesarray[:, i + current_offset])

            count += 1
            self.update_progress.emit(50 + np.floor(count / len(motion) / 2 * 100))

    def import_battery_to_database(self, settings, sampling_rate, battery: dict):
        # DL Oct. 16 2018, New import to database
        battery_sensor = self.add_sensor_to_db(SensorType.BATTERY, 'Battery', 'AppleWatch', 'Wrist',
                                               sampling_rate, 1, settings, self.device_id)

        battery_channel = self.add_channel_to_db(battery_sensor, Units.VOLTS, DataFormat.UINT8, 'Battery Percentage')

        # Data is already hour-aligned iterate through hours
        count = 0
        for timestamp in battery:
            # Filter invalid timestamp if needed
            if timestamp.year < 2000:
                continue
            # print('battery', timestamp, len(battery[timestamp]['times']),
            #      len(battery[timestamp]['values']))

            # Calculate recordset
            recordset = self.get_recordset(timestamp.timestamp(), session_name=self.session_name)

            # Import to database
            # Create time array as float64
            timesarray = np.asarray(battery[timestamp]['times'], dtype=np.float64)

            if len(timesarray) == 0:
                self.last_error = "Aucune donnée temporelle."
                return

            # Other values are float32
            valuesarray = np.asarray(battery[timestamp]['values'], dtype=np.uint8)

            # Create sensor timestamps first
            sensor_timestamps = self.create_sensor_timestamps(timesarray, recordset)

            self.add_sensor_data_to_db(recordset, battery_sensor, battery_channel, sensor_timestamps,
                                       valuesarray[:, 0])

            count += 1
            self.update_progress.emit(50 + np.floor(count / len(battery) / 2 * 100))

    def import_headings_to_database(self, settings, sampling_rate, headings: dict):
        # Create channels and sensors
        orientation_sensor = self.add_sensor_to_db(SensorType.HEADINGS, 'Headings', 'AppleWatch',
                                                   'Wrist', sampling_rate, 1, settings, self.device_id)

        orientation_channels = list()
        orientation_channels.append(self.add_channel_to_db(orientation_sensor, Units.DEGREES, DataFormat.FLOAT32,
                                                           'True Heading'))

        orientation_channels.append(self.add_channel_to_db(orientation_sensor, Units.DEGREES, DataFormat.FLOAT32,
                                                           'Accuracy'))

        orientation_channels.append(self.add_channel_to_db(orientation_sensor, Units.DEGREES, DataFormat.FLOAT32,
                                                           'Mag Heading'))

        # Create sensor
        magneto_sensor = self.add_sensor_to_db(SensorType.MAGNETOMETER, 'Magnetometer', 'AppleWatch',
                                               'Wrist', sampling_rate, 1, settings, self.device_id)

        magneto_channels = list()

        # Create channels
        magneto_channels.append(self.add_channel_to_db(magneto_sensor, Units.UTESLA, DataFormat.FLOAT32, 'Mag_X'))
        magneto_channels.append(self.add_channel_to_db(magneto_sensor, Units.UTESLA, DataFormat.FLOAT32, 'Mag_Y'))
        magneto_channels.append(self.add_channel_to_db(magneto_sensor, Units.UTESLA, DataFormat.FLOAT32, 'Mag_Z'))

        # Data is already hour-aligned iterate through hours
        count = 0
        for timestamp in headings:
            # Filter invalid timestamp if needed
            if timestamp.year < 2000:
                continue

            # Calculate recordset
            recordset = self.get_recordset(timestamp.timestamp(), session_name=self.session_name)

            # Add data to database

            # Create time array as float64
            timesarray = np.asarray(headings[timestamp]['times'], dtype=np.float64)

            if len(timesarray) == 0:
                self.last_error = "Aucune données temporelles."
                return

            # Other values are float32
            valuesarray = np.asarray(headings[timestamp]['values'], dtype=np.float32)

            # Create sensor timestamps first
            sensor_timestamps = self.create_sensor_timestamps(timesarray, recordset)

            # Headings
            for i, channel in enumerate(orientation_channels):
                self.add_sensor_data_to_db(recordset, orientation_sensor, channel,
                                           sensor_timestamps, valuesarray[:, i])

            # Magneto
            for i, channel in enumerate(magneto_channels):
                self.add_sensor_data_to_db(recordset, magneto_sensor, channel,
                                           sensor_timestamps, valuesarray[:, i + 3])

            count += 1
            self.update_progress.emit(50 + np.floor(count / len(headings) / 2 * 100))

    def import_health_to_database(self, settings, health: dict):
        # Check settings to find out what sensors are enabled
        if 'healthkitTypes' not in settings:
            # print("No healthkit types found - ignoring.")
            return

        health_types = json.loads(settings)['healthkitTypes']

        # Create base sensor(s)
        health_sensor = self.add_sensor_to_db(SensorType.BIOMETRICS, 'Health', 'AppleWatch',
                                              'Wrist', 0, 1, settings, self.device_id)

        step_sensor = None
        if 'stepCount' in health_types:
            step_sensor = self.add_sensor_to_db(SensorType.STEP, 'Step Count (Health)', 'AppleWatch', 'Wrist',
                                                0, 1, self.device_id)

        heartrate_sensor = None
        if 'heartRate' in health_types:
            heartrate_sensor = self.add_sensor_to_db(SensorType.HEARTRATE, 'Heartrate (Health)', 'AppleWatch', 'Wrist',
                                                     0, 1, self.device_id)

        health_channels = list()

        for health_type in health_types:
            # Set specific informations depending on type
            base_sensor = health_sensor
            units = Units.NONE

            if health_type == 'stepCount':
                base_sensor = step_sensor
            if health_type == 'heartRate':
                base_sensor = heartrate_sensor
            if health_type == 'activeEnergyBurned' or health_type == 'basalEnergyBurned':
                units = Units.KCALORIES
            if (health_type == 'heartRate' or health_type == 'respiratoryRate' or health_type == 'restingHeartRate'
                    or health_type == 'walkingHeartRateAverage'):
                units = Units.BPM
            if health_type == 'oxygenSaturation' or health_type == 'appleWalkingSteadiness':
                units = Units.PERCENTAGE
            if health_type == 'vo2Max':
                units = Units.MLKGMIN
            if health_type == 'heartRateVariability':
                units = Units.MILLISECONDS
            if health_type == 'bodyTemperature':
                units = Units.DEGREES
            if health_type == 'appleExerciseTime' or health_type == 'appleStandTime' or health_type == 'appleMoveTime':
                units = Units.SECONDS
            if health_type == 'walkingSpeed':
                units = Units.METERS_PER_SEC
            if health_type == 'walkingStepLength':
                units = Units.METERS

            # Create channel
            health_channels.append(self.add_channel_to_db(base_sensor, units, DataFormat.FLOAT32, health_type))

        # Import data depending on each sensors
        count = 0
        for timestamp in health:
            # Filter invalid timestamp if needed
            if timestamp.year < 2000:
                continue

            # Calculate recordset
            recordset = self.get_recordset(timestamp.timestamp(), session_name=self.session_name)

            # Add data to database
            # Create time array as float64
            timesarray = np.asarray(health[timestamp]['times'], dtype=np.float64)

            if len(timesarray) == 0:
                self.last_error = "Aucune données temporelles."
                return

            # Other values are float32
            valuesarray = np.asarray(health[timestamp]['values'], dtype=np.float32)

            # Regroup according to health_index
            for i, channel in enumerate(health_channels):
                # print("Importing channel #" + str(i) + ": " + channel.label)
                values_index = np.where(valuesarray[:, 2] == i)[0]
                if len(values_index) > 0:
                    times = timesarray[values_index]
                    values = valuesarray[values_index, :]
                    sensor_timestamps = self.create_sensor_timestamps(times, recordset)
                    # TODO: Manage specific reading start & end timestamp
                    self.add_sensor_data_to_db(recordset, channel.sensor, channel, sensor_timestamps, values[:, 3])

            count += 1
            self.update_progress.emit(50 + np.floor(count / len(health) / 2 * 100))

    def import_tremor_to_database(self, settings, tremor: dict):
        # Create channels and sensors
        tremor_sensor = self.add_sensor_to_db(SensorType.BIOMETRICS, 'Tremor', 'AppleWatch', 'Wrist', 0, 1,
                                              settings, self.device_id)

        tremor_channels = list()
        tremor_channels.append(self.add_channel_to_db(tremor_sensor, Units.MILLISECONDS, DataFormat.UINT64,
                                                      'Start Timestamp'))

        tremor_channels.append(self.add_channel_to_db(tremor_sensor, Units.MILLISECONDS, DataFormat.UINT64,
                                                      'End Timestamp'))

        tremor_channels.append(self.add_channel_to_db(tremor_sensor, Units.PERCENTAGE, DataFormat.FLOAT32, 'None'))
        tremor_channels.append(self.add_channel_to_db(tremor_sensor, Units.PERCENTAGE, DataFormat.FLOAT32, 'Slight'))
        tremor_channels.append(self.add_channel_to_db(tremor_sensor, Units.PERCENTAGE, DataFormat.FLOAT32, 'Mild'))
        tremor_channels.append(self.add_channel_to_db(tremor_sensor, Units.PERCENTAGE, DataFormat.FLOAT32, 'Moderate'))
        tremor_channels.append(self.add_channel_to_db(tremor_sensor, Units.PERCENTAGE, DataFormat.FLOAT32, 'Strong'))

        # Data is already hour-aligned iterate through hours
        count = 0
        for timestamp in tremor:
            # Filter invalid timestamp if needed
            if timestamp.year < 2000:
                continue

            # Calculate recordset
            recordset = self.get_recordset(timestamp.timestamp(), session_name=self.session_name)

            # Add data to database

            # Create time array as float64
            timesarray = np.asarray(tremor[timestamp]['times'], dtype=np.float64)

            if len(timesarray) == 0:
                self.last_error = "Aucune données temporelles."
                return

            valuesarray = np.asarray(tremor[timestamp]['values'], dtype=np.float32)

            # Create sensor timestamps first
            sensor_timestamps = self.create_sensor_timestamps(timesarray, recordset)

            for i, channel in enumerate(tremor_channels):
                # Start and end timestamp are larger than float32 - a cast is required (channel 0 and 1)
                if i <= 1:
                    current_timestamp = np.uint64(valuesarray[:, i*2:i*2+1])
                    self.add_sensor_data_to_db(recordset, tremor_sensor, channel, sensor_timestamps, current_timestamp)
                else:
                    self.add_sensor_data_to_db(recordset, tremor_sensor, channel, sensor_timestamps,
                                               valuesarray[:, i + 3])

            count += 1
            self.update_progress.emit(50 + np.floor(count / len(tremor) / 2 * 100))

    def import_dyskinetic_to_database(self, settings, dysk: dict):
        # Create channels and sensors
        dysk_sensor = self.add_sensor_to_db(SensorType.BIOMETRICS, 'Dyskinetic Mvt', 'AppleWatch', 'Wrist', 0, 1,
                                            settings, self.device_id)

        dysk_channels = list()
        dysk_channels.append(self.add_channel_to_db(dysk_sensor, Units.MILLISECONDS, DataFormat.UINT64,
                                                    'Start Timestamp'))

        dysk_channels.append(self.add_channel_to_db(dysk_sensor, Units.MILLISECONDS, DataFormat.UINT64,
                                                    'End Timestamp'))

        dysk_channels.append(self.add_channel_to_db(dysk_sensor, Units.PERCENTAGE, DataFormat.FLOAT32, 'Likeliness'))

        # Data is already hour-aligned iterate through hours
        count = 0
        for timestamp in dysk:
            # Filter invalid timestamp if needed
            if timestamp.year < 2000:
                continue

            # Calculate recordset
            recordset = self.get_recordset(timestamp.timestamp(), session_name=self.session_name)

            # Add data to database

            # Create time array as float64
            timesarray = np.asarray(dysk[timestamp]['times'], dtype=np.float64)

            if len(timesarray) == 0:
                self.last_error = "Aucune données temporelles."
                return

            valuesarray = np.asarray(dysk[timestamp]['values'], dtype=np.float32)

            # Create sensor timestamps first
            sensor_timestamps = self.create_sensor_timestamps(timesarray, recordset)

            for i, channel in enumerate(dysk_channels):
                # Start and end timestamp are larger than float32 - a cast is required (channel 0 and 1)
                if i <= 1:
                    current_timestamp = np.uint64(valuesarray[:, i*2:i*2+1])
                    self.add_sensor_data_to_db(recordset, dysk_sensor, channel, sensor_timestamps, current_timestamp)
                else:
                    self.add_sensor_data_to_db(recordset, dysk_sensor, channel, sensor_timestamps,
                                               valuesarray[:, i + 3])

            count += 1
            self.update_progress.emit(50 + np.floor(count / len(dysk) / 2 * 100))

    def import_question_to_database(self, settings, question: dict):
        # Create base sensor(s)
        questions_sensor = self.add_sensor_to_db(SensorType.QUESTIONS, 'Prompts', 'AppleWatch',
                                                 'Wrist', 0, 1, settings, self.device_id)

        # Create channel for each prompt
        prompt_channels = {}
        settings_json = json.loads(settings)
        if 'prompts' in settings_json:
            for prompt in settings_json['prompts']:
                prompt_channels[prompt['id']] = self.add_channel_to_db(questions_sensor, Units.NONE, DataFormat.JSON,
                                                                       prompt['id'])

        # Import data depending on each sensors
        count = 0
        for timestamp in question:
            # Filter invalid timestamp if needed
            if timestamp.year < 2000:
                continue

            # Calculate recordset
            recordset = self.get_recordset(timestamp.timestamp(), session_name=self.session_name)

            # Add data to database
            # Create time array as float64
            timesarray = np.asarray(question[timestamp]['times'], dtype=np.float64)

            if len(timesarray) == 0:
                self.last_error = "Aucune données temporelles."
                return

            for index in range(timesarray.size):
                answer = question[timestamp]['values'][index]
                question_time = answer[-1] / 1000
                sensor_timestamps = self.create_sensor_timestamps(np.array([question_time, timesarray[index]]),
                                                                  recordset)
                # JSON structure for answer
                answer_count = answer[1]
                answers_index = list(answer[2:2+answer_count])
                answer_id = answer[0].decode()
                answers_choices = [seta['answer']['choices'] for seta in settings_json['prompts']
                                   if seta['id'] == answer_id][0]
                answers_text = [answers_choices[i] for i in answers_index]
                answer_json = {'question_id': answer_id,
                               'answer_index': answers_index,
                               'answer_text': answers_text}
                data = np.array(json.dumps(answer_json).encode())
                self.add_sensor_data_to_db(recordset, questions_sensor, prompt_channels[answer_id], sensor_timestamps,
                                           data)


            # Other values are float32
            # valuesarray = np.asarray(health[timestamp]['values'], dtype=np.float32)
            #
            # # Regroup according to health_index
            # for i, channel in enumerate(health_channels):
            #     # print("Importing channel #" + str(i) + ": " + channel.label)
            #     values_index = np.where(valuesarray[:, 2] == i)[0]
            #     if len(values_index) > 0:
            #         times = timesarray[values_index]
            #         values = valuesarray[values_index, :]
            #         sensor_timestamps = self.create_sensor_timestamps(times, recordset)
            #         # TODO: Manage specific reading start & end timestamp
            #         self.add_sensor_data_to_db(recordset, channel.sensor, channel, sensor_timestamps, values[:, 3])

            count += 1
            self.update_progress.emit(50 + np.floor(count / len(question) / 2 * 100))

    def import_to_database(self, results):
        if results is None:
            return

        # We can have bot arrays or dict depending if we imported from a zip file or not
        process_list = []

        # Testing if we have an array of result
        if isinstance(results, dict):
            process_list.append(results)
        else:
            process_list = results

        for res in process_list:
            if res.__contains__('motion'):
                sampling_rate = res['motion']['sampling_rate']
                if res['motion']['timestamps']:
                    self.import_motion_to_database(res['motion']['settings'], sampling_rate,
                                                   res['motion']['timestamps'], res['motion']['version'])

            if res.__contains__('battery'):
                sampling_rate = res['battery']['sampling_rate']
                if res['battery']['timestamps']:
                    self.import_battery_to_database(res['battery']['settings'], sampling_rate,
                                                    res['battery']['timestamps'])

            if res.__contains__('sensoria'):
                sampling_rate = res['sensoria']['sampling_rate']
                if res['sensoria']['timestamps']:
                    self.import_sensoria_to_database(res['sensoria']['settings'], sampling_rate,
                                                     res['sensoria']['timestamps'])

            if res.__contains__('heartrate'):
                sampling_rate = res['heartrate']['sampling_rate']
                if res['heartrate']['timestamps']:
                    self.import_heartrate_to_database(res['heartrate']['settings'], sampling_rate,
                                                      res['heartrate']['timestamps'])

            if res.__contains__('beacons'):
                sampling_rate = res['beacons']['sampling_rate']
                if res['beacons']['timestamps']:
                    self.import_beacons_to_database(res['beacons']['settings'], sampling_rate,
                                                    res['beacons']['timestamps'])

            if res.__contains__('coordinates'):
                sampling_rate = res['coordinates']['sampling_rate']
                if res['coordinates']['timestamps']:
                    self.import_coordinates_to_database(res['coordinates']['settings'], sampling_rate,
                                                        res['coordinates']['timestamps'])

            if res.__contains__('raw_accelero'):
                sampling_rate = res['raw_accelero']['sampling_rate']
                if res['raw_accelero']['timestamps']:
                    self.import_raw_accelerometer_to_database(res['raw_accelero']['settings'], sampling_rate,
                                                              res['raw_accelero']['timestamps'])

            if res.__contains__('raw_gyro'):
                sampling_rate = res['raw_gyro']['sampling_rate']
                if res['raw_gyro']['timestamps']:
                    self.import_raw_gyro_to_database(res['raw_gyro']['settings'], sampling_rate,
                                                     res['raw_gyro']['timestamps'])

            if res.__contains__('pedometer'):
                if res['pedometer']['timestamps']:
                    self.import_pedometer_to_database(res['pedometer']['settings'], res['pedometer']['timestamps'])

            if res.__contains__('activity'):
                if res['activity']['timestamps']:
                    self.import_activity_to_database(res['activity']['settings'], res['activity']['timestamps'])

            if res.__contains__('headings'):
                sampling_rate = 50  # For now, since no frequency in settings?
                if res['headings']['timestamps']:
                    self.import_headings_to_database(res['headings']['settings'], sampling_rate,
                                                     res['headings']['timestamps'])

            if res.__contains__('health'):
                self.import_health_to_database(res['health']['settings'], res['health']['timestamps'])

            if res.__contains__('raw_magneto'):
                sampling_rate = res['raw_magneto']['sampling_rate']
                if res['raw_magneto']['timestamps']:
                    self.import_raw_magneto_to_database(res['raw_magneto']['settings'], sampling_rate,
                                                        res['raw_magneto']['timestamps'])

            if res.__contains__('tremor'):
                if res['tremor']['timestamps']:
                    self.import_tremor_to_database(res['tremor']['settings'], res['tremor']['timestamps'])

            if res.__contains__('question'):
                if res['question']['timestamps']:
                    self.import_question_to_database(res['question']['settings'], res['question']['timestamps'])

            # Commit DB
            self.db.commit()

    def get_sampling_rate_from_header(self, sensor_id, header):  # header = string of json
        sample_rate = 0
        if header != "":
            json_settings = json.loads(header)  # converts to json
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
            sample_rate = 1  # No sampling rate in beacons config

        if sensor_id == self.SENSORIA_ID:
            sample_rate = json_settings.get('frequency')

        return sample_rate

    def read_data_file(self, file, debug=False):
        """
        All binary files have a similar header
        • Two bytes for file identifier (based on Wimu format): 0xEA, 0xEA
        • File Version byte: eg. 0x01
        • 4 bytes (as UInt32) for participantID
        • Byte for sensor identification
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

        if version >= 2:
            [json_data_size] = struct.unpack("<I", file.read(4))
            [json_data] = struct.unpack("<{}s".format(json_data_size), file.read(json_data_size))
            settings_json_str = json_data.decode("utf-8")
            if debug:
                print('setting_json : ', settings_json_str)

            # Sort settings values
            settings_json = json.loads(settings_json_str)
            settings_json = dict(sorted(settings_json.items()))
            settings_json_str = json.dumps(settings_json)

            [end_header_id] = struct.unpack("<H", file.read(2))
            if end_header_id != self.HEADER:
                if debug:
                    print('Error unpacking file, header not ending with 0xEAEA')
                self.last_error = "Format de fichier incorrect - vérifiez qu'il s'agit bien du bon type de fichier."
                return None

        # Get correct sample_rate for data
        # results['sampling_rate'][sensor_id] = self.get_sampling_rate_from_header(sensor_id, settings_json_str)
        # print('sampling rate for sensor_id', sensor_id, ' : ', results['sampling_rate'][sensor_id])

        # prepare for loop by finding right sensor info
        dict_name = ""
        read_data_func = None
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
        elif sensor_id == self.RAW_MOTION_ID:
            # deprecated
            read_data_func = self.read_raw_motion_data
            dict_name = 'raw_motion'
        elif sensor_id == self.RAW_ACCELERO_ID:
            read_data_func = self.read_raw_accelerometer_data
            dict_name = 'raw_accelero'
        elif sensor_id == self.RAW_GYRO_ID:
            # Check if has processed motion (same data) - ignore if it's the case
            basename = os.path.basename(file.name)
            motion_file_name = file.name.replace(basename, 'watch_ProcessedMotion.data')
            if os.path.isfile(motion_file_name):
                self.last_error = "Ignoring gyro data - using processed motion instead"
                return None
            read_data_func = self.read_raw_gyro_data
            dict_name = 'raw_gyro'
        elif sensor_id == self.RAW_MAGNETO_ID:
            # Check if has processed motion (same data) - ignore if it's the case
            basename = os.path.basename(file.name)
            motion_file_name = file.name.replace(basename, 'watch_ProcessedMotion.data')
            if os.path.isfile(motion_file_name):
                self.last_error = "Ignoring magneto data - using processed motion instead"
                return None
            read_data_func = self.read_raw_magneto_data
            dict_name = 'raw_magneto'
        elif sensor_id == self.PEDOMETER_ID:
            read_data_func = self.read_pedometer_data
            dict_name = 'pedometer'
        elif sensor_id == self.ACTIVITY_ID:
            read_data_func = self.read_activity_data
            dict_name = 'activity'
        elif sensor_id == self.HEADINGS_ID:
            read_data_func = self.read_headings_data
            dict_name = 'headings'
        elif sensor_id == self.HEALTH_ID:
            read_data_func = self.read_health_data
            dict_name = 'health'
        elif sensor_id == self.QUESTION_ID:
            read_data_func = self.read_prompt_data
            dict_name = 'question'
        # elif sensor_id == self.TREMOR_ID:
        #     read_data_func = self.read_tremor_data
        #     dict_name = 'tremor'
        # elif sensor_id == self.DYSKINETIC_ID:
        #     read_data_func = self.read_dyskinetic_data
        #     dict_name = 'dysk'
        else:
            self.last_error = "Unknown sensor ID:" + str(sensor_id)
            return None

        # DL 16 oct. 2018. New format for results. Will keep all timestamps and group them by hour
        results[dict_name] = {}

        results[dict_name]['timestamps'] = {}

        # Insert sampling rate & file version information
        results[dict_name]['sampling_rate'] = self.get_sampling_rate_from_header(sensor_id, settings_json_str)
        results[dict_name]['version'] = version
        results[dict_name]['settings'] = settings_json_str

        # lists of co-dependant timestamp(ms) and data
        results_ms_ts = []
        results_ms_data = []

        if file.seekable():
            # Divided by 2, since loading is first step
            # DB import is second step
            progress = np.floor((file.tell() / self.current_file_size) * 100 / 2)

            if progress > 0:
                self.update_progress.emit(progress)

        # read the whole file
        try:
            progress = 0
            while file.readable() and read_data_func is not None:

                # Read timestamp
                [timestamp_ms] = struct.unpack("<Q", file.read(8))
                # local_ms_ts = (datetime.datetime.fromtimestamp(timestamp_ms / 1000).timestamp()) * 1000 + (
                #             timestamp_ms % 1000)
                # results_ms_ts.append(int(local_ms_ts))

                results_ms_ts.append(int(timestamp_ms))
                results_ms_data.append(read_data_func(file, debug=debug, version=version))

                if file.seekable():
                    new_progress = np.floor((file.tell() / self.current_file_size) * 100 / 2)
                    if new_progress != progress:  # Only send update if % was increased
                        progress = new_progress
                        self.update_progress.emit(progress)
        except Exception as e:
            # let's hope it's only eof...
            # Make sure data vectors are of the same size
            min_size = min(len(results_ms_ts), len(results_ms_data))
            results_ms_ts = results_ms_ts[0:min_size]
            results_ms_data = results_ms_data[0:min_size]

        # Create hour-aligned separated data
        for i, result in enumerate(results_ms_ts):
            hour_lower_limit_sec = np.floor(result / 3600000) * 3600
            mydate = datetime.datetime.fromtimestamp(hour_lower_limit_sec)

            # Create hour entry if it does not exist
            if not results[dict_name]['timestamps'].__contains__(mydate):
                results[dict_name]['timestamps'][mydate] = {'times': [], 'values': []}

            # Append data (slow?)
            # ms time to secs
            results[dict_name]['timestamps'][mydate]['times'].append(result / 1000.0)
            # data
            results[dict_name]['timestamps'][mydate]['values'].append(results_ms_data[i])

        # print('done processing: ', dict_name)

        # force the gc to clear temporary lists
        results_ms_ts.clear()
        results_ms_data.clear()
        gc.collect()

        return results

    @staticmethod
    def read_battery_data(file, debug=False, version=2):
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

    @staticmethod
    def read_sensoria_data(file, debug=False, version=2):
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

    @staticmethod
    def read_heartrate_data(file, debug=False, version=2):
        """
        unsigned integer as single Byte for bpm
        ** assumes that bpm cannot go above 255, hence values above are clamped to 255
        :param file:
        :param debug:
        :return:
        """
        chunk = file.read(1)
        data = struct.unpack("<B", chunk)
        if debug:
            print('HEARTRATE: ', data)
        return data

    @staticmethod
    def read_motion_data(file, debug=False, version=2):
        """
         13 to 16 Float32 values, with following fields
        • acceleration (x,y,z)
        • gravity vector (x,y,z)
        • gyroscope (x,y,z)
        • magneto (x,y,z) [File version 3+ only]
        • attitude quaternion (w,x,y,z)
            """
        if version == 3:
            chunk = file.read(64)
            data = struct.unpack("<16f", chunk)
        else:  # Version 2
            chunk = file.read(52)
            data = struct.unpack("<13f", chunk)
        if debug:
            print('MOTION: ', data)
        return data

    @staticmethod
    def read_beacons_data(file, debug=False, version=2):
        """
        10 Bytes Char for namespace
        6 Bytes Char for instance ID
        1 Int8 for TxPower
        1 Int8 for RSSI
        :return:
        """
        chunk = file.read(18)
        data = struct.unpack("<16B2b", chunk)
        if debug:
            print('BEACONS: ', data)
        return data

    @staticmethod
    def read_coordinates_data(file, debug=False, version=2):
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
    @staticmethod
    def read_raw_motion_data(file, debug=False, version=2):
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

    @staticmethod
    def read_raw_accelerometer_data(file, debug=False, version=2):
        """
         3 Float32 values, hence 12 bytes, with following fields
            acceleration (x,y,z)
        """
        chunk = file.read(12)
        data = struct.unpack("<3f", chunk)
        if debug:
            print('RAW ACCELERO: ', data)
        return data

    @staticmethod
    def read_raw_gyro_data(file, debug=False, version=2):
        """
         3 Float32 values, hence 12 bytes, with following fields
            gyroscope (x,y,z)
        """
        chunk = file.read(12)
        data = struct.unpack("<3f", chunk)
        if debug:
            print('RAW GYRO: ', data)
        return data

    @staticmethod
    def read_pedometer_data(file, debug=False, version=2):
        """
         - Number of steps:     uint32
         - Distance:            float32, -1.0 if the value is not available on device
         - Average active pace: float32, -1.0 if the value is not available on device
         - Current pace:        float32, -1.0 if the value is not available on device
         - Current cadence:     float32, -1.0 if the value is not available on device
         - Floors ascended:     int32, -1.0 if the value is not available on device
         - Floors descended:    int32, -1.0 if the value is not available on device
        """
        chunk = file.read(28)
        data = struct.unpack("<1I4f2i", chunk)
        if debug:
            print("RAW PEDOMETER: ", data)
        return data

    @staticmethod
    def read_activity_data(file, debug=False, version=2):
        """
        Detected Activities: UInt8 -- 1 byte: Detected activities and confidence level:
            Bits 0-1: Confidence level:
                00 : low
                01 : medium
                10 : high
            Bit 2: Automative activity detected
            Bit 3: Cycling activity detected
            Bit 4: Running activity detected
            Bit 5: Stationary activity detected
            Bit 6: Walking activity detected
            Bit 7: Unknown activity detected
        """
        chunk = file.read(1)
        data = struct.unpack("<1B", chunk)
        if debug:
            print("RAW ACTIVITY: ", data)
        return data

    @staticmethod
    def read_headings_data(file, debug=False, version=2):
        """
        True Heading: Float32 -- 4 bytes: Heading in degrees relative to true north (0 = North, 180 = South). Only valid if "True Heading Accuracy" is positive.
        True Heading Accuracy: Float32 -- 4 bytes: Accuracy in degrees of "True Heading", with negative values representing unreliable or uncalibrated sensor.
        Magnetic Heading: Float32 -- 4 bytes: Heading in degrees relative to magnetic north.
        Magnetometer x-data: Float32 -- 4 bytes: x-value of magnetometer (microTeslas)
        Magnetometer y-data: Float32 -- 4 bytes: y-value of magnetometer (microTeslas)
        Magnetometer z-data: Float32 -- 4 bytes: z-value of magnetometer (microTeslas)
        """
        chunk = file.read(24)
        data = struct.unpack("<6f", chunk)
        if debug:
            print("HEADINGS: ", data)
        return data

    @staticmethod
    def read_health_data(file, debug=False, version=2):
        """
        Start Timestamp: UInt64 -- 8 bytes: Sample start timestamp (Unix format) with milliseconds precision
        End Timestamp: UInt64 -- 8 bytes: Sample end timestamp (Unix format) with milliseconds precision
        Type index: UInt16 -- 2 byte: Index of the type of this sample in the list of types from the given settings list (see above)
        Value: Float64 -- 8 bytes: Value of the sample. Units are defined by the type of the sample (see above).
        """
        chunk = file.read(26)
        data = struct.unpack("<2Q1H1d", chunk)
        if debug:
            print("HEALTH: ", data)
        return data

    @staticmethod
    def read_raw_magneto_data(file, debug=False, version=2):
        """
        Magnetometer x-data: Float32 -- 4 bytes: Magnetometer data for x-axis (microTeslas)
        Magnetometer y-data: Float32 -- 4 bytes: Magnetometer data for y-axis (microTeslas)
        Magnetometer z-data: Float32 -- 4 bytes: Magnetometer data for z-axis (microTeslas)
        """
        chunk = file.read(12)
        data = struct.unpack("<3f", chunk)
        if debug:
            print('RAW MAGNETO: ', data)
        return data

    @staticmethod
    def read_tremor_data(file, debug=False, version=2):
        """
        Start Timestamp: Uint64 -- 8 bytes: Timestamp (Unix format) with milliseconds precision on which the measurement started
        End Timestamp: Uint64 -- 8 bytes: Timestamp (Unix format) with milliseconds precision on which the measurement ended
        No Tremor Ratio: Float32 -- 4 bytes: Ratio of time where no tremor where detected, between 0 and 1
        Slight Tremor Ratio: Float32 -- 4 bytes: Ratio of time where slight tremors where detected, between 0 and 1
        Mild Tremor Ratio: Float32 -- 4 bytes: Ratio of time where mild tremors where detected, between 0 and 1
        Moderate Tremor Ratio: Float32 -- 4 bytes: Ratio of time where moderate tremors where detected, between 0 and 1
        Strong Tremor Ratio: Float32 -- 4 bytes: Ratio of time where strong tremors where detected, between 0 and 1
        """
        chunk = file.read(36)
        data = struct.unpack("<2Q<4f", chunk)
        if debug:
            print('TREMOR: ', data)
        return data

    @staticmethod
    def read_dyskinetic_data(file, debug=False, version=2):
        """
        Start Timestamp: Uint64 -- 8 bytes: Timestamp (Unix format) with milliseconds precision on which the measurement started
        End Timestamp: Uint64 -- 8 bytes: Timestamp (Unix format) with milliseconds precision on which the measurement ended
        Percent likely: Float32 -- 4 bytes: Percent likely that there is dyskinetic movements
        """
        chunk = file.read(20)
        data = struct.unpack("<2Q<1f", chunk)
        if debug:
            print('DYSKINETIC: ', data)
        return data

    @staticmethod
    def read_prompt_data(file, debug=False, version=2):
        """
        Prompt ID size: UInt16 -- 2 bytes: Size of prompt ID string (N)
        Prompt ID: String -- N bytes: Prompt identifier
        Results size: UInt16 -- 2 bytes: Size of the results array (RN)
        Results: UInt16 -- RN*2 bytes: Selected results (index of the selected answer in the list of answers)
        Shown timestamp: UInt64 -- 8 bytes: Timestamp (Unix format) with milliseconds precision of the prompt first displaying to user.
        """
        chunk = file.read(2)
        size = struct.unpack("<1H", chunk)[0]
        chunk = file.read(size)
        # Question id
        data = struct.unpack("<" + str(size) + "s", chunk)
        # Question answers
        chunk = file.read(2)
        data += struct.unpack("<1H", chunk)
        # Browse each answer and put them in a list
        size = data[-1]
        for i in range(size):
            chunk = file.read(2)
            data += struct.unpack("<1H", chunk)
        chunk = file.read(8)
        data += struct.unpack("<1Q", chunk)
        if debug:
            print('PROMPT: ', data)
        return data
