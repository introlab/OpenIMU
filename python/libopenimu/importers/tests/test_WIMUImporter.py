"""

    Unit testing for WIMUImporter
    @authors Dominic Létourneau
    @date 27/04/2018

"""


import unittest
import numpy as np
import datetime
from libopenimu.importers.wimu import *


class WIMUImporterTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_acc_conversion(self):
        self.assertAlmostEqual(AccOptions.conversion_to_g(0, 32767, 2), 2.0)
        self.assertAlmostEqual(AccOptions.conversion_to_g(1, 32767, 2), 4.0)
        self.assertAlmostEqual(AccOptions.conversion_to_g(2, 32767, 2), 8.0)
        self.assertAlmostEqual(AccOptions.conversion_to_g(3, 32767, 2), 16.0)
        self.assertAlmostEqual(AccOptions.conversion_to_g(0, -32767, 2), -2.0)
        self.assertAlmostEqual(AccOptions.conversion_to_g(1, -32767, 2), -4.0)
        self.assertAlmostEqual(AccOptions.conversion_to_g(2, -32767, 2), -8.0)
        self.assertAlmostEqual(AccOptions.conversion_to_g(3, -32767, 2), -16.0)
        self.assertEqual(AccOptions.conversion_to_g(4, 32767, 2), None)

    def test_gyro_conversion(self):
        self.assertAlmostEqual(GyroOptions.conversion_to_deg_per_sec(0, 32767, 2), 250.0)
        self.assertAlmostEqual(GyroOptions.conversion_to_deg_per_sec(1, 32767, 2), 500.0)
        self.assertAlmostEqual(GyroOptions.conversion_to_deg_per_sec(2, 32767, 2), 1000.0)
        self.assertAlmostEqual(GyroOptions.conversion_to_deg_per_sec(3, 32767, 2), 2000.0)
        self.assertAlmostEqual(GyroOptions.conversion_to_deg_per_sec(0, -32767, 2), -250.0)
        self.assertAlmostEqual(GyroOptions.conversion_to_deg_per_sec(1, -32767, 2), -500.0)
        self.assertAlmostEqual(GyroOptions.conversion_to_deg_per_sec(2, -32767, 2), -1000.0)
        self.assertAlmostEqual(GyroOptions.conversion_to_deg_per_sec(3, -32767, 2), -2000.0)
        self.assertAlmostEqual(GyroOptions.conversion_to_deg_per_sec(5, 32767, 2), None)
