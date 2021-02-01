
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

    @timing
    def import_to_database(self, results):
        [info, data] = results

        # print(info)

        # Creating recordset
        # print(info['Start Date'], info['Last Sample Time'])
        # start = int(info['Start Date'])
        # stop = int(info['Last Sample Time'])

        # start_timestamp = ticksconverter(start)
        # end_timestamp = ticksconverter(stop)

        # all_counts = [0, 0, 0]
        if data.__contains__('activity'):

            # print('activity found')
            # Create sensor
            accelerometer_sensor = self.add_sensor_to_db(SensorType.ACCELEROMETER, 'Accelerometer', info['Device Type'],
                                                         'Unknown', info['Sample Rate'], 1)

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
            for epoch in data['activity']:
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

        if data.__contains__('battery'):
            # print('battery found')
            # Create sensor
            volt_sensor = self.add_sensor_to_db(SensorType.BATTERY, 'Battery', info['Device Type'], 'Unknown',
                                                0, 1)

            # Create channel
            volt_channel = self.add_channel_to_db(volt_sensor, Units.VOLTS, DataFormat.FLOAT32, 'Battery')

            for epoch in data['battery']:
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

                self.add_sensor_data_to_db(recordset, volt_sensor, volt_channel, sensor_timestamps, value)

            # Flush to DB (ram)
            self.db.flush()

        if data.__contains__('lux'):
            # print('lux found')
            # Create sensor
            lux_sensor = self.add_sensor_to_db(SensorType.LUX, 'Lux', info['Device Type'], 'Unknown', 0, 1)

            # Create channel
            lux_channel = self.add_channel_to_db(lux_sensor, Units.LUX, DataFormat.FLOAT32, 'Lux')

            for epoch in data['lux']:
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

        # Write data to file
        self.db.commit()

        self.update_progress.emit(100)
