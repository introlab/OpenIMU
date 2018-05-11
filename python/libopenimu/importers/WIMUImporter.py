from libopenimu.importers.BaseImporter import BaseImporter

import libopenimu.importers.wimu as wimu


from libopenimu.models.sensor_types import SensorType
from libopenimu.models.units import Units
from libopenimu.models.Recordset import Recordset
from libopenimu.models.data_formats import DataFormat
from libopenimu.tools.timing import timing
from libopenimu.db.DBManager import DBManager
from libopenimu.models.Participant import Participant

import numpy as np
import datetime


class WIMUImporter(BaseImporter):
    def __init__(self, manager: DBManager, participant: Participant):
        super().__init__(manager, participant)
        print('WIMU Importer')
        # No recordsets when starting
        self.recordsets = []

    @timing
    def load(self, filename):
        print('WIMUImporter loading:', filename)
        result = wimu.wimu_importer(filename)
        return result

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
    def import_to_database(self, result):

        config = result['config']

        # TODO Update those values
        start_timestamp = datetime.datetime.now()
        end_timestamp = datetime.datetime.now()

        # recordset = self.add_recordset_to_db('unknown', start_timestamp, end_timestamp)

        if result.__contains__('acc'):

            # Create sensor
            accelerometer_sensor = self.add_sensor_to_db(SensorType.ACCELEROMETER, 'Accelerometer',
                                                         'WIMUGPS',
                                                         'Unknown', config.general.sampling_rate, 1)

            accelerometer_channels = list()

            # Create channels
            accelerometer_channels.append(self.add_channel_to_db(accelerometer_sensor, Units.GRAVITY_G,
                                                                 DataFormat.FLOAT32, 'Accelerometer_X'))

            accelerometer_channels.append(self.add_channel_to_db(accelerometer_sensor, Units.GRAVITY_G,
                                                                 DataFormat.FLOAT32, 'Accelerometer_Y'))

            accelerometer_channels.append(self.add_channel_to_db(accelerometer_sensor, Units.GRAVITY_G,
                                                                 DataFormat.FLOAT32, 'Accelerometer_Z'))

            for item in result['acc']:

                # We have a list of list
                for record in item:
                    [timestamp, acc_dict] = record
                    acc_x = acc_dict['acc_x']
                    acc_y = acc_dict['acc_y']
                    acc_z = acc_dict['acc_z']

                    recordset = self.get_recordset(timestamp)

                    # Update end_timestamp if required
                    if timestamp > recordset.end_timestamp.timestamp():
                        recordset.end_timestamp = datetime.datetime.fromtimestamp(timestamp)

                    if len(acc_x) > 0:
                        data_len = len(acc_x) / config.general.sampling_rate
                        end_timestamp = timestamp + data_len
                        self.add_sensor_data_to_db(recordset, accelerometer_sensor, accelerometer_channels[0],
                                                   datetime.datetime.fromtimestamp(timestamp),
                                                   datetime.datetime.fromtimestamp(end_timestamp), acc_x)

                    if len(acc_y) > 0:
                        data_len = len(acc_y) / config.general.sampling_rate
                        end_timestamp = timestamp + data_len
                        self.add_sensor_data_to_db(recordset, accelerometer_sensor, accelerometer_channels[1],
                                                   datetime.datetime.fromtimestamp(timestamp),
                                                   datetime.datetime.fromtimestamp(end_timestamp), acc_y)

                    if len(acc_z) > 0:
                        data_len = len(acc_z) / config.general.sampling_rate
                        end_timestamp = timestamp + data_len
                        self.add_sensor_data_to_db(recordset, accelerometer_sensor, accelerometer_channels[2],
                                                   datetime.datetime.fromtimestamp(timestamp),
                                                   datetime.datetime.fromtimestamp(end_timestamp), acc_z)

                self.db.flush()

        if result.__contains__('gyr'):
            # Create sensor
            gyro_sensor = self.add_sensor_to_db(SensorType.GYROMETER, 'Gyro',
                                                'WIMUGPS',
                                                'Unknown', config.general.sampling_rate, 1)

            gyro_channels = list()

            # Create channels
            gyro_channels.append(self.add_channel_to_db(gyro_sensor, Units.DEG_PER_SEC,
                                                        DataFormat.FLOAT32, 'Gyro_X'))

            gyro_channels.append(self.add_channel_to_db(gyro_sensor, Units.DEG_PER_SEC,
                                                        DataFormat.FLOAT32, 'Gyro_Y'))

            gyro_channels.append(self.add_channel_to_db(gyro_sensor, Units.DEG_PER_SEC,
                                                        DataFormat.FLOAT32, 'Gyro_Z'))

            for item in result['gyr']:

                # We have a list of list
                for record in item:
                    [timestamp, gyro_dict] = record
                    gyro_x = gyro_dict['gyro_x']
                    gyro_y = gyro_dict['gyro_y']
                    gyro_z = gyro_dict['gyro_z']

                    recordset = self.get_recordset(timestamp)

                    # Update end_timestamp if required
                    if timestamp > recordset.end_timestamp.timestamp():
                        recordset.end_timestamp = datetime.datetime.fromtimestamp(timestamp)

                    if len(gyro_x) > 0:
                        data_len = len(gyro_x) / config.general.sampling_rate
                        end_timestamp = timestamp + data_len
                        self.add_sensor_data_to_db(recordset, gyro_sensor, gyro_channels[0],
                                                   datetime.datetime.fromtimestamp(timestamp),
                                                   datetime.datetime.fromtimestamp(end_timestamp), gyro_x)

                    if len(gyro_y) > 0:
                        data_len = len(gyro_y) / config.general.sampling_rate
                        end_timestamp = timestamp + data_len
                        self.add_sensor_data_to_db(recordset, gyro_sensor, gyro_channels[1],
                                                   datetime.datetime.fromtimestamp(timestamp),
                                                   datetime.datetime.fromtimestamp(end_timestamp), gyro_y)

                    if len(gyro_z) > 0:
                        data_len = len(gyro_z) / config.general.sampling_rate
                        end_timestamp = timestamp + data_len
                        self.add_sensor_data_to_db(recordset, gyro_sensor, gyro_channels[2],
                                                   datetime.datetime.fromtimestamp(timestamp),
                                                   datetime.datetime.fromtimestamp(end_timestamp), gyro_z)

                self.db.flush()

            if result.__contains__('gps'):

                gps_sensor = self.add_sensor_to_db(SensorType.GPS, 'GPS',
                                                   'WIMUGPS',
                                                   'Unknown', 1.0, 1)

                gps_channel = self.add_channel_to_db(gps_sensor, Units.NONE, DataFormat.UINT8, 'GPS_SIRF')

                for item in result['gps']:
                    # GPS item is a dict with key = timestamp, value = geo data
                    for key in item:
                        # print('gps item : ', key)
                        timestamp = key

                        recordset = self.get_recordset(timestamp)

                        self.add_sensor_data_to_db(recordset, gps_sensor, gps_channel,
                                                   datetime.datetime.fromtimestamp(timestamp),
                                                   datetime.datetime.fromtimestamp(timestamp), item[key])

                self.db.flush()

        # Write data to file
        self.db.commit()