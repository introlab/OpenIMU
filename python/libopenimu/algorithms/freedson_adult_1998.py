"""

@authors Dominic Létourneau
@date 24/04/2018

freedson_adult_1998

It is a uniaxial accelerometer that assesses accelerations ranging from 0.05-2.0 G and is band limited with a
frequency response from 0.25-2.5 Hz.

The acceleration signal is filtered by an analog bandpass filter and digitized by an 8 bit A/D converter at a sampling
rate of 10 samples per second.

Each digitized signal is summed over a user specified time interval (epoch), and at the end of each epoch the activity
count is stored internally and the accumulator is reset to zero. In the current study, a 60-s epoch was used and
activity counts were expressed as the average counts per minute over the 6 min of exercise.


Cut points (intensity buckets):
* https://actigraph.desk.com/customer/portal/articles/2515802

Counts (accelerator sum over 60 s)
* https://actigraph.desk.com/customer/portal/articles/2515580-What-are-counts-

Notes:
--> Only Y axis used on Actigraph devices
-->



8 bits = 256 = 2g

epoch = 60 seconds

0.001664g/count

"""

from libopenimu.models.SensorData import SensorData
import numpy as np
from scipy.signal import butter, sosfilt, sosfreqz
from libopenimu.tools.timing import timing


class CutPoints:
    # Cut points according to original paper

    SEDENTARY = 'Sedentary'
    LIGHT = 'Light'
    MODERATE = 'Moderate'
    VIGOROUS = 'Vigorous'
    VERY_VIGOROUS = 'Very Vigorous'
    UNKNOWN = 'Unknown'

    values = {SEDENTARY: [0, 99],
              LIGHT: [100, 1951],
              MODERATE: [1952, 5724],
              VIGOROUS: [5725, 9498],
              VERY_VIGOROUS: [9499, np.iinfo(np.int64).max]}

    @staticmethod
    def classify(value, scale=1.0):
        for keys in CutPoints.values:
            if CutPoints.values[keys][0] * scale <= value <= CutPoints.values[keys][1] * scale:
                return keys
        # Not found
        return CutPoints.UNKNOWN

    @staticmethod
    def base_frequency():
        # The base frequency for cut points
        return 10.0


def filter_data(data, fs, lowcut, highcut, order=5):

    # Create bandpass filter
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = butter(order, [low, high], btype='band', analog=False, output='sos')

    # Process data
    sosfilt(sos, data)

    return sosfilt(sos, data)


def generate_60s_epoch(timeseries, sampling_rate):
    # Number of samples in an epoch
    nb_samples = np.int32(60 * sampling_rate)

    # A list of 60 seconds epochs @ sampling_rate
    epochs = [[list(), list()]]

    # print('epoch size : ', nb_samples)
    # print('timeseries size : ', len(timeseries['values']))

    time = timeseries['time']
    values = timeseries['values']

    for i in range(0, len(time)):
        if len(epochs[-1][0]) >= nb_samples:
            epochs.append([list(), list()])

        # Insert values
        epochs[-1][0].append(np.double(time[i]))
        epochs[-1][1].append(np.float32(values[i]))

    # print('found epochs: ', len(epochs))

    return epochs


@timing
def freedson_adult_1998(samples: list, sampling_rate):

    scale = sampling_rate / CutPoints.base_frequency()
    print("Scaling: ", scale)

    results = {CutPoints.SEDENTARY: 0,
               CutPoints.LIGHT: 0,
               CutPoints.MODERATE: 0,
               CutPoints.VIGOROUS: 0,
               CutPoints.VERY_VIGOROUS: 0,
               CutPoints.UNKNOWN: 0}

    for sensor_data in samples:
        # Get time series
        timeseries = sensor_data.to_time_series()

        # Filter data bandpass (0.25-2.5 Hz), order = 4
        timeseries['values'] = filter_data(timeseries['values'], fs=sampling_rate, lowcut=0.25, highcut=2.5, order=4)

        # Separate into 60 secs epochs
        nb_samples = np.int32(60 * sampling_rate)
        epochs = generate_60s_epoch(timeseries, sampling_rate)

        for epoch in epochs:
            # print('len epoch 0,1', len(epoch[0]), len(epoch[1]))
            assert(len(epoch[0]) == len(epoch[1]))

            # Do not process empty epochs
            if len(epoch[0]) == 0:
                continue

            # Calculate if we have a fraction of an epoch
            complete_factor = nb_samples / len(epoch[1])

            # print('complete_factor: ', complete_factor)

            # Convert and scale to compare to reference cutpoints
            # Factor 128 is calculated since 2g = 256 (max 8 bit values)
            sum = int(128.0 * np.sum(np.abs(epoch[1])) * complete_factor)

            # Classify
            results[CutPoints.classify(sum, scale)] += 1

    print('results', results)
    return results


if __name__ == '__main__':
    from libopenimu.importers.ActigraphImporter import ActigraphImporter
    from libopenimu.models.sensor_types import SensorType
    from libopenimu.db.DBManager import DBManager

    import os


    db_filename = 'freedson.db'

    def import_data():
        # This will create the database (or overwrite it)s
        importer = ActigraphImporter(db_filename)
        # Load content of the file to the database
        results = importer.load('../../resources/samples/test.gt3x')
        importer.import_to_database(results)

    if not os.path.isfile(db_filename):
        print('importing actigraph data')
        import_data()

    manager = DBManager(db_filename)

    # Get recordsets
    recordsets = manager.get_all_recordsets()

    for record in recordsets:
        # Get all sensors in record
        sensors = manager.get_all_sensors()
        for sensor in sensors:
            if sensor.id_sensor_type == SensorType.ACCELEROMETER:
                print('Found Accelerometer')
                channels = manager.get_all_channels(sensor=sensor)
                for channel in channels:

                    if channel.label == 'Accelerometer_Y':
                        print('Processing Channel :', channel)
                        # Will get all data (converted to floats)
                        channel_data = manager.get_all_sensor_data(recordset=record, convert=True, sensor=sensor,
                                                                   channel=channel)

                        # Process all sensor data
                        results = freedson_adult_1998(channel_data, sensor.sampling_rate)

