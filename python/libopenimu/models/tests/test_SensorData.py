"""

    Unit testing for SensorData
    @authors Simon Brière, Dominic Létourneau
    @date 03/04/2018

"""


import unittest
from libopenimu.models.SensorData import SensorData
from libopenimu.models.SensorTimestamps import SensorTimestamps
from libopenimu.models.Channel import Channel
from libopenimu.models.Sensor import Sensor
from libopenimu.models.Recordset import Recordset
import numpy as np
import datetime


class SensorDataTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty_ctor(self):
        data = SensorData()
        self.assertEqual(data.id_sensor_data, None)

    def test_properties(self):
        sensordata = SensorData()
        sensordata.id_sensor_data = 1
        recordset = Recordset()
        sensordata.recordset = recordset
        sensor = Sensor()
        sensordata.sensor = sensor
        channel = Channel()
        sensordata.channel = channel
        sensordata.data_timestamp = 10
        sensordata.data = [1, 2, 3, 4, 5]

        self.assertEqual(sensordata.id_sensor_data, 1)
        self.assertEqual(sensordata.recordset, recordset)
        self.assertEqual(sensordata.sensor, sensor)
        self.assertEqual(sensordata.channel, channel)
        self.assertEqual(sensordata.data_timestamp, 10)
        self.assertEqual(sensordata.data, [1, 2, 3, 4, 5])

    def test_to_time_series(self):
        sensordata = SensorData()
        sensordata.id_sensor_data = 1
        recordset = Recordset()
        sensordata.recordset = recordset
        sensor = Sensor()
        sensor.sampling_rate = 5
        sensor.data_rate = 1
        sensordata.sensor = sensor
        channel = Channel()
        sensordata.channel = channel

        sensordata.data = np.array([1, 2, 3, 4, 5], dtype=float)

        sensordata.timestamps = SensorTimestamps()
        sensordata.timestamps.timestamps = np.array([0, 1, 2, 3, 4], dtype=np.float64)
        sensordata.timestamps.update_timestamps()

        print(sensordata.to_time_series())
        print(sensordata)
