'''
 Will contain sqlite driver
 @authors Simon Brière, Dominic Létourneau
 @date 19/03/2018
'''
import sqlite3
import os
import time
from sensor_types import SensorType

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

        conn.commit()

    except Exception as e:
        message = filename + ': ' + str(e)
        print('Insert Error: ', message)

    return conn


def add_group(dbconn, name, description):
    try:
        print('Adding group:', name, 'description:',description)
        dbconn.execute("INSERT INTO tabGroups (name, desc) VALUES (?,?)", [name,description])
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
    add_group(db,'Enfants','Les enfants de la famille')
    add_group(db, 'Parents', 'Les parents de la famille')

    db.commit()
    db.close()