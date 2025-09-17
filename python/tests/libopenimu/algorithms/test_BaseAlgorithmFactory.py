"""

Unit testing for freedson_adult_1998
@authors Dominic Létourneau
@date 24/04/2018

"""

import unittest
import libopenimu.algorithms.BaseAlgorithm as base


class TestBaseAlgorithmFactory(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_registered_factories(self):
        print("Printing factories: ")
        base.BaseAlgorithmFactory.print_factories()
        self.assertGreater(base.BaseAlgorithmFactory.factory_count(), 0)

    def test_get_factory_named(self):
        self.assertEqual(base.BaseAlgorithmFactory.get_factory_named("Unknown"), None)
        self.assertNotEqual(
            base.BaseAlgorithmFactory.get_factory_named("Freedson Adult 1998"), None
        )
        self.assertNotEqual(
            base.BaseAlgorithmFactory.get_factory_named("Evenson 2008"), None
        )
