'''
 Will contain sqlite driver
 @authors Simon Brière, Dominic Létourneau
 @date 19/03/2018
'''
import sqlite3
import os
import time
from sensor_types import SensorType
from data_formats import DataFormat

def create_database(filename, name='Unnamed', description='No description available', author='Anonymous'):
    print('creating database : ', filename)

    # Delete the old table
    if os.path.isfile(filename):
        os.remove(filename)

    conn = sqlite3.connect(filename)

    # Create the tables
    qry = open('../../../openimu_fileformat/OpenIMU_FileFormat.sql', 'r').read()
    sqlite3.complete_statement(qry)
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    try:
        cursor.executescript(qry)
    except Exception as e:
        message = filename + ': ' + str(e)
        print('Error: ', message)
        cursor.close()
        raise


    # Fill some base fields
    try:

        # tabInfos -> file_version (float)
        conn.execute("INSERT INTO tabInfos (file_version) VALUES (1.0)")

        # Get current unix time
        creation_date = time.time()

        # tabDataSet -> name, desc, creation_date, upload_date, author
        conn.execute("INSERT INTO tabDataSet (name, desc, creation_date, upload_date, author) "
                     "VALUES (?,?,?,?,?)", [name, description, creation_date, 0, author])



        DataFormat.populate_database(conn)

        conn.commit()

    except Exception as e:
        message = filename + ': ' + str(e)
        print('Insert Error: ', message)

    return conn


def add_group(dbconn, name, description):
    try:
        print('Adding group:', name, 'description:',description)
        cursor = dbconn.execute("INSERT INTO tabGroups (name, description) VALUES (?,?)", [name,description])
        return cursor.lastrowid
    except Exception as e:
        message = 'Error adding group' + ': ' + str(e)
        print('Error: ', message)
        raise


def add_participant(dbconn, name, id_group = None, description='No description available'):
    """

    :param dbconn:
    :param name:
    :param id_group:
    :param description:
    :return:
    """
    try:
        print('Adding participant:', name, id_group, description)
        if id_group is not None:
            cursor = dbconn.execute("INSERT INTO tabParticipants (id_group, name, description) VALUES (?,?,?)",
                                [id_group, name, description])
            return cursor.lastrowid
        else:
            cursor = dbconn.execute("INSERT INTO tabParticipants (name, description) VALUES (?,?)",
                                [name, description])
            return cursor.lastrowid

    except Exception as e:
        message = 'Error adding group' + ': ' + str(e)
        print('Error: ', message)
        raise





"""
Test function
"""
if __name__ == '__main__':
    print('Sensor type:', SensorType.ACCELEROMETER)
    db = create_database('openimu.db')
    group1 = add_group(db,'Enfants','Les enfants de la famille')
    group2 = add_group(db, 'Parents', 'Les parents de la famille')
    part1 = add_participant(db, name="Dominic", id_group=group1, description='Desc. Dominic')
    part2 = add_participant(db, name="Simon", description='Desc. Simon')

    db.commit()
    db.close()