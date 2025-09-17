import unittest
import libopenimu.algorithms.FreedsonAdult1998 as freedson1998
from libopenimu.algorithms.BaseAlgorithm import BaseAlgorithmFactory


class TestFreedsonAdult1998(unittest.TestCase):
    """
    Unit testing for FreedsonAdult1998
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_factory_registered(self):
        """
        Test if the factory is registered
        """
        factory = BaseAlgorithmFactory.get_factory_named("Freedson Adult 1998")
        self.assertIsNotNone(factory)
        self.assertEqual(factory.name(), "Freedson Adult 1998")
        self.assertEqual(factory.unique_id(), 1)
        factory_params = factory.params()
        self.assertGreater(len(factory_params), 0)
        self.assertIn("sedentary_cutoff", factory_params)
        self.assertIn("light_cutoff", factory_params)
        self.assertIn("moderate_cutoff", factory_params)
        self.assertIn("vigorous_cutoff", factory_params)
        info = factory.info()
        self.assertGreater(len(info), 0)
