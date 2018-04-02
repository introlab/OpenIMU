"""
 DBManager
 Will contain sqlite driver and model interface
 @authors Simon Brière, Dominic Létourneau
 @date 27/03/2018
"""

import sqlite3
import os
import time
from libopenimu.db.sensor_types import SensorType
from libopenimu.db.data_formats import DataFormat
from libopenimu.db.units import Units
import numpy as np
import math
from libopenimu.tools.timing import timing
import struct

# All the models
from libopenimu.models.Group import Group


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
            qry = open('../../../openimu_fileformat/OpenIMU_FileFormat.sql', 'r').read()
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
            myGroup = Group((cursor.lastrowid, name, description))
            return myGroup
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

    @property
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

    def add_participant(self, group, name, description ):
        return


if __name__ == '__main__':
    manager = DBManager('openimu.db', overwrite=True)
    manager.init_database(name='My DataSet', description='First test')

    manager.add_group('group1','description1')
    manager.add_group('group2', 'description2')
    manager.add_group('group3', 'description3')

    print('all groups', manager.get_all_groups)
    print('get group',manager.get_group(id_group=1))