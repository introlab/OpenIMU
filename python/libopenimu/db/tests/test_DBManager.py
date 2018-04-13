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
import numpy as np


class DBManagerTest(unittest.TestCase):

    # All tests will use this name for the database
    TESTDB_NAME = 'openimu.db'

    def setUp(self):
        pass

    def tearDown(self):
        # Cleanup database
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
        for i in range(0, 10):
            self.assertEqual(participants[i], all_participants[i])

    def test_add_recordset(self):
        manager = DBManager(filename='openimu.db', overwrite=True)

        # Participant information
        group = manager.add_group('My Group', 'My Group Description')
        name = 'Participant Name'
        description = 'Participant Description'
        participant = manager.add_participant(group, name, description)
        recordset = manager.add_recordset(participant, 'Record Name', 10, 20)
        recordset2 = manager.get_recordset(recordset.id_recordset)

        self.assertGreater(recordset.id_recordset, 0)
        self.assertEqual(recordset.participant, participant)
        self.assertEqual(recordset.name, 'Record Name')
        self.assertEqual(recordset.start_timestamp, 10)
        self.assertEqual(recordset.end_timestamp, 20)
        self.assertEqual(recordset, recordset2)

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
        recordset = manager.add_recordset(participant, 'My Record', 0, 0)

        data = np.zeros(40)
        sensordata = manager.add_sensor_data(recordset, sensor, channel, 0, data)

        sensordata2 = manager.get_sensor_data(sensordata.id_sensor_data)
        self.assertEqual(sensordata, sensordata2)