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
    VOLTS = 4
    LUX = 5

    value_dict = {METERS: 'METERS',
                  GRAVITY_G: 'G',
                  METERS_PER_SEC: 'M/S',
                  RAD_PER_SEC: 'RAD/S',
                  VOLTS: 'VOLTS',
                  LUX: 'LUX'}

    @staticmethod
    def as_dict():
        return Units.value_dict

    @staticmethod
    def name(id_unit):
        return Units.value_dict[id_unit]

    @staticmethod
    def populate_database(conn):
        """ Will populate database with table tabUnits """
        try:
            for id_unit in Units.value_dict:
                conn.execute("INSERT INTO tabUnits (id_unit, name)"
                             "VALUES (?,?)", (id_unit, Units.value_dict[id_unit]))

        except Exception as e:
            print('Insert Error: ', str(e))

    @staticmethod
    def is_valid(id_unit):
        return Units.value_dict.__contains__(id_unit)
