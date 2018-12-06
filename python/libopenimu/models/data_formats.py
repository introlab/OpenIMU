"""

"""
from libopenimu.models.Base import Base
from sqlalchemy import Column, Integer, String, Sequence
import numpy as np


class DataFormat:

    UINT8 = 0
    SINT8 = 1
    UINT16 = 2
    SINT16 = 3
    UINT32 = 4
    SINT32 = 5
    UINT64 = 6
    SINT64 = 7
    FLOAT32 = 8
    FLOAT64 = 9

    value_dict = {UINT8: 'UINT8',
                  SINT8: 'SINT8',
                  UINT16: 'UINT16',
                  SINT16: 'SINT16',
                  UINT32: 'UINT32',
                  SINT32: 'SINT32',
                  UINT64: 'UINT64',
                  SINT64: 'SINT64',
                  FLOAT32: 'FLOAT32',
                  FLOAT64: 'FLOAT64'}

    @staticmethod
    def name(id_data_format):
        return DataFormat.value_dict[id_data_format]

    @staticmethod
    def from_bytes(buffer, id_data_format):
        # Verify if valid
        # assert(DataFormat.is_valid(id_data_format))
        # assert(len(buffer) > 0)

        if id_data_format is DataFormat.UINT8:
            return np.frombuffer(buffer=buffer, dtype=np.uint8)

        elif id_data_format is DataFormat.SINT8:
            return np.frombuffer(buffer=buffer, dtype=np.int8)

        elif id_data_format is DataFormat.UINT16:
            return np.frombuffer(buffer=buffer, dtype=np.uint16)

        elif id_data_format is DataFormat.SINT16:
            return np.frombuffer(buffer=buffer, dtype=np.int16)

        elif id_data_format is DataFormat.UINT32:
            return np.frombuffer(buffer=buffer, dtype=np.uint32)

        elif id_data_format is DataFormat.SINT32:
            return np.frombuffer(buffer=buffer, dtype=np.int32)

        elif id_data_format is DataFormat.UINT64:
            return np.frombuffer(buffer=buffer, dtype=np.uint64)

        elif id_data_format is DataFormat.SINT64:
            return np.frombuffer(buffer=buffer, dtype=np.int64)

        elif id_data_format is DataFormat.FLOAT32:
            return np.frombuffer(buffer=buffer, dtype=np.float32)

        elif id_data_format is DataFormat.FLOAT64:
            return np.frombuffer(buffer=buffer, dtype=np.float64)

        else:
            return None

    @staticmethod
    def get_num_bytes(id_data_format):
        assert (DataFormat.is_valid(id_data_format))

        if id_data_format is DataFormat.UINT8 or id_data_format is DataFormat.SINT8:
            return 1

        if id_data_format is DataFormat.UINT16 or id_data_format is DataFormat.SINT16:
            return 2

        if id_data_format is DataFormat.UINT32 or id_data_format is DataFormat.SINT32 or id_data_format is DataFormat.FLOAT32:
            return 4

        if id_data_format is DataFormat.UINT64 or id_data_format is DataFormat.SINT64 or id_data_format is DataFormat.FLOAT64:
            return 8

        return None


    @staticmethod
    def populate_database(conn):
        """ Will populate database with table tabDataFormat """
        try:
            for format_id in DataFormat.value_dict:
                conn.execute("INSERT INTO tabDataFormat (id_data_format, name)"
                             "VALUES (?,?)", (format_id, DataFormat.value_dict[format_id]))

        except Exception as e:
            print('Insert Error: ', str(e))

    @staticmethod
    def is_valid(id_data_format):
        return DataFormat.value_dict.__contains__(id_data_format)


class DBDataFormat(Base):
    __tablename__ = 'tabDataFormats'
    id_data_format = Column(Integer, Sequence('id_data_format_sequence'), primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    precision = Column(Integer, nullable=False)

    # Database rep (optional)
    def __repr__(self):
        return "<DBDataFormat(name='%s')>" % self.name

