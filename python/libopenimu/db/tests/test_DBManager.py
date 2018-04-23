"""

    Unit testing for DBManager
    @authors Simon Brière, Dominic Létourneau
    @date 03/04/2018

"""


import unittest
import os
from libopenimu.db.DBManager import DBManager
from libopenimu.models.sensor_types import SensorType
from libopenimu.models.units import Units
from libopenimu.models.data_formats import DataFormat
from libopenimu.models.Sensor import Sensor
from libopenimu.models.Channel import Channel

import numpy as np
import datetime


class DBManagerTest(unittest.TestCase):

    # All tests will use this name for the database
    TESTDB_NAME = 'openimu.db'

    def setUp(self):
        pass

    def tearDown(self):
        # Cleanup database
        if False:
            if os.path.isfile(DBManagerTest.TESTDB_NAME):
                print('Removing database : ', DBManagerTest.TESTDB_NAME)
                os.remove(DBManagerTest.TESTDB_NAME)

    def test_add_group(self):
        manager = DBManager(filename=DBManagerTest.TESTDB_NAME, overwrite=True)

        # Group information
        name = 'Group Name'
        description = 'Group Description'
        group = manager.add_group(name=name, description=description)
        group2 = manager.get_group(group.id_group)
        self.assertEqual(group.id_group, group2.id_group)
        self.assertEqual(group.name, group2.name)

    def test_add_sensor(self):
        manager = DBManager(filename='openimu.db', overwrite=True)

        # Sensor information
        id_sensor_type = SensorType.ACCELEROMETER
        name = 'Accelerometer'
        hw_name = 'OpenIMU-HW'
        location = 'wrist'
        sampling_rate = 30.0
        data_rate = 1

        sensor = manager.add_sensor(id_sensor_type, name, hw_name, location, sampling_rate, data_rate)
        sensor2 = manager.get_sensor(sensor.id_sensor)

        self.assertEqual(sensor.id_sensor, sensor2.id_sensor)
        self.assertEqual(sensor.id_sensor_type, sensor2.id_sensor_type)
        self.assertEqual(sensor.name, sensor2.name)
        self.assertEqual(sensor.hw_name, sensor2.hw_name)
        self.assertEqual(sensor.location, sensor2.location)
        self.assertEqual(sensor.sampling_rate, sensor2.sampling_rate)
        self.assertEqual(sensor.data_rate, sensor2.data_rate)

    def test_get_all_sensors(self):

        manager = DBManager(filename='openimu.db', overwrite=True)

        # Sensor information
        id_sensor_type = SensorType.ACCELEROMETER
        name = 'Accelerometer'
        hw_name = 'OpenIMU-HW'
        location = 'wrist'
        sampling_rate = 30.0
        data_rate = 1
        count = 10

        sensors = []

        for i in range(0, count):
            sensors.append(manager.add_sensor(id_sensor_type, name, hw_name, location, sampling_rate, data_rate))

        all_sensors = manager.get_all_sensors()
        self.assertEqual(len(all_sensors), len(sensors))

        # Wrong type
        self.assertEqual(0, len(manager.get_all_sensors(SensorType.BATTERY)))

        # Compare content
        for i in range(0, count):
            self.assertEqual(sensors[i], all_sensors[i])

    def test_add_participant(self):
        manager = DBManager(filename='openimu.db', overwrite=True)

        # Participant information
        group = manager.add_group('My Group', 'My Group Description')
        name = 'Participant Name'
        description = 'Participant Description'
        participant = manager.add_participant(group, name, description)
        participant2 = manager.get_participant(participant.id_participant)

        self.assertEqual(participant.group, group)
        self.assertEqual(participant.name, name)
        self.assertEqual(participant.description, description)
        self.assertGreater(participant.id_participant, 0)
        self.assertEqual(participant, participant2)

    def test_get_all_participants(self):
        manager = DBManager(filename='openimu.db', overwrite=True)
        # This will add participants

        # Participant information
        group = manager.add_group('My Group', 'My Group Description')
        name = 'Participant Name'
        description = 'Participant Description'

        participants = []

        # Multiple participants, all the same info...
        for i in range(0, 10):
            participants.append(manager.add_participant(group, name, description))

        # Read back list of participants
        all_participants = manager.get_all_participants()

        # Compare size
        self.assertEqual(len(participants), len(all_participants))

        # Compare content
        for i in range(0, len(participants)):
            self.assertEqual(participants[i], all_participants[i])

    def test_add_recordset(self):
        manager = DBManager(filename='openimu.db', overwrite=True, echo=False)

        # Participant information
        group = manager.add_group('My Group', 'My Group Description')
        name = 'Participant Name'
        description = 'Participant Description'
        participant = manager.add_participant(group, name, description)
        # This gives datetime from seconds from epoch
        time1 = datetime.datetime.fromtimestamp(0)
        time2 = datetime.datetime.fromtimestamp(1)
        recordset = manager.add_recordset(participant, 'Record Name', time1, time2)
        recordset2 = manager.get_recordset(recordset.id_recordset)

        self.assertGreater(recordset.id_recordset, 0)
        self.assertEqual(recordset.participant, participant)
        self.assertEqual(recordset.name, 'Record Name')
        self.assertEqual(recordset.start_timestamp, time1)
        self.assertEqual(recordset.end_timestamp, time2)
        self.assertEqual(recordset, recordset2)

    def test_get_all_recordsets(self):
        manager = DBManager(filename='openimu.db', overwrite=True)

        # Participant information
        group = manager.add_group('My Group', 'My Group Description')
        name = 'Participant Name'
        description = 'Participant Description'
        participant1 = manager.add_participant(group, name, description)
        participant2 = manager.add_participant(group, name, description)
        participant3 = manager.add_participant(group, name, description)

        count = 10
        recordsets1 = []
        recordsets2 = []

        # Adding recordsets
        for i in range(0, count):
            time1 = datetime.datetime.now()
            time2 = datetime.datetime.now()

            recordsets1.append(manager.add_recordset(participant1, 'Record Name', time1,
                                                     time2))
            recordsets2.append(manager.add_recordset(participant2, 'Record Name', time1,
                                                     time2))

        # Compare size
        all_from_participant_1 = manager.get_all_recordsets(participant1)
        all_from_participant_2 = manager.get_all_recordsets(participant2)
        self.assertEqual(len(all_from_participant_1), len(recordsets1))
        self.assertEqual(len(all_from_participant_2), len(recordsets2))
        self.assertEqual(len(manager.get_all_recordsets()), len(recordsets1) + len(recordsets2))
        self.assertEqual(0, len(manager.get_all_recordsets(participant3)))

        # Compare contents
        for i in range(0, count):
            self.assertEqual(recordsets1[i], all_from_participant_1[i])
            self.assertEqual(recordsets2[i], all_from_participant_2[i])

    def test_add_channel(self):
        manager = DBManager(filename='openimu.db', overwrite=True)

        # Create sensor in DB
        sensor = manager.add_sensor(SensorType.ACCELEROMETER, 'Sensor Name', 'Hardware Name', 'Wrist', 30.0, 1)
        channel = manager.add_channel(sensor, Units.GRAVITY_G, DataFormat.FLOAT32, 'Accelerometer_X')
        channel2 = manager.get_channel(channel.id_channel)
        self.assertEqual(channel, channel2)

    def test_add_sensor_data(self):
        manager = DBManager(filename='openimu.db', overwrite=True)

        # Create sensor in DB
        group = manager.add_group('Group Name', 'Group Description')
        participant = manager.add_participant(group, 'Participant Name', 'Participant Description')
        sensor = manager.add_sensor(SensorType.ACCELEROMETER, 'Sensor Name', 'Hardware Name', 'Wrist', 30.0, 1)
        channel = manager.add_channel(sensor, Units.GRAVITY_G, DataFormat.FLOAT32, 'Accelerometer_X')
        time1 = datetime.datetime.now()
        time2 = datetime.datetime.now()
        recordset = manager.add_recordset(participant, 'My Record', time1, time2)

        data = np.zeros(40, dtype=np.float32)
        sensordata = manager.add_sensor_data(recordset, sensor, channel, time1, data)
        manager.commit()

        sensordata2 = manager.get_sensor_data(sensordata.id_sensor_data)
        self.assertEqual(sensordata, sensordata2)

    def test_get_all_sensor_data_with_args(self):
        manager = DBManager(filename='openimu.db', overwrite=True, echo=False)

        # Create sensor in DB
        group = manager.add_group('Group Name', 'Group Description')
        participant = manager.add_participant(group, 'Participant Name', 'Participant Description')
        sensor = manager.add_sensor(SensorType.ACCELEROMETER, 'Sensor Name', 'Hardware Name', 'Wrist', 30.0, 1)
        sensor2 = manager.add_sensor(SensorType.GYROMETER, 'Sensor Name', 'Hardware Name', 'Wrist', 30.0, 1)
        channel1 = manager.add_channel(sensor, Units.GRAVITY_G, DataFormat.FLOAT32, 'Accelerometer_X')
        channel2 = manager.add_channel(sensor, Units.GRAVITY_G, DataFormat.FLOAT32, 'Accelerometer_Y')
        time1 = datetime.datetime.now()
        time2 = datetime.datetime.now()
        recordset = manager.add_recordset(participant, 'My Record', time1, time2)

        data = np.zeros(40, dtype=np.float32)
        sensordata = manager.add_sensor_data(recordset, sensor, channel1, time1, data)
        sensordata = manager.add_sensor_data(recordset, sensor, channel2, time1, data)
        manager.commit()

        # Test with no args, return everything in the recordset
        sensordata_res = manager.get_all_sensor_data(recordset=recordset)
        self.assertEqual(len(sensordata_res), 2)

        # Test with a valid sensor arg
        sensordata_res = manager.get_all_sensor_data(recordset=recordset, sensor=sensor)
        self.assertEqual(len(sensordata_res), 2)

        # Test with not the right sensor arg
        sensordata_res = manager.get_all_sensor_data(recordset=recordset, sensor=sensor2)
        self.assertEqual(len(sensordata_res), 0)

        # Testing with invalid sensor arg
        sensordata_res = manager.get_all_sensor_data(recordset=recordset, sensor=Sensor())
        self.assertEqual(len(sensordata_res), 0)

        # Testing with channel1
        sensordata_res = manager.get_all_sensor_data(recordset=recordset, channel=channel1)
        self.assertEqual(len(sensordata_res), 1)

        # Testing with channel2
        sensordata_res = manager.get_all_sensor_data(recordset=recordset, channel=channel2)
        self.assertEqual(len(sensordata_res), 1)

        # Testing with invalid channel
        sensordata_res = manager.get_all_sensor_data(recordset=recordset, channel=Channel())
        self.assertEqual(len(sensordata_res), 0)