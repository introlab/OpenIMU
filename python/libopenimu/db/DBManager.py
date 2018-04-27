"""
 DBManager
 Will contain sqlite driver and model interface
 @authors Simon Brière, Dominic Létourneau
 @date 27/03/2018
"""

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import table, insert

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
from libopenimu.models.DataSet import DataSet

"""
TODO This might be optimized?

Offering the same interface as DBManagerOld

"""


class DBManager:
    def __init__(self, filename, overwrite=False, echo=False):
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

    def flush(self):
        self.session.flush()

    def create_session(self):
        return self.SessionMaker()

    def session_add(self, store):
        self.session.add_all(store)

    ######## GROUPS
    def update_group(self, group):
        try:
            if group.id_group is None:
                self.session.add(group)
            else:
                src_group = self.session.query(Group).filter(Group.id_group == group.id_group).first()
                src_group.name = group.name
                src_group.description = group.description
                group.id_group = src_group.id_group

            self.commit()
            return group

        except Exception as e:
            message = 'Error updating group' + ': ' + str(e)
            print('Error: ', message)
            raise

    def delete_group(self, group):
        try:
            self.session.delete(group)
            self.commit()
        except Exception as e:
            message = 'Error deleting group' + ': ' + str(e)
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

    ######## PARTICIPANTS
    def update_participant(self, participant):
        try:
            if participant.id_participant is None:
                self.session.add(participant)
            else:
                src_part = self.session.query(Participant).filter(Participant.id_participant == participant.id_participant).first()
                src_part.name = participant.name
                src_part.description = participant.description
                src_part.id_group = participant.id_group
                participant.id_participant = src_part.id_participant

            self.commit()
            return participant

        except Exception as e:
            message = 'Error updating participant' + ': ' + str(e)
            print('Error: ', message)
            raise

    def get_participant(self, id_participant):
        query = self.session.query(Participant).filter(Participant.id_participant == id_participant)
        return query.first()

    """def get_all_participants(self):
        query = self.session.query(Participant)
        return query.all()
    """

    def get_participants_for_group(self,group):
        if group is not None:
            query = self.session.query(Participant).filter(Participant.id_group == group.id_group)
        else:
            query = self.session.query(Participant).filter(Participant.id_group == None)
        return query.all()

    def delete_participant(self, part):
        try:
            self.session.delete(part)
            self.commit()
        except Exception as e:
            message = 'Error deleting participant' + ': ' + str(e)
            print('Error: ', message)
            raise

    #####################
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
        record = Recordset(participant=participant, name=name, start_timestamp=start_timestamp,
                           end_timestamp=end_timestamp)
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

    def get_all_channels(self, **kwargs):
        sensor = kwargs.get('sensor', None)

        # Get all channels
        query = self.session.query(Channel)

        if sensor is not None:
            query = query.filter(Channel.id_sensor == sensor.id_sensor)

        # Return all channels
        return query.all()

    def add_sensor_data(self, recordset: Recordset, sensor: Sensor, channel: Channel, timestamp, data):

        # Create object
        sensordata = SensorData(recordset=recordset, sensor=sensor,
                                channel=channel, data_timestamp=timestamp, data=data.tobytes())

        # Custom SQL code
        """
        self.session.execute("INSERT INTO tabSensorsData (id_recordset, id_sensor, id_channel, data_timestamp, data) "
                             "VALUES (:id_recordset, :id_sensor, :id_channel, :data_timestamp, :data)",
                             {'id_recordset': recordset.id_recordset, 'id_sensor': sensor.id_sensor,
                              'id_channel': channel.id_channel, 'data_timestamp': timestamp, 'data': data.tobytes()})

        """

        self.session.add(sensordata)

        # Do not commit, too slow!
        return sensordata

    def get_sensor_data(self, id_sensor_data):

        query = self.session.query(SensorData).filter(SensorData.id_sensor_data == id_sensor_data)

        my_sensor_data = query.first()

        # Do something to convert bytes in the right format
        my_sensor_data.data = DataFormat.from_bytes(my_sensor_data.data, my_sensor_data.channel.id_data_format)

        return my_sensor_data

    def get_all_sensor_data(self, recordset: Recordset, **kwargs):

        # Initialize from kwargs (and default values)
        convert = kwargs.get('convert', False)
        sensor = kwargs.get('sensor', None)
        channel = kwargs.get('channel', None)

        # Get all sensor data from recordset
        query = self.session.query(SensorData).filter(SensorData.id_recordset == recordset.id_recordset)

        if sensor is not None:
            # print('Should filter sensor id', sensor.id_sensor)
            query = query.filter(SensorData.id_sensor == sensor.id_sensor)

        if channel is not None:
            # print('Should filter channel', channel.id_channel)
            query = query.filter(SensorData.id_channel == channel.id_channel)

        # print(query)

        if not convert:
            return query.all()
        else:
            # Read result, data will be bytes array
            result = query.all()

            # Convert to the right format
            for sensor_data in result:
                # print('data len:', len(sensor_data.data))
                sensor_data.data = DataFormat.from_bytes(sensor_data.data, sensor_data.channel.id_data_format)

            return result

    def set_dataset_infos(self, name, desc, creation_date, upload_date, author):

        try:
            self.session.query(DataSet).delete()
            self.session.commit()
            dataset = DataSet(name=name, description=desc, creation_date=creation_date, upload_date=upload_date, author=author)
            self.session.add(dataset)
            self.commit()
            return dataset

        except Exception as e:
            message = 'Error setting dataset infos' + ': ' + str(e)
            print('Error: ', message)
            raise

    def get_dataset(self):
        query = self.session.query(DataSet)
        return query.first()

    def close(self):
        self.session.close()
