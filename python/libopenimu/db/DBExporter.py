from libopenimu.db.DBManager import DBManager
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QIcon

from libopenimu.models.Group import Group
from libopenimu.models.Participant import Participant
from libopenimu.models.Recordset import Recordset
from libopenimu.models.sensor_types import SensorType
from libopenimu.models.Sensor import Sensor
from libopenimu.models.SensorData import SensorData

import os
import csv
import scipy.io as sio
import numpy as np


class ExporterTypes:
    UNKNOWN = -1
    CSV = 0
    MATLAB = 1

    value_types = [CSV, MATLAB]
    value_names = ['CSV', 'Matlab']

    @staticmethod
    def get_icon_for_type(exporter_type_id: int) -> QIcon:
        if exporter_type_id == ExporterTypes.CSV:
            return QIcon(':/OpenIMU/icons/file_csv.png')

        if exporter_type_id == ExporterTypes.MATLAB:
            return QIcon(':/OpenIMU/icons/file_matlab.png')

        return QIcon()


class DBExporter(QObject):

    exportProcessed = Signal()

    def __init__(self, db_manager: DBManager, export_path: str, export_format: int, parent=None):
        QObject.__init__(self, parent=parent)

        self.dbMan = db_manager
        self.exportPath = export_path
        self.exportFormat = export_format

    @staticmethod
    def clean_string(to_clean: str) -> str:
        # Remove non-alphanumeric characters in string
        return ''.join(e for e in to_clean if e.isalnum())

    @staticmethod
    def dict_to_csv(filename: str, values: dict):
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=values.keys(), delimiter='\t', lineterminator='\n')
            writer.writeheader()
            writer.writerows([values])

    @staticmethod
    def dict_to_mat(filename: str, values: dict):
        # Remove None values
        for key in values.keys():
            if values[key] is None:
                values[key] = 0
            if isinstance(values[key], dict):
                values[key] = values[key] | {k: 0 for k in values[key].keys() if values[key][k] is None}

        sio.savemat(filename, values, do_compression=True, long_field_names=True)

    def get_base_path_for_group(self, group_name: str) -> str:
        return self.exportPath + os.sep + self.tr('GROUP') + '_' + DBExporter.clean_string(group_name)

    def get_base_path_for_participant(self, participant: Participant) -> str:
        if participant.group:
            part_dir = self.get_base_path_for_group(participant.group.name) + os.sep + \
                       DBExporter.clean_string(participant.name)
        else:
            part_dir = self.exportPath + os.sep + DBExporter.clean_string(participant.name)

        return part_dir

    def get_base_path_for_recordset(self, recordset: Recordset) -> str:
        return self.get_base_path_for_participant(recordset.participant) + os.sep + \
               DBExporter.clean_string(recordset.name)

    def export_group(self, id_group: int):
        group_name = self.tr('GROUP_None')
        group: Group | None = None
        if id_group >= 0:
            group = self.dbMan.get_group(id_group)
            if group:
                group_name = group.name

        if group_name:
            group_dir = self.get_base_path_for_group(group.name)
            if not os.path.exists(group_dir):
                os.mkdir(group_dir)

            if group:
                # Export group info in file
                group_info = {'id_group': group.id_group, 'name': group.name, 'description': group.description}
                if self.exportFormat == ExporterTypes.CSV:
                    DBExporter.dict_to_csv(group_dir + os.sep + 'infos_group.csv', group_info)
                if self.exportFormat == ExporterTypes.MATLAB:
                    DBExporter.dict_to_mat(group_dir + os.sep + 'infos_group.mat', {'group': group_info})

    def export_participant(self, id_participant: int):
        participant = self.dbMan.get_participant(id_participant)
        if participant:
            part_dir = self.get_base_path_for_participant(participant)

            if not os.path.exists(part_dir):
                os.mkdir(part_dir)

            # Export infos in file
            part_info = {'id_participant': participant.id_participant, 'name': participant.name,
                         'description': participant.description}
            if self.exportFormat == ExporterTypes.CSV:
                DBExporter.dict_to_csv(part_dir + os.sep + 'infos_participant.csv', part_info)
            if self.exportFormat == ExporterTypes.MATLAB:
                DBExporter.dict_to_mat(part_dir + os.sep + 'infos_participant.mat', {'participant': part_info})

    def export_recordset(self, id_recordset: int):
        recordset = self.dbMan.get_recordset(id_recordset)

        if recordset:
            rec_dir = self.get_base_path_for_recordset(recordset)

            if not os.path.exists(rec_dir):
                os.mkdir(rec_dir)

            # Export infos in file
            infos = {'id_recordset': recordset.id_recordset, 'name': recordset.name,
                     'start_time': str(recordset.start_timestamp), 'start_timestamp': recordset.start_timestamp.timestamp(),
                     'end_time': str(recordset.end_timestamp), 'end_timestamp': recordset.end_timestamp.timestamp()}
            if self.exportFormat == ExporterTypes.CSV:
                DBExporter.dict_to_csv(rec_dir + os.sep + 'infos_recordset.csv', infos)
            if self.exportFormat == ExporterTypes.MATLAB:
                DBExporter.dict_to_mat(rec_dir + os.sep + 'infos_recordset.mat', {'recordset': infos})

            # Process data in recordsets
            # Get all sensors
            sensors = self.dbMan.get_sensors(recordset)
            for sensor in sensors:
                # Do something
                all_data = self.dbMan.get_all_sensor_data(recordset=recordset, sensor=sensor)
                if sensor.id_sensor_type == SensorType.GPS:
                    self.export_sensor_data_gps(sensor, all_data, rec_dir)
                elif sensor.id_sensor_type == SensorType.BEACON:
                    self.export_sensor_data_beacons(sensor, all_data, rec_dir)
                else:
                    self.export_sensor_data(sensor, all_data, rec_dir)

    def export_sensor_data(self, sensor: Sensor, sensors_data: list[SensorData], base_dir: str):
        result = {}
        for sensor_data in sensors_data:
            if not result.__contains__(sensor_data.channel.id_channel):
                result[sensor_data.channel.id_channel] = []

            series = sensor_data.to_time_series()
            result[sensor_data.channel.id_channel].append(series)

        base_filename = sensor.location + '_' + sensor.name.replace(' ', '_')

        # Write sensor infos file
        self.export_sensor_infos(sensor, base_dir, base_filename)

        # Data files
        filename = base_dir + os.sep + base_filename
        if self.exportFormat == ExporterTypes.CSV:
            filename = filename + '.CSV'
        elif self.exportFormat == ExporterTypes.MATLAB:
            filename = filename + '.mat'

        value_list = []

        # Write header
        header = str()
        channels = self.dbMan.get_all_channels(sensor=sensor)
        for channel in channels:
            header = header + 'Time\t' + channel.label + '\t'

        for channel_key in result:
            time = []
            values = []
            for list_item in result[channel_key]:
                time.append(list_item['time'])
                values.append(list_item['values'])

            all_time = np.concatenate(time)
            all_values = np.concatenate(values)
            value_list.append(all_time)
            value_list.append(all_values)

        my_array = np.array(value_list)
        # print('dims:', my_array.shape)
        # Write values
        if self.exportFormat == ExporterTypes.CSV:
            np.savetxt(filename, my_array.transpose(), delimiter="\t", header=header)
        elif self.exportFormat == ExporterTypes.MATLAB:
            sio.savemat(filename, {sensor.name.replace(' ', ''): my_array.transpose(), 'labels': header.split('\t')},
                        do_compression=True, long_field_names=True)

    def export_sensor_data_gps(self, sensor: Sensor, sensors_data: list[SensorData], base_dir: str):
        # GPS is stored as SIRF data structures.
        from libopenimu.importers.wimu import GPSGeodetic

        base_filename = sensor.location + '_' + sensor.name.replace(' ', '_')

        # Write sensor infos file
        self.export_sensor_infos(sensor, base_dir, base_filename)

        filename = base_dir + os.sep + base_filename
        if self.exportFormat == ExporterTypes.CSV:
            filename = filename + '.CSV'
        elif self.exportFormat == ExporterTypes.MATLAB:
            filename = filename + '.mat'

        # Write header
        header = str()
        channels = self.dbMan.get_all_channels(sensor=sensor)

        # Create data array
        # WILL HANDLE ONLY ONE GPS CHANNEL FOR NOW
        my_array = np.zeros(shape=(len(sensors_data), 3))

        for channel in channels:
            header = header + 'TIME\t' + channel.label + '-Latitude\t' + channel.label + '-Longitude\t'

            for i in range(0, len(sensors_data)):
                gps_data = GPSGeodetic()
                gps_data.from_bytes(sensors_data[i].data)
                # Fill data
                my_array[i][0] = sensors_data[i].timestamps.start_timestamp.timestamp()
                my_array[i][1] = gps_data.get_latitude()
                my_array[i][2] = gps_data.get_longitude()

        # Save File
        # print('dims:', my_array.shape)
        # Write values
        if self.exportFormat == ExporterTypes.CSV:
            np.savetxt(filename, my_array, delimiter="\t", header=header)
        elif self.exportFormat == ExporterTypes.MATLAB:
            sio.savemat(filename, {sensor.name.replace(' ', '_'): my_array.transpose(), 'labels': header.split('\t')},
                        do_compression=True, long_field_names=True)

    def export_sensor_data_beacons(self, sensor: Sensor, sensors_data: list[SensorData], base_dir: str):
        result = {}
        for sensor_data in sensors_data:
            if not result.__contains__(sensor_data.channel.id_channel):
                result[sensor_data.channel.id_channel] = []

            series = sensor_data.to_time_series()
            result[sensor_data.channel.id_channel].append(series)

        # Beacons data are exported into separate files, one for each beacon
        base_filename = sensor.location + '_' + sensor.name.replace(' ', '_')

        # Write sensor infos file
        self.export_sensor_infos(sensor, base_dir, base_filename)

        # Data files
        # Write header

        beacons: dict = {}
        for id_channel in result.keys():
            # For beacons, one channel = one beacon power or tx
            channel = self.dbMan.get_channel(id_channel)
            if channel:
                beacon_id_parts = channel.label.split('_')
                if len(beacon_id_parts) >= 2:
                    beacon_id = beacon_id_parts[0] + beacon_id_parts[1]
                else:
                    beacon_id = channel.label

                if beacon_id not in beacons:
                    beacons[beacon_id] = None  # {'time': {'RSSI': [], 'Power': []} }

                for data in result[id_channel]:
                    if beacons[beacon_id] is None:
                        rows = len(data['time'])
                        beacons[beacon_id] = np.array([data['time'], [None]*rows, [None]*rows]).transpose()

                    if channel.label.endswith('RSSI'):
                        for index, t in enumerate(data['time']):
                            t_index = np.where(beacons[beacon_id][:, 0] == t)
                            if t_index:   # Time already there?
                                beacons[beacon_id][t_index, 1] = data['values'][index]
                            else:
                                beacons[beacon_id] = beacons[beacon_id] = np.vstack((beacons[beacon_id],
                                                                                    [t,  data['values'][index], None]))

                    if channel.label.endswith('Power'):
                        for index, t in enumerate(data['time']):
                            t_index = np.where(beacons[beacon_id][:, 0] == t)
                            if t_index:  # Time already there?
                                beacons[beacon_id][t_index, 2] = data['values'][index]
                            else:
                                beacons[beacon_id] = np.vstack((beacons[beacon_id], [t, None, data['values'][index]]))
        del result
        header = 'Time\tRSSI\tTx Power\t'
        for beacon in beacons:
            # Sort data (in case times were added afterwards)
            beacons[beacon].sort(0)
            # Save one file per beacon
            filename = base_dir + os.sep + base_filename + '_' + beacon
            if self.exportFormat == ExporterTypes.CSV:
                np.savetxt(filename + '.csv', beacons[beacon], delimiter="\t", header=header)
            elif self.exportFormat == ExporterTypes.MATLAB:

                var_name = sensor.name.replace(' ', '') + '_' + beacon
                sio.savemat(filename + '.mat', {var_name: beacons[beacon], 'labels': header.split('\t')},
                            do_compression=True, long_field_names=True)

    def export_sensor_infos(self, sensor: Sensor, base_dir: str, base_filename: str):
        infos = {'id_sensor': sensor.id_sensor, 'name': sensor.name, 'id_sensor_type': sensor.id_sensor_type,
                 'location': sensor.location, 'data_rate': sensor.data_rate, 'sampling_rate': sensor.sampling_rate,
                 'channels': len(sensor.channels), 'hardware_id': sensor.hw_id, 'hardware_name': sensor.hw_name}
        if self.exportFormat == ExporterTypes.CSV:
            DBExporter.dict_to_csv(base_dir + os.sep + 'infos_' + base_filename + '.csv', infos)
        if self.exportFormat == ExporterTypes.MATLAB:
            DBExporter.dict_to_mat(base_dir + os.sep + 'infos_' + base_filename + '.mat', {'sensor': infos})
