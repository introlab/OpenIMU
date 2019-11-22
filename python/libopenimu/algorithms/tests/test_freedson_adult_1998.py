"""

    Unit testing for freedson_adult_1998
    @authors Dominic Létourneau
    @date 24/04/2018

"""


import unittest
# import libopenimu.algorithms.freedson_adult_1998 as freedson1998
from libopenimu.algorithms.freedson_adult_1998 import CutPoints


class Freedson1998Test(unittest.TestCase):

    def setUp(self):
        pass

    def thread_finished_callback(self):
        pass

    def test_cutpoints(self):
        cutpoints = CutPoints()
        self.assertEqual(cutpoints.classify(value=0), cutpoints.SEDENTARY)
        self.assertEqual(cutpoints.classify(value=10), cutpoints.SEDENTARY)
        self.assertEqual(cutpoints.classify(value=99), cutpoints.SEDENTARY)

        self.assertEqual(cutpoints.classify(value=100), cutpoints.LIGHT)
        self.assertEqual(cutpoints.classify(value=500), cutpoints.LIGHT)
        self.assertEqual(cutpoints.classify(value=1951), cutpoints.LIGHT)

        self.assertEqual(cutpoints.classify(value=1952), cutpoints.MODERATE)
        self.assertEqual(cutpoints.classify(value=3000), cutpoints.MODERATE)
        self.assertEqual(cutpoints.classify(value=5724), cutpoints.MODERATE)

        self.assertEqual(cutpoints.classify(value=5726), cutpoints.VIGOROUS)
        self.assertEqual(cutpoints.classify(value=8000), cutpoints.VIGOROUS)
        self.assertEqual(cutpoints.classify(value=9498), cutpoints.VIGOROUS)

        self.assertEqual(cutpoints.classify(value=9499), cutpoints.VERY_VIGOROUS)
        self.assertEqual(cutpoints.classify(value=100000), cutpoints.VERY_VIGOROUS)
        self.assertEqual(cutpoints.classify(value=100000000000), cutpoints.VERY_VIGOROUS)
