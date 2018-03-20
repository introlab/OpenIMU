"""

"""
import sqlite3


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

    value_types = [UINT8, SINT8, UINT16, SINT16, UINT32, SINT32, UINT64, SINT64, FLOAT32, FLOAT64]
    value_names = ['UINT8', 'SINT8', 'UINT16', 'SINT16', 'UINT32', 'SINT32', 'UINT64', 'SINT64', 'FLOAT32', 'FLOAT64']


    @staticmethod
    def name(type):
        return DataFormat.value_names[type]


    @staticmethod
    def populate_database(conn):
        """ Will polulate database with table tabDataFormat """
        try:
            for type in DataFormat.value_types:
                conn.execute("INSERT INTO tabDataFormat (id_data_format, name)"
                             "VALUES (?,?)",[type, DataFormat.value_names[type]])

        except Exception as e:
            print('Insert Error: ', str(e))