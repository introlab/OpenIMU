from PyQt5.QtWidgets import QWidget, QListWidgetItem
from PyQt5.QtWidgets import QGraphicsScene, QApplication, QGraphicsRectItem, QGraphicsLineItem, QGraphicsItem
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon, QBrush, QPen, QColor, QFont
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QPoint, QRect, QObject

from resources.ui.python.RecordsetWidget_ui import Ui_frmRecordsets

from libopenimu.models.sensor_types import SensorType
from libopenimu.models.Base import Base
from libopenimu.importers.wimu import GPSGeodetic

from libopenimu.qt.Charts import IMUChartView
from libopenimu.qt.GPSView import GPSView
from libopenimu.qt.ProcessSelectWindow import ProcessSelectWindow

from libopenimu.tools.timing import timing
import numpy as np

from datetime import datetime, timedelta


class RecordsetWindow(QWidget):

    dataDisplayRequest = pyqtSignal(str, int)
    dataUpdateRequest = pyqtSignal(str, Base)

    # sensorsColor = ['e0c31e', '14148c', '006325', '6400aa', '14aaff', 'ae32a0', '80c342', '868482']

    def __init__(self, manager, recordset: list, parent=None):
        super(QWidget, self).__init__(parent=parent)
        self.UI = Ui_frmRecordsets()
        self.UI.setupUi(self)

        self.sensors = {}
        self.sensors_items = {}
        self.sensors_graphs = {}
        self.sensors_location = []

        self.time_pixmap = False

        self.time_bar = QGraphicsLineItem()
        self.selection_rec = QGraphicsRectItem()
        self.zoom_level = 1

        self.dbMan = manager
        self.recordsets = recordset

        # Init temporal browser
        self.timeScene = QGraphicsScene()
        self.UI.graphTimeline.setScene(self.timeScene)
        self.UI.graphTimeline.fitInView(self.timeScene.sceneRect())
        self.UI.graphTimeline.time_clicked.connect(self.timeview_clicked)
        self.UI.graphTimeline.time_selected.connect(self.timeview_selected)
        self.UI.scrollTimeline.valueChanged.connect(self.timeview_scroll)

        # Init temporal sensor list
        self.timeSensorsScene = QGraphicsScene()
        self.UI.graphSensorsTimeline.setScene(self.timeSensorsScene)
        self.UI.graphSensorsTimeline.fitInView(self.timeSensorsScene.sceneRect(), Qt.KeepAspectRatio)

        # Update general informations about recordsets
        self.update_recordset_infos()

        # Load sensors for that recordset
        self.load_sensors()

        self.UI.lstSensors.itemChanged.connect(self.sensor_current_changed)
        self.UI.btnClearSelection.clicked.connect(self.on_timeview_clear_selection_requested)
        self.UI.btnTimeZoomSelection.clicked.connect(self.on_timeview_zoom_selection_requested)
        self.UI.btnZoomReset.clicked.connect(self.on_timeview_zoom_reset_requested)
        self.UI.btnDisplayTimeline.clicked.connect(self.on_timeview_show_hide_requested)
        self.UI.btnZoomReset.setEnabled(False)
        self.UI.btnTimeZoomSelection.setEnabled(False)
        self.UI.btnClearSelection.setEnabled(False)

        # self.UI.frmSensors.setFixedHeight(self.height()-50)

    def paintEvent(self, paint_event):
        if not self.time_pixmap:
            self.refresh_timeview()
            self.time_pixmap = True

    def resizeEvent(self, resize_event):
        # self.refresh_timeview()
        return

    def refresh_timeview(self):
        # Computes required timescene size
        min_width = self.UI.graphTimeline.width() - 5
        num_days = (self.get_recordset_end_day_date() - self.get_recordset_start_day_date()).days

        # Minimum size for days
        if num_days * 75 > min_width:
            min_width = num_days * 75 - 5

        # Resize timeScene correctly
        self.timeScene.clear()
        self.timeScene.setSceneRect(self.timeScene.itemsBoundingRect())
        self.timeScene.addLine(0, 80, min_width, 80, QPen(Qt.transparent))

        # Set background color
        back_brush = QBrush(Qt.lightGray)
        self.timeScene.setBackgroundBrush(back_brush)
        self.timeSensorsScene.setBackgroundBrush(back_brush)

        # Update display
        self.draw_dates()
        self.draw_sensors_names()
        self.draw_recordsets()
        self.draw_sensors()
        self.draw_grid()
        self.draw_timebar()

        # Adjust splitter sizes
        self.adjust_timeview_size()
        # self.UI.frmSensors.hide()

    def adjust_timeview_size(self):
        self.UI.frameScrollSpacer.setFixedWidth(self.UI.graphTimeline.pos().x())
        if self.timeScene.itemsBoundingRect().width() * self.zoom_level > self.UI.graphTimeline.width():
            self.UI.scrollTimeline.setVisible(True)
            # self.UI.scrollTimeline.setMinimum(self.UI.graphTimeline.width()/2)
            self.UI.scrollTimeline.setMinimum(0)
            self.UI.scrollTimeline.setMaximum(self.timeScene.itemsBoundingRect().width() * self.zoom_level)
            self.UI.scrollTimeline.setPageStep(self.UI.graphTimeline.width()/2)
            self.UI.scrollTimeline.setSingleStep(self.UI.graphTimeline.width()/5)
        else:
            self.UI.scrollTimeline.setVisible(False)

        # self.timeScene.setSceneRect(self.timeScene.itemsBoundingRect())
        # self.timeSensorsScene.setSceneRect(self.timeSensorsScene.itemsBoundingRect())

        # Compute size based on items
        """ max_size = 20 # Date
        max_size += len(self.sensors)*20 + len(self.sensors_location)*15

        if self.UI.graphTimeline.horizontalScrollBar().isVisible():
            max_size += 20  # Scrollbar, if needed
        self.UI.graphTimeline.setFixedHeight(max_size)
        self.UI.graphSensorsTimeline.setFixedHeight(max_size)
        """
        # min_height = self.timeScene.itemsBoundingRect().height()
        # self.UI.graphTimeline.setFixedHeight(min_height)
        # self.UI.graphSensorsTimeline.setFixedHeight(min_height)
        # self.UI.frameTimeline.setMaximumHeight(self.timeSensorsScene.height() + self.UI.frameCursor.height() +
        #                                       self.UI.frameInfos.height())

        # min_height = self.timeScene.height() # self.UI.frameTimeline.maximumHeight()
        # self.UI.mainSplitter.setSizes([min_height, -1])

    def load_sensors(self):
        self.UI.lstSensors.clear()
        self.sensors = {}
        self.sensors_items = {}
        self.sensors_location = []

        # Create sensor colors
        # colors = QColor.colorNames()
        colors = ['darkblue', 'darkviolet', 'darkgreen', 'darkorange', 'darkred', 'darkslategray', 'darkturquoise',
                  'darkolivegreen', 'darkseagreen', 'darkmagenta', 'darkkhaki',
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
            # TODO: Use sensors from all recordsets
            for recordset in self.recordsets:
                for sensor in self.dbMan.get_sensors(recordset):
                    if sensor.id_sensor not in self.sensors:
                        self.sensors[sensor.id_sensor] = sensor
                    if sensor.location not in self.sensors_location:
                        self.sensors_location.append(sensor.location)

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
        self.UI.lblTotalValue.setText(start_time.strftime('%d-%m-%Y %H:%M:%S') + " @ " + end_time.strftime(
                                                                                                '%d-%m-%Y %H:%M:%S'))

        # Duration
        # TODO: format better
        self.UI.lblDurationValue.setText(str(end_time - start_time))

        self.UI.lblCursorTime.setText(start_time.strftime('%d-%m-%Y %H:%M:%S'))

    def get_recordset_start_day_date(self):
        start_time = self.recordsets[0].start_timestamp
        start_time = (datetime(start_time.year, start_time.month, start_time.day, 0, 0, 0))
        return start_time

    def get_recordset_end_day_date(self):
        end_time = self.recordsets[len(self.recordsets) - 1].end_timestamp
        end_time = (datetime(end_time.year, end_time.month, end_time.day, 0, 0, 0) + timedelta(days=1))
        return end_time

    def get_relative_timeview_pos(self, current_time):
        # start_time = self.recordsets[0].start_timestamp.timestamp()
        start_time = self.get_recordset_start_day_date().timestamp()
        # end_time = self.recordsets[len(self.recordsets) - 1].end_timestamp.timestamp()
        end_time = self.get_recordset_end_day_date().timestamp()
        time_span = (end_time - start_time)  # Total number of seconds in recordsets
        if type(current_time) is datetime:
            current_time = current_time.timestamp()

        if time_span > 0:
            # return ((current_time - start_time) / time_span) * self.UI.graphTimeline.width()
            return ((current_time - start_time) / time_span) * self.timeScene.width()
        else:
            return 0

    def get_time_from_timeview_pos(self, pos):
        start_time = self.get_recordset_start_day_date().timestamp()
        end_time = self.get_recordset_end_day_date().timestamp()

        current_time = (pos / self.timeScene.width()) * (end_time - start_time) + start_time
        current_time = datetime.fromtimestamp(current_time)

        return current_time

    def draw_dates(self):
        if len(self.recordsets) == 0:
            return

        # Computations
        start_time = self.recordsets[0].start_timestamp
        end_time = self.recordsets[len(self.recordsets) - 1].end_timestamp
        # time_span = (end_time - start_time).total_seconds()  # Total number of seconds in recordsets
        current_time = (datetime(start_time.year, start_time.month, start_time.day, 0, 0, 0) + timedelta(days=1))

        # Drawing tools
        black_pen = QPen(Qt.black)
        blue_brush = QBrush(Qt.darkBlue)

        # Date background
        self.timeScene.addRect(0, 0, self.timeScene.width(), 20, black_pen, blue_brush)
        self.timeSensorsScene.addRect(0, 0, self.timeSensorsScene.width(), 20, black_pen, blue_brush)

        # First date
        date_text = self.timeScene.addText(start_time.strftime("%d-%m-%Y"))
        date_text.setPos(0, 0)  # -5
        date_text.setDefaultTextColor(Qt.white)
        date_text.setFlag(QGraphicsItem.ItemIgnoresTransformations, True)

        # Date separators
        while current_time <= end_time:
            pos = self.get_relative_timeview_pos(current_time)
            date_text = self.timeScene.addText(current_time.strftime("%d-%m-%Y"))
            date_text.setPos(pos, 0)  # -5
            date_text.setDefaultTextColor(Qt.white)
            date_text.setFlag(QGraphicsItem.ItemIgnoresTransformations, True)
            current_time += timedelta(days=1)

        # self.UI.graphTimeline.fitInView(self.timeScene.sceneRect(), Qt.KeepAspectRatio)

    def draw_grid(self):
        if len(self.recordsets) == 0:
            return

        # Computations
        start_time = self.recordsets[0].start_timestamp
        end_time = self.recordsets[len(self.recordsets) - 1].end_timestamp
        # time_span = (end_time - start_time).total_seconds()  # Total number of seconds in recordsets
        current_time = (datetime(start_time.year, start_time.month, start_time.day, 0, 0, 0) + timedelta(days=1))

        vgrid_pen = QPen(Qt.gray)
        hgrid_pen = QPen(Qt.black)
        vgrid_pen.setCosmetic(True)

        # Horizontal lines
        pos = 20
        last_location = ""
        sensor_location_brush = QBrush(Qt.black)
        sensor_location_pen = QPen(Qt.transparent)
        for sensor in self.sensors.values():
            if sensor.location != last_location:
                # Must create a new location line
                self.timeScene.addRect(0, pos, self.timeScene.width()-1, 15, sensor_location_pen, sensor_location_brush)
                pos += 15
                last_location = sensor.location

            self.timeScene.addLine(0, pos, self.timeScene.width()-1, pos, hgrid_pen)
            self.timeSensorsScene.addLine(0, pos, self.timeSensorsScene.width(), pos, hgrid_pen)
            pos += 20

        # Final line
        self.timeScene.addLine(0, pos, self.timeScene.width() - 1, pos, hgrid_pen)
        self.timeSensorsScene.addLine(0, pos, self.timeSensorsScene.width() - 1, pos, hgrid_pen)

        # Date separators
        self.timeScene.addLine(0, 0, 0, self.timeScene.height(), vgrid_pen)

        # Other dates
        while current_time <= end_time:
            pos = self.get_relative_timeview_pos(current_time)
            self.timeScene.addLine(pos, 0, pos, self.timeScene.height(), vgrid_pen)
            current_time += timedelta(days=1)

    def draw_recordsets(self):
        recordset_brush = QBrush(QColor(212, 247, 192))  # Green
        recordset_pen = QPen(Qt.transparent)

        # Recording length
        for record in self.recordsets:
            start_pos = self.get_relative_timeview_pos(record.start_timestamp)
            end_pos = self.get_relative_timeview_pos(record.end_timestamp)
            span = end_pos - start_pos
            # print (str(span))
            self.timeScene.addRect(start_pos, 21, span, self.timeSensorsScene.height()-21, recordset_pen,
                                   recordset_brush)

        # self.UI.graphTimeline.update()
        return

    def draw_sensors_names(self):
        if len(self.sensors) == 0:
            return

        sensor_location_brush = QBrush(Qt.black)
        sensor_location_pen = QPen(Qt.transparent)

        # Sensor names
        pos = 20
        last_location = ""
        for sensor in self.sensors.values():
            # Sensor location
            if sensor.location != last_location:
                # Must create a new location space for later
                pos += 15
                last_location = sensor.location

            # Sensor names
            label = self.timeSensorsScene.addText(sensor.name)
            label.setPos(0, pos)
            label.setDefaultTextColor(Qt.black)
            # label.setFont(QFont("Times", 10, QFont.Bold))
            pos += 20

        # Adjust size appropriately
        self.timeSensorsScene.setSceneRect(self.timeSensorsScene.itemsBoundingRect())
        self.UI.graphSensorsTimeline.setMaximumWidth(self.timeSensorsScene.itemsBoundingRect().width())

        # Sensor location background
        pos = 20
        last_location = ""
        for sensor in self.sensors.values():
            # Sensor location
            if sensor.location != last_location:
                # Must create a new location line
                self.timeSensorsScene.addRect(0, pos, self.timeSensorsScene.width(), 15, sensor_location_pen,
                                              sensor_location_brush)
                label = self.timeSensorsScene.addText(sensor.location)
                label.setPos(0, pos)
                label.setDefaultTextColor(Qt.white)
                label.setFont(QFont("Times", 7))
                pos += 15
                last_location = sensor.location
            pos += 20

    def draw_sensors(self):
        if len(self.sensors) == 0:
            return

        sensor_brush = QBrush(Qt.darkGreen)
        sensor_pen = QPen(Qt.transparent)

        pos = 20
        last_location = ""
        for sensor in self.sensors.values():
            # Sensor location
            if sensor.location != last_location:
                # Must skips a space for sensor location
                pos += 15
                last_location = sensor.location

            # Sensor data
            for record in self.recordsets:
                datas = self.dbMan.get_all_sensor_data(sensor=sensor, recordset=record, channel=sensor.channels[0])
                for data in datas:
                    start_pos = self.get_relative_timeview_pos(data.timestamps.start_timestamp)
                    end_pos = self.get_relative_timeview_pos(data.timestamps.end_timestamp)
                    span = max(end_pos - start_pos, 1)
                    self.timeScene.addRect(start_pos, pos + 3, span, 14, sensor_pen, sensor_brush)
            pos += 20

        # Adjust size appropriately
        self.timeSensorsScene.setSceneRect(self.timeSensorsScene.itemsBoundingRect())
        self.UI.graphSensorsTimeline.setMaximumWidth(self.timeSensorsScene.itemsBoundingRect().width())
        # self.UI.graphSensorsTimeline.setMaximumHeight(self.timeSensorsScene.itemsBoundingRect().height())

    def draw_timebar(self):
        line_pen = QPen(Qt.cyan)
        line_pen.setWidth(2)
        self.time_bar = self.timeScene.addLine(0, 1, 0, self.timeScene.height(), line_pen)
        self.time_bar.setFlag(QGraphicsItem.ItemIgnoresTransformations, True)

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
                # self.UI.displayContents.layout().insertWidget(0,graph)

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
                    self.sensors_graphs[sensor.id_sensor].hide()
                    self.sensors_graphs[sensor.id_sensor] = None
                    # self.tile_graphs_vertically()
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

        # self.tile_graphs_vertically()
        self.UI.mdiArea.tileSubWindows()

    @pyqtSlot(float)
    def graph_cursor_changed(self, timestamp):
        for graph in self.sensors_graphs.values():
            if graph is not None:
                graph.setCursorPositionFromTime(timestamp/1000, False)

        pos = self.get_relative_timeview_pos(timestamp/1000)
        self.time_bar.setPos(pos,0)

        self.UI.lblCursorTime.setText(datetime.fromtimestamp(timestamp/1000).strftime('%d-%m-%Y %H:%M:%S'))

    @pyqtSlot(int)
    def timeview_scroll(self, pos):
        self.UI.graphTimeline.centerOn(pos / self.zoom_level, 0)

    @pyqtSlot(float)
    def timeview_clicked(self, x):
        self.time_bar.setPos(x, 0)
        # Find time corresponding to that position
        timestamp = self.get_time_from_timeview_pos(x)
        self.UI.lblCursorTime.setText(timestamp.strftime('%d-%m-%Y %H:%M:%S'))

        for graph in self.sensors_graphs.values():
            if graph is not None:
                # try:
                graph.setCursorPositionFromTime(timestamp, True)
            # except AttributeError:
            #    continue

    @pyqtSlot(float, float)
    def timeview_selected(self, start_x, end_x):
        selection_brush = QBrush(QColor(153, 204, 255, 128))
        selection_pen = QPen(Qt.transparent)
        self.timeScene.removeItem(self.selection_rec)
        self.selection_rec = self.timeScene.addRect(start_x, 20, end_x-start_x, self.timeScene.height()-20,
                                                    selection_pen, selection_brush)

        self.UI.btnClearSelection.setEnabled(True)
        self.UI.btnTimeZoomSelection.setEnabled(True)

    @pyqtSlot()
    def on_timeview_clear_selection_requested(self):
        self.timeScene.removeItem(self.selection_rec)
        self.UI.btnClearSelection.setEnabled(False)
        self.UI.btnTimeZoomSelection.setEnabled(False)

    @pyqtSlot()
    def on_timeview_zoom_selection_requested(self):
        self.UI.graphTimeline.scale(1 / self.zoom_level, 1)
        # zoom_value = (self.timeScene.width() / (self.selection_rec.rect().width()))
        zoom_value = (self.UI.graphTimeline.width() / (self.selection_rec.rect().width()))
        self.zoom_level = zoom_value
        self.UI.graphTimeline.scale(zoom_value, 1)
        self.UI.btnZoomReset.setEnabled(True)
        self.adjust_timeview_size()
        # self.UI.graphTimeline.ensureVisible(self.selection_rec.rect(), 0, 0)
        # self.UI.graphTimeline.centerOn(self.selection_rec.rect().x() + self.selection_rec.rect().width() / 2, 0)
        self.UI.scrollTimeline.setValue((self.selection_rec.rect().x() + self.selection_rec.rect().width() / 2)
                                        * self.zoom_level)
        self.on_timeview_clear_selection_requested()

    @pyqtSlot()
    def on_timeview_zoom_reset_requested(self):
        self.UI.graphTimeline.scale(1 / self.zoom_level, 1)
        self.zoom_level = 1
        self.UI.btnZoomReset.setEnabled(False)
        self.adjust_timeview_size()
        self.UI.scrollTimeline.setValue(0)

    @pyqtSlot()
    def on_timeview_show_hide_requested(self):
        visible = not self.UI.frameTimeline.isVisible()
        self.UI.frameTimeline.setVisible(visible)
        self.UI.frameTimelineControls.setVisible(visible)
        # self.UI.lblCursorTime.setVisible(visible)

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


