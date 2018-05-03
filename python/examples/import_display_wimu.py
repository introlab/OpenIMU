from libopenimu.importers.WIMUImporter import WIMUImporter
from libopenimu.db.DBManager import DBManager
from libopenimu.models.sensor_types import SensorType
from libopenimu.models.Participant import Participant
from libopenimu.qt.Charts import IMUChartView
from libopenimu.tools.timing import timing

import os
import numpy as np

db_filename = 'wimu.db'


@timing
def import_data_from_wimu_file(filename):
    # This will create the database (or overwrite it)s

    manager = DBManager(db_filename, overwrite=True)
    participant = Participant(name='My Participant', description='Participant Description')
    manager.update_participant(participant)

    importer = WIMUImporter(manager, participant)
    # Load content of the file to the database
    results = importer.load(filename)
    importer.import_to_database(results)


@timing
def create_data_timeseries(sensor_data_list: list):

    time_values = []
    data_values = []

    for sensor_data in sensor_data_list:
        # print('sensor_data', sensor_data)
        # Will get a dict with keys:  time, values
        vals = sensor_data.to_time_series()
        # print('vals is length', len(vals))
        time_values.append(vals['time'])
        data_values.append(vals['values'])

    # print('time_values length', len(time_values))
    # print('data_values length', len(data_values))

    # Concat vectors
    if len(time_values) > 0:
        time_array = np.concatenate(time_values)
        data_array = np.concatenate(data_values)
        return {'x': time_array, 'y': data_array}
    else:
        return {'x': [], 'y': []}


# Testing app
if __name__ == '__main__':

    import sys

    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWidgets import QMainWindow, QPushButton
    from PyQt5.QtCore import Qt
    app = QApplication(sys.argv)

    timeseries_acc = []
    timeseries_gyro = []

    if not os.path.isfile(db_filename):
        print('importing wimu data')
        import_data_from_wimu_file('../resources/samples/WIMU_ACC_GPS_GYRO_PreProcess.zip')

    # manager will handle the newly created database
    manager = DBManager(db_filename, overwrite=False)

    # Let's load all the recordsets (should have at least one)
    recordsets = manager.get_all_recordsets()

    for record in recordsets:
        # Get all sensors in record
        sensors = manager.get_all_sensors()
        for sensor in sensors:
            if sensor.id_sensor_type == SensorType.ACCELEROMETER:
                print('Found Accelerometer')
                channels = manager.get_all_channels(sensor=sensor)
                for channel in channels:
                    print('Found Channel (accelerometer)', channel)
                    # Will get all data (converted to floats)
                    channel_data = manager.get_all_sensor_data(recordset=record, convert=True, sensor=sensor,
                                                               channel=channel)
                    timeseries_acc.append(create_data_timeseries(channel_data))
                    timeseries_acc[-1]['label'] = channel.label
            if sensor.id_sensor_type == SensorType.GYROMETER:
                print('Found Gyro')
                channels = manager.get_all_channels(sensor=sensor)
                for channel in channels:
                    print('Found Channel (gyro)', channel)
                    # Will get all data (converted to floats)
                    channel_data = manager.get_all_sensor_data(recordset=record, convert=True, sensor=sensor,
                                                               channel=channel)
                    timeseries_gyro.append(create_data_timeseries(channel_data))
                    timeseries_gyro[-1]['label'] = channel.label

        # Only first recordset
        break

    # Create widgets
    def create_window(label=''):
        window = QMainWindow()
        view = IMUChartView(window)
        window.setCentralWidget(view)
        window.setWindowTitle(label)
        window.resize(640, 480)
        return [window, view]


    # Accelerometers
    [window_acc, view_acc] = create_window('IMUChartView Demo (Accelerometers)')

    # All colors needed for 3 series
    colors = [Qt.red, Qt.green, Qt.darkBlue]

    # Add series
    for series in timeseries_acc:
        view_acc.add_data(series['x'], series['y'], color=colors.pop(), legend_text=series['label'])

    window_acc.show()

    # Gyro
    [window_gyro, view_gyro] = create_window('IMUChartView Demo (Gyro)')

    # All colors needed for 3 series
    colors = [Qt.red, Qt.green, Qt.darkBlue]

    # Add series
    for series in timeseries_gyro:
        view_gyro.add_data(series['x'], series['y'], color=colors.pop(), legend_text=series['label'])

    window_gyro.show()

    # Exec application
    sys.exit(app.exec_())
