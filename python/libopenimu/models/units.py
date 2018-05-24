'''
 Will contain data units
 @authors Simon Brière, Dominic Létourneau
 @date 20/03/2018
'''

from libopenimu.models.Base import Base
from sqlalchemy import Column, Integer, String, Sequence


class Units:
    METERS = 0
    GRAVITY_G = 1
    METERS_PER_SEC = 2
    RAD_PER_SEC = 3
    DEG_PER_SEC = 4
    VOLTS = 5
    LUX = 6
    NONE = 7
    AMPERES = 8
    KPA = 9
    UTESLA = 10
    GAUSS = 11
    CELCIUS = 12

    value_dict = {METERS: 'METERS',
                  GRAVITY_G: 'G',
                  METERS_PER_SEC: 'M/S',
                  RAD_PER_SEC: 'RAD/S',
                  DEG_PER_SEC: 'DEG/S',
                  VOLTS: 'VOLTS',
                  LUX: 'LUX',
                  NONE: 'NONE',
                  AMPERES: 'AMPS',
                  KPA: 'KILOPASCALS',
                  UTESLA: 'MICROTESLA',
                  GAUSS: 'GAUSS',
                  CELCIUS: 'CELCIUS'}

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
