"""

Testing sqlalchemy ORM...

"""
import sqlalchemy

from sqlalchemy import Column, Integer, Float, String, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import os

# Declarative Base class definition
Base = declarative_base()


class SensorType(Base):
    __tablename__ = 'tabSensorTypes'
    id_sensor_type = Column(Integer, Sequence('id_sensor_type_sequence'), primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    @staticmethod
    def all_types():
        from libopenimu.models.sensor_types import SensorType as st
        dict = st.as_dict()

        result = []
        for key in dict:
            result.append(SensorType(id_sensor_type=key, name=dict[key]))

        return result

    # Database rep (optional)
    def __repr__(self):
        return "<SensorType(name='%s')>" % self.name


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
    id_sensor_type = Column(Integer, ForeignKey('tabSensorTypes.id_sensor_type'), nullable=False)
    name = Column(String, nullable=False)
    hw_name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    sampling_rate = Column(Float, nullable=False)
    data_rate = Column(Integer, nullable=False)

    # Which sensor type
    sensor_type = relationship("SensorType")

    # Database rep (optional)
    def __repr__(self):
        return "<Sensor(id_sensor_type='%i', name='%s', hw_name='%s', location='%s', sampling_rate='%f'" \
               ", data_rate='%i')>" % (self.id_sensor_type, self.name, self.hw_name, self.location, self.sampling_rate,
                                       self.data_rate)


class Channel(Base):
    __tablename__ = 'tabChannels'
    id_channel = Column(Integer, Sequence('id_channel_sequence'), primary_key=True, autoincrement=True)
    id_sensor = Column(Integer, ForeignKey('tabSensors.id_sensor'), nullable=False)


# Main
if __name__ == '__main__':

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    #Cleanup database
    if os.path.isfile('test.db'):
        print('removing database')
        os.remove('test.db')

    # engine = create_engine('sqlite:///:memory:', echo=True)
    engine = create_engine('sqlite:///test.db', echo=True)

    # Will create all tables
    Base.metadata.create_all(engine)

    objects = SensorType.all_types()
    print(objects)

    # Will create Session interface class
    Session = sessionmaker(bind=engine)

    # Session instance
    session = Session()

    # session.add(objects)
    for o in objects:
        session.add(o)

    print('Starting... sqlalchemy version: ', sqlalchemy.__version__)
    mygroup1 = Group(name='MyName', description='MyDescription')
    mygroup2 = Group(name='MyName', description='MyDescription')

    participant = Participant(name='My Participant Name', description='My Participant description')

    participant.group = mygroup1

    session.add(mygroup1)
    session.add(mygroup2)
    session.add(participant)
    session.commit()

    participant.group = mygroup2
    session.commit()

    print(participant.group.description)