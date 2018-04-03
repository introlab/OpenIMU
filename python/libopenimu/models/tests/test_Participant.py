"""

    Unit testing for Participant
    @authors Simon Brière, Dominic Létourneau
    @date 03/04/2018

"""


import unittest
from libopenimu.models.Participant import Participant


class ParticipantTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_as_tuple(self):
        participant = Participant()
        print(participant.as_tuple())