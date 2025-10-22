from scipy.signal import butter, sosfilt
import numpy as np

from .BaseAlgorithm import BaseAlgorithmFactory
from .BaseAlgorithm import BaseAlgorithm
from libopenimu.db.DBManager import DBManager
from libopenimu.models.sensor_types import SensorType


class Fraysse2021(BaseAlgorithm):
    def __init__(self, params: dict):
        super().__init__(params)

    def configure(self, params: dict):
        pass

    def calculate(self, manager: DBManager, recordsets: list):
        # Load accelerometer data for the recordsets
        results = []

        for record in recordsets:
            # Get all sensors in record
            sensors = manager.get_all_sensors(id_sensor_type=SensorType.ACCELEROMETER)

            for sensor in sensors:
                # print('Found Accelerometer')
                channels = manager.get_all_channels(sensor=sensor)
                samples_num = 0
                # print('Found channels: ', channels)
                all_channels_data = {
                    "Accelerometer_X": [],
                    "Accelerometer_Y": [],
                    "Accelerometer_Z": [],
                }
                for channel_index, channel in enumerate(channels):
                    # print('Processing Channel :', channel)
                    # Will get all data (converted to floats)
                    channel_data = manager.get_all_sensor_data(
                        recordset=record, convert=True, sensor=sensor, channel=channel
                    )
                    if len(channel_data) > 0:
                        for data in channel_data:
                            all_channels_data[channel.label].append(data)
                            if (
                                    channel_index == 0
                            ):  # Compute number of samples total, if we are at the first channel
                                samples_num += len(data.data)

                if len(all_channels_data["Accelerometer_X"]) > 0:  # We have data
                    # Filter data
                    wn = self.params["cutoff"] / sensor.sampling_rate
                    sos = butter(2, wn, btype='lowpass', output='sos')

                    all_values = np.zeros((samples_num, len(all_channels_data)))
                    all_timestamps = np.zeros(samples_num)

                    for channel_index, channel in enumerate(all_channels_data):
                        current_index = 0
                        for sample in all_channels_data[channel]:
                            # Get time series
                            values = sample.to_ndarray()

                            # Filter data bandpass (0.25-2.5 Hz), order = 4
                            filtered_data = sosfilt(sos, values)
                            all_values[
                                current_index: current_index + len(filtered_data), channel_index
                            ] = filtered_data
                            if channel_index == 0:
                                all_timestamps[
                                    current_index: current_index + len(filtered_data)
                                ] = sample.timestamps.to_ndarray()
                            current_index += len(filtered_data)

                    # Compute acceleration vector norm
                    timeseries = {
                        "values": np.linalg.norm(all_values, axis=1),
                        "time": all_timestamps,
                    }
                    del all_timestamps
                    del all_values
                    # Remove gravity
                    timeseries["values"][timeseries["values"] > 0] = timeseries["values"][
                                                                          timeseries["values"] > 0] - 1

                    # Remove negative values
                    np.absolute(timeseries['values'], out=timeseries['values'])

                    # Sum over window size
                    timeseries['values'] = np.convolve(timeseries['values'],
                                                       np.ones(self.params['window']*int(sensor.sampling_rate), dtype=int),
                                                       'valid')

                    # Categorize values
                    sedentary_light_threshold = self.params["light_cutoff"]/12*sensor.sampling_rate/100
                    light_moderate_threshold = self.params["moderate_cutoff"]/12*sensor.sampling_rate/100

                    cat = np.ones(timeseries['values'].size)
                    cat[timeseries['values'] > light_moderate_threshold] = 2
                    cat[timeseries['values'] < sedentary_light_threshold] = 0

                    # Compute time and generate results
                    result = {
                        "id_recordset": record.id_recordset,
                        "result_name": record.name
                                       + " ("
                                       + sensor.location
                                       + "/"
                                       + sensor.name
                                       + ")",
                        "id_sensor": sensor.id_sensor,
                        "result": {'Sedentary': np.sum(cat == 0) / sensor.sampling_rate,
                                   'Light': np.sum(cat == 1) / sensor.sampling_rate,
                                   'Moderate': np.sum(cat == 2) / sensor.sampling_rate},
                    }
                    results.append(result)

        return results



########################################################################################################################
class Fraysse2021Factory(BaseAlgorithmFactory):

    def __init__(self):
        super().__init__()

    def create(self, params: dict):
        # Create instance of algorithm
        return Fraysse2021(params)

    def unique_key(self) -> str:
        return "Fraysse2021"

    def params(self):
        return {
            "window": {
                "type": "integer",
                "default_value": 5,
                "min_value": 0,
                "max_value": 30,
                "description": "Rolling window size over which to process active time computation",
            },
            "cutoff": {
                "type": "float",
                "default_value": 20.0,
                "min_value": 0.0,
                "max_value": 15000.0,
                "description": "Cut-off frequency for data filtering",
            },
            "light_cutoff": {
                "type": "float",
                "default_value": 255.0,
                "min_value": 0.0,
                "max_value": 15000.0,
                "description": "Light threshold cut-off value",
            },
            "moderate_cutoff": {
                "type": "float",
                "default_value": 588.0,
                "min_value": 0.0,
                "max_value": 15000.0,
                "description": "Moderate threshold cut-off value",
            }
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
        ]

    def name(self):
        return "Fraysse 2021"

    def unique_id(self):
        return 3

    def info(self):
        my_info = {
            "description": """\
        Classify activity into various intensity levels (Sedentary, Light, Moderate) using 3D
        accelerometer data.

        This works for wrist-worn sensors with elderly.

        """,
            "name": self.name(),
            "key": self.unique_key(),
            "author": "Simon Brière",
            "version": "0.1",
            "reference": (
                "Fraysse F, Post D, Eston R, Kasai D, Rowlands AV, Parfitt G. "
                "Physical Activity Intensity Cut-Points for Wrist-Worn GENEActiv in Older Adults."
                "Front Sports Act Living.2021 Jan 15;2:579278. doi: 10.3389 / "
                "fspor.2020.579278.PMID: 33521631; PMCID: PMC7843957."
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
    """Initialize the Fraysse 2021 factory."""
    return BaseAlgorithmFactory.register_factory(Fraysse2021Factory())
