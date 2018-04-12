"""

"""


class SensorType:
    ACCELEROMETER = 0
    GYROMETER = 1
    MAGNETOMETER = 2
    LUX = 3
    GPS = 4
    HEARTRATE = 5
    ORIENTATION = 6
    STEP = 7
    BATTERY = 8

    value_types = [ACCELEROMETER, GYROMETER, MAGNETOMETER, LUX, GPS, HEARTRATE, ORIENTATION, STEP, BATTERY]
    value_names = ['ACCELEROMETER', 'GYROMETER', 'MAGNETOMETER', 'LUX', 'GPS', 'HEARTRATE', 'ORIENTATION', 'STEP',
                   'BATTERY']

    @staticmethod
    def is_valid_type(id_sensor_type):
        return SensorType.value_types.__contains__(id_sensor_type)

    @staticmethod
    def name(id_sensor_type):
        return SensorType.value_names[id_sensor_type]

    @staticmethod
    def populate_database(conn):
        """ Will populate database with table tabSensorTypes """
        try:
            for id_sensor in SensorType.value_types:
                conn.execute("INSERT INTO tabSensorTypes (id_sensor_type, name)"
                             "VALUES (?,?)", (id_sensor, SensorType.value_names[id_sensor]))

        except Exception as e:
            print('Insert Error: ', str(e))

    @staticmethod
    def sensor_type_validation(id_sensor_type):
        assert(SensorType.is_valid_type(id_sensor_type) is True), "SensorType not in valid range"
