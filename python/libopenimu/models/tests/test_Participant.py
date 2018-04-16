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

    def test_properties(self):
        id_participant = 1
        group = Group(id_group=1, name='Group Name', description='Group Description')
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
