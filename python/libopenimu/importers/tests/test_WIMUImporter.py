"""

    Unit testing for WIMUImporter
    @authors Dominic Létourneau
    @date 27/04/2018

"""


import unittest
import numpy as np
import datetime


class WIMUImporterTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def __init__(self, db_filename):
        super().__init__(db_filename)
        print('WIMU Importer')