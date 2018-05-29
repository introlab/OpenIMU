from .BaseAlgorithm import BaseAlgorithmFactory
from .BaseAlgorithm import BaseAlgorithm
from libopenimu.models.sensor_types import SensorType


# actual algorithm is here
from .freedson_adult_1998 import freedson_adult_1998


class FreedsonAdult1998(BaseAlgorithm):
    def __init__(self, params):
        super(BaseAlgorithm, self).__init__(params)

    def configure(self, params: dict):
        print('FreedsonAdult1998.configure')
        pass

    def calculate(self, recordsets : list):
        print('FreedsonAdult1998.calculate')
        return {}


class FreedsonAdult1998Factory(BaseAlgorithmFactory):
    def __init__(self):
        super(BaseAlgorithmFactory, self).__init__()
        pass

    def create(self, params: dict):
        # Create instance of algorithm
        return FreedsonAdult1998(params)

    def params(self):
        return dict()

    def name(self):
        return 'FreedsonAdult1998Factory'

    def description(self):
        return '''
        FreedsonAdult1998 Factory
        Description here.
        
        '''

    def required_sensors(self):
        return [SensorType.ACCELEROMETER]

# Factory init
def init():
    return BaseAlgorithmFactory.register_factory(FreedsonAdult1998Factory())



