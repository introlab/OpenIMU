"""
 SensorData
 @authors Simon Brière, Dominic Létourneau
 @date 10/10/2018
"""

from libopenimu.models.Base import Base

# Imports important for relationships, even if not visible from this file
# from libopenimu.models.Sensor import Sensor
# from libopenimu.models.Channel import Channel

from sqlalchemy import Column, Integer, Sequence, TIMESTAMP,  BLOB
from sqlalchemy.orm import deferred

import numpy as np
import datetime


class SensorTimestamps(Base):
    __tablename__ = 'tabSensorsTimestamps'
    id_sensor_timestamps = Column(Integer, Sequence('id_sensor_timestamps_sequence'),
                                  primary_key=True, autoincrement=True)

    # Useful?
    start_timestamp = Column(TIMESTAMP, nullable=False)
    end_timestamp = Column(TIMESTAMP, nullable=False)

    # Timestamps will be stored in as floating point (double) deltas from starting timestamp
    timestamps = deferred(Column(BLOB, nullable=False))

    def update_timestamps(self):
        if len(self.timestamps) > 0:
            self.start_timestamp = datetime.datetime.fromtimestamp(self.timestamps[0])
            self.end_timestamp = datetime.datetime.fromtimestamp(self.timestamps[-1])

    def to_ndarray(self):
        return np.frombuffer(buffer=self.timestamps, dtype=np.float64)

    # Database rep (optional)
    def __repr__(self):
        return "<SensorTimestamps(id_sensor_timestamps='%s', data_size='%s'" % \
               (str(self.id_sensor_timestamps), str(len(self.timestamps)))
