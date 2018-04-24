"""

    Unit testing for freedson_adult_1998
    @authors Dominic Létourneau
    @date 24/04/2018

"""


import unittest
import numpy as np
import libopenimu.algorithms.freedson_adult_1998 as freedson1998


class Freedson1998Test(unittest.TestCase):

    def setUp(self):
        pass

    def thread_finished_callback(self):
        pass

    def test_cutpoints(self):
        self.assertEqual(freedson1998.CutPoints.classify(0), freedson1998.CutPoints.SEDENTARY)
        self.assertEqual(freedson1998.CutPoints.classify(10), freedson1998.CutPoints.SEDENTARY)
        self.assertEqual(freedson1998.CutPoints.classify(99), freedson1998.CutPoints.SEDENTARY)

        self.assertEqual(freedson1998.CutPoints.classify(100), freedson1998.CutPoints.LIGHT)
        self.assertEqual(freedson1998.CutPoints.classify(500), freedson1998.CutPoints.LIGHT)
        self.assertEqual(freedson1998.CutPoints.classify(1951), freedson1998.CutPoints.LIGHT)

        self.assertEqual(freedson1998.CutPoints.classify(1952), freedson1998.CutPoints.MODERATE)
        self.assertEqual(freedson1998.CutPoints.classify(3000), freedson1998.CutPoints.MODERATE)
        self.assertEqual(freedson1998.CutPoints.classify(5724), freedson1998.CutPoints.MODERATE)

        self.assertEqual(freedson1998.CutPoints.classify(5726), freedson1998.CutPoints.VIGOROUS)
        self.assertEqual(freedson1998.CutPoints.classify(8000), freedson1998.CutPoints.VIGOROUS)
        self.assertEqual(freedson1998.CutPoints.classify(9498), freedson1998.CutPoints.VIGOROUS)

        self.assertEqual(freedson1998.CutPoints.classify(9499), freedson1998.CutPoints.VERY_VIGOROUS)
        self.assertEqual(freedson1998.CutPoints.classify(100000), freedson1998.CutPoints.VERY_VIGOROUS)
        self.assertEqual(freedson1998.CutPoints.classify(100000000000), freedson1998.CutPoints.VERY_VIGOROUS)