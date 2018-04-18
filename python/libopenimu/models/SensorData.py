"""
 SensorData
 @authors Simon Brière, Dominic Létourneau
 @date 05/04/2018
"""

from libopenimu.models.Base import Base

# Imports important for relationships, even if not visible from this file
from libopenimu.models.Recordset import Recordset
from libopenimu.models.Sensor import Sensor
from libopenimu.models.Channel import Channel

from libopenimu.models.data_formats import DataFormat

from sqlalchemy import Column, Integer, Sequence, ForeignKey, TIMESTAMP, Interval, BLOB
from sqlalchemy.orm import relationship

import numpy as np


class SensorData(Base):
    __tablename__ = 'tabSensorsData'
    id_sensor_data = Column(Integer, Sequence('id_sensor_data_sequence'), primary_key=True, autoincrement=True)
    id_recordset = Column(Integer, ForeignKey('tabRecordsets.id_recordset'), nullable=False)
    id_sensor = Column(Integer, ForeignKey('tabSensors.id_sensor'), nullable=False)
    id_channel = Column(Integer, ForeignKey('tabChannels.id_channel'), nullable=False)

    '''
    A type for datetime.timedelta() objects.
    The Interval type deals with datetime.timedelta objects. In PostgreSQL, the native INTERVAL type is used; 
    for others, the value is stored as a date which is relative to the “epoch” (Jan. 1, 1970).
    '''
    data_timestamp = Column(TIMESTAMP, nullable=False)
    data = Column(BLOB, nullable=False)

    # Relationships
    recordset = relationship("Recordset")
    sensor = relationship("Sensor")
    channel = relationship("Channel")

    def to_ndarray(self):
        if type(self.data) is bytes:
            return DataFormat.from_bytes(self.data, self.channel.id_data_format)
        else:
            return self.data

    def to_time_series(self):
        values = self.to_ndarray()

        time = np.linspace(self.data_timestamp.timestamp(),
                           num=len(values),
                           stop=self.data_timestamp.timestamp() + len(values) / self.sensor.sampling_rate,
                           dtype=np.float64, endpoint=False)

        return {'time': time, 'values': values}

    # Database rep (optional)
    def __repr__(self):
        return "<SensorData(id_recordset='%s', id_sensor='%s', id_channel='%s', data_timestamp='%s', data_size='%s'" % \
               (str(self.id_recordset), str(self.id_sensor), str(self.id_channel), str(self.data_timestamp),
                str(len(self.data)))


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
        # Compare data (can be a bool or an array of bools)
        data_compare = self.data == other.data
        if hasattr(data_compare, "__len__"):
            data_compare = data_compare.all()

        return (self.id_sensor_data == other.id_sensor_data and self.recordset == other.recordset
                and self.sensor == other.sensor and self.channel == other.channel
                and self.data_timestamp == other.data_timestamp and data_compare)

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

"""