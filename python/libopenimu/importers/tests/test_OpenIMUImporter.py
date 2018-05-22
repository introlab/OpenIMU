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
        manager = DBManager('test.db', overwrite=True)
        participant = Participant(name='My Participant', description='Participant Description')
        manager.update_participant(participant)

        # Import to database
        importer = OpenIMUImporter(manager, participant)
        results = importer.load('../../../resources/samples/openimu_sample.oimu')
        # print('results', results)
        importer.import_to_database(results)
