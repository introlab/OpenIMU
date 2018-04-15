"""

Testing sqlalchemy ORM...

"""
import sqlalchemy

from sqlalchemy import Column, Integer, Float, String, Sequence, TIMESTAMP, BLOB, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from libopenimu.models.sensor_types import SensorType as SensorType
from libopenimu.models.units import Units as Units
from libopenimu.models.data_formats import DataFormat as DataFormat

import os
import datetime
import numpy as np

# Declarative Base class definition
Base = declarative_base()


class DBSensorType(Base):
    __tablename__ = 'tabSensorTypes'
    id_sensor_type = Column(Integer, Sequence('id_sensor_type_sequence'), primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    # Database rep (optional)
    def __repr__(self):
        return "<DBSensorType(name='%s')>" % self.name


# Not used...
class DBDataFormat(Base):
    __tablename__ = 'tabDataFormats'
    id_data_format = Column(Integer, Sequence('id_data_format_sequence'), primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    # Database rep (optional)
    def __repr__(self):
        return "<DBDataFormat(name='%s')>" % self.name


# Not used...
class Group(Base):
    __tablename__ = 'tabGroups'

    id_group = Column(Integer, Sequence('id_group_sequence'), primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)

    # Database rep (optional)
    def __repr__(self):
        return "<Group(name='%s', description='%s')>" % (self.name, self.description)


class Participant(Base):
    __tablename__ = 'tabParticipants'
    id_participant = Column(Integer, Sequence('id_participant_sequence'), primary_key=True, autoincrement=True)
    id_group = Column(Integer, ForeignKey("tabGroups.id_group"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)

    # Which group
    group = relationship("Group")

    # Database rep (optional)
    def __repr__(self):
        return "<Participant(id_group='%i', name='%s', description='%s')>" % (self.id_group, self.name, self.description)


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

    # Database rep (optional)
    def __repr__(self):
        return "<Sensor(id_sensor_type='%i', name='%s', hw_name='%s', location='%s', sampling_rate='%f'" \
               ", data_rate='%i')>" % (self.id_sensor_type, self.name, self.hw_name, self.location, self.sampling_rate,
                                       self.data_rate)


class Channel(Base):
    __tablename__ = 'tabChannels'
    id_channel = Column(Integer, Sequence('id_channel_sequence'), primary_key=True, autoincrement=True)
    id_sensor = Column(Integer, ForeignKey('tabSensors.id_sensor'), nullable=False)
    id_sensor_unit = Column(Integer, nullable=False)
    id_data_format = Column(Integer, nullable=False)
    label = Column(String, nullable=False)

    # Relationships
    sensor = relationship("Sensor")

    # Database rep (optional)
    def __repr__(self):
        return "<Channel(id_sensor='%i', id_sensor_unit='%s', id_data_format='%s', label='%s'" % \
               (self.id_sensor, self.id_sensor_unit, self.id_data_format, self.label)


class Recordset(Base):
    __tablename__ = 'tabRecordsets'
    id_recordset = Column(Integer, Sequence('id_recordset_sequence'), primary_key=True, autoincrement=True)
    id_participant = Column(Integer, ForeignKey('tabParticipants.id_participant'), nullable=False)
    name = Column(String, nullable=False)
    start_timestamp = Column(TIMESTAMP, nullable=False)
    end_timestamp = Column(TIMESTAMP, nullable=False)

    # Relationships
    participant = relationship("Participant")

    # Database rep (optional)
    def __repr__(self):
        return "<Recordset(id_participant='%i', name='%s', start_timestamp='%s', end_timestamp='%s'" % \
               (self.id_participant, self.name, self.start_timestamp, self.end_timestamp)


class SensorData(Base):
    __tablename__ = 'tabSensorsData'
    id_sensor_data = Column(Integer, Sequence('id_sensor_data_sequence'), primary_key=True, autoincrement=True)
    id_recordset = Column(Integer, ForeignKey('tabRecordsets.id_recordset'), nullable=False)
    id_sensor = Column(Integer, ForeignKey('tabSensors.id_sensor'), nullable=False)
    id_channel = Column(Integer, ForeignKey('tabChannels.id_channel'), nullable=False)
    data_timestamp = Column(TIMESTAMP, nullable=False)
    data = Column(BLOB, nullable=False)

    # Relationships
    recordset = relationship("Recordset")
    sensor = relationship("Sensor")
    channel = relationship("Channel")

    # Database rep (optional)
    def __repr__(self):
        return "<SensorData(id_recordset='%i', id_sensor='%i', id_channel='%i', data_timestamp='%s', data_size='%i'" % \
               (self.id_recordset, self.id_sensor, self.id_channel, self.data_timestamp, len(self.data))


# Main
if __name__ == '__main__':

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # Cleanup database
    if os.path.isfile('test.db'):
        print('removing database')
        os.remove('test.db')

    # engine = create_engine('sqlite:///:memory:', echo=True)
    engine = create_engine('sqlite:///test.db', echo=True)

    # Will create all tables
    Base.metadata.create_all(engine)

    # Will create Session interface class
    Session = sessionmaker(bind=engine)

    # Session instance
    session = Session()

    # TODO ?
    # Populate database with sensor types
    # Populate database with data formats

    print('Starting... sqlalchemy version: ', sqlalchemy.__version__)
    mygroup1 = Group(name='MyName', description='MyDescription')
    mygroup2 = Group(name='MyName', description='MyDescription')

    participant1 = Participant(name='My Participant Name', description='My Participant description')
    participant1.group = mygroup1

    recordset1 = Recordset(name="Record Name", start_timestamp=datetime.datetime.now(), end_timestamp=datetime.datetime.now())
    recordset1.participant = participant1

    sensor1 = Sensor(id_sensor_type=SensorType.ACCELEROMETER, name='Sensor Name', hw_name='Hardware name',
                     location='Wrist', sampling_rate=30.0, data_rate=1)

    channel1 = Channel(id_sensor_unit=Units.GRAVITY_G, id_data_format=DataFormat.FLOAT32, label="custom label")
    channel1.sensor = sensor1

    sensordata1 = SensorData(data_timestamp=datetime.datetime.now())
    sensordata1.data = np.zeros(40)
    sensordata1.sensor = sensor1
    sensordata1.channel = channel1
    sensordata1.recordset = recordset1


    # Add objects to session
    session.add(mygroup1)
    session.add(mygroup2)
    session.add(participant1)
    session.add(recordset1)
    session.add(sensor1)
    session.add(channel1)
    session.add(sensordata1)
    session.commit()

    # Should generate a DB update...
    participant1.group = mygroup2
    session.commit()

    print(recordset1)