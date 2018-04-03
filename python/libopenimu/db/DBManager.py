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
            file_path = os.path.dirname(__file__)
            stream = open(file_path + '/../../../openimu_fileformat/OpenIMU_FileFormat.sql', 'r')
            qry = stream.read()
            stream.close()
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

    def add_participant(self, group, name, description):
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
