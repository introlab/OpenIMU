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

from sqlalchemy import Column, Integer, Sequence, ForeignKey, BLOB
from sqlalchemy.orm import relationship


class SensorData(Base):
    __tablename__ = 'tabSensorsData'
    id_sensor_data = Column(Integer, Sequence('id_sensor_data_sequence'), primary_key=True, autoincrement=True)
    id_recordset = Column(Integer, ForeignKey('tabRecordsets.id_recordset', ondelete="CASCADE"), nullable=False)
    id_sensor = Column(Integer, ForeignKey('tabSensors.id_sensor', ondelete="CASCADE"), nullable=False)
    id_channel = Column(Integer, ForeignKey('tabChannels.id_channel', ondelete="CASCADE"), nullable=False)
    # TODO, timestamps CASCADE?
    id_timestamps = Column(Integer, ForeignKey('tabSensorsTimestamps.id_sensor_timestamps', ondelete="CASCADE"),
                           nullable=False)

    # Store the data
    data = Column(BLOB, nullable=False)

    # Relationships
    recordset = relationship("Recordset", cascade="all,delete")
    sensor = relationship("Sensor", cascade="all,delete")
    channel = relationship("Channel", cascade="all,delete")
    # TODO look for orphan timestamps
    timestamps = relationship("SensorTimestamps", order_by="SensorTimestamps.start_timestamp")

    def to_ndarray(self):
        if isinstance(self.data, bytes):
            return DataFormat.from_bytes(self.data, self.channel.id_data_format)
        else:
            return self.data

    def to_time_series(self):
        # Values
        values = self.to_ndarray()
        # Time
        time = self.timestamps.to_ndarray()

        # Very important...
        # TODO this is causing problems for data structures len(struct) != len(time)
        # assert(len(values) == len(time))

        return {'time': time, 'values': values}

    # Database rep (optional)
    def __repr__(self):
        return "<SensorData(id_recordset='%s', id_sensor='%s', id_channel='%s', start_timestamp='%s', end_timestamp='%s', data_size='%s'" % \
               (str(self.id_recordset), str(self.id_sensor), str(self.id_channel), str(self.timestamps.start_timestamp), str(self.timestamps.end_timestamp),
                str(len(self.data)))


