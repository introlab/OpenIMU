from libopenimu.models.Base import Base
from libopenimu.models.Recordset import Recordset
from libopenimu.models.Subrecord import Subrecord
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, BLOB
from sqlalchemy.orm import relationship

class ProcessedDataRef(Base):
    __tablename__ = 'tabProcessedDataRef'
    id_processed_data_ref = Column(Integer, Sequence('id_processed_data_ref_sequence'), primary_key=True, autoincrement=True)
    id_processed_data = Column(Integer, ForeignKey("tabProcessedData.id_processed_data", ondelete="CASCADE"), nullable=False)
    id_recordset = Column(Integer, ForeignKey("tabRecordsets.id_recordset", ondelete="CASCADE"), nullable=True)
    id_subrecord = Column(Integer, ForeignKey("tabSubrecords.id_subrecord", ondelete="CASCADE"), nullable=True)

    # Relationships
    processed_data = relationship("ProcessedData")
    recordset = relationship("Recordset")
    subrecord = relationship("Subrecord")

    # Database rep (optional)
    def __repr__(self):
        return "<ProcessedDataRef(id_processed_data_ref='%i', id_processed_data='%i', id_recordset='%i', id_subrecord='%i')>" % (self.id_processed_data_ref, self.id_processed_data, self.id_recordset, self.id_subrecord)

