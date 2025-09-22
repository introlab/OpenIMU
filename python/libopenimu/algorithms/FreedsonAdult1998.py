from libopenimu.models.sensor_types import SensorType
from libopenimu.db.DBManager import DBManager
from .BaseAlgorithm import BaseAlgorithmFactory
from .BaseAlgorithm import BaseAlgorithm

# actual algorithm is here
from .freedson_adult_1998 import freedson_adult_1998


class FreedsonAdult1998(BaseAlgorithm):
    def __init__(self, params: dict):
        super().__init__(params)

    def configure(self, params: dict):
        # print('FreedsonAdult1998.configure')
        super().configure(params)

    def calculate(self, manager: DBManager, recordsets: list):
        # print('FreedsonAdult1998.calculate')
        # print('Using recordsets', recordsets)

        results = []

        for record in recordsets:
            # Get all sensors in record
            sensors = manager.get_all_sensors(id_sensor_type=SensorType.ACCELEROMETER)

            for sensor in sensors:
                # print('Found Accelerometer')
                channels = manager.get_all_channels(sensor=sensor)
                # print('Found channels: ', channels)
                for channel in channels:
                    if channel.label == "Accelerometer_Y":
                        # print('Processing Channel :', channel)
                        # Will get all data (converted to floats)
                        channel_data = manager.get_all_sensor_data(
                            recordset=record,
                            convert=True,
                            sensor=sensor,
                            channel=channel,
                        )
                        if len(channel_data) > 0:
                            # Process all sensor data
                            result = {
                                "id_recordset": record.id_recordset,
                                "result_name": record.name
                                + " ("
                                + sensor.location
                                + "/"
                                + sensor.name
                                + ")",
                                "id_sensor": sensor.id_sensor,
                                "result": freedson_adult_1998(
                                    self.params, channel_data, sensor.sampling_rate
                                ),
                            }
                            results.append(result)

        # Return an array with results for each recordset
        return results


class FreedsonAdult1998Factory(BaseAlgorithmFactory):
    """Factory for Freedson Adult 1998 algorithm."""

    def __init__(self):
        super().__init__()

    def unique_key(self) -> str:
        return "FreedsonAdult1998"

    def create(self, params: dict):
        # Create instance of algorithm
        return FreedsonAdult1998(params)

    def params(self):
        return {
            "sedentary_cutoff": {
                "type": "float",
                "default_value": 99.0,
                "min_value": 0,
                "max_value": 15000,
                "description": "sedentary_cutoff description",
            },
            "light_cutoff": {
                "type": "float",
                "default_value": 1951.0,
                "min_value": 0,
                "max_value": 15000,
                "description": "light_cutoff description",
            },
            "moderate_cutoff": {
                "type": "float",
                "default_value": 5724.0,
                "min_value": 0,
                "max_value": 15000,
                "description": "moderate_cutoff description",
            },
            "vigorous_cutoff": {
                "type": "float",
                "default_value": 9498.0,
                "min_value": 0,
                "max_value": 15000,
                "description": "vigorous_cutoff description",
            },
        }

    def results(self) -> list:
        """
        Should return a dict with the results structure and description.
        :return dict:
        """
        return [
            {"name": "sedentary", "description": "Minutes for sedentary activity"},
            {"name": "light", "description": "Minutes for light activity"},
            {"name": "moderate", "description": "Minutes for moderate activity"},
            {"name": "vigorous", "description": "Minutes for vigorous activity"},
        ]

    def name(self):
        return "Freedson Adult 1998"

    def unique_id(self):
        return 1

    def info(self):
        my_info = {
            "description": """ \
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

        """,
            "name": self.name(),
            "author": "Dominic Létourneau",
            "key": self.unique_key(),
            "version": "0.1",
            "reference": (
                "Freedson PS1, Melanson E, Sirard J., Calibration of the Computer Science and "
                "Applications, Inc. accelerometer., Med Sci Sports Exerc. 1998 May;30(5):777-81"
            ),
            "unique_id": self.unique_id(),
        }

        return my_info

    def required_sensors(self):
        return [SensorType.ACCELEROMETER]

    def build_data_table(self, results):
        data_table = {}
        headers = []
        data = []
        data_names = []
        # Results are stored in json, as a list of dict
        if isinstance(results, list):
            for result in results:
                if isinstance(result, dict):
                    result_data = result["result"]
                    result_name = result["result_name"]
                    headers.append(result_name)
                    if not data_names:
                        data_names = list(result_data.keys())
                    data.append(list(result_data.values()))

            data_table = {"headers": headers, "data_names": data_names, "data": data}

        return data_table


# Factory init
def init():
    """Initialize the Freedson Adult 1998 factory."""
    return BaseAlgorithmFactory.register_factory(FreedsonAdult1998Factory())
