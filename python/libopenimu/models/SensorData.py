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
from libopenimu.models.SensorTimestamps import SensorTimestamps

from libopenimu.models.data_formats import DataFormat

from sqlalchemy import Column, Integer, Sequence, ForeignKey, TIMESTAMP, Interval, BLOB
from sqlalchemy.orm import relationship

import numpy as np


class SensorData(Base):
    __tablename__ = 'tabSensorsData'
    id_sensor_data = Column(Integer, Sequence('id_sensor_data_sequence'), primary_key=True, autoincrement=True)
    id_recordset = Column(Integer, ForeignKey('tabRecordsets.id_recordset', ondelete="CASCADE"), nullable=False)
    id_sensor = Column(Integer, ForeignKey('tabSensors.id_sensor', ondelete="CASCADE"), nullable=False)
    id_channel = Column(Integer, ForeignKey('tabChannels.id_channel', ondelete="CASCADE"), nullable=False)

    # TODO, timestamps are optional for now...
    id_timestamps = Column(Integer, ForeignKey('tabSensorsTimestamps.id_sensor_timestamps', ondelete="CASCADE"),
                           nullable=True)

    '''
    A type for datetime.timedelta() objects.
    The Interval type deals with datetime.timedelta objects. In PostgreSQL, the native INTERVAL type is used; 
    for others, the value is stored as a date which is relative to the “epoch” (Jan. 1, 1970).
    '''
    start_timestamp = Column(TIMESTAMP, nullable=False)
    end_timestamp = Column(TIMESTAMP, nullable=False)
    data = Column(BLOB, nullable=False)

    # Relationships
    recordset = relationship("Recordset", cascade="all,delete")
    sensor = relationship("Sensor", cascade="all,delete")
    channel = relationship("Channel", cascade="all,delete")
    timestamps = relationship("SensorTimestamps", cascade="all,delete")

    def to_ndarray(self):
        if type(self.data) is bytes:
            return DataFormat.from_bytes(self.data, self.channel.id_data_format)
        else:
            return self.data

    def to_time_series(self):
        if self.sensor.sampling_rate > 0:
            values = self.to_ndarray()

            time = np.linspace(self.start_timestamp.timestamp(),
                               num=len(values),
                               stop=self.start_timestamp.timestamp() + len(values) / self.sensor.sampling_rate,
                               dtype=np.float64, endpoint=False)

            # np.set_printoptions(suppress=True)
            # if len(time) > 0:
            # print('time', self.data_timestamp)

            return {'time': time, 'values': values}
        else:
            values = self.to_ndarray()
            assert(len(values) == 1)
            return {'time': [self.start_timestamp.timestamp()], 'values': values}

    # Database rep (optional)
    def __repr__(self):
        return "<SensorData(id_recordset='%s', id_sensor='%s', id_channel='%s', start_timestamp='%s', end_timestamp='%s', data_size='%s'" % \
               (str(self.id_recordset), str(self.id_sensor), str(self.id_channel), str(self.start_timestamp), str(self.end_timestamp),
                str(len(self.data)))


