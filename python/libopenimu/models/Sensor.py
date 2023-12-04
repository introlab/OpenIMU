"""
 Sensor
 @authors Simon Brière, Dominic Létourneau
 @date 02/04/2018
"""

from libopenimu.models.Base import Base

# Important for relationships
from libopenimu.models.Channel import Channel

from sqlalchemy import Column, Integer, Float, String, Sequence
from sqlalchemy.orm import relationship


class Sensor(Base):
    __tablename__ = 'tabSensors'
    id_sensor = Column(Integer, Sequence('id_sensor_sequence'), primary_key=True, autoincrement=True)
    # id_sensor_type = Column(Integer, ForeignKey('tabSensorTypes.id_sensor_type'), nullable=False)
    id_sensor_type = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    hw_name = Column(String, nullable=False)
    hw_id = Column(String, nullable=True)
    location = Column(String, nullable=False)
    sampling_rate = Column(Float, nullable=False)
    data_rate = Column(Integer, nullable=False)
    settings = Column(String, nullable=True)

    # Which sensor type
    # sensor_type = relationship("SensorType")
    channels = relationship("Channel", cascade="all,delete-orphan", back_populates="sensor")

    # def __eq__(self, other):
    #    return self.id_sensor == other.id_sensor and self.id_sensor_type == other.id_sensor_type and \
    #        self.name == other.name and self.hw_name == other.hw_name and self.location == other.location and \
    #        self.sampling_rate == other.sampling_rate and self.data_rate == other.data_rate

    # Database rep (optional)
    def __repr__(self):
        return ("<Sensor(id_sensor_type='%i', name='%s', hw_name='%s', hw_id='%s', location='%s', sampling_rate='%f'" 
                ", data_rate='%i, settings='%s')>" %
                (self.id_sensor_type, self.name, self.hw_name, self.hw_id, self.location, self.sampling_rate,
                 self.data_rate, self.settings))


