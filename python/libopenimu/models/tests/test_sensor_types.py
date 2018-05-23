"""

    Unit testing for sensor_types
    @authors Simon Brière, Dominic Létourneau
    @date 03/04/2018

"""


import unittest
from libopenimu.models.sensor_types import SensorType


class SensorTypeTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_as_dict(self):
        my_dict = SensorType.as_dict()
        self.assertEqual(len(my_dict), 11)

    def test_validation(self):
        self.assertTrue(SensorType.is_valid_type(SensorType.ACCELEROMETER), "Accelerometer type invalid")
        self.assertTrue(SensorType.is_valid_type(SensorType.GYROMETER), "Gyrometer type invalid")
        self.assertTrue(SensorType.is_valid_type(SensorType.MAGNETOMETER), "Magnetometer type invalid")
        self.assertTrue(SensorType.is_valid_type(SensorType.LUX), "Lux type invalid")
        self.assertTrue(SensorType.is_valid_type(SensorType.GPS), "GPS type invalid")
        self.assertTrue(SensorType.is_valid_type(SensorType.HEARTRATE), "Heartrate type invalid")
        self.assertTrue(SensorType.is_valid_type(SensorType.ORIENTATION), "Orientation type invalid")
        self.assertTrue(SensorType.is_valid_type(SensorType.STEP), "Step type invalid")
        self.assertTrue(SensorType.is_valid_type(SensorType.BATTERY), "Battery type invalid")
        self.assertTrue(SensorType.is_valid_type(SensorType.CURRENT), "Current type invalid")
        self.assertTrue(SensorType.is_valid_type(SensorType.BAROMETER), "Barometer type invalid")