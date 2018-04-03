"""

    Unit testing for Sensor
    @authors Simon Brière, Dominic Létourneau
    @date 03/04/2018

"""


import unittest
from libopenimu.models.Sensor import Sensor
from libopenimu.models.sensor_types import SensorType


class SensorTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ctor_no_args(self):
        sensor = Sensor()
        self.assertEqual(sensor.id_sensor, None)
        self.assertEqual(sensor.id_sensor_type, None)
        self.assertEqual(sensor.name, None)
        self.assertEqual(sensor.hw_name, None)
        self.assertEqual(sensor.location, None)
        self.assertEqual(sensor.sampling_rate, None)
        self.assertEqual(sensor.data_rate, None)

    def test_ctor_all_args(self):
        _id_sensor = 0
        _id_sensor_type = 0
        _name = 'My Name'
        _hw_name = 'HW Name'
        _location = 'wrist'
        _sampling_rate = 30.0
        _data_rate = 1

        sensor = Sensor(id_sensor=_id_sensor, id_sensor_type=_id_sensor_type, name=_name, hw_name=_hw_name,
                        location=_location, sampling_rate=_sampling_rate, data_rate=_data_rate)

        self.assertEqual(_id_sensor, sensor.id_sensor)
        self.assertEqual(_id_sensor_type, sensor.id_sensor_type)
        self.assertEqual(_name, sensor.name)
        self.assertEqual(_hw_name, sensor.hw_name)
        self.assertEqual(_location, sensor.location)
        self.assertEqual(_sampling_rate, sensor.sampling_rate)
        self.assertEqual(_data_rate, sensor.data_rate)

    def test_properties(self):
        sensor = Sensor()
        my_id = 0
        my_id_type = SensorType.GPS
        my_name = 'My Name'
        my_hw_name = 'HW Name'
        my_location = 'My Location'
        my_sampling_rate = 1.0
        my_data_rate = 1

        sensor.id_sensor = my_id
        sensor.id_sensor_type = my_id_type
        sensor.name = my_name
        sensor.hw_name = my_hw_name
        sensor.location = my_location
        sensor.sampling_rate = my_sampling_rate
        sensor.data_rate = my_data_rate

        self.assertEqual(sensor.id_sensor, my_id)
        self.assertEqual(my_id, sensor.get_id_sensor())

        self.assertEqual(sensor.id_sensor_type, my_id_type)
        self.assertEqual(my_id_type, sensor.get_id_sensor_type())

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

    def test_as_from_tuple(self):
        my_id = 0
        my_id_type = SensorType.GPS
        my_name = 'My Name'
        my_hw_name = 'HW Name'
        my_location = 'My Location'
        my_sampling_rate = 1.0
        my_data_rate = 1
        my_tuple = (my_id, my_id_type, my_name, my_hw_name, my_location, my_sampling_rate, my_data_rate)
        sensor = Sensor(my_tuple)
        self.assertEqual(sensor.as_tuple(), my_tuple)
