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

    def test_as_from_tuple(self):

        group = Group((1, 'Group Name', 'Group Description'))
        participant = Participant((2, group.as_tuple(), 'Participant Name', 'Participant Description'))
        t = (3, participant.as_tuple(), 'Recordset Name', 10, 20)
        record = Recordset(t)

        self.assertEqual(record.id_recordset, 3)
        self.assertEqual(record.participant.as_tuple(), participant.as_tuple())
        self.assertEqual(record.name, 'Recordset Name')
        self.assertEqual(record.start_timestamp, 10)
        self.assertEqual(record.end_timestamp, 20)
        self.assertEqual(t, record.as_tuple())

    def test_properties(self):
        record = Recordset()
        record.id_recordset = 3
        record.participant = Participant()
        record.name = 'Record Name'
        record.start_timestamp = 22
        record.end_timestamp = 33

        self.assertEqual(record.get_id_recordset(), 3)
        self.assertEqual(record.participant, Participant())
        self.assertEqual(record.name, 'Record Name')
        self.assertEqual(record.start_timestamp, 22)
        self.assertEqual(record.end_timestamp, 33)

    def test_equality(self):
        record1 = Recordset()
        record2 = Recordset()
        group = Group((1, 'Group Name', 'Group Description'))
        participant = Participant((2, group.as_tuple(), 'Participant Name', 'Participant Description'))
        t = (3, participant.as_tuple(), 'Recordset Name', 10, 20)
        record3 = Recordset(t)

        self.assertNotEqual(record1, record3)
        self.assertNotEqual(record2, record3)
        self.assertEqual(record1, record2)
        self.assertEqual(record3, record3)