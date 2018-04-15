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

    # All values in a dictionary
    value_dict = {ACCELEROMETER: 'ACCELEROMETER',
                  GYROMETER: 'GYROMETER',
                  MAGNETOMETER: 'MAGNETOMETER',
                  LUX: 'LUX',
                  GPS: 'GPS',
                  HEARTRATE: 'HEARTRATE',
                  ORIENTATION: 'ORIENTATION',
                  STEP: 'STEP',
                  BATTERY: 'BATTERY'}

    @staticmethod
    def is_valid_type(id_sensor_type):
        if id_sensor_type in SensorType.value_dict:
            return True
        else:
            return False

    @staticmethod
    def as_dict():
        return SensorType.value_dict

    @staticmethod
    def name(id_sensor_type):
        return SensorType.value_dict[id_sensor_type]

    @staticmethod
    def populate_database(conn):
        """ Will populate database with table tabSensorTypes """
        try:
            for id_sensor in SensorType.value_dict:
                conn.execute("INSERT INTO tabSensorTypes (id_sensor_type, name)"
                             "VALUES (?,?)", (id_sensor, SensorType.value_dict[id_sensor]))

        except Exception as e:
            print('Insert Error: ', str(e))

    @staticmethod
    def sensor_type_validation(id_sensor_type):
        assert(SensorType.is_valid_type(id_sensor_type) is True), "SensorType not in valid range"
