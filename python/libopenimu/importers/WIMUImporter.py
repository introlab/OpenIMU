from libopenimu.importers.BaseImporter import BaseImporter

import libopenimu.importers.wimu as wimu

from libopenimu.tools.timing import timing
from libopenimu.db.DBManager import DBManager
from libopenimu.models.Participant import Participant



class WIMUImporter(BaseImporter):
    def __init__(self, manager: DBManager, participant: Participant):
        super().__init__(manager, participant)
        print('WIMU Importer')

    @timing
    def load(self, filename):
        print('WIMUImporter loading:', filename)
        result = wimu.wimu_importer(filename)
        return result

    @timing
    def import_to_database(self, results):

        # config = result['config']

        # TODO UPDATE THIS IMPORTER FOR THE NEW TIMESTAMP FORMAT IN DATABASE!
        # start_timestamp = datetime.datetime.now()
        # end_timestamp = datetime.datetime.now()

        # recordset = self.add_recordset_to_db('unknown', start_timestamp, end_timestamp)

        if results.__contains__('acc'):

            # Create sensor
            """accelerometer_sensor = self.add_sensor_to_db(SensorType.ACCELEROMETER, 'Accelerometer',
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

                self.db.flush()"""

        if results.__contains__('gyr'):
            # Create sensor
            """gyro_sensor = self.add_sensor_to_db(SensorType.GYROMETER, 'Gyro',
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
                        # self.add_sensor_data_to_db(recordset, gyro_sensor, gyro_channels[0],
                        #                           datetime.datetime.fromtimestamp(timestamp),
                        #                           datetime.datetime.fromtimestamp(end_timestamp), gyro_x)

                    if len(gyro_y) > 0:
                        data_len = len(gyro_y) / config.general.sampling_rate
                        end_timestamp = timestamp + data_len
                        # self.add_sensor_data_to_db(recordset, gyro_sensor, gyro_channels[1],
                        #                          datetime.datetime.fromtimestamp(timestamp),
                        #                           datetime.datetime.fromtimestamp(end_timestamp), gyro_y)

                    if len(gyro_z) > 0:
                        data_len = len(gyro_z) / config.general.sampling_rate
                        end_timestamp = timestamp + data_len
                        self.add_sensor_data_to_db(recordset, gyro_sensor, gyro_channels[2],
                                                   datetime.datetime.fromtimestamp(timestamp),
                                                   datetime.datetime.fromtimestamp(end_timestamp), gyro_z)

                self.db.flush()"""

            if results.__contains__('mag'):
                # Create sensor
                """mag_sensor = self.add_sensor_to_db(SensorType.MAGNETOMETER, 'Magneto',
                                                    'WIMUGPS',
                                                    'Unknown', config.general.sampling_rate, 1)

                mag_channels = list()

                # Create channels
                mag_channels.append(self.add_channel_to_db(mag_sensor, Units.GAUSS,
                                                            DataFormat.FLOAT32, 'Magneto_X'))

                mag_channels.append(self.add_channel_to_db(mag_sensor, Units.GAUSS,
                                                            DataFormat.FLOAT32, 'Magneto_Y'))

                mag_channels.append(self.add_channel_to_db(mag_sensor, Units.GAUSS,
                                                            DataFormat.FLOAT32, 'Magneto_Z'))

                for item in result['mag']:

                    # We have a list of list
                    for record in item:
                        [timestamp, mag_dict] = record
                        mag_x = mag_dict['magneto_x']
                        mag_y = mag_dict['magneto_y']
                        mag_z = mag_dict['magneto_z']

                        recordset = self.get_recordset(timestamp)

                        # Update end_timestamp if required
                        if timestamp > recordset.end_timestamp.timestamp():
                            recordset.end_timestamp = datetime.datetime.fromtimestamp(timestamp)

                        if len(mag_x) > 0:
                            data_len = len(mag_x) / config.general.sampling_rate
                            end_timestamp = timestamp + data_len
                            self.add_sensor_data_to_db(recordset, mag_sensor, mag_channels[0],
                                                       datetime.datetime.fromtimestamp(timestamp),
                                                       datetime.datetime.fromtimestamp(end_timestamp), mag_x)

                        if len(mag_y) > 0:
                            data_len = len(mag_y) / config.general.sampling_rate
                            end_timestamp = timestamp + data_len
                            self.add_sensor_data_to_db(recordset, mag_sensor, mag_channels[1],
                                                       datetime.datetime.fromtimestamp(timestamp),
                                                       datetime.datetime.fromtimestamp(end_timestamp), mag_y)

                        if len(mag_z) > 0:
                            data_len = len(mag_z) / config.general.sampling_rate
                            end_timestamp = timestamp + data_len
                            self.add_sensor_data_to_db(recordset, mag_sensor, mag_channels[2],
                                                       datetime.datetime.fromtimestamp(timestamp),
                                                       datetime.datetime.fromtimestamp(end_timestamp), mag_z)

                    self.db.flush()"""

            if results.__contains__('imu'):

                # Create sensor
                """imu_sensor = self.add_sensor_to_db(SensorType.ORIENTATION, 'Orientation',
                                                             'WIMUGPS',
                                                             'Unknown', config.general.sampling_rate, 1)

                imu_channels = list()

                # Create channels
                imu_channels.append(self.add_channel_to_db(imu_sensor, Units.NONE, DataFormat.FLOAT32, 'Q0'))
                imu_channels.append(self.add_channel_to_db(imu_sensor, Units.NONE, DataFormat.FLOAT32, 'Q1'))
                imu_channels.append(self.add_channel_to_db(imu_sensor, Units.NONE, DataFormat.FLOAT32, 'Q2'))
                imu_channels.append(self.add_channel_to_db(imu_sensor, Units.NONE, DataFormat.FLOAT32, 'Q3'))

                for item in result['imu']:

                    # We have a list of list
                    for record in item:
                        [timestamp, acc_dict] = record
                        q0 = acc_dict['q0']
                        q1 = acc_dict['q1']
                        q2 = acc_dict['q2']
                        q3 = acc_dict['q3']

                        recordset = self.get_recordset(timestamp)

                        # Update end_timestamp if required
                        if timestamp > recordset.end_timestamp.timestamp():
                            recordset.end_timestamp = datetime.datetime.fromtimestamp(timestamp)

                        if len(q0) > 0:
                            data_len = len(q0) / config.general.sampling_rate
                            end_timestamp = timestamp + data_len
                            self.add_sensor_data_to_db(recordset, imu_sensor, imu_channels[0],
                                                       datetime.datetime.fromtimestamp(timestamp),
                                                       datetime.datetime.fromtimestamp(end_timestamp), q0)

                        if len(q1) > 0:
                            data_len = len(q1) / config.general.sampling_rate
                            end_timestamp = timestamp + data_len
                            self.add_sensor_data_to_db(recordset, imu_sensor, imu_channels[1],
                                                       datetime.datetime.fromtimestamp(timestamp),
                                                       datetime.datetime.fromtimestamp(end_timestamp), q1)

                        if len(q2) > 0:
                            data_len = len(q2) / config.general.sampling_rate
                            end_timestamp = timestamp + data_len
                            self.add_sensor_data_to_db(recordset, imu_sensor, imu_channels[2],
                                                       datetime.datetime.fromtimestamp(timestamp),
                                                       datetime.datetime.fromtimestamp(end_timestamp), q2)

                        if len(q3) > 0:
                            data_len = len(q3) / config.general.sampling_rate
                            end_timestamp = timestamp + data_len
                            self.add_sensor_data_to_db(recordset, imu_sensor, imu_channels[3],
                                                       datetime.datetime.fromtimestamp(timestamp),
                                                       datetime.datetime.fromtimestamp(end_timestamp), q3)

                    self.db.flush()"""

            if results.__contains__('pow'):
                """temp_sensor = self.add_sensor_to_db(SensorType.TEMPERATURE, 'Temperature', 'WIMUGPS', 'Unknown', 1.0, 1)
                temp_channel = self.add_channel_to_db(temp_sensor, Units.CELCIUS, DataFormat.FLOAT32, 'Temperature')

                batt_sensor = self.add_sensor_to_db(SensorType.BATTERY, 'Battery', 'WIMUGPS', 'Unknown', 1.0, 1)
                batt_channel = self.add_channel_to_db(batt_sensor, Units.VOLTS, DataFormat.FLOAT32, 'Level')

                #TODO: Power status.

                for item in result['pow']:
                    for record in item:
                        [timestamp, pow_dict] = record

                        temperature = pow_dict['temperature']
                        battery = pow_dict['battery']

                        recordset = self.get_recordset(timestamp)

                        # Update end_timestamp if required
                        if timestamp > recordset.end_timestamp.timestamp():
                            recordset.end_timestamp = datetime.datetime.fromtimestamp(timestamp)

                        self.add_sensor_data_to_db(recordset, temp_sensor, temp_channel,
                                                   datetime.datetime.fromtimestamp(timestamp),
                                                   datetime.datetime.fromtimestamp(timestamp+len(temperature)),temperature)

                        self.add_sensor_data_to_db(recordset, batt_sensor, batt_channel,
                                                   datetime.datetime.fromtimestamp(timestamp),
                                                   datetime.datetime.fromtimestamp(timestamp + len(battery)),
                                                   battery)

                    self.db.flush()"""

            if results.__contains__('gps'):

                """gps_sensor = self.add_sensor_to_db(SensorType.GPS, 'GPS',
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

                self.db.flush()"""

        # Write data to file
        self.db.commit()
