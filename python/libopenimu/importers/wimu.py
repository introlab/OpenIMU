from libopenimu.tools.timing import timing

import os
import zipfile
import struct
import numpy as np
import math


class WIMUConfig_DateTimeOptions:
    time_offset = np.uint16(0)
    enable_gps_time = False
    enable_auto_offset = False


class WIMUConfig_UIOptions:
    led_blink_time = np.uint8(0)
    write_led = False
    enable_marking = False
    gps_fix_led = False
    ble_activity_led = False


class WIMUConfig_GlobalOptions:
    sampling_rate = np.uint16(0)
    enable_watchdog = False


class WIMUConfig_LoggerOptions:
    max_files_in_folder = np.uint8(0)
    split_by_day = False


class WIMUConfig_GPSOptions:
    interval = np.uint8(0)
    force_cold = False
    enable_scan_when_charged = False


class WIMUConfig_PowerOptions:
    power_manage = False
    enable_motion_detection = False
    adv_power_manage = False


class WIMUConfig_BLEOptions:
    enable_control = False


class WIMUConfig_AccOptions:
    range = np.uint8(0)


class WIMUConfig_GyroOptions:
    range = np.uint8(0)


class WIMUConfig_MagOptions:
    range = np.uint8(0)


class WIMUConfig_IMUOptions:
    beta = np.float(0.0)
    disable_magneto = False
    auto_calib_gyro = False



class WIMUConfig:
    datetime = WIMUConfig_DateTimeOptions()
    ui = WIMUConfig_UIOptions()
    general = WIMUConfig_GlobalOptions()
    logger = WIMUConfig_LoggerOptions()
    gps = WIMUConfig_GPSOptions()
    power = WIMUConfig_PowerOptions()
    ble = WIMUConfig_BLEOptions()
    acc = WIMUConfig_AccOptions()
    gyro = WIMUConfig_GyroOptions()
    magneto = WIMUConfig_MagOptions()
    imu = WIMUConfig_IMUOptions()
    enabled_modules = np.uint16(0)
    crc = np.uint32(0)

    def from_bytes(self, data, hw_id=2):
        print('WIMUConfig.from_bytes', len(data))
        if hw_id == 2:
            buf16 = np.uint16(0)
            buf8 = np.uint8(0)

            # Unsigned int
            self.enabled_modules = struct.unpack_from('<I', data, offset=0)

            # Unsigned short
            buf16 = struct.unpack_from('<H', data, offset=4)

            # Unsigned char, CPU Options
            buf8 = struct.unpack_from('<B', data, offset=6)

            if np.bitwise_and(buf8, 0x01):
                self.general.enable_watchdog = True

            if np.bitwise_and(buf8, 0x02):
                self.general.sampling_rate = 100
            else:
                self.general.sampling_rate = 50

            self.ui.led_blink_time = np.bitwise_and(buf8, 0x7c) >> 2

            print('general.enable_watchdog', self.general.enable_watchdog)
            print('general.sampling_rate', self.general.sampling_rate)
            print('ui.led_blink_time', self.ui.led_blink_time)

            # Unsigned char, Log filetime
            buf8 = struct.unpack_from('<B', data, offset=7)

            # Unsigned char, Log reset time
            buf8 = struct.unpack_from('<B', data, offset=8)

            # Unsigned char, Logger options
            buf8 = struct.unpack_from('<B', data, offset=9)

            if np.bitwise_and(buf8, 0x01):
                self.ui.write_led = True

            if np.bitwise_and(buf8, 0x02):
                self.ui.enable_marking = True

            if np.bitwise_and(buf8, 0x04):
                self.logger.split_by_day = True

            self.datetime.time_offset = np.bitwise_and(buf8, 0xF7) >> 3
            if np.bitwise_and(buf8, 0x80):
                self.datetime.time_offset = -self.datetime.time_offset

            print('self.ui.write_led', self.ui.write_led)
            print('self.ui.enable_marking', self.ui.enable_marking)
            print('self.logger.split_by_day', self.logger.split_by_day)
            print('self.datetime.time_offset', self.datetime.time_offset)

            # GPS dead time
            buf8 = struct.unpack_from('<B', data, offset=10)

            # GPS Degrad time
            buf8 = struct.unpack_from('<B', data, offset=11)

            # GPS Deadrec time
            buf8 = struct.unpack_from('<B', data, offset=12)

            # GPS options
            buf8 = struct.unpack_from('<B', data, offset=13)
            if np.bitwise_and(buf8, 0x08):
                self.gps.force_cold = True

            print('self.gps.force_cold',self.gps.force_cold)

            # Power options
            buf8 = struct.unpack_from('<B', data, offset=14)

            # Zigbee options
            buf8 = struct.unpack_from('<B', data, offset=15)

            # Acc range
            self.acc.range = struct.unpack_from('<B', data, offset=16)
            self.gyro.range = struct.unpack_from('<B', data, offset=17)
            self.magneto.range = struct.unpack_from('<B', data, offset=18)

            print('self.acc.range', self.acc.range)
            print('self.gyro.range', self.gyro.range)
            print('self.magneto.range', self.magneto.range)

            # Ignore the rest...

        else:
            pass

@timing
def wimu_load_settings(data):
    """
    QDataStream ds(*data);
    ds.setByteOrder(QDataStream::LittleEndian);

    ds >> id;
    ds >> hw_id;

    if (hw_id==3){
        ds >> version_major;
        ds >> version_minor;
        ds >> version_rev;
    }else{
        // WIMUv2
        version_major = 2;
        version_minor = 0;
        version_rev = 0;
    }

    for (int i=0; i<3; i++)
        ds >> acc_gain[i];
    for (int i=0; i<3; i++)
        ds >> acc_offset[i];
    for (int i=0; i<3; i++)
        ds >> gyro_gain[i];
    for (int i=0; i<3; i++)
        ds >> gyro_offset[i];
    for (int i=0; i<3; i++)
        ds >> mag_gain[i];
    for (int i=0; i<3; i++)
        ds >> mag_offset[i];

    if (hw_id==2){
        //WIMUv2 unused bytes
        quint8 old_byte;
        for (int i=0; i<7; i++){
            ds >> old_byte;
        }
    }
    ds >> crc;

    quint16 id;             // Serial Number
    quint8 hw_id; 			// Hardware revision ID
    quint8 version_major;   // Version Number
    quint8 version_minor;
    quint8 version_rev;
    qint16 acc_gain[3];     // Accelerometers gain
    qint16 acc_offset[3];   // Accelerometers offset
    qint16 gyro_gain[3];    // Gyroscope gain
    qint16 gyro_offset[3];  // Gyroscope offset
    qint16 mag_gain[3];     // Magnetometers gain
    qint16 mag_offset[3];   // Magnetometers offset
    quint32 crc;


    :param data:
    :return:
    """
    print('settings reading length: ', len(data))

    result = {}

    # data_offset = 0

    # unsigned short, unsigned char
    [id, hw_id] = struct.unpack_from('<HB', data, offset=0)

    version_major = 0
    version_minor = 0
    version_rev = 0
    acc_gain = [0, 0, 0]
    acc_offset = [0, 0, 0]
    gyro_gain = [0, 0, 0]
    gyro_offset = [0, 0, 0]
    mag_gain = [0, 0, 0]
    mag_offset = [0, 0, 0]
    crc = 0

    if hw_id == 3:
        pass
    else:
        version_major = 2
        version_minor = 0
        version_rev = 0
        # Read gains, offsets (3x signed short)
        acc_gain[0], acc_gain[1], acc_gain[2] = struct.unpack_from('<hhh', data, offset=3)
        acc_offset[0], acc_offset[1], acc_offset[2] = struct.unpack_from('<hhh', data, offset=9)

        gyro_gain[0], gyro_gain[1], gyro_gain[2] = struct.unpack_from('<hhh', data, offset=15)
        gyro_offset[0], gyro_offset[1], gyro_offset[2] = struct.unpack_from('<hhh', data, offset=21)

        mag_gain[0], mag_gain[1], mag_gain[2] = struct.unpack_from('<hhh', data, offset=27)
        mag_offset[0], mag_offset[1], mag_offset[2] = struct.unpack_from('<hhh', data, offset=33)

        # Read 7 unused bytes
        struct.unpack_from('<BBBBBBB', data, offset=39)

        # Read CRC (unsigned int)
        crc = struct.unpack_from('<I', data, offset=46)

    # Fill results
    result['id'] = id
    result['hw_id'] = hw_id
    result['version_major'] = version_major
    result['version_minor'] = version_minor
    result['version_rev'] = version_rev
    result['acc_gains'] = acc_gain
    result['acc_offsets'] = acc_offset
    result['gyro_gains'] = gyro_gain
    result['gyro_offsets'] = gyro_offset
    result['mag_gains'] = mag_gain
    result['mag_offsets'] = mag_offset
    # Useless CRC for now
    # result['crc'] = crc

    print('settings', result)
    return result

@timing
def wimu_load_config(data, hw_id =2):
    """

    :param data:
    :return:



    """
    config = WIMUConfig()
    config.from_bytes(data, hw_id)
    return {'config': config}

@timing
def wimu_load_acc(time_data, acc_data):
    pass

@timing
def wimu_load_gps(time_data, index_data, gps_data):
    pass

@timing
def wimu_load_gyro(time_data, gyro_data):
    pass

@timing
def wimu_load_pow(time_data, pow_data):
    pass

@timing
def wimu_load_log(time_data, log_data):
    pass

@timing
def wimu_importer(filename):
    if not os.path.isfile(filename):
        print('file not found')
        return None

    print('wimu_importer processing', filename)
    result = {}

    with zipfile.ZipFile(filename) as myzip:
        print('zip opened')
        namelist = myzip.namelist()

        # First read settings file
        if namelist.__contains__('PreProcess/SETTINGS'):
            settings = wimu_load_settings(myzip.open('PreProcess/SETTINGS').read())
            result['settings'] = settings

        else:
            return None

        # Then read config file
        if namelist.__contains__('PreProcess/CONFIG.WCF'):
            config = wimu_load_config(myzip.open('PreProcess/CONFIG.WCF').read())
            result['config'] = config
        else:
            return None

        return result

        # Must have matching pairs with VALUES /TIME
        filedict = {}

        # First pass extract files with no TIME
        for file in namelist:
            # print('listing:', file)
            if '.DAT' in file:
                if '/ACC_' in file:
                    filedict[file] = []
                elif '/GYR_' in file:
                    filedict[file] = []
                elif '/POW_' in file:
                    filedict[file] = []
                elif '/GPS_' in file:
                    filedict[file] = []
                elif '/LOG_' in file:
                    filedict[file] = []
                else:
                    pass
                    # print('not handling:', file)
            else:
                pass
                # print('removing:', file)
                # Not interested in other files
                # namelist.remove(file)

        for file in namelist:
            if '.DAT' in file:
                if 'TIME_' in file:
                    key = file.replace('TIME_', "")
                    if filedict.__contains__(key):
                        filedict[key].append(file)
                    else:
                        print('key error', key)
                if 'INDEX_' in file:
                    key = file.replace('INDEX_', "")
                    if filedict.__contains__(key):
                        filedict[key].append(file)
                    else:
                        print('key error', key)

        # now process data if everything is ok
        for key in filedict:
            # print(key, filedict[key])
            if 'ACC' in key:
                if len(filedict[key]) == 1:
                    acc_data = myzip.open(key).read()
                    time_data = myzip.open(filedict[key][0]).read()
                    wimu_load_acc(time_data, acc_data)
                else:
                    print('error ACC')
            elif 'GYR' in key:
                if len(filedict[key]) == 1:
                    gyro_data = myzip.open(key).read()
                    time_data = myzip.open(filedict[key][0]).read()
                    wimu_load_gyro(time_data, gyro_data)
                else:
                    print('error GYRO')
            elif 'GPS' in key:
                if len(filedict[key]) == 2:
                    gps_data = myzip.open(key).read()
                    index_data = myzip.open(filedict[key][0]).read()
                    time_data = myzip.open(filedict[key][1]).read()
                    wimu_load_gps(time_data, index_data, gps_data)
                else:
                    print('error GPS')
            elif 'POW' in key:
                if len(filedict[key]) == 1:
                    pow_data = myzip.open(key).read()
                    time_data = myzip.open(filedict[key][0]).read()
                    wimu_load_pow(time_data, pow_data)
                else:
                    print('error POW')
            elif 'LOG' in key:
                if len(filedict[key]) == 1:
                    log_data = myzip.open(key).read()
                    time_data = myzip.open(filedict[key][0]).read()
                    wimu_load_log(time_data, log_data)
                else:
                    print('error LOG')
            else:
                print('unhandled key', key)

    return result


# Testing app
if __name__ == '__main__':
    result = wimu_importer('../../resources/samples/WIMU_ACC_GPS_GYRO_PreProcess.zip')
    print(result)