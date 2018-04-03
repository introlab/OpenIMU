"""
 Participant
 @authors Simon Brière, Dominic Létourneau
 @date 27/03/2018
"""


from libopenimu.models.Group import Group


class Participant:
    def __init__(self, *args, **kwargs):

        # Initialize from kwargs (and default values)
        self._id_participant = kwargs.get('id_participant', None)
        self._group = kwargs.get('group', Group())
        self._name = kwargs.get('name', None)
        self._description = kwargs.get('description', None)

        # Initialize from args
        for arg in args:
            if isinstance(arg, tuple):
                self.from_tuple(arg)
            elif isinstance(arg, Participant):
                self.from_tuple(arg.as_tuple())

    def __str__(self):
        return 'Participant: ' + str(self.as_tuple())

    def as_tuple(self):
        return self._id_participant, self._group.as_tuple(), self._name, self._description

    def from_tuple(self, t):
        (self._id_participant, group_tuple, self._name, self._description) = t
        self._group.from_tuple(group_tuple)

    def get_id_participant(self):
        return self._id_participant

    def set_id_participant(self, id_participant):
        self._id_participant = id_participant

    def get_group(self):
        return self._group

    def set_group(self, group):
        self._group = group

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_description(self):
        return self._description

    def set_description(self, description):
        self._description = description

    # Properties
    id_participant = property(get_id_participant, set_id_participant)
    group = property(get_group, set_group)
    name = property(get_name, set_name)
    description = property(get_description, set_description)


if __name__ == '__main__':
    p = Participant(id_participant=1, group=Group(), name='My Name', description='Description')
    p2 = Participant(p.as_tuple())
    print(p, p2)

