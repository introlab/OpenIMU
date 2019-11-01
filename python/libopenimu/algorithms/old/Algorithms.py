import numpy as np
from scipy import interpolate
from scipy import linspace


def resample_data(data, rate):
    # First get start time and end time
    start_time = data[0, 0]
    stop_time = data[len(data) - 1, 0]
    print('data length: ', len(data))
    print('start time ', start_time, ' stop_time ', stop_time)

    print('input dims', data.shape)

    # Interpolation

    # x,y,z accelerometer interpolation function (cubic)
    fx = interpolate.interp1d(data[:, 0], data[:, 1], kind='cubic')
    fy = interpolate.interp1d(data[:, 0], data[:, 2], kind='cubic')
    fz = interpolate.interp1d(data[:, 0], data[:, 3], kind='cubic')

    # Linear time
    t = linspace(start_time, stop_time, num=((stop_time - start_time) * rate) + 1)
    print('time length', len(t), t)
    xint = fx(t)
    yint = fy(t)
    zint = fz(t)

    print('size ', len(xint), len(yint), len(zint))
    return np.array((t, xint, yint, zint)).transpose()


#
# Calculating magnitude
# array contains t, acc_x, acc_y, acc_z
# will return t, sqrt(acc_x^2,acc_y^2,acc_z^2)
#


def svm(data):
    # create result array
    mag = np.array((data[:, 0], np.sqrt(data[:, 1]**2 + data[:, 2]**2 + data[:, 3]**2))).transpose()
    print('mag : ', mag)
    print('mag shape ', mag.shape)
    return mag


#
#     Calculating counts
#     mag[t,mag_xyz]
#     epoch in seconds
#     rate in Hz
#


def counts(mag, epoch=60, rate=100):

    # empty counts
    counts = np.array([])

    # calculate the number of epochs to processed
    nb_epochs = np.ceil(len(mag) / (rate * epoch))
    padding = np.zeros((rate * epoch) - len(mag) % (rate * epoch))

    print('padding size: ', len(padding))
    print('should have nb_epochs', nb_epochs)

    # Put all data, padded with zeros
    tmpdata = np.append(mag[:, 1], padding)
    print('Total size', len(tmpdata))

    # Split into epochs of x seconds
    epochs = np.split(tmpdata, len(tmpdata) / (rate * epoch))

    # Iterate through epochs
    # for i in range(0, len(epochs)):
    #   counts = np.append(counts, np.sum(epochs[i]))
    for s_epoch in enumerate(epochs):
       counts = np.append(counts, np.sum(s_epoch))
    # print('counts ', counts)
    # plt.show()
    return [nb_epochs, counts]


# Freedson,Adult, 1998
#
# It is a uniaxial accelerometer that assesses accelerations ranging from 0.05-2.0 G and is band limited with a
# frequency response from 0.25-2.5 Hz.
#
# The acceleration signal is filtered by an analog bandpass filter and digitized by an 8 bit A/D converter at a sampling
# rate of 10 samples per second.
#
# Each digitized signal is summed over a user specified time interval (epoch), and at the end of each epoch the activity
# count is stored internally and the accumulator is reset to zero. In the current study, a 60-s epoch was used and
# activity counts were expressed as the average counts per minute over the 6 min of exercise.


def freedson_adult_1998(data, epoch_secs, rate):
    # First let's resample the data
    resampled_data = resample_data(data, rate)

    # Then calculate the magnitude
    mag = svm(resampled_data)

    # Then calculate the counts per epochs
    [nb_epochs, my_counts] = counts(mag, epoch_secs, rate)

    # Return the result
    return [nb_epochs, my_counts]


if __name__ == '__main__':
    np.set_printoptions(suppress=True)
    import libopenimu.importers.DataImporter as importer
    # import matplotlib.pyplot as plt
    # Load test data
    rawData = importer.load_mat_file('../../resources/test_data.mat')['data2']

    # Convert time to seconds
    # Our example have fractional days increments
    rawData[:, 0] = rawData[:, 0] * 24 * 60 * 60

    [nb_epochs, my_counts] = freedson_adult_1998(rawData, epoch_secs=60 ,rate=100)

    # plt.title('Counts')
    # plt.plot(my_counts)
    # plt.show()

