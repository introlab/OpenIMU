"""

    Unit testing for OpenIMUImporter
    @authors Dominic Létourneau
    @date 22/05/2018

"""


import unittest
from libopenimu.importers.OpenIMUImporter import OpenIMUImporter
from libopenimu.models.Participant import Participant
from libopenimu.db.DBManager import DBManager


class OpenIMUImporterTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load(self):
        manager = DBManager('openimu.oi', overwrite=True, newfile=True)
        participant = Participant(name='My Participant', description='Participant Description')
        manager.update_participant(participant)

        # Import to database
        importer = OpenIMUImporter(manager, participant)
        results = importer.load('../../../resources/samples/openimu_sample.oimu')

        # results = importer.load('/Volumes/MINILOGGER/log_20190101_000034/record_20190101_000034.mdat')
        # print('results', results)
        importer.import_to_database(results)

        self.assertTrue(True)
