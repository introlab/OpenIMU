"""
 Recordset
 @authors Simon Brière, Dominic Létourneau
 @date 05/04/2018
"""
from libopenimu.models.Base import Base
from libopenimu.models.Participant import Participant
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship


class Recordset(Base):
    __tablename__ = 'tabRecordsets'
    id_recordset = Column(Integer, Sequence('id_recordset_sequence'), primary_key=True, autoincrement=True)
    id_participant = Column(Integer, ForeignKey('tabParticipants.id_participant', ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)

    '''
    A type for datetime.timedelta() objects.
    The Interval type deals with datetime.timedelta objects. In PostgreSQL, the native INTERVAL type is used; 
    for others, the value is stored as a date which is relative to the “epoch” (Jan. 1, 1970).
    '''
    start_timestamp = Column(TIMESTAMP, nullable=False)
    end_timestamp = Column(TIMESTAMP, nullable=False)

    # Relationships
    participant = relationship("Participant")

    # Database rep (optional)
    def __repr__(self):
        return "<Recordset(id_participant='%s', name='%s', start_timestamp='%s', end_timestamp='%s'" % \
               (str(self.id_participant), str(self.name), str(self.start_timestamp), str(self.end_timestamp))





