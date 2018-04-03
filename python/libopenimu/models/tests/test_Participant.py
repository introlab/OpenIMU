"""

    Unit testing for Participant
    @authors Simon Brière, Dominic Létourneau
    @date 03/04/2018

"""


import unittest
from libopenimu.models.Participant import Participant
from libopenimu.models.Group import Group


class ParticipantTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_as_from_tuple(self):
        my_tuple = (1, (1, 'Group Name', 'Group Description'), 'Participant Name', 'Participant Description')
        participant = Participant(my_tuple)
        participant2 = Participant()
        participant2.from_tuple(my_tuple)

        self.assertEqual(my_tuple, participant.as_tuple())
        self.assertEqual(participant.as_tuple(), participant2.as_tuple())

    def test_properties(self):
        id_participant = 1
        group = Group((1, 'Group Name', 'Group Description'))
        name = 'Participant Name'
        description = 'Participant Description'

        participant = Participant()
        participant.id_participant = id_participant
        participant.group = group
        participant.name = name
        participant.description = description

        self.assertEqual(participant.id_participant, id_participant)
        self.assertEqual(participant.group, group)
        self.assertEqual(participant.name, name)
        self.assertEqual(participant.description, description)
