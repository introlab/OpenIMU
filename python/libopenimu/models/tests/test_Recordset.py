"""

    Unit testing for Recordset
    @authors Simon Brière, Dominic Létourneau
    @date 05/04/2018

"""

import unittest
from libopenimu.models.Recordset import Recordset
from libopenimu.models.Participant import Participant
from libopenimu.models.Group import Group


class RecordsetTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_properties(self):
        record = Recordset()
        record.id_recordset = 3
        participant = Participant()
        record.participant = participant
        record.name = 'Record Name'
        record.start_timestamp = 22
        record.end_timestamp = 33

        self.assertEqual(record.id_recordset, 3)
        self.assertEqual(record.participant, participant)
        self.assertEqual(record.name, 'Record Name')
        self.assertEqual(record.start_timestamp, 22)
        self.assertEqual(record.end_timestamp, 33)

    def test_empty(self):
        record = Recordset()
        print(record)
        self.assertEqual(record.id_recordset, None)
        self.assertEqual(record.participant, None)
        self.assertEqual(record.name, None)
        self.assertEqual(record.start_timestamp, None)
        self.assertEqual(record.end_timestamp, None)
