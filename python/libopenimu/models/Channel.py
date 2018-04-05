"""
 Channel
 @authors Simon Brière, Dominic Létourneau
 @date 05/04/2018
"""

from libopenimu.models.Sensor import Sensor
from libopenimu.models.data_formats import DataFormat
from libopenimu.models.units import Units


class Channel:
    def __init__(self, *args, **kwargs):
        # Initialize from kwargs (and default values)
        self._id_channel = kwargs.get('id_channel', None)
        self._sensor = kwargs.get('sensor', Sensor())
        self._id_unit = kwargs.get('id_unit', None)
        self._id_data_format = kwargs.get('id_data_format', None)
        self._label = kwargs.get('label', None)

        for arg in args:
            if isinstance(arg, tuple):
                self.from_tuple(arg)
            elif isinstance(arg, Channel):
                self.from_tuple(arg.as_tuple())

    def __str__(self):
        return 'Channel' + str(self.as_tuple())

    def __eq__(self, other):
        return self.as_tuple() == other.as_tuple()

    def get_id_channel(self):
        return self._id_channel

    def set_id_channel(self, id_channel):
        self._id_channel = id_channel

    def get_sensor(self):
        return self._sensor

    def set_sensor(self, sensor):
        self._sensor = sensor

    def get_id_unit(self):
        return self._id_unit

    def set_id_unit(self, id_unit):
        assert(Units.is_valid(id_unit))
        self._id_unit = id_unit

    def get_id_data_format(self):
        return self._id_data_format

    def set_id_data_format(self, id_data_format):
        assert(DataFormat.is_valid(id_data_format))
        self._id_data_format = id_data_format

    def get_label(self):
        return self._label

    def set_label(self, label):
        self._label = label

    def as_tuple(self):
        return self._id_channel, self._sensor.as_tuple(), self._id_unit, self._id_data_format, self._label

    def from_tuple(self, t):
        (self._id_channel, sensor_tuple, self._id_unit, self._id_data_format, self._label) = t
        self._sensor.from_tuple(sensor_tuple)

    # Properties
    id_channel = property(get_id_channel, set_id_channel)
    sensor = property(get_sensor, set_sensor)
    id_unit = property(get_id_unit, set_id_unit)
    id_data_format = property(get_id_data_format, set_id_data_format)
    label = property(get_label, set_label)
