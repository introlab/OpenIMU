"""
 Participant
 @authors Simon Brière, Dominic Létourneau
 @date 27/03/2018
"""


from libopenimu.models.Group import Group


class Participant:
    def __init__(self, id_participant=None, group=Group(), name=None, description=None):
        self.id_participant = id_participant
        self.group = group
        self.name = name
        self.description = description

    def __str__(self):
        return 'Participant: ' + str(self.as_tuple())

    def as_tuple(self):
        return self.id_participant, self.group.as_tuple(), self.name, self.description


