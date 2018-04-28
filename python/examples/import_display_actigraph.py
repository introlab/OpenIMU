from libopenimu.importers.ActigraphImporter import ActigraphImporter
from libopenimu.db.DBManager import DBManager
from libopenimu.models.sensor_types import SensorType
from libopenimu.qt.Charts import IMUChartView
from libopenimu.tools.timing import timing

import os
import numpy as np

db_filename = 'actigraph.db'


@timing
def import_data_from_actigraph_file(filename):
    # This will create the database (or overwrite it)s
    importer = ActigraphImporter(db_filename)
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
    time_array = np.concatenate(time_values)
    data_array = np.concatenate(data_values)

    # Test, remove first time
    # time_array = time_array - time_array[0]

    # print('time_array_shape, data_array_shape', time_array.shape, data_array.shape)
    # return data
    return {'x': time_array, 'y': data_array}


# Testing app
if __name__ == '__main__':

    import sys

    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWidgets import QMainWindow, QPushButton
    from PyQt5.QtCore import Qt
    app = QApplication(sys.argv)

    timeseries_acc = []
    timeseries_batt = []
    timeseries_lux = []

    if not os.path.isfile(db_filename):
        print('importing actigraph data')
        import_data_from_actigraph_file('../resources/samples/test.gt3x')

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

            if sensor.id_sensor_type == SensorType.BATTERY:
                channels = manager.get_all_channels(sensor=sensor)
                for channel in channels:
                    print('Found Channel (battery)', channel)
                    channel_data = manager.get_all_sensor_data(recordset=record, convert=True, sensor=sensor,
                                                               channel=channel)
                    timeseries_batt.append(create_data_timeseries(channel_data))
                    timeseries_batt[-1]['label'] = channel.label

            if sensor.id_sensor_type == SensorType.LUX:
                channels = manager.get_all_channels(sensor=sensor)
                for channel in channels:
                    print('Found Channel (lux)', channel)
                    channel_data = manager.get_all_sensor_data(recordset=record, convert=True, sensor=sensor,
                                                               channel=channel)
                    timeseries_lux.append(create_data_timeseries(channel_data))
                    timeseries_lux[-1]['label'] = channel.label

    # Create widgets

    # Accelerometers
    def create_window(label=''):
        window = QMainWindow()
        view = IMUChartView(window)
        window.setCentralWidget(view)
        window.setWindowTitle(label)
        window.resize(640, 480)
        return [window, view]

    [window_acc, view_acc] = create_window('IMUChartView Demo (Accelerometers)')

    # All colors needed for 5 series
    colors = [Qt.red, Qt.green, Qt.darkBlue]

    # Add series
    for series in timeseries_acc:
        view_acc.add_data(series['x'], series['y'], color=colors.pop(), legend_text=series['label'])

    window_acc.show()

    # Battery
    [window_batt, view_batt] = create_window('IMUChartView Demo (Battery)')

    # Add series
    for series in timeseries_batt:
        view_batt.add_data(series['x'], series['y'], color=Qt.darkGreen, legend_text=series['label'])

    window_batt.show()

    # Lux
    [window_lux, view_lux] = create_window('IMUChartView Demo (Lux)')

    # Add series
    for series in timeseries_lux:
        view_lux.add_data(series['x'], series['y'], color=Qt.darkCyan, legend_text=series['label'])

    window_lux.show()

    # Exec application
    sys.exit(app.exec_())
