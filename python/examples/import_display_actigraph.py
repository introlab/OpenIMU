from libopenimu.importers.ActigraphImporter import ActigraphImporter
from libopenimu.db.DBManager import DBManager
from libopenimu.models.Recordset import  Recordset
from libopenimu.models.sensor_types import SensorType
from libopenimu.qt.Charts import IMUChartView

import os
import numpy as np


def import_data_from_actigraph_file(filename):
    # This will create the database (or overwrite it)s
    importer = ActigraphImporter('actigraph.db')
    # Load content of the file to the database
    results = importer.load(filename)
    importer.import_to_database(results)


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

    print('time_values length', len(time_values))
    print('data_values length', len(data_values))

    # Concat vectors
    time_array = np.concatenate(time_values)
    data_array = np.concatenate(data_values)

    print('time_array_shape, data_array_shape', time_array.shape, data_array.shape)
    # return data
    return {'x': time_array, 'y': data_array}


# Testing app
if __name__ == '__main__':

    import sys

    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWidgets import QMainWindow, QPushButton
    from PyQt5.QtCore import Qt
    app = QApplication(sys.argv)

    timeseries  = []

    if not os.path.isfile('actigraph.db'):
        print('importing actigraph data')
        import_data_from_actigraph_file('../resources/samples/test.gt3x')

    # manager will handle the newly created database
    manager = DBManager('actigraph.db', overwrite=False)

    # Let's load all the recordsets (should have at least one)
    recordsets = manager.get_all_recordsets()

    for record in recordsets:
        print('Processing record', record)

        # Get all sensors in record
        sensors = manager.get_all_sensors()
        for sensor in sensors:
            print('Processing sensor', sensor)
            if sensor.id_sensor_type == SensorType.ACCELEROMETER:
                print('Found Accelerometer')
                channels = manager.get_all_channels(sensor=sensor)
                for channel in channels:
                    print('Found Channel', channel)

                    # Will get all data (converted to floats)
                    channel_data = manager.get_all_sensor_data(recordset=record, convert=True, sensor=sensor,
                                                               channel=channel)

                    print('Channel data len', len(channel_data))
                    timeseries.append(create_data_timeseries(channel_data))
                    timeseries[-1]['label'] = channel.label

    # Create widgets
    window = QMainWindow()
    view = IMUChartView(window)
    window.setCentralWidget(view)
    window.setWindowTitle("IMUChartView Demo")
    window.resize(640, 480)

    colors = [Qt.red, Qt.green, Qt.darkBlue]

    # Add series
    for series in timeseries:
        view.add_data(series['x'], series['y'], color=colors.pop(), legend_text=series['label'])

    window.show()

    # Exec application
    sys.exit(app.exec_())