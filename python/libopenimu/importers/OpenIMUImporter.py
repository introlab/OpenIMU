from libopenimu.importers.BaseImporter import BaseImporter
from libopenimu.models.sensor_types import SensorType
from libopenimu.models.units import Units
from libopenimu.models.Recordset import Recordset
from libopenimu.models.data_formats import DataFormat
from libopenimu.tools.timing import timing
from libopenimu.db.DBManager import DBManager
from libopenimu.models.Participant import Participant

import numpy as np
import datetime

import struct
import sys
import binascii
import datetime
import string


class OpenIMUImporter(BaseImporter):
    def __init__(self, manager: DBManager, participant: Participant):
        super().__init__(manager, participant)
        print('OpenIMU Importer')
        # No recordsets when starting
        self.recordsets = []

    def load(self, filename):
        print('OpenIMUImporter.load')
        with open(filename, "rb") as file:
            print('Loading File: ', filename)
            self.readDataFile(file)

        print('Done!')

    def import_to_database(self, result):
        print('OpenIMUImporter.import_to_database')
        pass

    def processImuChunk(self, chunk):
        data = struct.unpack("9f", chunk)
        for value in data:
            # print(value)
            pass


    def processTimestampChunk(self, chunk):
        [timestamp] = struct.unpack("i", chunk)
        print(datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'))

    def processGPSChunk(self, chunk):
        data = struct.unpack("?3f", chunk)
        fix = data[0]
        if fix:
            print("GPS : ", data[1], data[2], data[3])
        else:
            print("No gps fix")

    def processBarometerChunk(self, chunk):
        data = struct.unpack("2f", chunk)
        print("BARO: ", data[0], data[1])

    def processPowerChunk(self, chunk):
        data = struct.unpack("2f", chunk)
        print("Power  : ", data[0], data[1])

    def readDataFile(self, file):
        n = 0
        while True:
            chunk = file.read(1)
            if len(chunk) < 1:
                print("Reached end of file")
                break

            (headChar) = struct.unpack("c", chunk)
            # print('headchar ', headChar)

            if headChar[0] == b'h':
                n = n + 1
                print("New log stream")
            elif headChar[0] == b't':
                n = n + 1
                chunk = file.read(struct.calcsize("i"))
                self.processTimestampChunk(chunk)
            elif headChar[0] == b'i':
                n = n + 1
                chunk = file.read(struct.calcsize("9f"))
                self.processImuChunk(chunk)
            elif headChar[0] == b'g':
                n = n + 1
                chunk = file.read(struct.calcsize("?3f"))
                self.processGPSChunk(chunk)
            elif headChar[0] == b'p':
                n = n + 1
                chunk = file.read(struct.calcsize("2f"))
                self.processPowerChunk(chunk)
            elif headChar[0] == b'b':
                n = n + 1
                chunk = file.read(struct.calcsize("2f"))
                self.processBarometerChunk(chunk)
            else:
                print("Unrecognised chunk :", headChar[0])
                n = n + 1
                if n > 2:
                    break

