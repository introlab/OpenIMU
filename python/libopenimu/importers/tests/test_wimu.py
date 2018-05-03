"""

    Unit testing for wimu
    @authors Dominic Létourneau
    @date 03/05/2018

"""


import unittest
import libopenimu.importers.wimu as wimu
import numpy as np


class WIMUTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_wimu(self):
        results = wimu.wimu_importer('../../../resources/samples/WIMU_ACC_GPS_GYRO_PreProcess.zip')
        self.assertGreater(len(results), 0)
