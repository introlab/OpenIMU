"""
 Group
 @authors Simon Brière, Dominic Létourneau
 @date 27/03/2018
"""

from libopenimu.models.Base import Base
from sqlalchemy import Column, Integer, Float, String, Sequence, TIMESTAMP, BLOB, ForeignKey
# from sqlalchemy.orm import relationship


class Group(Base):
    __tablename__ = 'tabGroups'

    id_group = Column(Integer, Sequence('id_group_sequence'), primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)

    def is_valid(self):
        return self.id_group is not None and self.name is not None and self.description is not None

    # Database rep (optional)
    def __repr__(self):

        return "<Group(id=%d name='%s', description='%s')>" % (self.id_group, self.name, self.description)



"""

# Old implementation

class Group:
    def __init__(self, *args, **kwargs):
        # Initial state
        self._id_group = None
        self._name = None
        self._description = None

        # Variable args
        if len(args) == 1:
            self.from_tuple(args[0])
        elif len(kwargs) == 3:
            self._id_group = kwargs.get('id_group', None)
            self._name = kwargs.get('name', None)
            self._description = kwargs.get('description', None)

    def __str__(self):
        return 'Group: ' + str(self.as_tuple())

    def __eq__(self, other):
        return self.as_tuple() == other.as_tuple()

    def set_id_group(self, id_group):
        self._id_group = id_group

    def get_id_group(self):
        return self._id_group

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_description(self, description):
        self._description = description

    def get_description(self):
        return self._description

    def print(self):
        print('Group', 'id_group:', self._id_group, 'name:', self._name, 'description:', self._description)

    def as_tuple(self):
        return self._id_group, self._name, self._description

    def from_tuple(self, tuple):
        (self._id_group, self._name, self._description) = tuple

    def is_valid(self):
        if self._id_group is None:
            return False
        if self._name is None:
            return False
        if self._description is None:
            return False
        return True

    # Properties
    id_group = property(get_id_group, set_id_group)
    name = property(get_name, set_name)
    description = property(get_description, set_description)

"""