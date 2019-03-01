from libopenimu.models.Base import Base
from libopenimu.models.ProcessedDataRef import ProcessedDataRef  # Important for relationships, don't delete!
from sqlalchemy import Column, Integer, String, Sequence, BLOB, TIMESTAMP
from sqlalchemy.orm import relationship


class ProcessedData(Base):
    __tablename__ = 'tabProcessedData'
    id_processed_data = Column(Integer, Sequence('id_processed_data_sequence'), primary_key=True, autoincrement=True)
    id_data_processor = Column(Integer, nullable=False) #TODO: Relationship with data processor table...
    name = Column(String, nullable=False)
    data = Column(BLOB, nullable=False)
    processed_time = Column(TIMESTAMP, nullable=False)

    # Relationships
    processed_data_ref = relationship("ProcessedDataRef", cascade="all,delete")

    # Database rep (optional)
    def __repr__(self):
        return "<ProcessedData(id_processed_data='%i', id_data_processor='%i', name='%s', data='%s')>" % (self.id_processed_data, self.id_data_processor, self.name, self.data)

