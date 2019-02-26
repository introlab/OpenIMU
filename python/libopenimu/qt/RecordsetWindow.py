from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGraphicsScene, QApplication, QGraphicsRectItem, QGraphicsLineItem, QGraphicsItem
from PyQt5.QtWidgets import QDialog, QMenu, QAction
from PyQt5.QtGui import QBrush, QPen, QColor, QFont, QGuiApplication
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QPoint, QRect, QObject, QRectF

from resources.ui.python.RecordsetWidget_ui import Ui_frmRecordsets
from libopenimu.qt.GraphWindow import GraphType, GraphWindow

from libopenimu.models.sensor_types import SensorType
from libopenimu.models.Sensor import Sensor
from libopenimu.models.Base import Base
from libopenimu.importers.wimu import GPSGeodetic
from libopenimu.qt.BackgroundProcess import BackgroundProcess, ProgressDialog, WorkerTask
from libopenimu.db.DBManager import DBManager

from libopenimu.qt.ProcessSelectWindow import ProcessSelectWindow

# from libopenimu.tools.timing import timing
import numpy as np
import string

from datetime import datetime, timedelta


# This class is a worker task that queries the database for specific sensor data for all current recordsets
# Used from "get_sensor_data"
class DBSensorAllDataTask(WorkerTask):
    def __init__(self, title: string, db_manager: DBManager, task_sensor: Sensor, task_start_time: int,
                 task_end_time: int, recordsets: list, parent=None):
        super().__init__(title, 0, parent)

        self.dbMan = db_manager
        self.start_time = task_start_time
        self.end_time = task_end_time
        self.sensor = task_sensor
        self.recordsets = recordsets
        self.size = 0

        self.results = {}

    @staticmethod
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

    def process(self):
        timeseries = []
        channels = self.dbMan.get_all_channels(sensor=self.sensor)
        self.size = len(channels)*len(self.recordsets)
        count = 0
        for channel in channels:
            # Will get all data (converted to floats)
            channel_data = []
            for record in self.recordsets:
                channel_data += self.dbMan.get_all_sensor_data(recordset=record, convert=True, sensor=self.sensor,
                                                               channel=channel, start_time=self.start_time,
                                                               end_time=self.end_time)
                count += 1
                self.update_progress.emit(count)

            if len(channel_data) > 0:
                timeseries.append(self.create_data_timeseries(channel_data))
                timeseries[-1]['label'] = channel.label
        self.results = {'sensor': self.sensor, 'timeseries': timeseries, 'channel_data': channel_data}


# This class is a worker task that queries the database for specific sensor data for all current recordsets
# Used from "create_sensors_rect"
class DBSensorTimesTask(WorkerTask):
    def __init__(self, title: string, db_manager: DBManager, sensor_id: int, recordset, parent=None):
        super().__init__(title, 0, parent)

        self.dbMan = db_manager
        self.sensor_id = sensor_id
        self.recordset = recordset
        self.size = 0

        self.results = {}

    def process(self):
        sensor = self.dbMan.get_sensor(self.sensor_id)
        datas = self.dbMan.get_all_sensor_data(sensor=sensor, recordset=self.recordset, channel=sensor.channels[0])
        times = []
        for data in datas:
            time = {"sensor_id": self.sensor_id,
                    "start_time": data.timestamps.start_timestamp,
                    "end_time": data.timestamps.end_timestamp}
            times.append(time)

        self.results = times


class RecordsetWindow(QWidget):

    dataDisplayRequest = pyqtSignal(str, int)
    dataUpdateRequest = pyqtSignal(str, Base)

    def __init__(self, manager, recordset: list, parent=None):
        super().__init__(parent=parent)
        self.UI = Ui_frmRecordsets()
        self.UI.setupUi(self)

        # Internal lists
        self.sensors = {}           # List of sensors objects
        self.sensors_items = {}     # List of QAction corresponding to each sensors
        self.sensors_graphs = {}    # List of graph corresponding to each sensor graph
        self.sensors_location = []  # List of sensors location in this recordset
        self.sensors_blocks = {}    # Sensor blocks - each block of data for each sensor

        # Variables
        self.time_pixmap = False    # Flag used to check if we need to repaint the timeline or not
        self.zoom_level = 1         # Current timeview zoom level

        # Manually created UI objects
        self.time_bar = QGraphicsLineItem()         # Currently selected timestamp bar
        self.selection_rec = QGraphicsRectItem()    # Section rectangle
        self.sensors_menu = QMenu(self.UI.btnNewGraph)
        self.UI.btnNewGraph.setMenu(self.sensors_menu)

        # Data access informations
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

        # Connect signals to slots
        self.UI.btnClearSelection.clicked.connect(self.on_timeview_clear_selection_requested)
        self.UI.btnTimeZoomSelection.clicked.connect(self.on_timeview_zoom_selection_requested)
        self.UI.btnZoomReset.clicked.connect(self.on_timeview_zoom_reset_requested)
        self.UI.btnDisplayTimeline.clicked.connect(self.on_timeview_show_hide_requested)
        self.UI.btnTileHorizontal.clicked.connect(self.tile_graphs_horizontally)
        self.UI.btnTileVertical.clicked.connect(self.tile_graphs_vertically)
        self.UI.btnTileAuto.clicked.connect(self.tile_graphs_auto)
        self.sensors_menu.triggered.connect(self.sensor_graph_selected)

        # Initial UI state
        self.UI.btnZoomReset.setEnabled(False)
        self.UI.btnTimeZoomSelection.setEnabled(False)
        self.UI.btnClearSelection.setEnabled(False)
        self.update_tile_buttons_state()

    def paintEvent(self, paint_event):
        if not self.time_pixmap:
            self.refresh_timeview()
            self.time_pixmap = True

    def resizeEvent(self, resize_event):
        if self.time_pixmap:
            self.refresh_timeview()

    def refresh_timeview(self):
        QGuiApplication.setOverrideCursor(Qt.BusyCursor)

        # Computes required timescene size
        min_width = self.UI.graphTimeline.width() - 5
        if len(self.recordsets) > 0:
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

        QGuiApplication.restoreOverrideCursor()

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

    def load_sensors(self):

        # self.UI.lstSensors.clear()
        self.sensors = {}
        self.sensors_items = {}
        self.sensors_location = []
        self.sensors_menu.clear()

        if len(self.recordsets) > 0:
            for recordset in self.recordsets:
                for sensor in self.dbMan.get_sensors(recordset):
                    if sensor.location not in self.sensors_location:
                        self.sensors_location.append(sensor.location)
                        self.sensors_menu.addSection(sensor.location)
                    if sensor.id_sensor not in self.sensors:
                        self.sensors[sensor.id_sensor] = sensor
                        sensor_item = QAction(sensor.name)
                        sensor_item.setCheckable(True)
                        sensor_item.setProperty("sensor_id", sensor.id_sensor)
                        self.sensors_items[sensor.id_sensor] = sensor_item
                        self.sensors_menu.addAction(sensor_item)

            # Create sensors blocks for display
            self.load_sensors_blocks()
        else:
            self.UI.btnNewGraph.setEnabled(False)

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
        if len(self.recordsets) == 0:
            return None
        start_time = self.recordsets[0].start_timestamp
        start_time = (datetime(start_time.year, start_time.month, start_time.day, 0, 0, 0))
        return start_time

    def get_recordset_end_day_date(self):
        if len(self.recordsets) == 0:
            return None
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
        if len(self.recordsets) == 0:
            return None;

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
        # last_location = ""
        sensor_location_brush = QBrush(Qt.black)
        sensor_location_pen = QPen(Qt.transparent)
        for location in self.sensors_location:
            # Must create a new location line
            self.timeScene.addRect(0, pos, self.timeScene.width() - 1, 15, sensor_location_pen, sensor_location_brush)
            pos += 15
            sensors = self.get_sensors_for_location(location)
            for _ in sensors:
                self.timeScene.addLine(0, pos, self.timeScene.width() - 1, pos, hgrid_pen)
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

        for location in self.sensors_location:
            # Must create a new location space for later
            pos += 15
            sensors = self.get_sensors_for_location(location)
            for sensor_id in sensors:
                sensor = self.sensors[sensor_id]
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
        for location in self.sensors_location:
            # Must create a new location line
            self.timeSensorsScene.addRect(0, pos, self.timeSensorsScene.width(), 15, sensor_location_pen,
                                          sensor_location_brush)
            label = self.timeSensorsScene.addText(location)
            label.setPos(0, pos)
            label.setDefaultTextColor(Qt.white)
            label.setFont(QFont("Times", 7))
            pos += 15
            sensors = self.get_sensors_for_location(location)
            for sensor_id in sensors:
                pos += 20

    def draw_sensors(self):
        if len(self.sensors) == 0:
            return

        sensor_brush = QBrush(Qt.darkGreen)
        sensor_pen = QPen(Qt.transparent)

        sensors_rects = self.create_sensors_rects()
        for _, rect in enumerate(sensors_rects):
            self.timeScene.addRect(rect, sensor_pen, sensor_brush)

        # Adjust size appropriately
        self.timeSensorsScene.setSceneRect(self.timeSensorsScene.itemsBoundingRect())
        self.UI.graphSensorsTimeline.setMaximumWidth(self.timeSensorsScene.itemsBoundingRect().width())
        # self.UI.graphSensorsTimeline.setMaximumHeight(self.timeSensorsScene.itemsBoundingRect().height())

    def load_sensors_blocks(self):
        # Create request tasks
        tasks = []
        for location in self.sensors_location:
            sensors = self.get_sensors_for_location(location)
            for sensor_id in sensors:
                for record in self.recordsets:
                    tasks.append(DBSensorTimesTask(title="Chargement des données temporelles", db_manager=self.dbMan,
                                                   sensor_id=sensor_id, recordset=record))

        QGuiApplication.setOverrideCursor(Qt.BusyCursor)
        process = BackgroundProcess(tasks)
        dialog = ProgressDialog(process, "Chargement")

        process.start()
        dialog.exec()
        QGuiApplication.restoreOverrideCursor()

        # Combine tasks results
        self.sensors_blocks = {}
        for task in tasks:
                for result in task.results:
                    if result['sensor_id'] not in self.sensors_blocks:
                        self.sensors_blocks[result['sensor_id']] = []
                    start_time = result['start_time']
                    end_time = result['end_time']
                    data = {"start_time": start_time, "end_time": end_time}
                    self.sensors_blocks[result['sensor_id']].append(data)

    def create_sensors_rects(self):
        rects = []
        pos = 20
        for location in self.sensors_location:
            # Must create a new location space for later
            pos += 15
            sensors = self.get_sensors_for_location(location)
            for sensor_id in sensors:
                """sensor = self.sensors[sensor_id]
                for record in self.recordsets:
                    datas = self.dbMan.get_all_sensor_data(sensor=sensor, recordset=record, channel=sensor.channels[0])
                    for data in datas:
                        start_pos = self.get_relative_timeview_pos(data.timestamps.start_timestamp)
                        end_pos = self.get_relative_timeview_pos(data.timestamps.end_timestamp)
                        span = max(end_pos - start_pos, 1)
                        rects.append(QRectF(start_pos, pos + 3, span, 14))
                """
                for block in self.sensors_blocks[sensor_id]:
                    start_pos = self.get_relative_timeview_pos(block['start_time'])
                    end_pos = self.get_relative_timeview_pos(block['end_time'])
                    span = max(end_pos - start_pos, 1)
                    rects.append(QRectF(start_pos, pos + 3, span, 14))
                pos += 20

        return rects

    def draw_timebar(self):
        line_pen = QPen(Qt.cyan)
        line_pen.setWidth(2)
        self.time_bar = self.timeScene.addLine(1, 21, 1, self.timeScene.height()-1, line_pen)
        # self.time_bar = self.timeScene.addLine(0, 1, 0, self.timeScene.height() - 1, line_pen)
        self.time_bar.setFlag(QGraphicsItem.ItemIgnoresTransformations, True)

    def get_sensors_for_location(self, location):
        sensors_id = []
        for sensor in self.sensors.values():
            if sensor.location == location:
                sensors_id.append(sensor.id_sensor)

        return sensors_id

    @staticmethod
    def get_sensor_graph_type(sensor):
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
            return GraphType.LINECHART

        if sensor.id_sensor_type == SensorType.GPS:
            return GraphType.MAP

        return GraphType.UNKNOWN

    @pyqtSlot(Sensor, datetime, datetime)
    def query_sensor_data(self, sensor: Sensor, start_time: datetime, end_time: datetime):
        timeseries = self.get_sensor_data(sensor, start_time, end_time)[0]

        if self.sensors_graphs[sensor.id_sensor]:
            graph_type = self.get_sensor_graph_type(sensor)
            graph_window = self.sensors_graphs[sensor.id_sensor]
            if graph_type == GraphType.LINECHART:
                series_id = 0
                for series in timeseries:
                    # Filter times that don't fit in the range
                    y_range = series['y']
                    x_range = series['x']
                    y_range = y_range[x_range >= start_time.timestamp()]
                    x_range = x_range[x_range >= start_time.timestamp()]
                    y_range = y_range[x_range <= end_time.timestamp()]
                    x_range = x_range[x_range <= end_time.timestamp()]
                    if len(x_range)>0 and len(y_range)>0:
                        graph_window.graph.update_data(x_range, y_range, series_id)
                    series_id += 1
        return

    @pyqtSlot(QAction)
    # @timing
    def sensor_graph_selected(self, sensor_item):
        sensor_id = sensor_item.property("sensor_id")
        sensor = self.sensors[sensor_id]
        sensor_label = sensor.name + " (" + sensor.location + ")"

        if sensor_item.isChecked():
            # Choose the correct display for each sensor
            graph_window = None
            timeseries, channel_data = self.get_sensor_data(sensor)  # Fetch all sensor data

            # Color map for curves
            colors = [Qt.blue, Qt.green, Qt.yellow, Qt.red]

            graph_type = self.get_sensor_graph_type(sensor)
            graph_window = GraphWindow(graph_type, sensor, self.UI.mdiArea)
            graph_window.setStyleSheet(self.styleSheet() + graph_window.styleSheet())

            if graph_type == GraphType.LINECHART:
                # Add series
                for series in timeseries:
                    graph_window.graph.add_data(series['x'], series['y'], color=colors.pop(),
                                                legend_text=series['label'])

                graph_window.graph.set_title(sensor_label)

            if graph_type == GraphType.MAP:
                for data in channel_data:
                    gps = GPSGeodetic()
                    gps.from_bytes(data.data)
                    if gps.latitude != 0 and gps.longitude != 0:
                        graph_window.graph.addPosition(data.timestamps.start_timestamp, gps.latitude / 1e7,
                                                       gps.longitude / 1e7)
                        graph_window.setCursorPositionFromTime(data.timestamps.start_timestamp)

            if graph_window is not None:
                self.UI.mdiArea.addSubWindow(graph_window).setWindowTitle(sensor_label)
                self.sensors_graphs[sensor.id_sensor] = graph_window
                # self.UI.displayContents.layout().insertWidget(0,graph)

                graph_window.show()
                QApplication.instance().processEvents()

                graph_window.aboutToClose.connect(self.graph_was_closed)
                graph_window.requestData.connect(self.query_sensor_data)
                graph_window.graph.cursorMoved.connect(self.graph_cursor_changed)
                graph_window.graph.selectedAreaChanged.connect(self.graph_selected_area_changed)
                graph_window.graph.clearedSelectionArea.connect(self.on_timeview_clear_selection_requested)
                graph_window.zoomAreaRequested.connect(self.graph_zoom_area)
                graph_window.zoomResetRequested.connect(self.graph_zoom_reset)

                self.UI.mdiArea.tileSubWindows()
        else:
            # Remove from display
            try:
                if self.sensors_graphs[sensor.id_sensor] is not None:
                    self.UI.mdiArea.removeSubWindow(self.sensors_graphs[sensor.id_sensor].parent())
                    self.sensors_graphs[sensor.id_sensor].hide()
                    del self.sensors_graphs[sensor.id_sensor]
                    self.UI.mdiArea.tileSubWindows()
            except KeyError:
                pass
        self.update_tile_buttons_state()

    # @timing
    def get_sensor_data(self, sensor, start_time=None, end_time=None):
        QGuiApplication.setOverrideCursor(Qt.BusyCursor)
        task = DBSensorAllDataTask("Chargement des données...", self.dbMan, sensor, start_time, end_time,
                                   self.recordsets)

        process = BackgroundProcess([task])
        dialog = ProgressDialog(process, "Traitement")

        process.start()
        dialog.exec()
        QGuiApplication.restoreOverrideCursor()

        return task.results['timeseries'], task.results['channel_data']

    def update_tile_buttons_state(self):
        if self.sensors_graphs.keys().__len__() > 1:
            self.UI.btnTileAuto.setEnabled(True)
            self.UI.btnTileHorizontal.setEnabled(True)
            self.UI.btnTileVertical.setEnabled(True)
        else:
            self.UI.btnTileAuto.setEnabled(False)
            self.UI.btnTileHorizontal.setEnabled(False)
            self.UI.btnTileVertical.setEnabled(False)

    @pyqtSlot(QObject)
    def graph_was_closed(self, graph):
        for sensor_id, sensor_graph in self.sensors_graphs.items():
            if sensor_graph == graph:
                # self.sensors_graphs[sensor_id] = None
                del self.sensors_graphs[sensor_id]
                self.sensors_items[sensor_id].setChecked(False)
                break

        self.UI.mdiArea.tileSubWindows()
        self.update_tile_buttons_state()

    @pyqtSlot(float)
    def graph_cursor_changed(self, timestamp):
        current_time = timestamp / 1000
        for graph in self.sensors_graphs.values():
            if graph is not None:
                graph.setCursorPositionFromTime(current_time, False)

        pos = self.get_relative_timeview_pos(current_time)
        self.time_bar.setPos(pos,0)

        # Ensure time bar is visible if scrollable
        self.ensure_time_bar_visible(pos)

        self.UI.lblCursorTime.setText(datetime.fromtimestamp(current_time).strftime('%d-%m-%Y %H:%M:%S'))

    def ensure_time_bar_visible(self, pos):
        if self.UI.scrollTimeline.isVisible():
            max_visible_x = self.UI.graphTimeline.mapToScene(self.UI.graphTimeline.rect()).boundingRect().x() \
                            + self.UI.graphTimeline.mapToScene(self.UI.graphTimeline.rect()).boundingRect().width()
            min_visible_x = self.UI.graphTimeline.mapToScene(self.UI.graphTimeline.rect()).boundingRect().x()
            if pos < min_visible_x or pos > max_visible_x:
                self.UI.scrollTimeline.setValue(pos)

    @pyqtSlot(datetime, datetime)
    def graph_zoom_area(self, start_time, end_time):
        for graph in self.sensors_graphs.values():
            if graph is not None:
                graph.zoomAreaRequestTime(start_time, end_time)

    @pyqtSlot()
    def graph_zoom_reset(self):
        for graph in self.sensors_graphs.values():
            if graph is not None:
                graph.zoomResetRequest(False)

    @pyqtSlot(float, float)
    def graph_selected_area_changed(self, start_timestamp, end_timestamp):
        # Update timeview selection area
        start_pos = self.get_relative_timeview_pos(start_timestamp / 1000)
        end_pos = self.get_relative_timeview_pos(end_timestamp / 1000)
        self.timeview_selected(start_pos, end_pos)

        # Ensure time bar is visible if scrollable
        self.ensure_time_bar_visible(start_pos)

        # Update selection for each graph
        for graph in self.sensors_graphs.values():
            if graph is not None:
                graph.setSelectionAreaFromTime(start_timestamp, end_timestamp)

    @pyqtSlot(int)
    def timeview_scroll(self, pos):
        self.UI.graphTimeline.centerOn(pos / self.zoom_level, 0)

    @pyqtSlot(float)
    def timeview_clicked(self, x):
        self.time_bar.setPos(x, 0)
        if len(self.recordsets)==0:
            return

        # Find time corresponding to that position
        timestamp = self.get_time_from_timeview_pos(x)
        self.UI.lblCursorTime.setText(timestamp.strftime('%d-%m-%Y %H:%M:%S'))

        for graph in self.sensors_graphs.values():
            if graph is not None:
                # try:
                graph.setCursorPositionFromTime(timestamp, False)
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

        # Update selection for each graph
        for graph in self.sensors_graphs.values():
            if graph is not None:
                graph.setSelectionAreaFromTime(self.get_time_from_timeview_pos(start_x),
                                               self.get_time_from_timeview_pos(end_x))

    @pyqtSlot()
    def on_timeview_clear_selection_requested(self):
        self.timeScene.removeItem(self.selection_rec)
        self.UI.btnClearSelection.setEnabled(False)
        self.UI.btnTimeZoomSelection.setEnabled(False)

        # Clear all selected areas in graphs
        for graph in self.sensors_graphs.values():
            graph.clearSelectionArea()

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

    @pyqtSlot()
    def on_process_recordset(self):
        # Display Process Window
        window = ProcessSelectWindow(self.dbMan, self.recordsets)
        window.setStyleSheet(self.styleSheet())

        if window.exec() == QDialog.Accepted:
            self.dataUpdateRequest.emit("result", window.processed_data)
            self.dataDisplayRequest.emit("result", window.processed_data.id_processed_data)

    @pyqtSlot()
    def tile_graphs_horizontally(self):
        self.tile_graphs(True)

    @pyqtSlot()
    def tile_graphs_vertically(self):
        self.tile_graphs(False)

    def tile_graphs(self, horizontal: bool):
        if self.UI.mdiArea.subWindowList() is None:
            return

        position = QPoint(0, 0)

        for window in self.UI.mdiArea.subWindowList():
            if horizontal:
                rect = QRect(0, 0, self.UI.mdiArea.width() / len(self.UI.mdiArea.subWindowList()),
                             self.UI.mdiArea.height())
            else:
                rect = QRect(0, 0, self.UI.mdiArea.width(),
                             self.UI.mdiArea.height() / len(self.UI.mdiArea.subWindowList()))
            window.setGeometry(rect)
            window.move(position)
            if horizontal:
                position.setX(position.x() + window.width())
            else:
                position.setY(position.y() + window.height())

    @pyqtSlot()
    def tile_graphs_auto(self):
        self.UI.mdiArea.tileSubWindows()
