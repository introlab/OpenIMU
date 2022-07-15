from PySide6.QtWidgets import QWidget, QButtonGroup, QAbstractButton
from PySide6.QtCore import Signal, QObject, QEvent, Slot

from resources.ui.python.GraphWidget_ui import Ui_frmGraphWidget
from libopenimu.qt.Charts import IMUChartView
from libopenimu.qt.BeaconsView import BeaconsView
from libopenimu.qt.BaseGraph import GraphInteractionMode
from libopenimu.qt.DataInfosWidget import DataInfosWidget

from libopenimu.models.Sensor import Sensor

import datetime


class GraphType:
    UNKNOWN = -1
    LINECHART = 0
    MAP = 1
    BARCHART = 2
    BEACON = 3


class GraphWindow(QWidget):

    aboutToClose = Signal(QObject)
    requestData = Signal(Sensor, datetime.datetime, datetime.datetime)
    zoomAreaRequested = Signal(datetime.datetime, datetime.datetime)
    zoomResetRequested = Signal()

    def __init__(self, graph_type: GraphType, sensor: Sensor, parent=None):
        super().__init__(parent=parent)
        self.UI = Ui_frmGraphWidget()
        self.UI.setupUi(self)

        self.sensor = sensor

        # Create correct graph
        self.graph = None
        if graph_type == GraphType.LINECHART:
            self.graph = IMUChartView()

        if graph_type == GraphType.MAP:
            from libopenimu.qt.GPSView import GPSView
            self.graph = GPSView(self)
            self.UI.btnMove.hide()
            self.UI.btnSelect.hide()
            self.UI.btnClearSelection.hide()
            self.UI.btnZoomArea.hide()

        if graph_type == GraphType.BEACON:
            self.graph = BeaconsView(self)
            self.UI.frameTools.hide()

        if self.graph is None:
            print("GraphWindow: Undefined graph type.")
            return
        self.UI.wdgChart.layout().addWidget(self.graph)

        # Initial UI state
        self.UI.btnClearSelection.setEnabled(False)
        self.mode_buttons_group = QButtonGroup()
        self.mode_buttons_group.addButton(self.UI.btnSelect)
        self.mode_buttons_group.addButton(self.UI.btnMove)

        self.update_zoom_buttons_state()

        # Connect signals
        self.UI.btnClearSelection.clicked.connect(self.clear_selection_request)
        self.UI.btnZoomArea.clicked.connect(self.zoom_area_request)
        self.UI.btnZoomIn.clicked.connect(self.zoom_in_request)
        self.UI.btnZoomOut.clicked.connect(self.zoom_out_request)
        self.UI.btnZoomReset.clicked.connect(self.zoom_reset_request)
        self.UI.btnDataInfos.clicked.connect(self.data_infos_request)
        self.mode_buttons_group.buttonClicked.connect(self.graph_interaction_mode_changed)
        self.graph.selectedAreaChanged.connect(self.graph_selection_changed)
        self.graph.clearedSelectionArea.connect(self.graph_selection_changed)

        # self.UI.btnMove.setChecked(True)
        # self.graph.set_interaction_mode(GraphInteractionMode.MOVE)
        self.UI.btnSelect.setChecked(True)
        self.graph.set_interaction_mode(GraphInteractionMode.SELECT)

    def event(self, e):
        if e.type() == QEvent.Enter:
            # Over the widget - show toolbar
            # self.UI.frameTools.show()
            pass

        if e.type() == QEvent.Leave:
            # Not over the widget - hide toolbar
            # self.UI.frameTools.hide()
            pass

        if e.type() == QEvent.Close:
            self.aboutToClose.emit(self)

        return super().event(e)

    def set_cursor_position_from_time(self, timestamp, emit_signal=False):
        if self.graph is not None:
            self.graph.set_cursor_position_from_time(timestamp, emit_signal)

    def set_selection_area_from_time(self, start_time, end_time, emit_signal=False):
        if self.graph is not None:
            self.graph.set_selection_area_from_time(start_time, end_time, emit_signal)
            self.update_zoom_buttons_state()

    def clear_selection_area(self):
        if self.graph is not None:
            self.graph.clear_selection_area(False)
            self.UI.btnClearSelection.setEnabled(False)
            self.update_zoom_buttons_state()

    def update_zoom_buttons_state(self):
        self.UI.btnZoomArea.setEnabled(self.graph.selection_rec is not None)
        self.UI.btnZoomOut.setEnabled(self.graph.is_zoomed)
        self.UI.btnZoomReset.setEnabled(self.graph.is_zoomed)

    @Slot()
    def clear_selection_request(self):
        self.graph.clear_selection_area(True)
        self.UI.btnClearSelection.setEnabled(False)

    @Slot()
    def zoom_area_request(self):
        if self.graph:
            self.graph.zoom_area()
            self.requestData.emit(self.sensor, self.graph.get_displayed_start_time(), self.graph.get_displayed_end_time())
            self.zoomAreaRequested.emit(self.graph.get_displayed_start_time(), self.graph.get_displayed_end_time())
        self.update_zoom_buttons_state()

    def zoom_area_request_time(self, start_time: float, end_time: float, emit_signal=False):
        if self.graph:
            self.graph.set_selection_area_from_time(start_time, end_time, emit_signal)
            self.graph.zoom_area()

    @Slot()
    def zoom_out_request(self):
        if self.graph:
            self.graph.zoom_out()
            self.requestData.emit(self.sensor, self.graph.get_displayed_start_time(),
                                  self.graph.get_displayed_end_time())
            self.zoomAreaRequested.emit(self.graph.get_displayed_start_time(), self.graph.get_displayed_end_time())
        self.update_zoom_buttons_state()

    @Slot()
    def zoom_in_request(self):
        if self.graph:
            self.graph.zoom_in()
            self.requestData.emit(self.sensor, self.graph.get_displayed_start_time(),
                                  self.graph.get_displayed_end_time())
            self.zoomAreaRequested.emit(self.graph.get_displayed_start_time(), self.graph.get_displayed_end_time())
        self.update_zoom_buttons_state()

    @Slot()
    def zoom_reset_request(self, emit_signal=True):
        if self.graph:
            self.graph.zoom_reset()
            if emit_signal:
                self.zoomResetRequested.emit()
        self.update_zoom_buttons_state()

    @Slot()
    def data_infos_request(self):
        infos = DataInfosWidget(self.sensor, self.graph.total_samples, parent=self)
        # infos.setStyleSheet(self.styleSheet())
        infos.exec()

    @Slot()
    def graph_selection_changed(self):
        self.UI.btnClearSelection.setEnabled(self.graph.selection_rec is not None)
        self.update_zoom_buttons_state()

    @Slot(QAbstractButton)
    def graph_interaction_mode_changed(self, button = QAbstractButton):
        if button == self.UI.btnSelect:
            self.graph.set_interaction_mode(GraphInteractionMode.SELECT)
        if button == self.UI.btnMove:
            self.graph.set_interaction_mode(GraphInteractionMode.MOVE)

