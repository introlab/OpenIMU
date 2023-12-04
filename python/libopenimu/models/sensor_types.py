# from libopenimu.models.Base import Base
# from sqlalchemy import Column, Integer, String, Sequence


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
    CURRENT = 9
    BAROMETER = 10
    TEMPERATURE = 11
    FSR = 12
    BEACON = 13
    ACTIVITY = 14
    HEADINGS = 15
    BIOMETRICS = 16
    QUESTIONS = 17

    # All values in a dictionary
    value_dict = {ACCELEROMETER: 'ACCELEROMETER',
                  GYROMETER: 'GYROMETER',
                  MAGNETOMETER: 'MAGNETOMETER',
                  LUX: 'LUX',
                  GPS: 'GPS',
                  HEARTRATE: 'HEARTRATE',
                  ORIENTATION: 'ORIENTATION',
                  STEP: 'STEP',
                  BATTERY: 'BATTERY',
                  CURRENT: 'CURRENT',
                  BAROMETER: 'BAROMETER',
                  TEMPERATURE: 'TEMPERATURE',
                  ACTIVITY: 'ACTIVITY',
                  HEADINGS: 'HEADINGS',
                  BIOMETRICS: 'BIOMETRICS',
                  QUESTIONS: 'QUESTIONS'}

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
        # Will populate database with table tabSensorTypes
        try:
            for id_sensor in SensorType.value_dict:
                conn.execute("INSERT INTO tabSensorTypes (id_sensor_type, name)"
                             "VALUES (?,?)", (id_sensor, SensorType.value_dict[id_sensor]))

        except Exception as e:
            print('Insert Error: ', str(e))

    @staticmethod
    def sensor_type_validation(id_sensor_type):
        # assert(SensorType.is_valid_type(id_sensor_type) is True), "SensorType not in valid range"
        return


# Not used...
# class DBSensorType(Base):
#     __tablename__ = 'tabSensorTypes'
#     id_sensor_type = Column(Integer, Sequence('id_sensor_type_sequence'), primary_key=True, autoincrement=True)
#     name = Column(String, nullable=False)
#
#     # Database rep (optional)
#     def __repr__(self):
#         return "<DBSensorType(name='%s')>" % self.name
