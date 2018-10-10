"""
 Channel
 @authors Simon Brière, Dominic Létourneau
 @date 05/04/2018
"""

from libopenimu.models.Base import Base
# from libopenimu.models.Sensor import Sensor
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship


class Channel(Base):
    __tablename__ = 'tabChannels'
    id_channel = Column(Integer, Sequence('id_channel_sequence'), primary_key=True, autoincrement=True)
    id_sensor = Column(Integer, ForeignKey('tabSensors.id_sensor'), nullable=False)
    id_sensor_unit = Column(Integer, nullable=False)
    id_data_format = Column(Integer, nullable=False)
    label = Column(String, nullable=False)

    # Relationships
    sensor = relationship("Sensor", cascade="all,delete")

    # Database rep (optional)
    def __repr__(self):
        return "<Channel(id_sensor='%s', id_sensor_unit='%s', id_data_format='%s', label='%s'" % \
               (str(self.id_sensor), str(self.id_sensor_unit), str(self.id_data_format), str(self.label))

