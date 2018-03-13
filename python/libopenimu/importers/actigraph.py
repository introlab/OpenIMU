"""
This is a prototype Actigraph data importer.
Documentation of the binary format : https://github.com/actigraph/GT3X-File-Format (for newer devices)

@author Dominic Létourneau
"""

# Everything needed for zip
import zipfile
import struct
import numpy as np
import time

class RecordType:
    """
        All Actigraph record types.
    """
    ACTIVITY = 0x00
    BATTERY = 0x02
    EVENT = 0x03
    HEART_RATE_BPM = 0x04
    LUX = 0x05
    METADATA = 0x06
    TAG = 0x07
    EPOCH = 0x09
    HEART_RATE_ANT = 0x0B
    EPOCH2 = 0x0C
    CAPSENSE = 0x0D
    HEART_RATE_BLE = 0x0E
    EPOCH3 = 0x0F
    EPOCH4 = 0x10
    PARAMETERS = 0x15
    SENSOR_SCHEMA = 0x18
    SENSOR_DATA = 0x19
    ACTIVITY2 = 0x1A


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print("%s function took %0.3f ms" % (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap


def gt3x_read_uint12(data, nb_axis=3):
    """
    Based on the c# code here:
    https://github.com/actigraph/GT3X-File-Format/blob/master/LogRecords/Activity.md

    :param data:
    :param nb_axis:
    :return:
    """
    # print('reading.')

    offset = 0
    current = np.uint16(0)
    byte_index = 0

    # C-Style array
    lines = int(np.floor(len(data) * 8 / (12 * nb_axis)))
    # print ('lines:',lines)
    samples = np.ndarray(shape=(lines, nb_axis), dtype=np.int16, order='C')

    # We know exactly how many samples the data should contain
    for line in range(0, lines):
        for axis in range(0, nb_axis):
            # print('axis:', axis)
            shifter = np.uint16(0)

            if (offset & 0x7) == 0x0000:
                current = data[byte_index]
                byte_index += 1
                shifter = (current & 0xFF) << 4
                offset += 8
                current = data[byte_index]
                byte_index += 1
                shifter |= (current & 0xF0) >> 4
                offset += 4
            else:
                shifter = (current & 0x0F) << 8
                offset += 4
                current = data[byte_index]
                byte_index += 1
                shifter |= (current & 0xFF)
                offset += 8
            # Sign extension
            if (shifter & 0x0800) != 0:
                shifter |= 0xF000

            #fill data
            samples[line][axis] = np.int16(shifter)
            # print('sample:', np.int16(shifter))

    return samples

def gt3x_activity_extractor(timestamp, data, samplerate, scale):
    """

    One second of raw activity samples packed into 12-bit values in YXZ order. Activity data is stored
    continuously for every sample the device records over one second. Each sample contains all three axis
    of data in the following order: y-axis, x-axis, and z-axis.

    To help conserve space, activity samples are bit-packed. A single 3-axis sample takes up 36 bits of data
    (12 bits per axis). To parse this data, you will have to portion the byte data into nibbles.

    The activity samples are encoded as 12-bit two's complement values. Two's complement is the standard signed
    integer encoding used in modern architectures.

    To convert the 12-bit values to 16-bit signed integers (Int16) for use, they must be sign-extended.
    Endianness doesn't exactly apply for 12-bit values, but it is basically big-endian. In other words,
    the bits are in order from most-significant to least-significant.


    :param data:
    :param timestamp:
    :param samplerate:
    :return:
    """

    # Read all at once and scale
    samples = gt3x_read_uint12(data) / scale

    # Add time
    # stop, num=50, endpoint=True, retstep=False, dtype=None):
    my_time = np.linspace(timestamp, timestamp + 1, num=samplerate, endpoint=False)

    # Make sure time is of the same size (some records are not complete)
    my_time.resize(len(samples))

    # Add column at the beginning with time values
    result = np.column_stack((my_time, samples))

    # return samples in g
    return result

def gt3x_battery_extractor(timestamp, data, samplerate):
    """

    Battery voltage in millivolts as a little-endian unsigned short (2 bytes).

    :param data:
    :param samplerate:
    :return:
    """
    # print('Battery Extractor')
    battery = 0.0

    if len(data) is 2:
        [battery] = struct.unpack_from('<H', data)
        # Convert to volts
        battery *= 0.001
        # print('battery:', battery)

    # Return timestamp and battery data
    return np.column_stack((timestamp, battery))

def gt3x_event_extractor(timestamp, data, samplerate):
    """

    :param data:
    :param samplerate:
    :return:
    """
    #print('Event Extractor',timestamp, data)
    return np.column_stack((timestamp, data))


def gt3x_lux_extractor(timestamp, data, samplerate):
    """

    :param data:
    :param samplerate:
    :return:
    """
    # print('Lux Extractor')
    lux = 0

    if len(data) is 2:
        lux = struct.unpack_from('<H', data)

    return np.column_stack((timestamp, lux))


def gt3x_metadata_extractor(timestamp, data, samplerate):
    """
    Should contain a json object

    :param data:
    :param samplerate:
    :return:
    """
    #print('Metadata Extractor', timestamp, data)
    # TODO Not yet implemented
    return np.column_stack((timestamp,data))


def gt3x_parameters_extractor(timestamp, data, samplerate):
    """
    https://github.com/actigraph/GT3X-File-Format/blob/master/LogRecords/Parameters.md
    :param data:
    :param samplerate:
    :return:
    """
    #print('Parameters Extractor', timestamp, data)
    # TODO Not yet implemented
    return np.column_stack((timestamp,data))


def gt3x_calculate_checksum(separator, record_type, timestamp, record_size, record_data):
    """

    A 1-byte checksum immediately follows the record payload. It is a 1's complement,
    exclusive-or (XOR) of the log header and payload with an initial value of zero.

    :param separator: 0x1E
    :param record_type: record data type
    :param timestamp: unix timestamp
    :param record_size: payload size
    :param record_data: payload
    :return: checksum
    """

    # date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(timestamp))
    # print('date:', date)

    checksum = np.uint8(separator)
    checksum ^= record_type & 0xFF
    checksum ^= (timestamp & 0xFF)
    checksum ^= ((timestamp >> 8) & 0xFF)
    checksum ^= ((timestamp >> 16) & 0xFF)
    checksum ^= ((timestamp >> 24) & 0xFF)
    checksum ^= (record_size & 0xFF)
    checksum ^= ((record_size >> 8) & 0xFF)

    for i in range(0, len(record_data)):
        checksum ^= record_data[i]

    checksum = ~checksum

    return np.uint8(checksum)

@timing
def gt3x_importer(filename):
    """

    The zipped file should contain two files info.txt and log.bin.

    :param filename: The gt3x file name
    :return: The data
    """
    print('Loading: ', filename)

    # Dict containing the information of the file
    info = {}

    # Empty lists to fill with data from records
    activity_data = []
    battery_data = []
    lux_data = []
    event_data = []
    metadata_data = []
    parameters_data = []

    with zipfile.ZipFile(filename) as myzip:
        # Reading info.txt file
        with myzip.open('info.txt') as myfile:
            lines = myfile.readlines()
            for line in lines:
                items = line.decode('UTF-8').rstrip('\r\n').split(': ')
                # We must have the list with 2 items, key and value
                if len(items) is 2:
                    info[items[0]] = items[1]

        sample_rate = float(info['Sample Rate'])
        scale = float(info['Acceleration Scale'])
        print ('info', info)
        # print('My Sample rate:', sample_rate)

        # Reading log.bin
        with myzip.open('log.bin') as myfile:
            filedata = myfile.read()
            print('filedata size', len(filedata), 'type:', type(filedata))
            data_offset = 0

            while data_offset < len(filedata):
                # print('data_offset:', data_offset)
                # < Little Endian, byte, byte, uint32, uint16
                [separator, record_type, timestamp, record_size] = struct.unpack_from('<BBIH', filedata, offset= data_offset)
                if separator is not 0x1e:
                    print('Separator Error!!!')

                # print('Extracting record: ', hex(separator), hex(record_type), hex(timestamp), hex(record_size))
                [record_data, checksum] = struct.unpack_from('<' + str(record_size) + 'sB', filedata, offset= data_offset + 8)

                # Verify checksum
                cs_check = gt3x_calculate_checksum(separator, record_type, timestamp, record_size, record_data)

                if checksum == cs_check:
                    if record_type is RecordType.ACTIVITY:
                        activity_data.append(gt3x_activity_extractor(timestamp, record_data, sample_rate, scale))
                    elif record_type is RecordType.BATTERY:
                        battery_data.append(gt3x_battery_extractor(timestamp, record_data, sample_rate))
                    elif record_type is RecordType.EVENT:
                        event_data.append(gt3x_event_extractor(timestamp, record_data, sample_rate))
                    elif record_type is RecordType.LUX:
                        lux_data.append(gt3x_lux_extractor(timestamp, record_data, sample_rate))
                    elif record_type is RecordType.METADATA:
                        metadata_data.append(gt3x_metadata_extractor(timestamp, record_data, sample_rate))
                    elif record_type is RecordType.PARAMETERS:
                        parameters_data.append(gt3x_parameters_extractor(timestamp, record_data, sample_rate))
                    else:
                        print('Unhandled record type:', hex(record_type), 'size:', len(record_data))
                else:
                    print('Checksum error read:',checksum, 'calculated:',cs_check)

                # print('record length:', len(record_data), 'checksum:', hex(checksum))
                data_offset += 8 + len(record_data) + 1

    # Return file info and data contents
    return [info, {'activity': activity_data,
                   'battery': battery_data,
                   'lux': lux_data,
                   'event': event_data,
                   'parameters': parameters_data,
                   'metadata': metadata_data
                   }]


if __name__ == '__main__':
    np.set_printoptions(suppress=True)
    print('Testing gt3x importer')

    # Epoch separated data
    [info, my_dict] = gt3x_importer('test.gt3x')

    activity = np.concatenate(my_dict['activity'])
    print('final shape:', activity.shape)

    # print('info:', info)
    # print('data:', data)

    #taken from the example
    # rawdata = bytearray.fromhex('00 60 08 EB D0 07 00 9E BF 00 70 08 EB F0')
    # print('len rawdata:', len(rawdata))
    # samples = gt3x_read_uint12(rawdata,3)
    # print('samples:', samples)
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWidgets import QMainWindow
    from libopenimu.qt.Charts import IMUChartView
    from PyQt5.QtCore import Qt
    from numpy import linspace

    app = QApplication(sys.argv)


    # Accelerometers
    window = QMainWindow()
    imuView = IMUChartView(window)
    imuView.add_data(activity[:, 0], activity[:, 1], Qt.green, 'Accelerometer Y')
    imuView.add_data(activity[:, 0], activity[:, 2], Qt.red, 'Accelerometer X')
    imuView.add_data(activity[:, 0], activity[:, 3], Qt.blue, 'Accelerometer Z')

    window.setCentralWidget(imuView)
    window.setWindowTitle("Actigraph GTX3 Importer Demo (Accelerometers)")
    window.resize(640, 480)
    window.show()

    # Battery
    window2 = QMainWindow()
    imuView2 = IMUChartView(window)
    battery = np.concatenate(my_dict['battery'])
    print('final shape:', battery.shape)
    imuView2.add_data(battery[:, 0], battery[:, 1], Qt.green, 'Battery')


    window2.setCentralWidget(imuView2)
    window2.setWindowTitle("Actigraph GTX3 Importer Demo (Battery)")
    window2.resize(640, 480)
    window2.show()


    # Lux
    window3 = QMainWindow()
    imuView3 = IMUChartView(window)
    lux = np.concatenate(my_dict['lux'])
    print('final shape:', lux.shape)
    imuView3.add_data(lux[:, 0], lux[:, 1], Qt.green, 'Lux')


    window3.setCentralWidget(imuView3)
    window3.setWindowTitle("Actigraph GTX3 Importer Demo (lux)")
    window3.resize(640, 480)
    window3.show()


    sys.exit(app.exec_())

