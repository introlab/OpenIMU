"""

Testing sqlalchemy ORM...

"""

import sqlalchemy

from libopenimu.models.Group import Group
from libopenimu.models.Sensor import Sensor
from libopenimu.models.Participant import Participant
from libopenimu.models.Recordset import Recordset
from libopenimu.models.Base import Base
from libopenimu.models.Channel import Channel
from libopenimu.models.sensor_types import SensorType
from libopenimu.models.data_formats import DataFormat
from libopenimu.models.units import Units
from libopenimu.models.SensorData import SensorData

import os
import datetime
import numpy as np



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