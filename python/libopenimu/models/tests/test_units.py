"""

    Unit testing for units
    @authors Simon Brière, Dominic Létourneau
    @date 03/04/2018

"""


import unittest
from libopenimu.models.units import Units


class UnitsTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_as_dict(self):
        my_dict = Units.as_dict()
        self.assertEqual(len(my_dict), 13)

    def test_validation(self):
        self.assertTrue(Units.is_valid(Units.METERS))
        self.assertTrue(Units.is_valid(Units.GRAVITY_G))
        self.assertTrue(Units.is_valid(Units.METERS_PER_SEC))
        self.assertTrue(Units.is_valid(Units.RAD_PER_SEC))
        self.assertTrue(Units.is_valid(Units.DEG_PER_SEC))
        self.assertTrue(Units.is_valid(Units.VOLTS))
        self.assertTrue(Units.is_valid(Units.LUX))
        self.assertTrue(Units.is_valid(Units.NONE))
        self.assertTrue(Units.is_valid(Units.AMPERES))
        self.assertTrue(Units.is_valid(Units.KPA))
        self.assertTrue(Units.is_valid(Units.UTESLA))

