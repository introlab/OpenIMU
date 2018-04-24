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

import sys


class CutPoints:
    # Cut points

    SEDENTARY = 'Sedentary'
    LIGHT = 'Light'
    MODERATE = 'Moderate'
    VIGOROUS = 'Vigorous'
    VERY_VIGOROUS = 'Very Vigorous'

    values = {SEDENTARY: [0, 99],
              LIGHT: [100, 1951],
              MODERATE: [1952, 5724],
              VIGOROUS: [5725, 9498],
              VERY_VIGOROUS: [9499, sys.maxsize]}

    @staticmethod
    def classify(value, scale=1.0):
        for keys in CutPoints.values:
            if CutPoints.values[keys][0] * scale <= value <= CutPoints.values[keys][1] * scale:
                return keys
        # Not found
        return 'Unknown'

    @staticmethod
    def base_frequency():
        # The base frequency for cut points
        return 10.0


def resample_data(data, in_sampling_rate, out_samping_rate):
    pass


def freedson_adult_1998(timeseries, sampling_rate):
    pass




