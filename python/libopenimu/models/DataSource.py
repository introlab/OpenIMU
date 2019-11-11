from libopenimu.models.Base import Base
from libopenimu.models.Participant import Participant
from libopenimu.models.Recordset import Recordset

from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

import hashlib
import os


class DataSource(Base):
    __tablename__ = 'tabDataSources'
    # IDs and keys
    id_data_source = Column(Integer, Sequence('id_data_source_sequence'), primary_key=True, autoincrement=True)
    id_recordset = Column(Integer, ForeignKey('tabRecordsets.id_recordset', ondelete="CASCADE"), nullable=False)

    # Structure
    file_name = Column(String, nullable=False)
    file_md5 = Column(String, nullable=False)

    # Relationships
    recordset = relationship("Recordset", cascade="all,delete")

    @staticmethod
    def compute_md5(filename):
        # Initialize MD5
        md5 = hashlib.md5()

        # Read file and compute
        with open(filename, 'rb') as f:
            data = f.read(65536)
            while data:
                md5.update(data)
                data = f.read(65536)

        return md5

    @staticmethod
    def build_short_filename(filename):
        short_filename = filename
        filename = filename.replace('/', os.sep)
        file_split = filename.split(os.sep)

        if len(file_split) >= 4:
            short_filename = file_split[len(file_split) - 3] + '/' + file_split[len(file_split) - 2] \
                             + '/' + file_split[len(file_split) - 1]
        elif len(file_split) >= 3:
            short_filename = file_split[len(file_split) - 2] + '/' + file_split[len(file_split) - 1]

        return short_filename

    @staticmethod
    def datasource_exists_for_recordset(filename, recordset, md5, db_session):
        query = db_session.query(DataSource).filter(DataSource.file_name == filename, DataSource.recordset == recordset,
                                                    DataSource.file_md5 == md5)
        return query.first() is not None

    @staticmethod
    def datasource_exists(filename, md5, db_session):
        query = db_session.query(DataSource).filter(DataSource.file_name == filename, DataSource.file_md5 == md5)
        return query.first() is not None

    @staticmethod
    def datasource_exists_for_participant(filename, participant, md5, db_session):
        query = db_session.query(DataSource).join(Recordset).join(Participant).filter(DataSource.file_name == filename,
                                                                                      Participant.id_participant ==
                                                                                      participant.id_participant,
                                                                                      DataSource.file_md5 == md5)
        return query.first() is not None

    def update_datasource(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except Exception as e:
            message = 'Error updating datasource' + ': ' + str(e)
            print('Error: ', message)
            raise
