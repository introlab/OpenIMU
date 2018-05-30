"""

    test_AppleWatchImporter
    @authors Dominic Létourneau, Simon Brière
    @date 30/05/2018

"""


import unittest
import numpy as np
import datetime
import libopenimu.importers.wimu as wimu
from libopenimu.importers.AppleWatchImporter import AppleWatchImporter
from libopenimu.models.Participant import Participant
from libopenimu.db.DBManager import DBManager

class AppleWatchImporterTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

