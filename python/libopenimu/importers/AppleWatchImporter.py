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


class AppleWatchImporter(BaseImporter):
    def __init__(self, manager: DBManager, participant: Participant):
        super(BaseImporter, self).__init__(manager, participant)
        pass

    def load(self, filename):
        print('AppleWatchImporter.load')
        pass

    def import_to_database(self, result):
        print('AppleWatchImporter.import_to_database')
        pass
