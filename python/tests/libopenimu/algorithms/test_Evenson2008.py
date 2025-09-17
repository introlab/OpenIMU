import unittest
import libopenimu.algorithms.Evenson2008 as evenson2008
from libopenimu.algorithms.BaseAlgorithm import BaseAlgorithmFactory


class TestEvenson2008(unittest.TestCase):
    """
    Unit testing for Evenson2008
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_factory_registered(self):
        """
        Test if the factory is registered
        """
        factory = BaseAlgorithmFactory.get_factory_named("Evenson 2008")
        self.assertIsNotNone(factory)
        self.assertEqual(factory.name(), "Evenson 2008")
        self.assertEqual(factory.unique_id(), 2)
        factory_params = factory.params()
        self.assertGreater(len(factory_params), 0)
        self.assertIn("sedentary_cutoff", factory_params)
        self.assertIn("light_cutoff", factory_params)
        self.assertIn("moderate_cutoff", factory_params)
        info = factory.info()
        self.assertGreater(len(info), 0)
