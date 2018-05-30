"""
 Sensor
 @authors Simon Brière, Dominic Létourneau
 @date 02/04/2018
"""

from libopenimu.models.Base import Base
# from libopenimu.models.sensor_types import *
from sqlalchemy import Column, Integer, Float, String, Sequence, TIMESTAMP, BLOB, ForeignKey
from sqlalchemy.orm import relationship


class Sensor(Base):
    __tablename__ = 'tabSensors'
    id_sensor = Column(Integer, Sequence('id_sensor_sequence'), primary_key=True, autoincrement=True)
    # id_sensor_type = Column(Integer, ForeignKey('tabSensorTypes.id_sensor_type'), nullable=False)
    id_sensor_type = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    hw_name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    sampling_rate = Column(Float, nullable=False)
    data_rate = Column(Integer, nullable=False)

    # Which sensor type
    # TODO USEFUL?
    # sensor_type = relationship("SensorType")
    channels = relationship("Channel", cascade = "all,delete-orphan")

    # def __eq__(self, other):
    #    return self.id_sensor == other.id_sensor and self.id_sensor_type == other.id_sensor_type and \
    #        self.name == other.name and self.hw_name == other.hw_name and self.location == other.location and \
    #        self.sampling_rate == other.sampling_rate and self.data_rate == other.data_rate

    # Database rep (optional)
    def __repr__(self):
        return "<Sensor(id_sensor_type='%i', name='%s', hw_name='%s', location='%s', sampling_rate='%f'" \
               ", data_rate='%i')>" % (self.id_sensor_type, self.name, self.hw_name, self.location, self.sampling_rate,
                                       self.data_rate)


"""

class Sensor:
    def __init__(self, *args, **kwargs):
        # Default values
        self._id_sensor = kwargs.get('id_sensor', None)
        self._id_sensor_type = kwargs.get('id_sensor_type', None)
        self._name = kwargs.get('name', None)
        self._hw_name = kwargs.get('hw_name', None)
        self._location = kwargs.get('location', None)
        self._sampling_rate = kwargs.get('sampling_rate', None)
        self._data_rate = kwargs.get('data_rate', None)

        for arg in args:
            if isinstance(arg,tuple):
                self.from_tuple(arg)
            elif isinstance(arg, Sensor):
                self.from_tuple(arg.as_tuple())

        # Validation
        if self._id_sensor_type is not None:
            SensorType.sensor_type_validation(self._id_sensor_type)

    def __str__(self):
        return "Sensor: " + str(self.as_tuple())

    def __eq__(self, other):
        return self.as_tuple() == other.as_tuple()

    def set_id_sensor(self, id_sensor):
        self._id_sensor = id_sensor

    def get_id_sensor(self):
        return self._id_sensor

    def set_id_sensor_type(self, id_sensor_type):
        SensorType.sensor_type_validation(id_sensor_type)
        self._id_sensor_type = id_sensor_type

    def get_id_sensor_type(self):
        return self._id_sensor_type

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_hw_name(self, hw_name):
        self._hw_name = hw_name

    def get_hw_name(self):
        return self._hw_name

    def set_location(self, location):
        self._location = location

    def get_location(self):
        return self._location

    def set_sampling_rate(self, sampling_rate):
        self._sampling_rate = sampling_rate

    def get_sampling_rate(self):
        return self._sampling_rate

    def set_data_rate(self, data_rate):
        self._data_rate = data_rate

    def get_data_rate(self):
        return self._data_rate

    def as_tuple(self):
        return self.id_sensor, self.id_sensor_type, self.name, self.hw_name, \
               self.location, self.sampling_rate, self.data_rate

    def from_tuple(self, tuple):
        (self._id_sensor, self._id_sensor_type, self._name, self._hw_name,
         self._location, self._sampling_rate, self._data_rate) = tuple



    # Properties
    id_sensor = property(get_id_sensor, set_id_sensor)
    id_sensor_type = property(get_id_sensor_type, set_id_sensor_type)
    name = property(get_name, set_name)
    hw_name = property(get_hw_name, set_hw_name)
    location = property(get_location, set_location)
    sampling_rate = property(get_sampling_rate, set_sampling_rate)
    data_rate = property(get_data_rate, set_data_rate)

"""

