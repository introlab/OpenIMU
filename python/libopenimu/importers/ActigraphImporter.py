
"""
    Actigraph data importer
    @authors Dominic Létourneau
    @date 18/04/2018

"""

from libopenimu.importers.BaseImporter import BaseImporter
from libopenimu.db.DBManager import DBManager
from libopenimu.models.Participant import Participant
import libopenimu.importers.actigraph as actigraph


from libopenimu.models.sensor_types import SensorType
from libopenimu.models.units import Units
from libopenimu.models.data_formats import DataFormat
from libopenimu.tools.timing import timing
from libopenimu.models.SensorTimestamps import SensorTimestamps

import numpy as np
import datetime


class ActigraphImporter(BaseImporter):
    def __init__(self, manager: DBManager, participant: Participant):
        super().__init__(manager, participant)

        print('Actigraph Importer')

    def get_recordset(self, timestamp, session_name=str()):
        try:
            my_time = datetime.datetime.fromtimestamp(timestamp)
        except ValueError:
            return None

        # Validate timestamp
        if my_time > datetime.datetime.now() or my_time < datetime.datetime(2000, 1, 1):
            print("Invalid timestamp: " + str(timestamp))
            return None

        # Find a record the same day
        for record in self.recordsets:
            # Same date return this record
            if record.start_timestamp.date() == my_time.date():
                # print('Returning existing recordset', record.start_timestamp.date(), my_time.date())
                return record

        # Return new record
        # print('New recordset', my_time, my_time)
        recordset = self.db.add_recordset(self.participant, session_name, my_time, my_time, True)
        self.recordsets.append(recordset)
        return recordset

    @timing
    def load(self, filename):
        # print('ActigraphImporter loading:', filename)
        result = actigraph.gt3x_importer(filename)
        self.update_progress.emit(50)
        return result

    def import_activity_to_database(self, info, activity: dict):
        # print('activity found')
        # Create sensor
        accelerometer_sensor = self.add_sensor_to_db(SensorType.ACCELEROMETER, 'Accelerometer', info['Device Type'],
                                                     'Activity', info['Sample Rate'], 1)

        accelerometer_channels = list()

        # Create channels
        accelerometer_channels.append(self.add_channel_to_db(accelerometer_sensor, Units.GRAVITY_G,
                                                             DataFormat.FLOAT32, 'Accelerometer_Y'))

        accelerometer_channels.append(self.add_channel_to_db(accelerometer_sensor, Units.GRAVITY_G,
                                                             DataFormat.FLOAT32, 'Accelerometer_X'))

        accelerometer_channels.append(self.add_channel_to_db(accelerometer_sensor, Units.GRAVITY_G,
                                                             DataFormat.FLOAT32, 'Accelerometer_Z'))

        # Should be 1970, epoch
        last_timestamp = 0
        all_timestamps = []
        value_dict = {}

        # Import data
        for epoch in activity:
            # An epoch will contain a timestamp and array with each acc_x, acc_y, acc_z

            current_timestamp = epoch[0]
            # print('current_timestamp', current_timestamp, current_timestamp == (last_timestamp + 1))

            # Check for consecutive timestamps
            create_array = current_timestamp != (last_timestamp + 1)

            # Do not allow more than one hour of consecutive data
            if create_array is not True:
                if current_timestamp - all_timestamps[-1] >= 3600:
                    create_array = True

            # Consecutive timestamps?
            if create_array is True:
                all_timestamps.append(current_timestamp)
                # Create list for all values for this timestamp
                value_dict[current_timestamp] = [list(), list(), list()]

            # Get data
            samples = epoch[1]

            # Separate write for each channel
            for index in range(0, len(accelerometer_channels)):
                # Using last timestamp to append data
                value_dict[all_timestamps[-1]][index].append(samples[:, index])
                # print("samples shape", samples.shape, samples[:, index].shape)

            # Update timestamp
            last_timestamp = current_timestamp

        # Insert into DB as chunks of data
        # print('should insert records count: ', len(all_timestamps))
        # print('should insert data count:', len(value_dict))
        counters = [0, 0, 0]

        for timestamp in all_timestamps:
            session_name = str(timestamp) + '_' + info['Device Type'] + '_' \
                           + info['Subject Name'] + '_SN:' + info['Serial Number']

            for index in range(0, len(value_dict[timestamp])):
                # print(index, timestamp, len(value_dict[timestamp][index]))
                vector = np.concatenate(value_dict[timestamp][index])
                # print('inserting values :', len(value_dict[timestamp][index]))
                # print('vector: ', len(vector), vector.shape, vector.dtype)

                # Create sensor timestamps first
                sensor_timestamps = SensorTimestamps()

                # Create time vector
                # TODO Share time vector for all accelerometers?
                timevect = np.linspace(timestamp, timestamp + len(value_dict[timestamp][index]),
                                       num=len(vector), endpoint=False, dtype=np.float64)
                sensor_timestamps.timestamps = timevect
                sensor_timestamps.update_timestamps()

                recordset = self.get_recordset(timestamp, session_name)

                # Update end_timestamp if required
                if timestamp > recordset.end_timestamp.timestamp():
                    recordset.end_timestamp = datetime.datetime.fromtimestamp(timestamp)

                counters[index] += len(vector)
                if len(vector) > 0:
                    self.add_sensor_data_to_db(recordset, accelerometer_sensor, accelerometer_channels[index],
                                               sensor_timestamps, vector)

        # print('total samples inserted:', counters)
        # print('total timestamps processed:', len(all_timestamps))

        # Flush DB
        self.db.flush()

    def import_battery_to_database(self, info, battery: dict):
        # Create sensor
        volt_sensor = self.add_sensor_to_db(SensorType.BATTERY, 'Battery', info['Device Type'], 'General',
                                            10, 1)

        # Create channel
        volt_channel = self.add_channel_to_db(volt_sensor, Units.VOLTS, DataFormat.FLOAT32, 'Battery')

        for epoch in battery:
            timestamp = datetime.datetime.fromtimestamp(epoch[0])
            session_name = str(timestamp) + '_' + info['Device Type'] + '_' + info['Subject Name'] \
                                          + '_SN:' + info['Serial Number']
            value = np.float32(epoch[1])

            recordset = self.get_recordset(epoch[0], session_name)

            timevect = np.linspace(epoch[0], epoch[0] + 1, num=1, endpoint=False, dtype=np.float64)
            # Create sensor timestamps first
            sensor_timestamps = SensorTimestamps()
            sensor_timestamps.timestamps = timevect
            sensor_timestamps.update_timestamps()

            # Update end_timestamp if required
            if epoch[0] > recordset.end_timestamp.timestamp():
                recordset.end_timestamp = timestamp

            self.add_sensor_data_to_db(recordset, volt_sensor, volt_channel, sensor_timestamps, value)

        # Flush to DB (ram)
        self.db.flush()

    def import_lux_to_database(self, info, lux: dict):
        # Create sensor
        lux_sensor = self.add_sensor_to_db(SensorType.LUX, 'Lux', info['Device Type'], 'Unknown', 0, 1)

        # Create channel
        lux_channel = self.add_channel_to_db(lux_sensor, Units.LUX, DataFormat.FLOAT32, 'Lux')

        for epoch in lux:
            timestamp = datetime.datetime.fromtimestamp(epoch[0])
            session_name = str(timestamp) + '_' + info['Device Type'] + '_' \
                           + info['Subject Name'] + '_SN:' + info['Serial Number']
            value = np.float32(epoch[1])

            recordset = self.get_recordset(epoch[0], session_name)

            timevect = np.linspace(epoch[0], epoch[0] + 1, num=1, endpoint=False, dtype=np.float64)
            # Create sensor timestamps first
            sensor_timestamps = SensorTimestamps()
            sensor_timestamps.timestamps = timevect
            sensor_timestamps.update_timestamps()

            # Update end_timestamp if required
            if epoch[0] > recordset.end_timestamp.timestamp():
                recordset.end_timestamp = timestamp

            self.add_sensor_data_to_db(recordset, lux_sensor, lux_channel, sensor_timestamps, value)

        # Flush to DB (ram)
        self.db.flush()

    def import_sensor_data_to_database(self, info, sensor_data: dict):
        if len(sensor_data) == 0:
            return

        accelerometer_sensor = None
        gyroscope_sensor = None
        magneto_sensor = None
        temp_sensor = None

        accelerometer_channels = list()
        gyroscope_channels = list()
        magneto_channels = list()
        temp_channel = None

        # Create channels for sensors
        sensor_names = sensor_data[0][1].keys()
        for sensor in sensor_names:
            if sensor == 'Accelerometer':
                # Create sensor
                accelerometer_sensor = self.add_sensor_to_db(SensorType.ACCELEROMETER, 'Accelerometer',
                                                             info['Device Type'],
                                                             'Other', info['Sample Rate'], 1)

                # Create channels
                accelerometer_channels.append(self.add_channel_to_db(accelerometer_sensor, Units.GRAVITY_G,
                                                                     DataFormat.FLOAT32, 'Accelerometer_X'))

                accelerometer_channels.append(self.add_channel_to_db(accelerometer_sensor, Units.GRAVITY_G,
                                                                     DataFormat.FLOAT32, 'Accelerometer_Y'))

                accelerometer_channels.append(self.add_channel_to_db(accelerometer_sensor, Units.GRAVITY_G,
                                                                     DataFormat.FLOAT32, 'Accelerometer_Z'))
            if sensor == 'Gyroscope':
                # Create sensor
                gyroscope_sensor = self.add_sensor_to_db(SensorType.GYROMETER, 'Gyroscope',
                                                         info['Device Type'], 'Other', info['Sample Rate'],
                                                         1)

                # Create channels
                gyroscope_channels.append(self.add_channel_to_db(gyroscope_sensor, Units.DEG_PER_SEC,
                                                                 DataFormat.FLOAT32, 'Gyroscope_X'))

                gyroscope_channels.append(self.add_channel_to_db(gyroscope_sensor, Units.DEG_PER_SEC,
                                                                 DataFormat.FLOAT32, 'Gyroscope_Y'))

                gyroscope_channels.append(self.add_channel_to_db(gyroscope_sensor, Units.DEG_PER_SEC,
                                                                 DataFormat.FLOAT32, 'Gyroscope_Z'))
            if sensor == 'Magnetometer':
                # Create sensor
                magneto_sensor = self.add_sensor_to_db(SensorType.MAGNETOMETER, 'Magnetometer',
                                                       info['Device Type'], 'Other', info['Sample Rate'], 1)

                # Create channels
                magneto_channels.append(self.add_channel_to_db(magneto_sensor, Units.UTESLA,
                                                               DataFormat.FLOAT32, 'Magnetometer_X'))

                magneto_channels.append(self.add_channel_to_db(magneto_sensor, Units.UTESLA,
                                                               DataFormat.FLOAT32, 'Magnetometer_Y'))

                magneto_channels.append(self.add_channel_to_db(magneto_sensor, Units.UTESLA,
                                                               DataFormat.FLOAT32, 'Magnetometer_Z'))
            if sensor == 'Temperature':
                # Create sensor
                temp_sensor = self.add_sensor_to_db(SensorType.TEMPERATURE, 'Temperature',
                                                    info['Device Type'], 'Other', info['Sample Rate'], 1)

                temp_channel = self.add_channel_to_db(temp_sensor, Units.CELCIUS, DataFormat.FLOAT32,
                                                      'Temperature')

        # Reshape data vectors
        data_times = [data[0] for data in sensor_data]

        acc_data = []
        gyro_data = []
        mag_data = []
        temp_data = []
        if 'Accelerometer' in sensor_names:
            values = [data[1]['Accelerometer'] for data in sensor_data]

            for index, value in enumerate(values):
                timevect = np.linspace(data_times[index], data_times[index] + 1, num=len(value), endpoint=False,
                                       dtype=np.float64)
                shaped_values = np.reshape(value, [-1, 3])
                acc_data.extend(list(zip(timevect, shaped_values)))

        if 'Gyroscope' in sensor_names:
            values = [data[1]['Gyroscope'] for data in sensor_data]

            for index, value in enumerate(values):
                timevect = np.linspace(data_times[index], data_times[index] + 1, num=len(value), endpoint=False,
                                       dtype=np.float64)
                shaped_values = np.reshape(value, [-1, 3])
                gyro_data.extend(list(zip(timevect, shaped_values)))

        if 'Magnetometer' in sensor_names:
            values = [data[1]['Magnetometer'] for data in sensor_data]

            for index, value in enumerate(values):
                timevect = np.linspace(data_times[index], data_times[index] + 1, num=len(value), endpoint=False,
                                       dtype=np.float64)
                shaped_values = np.reshape(value, [-1, 3])
                mag_data.extend(list(zip(timevect, shaped_values)))

        if 'Temperature' in sensor_names:
            values = [data[1]['Temperature'] for data in sensor_data]

            for index, value in enumerate(values):
                timevect = np.linspace(data_times[index], data_times[index] + 1, num=len(value), endpoint=False,
                                       dtype=np.float64)
                temp_data.extend(list(zip(timevect, value)))

        # Find holes in the recording
        split_indexes = [0]
        split_indexes.extend([index+1 for index, value in enumerate(np.diff(data_times)) if value != 1])
        split_indexes.append(len(data_times)-1)

        # Find chunks of data longer than 1h
        indexes_to_add = []
        for index in range(1, len(split_indexes)):
            if (split_indexes[index] - split_indexes[index-1]) > 3600:
                current_index = split_indexes[index-1]
                while current_index < split_indexes[index]:
                    current_index += 3600
                    if current_index < split_indexes[-1]:
                        indexes_to_add.append(current_index)

        split_indexes.extend(indexes_to_add)
        split_indexes.sort()

        if 'Accelerometer' in sensor_names:
            # Detect hours transition to prevent recordset from being longer than 1h
            for record_index in range(1, len(split_indexes)):
                if record_index == len(split_indexes):
                    next_cut_timestamp = acc_data[-1][0]+1
                else:
                    next_cut_timestamp = data_times[split_indexes[record_index]]
                current_timestamp = data_times[split_indexes[record_index-1]]
                data_recordset = [data for data in acc_data if current_timestamp <= data[0] < next_cut_timestamp]

                base_timestamp = data_recordset[0][0]
                session_name = str(base_timestamp) + '_' + info['Device Type'] + '_' \
                                                   + info['Subject Name'] + '_SN:' + info['Serial Number']

                recordset = self.get_recordset(base_timestamp, session_name)

                # Create sensor timestamps first
                sensor_timestamps = SensorTimestamps()
                sensor_timestamps.timestamps = np.asarray([row[0] for row in data_recordset], dtype=np.float64)
                sensor_timestamps.update_timestamps()

                # Update end_timestamp if required
                if base_timestamp > recordset.end_timestamp.timestamp():
                    recordset.end_timestamp = base_timestamp

                for index in range(0, len(accelerometer_channels)):
                    values = np.asarray([row[1][index] for row in data_recordset], dtype=np.float32)
                    self.add_sensor_data_to_db(recordset, accelerometer_sensor, accelerometer_channels[index],
                                               sensor_timestamps, values)

        if 'Gyroscope' in sensor_names:
            # Detect hours transition to prevent recordset from being longer than 1h
            for record_index in range(1, len(split_indexes)):
                if record_index == len(split_indexes):
                    next_cut_timestamp = gyro_data[-1][0] + 1
                else:
                    next_cut_timestamp = data_times[split_indexes[record_index]]
                current_timestamp = data_times[split_indexes[record_index - 1]]
                data_recordset = [data for data in gyro_data if current_timestamp <= data[0] < next_cut_timestamp]

                base_timestamp = data_recordset[0][0]
                session_name = str(base_timestamp) + '_' + info['Device Type'] + '_' \
                               + info['Subject Name'] + '_SN:' + info['Serial Number']

                recordset = self.get_recordset(base_timestamp, session_name)

                # Create sensor timestamps first
                sensor_timestamps = SensorTimestamps()
                sensor_timestamps.timestamps = np.asarray([row[0] for row in data_recordset], dtype=np.float64)
                sensor_timestamps.update_timestamps()

                # Update end_timestamp if required
                if base_timestamp > recordset.end_timestamp.timestamp():
                    recordset.end_timestamp = base_timestamp

                for index in range(0, len(gyroscope_channels)):
                    values = np.asarray([row[1][index] for row in data_recordset], dtype=np.float32)
                    self.add_sensor_data_to_db(recordset, gyroscope_sensor, gyroscope_channels[index],
                                               sensor_timestamps, values)

                next_cut_timestamp += 3600

        if 'Magnetometer' in sensor_names:
            # Detect hours transition to prevent recordset from being longer than 1h
            for record_index in range(1, len(split_indexes)):
                if record_index == len(split_indexes):
                    next_cut_timestamp = mag_data[-1][0] + 1
                else:
                    next_cut_timestamp = data_times[split_indexes[record_index]]
                current_timestamp = data_times[split_indexes[record_index - 1]]
                data_recordset = [data for data in mag_data if current_timestamp <= data[0] < next_cut_timestamp]

                base_timestamp = data_recordset[0][0]
                session_name = str(base_timestamp) + '_' + info['Device Type'] + '_' \
                               + info['Subject Name'] + '_SN:' + info['Serial Number']

                recordset = self.get_recordset(base_timestamp, session_name)

                # Create sensor timestamps first
                sensor_timestamps = SensorTimestamps()
                sensor_timestamps.timestamps = np.asarray([row[0] for row in data_recordset], dtype=np.float64)
                sensor_timestamps.update_timestamps()

                # Update end_timestamp if required
                if base_timestamp > recordset.end_timestamp.timestamp():
                    recordset.end_timestamp = base_timestamp

                for index in range(0, len(magneto_channels)):
                    values = np.asarray([row[1][index] for row in data_recordset], dtype=np.float32)
                    self.add_sensor_data_to_db(recordset, magneto_sensor, magneto_channels[index],
                                               sensor_timestamps, values)

                next_cut_timestamp += 3600

        if 'Temperature' in sensor_names:
            # Detect hours transition to prevent recordset from being longer than 1h
            for record_index in range(1, len(split_indexes)):
                if record_index == len(split_indexes):
                    next_cut_timestamp = temp_data[-1][0] + 1
                else:
                    next_cut_timestamp = data_times[split_indexes[record_index]]
                current_timestamp = data_times[split_indexes[record_index - 1]]
                data_recordset = [data for data in temp_data if current_timestamp <= data[0] < next_cut_timestamp]
                base_timestamp = data_recordset[0][0]
                session_name = str(base_timestamp) + '_' + info['Device Type'] + '_' \
                               + info['Subject Name'] + '_SN:' + info['Serial Number']

                recordset = self.get_recordset(base_timestamp, session_name)

                # Create sensor timestamps first
                sensor_timestamps = SensorTimestamps()
                sensor_timestamps.timestamps = np.asarray([row[0] for row in data_recordset], dtype=np.float64)
                sensor_timestamps.update_timestamps()

                # Update end_timestamp if required
                if base_timestamp > recordset.end_timestamp.timestamp():
                    recordset.end_timestamp = base_timestamp

                values = np.asarray([row[1] for row in data_recordset], dtype=np.float32)
                self.add_sensor_data_to_db(recordset, temp_sensor, temp_channel, sensor_timestamps, values)

                next_cut_timestamp += 3600

        # Flush DB
        self.db.flush()

    @timing
    def import_to_database(self, results):
        [info, data] = results

        if data.__contains__('activity'):
            self.import_activity_to_database(info, data['activity'])

        if data.__contains__('battery'):
            # print('battery found')
            self.import_battery_to_database(info, data['battery'])

        if data.__contains__('lux'):
            # print('lux found')
            self.import_lux_to_database(info, data['lux'])

        if data.__contains__('sensor_data'):
            self.import_sensor_data_to_database(info, data['sensor_data'])

        # Write data to file
        self.db.commit()

        self.update_progress.emit(100)
