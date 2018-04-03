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

    @staticmethod
    def database_name():
        return 'openimu.db'

    def setUp(self):
        pass

    def tearDown(self):

        if os.path.isfile(DBManagerTest.database_name()):
            print('Removing database : ', DBManagerTest.database_name())
            os.remove(DBManagerTest.database_name())

    def test_add_group(self):
        manager = DBManager(filename=DBManagerTest.database_name(), overwrite=True)

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

