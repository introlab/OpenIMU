"""
 Group
 @authors Simon Brière, Dominic Létourneau
 @date 27/03/2018
"""

from libopenimu.models.Base import Base
from sqlalchemy import Column, Integer, String, Sequence
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

