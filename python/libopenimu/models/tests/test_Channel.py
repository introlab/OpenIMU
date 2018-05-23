"""

    Unit testing for Channel
    @authors Simon Brière, Dominic Létourneau
    @date 03/04/2018

"""


import unittest
from libopenimu.models.Channel import Channel
from libopenimu.models.Sensor import Sensor


class ChannelTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_properties(self):
        channel = Channel()
        channel.id_channel = 1
        sensor = Sensor()
        channel.sensor = sensor

        # print(channel.sensor)

        channel.id_data_format = 0
        channel.id_sensor_unit = 0
        channel.label = 'My label'

        self.assertEqual(channel.id_channel, 1)
        self.assertEqual(channel.sensor, sensor)
        self.assertEqual(channel.id_data_format, 0)
        self.assertEqual(channel.id_sensor_unit, 0)
        self.assertEqual(channel.label, 'My label')

    def test_empty(self):
        channel = Channel()
        self.assertEqual(print(channel), None)
        self.assertEqual(channel.id_channel, None)
        self.assertEqual(channel.sensor, None)
        self.assertEqual(channel.id_data_format, None)
        self.assertEqual(channel.id_sensor_unit, None)
        self.assertEqual(channel.label, None)

