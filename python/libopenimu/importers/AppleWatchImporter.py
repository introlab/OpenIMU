"""

    AppleWatchImporter
    @authors Dominic Létourneau, Simon Brière
    @date 30/05/2018

"""

from libopenimu.importers.BaseImporter import BaseImporter
from libopenimu.models.sensor_types import SensorType
from libopenimu.models.units import Units
from libopenimu.models.Recordset import Recordset
from libopenimu.models.data_formats import DataFormat
from libopenimu.tools.timing import timing
from libopenimu.db.DBManager import DBManager
from libopenimu.models.Participant import Participant
from libopenimu.importers.wimu import GPSGeodetic

import numpy as np
import math
import datetime

import struct
import sys
import binascii
import datetime
import string
import os
import zipfile
import struct

class AppleWatchImporter(BaseImporter):

    HEADER = 0xEAEA
    BATTERY_ID = 0x01
    SENSORIA_ID = 0x02
    HEARTRATE_ID = 0x03
    MOTION_ID = 0x04
    # LOCATION_ID = 0x05
    BEACONS_ID = 0x06
    COORDINATES_ID = 0x7

    def __init__(self, manager: DBManager, participant: Participant):
        super().__init__(manager, participant)
        pass

    def load(self, filename):
        print('AppleWatchImporter.load')
        results = {}

        if 'zip' in filename:
            results = self.load_zip(filename)
        else:
            with open(filename, "rb") as file:
                print('Loading File: ', filename)
                results = self.readDataFile(file)

        print('results len', len(results))
        return results

    def load_zip(self, filename):
        results = {}
        with zipfile.ZipFile(filename) as myzip:
            print('zip opened')
            namelist = myzip.namelist()

            print('zip contains : ', namelist)

            # First find SETTINGS file
            for file in namelist:
                if '.data' in file:
                    print('Reading file: ', file)
                    my_file = myzip.open(file)
                    values = self.readDataFile(my_file, False)

                    # Add to global results
                    if values is not None:
                        for timestamp in values:
                            if not results.__contains__(timestamp):
                                results[timestamp] = values[timestamp]
                            else:
                                results[timestamp]['battery'].append(values[timestamp]['battery'])
                                results[timestamp]['sensoria'].append(values[timestamp]['sensoria'])
                                results[timestamp]['heartrate'].append(values[timestamp]['heartrate'])
                                results[timestamp]['motion'].append(values[timestamp]['motion'])
                                # results[timestamp]['location'].append(values[timestamp]['location'])
                                results[timestamp]['coordinates'].append(values[timestamp]['coordinates'])
                else:
                    pass
                    # print('Unknown file : ', file)

        return results

    def import_to_database(self, result):
        print('AppleWatchImporter.import_to_database')
        pass

    def readDataFile(self, file, debug=True):
        '''
        All binary files have a similar header
        • Two bytes for file identifier (based on Wimu format): 0xEA, 0xEA
        • File Version byte: eg. 0x01
        • 4 bytes (as UInt32) for participantID
        • Byte for sensor identification
        ◦ Battery: 1
        ◦ Sensoria: 2
        ◦ Heartrate: 3
        ◦ Motion: 4
        * Location : 5
        ◦ Beacons: 6
        ◦ Coordinates: 7
        '''

        results = {}

        [id, version, participant_id] = struct.unpack("<HBI", file.read(2 + 1 + 4))

        if id != self.HEADER:
            return None

        if debug:
            print('reading header : ', hex(id), hex(version), participant_id)

        # Read sensor ID
        [sensor_id] = struct.unpack("<B", file.read(1))

        if debug:
            print('sensor_id : ', hex(sensor_id))

        try:
            while file.readable():
                # Read timestamp
                [timestamp_ms] = struct.unpack("<Q", file.read(8))
                timestamp_sec = int(np.round(timestamp_ms / 1000))
                if debug:
                    print('TIMESTAMP (MS): ', timestamp_ms)
                    print('time: ',  datetime.datetime.fromtimestamp(timestamp_sec))

                # Initialize data structure at this timestamp if required
                if not results.__contains__(timestamp_sec):
                    # print("init timestamp = ", timestamp_ms)
                    results[timestamp_sec] = {}
                    results[timestamp_sec]['battery'] = []
                    results[timestamp_sec]['sensoria'] = []
                    results[timestamp_sec]['heartrate'] = []
                    results[timestamp_sec]['motion'] = []
                    # results[timestamp_sec]['location'] = []
                    results[timestamp_sec]['beacons'] = []
                    results[timestamp_sec]['coordinates'] = []

                if sensor_id == self.BATTERY_ID:
                    # Battery data
                    data = self.read_battery_data(file.read(2), debug)
                    results[timestamp_sec]['battery'].append(data)

                elif sensor_id == self.SENSORIA_ID:
                    # Sensoria data
                    data = self.read_sensoria_data(file.read(20), debug)
                    results[timestamp_sec]['sensoria'].append(data)

                elif sensor_id == self.HEARTRATE_ID:
                    # Heartrate data
                    data = self.read_heartrate_data(file.read(1), debug)
                    results[timestamp_sec]['heartrate'].append(data)

                elif sensor_id == self.MOTION_ID:
                    # Motion data
                    data =  self.read_motion_data(file.read(52), debug)
                    results[timestamp_sec]['motion'].append(data)

                # elif sensor_id == self.LOCATION_ID:
                #    # Location data
                #    # ????
                #    data = self.read_location_data(file.read(0), debug)
                #    results[timestamp_ms]['location'].append(data)

                elif sensor_id == self.BEACONS_ID:
                    # Beacons data
                    data = self.read_beacons_data(file.read(5), debug)
                    results[timestamp_sec]['beacons'].append(data)

                elif sensor_id == self.COORDINATES_ID:
                    # Coordinates data
                    data = self.read_coordinates_data(file.read(28), debug)
                    results[timestamp_sec]['coordinates'].append(data)

                else:
                    print("unknown sensor_id: ", hex(sensor_id))
                    return None

        except:
            pass

        return results

    def read_battery_data(self, chunk, debug=False):
        """
        • Byte integer for battery level between 0 and 100 (percent)
        ◦ 0 meaning invalid level (eg. where state is .unknown)
        • Byte for battery state
        ◦ unknown: 0
        ◦ unplugged: 1
        ◦ charging: 2
        ◦ full: 3
        :param chunk:
        :return:
        """
        assert(len(chunk) == 2)
        data = struct.unpack("BB", chunk)
        if debug:
            print('BATTERY: ', data)
        return data

    def read_sensoria_data(self, chunk, debug=False):
        """
        42 bytes of received frame (will require further processing)
        This assumes that all socks we have use the F20 streaming protocol, as defined in
        SensoriaCoreData. As of now, the app ignores all other protocol to not pollute the files. In the
        future, it would be the best to deserialize these frames directly upon importation into OpenIMU.
        As this will be more cumbersome, for now the deserialization is made directly on reception.
        • 3 Int16 for the 3 channels (pressure sensors)
        • 9 Float32 for inertial sensors
        ◦ accelerometer (x,y,z)
        ◦ gyroscope (x,y,z)
        ◦ magnetometer (x,y,z)

        """
        assert(len(chunk) == 20)

        data = struct.unpack("<20B", chunk)

        # assert(len(chunk) == 42)
        # data = struct.unpack("<3h9f", chunk)
        if debug:
            print('SENSORIA: ', data)
        return data

    def read_heartrate_data(self, chunk, debug=False):
        """
        unsigned integer as single Byte for bpm
        ** assumes that bpm cannot go above 255, hence values above are clamped to 255
        :param chunk:
        :return:
        """
        assert (len(chunk) == 1)
        data = struct.unpack("<B", chunk)
        if debug:
            print('HEARTRATE: ', data)
        return data

    def read_motion_data(self, chunk, debug=False):
        """
         13 Float32 values, hence 52 bytes, with following fields
        • acceleration (x,y,z)
        • gravity vector (x,y,z)
        • gyroscope (x,y,z)
        • attitude quaternion (w,x,y,z)
            """
        assert (len(chunk) == 52)
        data = struct.unpack("<13f", chunk)
        if debug:
            print('MOTION: ', data)
        return data

    def read_location_data(self, chunk, debug=False):
        # TODO
        return []

    def read_beacons_data(self, chunk, debug=False):
        """
        4 Bytes Char for beacon name, with XXXX defining unnamed beacon
        • signed byte integer for rssi, between -128 and 127
        :param chunk:
        :return:
        """
        assert (len(chunk) == 5)
        data = struct.unpack("<4Bb", chunk)
        if debug:
            print('BEACONS: ', data)
        return data

    def read_coordinates_data(self, chunk, debug=False):
        """
          7 Float32 values, hence 28 bytes
        • latitude
        • longitude
        • accuracy in meters for lat/long
        • altitude in meters from sea level
        • accuracy in meters for altitude
        • speed (meters per second)
        • course (degrees relative to true north)
        :return:
        """
        assert (len(chunk) == 28)
        data = struct.unpack("<7f", chunk)
        if debug:
            print('COORDINATES: ', data)
        return data







