from .BaseAlgorithm import BaseAlgorithmFactory
from .BaseAlgorithm import BaseAlgorithm
from libopenimu.models.sensor_types import SensorType
from libopenimu.db.DBManager import DBManager

# actual algorithm is here
from .freedson_adult_1998 import freedson_adult_1998


class FreedsonAdult1998(BaseAlgorithm):
    def __init__(self, params: dict):
        super().__init__(params)

    def configure(self, params: dict):
        print('FreedsonAdult1998.configure')
        pass

    def calculate(self, manager: DBManager, recordsets : list):
        print('FreedsonAdult1998.calculate')
        print('Using recordsets', recordsets)

        results = []

        for record in recordsets:
            # Get all sensors in record
            sensors = manager.get_all_sensors(id_sensor_type=SensorType.ACCELEROMETER)
            for sensor in sensors:

                # print('Found Accelerometer')
                channels = manager.get_all_channels(sensor=sensor)

                # print('Found channels: ', channels)
                for channel in channels:
                    if channel.label == 'Accelerometer_Y':
                        # print('Processing Channel :', channel)
                        # Will get all data (converted to floats)
                        channel_data = manager.get_all_sensor_data(recordset=record, convert=True, sensor=sensor,
                                                                   channel=channel)
                        if len(channel_data) > 0:
                            # Process all sensor data
                            results.append(freedson_adult_1998(channel_data, sensor.sampling_rate))

        # Return an array with results for each recordset
        return results


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
        return 'Freedson Adult 1998'

    def unique_id(self):
        return 1

    def info(self):

        my_info = {}

        my_info['description'] = """ \
        It is a uniaxial accelerometer that assesses accelerations ranging from 0.05-2.0 G and is band limited with a 
        frequency response from 0.25-2.5 Hz.
                
        The acceleration signal is filtered by an analog bandpass filter and digitized by an 8 bit A/D converter at a 
        sampling rate of 10 samples per second.
        
        Each digitized signal is summed over a user specified time interval (epoch), and at the end of each epoch 
        the activity count is stored internally and the accumulator is reset to zero. In the current study, a 60-s
         epoch was used and activity counts were expressed as the average counts per minute over the 6 min of exercise. 
        
        
        Cut points (intensity buckets): 
        * https://actigraph.desk.com/customer/portal/articles/2515802
        
        Counts (accelerator sum over 60 s)
        * https://actigraph.desk.com/customer/portal/articles/2515580-What-are-counts-
        
        Notes:
        --> Only Y axis used on Actigraph devices.
        8 bits = 256 = 2g
        
        epoch = 60 seconds
                        
        """
        my_info['name'] = self.name()
        my_info['author'] = 'Dominic Létourneau'
        my_info['version'] = '0.1'
        my_info['reference'] = ("Freedson PS1, Melanson E, Sirard J., Calibration of the Computer Science and "
                                "Applications, Inc. accelerometer., Med Sci Sports Exerc. 1998 May;30(5):777-81")
        my_info['unique_id'] = self.unique_id()

        return my_info

    def required_sensors(self):
        return [SensorType.ACCELEROMETER]

# Factory init
def init():
    return BaseAlgorithmFactory.register_factory(FreedsonAdult1998Factory())



