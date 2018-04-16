"""
 DBManager
 Will contain sqlite driver and model interface
 @authors Simon Brière, Dominic Létourneau
 @date 27/03/2018
"""

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
import datetime

# Basic definitions
from libopenimu.models.sensor_types import SensorType
from libopenimu.models.data_formats import DataFormat
from libopenimu.models.units import Units

# All the models
from libopenimu.models.Base import Base
from libopenimu.models.Group import Group
from libopenimu.models.Sensor import Sensor
from libopenimu.models.Participant import Participant
from libopenimu.models.Recordset import Recordset
from libopenimu.models.Channel import Channel
from libopenimu.models.SensorData import SensorData

"""
TODO This might be optimized?

Offering the same interface as DBManagerOld

"""


class DBManager:
    def __init__(self, filename, overwrite=False, echo=True):
        # Cleanup database
        if overwrite is True:
            if os.path.isfile(filename):
                print('removing database')
                os.remove(filename)

        print('Using sqlalchemy version: ', sqlalchemy.__version__)

        # Create engine (sqlite), echo will output logging information
        self.engine = create_engine('sqlite:///' + filename, echo=echo)

        # Will create all tables
        Base.metadata.create_all(self.engine)

        # Will create Session interface class
        self.SessionMaker = sessionmaker(bind=self.engine)

        # Session instance
        self.session = self.SessionMaker()

    def commit(self):
        self.session.commit()

    def add_group(self, name, description):
        try:
            group = Group(name=name, description=description)
            self.session.add(group)
            self.commit()
            return group

        except Exception as e:
            message = 'Error adding group' + ': ' + str(e)
            print('Error: ', message)
            raise

    def get_group(self, id_group):
        query = self.session.query(Group).filter(Group.id_group == id_group)
        # print('first group', query.first())
        return query.first()

    def get_all_groups(self):
        query = self.session.query(Group)
        # print('all groups', query.all())
        return query.all()

    def add_participant(self, group: Group, name, description):
        # Create object
        participant = Participant(group=group, name=name, description=description)
        self.session.add(participant)
        self.commit()
        return participant

    def get_participant(self, id_participant):
        query = self.session.query(Participant).filter(Participant.id_participant == id_participant)
        return query.first()

    def get_all_participants(self):
        query = self.session.query(Participant)
        return query.all()

    def add_sensor(self, _id_sensor_type, _name, _hw_name, _location, _sampling_rate, _data_rate):
        # Create object
        sensor = Sensor(
                        id_sensor_type=_id_sensor_type,
                        name=_name,
                        hw_name=_hw_name,
                        location=_location,
                        sampling_rate=_sampling_rate,
                        data_rate=_data_rate)

        self.session.add(sensor)
        self.commit()
        return sensor

    def get_sensor(self, id_sensor):
        query = self.session.query(Sensor).filter(Sensor.id_sensor == id_sensor)
        # print('first sensor', query.first())
        return query.first()

    def get_all_sensors(self, id_sensor_type=None):
        if id_sensor_type is None:
            query = self.session.query(Sensor)
            return query.all()
        else:
            query = self.session.query(Sensor).filter(Sensor.id_sensor_type == id_sensor_type)
            return query.all()

    def add_recordset(self, participant: Participant, name, start_timestamp, end_timestamp):
        # Create object
        record = Recordset(participant=participant, name=name, start_timestamp=start_timestamp, end_timestamp=end_timestamp)
        self.session.add(record)
        self.commit()
        return record

    def get_recordset(self, id_recordset):
        query = self.session.query(Recordset).filter(Recordset.id_recordset == id_recordset)
        print('get_recordset', query.first())
        return query.first()

    def get_all_recordsets(self, participant=Participant()):
        if participant.id_participant is None:
            query = self.session.query(Recordset)
            return query.all()
        else:
            query = self.session.query(Recordset).filter(Recordset.id_participant == participant.id_participant)
            return query.all()

    def add_channel(self, sensor, id_sensor_unit, id_data_format, label):
        # Create object
        channel = Channel(sensor=sensor, id_sensor_unit=id_sensor_unit,
                          id_data_format=id_data_format, label=label)

        self.session.add(channel)
        self.commit()
        return channel

    def get_channel(self, id_channel):
        query = self.session.query(Channel).filter(Channel.id_channel == id_channel)
        return query.first()

    def add_sensor_data(self, recordset: Recordset, sensor: Sensor, channel: Channel, timestamp, data):
        # Create object
        sensordata = SensorData(recordset=recordset, sensor=sensor,
                                channel=channel, data_timestamp=timestamp, data=data)

        self.session.add(sensordata)

        # Do not commit, too slow!
        # self.commit()
        return sensordata

    def get_sensor_data(self, id_sensor_data):

        query = self.session.query(SensorData).filter(SensorData.id_sensor_data == id_sensor_data)

        my_sensor_data = query.first()

        # Do something to convert bytes in the right format
        my_sensor_data.data = DataFormat.from_bytes(my_sensor_data.data, my_sensor_data.channel.id_data_format)

        return my_sensor_data
