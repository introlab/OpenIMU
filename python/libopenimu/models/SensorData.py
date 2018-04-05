"""
 SensorData
 @authors Simon Brière, Dominic Létourneau
 @date 05/04/2018
"""

from libopenimu.models.Recordset import Recordset
from libopenimu.models.Sensor import Sensor
from libopenimu.models.Channel import Channel


class SensorData:
    def __init__(self, *args, **kwargs):
        # Default values
        self._id_sensor_data = kwargs.get('id_sensor_data', None)
        self._recordset = kwargs.get('recordset', Recordset())
        self._sensor = kwargs.get('sensor', Sensor())
        self._channel = kwargs.get('channel', Channel())
        self._data_timestamp = kwargs.get('data_timestamp', 0)
        self._data = kwargs.get('data', None)

        for arg in args:
            if isinstance(arg, tuple):
                self.from_tuple(arg)
            elif isinstance(arg, SensorData):
                self.from_tuple(arg.as_tuple())

    def __str__(self):
        return "SensorData: " + str(self.as_tuple())

    def __eq__(self, other):
        # TODO Compare data
        return (self.id_sensor_data == other.id_sensor_data and self.recordset == other.recordset
                and self.sensor == other.sensor and self.channel == other.channel
                and self.data_timestamp == other.data_timestamp)

    def get_id_sensor_data(self):
        return self._id_sensor_data

    def set_id_sensor_data(self, id_sensor_data):
        self._id_sensor_data = id_sensor_data

    def get_recordset(self):
        return self._recordset

    def set_recordset(self, recordset):
        self._recordset = recordset

    def get_sensor(self):
        return self._sensor

    def set_sensor(self, sensor):
        self._sensor = sensor

    def get_channel(self):
        return self._channel

    def set_channel(self, channel):
        self._channel = channel

    def get_data_timestamp(self):
        return self._data_timestamp

    def set_data_timestamp(self, data_timestamp):
        self._data_timestamp = data_timestamp

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data

    def as_tuple(self):
        return self._id_sensor_data, self._recordset.as_tuple(), self._sensor.as_tuple(), self._channel.as_tuple(), \
               self._data_timestamp, self._data

    def from_tuple(self, t):
        (self._id_sensor_data, recordset_tuple, sensor_tuple, channel_tuple, self._data_timestamp, self._data) = t;
        # Read other tuples
        self._recordset.from_tuple(recordset_tuple)
        self._sensor.from_tuple(sensor_tuple)
        self._channel.from_tuple(channel_tuple)

    # Properties
    id_sensor_data = property(get_id_sensor_data, set_id_sensor_data)
    recordset = property(get_recordset, set_recordset)
    sensor = property(get_sensor, set_sensor)
    channel = property(get_channel, set_channel)
    data_timestamp = property(get_data_timestamp, set_data_timestamp)
    data = property(get_data, set_data)
