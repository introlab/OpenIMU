"""
This is a prototype Actigraph data importer.
Documentation of the binary format : https://github.com/actigraph/GT3X-File-Format (for newer devices)

@author Dominic Létourneau
"""

# Everything needed for zip
import zipfile
import struct
import numpy as np
import bitstring
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

        #print('before: ', byte_index)
        before = byte_index

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

def gt3x_activity_extractor(data, samplerate, scale):
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
    :param samplerate:
    :return:
    """

    # Read all at once and scale
    samples = gt3x_read_uint12(data) / scale
    # print('samples:', samples)

    # return samples in g
    return samples

def gt3x_battery_extractor(data, samplerate):
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

    return battery

def gt3x_event_extractor(data, samplerate):
    """

    :param data:
    :param samplerate:
    :return:
    """
    # print('Event Extractor')


def gt3x_lux_extractor(data, samplerate):
    """

    :param data:
    :param samplerate:
    :return:
    """
    # print('Lux Extractor')


def gt3x_metadata_extractor(data, samplerate):
    """

    :param data:
    :param samplerate:
    :return:
    """
    # print('Metadata Extractor')


def gt3x_parameters_extractor(data, samplerate):
    """

    :param data:
    :param samplerate:
    :return:
    """
    # print('Metadata Extractor')

@timing
def gt3x_importer(filename):
    """

    The zipped file should contain two files info.txt and log.bin.

    :param filename: The gt3x file name
    :return: The data
    """
    print('Loading: ', filename)

    # Dict containing the information
    info = {}

    activity_data = []

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
        print('My Sample rate:', sample_rate)

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

                # TODO verify checksum
                """
                byte chkSum = Header.Sync;
                chkSum ^= Header.Type;
                var timestamp = DeviceUtilities.DateTime.ToUnixTime(Header.TimeStamp);
                chkSum ^= (byte)(timestamp & 0xFF);
                chkSum ^= (byte)((timestamp >> 8) & 0xFF);
                chkSum ^= (byte)((timestamp >> 16) & 0xFF);
                chkSum ^= (byte)((timestamp >> 24) & 0xFF);
                chkSum ^= (byte)(Header.Size & 0xFF);
                chkSum ^= (byte)((Header.Size >> 8) & 0xFF);
                for (int i = 0; i < Payload.Length; ++i)
                    chkSum ^= Payload[i];
                chkSum = (byte)~chkSum;
                """

                if record_type is RecordType.ACTIVITY:
                    activity_data.append(gt3x_activity_extractor(record_data, sample_rate, scale))
                    # print('skipping activity, too long...')
                    # print('lengths', len(x), len(y), len(z))
                    #print('shape:', activity_data.shape)

                elif record_type is RecordType.BATTERY:
                    gt3x_battery_extractor(record_data, sample_rate)
                elif record_type is RecordType.EVENT:
                    gt3x_event_extractor(record_data, sample_rate)
                elif record_type is RecordType.LUX:
                    gt3x_lux_extractor(record_data, sample_rate)
                elif record_type is RecordType.METADATA:
                    gt3x_metadata_extractor(record_data, sample_rate)
                elif record_type is RecordType.PARAMETERS:
                    gt3x_parameters_extractor(record_data, sample_rate)
                else:
                    print('Unhandled record type:', hex(record_type), 'size:', len(record_data))

                # print('record length:', len(record_data), 'checksum:', hex(checksum))
                data_offset += 8 + len(record_data) + 1


    print('activity_data len:',len(activity_data))

    # Return file info and data contents
    return [info, activity_data]


if __name__ == '__main__':
    print('Testing gt3x importer')

    # Epoch separated data
    [info, data] = gt3x_importer('test.gt3x')

    result = np.concatenate(data)
    print('final shape:', result.shape, 'info:', info)

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

    time = linspace(0,len(result) / 30.0,len(result))
    print('time size:', len(time))

    app = QApplication(sys.argv)
    window = QMainWindow()
    imuView = IMUChartView(window)
    # imuView.add_test_data()
    imuView.add_data(time, result[:, 0], Qt.green, 'Accelerometer Y')
    imuView.add_data(time, result[:, 1], Qt.red, 'Accelerometer X')
    imuView.add_data(time, result[:, 2], Qt.blue, 'Accelerometer Z')

    window.setCentralWidget(imuView)
    window.setWindowTitle("Actigraph GTX3 Importer Demo")
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())

