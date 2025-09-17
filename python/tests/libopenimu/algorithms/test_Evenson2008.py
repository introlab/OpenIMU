import unittest
import os
import libopenimu.algorithms.Evenson2008 as evenson2008
from libopenimu.algorithms.BaseAlgorithm import BaseAlgorithmFactory
from libopenimu.db.DBManager import DBManager
from libopenimu.models.Participant import Participant
from libopenimu.importers.AppleWatchImporter import AppleWatchImporter


class TestEvenson2008(unittest.TestCase):
    """
    Unit testing for Evenson2008
    """

    def setUp(self):
        self.db_manager = self._open_database()
        self.session = self.db_manager.session
        self.participant = self._create_participant(
            self.session, "Test Participant", "For unit testing"
        )
        self.assertIsNotNone(self.participant)

    def tearDown(self):
        self.session.close()

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

    def test_data_importation(self):
        """
        Test if sample AppleWatch data can be imported
        """
        success = self._load_sample_applewatch_data(self.participant)
        self.assertTrue(success)

    def test_algorithm_execution(self):
        """
        Test if the FreedsonAdult1998 algorithm can be executed on sample data
        """
        # Load sample data first
        success = self._load_sample_applewatch_data(self.participant)
        self.assertTrue(success)

        # Get all recordsets for this participant
        recordsets = self.db_manager.get_all_recordsets(self.participant)
        self.assertIsNotNone(recordsets)
        self.assertGreater(len(recordsets), 0)

        # Get the factory
        factory = BaseAlgorithmFactory.get_factory_named("Evenson 2008")
        self.assertIsNotNone(factory)

        params = {
            "sedentary_cutoff": 25,
            "light_cutoff": 573,
            "moderate_cutoff": 1002,
        }

        # Create the algorithm with default parameters
        algorithm = factory.create(params)
        self.assertIsNotNone(algorithm)
        self.assertIsInstance(algorithm, evenson2008.Evenson2008)

        # Execute the algorithm
        results = algorithm.calculate(self.db_manager, recordsets)
        self.assertIsNotNone(results)
        self.assertEqual(len(results), 1)  # Expecting 4 categories
        self.assertIn("Sedentary", results[0]["result"])
        self.assertIn("Light", results[0]["result"])
        self.assertIn("Moderate", results[0]["result"])

    def _open_database(self, db_path: str = ":memory:"):
        # Create a new database in RAM
        self.manager = DBManager(db_path, overwrite=True, echo=False, newfile=True)
        self.assertIsNotNone(self.manager)
        return self.manager

    def _create_participant(self, session, name: str, description: str) -> Participant:
        participant = Participant()
        participant.name = name
        participant.description = description
        session.add(participant)
        session.commit()
        return participant

    def _load_sample_applewatch_data(
        self, participant: Participant = None
    ) -> list | None:
        if participant is None:
            return None

        importer = AppleWatchImporter(self.db_manager, participant)
        self.assertIsNotNone(importer)

        # Get current file path
        current_path = os.path.dirname(os.path.abspath(__file__))
        sample_data_path = os.path.join(
            current_path, "..", "importers", "samples", "AppleWatch.zip"
        )

        results = importer.load(sample_data_path)
        self.assertIsNotNone(results)
        self.assertGreater(len(results), 0)

        importer.import_to_database(results)
        return True
