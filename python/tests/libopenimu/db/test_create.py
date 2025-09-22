import unittest

from sqlalchemy import create_engine, inspect

from libopenimu.models.Base import Base


class CreateTest(unittest.TestCase):

    # All tests will use this name for the database
    TESTDB_NAME = ":memory:"

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_database(self):

        # engine = create_engine('sqlite:///:memory:', echo=True)
        engine = create_engine("sqlite:///" + self.TESTDB_NAME, echo=True)

        # Will create all tables
        Base.metadata.create_all(engine)

        # Check that tables exist
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print("Tables in database:", tables)
        self.assertGreater(len(tables), 0)
