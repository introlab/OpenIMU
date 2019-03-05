"""

    test_AppleWatchImporter
    @authors Dominic Létourneau, Simon Brière
    @date 30/05/2018

"""
import unittest
from libopenimu.importers.AppleWatchImporter import AppleWatchImporter
from libopenimu.models.Participant import Participant
from libopenimu.db.DBManager import DBManager


class AppleWatchImporterTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load_file(self):
        pass

    @staticmethod
    def test_load_zip_file():
        # Testing

        manager = DBManager('applewatch.oi', overwrite=True)
        participant = Participant(name='My Participant', description='Participant Description')
        manager.update_participant(participant)
        importer = AppleWatchImporter(manager, participant)

        results = importer.load('/Users/dominic/WA/OpenIMU.git/python/applewatch_data.zip')
        # print('results', results)
        importer.import_to_database(results)

    @staticmethod
    def test_load_data_file():
        # Testing

        manager = DBManager('applewatch.oi', overwrite=True)
        participant = Participant(name='My Participant', description='Participant Description')
        manager.update_participant(participant)
        importer = AppleWatchImporter(manager, participant)

        results = importer.load('/Users/dominic/Documents/working_area/OpenIMU.git/python/watch_ProcessedMotion.data')
        # print('results', results)
        importer.import_to_database(results)
