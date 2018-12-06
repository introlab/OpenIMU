"""
 Will contain sqlite driver
 @authors Simon Brière, Dominic Létourneau
 @date 27/03/2018
"""

from libopenimu.models.Base import Base

from sqlalchemy import Column, Integer, Sequence, ForeignKey, TIMESTAMP, Interval, BLOB, String

class DataSet(Base):
    __tablename__ = 'tabDataSet'
    name = Column(String, nullable=False, primary_key=True)
    description = Column(String)
    creation_date = Column(TIMESTAMP, nullable=False)
    upload_date = Column(TIMESTAMP, nullable=False)
    author = Column(String, nullable=False)

    # Database rep (optional)
    def __repr__(self):
        return "<Dataset(name='%s', description='%s', author='%s', creation_date='%s', upload_date='%s')>" % \
               (self.name, self.description, self.author, str(self.creation_date), str(self.upload_date))
