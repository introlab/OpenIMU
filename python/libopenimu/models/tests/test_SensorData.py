"""

    Unit testing for SensorData
    @authors Simon Brière, Dominic Létourneau
    @date 03/04/2018

"""


import unittest
from libopenimu.models.SensorData import SensorData
from libopenimu.models.Channel import Channel
from libopenimu.models.Sensor import Sensor
from libopenimu.models.Recordset import Recordset
from libopenimu.models.Participant import Participant

class SensorDataTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty_ctor(self):
        data = SensorData()
        self.assertEqual(data.id_sensor_data, None)

    def test_from_to_tuple(self):
        participant = Participant(name="Participant Name", description="Participant Description")
        sensor = Sensor(id_sensor_type=1, name="Sensor Name", hw_name="Hardware", location="Wrist", sampling_rate=30.0,
                        data_rate=1)
        channel = Channel(sensor=sensor, id_unit=1, id_data_format=1, label='Sensor Label')
        recordset = Recordset(participant=participant, name="My Record", start_timestamp=0, end_timestamp=0)
        sensordata = SensorData(recordset=recordset, sensor=sensor, channel=channel, data_timestamp=0, data=None)

        my_tuple = sensordata.as_tuple()
        sensordata2 = SensorData(my_tuple)
        self.assertEqual(sensordata, sensordata2)

    def test_properties(self):
        sensordata = SensorData()
        sensordata.id_sensor_data = 1
        sensordata.recordset = Recordset()
        sensordata.sensor = Sensor()
        sensordata.channel = Channel()
        sensordata.data_timestamp = 10
        sensordata.data = [1, 2, 3, 4, 5]

        self.assertEqual(sensordata.id_sensor_data, 1)
        self.assertEqual(sensordata.recordset, Recordset())
        self.assertEqual(sensordata.sensor, Sensor())
        self.assertEqual(sensordata.channel, Channel())
        self.assertEqual(sensordata.data_timestamp, 10)
        self.assertEqual(sensordata.data,[1, 2, 3, 4, 5])
