"""

    Unit testing for OpenIMUImporter
    @authors Dominic Létourneau
    @date 22/05/2018

"""


import unittest
import numpy as np
import datetime
import libopenimu.importers.wimu as wimu
from libopenimu.importers.OpenIMUImporter import OpenIMUImporter
from libopenimu.models.Participant import Participant
from libopenimu.db.DBManager import DBManager


class OpenIMUImporterTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load(self):
        pass