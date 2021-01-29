"""
This is a prototype Actigraph data importer.
Documentation of the binary format : https://github.com/actigraph/GT3X-File-Format (for newer devices)

@author Dominic Létourneau
"""

# Everything needed for zip
import zipfile
import struct
import numpy as np
import math
import sys
from libopenimu.tools.timing import timing


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


class ParameterKeys:
    """
    All Parameters keys
    """

    # Important constants for conversion
    class Conversion:
        FLOAT_MINIMUM = np.double(0.00000011920928955078125)
        FLOAT_MAXIMUM = np.double(8388608.0)
        ENCODED_MINIMUM = np.uint32(0x00800000)
        ENCODED_MAXIMUM = np.uint32(0x007FFFFF)
        SIGNIFICAND_MASK = np.uint32(0x00FFFFFF)
        EXPONENT_MINIMUM = np.int32(-128)
        EXPONENT_MAXIMUM = np.int32(127)
        EXPONENT_MASK = np.uint32(0xFF000000)
        EXPONENT_OFFSET = np.int32(24)

    # ADDRESS_SPACE = 0x0000
    BATTERY_STATE = 0x00060000
    BATTERY_VOLTAGE = 0x00070000
    BOARD_REVISION = 0x00080000
    CALIBRATION_TIME = 0x00090000
    FIRMWARE_VERSION = 0x000D0000
    MEMORY_SIZE = 0x00100000
    FEATURE_CAPABILITIES = 0x001C0000
    DISPLAY_CAPABILITIES = 0x001D0000
    WIRELESS_FIRMWARE_VERSION = 0x00200000
    IMU_ACCEL_SCALE = 0x00310000
    IMU_GYRO_SCALE = 0x00320000
    IMU_MAG_SCALE = 0x00330000
    ACCEL_SCALE = 0x00370000
    IMU_TEMP_SCALE = 0x00390000
    IMU_TEMP_OFFSET = 0x003A0000

    # ADDRESS_SPACE = 0x0001
    WIRELESS_MODE = 0x00000001
    WIRELESS_SERIAL_NUMBER = 0x00010001
    FEATURE_ENABLE = 0x00020001
    DISPLAY_CONFIGURATION = 0x00030001
    NEGATIVE_G_OFFSET_X = 0x00040001
    NEGATIVE_G_OFFSET_Y = 0x00050001
    NEGATIVE_G_OFFSET_Z = 0x00060001
    POSITIVE_G_OFFSET_X = 0x00070001
    POSITIVE_G_OFFSET_Y = 0x00080001
    POSITIVE_G_OFFSET_Z = 0x00090001
    SAMPLE_RATE = 0x000A0001
    TARGET_START_TIME = 0x000C0001
    TARGET_STOP_TIME = 0x000D0001
    TIME_OF_DAY = 0x000E0001
    ZERO_G_OFFSET_X = 0x000F0001
    ZERO_G_OFFSET_Y = 0x00100001
    ZERO_G_OFFSET_Z = 0x00110001
    HRM_SERIAL_NUMBER_H = 0x00140001
    HRM_SERIAL_NUMBER_L = 0x00150001
    PROXIMITY_INTERVAL = 0x00210001
    IMU_NEGATIVE_G_OFFSET_X = 0x00220001
    IMU_NEGATIVE_G_OFFSET_Y = 0x00230001
    IMU_NEGATIVE_G_OFFSET_Z = 0x00240001
    IMU_POSITIVE_G_OFFSET_X = 0x00250001
    IMU_POSITIVE_G_OFFSET_Y = 0x00260001
    IMU_POSITIVE_G_OFFSET_Z = 0x00270001
    UTC_OFFSET = 0x00280001
    IMU_ZERO_G_OFFSET_X = 0x00290001
    IMU_ZERO_G_OFFSET_Y = 0x002A0001
    IMU_ZERO_G_OFFSET_Z = 0x002B0001
    SENSOR_CONFIGURATION = 0x002C0001

    @staticmethod
    def decode_float(data):
        value = struct.unpack_from('<I', data)

        if ParameterKeys.Conversion.ENCODED_MAXIMUM == value:
            return sys.float_info.max
        elif ParameterKeys.Conversion.ENCODED_MINIMUM == value:
            return -sys.float_info.max

        # Exponent
        i32 = np.int32((value & ParameterKeys.Conversion.EXPONENT_MASK) >> ParameterKeys.Conversion.EXPONENT_OFFSET)
        if 0 != (i32 & 0x80):
            i32 |= 0xFFFFFF00
        exponent = np.double(i32)

        # Significand
        i32 = np.int32(value & ParameterKeys.Conversion.SIGNIFICAND_MASK)
        if 0 != (i32 & ParameterKeys.Conversion.ENCODED_MINIMUM):
            i32 |= 0xFF000000
        significand = np.double(i32 / ParameterKeys.Conversion.FLOAT_MAXIMUM)

        # Calculate the floating point value
        return significand * math.pow(2.0, exponent)

    @staticmethod
    def decode_uint32(data):
        # print('decode uint32')
        (value) = struct.unpack_from('<I', data)
        return value

    @staticmethod
    def decode_int32(data):
        # print('decode int32')
        (value) = struct.unpack_from('<i', data)
        return value

    @staticmethod
    def parameter_name(value):
        # print('dict:',ParameterKeys.__dict__)
        for v in ParameterKeys.__dict__:
            if ParameterKeys.__dict__[v] == value:
                return v
        return 'unknown'

    @staticmethod
    def decode_param(key, param_data):

        # Get the parameter name
        param_name = ParameterKeys.parameter_name(key)
        value = 0

        if key == ParameterKeys.BATTERY_STATE:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.BATTERY_VOLTAGE:
            value = ParameterKeys.decode_float(param_data)
        elif key == ParameterKeys.BOARD_REVISION:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.CALIBRATION_TIME:
            value = ParameterKeys.decode_uint32(param_data)
        elif key == ParameterKeys.FIRMWARE_VERSION:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.MEMORY_SIZE:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.FEATURE_CAPABILITIES:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.DISPLAY_CAPABILITIES:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.WIRELESS_FIRMWARE_VERSION:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.IMU_ACCEL_SCALE:
            value = ParameterKeys.decode_float(param_data)
        elif key == ParameterKeys.IMU_GYRO_SCALE:
            value = ParameterKeys.decode_float(param_data)
        elif key == ParameterKeys.IMU_MAG_SCALE:
            value = ParameterKeys.decode_float(param_data)
        elif key == ParameterKeys.ACCEL_SCALE:
            value = ParameterKeys.decode_float(param_data)
        elif key == ParameterKeys.IMU_TEMP_SCALE:
            value = ParameterKeys.decode_float(param_data)
        elif key == ParameterKeys.IMU_TEMP_OFFSET:
            value = ParameterKeys.decode_float(param_data)
        elif key == ParameterKeys.WIRELESS_MODE:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.WIRELESS_SERIAL_NUMBER:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.FEATURE_ENABLE:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.DISPLAY_CONFIGURATION:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.NEGATIVE_G_OFFSET_X:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.NEGATIVE_G_OFFSET_Y:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.NEGATIVE_G_OFFSET_Z:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.POSITIVE_G_OFFSET_X:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.POSITIVE_G_OFFSET_Y:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.POSITIVE_G_OFFSET_Z:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.SAMPLE_RATE:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.TARGET_START_TIME:
            value = ParameterKeys.decode_uint32(param_data)
        elif key == ParameterKeys.TARGET_STOP_TIME:
            value = ParameterKeys.decode_uint32(param_data)
        elif key == ParameterKeys.TIME_OF_DAY:
            value = ParameterKeys.decode_uint32(param_data)
        elif key == ParameterKeys.ZERO_G_OFFSET_X:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.ZERO_G_OFFSET_Y:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.ZERO_G_OFFSET_Z:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.HRM_SERIAL_NUMBER_H:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.HRM_SERIAL_NUMBER_L:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.PROXIMITY_INTERVAL:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.IMU_NEGATIVE_G_OFFSET_X:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.IMU_NEGATIVE_G_OFFSET_Y:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.IMU_NEGATIVE_G_OFFSET_Z:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.IMU_POSITIVE_G_OFFSET_X:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.IMU_POSITIVE_G_OFFSET_Y:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.IMU_POSITIVE_G_OFFSET_Z:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.UTC_OFFSET:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.IMU_ZERO_G_OFFSET_X:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.IMU_ZERO_G_OFFSET_Y:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.IMU_ZERO_G_OFFSET_Z:
            value = ParameterKeys.decode_int32(param_data)
        elif key == ParameterKeys.SENSOR_CONFIGURATION:
            value = ParameterKeys.decode_int32(param_data)
        else:
            print('Ignore key:', hex(key))

        if param_name == 'unknown':
            return {}
        else:
            return {param_name: value}


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

            # Fill data
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

    # Read all at once and scale in g units

    # This will generate double values
    # samples = gt3x_read_uint12(data) / scale

    # This will generate float values
    samples = gt3x_read_uint12(data) / np.float32(scale)

    # return samples in g
    return [timestamp, samples]


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
    return [timestamp, battery]


def gt3x_event_extractor(timestamp, data, samplerate):
    """

    :param data:
    :param samplerate:
    :return:
    """
    # print('Event Extractor',timestamp, data)
    return [timestamp, data]


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

    return [timestamp, np.int16(lux)]


def gt3x_capsense_extractor(timestamp, data, samplerate):
    """
    https://github.com/actigraph/GT3X-File-Format/blob/main/LogRecords/Capsense.md
    :param timestamp:
    :param data:
    :param samplerate:
    :return:
    """
    if len(data) is 6:
        [signal, reference, state, bursts] = struct.unpack_from('<HHBB', data)
        return [timestamp, np.uint16(signal), np.uint16(reference), np.uint8(state), np.uint8(bursts)]
    else:
        return [timestamp, [np.uint16(0), np.uint16(0), np.uint8(0), np.uint8(0)]]


def gt3x_metadata_extractor(timestamp, data, samplerate):
    """
    Should contain a json object

    :param data:
    :param samplerate:
    :return:
    """
    # print('Metadata Extractor', timestamp, data)
    # TODO Not yet implemented
    return [timestamp, data]


def gt3x_parameters_extractor(timestamp, data, samplerate):
    """
    The record payload is of variable length consisting of 8-byte key/value pairs. The key is made up of a 16-bit
    unsigned address space and 16-bit unsigned identifier. All values are encoded in a 32-bit unsigned integer.
    The address space, identifier and value are in little-endian byte order.

    https://github.com/actigraph/GT3X-File-Format/blob/master/LogRecords/Parameters.md
    :param data:
    :param samplerate:
    :return:
    """
    # print('Parameters Extractor', timestamp, data)

    result = {}

    # Each parameter is 8 bytes
    for param_index in range(0, int(len(data) / 8)):
        # unsigned int32, 4 bytes of data
        [key, param_data] = struct.unpack_from('<I4s', data, offset=param_index * 8)

        # update parameters result dict
        result.update(ParameterKeys.decode_param(key, param_data))

    return [timestamp, result]


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

    for record in record_data:
        checksum ^= record

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
    capsense_data = []

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
        print('info', info)
        # print('My Sample rate:', sample_rate)

        # Reading log.bin
        with myzip.open('log.bin') as myfile:
            filedata = myfile.read()
            print('filedata size', len(filedata), 'type:', type(filedata))
            data_offset = 0

            while data_offset < len(filedata):
                # print('data_offset:', data_offset)
                # < Little Endian, byte, byte, uint32, uint16
                [separator, record_type, timestamp, record_size] = struct.unpack_from('<BBIH', filedata, offset=data_offset)
                if separator is not 0x1e:
                    print('Separator Error!!!')

                # print('Extracting record: ', hex(separator), hex(record_type), hex(timestamp), hex(record_size))
                [record_data, checksum] = struct.unpack_from('<' + str(record_size) + 'sB', filedata, offset=data_offset + 8)

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
                    elif record_type is RecordType.CAPSENSE:
                        capsense_data.append(gt3x_capsense_extractor(timestamp, record_data, sample_rate))
                    else:
                        print('Unhandled record type:', hex(record_type), 'size:', len(record_data),
                              ' read ', data_offset, ' / ', len(filedata))
                else:
                    print('Checksum error read:', checksum, 'calculated:', cs_check, ' read ',
                          data_offset, ' / ', len(filedata))
                    print('Extracted record: ', hex(separator), hex(record_type), hex(timestamp), hex(record_size))

                # print('record length:', len(record_data), 'checksum:', hex(checksum))
                data_offset += 8 + len(record_data) + 1

    # Return file info and data contents
    return [info, {'activity': activity_data,
                   'battery': battery_data,
                   'lux': lux_data,
                   'capsense': capsense_data,
                   'event': event_data,
                   'parameters': parameters_data,
                   'metadata': metadata_data
                   }]




