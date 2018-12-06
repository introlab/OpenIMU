from libopenimu.models.Base import Base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship


class Subrecord(Base):
    __tablename__ = 'tabSubrecords'
    id_subrecord = Column(Integer, Sequence('id_subrecord_sequence'), primary_key=True, autoincrement=True)
    id_recordset = Column(Integer, ForeignKey('tabRecordsets.id_recordset', ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)

    '''
    A type for datetime.timedelta() objects.
    The Interval type deals with datetime.timedelta objects. In PostgreSQL, the native INTERVAL type is used; 
    for others, the value is stored as a date which is relative to the “epoch” (Jan. 1, 1970).
    '''
    start_timestamp = Column(TIMESTAMP, nullable=False)
    end_timestamp = Column(TIMESTAMP, nullable=False)

    # Relationships
    recordset = relationship("Recordset")

    # Database rep (optional)
    def __repr__(self):
        return "<SubRecord(id_subrecord='%i', id_recordset='%i', name='%s', start_timestamp='%s', end_timestamp='%s'" %\
               (self.id_subrecord, self.id_recordset, self.name, str(self.start_timestamp), str(self.end_timestamp))
