import numpy as np
from scipy import interpolate
from scipy import linspace


def resample_data(data, rate):
    # First get start time and end time
    start_time = data[0,0]
    stop_time = data[len(data) - 1,0]
    print('data length: ',len(data))
    print('start time ',start_time, ' stop_time ', stop_time)

    print('input dims',data.shape)

    # Interpolation

    # x,y,z accelerometer interpolation function (cubic)
    fx = interpolate.interp1d(data[:,0], data[:,1], kind='cubic')
    fy = interpolate.interp1d(data[:,0], data[:,2], kind='cubic')
    fz = interpolate.interp1d(data[:,0], data[:,3], kind='cubic')

    # Linear time
    t = linspace(start_time, stop_time, num=len(data))
    print('time length', len(t), t)
    xint = fx(t)
    yint = fy(t)
    zint = fz(t)

    print('size ', len(xint), len(yint), len(zint))
    return np.array((t, xint, yint, zint)).transpose()


"""
Test function
"""
if __name__ == '__main__':
    np.set_printoptions(suppress=True)
    import DataImporter as importer
    # Load test data
    rawData =  importer.load_mat_file('resources/test_data.mat')['data2']


    # Rate is 100Hz
    val = resample_data(rawData,100)

    print('answer dims',val.shape)

    t = val[:, 0]
    x = val[:, 1]
    y = val[:, 2]
    z = val[:, 3]

    print(len(t), len(x),len(y),len(z))
    print(type(t), type(rawData))

