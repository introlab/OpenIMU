"""
 Sensor
 @authors Simon Brière, Dominic Létourneau
 @date 02/04/2018
"""

import unittest
from libopenimu.models.sensor_types import *


class Sensor:
    def __init__(self, **kwargs):
        self._id_sensor = kwargs.get('id_sensor', None)
        self._name = kwargs.get('name', None)
        self._hw_name = kwargs.get('hw_name', None)
        self._location = kwargs.get('location', None)
        self._sampling_rate = kwargs.get('sampling_rate', None)
        self._data_rate = kwargs.get('data_rate', None)

        # Validation
        if self._id_sensor is not None:
            SensorType.sensor_type_validation(self._id_sensor)

    def set_id_sensor(self, id_sensor):
        SensorType.sensor_type_validation(id_sensor)
        self._id_sensor = id_sensor

    def get_id_sensor(self):
        return self._id_sensor

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_hw_name(self, hw_name):
        self._hw_name = hw_name

    def get_hw_name(self):
        return self._hw_name

    def set_location(self, location):
        self._location = location

    def get_location(self):
        return self._location

    def set_sampling_rate(self, sampling_rate):
        self._sampling_rate = sampling_rate

    def get_sampling_rate(self):
        return self._sampling_rate

    def set_data_rate(self, data_rate):
        self._data_rate = data_rate

    def get_data_rate(self):
        return self._data_rate

    # Properties
    id_sensor = property(get_id_sensor, set_id_sensor)
    name = property(get_name, set_name)
    hw_name = property(get_hw_name, set_hw_name)
    location = property(get_location, set_location)
    sampling_rate = property(get_sampling_rate, set_sampling_rate)
    data_rate = property(get_data_rate, set_data_rate)

class SensorTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ctor_no_args(self):
        sensor = Sensor()
        self.assertEqual(sensor.id_sensor, None)
        self.assertEqual(sensor.name, None)
        self.assertEqual(sensor.hw_name, None)
        self.assertEqual(sensor.location, None)
        self.assertEqual(sensor.sampling_rate, None)
        self.assertEqual(sensor.data_rate, None)

    def test_properties(self):
        sensor = Sensor()
        my_id = SensorType.GPS
        my_name = 'My Name'
        my_hw_name = 'HW Name'
        my_location = 'My Location'
        my_sampling_rate = 1.0
        my_data_rate = 1

        sensor.id_sensor = my_id
        sensor.name = my_name
        sensor.hw_name = my_hw_name
        sensor.location = my_location
        sensor.sampling_rate = my_sampling_rate
        sensor.data_rate = my_data_rate

        self.assertEqual(sensor.id_sensor, my_id)
        self.assertEqual(my_id, sensor.get_id_sensor())

        self.assertEqual(sensor.name, my_name)
        self.assertEqual(my_name, sensor.get_name())

        self.assertEqual(sensor.hw_name, my_hw_name)
        self.assertEqual(my_hw_name, sensor.get_hw_name())

        self.assertEqual(sensor.location, my_location)
        self.assertEqual(my_location, sensor.get_location())

        self.assertEqual(sensor.sampling_rate, my_sampling_rate)
        self.assertEqual(my_sampling_rate, sensor.get_sampling_rate())

        self.assertEqual(sensor.data_rate, my_data_rate)
        self.assertEqual(my_data_rate, sensor.get_data_rate())