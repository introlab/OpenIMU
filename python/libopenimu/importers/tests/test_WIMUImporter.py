"""

    Unit testing for WIMUImporter
    @authors Dominic Létourneau
    @date 27/04/2018

"""


import unittest
import libopenimu.importers.wimu as wimu
from libopenimu.importers.WIMUImporter import WIMUImporter
from libopenimu.models.Participant import Participant
from libopenimu.db.DBManager import DBManager


class WIMUImporterTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_acc_conversion(self):
        self.assertAlmostEqual(wimu.AccOptions.conversion_to_g(0, 32767, 2), 2.0)
        self.assertAlmostEqual(wimu.AccOptions.conversion_to_g(1, 32767, 2), 4.0)
        self.assertAlmostEqual(wimu.AccOptions.conversion_to_g(2, 32767, 2), 8.0)
        self.assertAlmostEqual(wimu.AccOptions.conversion_to_g(3, 32767, 2), 16.0)
        self.assertAlmostEqual(wimu.AccOptions.conversion_to_g(0, -32767, 2), -2.0)
        self.assertAlmostEqual(wimu.AccOptions.conversion_to_g(1, -32767, 2), -4.0)
        self.assertAlmostEqual(wimu.AccOptions.conversion_to_g(2, -32767, 2), -8.0)
        self.assertAlmostEqual(wimu.AccOptions.conversion_to_g(3, -32767, 2), -16.0)
        self.assertEqual(wimu.AccOptions.conversion_to_g(4, 32767, 2), None)

    def test_gyro_conversion(self):
        self.assertAlmostEqual(wimu.GyroOptions.conversion_to_deg_per_sec(0, 32767, 2), 250.0)
        self.assertAlmostEqual(wimu.GyroOptions.conversion_to_deg_per_sec(1, 32767, 2), 500.0)
        self.assertAlmostEqual(wimu.GyroOptions.conversion_to_deg_per_sec(2, 32767, 2), 1000.0)
        self.assertAlmostEqual(wimu.GyroOptions.conversion_to_deg_per_sec(3, 32767, 2), 2000.0)
        self.assertAlmostEqual(wimu.GyroOptions.conversion_to_deg_per_sec(0, -32767, 2), -250.0)
        self.assertAlmostEqual(wimu.GyroOptions.conversion_to_deg_per_sec(1, -32767, 2), -500.0)
        self.assertAlmostEqual(wimu.GyroOptions.conversion_to_deg_per_sec(2, -32767, 2), -1000.0)
        self.assertAlmostEqual(wimu.GyroOptions.conversion_to_deg_per_sec(3, -32767, 2), -2000.0)
        self.assertAlmostEqual(wimu.GyroOptions.conversion_to_deg_per_sec(5, 32767, 2), None)

    def test_loading(self):
        manager = DBManager('test.db', overwrite=True)
        participant = Participant(name='My Participant', description='Participant Description')
        manager.update_participant(participant)

        # Import to database
        importer = WIMUImporter(manager, participant)
        # results = importer.load('../../../resources/samples/WIMU_ACC_GPS_GYRO_PreProcess.zip')
        results = importer.load('../../../resources/samples/REPAR_Sujet7_Semaine_T4.zip')
        importer.import_to_database(results)

        recordsets = manager.get_all_recordsets(participant)
        print('recordsets', recordsets)
        self.assertGreater(len(recordsets), 0)
