"""

    Unit testing for import to DB
    @authors Simon Brière, Dominic Létourneau
    @date 120/04/2018

"""


import unittest
from libopenimu.models.Group import Group
from libopenimu.models.SensorData import SensorData
from libopenimu.models.sensor_types import SensorType
from libopenimu.models.units import Units
from libopenimu.models.data_formats import DataFormat
from libopenimu.db.DBManager import DBManager
from libopenimu.importers.actigraph import gt3x_importer
from libopenimu.tools.timing import datetime_from_dotnet_ticks as ticksconverter
from libopenimu.tools.timing import timing

import numpy as np
import datetime


class ActigraphDBTest1(unittest.TestCase):

    @timing
    def setUp(self):
        np.set_printoptions(suppress=True)
        print(__file__ + ' Creating database')
        self.db = DBManager('actigraph.db', True, False)
        self.group = self.db.add_group('MyGroup', 'MyDescription')
        self.participant = self.db.add_participant(group=self.group, name='Anonymous', description='Participant')

    @timing
    def tearDown(self):
        self.db.commit()

    @timing
    def load_file(self, name='../resources/samples/test.gt3x'):
        print('loading file :', name)
        result = gt3x_importer(name)
        self.assertEqual(len(result), 2)
        return result

    def add_recordset_to_db(self, name, start_timestamp, stop_timestamp):
        recordset = self.db.add_recordset(self.participant, name, start_timestamp, stop_timestamp)
        return recordset

    def add_sensor_to_db(self, sensor_type, name, hw_name, location, sampling_rate, data_rate):
        #  _id_sensor_type, _name, _hw_name, _location, _sampling_rate, _data_rate):
        sensor = self.db.add_sensor(sensor_type, name, hw_name, location, sampling_rate, data_rate)
        return sensor

    def add_channel_to_db(self, sensor, unit, data_format, label):
        channel = self.db.add_channel(sensor, unit, data_format, label)
        return channel

    def add_sensor_data_to_db(self, recordset, sensor, channel, timestamp, data):
        self.db.add_sensor_data(recordset, sensor, channel, timestamp, data)
        # return data

    @timing
    def commit(self):
        return self.db.commit()

    @timing
    def flush(self):
        return self.db.flush()

    def test_import(self):
        # Return file info and data contents
        """
        return [info, {'activity': activity_data,
                       'battery': battery_data,
                       'lux': lux_data,
                       'event': event_data,
                       'parameters': parameters_data,
                       'metadata': metadata_data
                       }]
        """
        [info, data] = self.load_file()
        self.assertTrue(len(info) > 0)
        self.assertTrue(len(data) == 6)

        print(info)

        # Creating recordset
        # print(info['Start Date'], info['Last Sample Time'])
        start = int(info['Start Date'])
        stop = int(info['Last Sample Time'])
        print(start, stop)
        start_timestamp = ticksconverter(start)
        end_timestamp = ticksconverter(stop)
        print(start_timestamp, end_timestamp)

        recordset = self.add_recordset_to_db(info['Subject Name'], start_timestamp, end_timestamp)
        print(recordset)

        if data.__contains__('activity'):
            print('activity found')
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

            # Import data
            for epoch in data['activity']:
                # An epoch will contain a timestamp and array with each acc_x, acc_y, acc_z
                self.assertEqual(len(epoch), 2)

                # print(epoch, len(epoch))

                # Get data
                timestamp = datetime.datetime.fromtimestamp(epoch[0])
                samples = epoch[1]

                # Separate write for each channel
                for index in range(0, len(accelerometer_channels)):
                    # print(samples[:, index])
                    if len(samples[:, index]) > 0:
                        self.add_sensor_data_to_db(recordset, accelerometer_sensor, accelerometer_channels[index],
                                                   timestamp, samples[:, index])

            # Flush DB
            self.flush()

        if data.__contains__('battery'):
            print('battery found')
            # Create sensor
            volt_sensor = self.add_sensor_to_db(SensorType.BATTERY, 'Battery', info['Device Type'], 'Unknown',
                                                1/60, 1)

            # Create channel
            volt_channel = self.add_channel_to_db(volt_sensor, Units.VOLTS, DataFormat.FLOAT32, 'Battery')

            for epoch in data['battery']:
                timestamp = datetime.datetime.fromtimestamp(epoch[0])
                value = np.float32(epoch[1])
                self.assertEqual(len(value.tobytes()), 4)
                self.add_sensor_data_to_db(recordset, volt_sensor, volt_channel, timestamp, value)

            # Flush to DB (ram)
            self.db.flush()

        if data.__contains__('lux'):
            print('lux found')
            # Create sensor
            lux_sensor = self.add_sensor_to_db(SensorType.LUX, 'Lux', info['Device Type'], 'Unknown', 1, 1)

            # Create channel
            lux_channel = self.add_channel_to_db(lux_sensor, Units.LUX, DataFormat.FLOAT32, 'Lux')

            for epoch in data['lux']:
                timestamp = datetime.datetime.fromtimestamp(epoch[0])
                value = np.float32(epoch[1])
                self.assertEqual(len(value.tobytes()), 4)
                self.add_sensor_data_to_db(recordset, lux_sensor, lux_channel, timestamp, value)

            # Flush to DB (ram)
            self.flush()

        # Write data to file
        self.commit()

    @timing
    def read_back_data(self, participant):
        recordsets = self.db.get_all_recordsets(participant)
        print(recordsets)

        for record in recordsets:
            alldata = self.db.get_all_sensor_data(record)
            print('recordset size', len(alldata))
            for data in alldata:
                print('type', type(data.data))
                break

    def test_reload_from_db(self):
        # Import data first
        self.test_import()

        self.read_back_data(self.participant)


class ActigraphDBTest2(unittest.TestCase):

    @timing
    def setUp(self):
        np.set_printoptions(suppress=True)
        print(__file__ + ' Creating database')

        # Will read already existing file
        self.db = DBManager('actigraph.db', False, False)

    @timing
    def tearDown(self):
        self.db.commit()

    def test_read_all_participant(self):
        participants = self.db.get_all_participants()
        print(participants)
        for participant in participants:
            print(participant, participant.group)

    def test_read_all_data(self):
        recordsets = self.db.get_all_recordsets()
        
        for record in recordsets:
            all_data = self.db.get_all_sensor_data(record, convert=False)
            accelerometer_x = []
            for data in all_data:
                print(data.to_time_series())
                break
