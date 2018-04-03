'''
 Will contain data units
 @authors Simon Brière, Dominic Létourneau
 @date 20/03/2018
'''


import sqlite3


class Units:
    METERS = 0
    GRAVITY_G = 1
    METERS_PER_SEC = 2
    RAD_PER_SEC = 3

    value_types = [METERS, GRAVITY_G, METERS_PER_SEC, RAD_PER_SEC]
    value_names = ['METERS', 'G', 'M/S', 'RAD/S']

    @staticmethod
    def name(id_unit):
        return Units.value_names[id_unit]

    @staticmethod
    def populate_database(conn):
        """ Will populate database with table tabUnits """
        try:
            for id_unit in Units.value_types:
                conn.execute("INSERT INTO tabUnits (id_unit, name)"
                             "VALUES (?,?)", [id_unit, Units.value_names[id_unit]])

        except Exception as e:
            print('Insert Error: ', str(e))
