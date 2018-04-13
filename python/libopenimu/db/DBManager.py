"""
 DBManager
 Will contain sqlite driver and model interface
 @authors Simon Brière, Dominic Létourneau
 @date 27/03/2018
"""

import sqlite3
import os
import time

# Basic definitions
from libopenimu.models.sensor_types import SensorType
from libopenimu.models.data_formats import DataFormat
from libopenimu.models.units import Units

# All the models
from libopenimu.models.Group import Group
from libopenimu.models.Sensor import Sensor
from libopenimu.models.Participant import Participant
from libopenimu.models.Recordset import Recordset
from libopenimu.models.Channel import Channel
from libopenimu.models.SensorData import SensorData

import numpy as np

sql_init_script = '''

CREATE TABLE tabUnits (
                id_unit INTEGER PRIMARY KEY NOT NULL,
                name VARCHAR NOT NULL
);


CREATE TABLE tabSensorTypes (
                id_sensor_type INTEGER PRIMARY KEY NOT NULL,
                name VARCHAR NOT NULL
);


CREATE TABLE tabGroups (
                id_group INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name VARCHAR NOT NULL,
                description VARCHAR NOT NULL);


CREATE TABLE tabParticipants (
                id_participant INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_group INTEGER,
                name VARCHAR NOT NULL,
                description VARCHAR,
		FOREIGN KEY (id_group) REFERENCES tabGroups (id_group) ON DELETE CASCADE ON UPDATE NO ACTION
);


CREATE TABLE tabRecordsets (
                id_recordset INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_participant INTEGER NOT NULL,
                name VARCHAR NOT NULL,
                start_timestamp DATETIME NOT NULL,
                end_timestamp DATETIME NOT NULL,
		FOREIGN KEY (id_participant) REFERENCES tabParticipants (id_participant) ON DELETE CASCADE ON UPDATE NO ACTION
);


CREATE TABLE tabSubrecords (
                id_subrecord INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_recordset INTEGER NOT NULL,
                name VARCHAR NOT NULL,
                start_timestamp DATETIME NOT NULL,
                end_timestamp DATETIME NOT NULL,
		FOREIGN KEY (id_recordset) REFERENCES tabRecordsets (id_recordset) ON DELETE CASCADE ON UPDATE NO ACTION
);


CREATE TABLE tabDataProcessors (
                id_data_processor INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name VARCHAR NOT NULL,
                unique_id VARCHAR NOT NULL,
                version DOUBLE PRECISIONS NOT NULL,
                author VARCHAR NOT NULL,
                custom_script TEXT NOT NULL
);


CREATE TABLE tabDataSet (
                name VARCHAR NOT NULL,
                description VARCHAR,
                creation_date DATETIME NOT NULL,
                upload_date DATETIME NOT NULL,
                author VARCHAR NOT NULL
);


CREATE TABLE tabDataFormat (
                id_data_format INTEGER NOT NULL,
                name VARCHAR NOT NULL,
                PRIMARY KEY (id_data_format)
);


CREATE TABLE tabSensors (
                id_sensor INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_sensor_type INTEGER NOT NULL,
                name VARCHAR NOT NULL,
                hw_name VARCHAR NOT NULL,
                location VARCHAR NOT NULL,
                sampling_rate FLOAT NOT NULL,
                data_rate INTEGER NOT NULL,
		FOREIGN KEY (id_sensor_type) REFERENCES tabSensorTypes (id_sensor_type) ON DELETE CASCADE ON UPDATE NO ACTION
);


CREATE TABLE tabChannels (
                id_channel INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_sensor INTEGER NOT NULL,
                id_unit INTEGER NOT NULL,
                id_data_format BIGINTEGER NOT NULL,
                label VARCHAR NOT NULL,
		FOREIGN KEY (id_unit) REFERENCES tabUnits (id_unit) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_data_format) REFERENCES tabDataFormat (id_data_format) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_sensor) REFERENCES tabSensors (id_sensor) ON DELETE CASCADE ON UPDATE NO ACTION
);


CREATE TABLE tabProcessedData (
                id_processed_data INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_subrecord INTEGER NOT NULL,
                id_recordset INTEGER NOT NULL,
                id_channel INTEGER,
                id_data_processor INTEGER NOT NULL,
                name VARCHAR NOT NULL,
                data LONGBLOB NOT NULL,
                data_timestamp DATETIME NOT NULL,
		FOREIGN KEY (id_recordset) REFERENCES tabRecordsets (id_recordset) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_subrecord) REFERENCES tabSubrecords (id_subrecord) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_data_processor) REFERENCES tabDataProcessors (id_data_processor) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_channel) REFERENCES tabChannels (id_channel) ON DELETE CASCADE ON UPDATE NO ACTION
);


CREATE TABLE tabNotebook (
                id_note INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_sensor INTEGER NOT NULL,
                id_processed_data INTEGER NOT NULL,
                id_subrecord INTEGER NOT NULL,
                id_data_processor INTEGER NOT NULL,
                id_recordset INTEGER NOT NULL,
                id_participant INTEGER NOT NULL,
                id_group INTEGER NOT NULL,
                note VARCHAR NOT NULL,
		FOREIGN KEY (id_group) REFERENCES tabGroups (id_group) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_participant) REFERENCES tabParticipants (id_participant) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_recordset) REFERENCES tabRecordsets (id_recordset) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_subrecord) REFERENCES tabSubrecords (id_subrecord) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_data_processor) REFERENCES tabDataProcessors (id_data_processor) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_sensor) REFERENCES tabSensors (id_sensor) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_processed_data) REFERENCES tabProcessedData (id_processed_data) ON DELETE CASCADE ON UPDATE NO ACTION
);


CREATE TABLE tabCalibration (
                id_calibration INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_sensor INTEGER NOT NULL,
                data LONGBLOB NOT NULL,
		FOREIGN KEY (id_sensor) REFERENCES tabSensors (id_sensor) ON DELETE CASCADE ON UPDATE NO ACTION
);


CREATE TABLE tabSensorsData (
                id_sensor_data INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_recordset INTEGER NOT NULL,
                id_sensor INTEGER NOT NULL,
                id_channel INTEGER NOT NULL,
                data_timestamp DATETIME NOT NULL,
                data LONGBLOB NOT NULL,
		FOREIGN KEY (id_recordset) REFERENCES tabRecordsets (id_recordset) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_sensor) REFERENCES tabSensors (id_sensor) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_channel) REFERENCES tabChannels (id_channel) ON DELETE CASCADE ON UPDATE NO ACTION
);


CREATE TABLE tabInfos (
                file_version DOUBLE PRECISIONS NOT NULL
);
'''


class DBManager:
    def __init__(self, filename, overwrite=False):
        self.filename = filename
        self.db = self.open_database(filename, overwrite)

    def open_database(self, filename, overwrite=False):

        # Delete the old table if overwrite is True
        if os.path.isfile(filename):
            if overwrite is True:
                print('Removing old database : ', filename)
                os.remove(filename)
            else:
                print('DB already exist: ', filename)
                return sqlite3.connect(filename)

        print('Creating database : ', filename)

        conn = sqlite3.connect(filename)

        # Create the tables
        try:
            # TODO - store table sql table creation script into a local file?
            # file_path = os.path.dirname(__file__)
            # stream = open(file_path + '/../../../openimu_fileformat/OpenIMU_FileFormat.sql', 'r')
            # qry = stream.read()
            # stream.close()
            qry = sql_init_script
            sqlite3.complete_statement(qry)
            conn = sqlite3.connect(filename)
            cursor = conn.cursor()
            cursor.executescript(qry)
            conn.commit()
        except Exception as e:
            message = filename + ': ' + str(e)
            print('Error creating database tables: ', message)
            cursor.close()
            raise

        return conn

    def commit(self):
        self.db.commit()

    def init_database(self, name='No name', description='No description', creation_date=time.time(),
                      upload_date=time.time(), author='Anonymous'):
        """
        Init the database with some basic information.

        :param name:
        :param description:
        :param creation_date:
        :param upload_date:
        :param author:
        :return:
        """
        try:

            # tabInfos -> file_version (float)
            self.db.execute("INSERT INTO tabInfos (file_version) VALUES (1.0)")

            # tabDataSet -> name, desc, creation_date, upload_date, author
            self.db.execute("INSERT INTO tabDataSet (name, description, creation_date, upload_date, author) "
                            "VALUES (?,?,?,?,?)", (name, description, creation_date, upload_date, author))

            # Fill default values
            DataFormat.populate_database(self.db)
            SensorType.populate_database(self.db)
            Units.populate_database(self.db)

            self.db.commit()

        except Exception as e:
            print('Init database error: ', str(e))
            raise

    def add_group(self, name, description):
        """

        :param name:
        :param description:
        :return: Group
        """

        try:
            # print('Adding group:', name, 'description:',description)
            cursor = self.db.execute("INSERT INTO tabGroups (name, description) VALUES (?,?)", (name, description))
            group = Group((cursor.lastrowid, name, description))
            self.db.commit()
            return group
        except Exception as e:
            message = 'Error adding group' + ': ' + str(e)
            print('Error: ', message)
            raise

    def get_group(self, id_group):
        try:
            # print('Adding group:', name, 'description:',description)
            cursor = self.db.execute("SELECT * FROM tabGroups WHERE id_group=?",(id_group,))
            return Group(cursor.fetchone())

        except Exception as e:
            message = 'Error getting group' + ': ' + str(e)
            print('Error: ', message)
            raise

    def get_all_groups(self):
        try:
            # print('Adding group:', name, 'description:',description)
            cursor = self.db.execute("SELECT * FROM tabGroups")

            result = []

            # This will load groups from tuples
            for row in cursor.fetchall():
                result.append(Group(row))

            return result

        except Exception as e:
            message = 'Error getting groups' + ': ' + str(e)
            print('Error: ', message)
            raise

    def add_participant(self, group: Group, name: object, description: object) -> object:
        try:
            cursor = self.db.execute("INSERT INTO tabParticipants (id_group, name, description) VALUES (?,?,?)",
                                     (group.id_group, name, description))

            # Create object
            participant = Participant(id_participant=cursor.lastrowid, group=group, name=name, description=description)

            self.db.commit()

            return participant
        except Exception as e:
            message = 'Error adding Participant' + ': ' + str(e)
            print('Error: ', message)
            raise

    def get_participant(self, id_participant):
        try:
            cursor = self.db.execute("SELECT * FROM tabParticipants WHERE id_participant=?", (id_participant,))

            (_id_participant, _id_group, _name, _description) = cursor.fetchone()
            # Get Group
            group = self.get_group(_id_group)
            # Return participant
            return Participant(id_participant=id_participant, group=group, name=_name, description=_description)

        except Exception as e:
            message = 'Error getting Participant' + ': ' + str(e)
            print('Error: ', message)
            raise

    def add_sensor(self, _id_sensor_type, _name, _hw_name, _location, _sampling_rate, _data_rate):
        try:
            cursor = self.db.execute("INSERT INTO tabSensors (id_sensor_type, name, hw_name, "
                                     "location, sampling_rate, data_rate) VALUES (?,?,?,?,?,?)",
                                     (_id_sensor_type, _name, _hw_name, _location, _sampling_rate, _data_rate))

            # Create object
            sensor = Sensor(id_sensor=cursor.lastrowid,
                            id_sensor_type=_id_sensor_type,
                            name=_name,
                            hw_name=_hw_name,
                            location=_location,
                            sampling_rate=_sampling_rate,
                            data_rate=_data_rate)

            self.db.commit()

            return sensor
        except Exception as e:
            message = 'Error adding sensor' + ': ' + str(e)
            print('Error: ', message)
            raise

    def get_sensor(self, id_sensor):
        try:
            cursor = self.db.execute("SELECT * FROM tabSensors WHERE id_sensor=?", (id_sensor,))
            return Sensor(cursor.fetchone())

        except Exception as e:
            message = 'Error getting sensor' + ': ' + str(e)
            print('Error: ', message)
            raise

    def add_recordset(self, participant, name, start_timestamp, end_timestamp):
        try:
            cursor = self.db.execute("INSERT INTO tabRecordsets (id_participant, name, start_timestamp, "
                                     "end_timestamp) VALUES (?,?,?,?)",
                                     (participant.id_participant, name, start_timestamp, end_timestamp))

            # Create object
            record = Recordset(id_recordset=cursor.lastrowid,
                               participant=participant,
                               name=name,
                               start_timestamp=start_timestamp,
                               end_timestamp=end_timestamp)

            self.db.commit()

            return record
        except Exception as e:
            message = 'Error adding recordset' + ': ' + str(e)
            print('Error: ', message)
            raise

    def get_recordset(self, id_recordset):
        try:
            cursor = self.db.execute("SELECT * FROM tabRecordsets WHERE id_recordset=?", (id_recordset,))

            (_id_record_set, _id_participant, _name, _start_timestamp, _end_timestamp) = cursor.fetchone()

            # Get Participant
            _participant = self.get_participant(_id_participant)

            # Create Recordset
            _recordset = Recordset(id_recordset=_id_record_set, participant=_participant, name=_name,
                                   start_timestamp=_start_timestamp, end_timestamp=_end_timestamp)

            return _recordset
        except Exception as e:
            message = 'Error getting recordset' + ': ' + str(e)
            print('Error: ', message)
            raise

    def add_channel(self, sensor, id_unit, id_data_format, label):
        try:
            cursor = self.db.execute("INSERT INTO tabChannels (id_sensor, id_unit, "
                                     "id_data_format, label) VALUES (?,?,?,?)",
                                     (sensor.id_sensor, id_unit, id_data_format, label))

            # Create object
            channel = Channel(id_channel=cursor.lastrowid, sensor=sensor, id_unit=id_unit,
                              id_data_format=id_data_format, label=label)

            self.db.commit()

            return channel
        except Exception as e:
            message = 'Error adding channel' + ': ' + str(e)
            print('Error: ', message)
            raise

    def get_channel(self, id_channel):
        try:
            cursor = self.db.execute("SELECT * FROM tabChannels WHERE id_channel=?", (id_channel,))

            (_id_channel, _id_sensor, _id_unit, _id_data_format, _label) = cursor.fetchone()

            # Get Sensor
            _sensor = self.get_sensor(_id_sensor)

            # Create channel
            _channel = Channel(id_channel=_id_channel, sensor=_sensor, id_unit=_id_unit, id_data_format=_id_data_format,
                               label=_label)

            return _channel
        except Exception as e:
            message = 'Error getting recordset' + ': ' + str(e)
            print('Error: ', message)
            raise

    def add_sensor_data(self, recordset, sensor, channel, timestamp, data):
        try:

            # print('Trying insert of type:', type(data))

            cursor = self.db.execute("INSERT INTO tabSensorsData (id_recordset, id_sensor, "
                                     "id_channel, data_timestamp, data) VALUES (?,?,?,?,?)",
                                     (recordset.id_recordset, sensor.id_sensor, channel.id_channel, timestamp,
                                      data.tobytes()))

            # Create object
            sensordata = SensorData(id_sensor_data=cursor.lastrowid, recordset=recordset, sensor=sensor,
                                    channel=channel, data_timestamp=timestamp, data=data)

            # Do not commit, too slow!
            # self.db.commit()

            return sensordata
        except Exception as e:
            message = 'Error adding sensordata' + ': ' + str(e)
            print('Error: ', message)
            raise

    def get_sensor_data(self, id_sensor_data):
        try:
            cursor = self.db.execute("SELECT * FROM tabSensorsData WHERE id_sensor_data=?", (id_sensor_data,))

            (_id_sensor_data, _id_recordset, _id_sensor, _id_channel, _data_timestamp, _data) = cursor.fetchone()

            print('get_sensor_data data type', type(_data))

            # Get Recordset
            _recordset = self.get_recordset(_id_recordset)

            # Get Sensor
            _sensor = self.get_sensor(_id_sensor)

            # Get Channel
            _channel = self.get_channel(_id_channel)

            # Do something to convert bytes in the right format
            _data = DataFormat.from_bytes(_data, _channel.id_data_format)

            # Create SensorData
            _sensordata = SensorData(id_sensor_data=_id_sensor_data, recordset=_recordset, sensor=_sensor,
                                     channel=_channel, data_timestamp=_data_timestamp, data=_data)

            return _sensordata
        except Exception as e:
            message = 'Error getting sensordata' + ': ' + str(e)
            print('Error: ', message)
            raise