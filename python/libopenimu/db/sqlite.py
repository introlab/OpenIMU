'''
 Will contain sqlite driver
 @authors Simon Brière, Dominic Létourneau
 @date 19/03/2018
'''
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
        conn.execute("INSERT INTO tabDataSet (name, description, creation_date, upload_date, author) "
                     "VALUES (?,?,?,?,?)", (name, description, creation_date, 0, author))

        DataFormat.populate_database(conn)

        SensorType.populate_database(conn)

        Units.populate_database(conn)

        conn.commit()

    except Exception as e:
        message = filename + ': ' + str(e)
        print('Insert Error: ', message)

    return conn


def add_group(dbconn, name, description):
    try:
        # print('Adding group:', name, 'description:',description)
        cursor = dbconn.execute("INSERT INTO tabGroups (name, description) VALUES (?,?)", (name,description))
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
        # print('Adding participant:', name, id_group, description)
        cursor = dbconn.execute("INSERT INTO tabParticipants (id_group, name, description) VALUES (?,?,?)",
                                (id_group, name, description))
        return cursor.lastrowid


    except Exception as e:
        message = 'Error adding group' + ': ' + str(e)
        print('Error: ', message)
        raise


def add_sensor(dbconn, sensor_type, name, hw_name, location, sampling_rate, data_rate):
    """
    
    :param dbconn: 
    :param sensor_type: 
    :param name: 
    :param hw_name: 
    :param location: 
    :param sampling_rate: 
    :param data_rate: 
    :return: 
    """
    try:
        # print('Adding sensor:', sensor_type, name, hw_name, location, sampling_rate, data_rate)
        cursor = dbconn.execute("INSERT INTO tabSensors (id_sensor_type, name, hw_name, location, sampling_rate, data_rate) "
                                "VALUES (?,?,?,?,?,?)",
                                (sensor_type, name, hw_name, location, sampling_rate, data_rate))

        return cursor.lastrowid

    except Exception as e:
        message = 'Error adding sensor' + ': ' + str(e)
        print('Error: ', message)
        raise


def add_channel(dbconn, id_sensor, id_unit, id_data_format, label):
    """

    :param dbconn:
    :param id_sensor:
    :param id_unit:
    :param id_data_format:
    :param label:
    :return:
    """
    try:
        # print('Adding channel', id_sensor, id_unit, id_data_format, label)
        cursor = dbconn.execute("INSERT INTO tabChannels (id_sensor, id_unit, id_data_format, label) "
                                "VALUES (?,?,?,?)",
                                (id_sensor, id_unit, id_data_format, label))
        return cursor.lastrowid

    except Exception as e:
        message = 'Error adding channel' + ': ' + str(e)
        print('Error: ', message)
        raise


def add_recordset(dbconn, id_participant, name, start_timestamp=0, end_timestamp=0):
    """

    :param dbconn:
    :param id_participant:
    :param name:
    :param start_timestamp:
    :param end_timestamp:
    :return:
    """
    try:
        # print('Adding recordset', id_participant, name, start_timestamp, end_timestamp)
        cursor = dbconn.execute("INSERT INTO tabRecordSets (id_participant, name, start_timestamp, end_timestamp) "
                                "VALUES (?,?,?,?)",
                                (id_participant, name, start_timestamp, end_timestamp))
        return cursor.lastrowid

    except Exception as e:
        message = 'Error adding recordset' + ': ' + str(e)
        print('Error: ', message)
        raise


def add_sensor_data(dbconn, id_recordset, id_sensor, id_channel, data_timestamp, data):
    """

    :param dbconn:
    :param id_recordset:
    :param id_sensor:
    :param id_channel:
    :param data_timestamp:
    :param data:
    :return:
    """
    try:
        # print('Adding sensor data', id_recordset, id_sensor, id_channel, data_timestamp, len(data))
        cursor = dbconn.execute("INSERT INTO tabSensorsData (id_recordset, id_sensor, id_channel, data_timestamp, data) "
                                "VALUES (?,?,?,?,?)",
                                (id_recordset, id_sensor, id_channel, data_timestamp, data))
        return cursor.lastrowid

    except Exception as e:
        message = 'Error adding sensor data' + ': ' + str(e)
        print('Error: ', message)
        raise

@timing
def read_sensor_data(dbconn, id_recordset, id_sensor, id_channel):
    """

    :param dbconn:
    :param id_recordset:
    :param id_sensor:
    :return:
    """
    try:
        print('read_sensor_data',id_recordset, id_sensor, id_channel)

        # Get raw data
        cursor = dbconn.execute("SELECT data_timestamp, data FROM tabSensorsData WHERE id_recordset=? AND id_sensor=? AND id_channel=? "
                                "ORDER BY data_timestamp", (id_recordset, id_sensor, id_channel))

        sensor_data = cursor.fetchall()

        # Get Sensor info (timestamp + data)
        cursor = dbconn.execute("SELECT * FROM tabSensors WHERE id_sensor=?",(id_sensor,))

        # All information on sensor
        [sensor_id, sensor_type, name, hw_name, location, sampling_rate, data_rate] = cursor.fetchone()

        # All information on channel
        cursor = dbconn.execute("SELECT id_unit, id_data_format,label FROM tabChannels WHERE id_channel=?",(id_channel,))
        [unit, data_format, label] = cursor.fetchone()
        print("data_format", DataFormat.name(data_format),"unit",Units.name(unit), "label", label)

        result = {}
        all_data = []

        # Read all data in the right format
        for row in sensor_data:
            if data_format == DataFormat.FLOAT32:
                nb_bytes = len(row[1])
                nb_samples = int(nb_bytes / 4)
                # print('should read nb_samples:',nb_samples)
                samples = struct.unpack_from('<' + str(nb_samples) + 'f', row[1])
                # print('samples:', samples)
                all_data.append((row[0],samples))


        # Fill the result struct
        result['data'] = all_data
        result['id_recordset']  = id_recordset
        result['id_sensor'] = id_sensor
        result['id_channel'] = id_channel
        result['id_unit'] = unit
        result['id_data_format'] = data_format
        result['label'] = label
        result['sampling_rate'] = sampling_rate
        result['data_rate'] = data_rate

        return result

    except Exception as e:
        message = 'Error reading sensor data' + ': ' + str(e)
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
    sensor1 = add_sensor(db, sensor_type=SensorType.ACCELEROMETER,
                         name='My Accelerometers',
                         hw_name = 'OpenIMU-HW',
                         location = 'wrist',
                         sampling_rate = 100, data_rate = 1)

    # Add 3 axis accelerometer
    channel_acc_x = add_channel(db, id_sensor=sensor1, id_unit=Units.GRAVITY_G,id_data_format=DataFormat.FLOAT32,label='Accelerometer_X')
    channel_acc_y = add_channel(db, id_sensor=sensor1, id_unit=Units.GRAVITY_G,id_data_format=DataFormat.FLOAT32,label='Accelerometer_Y')
    channel_acc_z = add_channel(db, id_sensor=sensor1, id_unit=Units.GRAVITY_G,id_data_format=DataFormat.FLOAT32,label='Accelerometer_Z')

    # Add record (no timestamp)
    record = add_recordset(db, id_participant=part1, name='Un enregistrement')

    # Add fake data for 120 seconds
    for timestamp in range(0, 120):
        # Generate one second of data @ 100Hz
        npoints = 100
        xtime = np.linspace(0., 2 * math.pi, npoints, dtype=np.float32)
        xdata = np.sin(xtime)
        ydata = np.sin(2 * xtime)
        zdata = np.sin(4 * xtime)

        add_sensor_data(db, id_recordset=record,id_sensor=sensor1,id_channel=channel_acc_x,data_timestamp=timestamp,data=xdata)
        add_sensor_data(db, id_recordset=record, id_sensor=sensor1, id_channel=channel_acc_y, data_timestamp=timestamp,
                        data=ydata)
        add_sensor_data(db, id_recordset=record, id_sensor=sensor1, id_channel=channel_acc_z, data_timestamp=timestamp,
                        data=zdata)

    db.commit()
    # Reading back data
    data = read_sensor_data(db, record, sensor1, channel_acc_x)
    # print('read data:',data)

    db.close()