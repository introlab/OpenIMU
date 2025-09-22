from scipy.signal import butter, sosfilt
import numpy as np
from .BaseAlgorithm import BaseAlgorithmFactory
from .BaseAlgorithm import BaseAlgorithm
from libopenimu.models.sensor_types import SensorType
from libopenimu.db.DBManager import DBManager


class CutPoints:
    # Cut points according to original paper

    SEDENTARY = "Sedentary"
    LIGHT = "Light"
    MODERATE = "Moderate"
    VIGOROUS = "Vigorous"

    values = {
        SEDENTARY: [0, 99],
        LIGHT: [100, 1951],
        MODERATE: [1952, 5724],
        VIGOROUS: [5724, np.iinfo(np.int64).max],
    }

    def set_cutoff_values(self, values: dict):
        self.values = {
            CutPoints.SEDENTARY: [0, values["sedentary_cutoff"]],
            CutPoints.LIGHT: [
                values["sedentary_cutoff"] + 0.001,
                values["light_cutoff"],
            ],
            CutPoints.MODERATE: [
                values["light_cutoff"] + 0.001,
                values["moderate_cutoff"],
            ],
            CutPoints.VIGOROUS: [
                values["moderate_cutoff"] + 0.001,
                np.iinfo(np.int64).max,
            ],
        }

    def classify(self, value, scale=1.0):
        for keys in self.values:
            if self.values[keys][0] <= value / scale <= self.values[keys][1]:
                return keys
        print("Classify out of range: " + str(value / scale))

    @staticmethod
    def base_frequency():
        # The base frequency for cut points
        return 10.0

    @staticmethod
    def build_dict():
        return {
            CutPoints.SEDENTARY: 0,
            CutPoints.LIGHT: 0,
            CutPoints.MODERATE: 0,
            CutPoints.VIGOROUS: 0,
        }


class Evenson2008(BaseAlgorithm):
    def __init__(self, params: dict):
        super().__init__(params)

    def configure(self, params: dict):
        # print('Evenson2008.configure')
        super().configure(params)

    def calculate(self, manager: DBManager, recordsets: list):
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
                    # if channel.label == 'Accelerometer_Y':
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

                if len(all_channels_data["Accelerometer_X"]) > 0:
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
                        "result": self.do_calculation(
                            all_channels_data, sensor.sampling_rate, samples_num
                        ),
                    }
                    results.append(result)

        # Return an array with results for each recordset
        return results

    @staticmethod
    def filter_data(data, fs, lowcut, highcut, order=5):

        # Create bandpass filter
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        sos = butter(order, [low, high], btype="band", analog=False, output="sos")

        return sosfilt(sos, data)

    @staticmethod
    def generate_15s_epoch(timeseries, sampling_rate):
        # Number of samples in an epoch
        nb_samples = np.int32(15 * sampling_rate)

        # A list of 15 seconds epochs @ sampling_rate
        epochs = [[list(), list()]]

        # print('epoch size : ', nb_samples)
        # print('timeseries size : ', len(timeseries['values']))

        time = timeseries["time"]
        values = timeseries["values"]

        # for i in range(0, len(time)):
        for i, _ in enumerate(time):
            if len(epochs[-1][0]) >= nb_samples:
                epochs.append([list(), list()])

            # Insert values
            epochs[-1][0].append(np.double(time[i]))
            epochs[-1][1].append(np.float32(values[i]))

        # print('found epochs: ', len(epochs))

        return epochs

    def do_calculation(self, samples: [list], sampling_rate, samples_num):

        scale = (
            sampling_rate / CutPoints.base_frequency() / 4
        )  # /4 because we have 15s epochs
        # print("Scaling: ", scale)

        c_results = CutPoints.build_dict()
        cutpoints = CutPoints()
        cutpoints.set_cutoff_values(self.params)

        all_values = np.zeros((samples_num, len(samples)))
        all_timestamps = np.zeros(samples_num)

        for channel_index, channel in enumerate(samples):
            current_index = 0
            for sample in samples[channel]:
                # Get time series
                values = sample.to_ndarray()

                # Filter data bandpass (0.25-2.5 Hz), order = 4
                filtered_data = Evenson2008.filter_data(
                    values, fs=sampling_rate, lowcut=0.25, highcut=2.5, order=4
                )
                all_values[
                    current_index : current_index + len(filtered_data), channel_index
                ] = filtered_data
                if channel_index == 0:
                    all_timestamps[
                        current_index : current_index + len(filtered_data)
                    ] = sample.timestamps.to_ndarray()
                current_index += len(filtered_data)

        # Compute magnitude of all acceleration components
        timeseries = {
            "values": np.linalg.norm(all_values, axis=1),
            "time": all_timestamps,
        }
        del all_timestamps
        del all_values
        # timeseries['values'] = samples[1].to_time_series()['values']

        # Separate into 15 secs epochs
        nb_samples = np.int32(15 * sampling_rate)
        epochs = Evenson2008.generate_15s_epoch(timeseries, sampling_rate)
        for epoch in epochs:
            # print('len epoch 0,1', len(epoch[0]), len(epoch[1]))
            # assert(len(epoch[0]) == len(epoch[1]))

            # Do not process empty epochs
            if len(epoch[0]) == 0:
                continue

            # Calculate if we have a fraction of an epoch
            complete_factor = nb_samples / len(epoch[1])

            # print('complete_factor: ', complete_factor)

            # Convert and scale to compare to reference cutpoints
            # Factor 128 is calculated since 2g = 256 (max 8 bit values)
            result_sum = int(np.sum(np.abs(epoch[1])) * complete_factor)

            # Classify
            c_results[
                cutpoints.classify(result_sum, scale)
            ] += 0.25  # 15 seconds epoch = 0.25 minutes

        # print('results', c_results)
        return c_results


class Evenson2008Factory(BaseAlgorithmFactory):
    # config_preset_input = QComboBox
    # config_sedentary_input = QSpinBox
    # config_light_input = QSpinBox
    # config_moderate_input = QSpinBox

    def __init__(self):
        super().__init__()

    def create(self, params: dict):
        # Create instance of algorithm
        return Evenson2008(params)

    def unique_key(self) -> str:
        return "Evenson2008"

    def params(self):
        return {
            "sedentary_cutoff": {
                "type": "float",
                "default_value": 25.0,
                "min_value": 0.0,
                "max_value": 15000.0,
                "description": "sedentary_cutoff description",
            },
            "light_cutoff": {
                "type": "float",
                "default_value": 573.0,
                "min_value": 0.0,
                "max_value": 15000.0,
                "description": "light_cutoff description",
            },
            "moderate_cutoff": {
                "type": "float",
                "default_value": 1000.0,
                "min_value": 0.0,
                "max_value": 15000.0,
                "description": "moderate_cutoff description",
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
        ]

    def name(self):
        return "Evenson 2008"

    def unique_id(self):
        return 2

    def info(self):
        my_info = {
            "description": """\
        Classify activity counts into various intensity levels (Sedentary, Light, Moderate, Vigorous) using 3D
        accelerometer data.

        A band-filter is applied to raw accelerometers data with a frequency response of 0.25 to 2.5 Hz.

        Each digitized signal is summed over a user specified time interval (epoch), and at the end of each epoch
        the activity count is stored internally and the accumulator is reset to zero.

        Epoch sizes of 15s are used, and activity counts are expressed as the average counts per epoch.

        Notes:
            - Uses all 3 accelerometers axis
            - Epoch size = 15 seconds
            - Final data is reported in seconds

        """,
            "name": self.name(),
            "key": self.unique_key(),
            "author": "Simon Brière",
            "version": "0.1",
            "reference": (
                "Kelly R. Evenson, Diane J. Catellier, Karminder Gill, Kristin S. Ondrak & Robert G. "
                "McMurray (2008) Calibration of two objective measures of physical activity for "
                "children, Journal of Sports Sciences, 26:14, 1557-1565, "
                "DOI: 10.1080/02640410802334196 "
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
    """Initialize the Evenson 2008 factory."""
    return BaseAlgorithmFactory.register_factory(Evenson2008Factory())
