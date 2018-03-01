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
    # print('Activity Extractor', 'size:', len(data), 'epoch size should be :', int(36 * samplerate / 8))

    # Initialize data to zero
    x_vec = np.zeros(int(samplerate))
    y_vec = np.zeros(int(samplerate))
    z_vec = np.zeros(int(samplerate))

    # Initialize bitstream
    stream = bitstring.BitStream(data)

    # This is really slow...
    if len(data) is int(36 * samplerate / 8):
        for index in range(0, int(samplerate)):
            y = np.uint16(stream.read('uint:12'))
            x = np.uint16(stream.read('uint:12'))
            z = np.uint16(stream.read('uint:12'))

            if x > 2047:
                x += np.uint16(61440)

            if y > 2047:
                y += np.uint16(61440)

            if z > 2047:
                z += np.uint16(61440)

            # Convert to signed values
            x = np.int16(x) / scale
            y = np.int16(y) / scale
            z = np.int16(z) / scale

            # Fill vector
            x_vec[index] = x
            y_vec[index] = y
            z_vec[index] = z
    else:
        print('Invalid size: ', 36 * samplerate / 8 )

    return [x_vec, y_vec, z_vec]


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

def gt3x_importer(filename):
    """

    The zipped file should contain two files info.txt and log.bin.

    :param filename: The gt3x file name
    :return: The data
    """
    print('Loading: ', filename)

    # Dict containing the information
    info = {}
    data = {}

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
                    scale = float(info['Acceleration Scale'])
                    [x, y, z] = gt3x_activity_extractor(record_data, sample_rate, scale)
                    # print('lengths', len(x), len(y), len(z))

                elif record_type is RecordType.BATTERY:
                    gt3x_battery_extractor(record_data, sample_rate)
                elif record_type is RecordType.EVENT:
                    gt3x_event_extractor(record_data, sample_rate)
                elif record_type is RecordType.LUX:
                    gt3x_lux_extractor(record_data, sample_rate)
                elif record_type is RecordType.METADATA:
                    gt3x_metadata_extractor(data, sample_rate)
                elif record_type is RecordType.PARAMETERS:
                    gt3x_parameters_extractor(data, sample_rate)
                else:
                    print('Unhandled record type:', hex(record_type), 'size:', len(record_data))

                # print('record length:', len(record_data), 'checksum:', hex(checksum))
                data_offset += 8 + len(record_data) + 1




    # Return file info and data contents
    return [info, data]


if __name__ == '__main__':
    print('Testing gt3x importer')
    [info, data] = gt3x_importer('test.gt3x')
    print('info:', info)
    print('data:', data)
    print('Done!')
