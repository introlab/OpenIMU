"""
 DBManager
 Will contain sqlite driver and model interface
 @authors Simon Brière, Dominic Létourneau
 @date 27/03/2018
"""

import sqlalchemy
from sqlalchemy import create_engine, asc, or_, and_
from sqlalchemy.orm import sessionmaker
# noinspection PyProtectedMember
from sqlalchemy.engine import Engine
from sqlalchemy import event, text

import os
import datetime
import pickle
import sys
import warnings

from PySide6.QtCore import QObject, Signal

# Basic definitions
from libopenimu.models.data_formats import DataFormat

# All the models
from libopenimu.models.Base import Base
from libopenimu.models.Group import Group
from libopenimu.models.Sensor import Sensor
from libopenimu.models.Participant import Participant
from libopenimu.models.Recordset import Recordset
from libopenimu.models.Channel import Channel
from libopenimu.models.SensorData import SensorData
from libopenimu.models.sensor_types import SensorType
from libopenimu.models.SensorTimestamps import SensorTimestamps
from libopenimu.models.DataSet import DataSet
from libopenimu.models.ProcessedData import ProcessedData
from libopenimu.models.ProcessedDataRef import ProcessedDataRef

from alembic.config import Config
from alembic import command


class DBManager(QObject):

    groupUpdated = Signal(Group)
    participantUpdated = Signal(Participant)

    def __init__(self, filename, overwrite=False, echo=False, newfile=False):
        QObject.__init__(self)
        warnings.simplefilter(action='ignore', category=FutureWarning)

        dburl = 'sqlite:///' + filename + '?check_same_thread=False'
        # Cleanup database
        if overwrite is True:
            if os.path.isfile(filename):
                print('removing database')
                os.remove(filename)

        # print('Using sqlalchemy version: ', sqlalchemy.__version__)

        # Create engine (sqlite), echo will output logging information
        self.engine = create_engine(dburl, echo=echo)

        # Will create all tables
        Base.metadata.create_all(self.engine)

        if newfile is False:
            # Check if database scheme upgrade is needed
            self.upgrade_db(dburl=dburl)
        else:
            # Stamp the database with the latest migration id
            self.stamp_db(dburl=dburl)

        # Will create Session interface class
        self.SessionMaker = sessionmaker(bind=self.engine)

        # Session instance
        self.session = self.SessionMaker()

        # Keep copy of the filename
        self.dbFilename = filename

    @staticmethod
    def init_alembic(dburl):
        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle, the pyInstaller bootloader
            # extends the sys module by a flag frozen=True and sets the app
            # path into variable _MEIPASS'.
            this_file_directory = sys._MEIPASS
            # When frozen, file directory = executable directory
            root_directory = this_file_directory
        else:
            this_file_directory = os.path.dirname(os.path.abspath(__file__))
            root_directory = os.path.join(this_file_directory, '..' + os.sep + '..')

        # this_file_directory = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))

        alembic_directory = os.path.join(root_directory, 'alembic')
        ini_path = os.path.join(root_directory, 'alembic.ini')

        # create Alembic config and feed it with paths
        config = Config(ini_path)
        config.set_main_option('script_location', alembic_directory)
        config.set_main_option('sqlalchemy.url', dburl)

        return config

    def upgrade_db(self, dburl):
        config = self.init_alembic(dburl)

        # prepare and run the command
        revision = 'head'
        sql = False
        tag = None

        # upgrade command
        command.upgrade(config, revision, sql=sql, tag=tag)

    def stamp_db(self, dburl):
        config = self.init_alembic(dburl)

        # prepare and run the command
        revision = 'head'
        sql = False
        tag = None

        # Stamp database
        command.stamp(config, revision, sql, tag)

    @staticmethod
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    def close(self):
        self.session.close()

    def commit(self):
        self.session.commit()

    def flush(self):
        self.session.flush()

    def create_session(self):
        return self.SessionMaker()

    def session_add(self, store):
        self.session.add_all(store)

    def compact(self):
        self.clean_db()
        with self.engine.connect() as connection:
            connection.execute(text("VACUUM"))

    # GROUPS
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
            self.groupUpdated.emit(group)
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

        # Check if we have orphan items dandling around
        # self.clean_db()
        # self.engine.execute("VACUUM")

    def get_group(self, id_group):
        query = self.session.query(Group).filter(Group.id_group == id_group)
        # print('first group', query.first())
        return query.first()

    def get_all_groups(self):
        query = self.session.query(Group)
        # print('all groups', query.all())
        return query.all()

    # PARTICIPANTS
    def update_participant(self, participant):
        try:
            if participant.id_participant is None:
                self.session.add(participant)
            else:
                src_part = self.session.query(Participant).filter(
                    Participant.id_participant == participant.id_participant).first()
                src_part.name = participant.name
                src_part.description = participant.description
                src_part.id_group = participant.id_group
                participant.id_participant = src_part.id_participant

            self.commit()
            self.participantUpdated.emit(participant)
            return participant

        except Exception as e:
            message = 'Error updating participant' + ': ' + str(e)
            print('Error: ', message)
            raise

    def get_participant(self, id_participant) -> Participant:
        query = self.session.query(Participant).filter(Participant.id_participant == id_participant)
        return query.first()

    def get_processed_data(self, id_processed_data) -> ProcessedData:
        query = self.session.query(ProcessedData).filter(ProcessedData.id_processed_data == id_processed_data)
        return query.first()

    def get_all_participants(self):
        query = self.session.query(Participant).order_by(Participant.name.asc(), Participant.id_group.asc())
        return query.all()

    def get_participants_for_group(self, group):
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

        # Check if we have orphan items dandling around
        # self.clean_db()
        # self.engine.execute("VACUUM")

    #
    def add_sensor(self, _id_sensor_type, _name, _hw_name, _location, _sampling_rate, _data_rate):
        # Check if that sensor is already present in the database
        query = self.session.query(Sensor).filter((Sensor.id_sensor_type == _id_sensor_type) &
                                                  (Sensor.location == _location) &
                                                  (Sensor.name == _name) &
                                                  (Sensor.hw_name == _hw_name) &
                                                  (Sensor.sampling_rate == _sampling_rate) &
                                                  (Sensor.data_rate) == _data_rate)

        if query.first():
            # print("Sensor " + _name + " already present in DB!")
            return query.first();

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

    def add_recordset(self, participant: Participant, name, start_timestamp, end_timestamp, force=False):

        if not force:  # Check if we already have a recordset for that period
            query = self.session.query(Recordset).filter(
                (Recordset.participant == participant) & (Recordset.name == name))
            if query.first():
                # Update start and end times, if needed.
                current_record = query.first()
                # print("Recordset found: " + current_record.name)
                new_starttime = current_record.start_timestamp
                if start_timestamp < new_starttime:
                    new_starttime = start_timestamp
                new_endtime = current_record.end_timestamp
                if end_timestamp > new_endtime:
                    new_endtime = end_timestamp
                current_record.start_timestamp = new_starttime
                current_record.end_timestamp = new_endtime
                self.commit()
                return current_record

        # Create object
        record = Recordset(participant=participant, name=name, start_timestamp=start_timestamp,
                           end_timestamp=end_timestamp)
        self.session.add(record)
        self.commit()
        return record

    def get_recordset(self, id_recordset) -> Recordset | None:
        query = self.session.query(Recordset).filter(Recordset.id_recordset == id_recordset)
        # print('get_recordset', query.first())
        return query.first()

    def delete_recordset(self, recordset):
        # id = recordset.id_recordset
        try:
            self.session.delete(recordset)
            self.commit()
        except Exception as e:
            message = 'Error deleting recordset' + ': ' + str(e)
            print('Error: ', message)
            raise

        # Check if we have orphan items dandling around
        # self.clean_db()

    def delete_orphan_sensors(self):
        query = self.session.query(Sensor.id_sensor).outerjoin(SensorData).filter(SensorData.id_sensor_data == None)
        orphan_sensors = query.all()
        if len(orphan_sensors) > 0:
            query = self.session.query(Sensor).filter(Sensor.id_sensor.in_(query))
            query.delete(synchronize_session=False)
            self.commit()

    def delete_orphan_channels(self):
        query = self.session.query(Channel.id_channel).outerjoin(SensorData).filter(SensorData.id_sensor_data == None)
        orphan_channels = query.all()
        if len(orphan_channels) > 0:
            query = self.session.query(Channel).filter(Channel.id_channel.in_(query))
            query.delete(synchronize_session=False)
            self.commit()

    def delete_orphan_processed_data(self):
        query = self.session.query(ProcessedData.id_processed_data).outerjoin(ProcessedDataRef).filter(
            ProcessedDataRef.id_processed_data_ref == None)
        orphan = query.all()
        if len(orphan) > 0:
            query = self.session.query(ProcessedData).filter(ProcessedData.id_processed_data.in_(query))
            query.delete(synchronize_session=False)
            self.commit()

    def delete_orphan_sensors_timestamps(self):
        query = self.session.query(SensorTimestamps.id_sensor_timestamps).outerjoin(SensorData).filter(
            SensorData.id_sensor_data == None)
        orphan = query.all()
        if len(orphan) > 0:
            query = self.session.query(SensorTimestamps).filter(SensorTimestamps.id_sensor_timestamps.in_(query))
            query.delete(synchronize_session=False)
            self.commit()

    def clean_db(self):
        self.delete_orphan_channels()
        self.delete_orphan_sensors()
        self.delete_orphan_processed_data()
        self.delete_orphan_sensors_timestamps()
        # self.engine.execute("VACUUM")

    def get_all_recordsets(self, participant=Participant(), start_date=None):
        from sqlalchemy import func
        if start_date is not None:
            query = self.session.query(Recordset).filter(func.date(Recordset.start_timestamp) == start_date) \
                .order_by(asc(Recordset.start_timestamp))
            if participant.id_participant is not None:
                query = query.filter(Recordset.id_participant == participant.id_participant)
            return query.all()

        if participant.id_participant is None:
            query = self.session.query(Recordset).order_by(asc(Recordset.start_timestamp))
            # print (query)
            return query.all()
        else:
            query = self.session.query(Recordset).filter(Recordset.id_participant == participant.id_participant) \
                .order_by(asc(Recordset.start_timestamp))
            return query.all()

    def get_sensors(self, recordset):
        query = self.session.query(Sensor).join(SensorData).filter(SensorData.id_recordset == recordset.id_recordset) \
            .group_by(Sensor.id_sensor).order_by(asc(Sensor.location)).order_by(asc(Sensor.name))
        return query.all()

    def add_channel(self, sensor, id_sensor_unit, id_data_format, label):
        # Check if that sensor is already present in the database
        query = self.session.query(Channel).filter((Channel.sensor == sensor) &
                                                   (Channel.id_sensor_unit == id_sensor_unit) &
                                                   (Channel.id_data_format == id_data_format) &
                                                   (Channel.label == label))

        if query.first():
            # print("Channel " + label + " already present in DB!")
            return query.first()

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

    def add_sensor_data(self, recordset: Recordset, sensor: Sensor, channel: Channel, timestamps: SensorTimestamps,
                        data):

        # Create object
        sensordata = SensorData(recordset=recordset, sensor=sensor,
                                channel=channel, timestamps=timestamps,
                                data=data.tobytes())

        self.session.add(sensordata)

        # Do not commit, too slow!
        return sensordata

    def get_sensor_data(self, id_sensor_data):

        query = self.session.query(SensorData).filter(SensorData.id_sensor_data == id_sensor_data)

        my_sensor_data = query.first()

        # Do something to convert bytes in the right format
        my_sensor_data.data = DataFormat.from_bytes(my_sensor_data.data, my_sensor_data.channel.id_data_format)

        return my_sensor_data

    def get_all_sensor_data(self, **kwargs):

        # Initialize from kwargs (and default values)
        convert = kwargs.get('convert', False)
        sensor = kwargs.get('sensor', None)
        channel = kwargs.get('channel', None)
        recordset = kwargs.get('recordset', None)
        start_time = kwargs.get('start_time', None)
        end_time = kwargs.get('end_time', None)

        # Get all sensor data
        query = self.session.query(SensorData)

        if recordset is not None:
            query = query.filter(SensorData.id_recordset == recordset.id_recordset)

        if sensor is not None:
            # print('Should filter sensor id', sensor.id_sensor)
            query = query.filter(SensorData.id_sensor == sensor.id_sensor)

        if channel is not None:
            # print('Should filter channel', channel.id_channel)
            query = query.filter(SensorData.id_channel == channel.id_channel)

        if start_time is not None:
            query = query.filter(or_(SensorData.timestamps.has(SensorTimestamps.start_timestamp >= start_time),
                                     and_(SensorData.timestamps.has(SensorTimestamps.start_timestamp <= start_time),
                                          SensorData.timestamps.has(SensorTimestamps.end_timestamp >= start_time))))

        if end_time is not None:
            query = query.filter(or_(SensorData.timestamps.has(SensorTimestamps.end_timestamp <= end_time),
                                     and_(SensorData.timestamps.has(SensorTimestamps.start_timestamp <= end_time),
                                          SensorData.timestamps.has(SensorTimestamps.end_timestamp >= end_time))))

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

    def get_sensor_times(self, sensor: Sensor, recordset: Recordset):
        # from sqlalchemy.orm import noload
        query = self.session.query(SensorTimestamps).join(SensorData).filter(SensorData.id_sensor == sensor.id_sensor) \
            .filter(SensorData.id_recordset == recordset.id_recordset) \
            .filter(SensorData.id_channel == sensor.channels[0].id_channel)
        return query.all()

    def set_dataset_infos(self, name, desc, creation_date, upload_date, author):

        try:
            self.session.query(DataSet).delete()
            self.session.commit()
            dataset = DataSet(name=name, description=desc, creation_date=creation_date, upload_date=upload_date,
                              author=author)
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

    #####################
    def add_processed_data(self, data_processor_id: int, name: str, results, recordsets, params: dict):
        import json
        # Add results
        data = ProcessedData()
        data.id_data_processor = data_processor_id
        data.data = pickle.dumps(results)
        data.name = name
        data.processed_time = datetime.datetime.now()
        data.params = json.dumps(params)

        self.session.add(data)
        self.commit()

        # Add references
        for record in recordsets:
            ref = ProcessedDataRef()
            ref.id_processed_data = data.id_processed_data
            ref.recordset = record
            self.session.add(ref)
            self.commit()

        return data

    def get_all_processed_data(self, participant=Participant()):
        if participant.id_participant is None:
            query = self.session.query(ProcessedData)
            datas = query.all()
        else:
            query = self.session.query(ProcessedData).join(ProcessedDataRef).join(Recordset).join(Participant).filter(
                Participant.id_participant == participant.id_participant)
            datas = query.all()

        return datas

    def delete_processed_data(self, result):
        try:
            self.session.delete(result)
            self.commit()
        except Exception as e:
            message = 'Error deleting processed data' + ': ' + str(e)
            print('Error: ', message)
            raise
