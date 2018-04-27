from libopenimu.tools.timing import timing

import os
import zipfile
import struct
import numpy as np
import math

@timing
def wimu_load_settings(data):
    pass

@timing
def wimu_load_config(data):
    pass

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

    with zipfile.ZipFile(filename) as myzip:
        print('zip opened')
        namelist = myzip.namelist()

        # First read config file
        if namelist.__contains__('PreProcess/CONFIG.WCF'):
            wimu_load_config(myzip.open('PreProcess/CONFIG.WCF').read())
        else:
            return None

        if namelist.__contains__('PreProcess/SETTINGS'):
            wimu_load_settings(myzip.open('PreProcess/SETTINGS').read())
        else:
            return None

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


# Testing app
if __name__ == '__main__':
    result = wimu_importer('../../resources/samples/WIMU_ACC_GPS_GYRO_PreProcess.zip')