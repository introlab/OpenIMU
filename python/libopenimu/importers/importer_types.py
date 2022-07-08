import numpy as np
import struct


class ImporterTypes:
    # WIMU2 = 0
    UNKNOWN = -1
    WIMU = 0
    ACTIGRAPH = 1
    OPENIMU = 2
    APPLEWATCH = 3

    value_types = [WIMU, ACTIGRAPH, OPENIMU, APPLEWATCH]
    value_names = ['WIMU', 'Actigraph', 'OpenIMU', 'AppleWatch']

    @staticmethod
    def detect_type_from_file(filename: str) -> (int, str):
        file_extension = filename.split('.')
        # TODO: Use more than file extension for more reliable identification...
        if file_extension:
            # Identify file with extension
            file_extension = file_extension[-1]  # Last part of the filename
            if file_extension.lower() == 'gt3x' or file_extension.lower() == 'gtx':
                file_type = ImporterTypes.ACTIGRAPH
                return file_type, ImporterTypes.value_names[file_type]

            if file_extension.lower() == 'oimu':
                file_type = ImporterTypes.OPENIMU
                return file_type, ImporterTypes.value_names[file_type]

            if file_extension.lower() == 'data':
                file_type = ImporterTypes.APPLEWATCH
                return file_type, ImporterTypes.value_names[file_type]

        return ImporterTypes.UNKNOWN, ''


class BeaconData:
    tx_power = 0
    rssi = 0

    def from_bytes(self, data, offset=0):

        [self.tx_power] = struct.unpack_from('>b', data, offset=0)
        [self.rssi] = struct.unpack_from('>b', data, offset=1)

        return True

    def __str__(self):
        return "Beacon TX Power: %s, RSSI %s" % (str(self.tx_power), str(self.rssi))

    # Same interface as numpy vectors for serialization
    def tobytes(self):
        data = np.zeros(2, dtype=np.int8)
        struct.pack_into('>b', data, 0, int(self.tx_power))
        struct.pack_into('>b', data, 1, int(self.rssi))
        return data
