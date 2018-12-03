from PyQt5.QtWidgets import QWidget, QButtonGroup, QAbstractButton
from PyQt5.QtCore import pyqtSignal, QObject, QEvent, pyqtSlot

from resources.ui.python.GraphWidget_ui import Ui_frmGraphWidget
from libopenimu.qt.Charts import IMUChartView
from libopenimu.qt.GPSView import GPSView
from libopenimu.qt.BaseGraph import GraphInteractionMode
from libopenimu.models.Sensor import Sensor

import datetime


class GraphType:
    UNKNOWN = -1
    LINECHART = 0
    MAP = 1
    BARCHART = 2


class GraphWindow(QWidget):

    aboutToClose = pyqtSignal(QObject)
    requestData = pyqtSignal(Sensor, datetime.datetime, datetime.datetime)

    def __init__(self, graph_type: GraphType, sensor: Sensor, parent=None):
        super(QWidget, self).__init__(parent=parent)
        self.UI = Ui_frmGraphWidget()
        self.UI.setupUi(self)

        self.UI.frameTools.hide()

        self.sensor = sensor

        # Create correct graph
        self.graph = None
        if graph_type == GraphType.LINECHART:
            self.graph = IMUChartView(self)

        if graph_type == GraphType.MAP:
            self.graph = GPSView(self)

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
        self.UI.btnClearSelection.clicked.connect(self.clearSelectionRequest)
        self.UI.btnZoomArea.clicked.connect(self.zoomAreaRequest)
        self.UI.btnZoomIn.clicked.connect(self.zoomInRequest)
        self.UI.btnZoomOut.clicked.connect(self.zoomOutRequest)
        self.UI.btnZoomReset.clicked.connect(self.zoomResetRequest)
        self.UI.btnDataInfos.clicked.connect(self.dataInfosRequest)
        self.mode_buttons_group.buttonClicked.connect(self.graph_interaction_mode_changed)
        self.graph.selectedAreaChanged.connect(self.graph_selection_changed)
        self.graph.clearedSelectionArea.connect(self.graph_selection_changed)

        self.UI.btnMove.setChecked(True)

    def event(self, e):
        if e.type() == QEvent.Enter:
            # Over the widget - show toolbar
            self.UI.frameTools.show()

        if e.type() == QEvent.Leave:
            # Not over the widget - hide toolbar
            self.UI.frameTools.hide()

        if e.type() == QEvent.Close:
            self.aboutToClose.emit(self)

        return super(QWidget, self).event(e)

    def setCursorPositionFromTime(self, timestamp, emit_signal=False):
        if self.graph is not None:
            self.graph.setCursorPositionFromTime(timestamp, emit_signal)

    def setSelectionAreaFromTime(self, start_time, end_time, emit_signal=False):
        if self.graph is not None:
            self.graph.setSelectionAreaFromTime(start_time, end_time, emit_signal)

    def clearSelectionArea(self):
        if self.graph is not None:
            self.graph.clearSelectionArea(False)
            self.UI.btnClearSelection.setEnabled(False)

    def update_zoom_buttons_state(self):
        self.UI.btnZoomArea.setEnabled(self.graph.selection_rec is not None)
        self.UI.btnZoomOut.setEnabled(self.graph.is_zoomed)
        self.UI.btnZoomReset.setEnabled(self.graph.is_zoomed)

    @pyqtSlot()
    def clearSelectionRequest(self):
        self.graph.clearSelectionArea(True)
        self.UI.btnClearSelection.setEnabled(False)

    @pyqtSlot()
    def zoomAreaRequest(self):
        if self.graph:
            self.graph.zoom_area()
            self.requestData.emit(self.sensor, self.graph.get_displayed_start_time(), self.graph.get_displayed_end_time())
        self.update_zoom_buttons_state()

    @pyqtSlot()
    def zoomOutRequest(self):
        if self.graph:
            self.graph.zoom_out()
            self.requestData.emit(self.sensor, self.graph.get_displayed_start_time(),
                                  self.graph.get_displayed_end_time())
        self.update_zoom_buttons_state()

    @pyqtSlot()
    def zoomInRequest(self):
        if self.graph:
            self.graph.zoom_in()
            self.requestData.emit(self.sensor, self.graph.get_displayed_start_time(),
                                  self.graph.get_displayed_end_time())
        self.update_zoom_buttons_state()

    @pyqtSlot()
    def zoomResetRequest(self):
        if self.graph:
            self.graph.zoom_reset()
        self.update_zoom_buttons_state()

    @pyqtSlot()
    def dataInfosRequest(self):
        return

    @pyqtSlot()
    def graph_selection_changed(self):
        self.UI.btnClearSelection.setEnabled(self.graph.selection_rec is not None)
        self.update_zoom_buttons_state()

    @pyqtSlot(QAbstractButton)
    def graph_interaction_mode_changed(self, button = QAbstractButton):
        if button == self.UI.btnSelect:
            self.graph.set_interaction_mode(GraphInteractionMode.SELECT)
        if button == self.UI.btnMove:
            self.graph.set_interaction_mode(GraphInteractionMode.MOVE)

