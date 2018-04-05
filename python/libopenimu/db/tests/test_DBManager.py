"""

    Unit testing for DBManager
    @authors Simon Brière, Dominic Létourneau
    @date 03/04/2018

"""


import unittest
import os
from libopenimu.db.DBManager import DBManager
from libopenimu.models.sensor_types import SensorType


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