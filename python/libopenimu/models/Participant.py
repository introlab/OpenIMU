"""
 Participant
 @authors Simon Brière, Dominic Létourneau
 @date 27/03/2018
"""


from libopenimu.models.Base import Base
from libopenimu.models.Group import Group
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship


class Participant(Base):
    __tablename__ = 'tabParticipants'
    id_participant = Column(Integer, Sequence('id_participant_sequence'), primary_key=True, autoincrement=True)
    id_group = Column(Integer, ForeignKey("tabGroups.id_group", ondelete="CASCADE"), nullable=True)
    name = Column(String, nullable=False)
    description = Column(String)

    # Which group
    group = relationship("Group")

    # Database rep (optional)
    def __repr__(self):
        return "<Participant(id_group='%i', name='%s', description='%s')>" % (self.id_group, self.name, self.description)

