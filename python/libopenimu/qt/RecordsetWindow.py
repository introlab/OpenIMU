from PyQt5.QtWidgets import QLineEdit, QWidget, QPushButton, QListWidget, QListWidgetItem, QGraphicsScene, QLayout, \
    QGraphicsRectItem, QGraphicsItem, QGraphicsView, QGraphicsTextItem, QMdiArea, QVBoxLayout, QScrollArea, QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon, QBrush, QPen, QColor, QPixmap
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal, QModelIndex, QPoint, QRect, QObject, QDateTime

from resources.ui.python.RecordsetWidget_ui import Ui_frmRecordsets

from libopenimu.models.Recordset import Recordset
from libopenimu.db.DBManager import DBManager

from libopenimu.qt.TimeView import TimeView

from libopenimu.models.sensor_types import SensorType
from libopenimu.models.Base import Base
from libopenimu.importers.wimu import GPSGeodetic

from libopenimu.qt.Charts import IMUChartView
from libopenimu.qt.GPSView import GPSView
from libopenimu.qt.ProcessSelectWindow import ProcessSelectWindow


from libopenimu.tools.timing import timing
import os
import numpy as np

from datetime import datetime, timedelta
from random import shuffle

class RecordsetWindow(QWidget):

    dataDisplayRequest = pyqtSignal(str, int)
    dataUpdateRequest = pyqtSignal(str, Base)

    # sensorsColor = ['e0c31e', '14148c', '006325', '6400aa', '14aaff', 'ae32a0', '80c342', '868482']

    def __init__(self, manager, recordset : list, parent=None):
        super(QWidget, self).__init__(parent=parent)
        self.UI = Ui_frmRecordsets()
        self.UI.setupUi(self)

        #TODO
        self.UI.grpSubRecord.hide()

        self.sensors = {}
        self.sensors_items = {}
        self.sensors_graphs = {}

        self.time_pixmap = False

        self.time_bar = None

        self.dbMan = manager
        self.recordsets = recordset

        # Init temporal browser
        self.timeScene = QGraphicsScene()
        self.UI.graphTimeline.setScene(self.timeScene)
        self.UI.graphTimeline.fitInView(self.timeScene.sceneRect(), Qt.KeepAspectRatio)
        self.UI.graphTimeline.time_clicked.connect(self.timeview_clicked)

        # Init graph viewer
        #layout = QVBoxLayout()
        #layout.setSizeConstraint(QLayout.SetFixedSize)
        #self.UI.displayContents.setLayout(layout)
        #self.UI.displayContents.setMinimumWidth(self.UI.displayArea.width())

        # Update general informations about recordsets
        self.update_recordset_infos()

        # Load sensors for that recordset
        self.load_sensors()

        self.UI.lstSensors.itemChanged.connect(self.sensor_current_changed)

        # Connect process button
        self.UI.btnProcess.clicked.connect(self.on_process_recordset)

    def paintEvent(self, QPaintEvent):
        if not self.time_pixmap:
            self.draw_recordsets()
            self.draw_sensors()
            self.draw_dates()
            self.draw_timebar()
            self.time_pixmap = True

    def load_sensors(self):
        self.UI.lstSensors.clear()
        self.sensors = {}
        self.sensors_items = {}

        # Create sensor colors
        used_colors = []
        # colors = QColor.colorNames()
        colors = ['darkblue', 'darkviolet', 'darkgreen', 'darkorange', 'darkred','darkslategray', 'darkturquoise',
                  'darkolivegreen','darkseagreen','darkmagenta', 'darkkhaki' ,
                  'darkslateblue', 'darksalmon', 'darkorchid',  'darkcyan']

        # Filter "bad" colors for sensors
        """colors.remove("white")
        colors.remove("black")
        colors.remove("transparent")
        colors.remove("red")
        colors.remove("green")"""

        # shuffle(colors)
        color_index = 0

        if len(self.recordsets) > 0:
            for sensor in self.dbMan.get_sensors(self.recordsets[0]):
                self.sensors[sensor.id_sensor] = sensor

        for sensor in self.sensors.values():
            index = -1
            location_item = self.UI.lstSensors.findItems(sensor.location, Qt.MatchExactly)
            if len(location_item) == 0:
                item = QListWidgetItem(sensor.location)
                item.setFlags(Qt.NoItemFlags)
                item.setForeground(QBrush(Qt.black))

                self.UI.lstSensors.addItem(item)
            else:
                index = self.UI.lstSensors.indexFromItem(location_item[0]).row()

            # Check if sensor is already there under that location item
            sensor_name = sensor.name + " (" + sensor.hw_name + ")"
            present = False
            if index != -1:
                for i in range(index, self.UI.lstSensors.count()):
                    if self.UI.lstSensors.item(i).text() == sensor_name:
                        present = True
                        break

            if not present:
                item = QListWidgetItem(QIcon(':/OpenIMU/icons/sensor.png'), sensor_name)
                item.setCheckState(Qt.Unchecked)
                item.setForeground(QColor(colors[color_index]))
                item.setData(Qt.UserRole, sensor.id_sensor)
                # self.sensors_colors.append(colors[color_index])
                self.sensors_items[sensor.id_sensor] = item
                color_index += 1
                if color_index >= len(colors):
                    color_index = 0

                if index == -1:
                    self.UI.lstSensors.addItem(item)
                else:
                    self.UI.lstSensors.insertItem(index + 2, item)

    def update_recordset_infos(self):
        if len(self.recordsets) == 0:
            self.UI.lblTotalValue.setText("Aucune donnée.")
            self.UI.lblDurationValue.setText("Aucune donnée.")
            return

        start_time = self.recordsets[0].start_timestamp
        end_time = self.recordsets[len(self.recordsets) - 1].end_timestamp

        # Coverage
        self.UI.lblTotalValue.setText(str(start_time) + " @ " + str(end_time))

        # Duration
        self.UI.lblDurationValue.setText(str(end_time - start_time))

        self.UI.lblCursorTime.setText(str(start_time))

    def get_relative_timeview_pos(self, current_time):
        start_time = self.recordsets[0].start_timestamp
        end_time = self.recordsets[len(self.recordsets) - 1].end_timestamp
        time_span = (end_time - start_time).total_seconds()  # Total number of seconds in recordsets
        if time_span>0:
            return (((current_time - self.recordsets[
                0].start_timestamp).total_seconds()) / time_span) * self.UI.graphTimeline.width()
        else:
            return 0

    def draw_dates(self):
        if len(self.recordsets) == 0:
            return

        # Computations
        start_time = self.recordsets[0].start_timestamp
        end_time = self.recordsets[len(self.recordsets) - 1].end_timestamp
        time_span = (end_time - start_time).total_seconds()  # Total number of seconds in recordsets
        current_time = (datetime(start_time.year, start_time.month, start_time.day, 0, 0, 0) + timedelta(days=1))

        # Drawing tools
        whitePen = QPen(Qt.white)
        blackPen = QPen(Qt.black)
        blackBrush = QBrush(Qt.black)

        # Date background rectangle
        self.timeScene.addRect(0, 0, self.UI.graphTimeline.width(), self.UI.graphTimeline.height() / 4, blackPen,
                               blackBrush);

        # First date
        date_text = self.timeScene.addText(start_time.strftime("%d-%m-%Y"))
        date_text.setPos(0, -5)
        date_text.setDefaultTextColor(Qt.white)
        self.timeScene.addLine(0, 0, 0, self.UI.graphTimeline.height(), whitePen)

        # Date separators
        while current_time <= end_time:
            pos = self.get_relative_timeview_pos(current_time)
            self.timeScene.addLine(pos, 0, pos, self.UI.graphTimeline.height(), whitePen)
            date_text = self.timeScene.addText(current_time.strftime("%d-%m-%Y"))
            date_text.setPos(pos, -5)
            date_text.setDefaultTextColor(Qt.white)
            current_time += timedelta(days=1)

    def draw_recordsets(self):
        greenBrush = QBrush(QColor(212, 247, 192))
        transPen = QPen(Qt.transparent)

        # Empty rectangle (background)
        self.timeScene.addRect(0, 0, self.UI.graphTimeline.width(), self.UI.graphTimeline.height(), transPen,
                               QBrush(Qt.red))
        self.timeScene.setBackgroundBrush(QBrush(Qt.red))

        # Recording length
        for record in self.recordsets:
            start_pos = self.get_relative_timeview_pos(record.start_timestamp)
            end_pos = self.get_relative_timeview_pos(record.end_timestamp)
            span = end_pos - start_pos
            #print (str(span))
            self.timeScene.addRect(start_pos, 0, span, self.UI.graphTimeline.height(), transPen, greenBrush)

        self.UI.graphTimeline.update()

    def draw_sensors(self):
        if len(self.sensors) == 0:
            return

        bar_height = (3 * (self.UI.graphTimeline.height() / 4)) / len(self.sensors)
        # for sensor in self.sensors:
        i = 0
        for sensor in self.sensors.values():
            sensorBrush = QBrush(self.sensors_items[sensor.id_sensor].foreground())
            sensorPen = QPen(Qt.transparent)
            for record in self.recordsets:
                datas = self.dbMan.get_all_sensor_data(sensor=sensor, recordset=record, channel=sensor.channels[0])
                for data in datas:
                    start_pos = self.get_relative_timeview_pos(data.timestamps.start_timestamp)
                    end_pos = self.get_relative_timeview_pos(data.timestamps.end_timestamp)
                    span = max(end_pos - start_pos, 1)
                    self.timeScene.addRect(start_pos, i * bar_height + (self.UI.graphTimeline.height() / 4), span,
                                           bar_height, sensorPen, sensorBrush)
            i += 1

    def draw_timebar(self):
        self.time_bar = self.timeScene.addLine(0, 0, 0, self.timeScene.height(), QPen(Qt.cyan))

    @pyqtSlot(QListWidgetItem)
    def sensor_current_changed(self, item):
        sensor = self.sensors[item.data(Qt.UserRole)]
        timeseries = []
        # Color map
        colors = [Qt.red, Qt.green, Qt.yellow, Qt.cyan]

        if item.checkState() == Qt.Checked:
            # Choose the correct display for each sensor
            graph = None
            channels = self.dbMan.get_all_channels(sensor=sensor)
            for channel in channels:
                # Will get all data (converted to floats)
                channel_data = []
                for record in self.recordsets:
                    channel_data += self.dbMan.get_all_sensor_data(recordset=record, convert=True, sensor=sensor,
                                                                   channel=channel)
                timeseries.append(self.create_data_timeseries(channel_data))
                timeseries[-1]['label'] = channel.label

            if sensor.id_sensor_type == SensorType.ACCELEROMETER \
                    or sensor.id_sensor_type == SensorType.GYROMETER \
                    or sensor.id_sensor_type == SensorType.BATTERY \
                    or sensor.id_sensor_type == SensorType.LUX \
                    or sensor.id_sensor_type == SensorType.CURRENT \
                    or sensor.id_sensor_type == SensorType.BAROMETER \
                    or sensor.id_sensor_type == SensorType.MAGNETOMETER \
                    or sensor.id_sensor_type == SensorType.TEMPERATURE \
                    or sensor.id_sensor_type == SensorType.HEARTRATE \
                    or sensor.id_sensor_type == SensorType.ORIENTATION \
                    or sensor.id_sensor_type == SensorType.FSR:

                #graph = IMUChartView(self.UI.displayContents)
                graph = IMUChartView(self.UI.mdiArea)
                # graph.add_test_data()
                # Add series
                for series in timeseries:
                    graph.add_data(series['x'], series['y'], color=colors.pop(), legend_text=series['label'])

                graph.set_title(item.text())

            if sensor.id_sensor_type == SensorType.GPS:
                # graph = GPSView(self.UI.mdiArea)
                """base_widget = QWidget(self.UI.displayContents)
                base_widget.setFixedHeight(400)
                base_widget.setMaximumHeight(400)"""
                base_widget = self.UI.mdiArea
                graph = GPSView(base_widget)

                for data in channel_data:
                    gps = GPSGeodetic()
                    gps.from_bytes(data.data)
                    if gps.latitude != 0 and gps.longitude != 0:
                        graph.addPosition(data.timestamps.start_timestamp, gps.latitude / 1e7, gps.longitude / 1e7)
                        graph.setCursorPositionFromTime(data.timestamps.start_timestamp)
                    # print (gps)

            if graph is not None:
                self.UI.mdiArea.addSubWindow(graph).setWindowTitle(item.text())
                self.sensors_graphs[sensor.id_sensor] = graph
                #self.UI.displayContents.layout().insertWidget(0,graph)

                graph.show()
                QApplication.instance().processEvents()

                graph.aboutToClose.connect(self.graph_was_closed)
                graph.cursorMoved.connect(self.graph_cursor_changed)

                #self.UI.displayArea.ensureWidgetVisible(graph)
                # self.UI.displayArea.verticalScrollBar().setSliderPosition(self.UI.displayArea.verticalScrollBar().maximum())
                # self.tile_graphs_vertically()
                self.UI.mdiArea.tileSubWindows()

        else:
            # Remove from display
            try:
                if self.sensors_graphs[sensor.id_sensor] is not None:
                    self.UI.mdiArea.removeSubWindow(self.sensors_graphs[sensor.id_sensor].parent())

                    #self.UI.displayContents.layout().removeWidget(self.sensors_graphs[sensor.id_sensor])
                    self.sensors_graphs[sensor.id_sensor].hide()
                    self.sensors_graphs[sensor.id_sensor] = None
                    #self.tile_graphs_vertically()
                    self.UI.mdiArea.tileSubWindows()
            except KeyError:
                pass

    @pyqtSlot(QObject)
    def graph_was_closed(self, graph):
        for sensor_id, sensor_graph in self.sensors_graphs.items():
            if sensor_graph == graph:
                self.sensors_graphs[sensor_id] = None
                self.sensors_items[sensor_id].setCheckState(Qt.Unchecked)
                break

        #self.tile_graphs_vertically()
        self.UI.mdiArea.tileSubWindows()

    @pyqtSlot(datetime)
    def graph_cursor_changed(self, timestamp):
        for graph in self.sensors_graphs.values():
            if graph is not None:
                graph.setCursorPositionFromTime(timestamp, False)

        pos = self.get_relative_timeview_pos(timestamp)
        self.time_bar.setPos(pos,0)
        self.UI.lblCursorTime.setText(str(timestamp))

    @pyqtSlot(int)
    def timeview_clicked(self, x):
        self.time_bar.setPos(x, 0)

        # Find time corresponding to that position
        timestamp = (x / self.timeScene.width()) * (
                    self.recordsets[len(self.recordsets) - 1].end_timestamp - self.recordsets[0].start_timestamp) + \
                    self.recordsets[0].start_timestamp
        self.UI.lblCursorTime.setText(str(timestamp))

        for graph in self.sensors_graphs.values():
            if graph is not None:
                # try:
                graph.setCursorPositionFromTime(timestamp, True)
            # except AttributeError:
            #    continue

    @timing
    def create_data_timeseries(self, sensor_data_list: list):

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

    @pyqtSlot()
    def on_process_recordset(self):
        # Display Process Window
        window = ProcessSelectWindow(self.dbMan, self.recordsets)
        window.setStyleSheet(self.styleSheet())

        if window.exec() == QDialog.Accepted:
            self.dataUpdateRequest.emit("result", window.processed_data)
            self.dataDisplayRequest.emit("result", window.processed_data.id_processed_data)

    def tile_graphs_horizontally(self):

        if self.UI.mdiArea.subWindowList() is None:
            return

        position = QPoint(0,0)

        for window in self.UI.mdiArea.subWindowList():
            rect = QRect(0,0, self.UI.mdiArea.width() / len(self.UI.mdiArea.subWindowList()), self.UI.mdiArea.height())
            window.setGeometry(rect)
            window.move(position)
            position.setX(position.x() + window.width())

    def tile_graphs_vertically(self):

        if self.UI.mdiArea.subWindowList() is None:
            return

        position = QPoint(0,0)

        for window in self.UI.mdiArea.subWindowList():
            rect = QRect(0,0, self.UI.mdiArea.width(), self.UI.mdiArea.height()/ len(self.UI.mdiArea.subWindowList()))
            window.setGeometry(rect)
            window.move(position)
            position.setY(position.y() + window.height())


