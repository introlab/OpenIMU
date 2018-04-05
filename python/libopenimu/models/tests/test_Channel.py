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

    def test_as_from_tuple(self):
        t = (1, Sensor().as_tuple(), 1, 1, 'label')
        channel = Channel(t)
        self.assertTrue(channel.as_tuple(), t)

    def test_properties(self):
        channel = Channel()
        channel.id_channel = 1
        channel.sensor = Sensor()
        channel.id_data_format = 0
        channel.id_unit = 0
        channel.label = 'My label'

        self.assertEqual(channel.id_channel, 1)
        self.assertEqual(channel.sensor, Sensor())
        self.assertEqual(channel.id_data_format, 0)
        self.assertEqual(channel.id_unit, 0)
        self.assertEqual(channel.label, 'My label')
