from libopenimu.tools.timing import timing

import os
import zipfile
import struct
import numpy as np
import math


class WIMUSettings:
    # Serial Number
    id = np.uint16(0)
    # Hardware revision id
    hw_id = np.uint8(0)
    # Version number
    version_major = np.uint8(0)
    version_minor = np.uint8(0)
    version_rev = np.uint8(0)
    # Acc gains and offsets
    acc_gain = [np.int16(0), np.int16(0), np.int16(0)]
    acc_offset = [np.int16(0), np.int16(0), np.int16(0)]
    # Gyro gains and offsets
    gyro_gain = [np.int16(0), np.int16(0), np.int16(0)]
    gyro_offset = [np.int16(0), np.int16(0), np.int16(0)]
    # Magneto gains and offsets
    mag_gain = [np.int16(0), np.int16(0), np.int16(0)]
    mag_offset = [np.int16(0), np.int16(0), np.int16(0)]
    # CRC
    crc = np.uint32(0)

    def __str__(self):
        my_dict = {}
        my_dict['id'] = self.id
        my_dict['hw_id'] = self.hw_id
        my_dict['version_major'] = self.version_major
        my_dict['version_minor'] = self.version_minor
        my_dict['version_rev'] = self.version_rev
        my_dict['acc_gain'] = self.acc_gain
        my_dict['acc_offset'] = self.acc_offset
        my_dict['gyro_gain'] = self.acc_gain
        my_dict['gyro_offset'] = self.acc_offset
        my_dict['mag_gain'] = self.acc_gain
        my_dict['mag_offset'] = self.acc_offset
        my_dict['crc'] = self.crc
        return str([self.__class__.__name__, my_dict])

    def from_bytes(self, data):
        # unsigned short, unsigned char
        [self.id, self.hw_id] = struct.unpack_from('<HB', data, offset=0)

        if self.hw_id == 3:
            print('error hw_id not supported:', self.hw_id)
            return
        else:
            assert(len(data) == 50)
            self.version_major = 2
            self.version_minor = 0
            self.version_rev = 0
            # Read gains, offsets (3x signed short)
            self.acc_gain[0], self.acc_gain[1], self.acc_gain[2] = struct.unpack_from('<hhh', data, offset=3)
            self.acc_offset[0], self.acc_offset[1], self.acc_offset[2] = struct.unpack_from('<hhh', data, offset=9)

            self.gyro_gain[0], self.gyro_gain[1], self.gyro_gain[2] = struct.unpack_from('<hhh', data, offset=15)
            self.gyro_offset[0], self.gyro_offset[1], self.gyro_offset[2] = struct.unpack_from('<hhh', data, offset=21)

            self.mag_gain[0], self.mag_gain[1], self.mag_gain[2] = struct.unpack_from('<hhh', data, offset=27)
            self.mag_offset[0], self.mag_offset[1], self.mag_offset[2] = struct.unpack_from('<hhh', data, offset=33)

            # Read 7 unused bytes
            struct.unpack_from('<BBBBBBB', data, offset=39)

            # Read CRC (unsigned int)
            self.crc = struct.unpack_from('<I', data, offset=46)


class DateTimeOptions:
    time_offset = np.uint16(0)
    enable_gps_time = False
    enable_auto_offset = False

    def __str__(self):
        return str([self.__class__.__name__,  {'time_offset':self.time_offset, 'enable_gps_time':self.enable_gps_time,
                                               'enable_auto_offset': self.enable_auto_offset}])


class UIOptions:
    led_blink_time = np.uint8(0)
    write_led = False
    enable_marking = False
    gps_fix_led = False
    ble_activity_led = False

    def __str__(self):
        return str([self.__class__.__name__, {'led_blink_time': self.led_blink_time, 'write_led': self.write_led,
                                              'enable_marking': self.enable_marking, 'gps_fix_led': self.gps_fix_led,
                                              'ble_activity_led': self.ble_activity_led}])


class GlobalOptions:
    sampling_rate = np.uint16(0)
    enable_watchdog = False

    def __str__(self):
        return str([self.__class__.__name__, {'sampling_rate': self.sampling_rate,
                                              'enable_watchdog': self.enable_watchdog}])


class LoggerOptions:
    max_files_in_folder = np.uint8(0)
    split_by_day = False

    def __str__(self):
        return str([self.__class__.__name__, {'max_files_in_folder': self.max_files_in_folder,
                                              'split_by_day': self.split_by_day}])


class GPSOptions:
    interval = np.uint8(0)
    force_cold = False
    enable_scan_when_charged = False

    def __str__(self):
        return str([self.__class__.__name__, {'interval': self.interval, 'force_cold': self.force_cold,
                                              'enable_scan_when_charged': self.enable_scan_when_charged}])


class PowerOptions:
    power_manage = False
    enable_motion_detection = False
    adv_power_manage = False

    def __str__(self):
        return str([self.__class__.__name__, {'power_manage': self.power_manage,
                                              'enable_motion_detection': self.enable_motion_detection,
                                              'adv_power_manage': self.adv_power_manage}])


class BLEOptions:
    enable_control = False

    def __str__(self):
        return str([self.__class__.__name__, {'enable_control': self.enable_control}])


class AccOptions:
    range = np.uint8(0)

    def __str__(self):
        return str([self.__class__.__name__, {'range': self.range}])


class GyroOptions:
    range = np.uint8(0)

    def __str__(self):
        return str([self.__class__.__name__, {'range': self.range}])


class MagOptions:
    range = np.uint8(0)

    def __str__(self):
        return str([self.__class__.__name__, {'range': self.range}])


class IMUOptions:
    beta = np.float(0.0)
    disable_magneto = False
    auto_calib_gyro = False

    def __str__(self):
        return str([self.__class__.__name__, {'beta': self.beta, 'disable_magneto': self.disable_magneto,
                                              'auto_calib_gyro': self.auto_calib_gyro}])


class WIMUConfig:
    datetime = DateTimeOptions()
    ui = UIOptions()
    general = GlobalOptions()
    logger = LoggerOptions()
    gps = GPSOptions()
    power = PowerOptions()
    ble = BLEOptions()
    acc = AccOptions()
    gyro = GyroOptions()
    magneto = MagOptions()
    imu = IMUOptions()
    enabled_modules = np.uint16(0)
    crc = np.uint32(0)
    WIMUSettings = WIMUSettings()

    def __str__(self):
        my_dict = {}
        my_dict['datetime'] = str(self.datetime)
        my_dict['ui'] = str(self.ui)
        my_dict['general'] = str(self.general)
        my_dict['logger'] = str(self.logger)
        my_dict['gps'] = str(self.gps)
        my_dict['power'] = str(self.power)
        my_dict['ble'] = str(self.ble)
        my_dict['acc'] = str(self.acc)
        my_dict['gyro'] = str(self.gyro)
        my_dict['magneto'] = str(self.magneto)
        my_dict['imu'] = str(self.imu)
        my_dict['enabled_modules'] = str(self.enabled_modules)
        my_dict['crc'] = str(self.crc)
        return str([__class__.__name__, my_dict])

    def from_bytes(self, data, hw_id=2):
        # print('WIMUConfig.from_bytes', len(data))
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

            # print('general.enable_watchdog', self.general.enable_watchdog)
            # print('general.sampling_rate', self.general.sampling_rate)
            # print('ui.led_blink_time', self.ui.led_blink_time)

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

            # print('self.ui.write_led', self.ui.write_led)
            # print('self.ui.enable_marking', self.ui.enable_marking)
            # print('self.logger.split_by_day', self.logger.split_by_day)
            # print('self.datetime.time_offset', self.datetime.time_offset)

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

            # print('self.gps.force_cold',self.gps.force_cold)

            # Power options
            buf8 = struct.unpack_from('<B', data, offset=14)

            # Zigbee options
            buf8 = struct.unpack_from('<B', data, offset=15)

            # Acc range
            self.acc.range = struct.unpack_from('<B', data, offset=16)
            self.gyro.range = struct.unpack_from('<B', data, offset=17)
            self.magneto.range = struct.unpack_from('<B', data, offset=18)

            # print('self.acc.range', self.acc.range)
            # print('self.gyro.range', self.gyro.range)
            # print('self.magneto.range', self.magneto.range)

            # Ignore the rest...

        else:
            pass


@timing
def wimu_load_settings(data):
    settings = WIMUSettings()
    settings.from_bytes(data)
    print(settings)
    return settings


@timing
def wimu_load_config(data, settings: WIMUSettings):
    config = WIMUConfig()
    config.from_bytes(data, settings.hw_id)
    config.settings = settings
    print(config)
    return config


@timing
def wimu_load_acc(time_data, acc_data, config: WIMUConfig):
    pass


@timing
def wimu_load_gps(time_data, index_data, gps_data, config: WIMUConfig):
    pass


@timing
def wimu_load_gyro(time_data, gyro_data, config: WIMUConfig):
    pass


@timing
def wimu_load_pow(time_data, pow_data, config: WIMUConfig):
    pass


@timing
def wimu_load_log(time_data, log_data, config: WIMUConfig):
    pass


@timing
def wimu_importer(filename):
    if not os.path.isfile(filename):
        print('file not found')
        return None

    print('wimu_importer processing', filename)
    results = {}

    with zipfile.ZipFile(filename) as myzip:
        print('zip opened')
        namelist = myzip.namelist()

        # First read settings file
        if namelist.__contains__('PreProcess/SETTINGS'):
            results['settings'] = wimu_load_settings(myzip.open('PreProcess/SETTINGS').read())
        else:
            return results

        # Then read config file
        if namelist.__contains__('PreProcess/CONFIG.WCF'):
            results['config'] = wimu_load_config(myzip.open('PreProcess/CONFIG.WCF').read(), results['settings'])
        else:
            return results

        print(str(results))
        return results

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