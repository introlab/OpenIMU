from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtCore import QUrl, Slot, Signal, QPointF

from libopenimu.qt.BaseGraph import BaseGraph

import numpy as np
import datetime
import collections
import sys


class GPSView(QWebEngineView, BaseGraph):

    # aboutToClose = Signal(QObject)
    cursorMoved = Signal(float)

    def __init__(self, parent):
        BaseGraph.__init__(self)
        QWebEngineView.__init__(self, parent)
        self.path = []
        self.marker_position = []
        self.positions = collections.OrderedDict()
        self.pageReady = False

        # Settings
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)

        self.loadFinished.connect(self.page_loaded)

        # Load file from qrc
        self.setUrl(QUrl('qrc:/OpenIMU/html/map.html'))

    # def closeEvent(self, QCloseEvent):
    #    self.aboutToClose.emit(self)

    def add_position(self, timestamp, latitude, longitude):
        # if timestamp < self.reftime:
        #    self.reftime = timestamp
        if isinstance(timestamp, datetime.datetime):
            timestamp = timestamp.timestamp()

        self.positions[timestamp] = QPointF(latitude, longitude)
        self.total_samples += 1

        if self.pageReady is True:
            self.page().runJavaScript('addPosition(' + str(latitude) + ',' + str(longitude) + ');')
        else:
            self.path.append([latitude, longitude])

    def set_cursor_position_from_time(self, timestamp, emit_signal=False):

        # timestamp -= datetime.timedelta(microseconds=timestamp.microsecond)
        # position = None

        try:
            position = self.positions[timestamp]  # Right on the value!
        except KeyError:
            # Find the closest best position
            # if timestamp < self.reftime:
            #    timestamp = self.reftime
            # start_timestamp = next(iter(self.positions))

            # if type(timestamp) is datetime.datetime:
            if isinstance(timestamp, datetime.datetime):
                timestamp = timestamp.timestamp()

            # Find nearest point
            idx = (np.abs(np.asarray(list(self.positions.keys())) - timestamp)).argmin()
            position = list(self.positions.values())[idx]

        if position is not None:
            self.marker_position = [position.x(), position.y()]
            if self.pageReady:
                self.page().runJavaScript('setMarkerPosition(' + str(position.x()) + ',' + str(position.y()) + ');')

    def clearMap(self):
        if self.pageReady:
            self.page().runJavaScript('clearMap();')

    def zoom_reset(self):
        if self.pageReady:
            self.page().runJavaScript('resetZoom();')

    def zoom_in(self):
        if self.pageReady:
            self.page().runJavaScript('zoomIn();')

    def zoom_out(self):
        if self.pageReady:
            self.page().runJavaScript('zoomOut();')

    def clear_selection_area(self, emit_signal=False):
        if self.pageReady:
            self.page().runJavaScript('clearSelectedPath();')

    def set_selection_area_from_time(self, start_time, end_time, emit_signal=False):
        self.clear_selection_area()
        if not start_time:
            return
        try:
            start_pos = self.positions[start_time]  # Right on the value!
        except KeyError:
            # Find the closest best position
            # if timestamp < self.reftime:
            #    timestamp = self.reftime
            # start_timestamp = next(iter(self.positions))

            if isinstance(start_time, datetime.datetime):
                start_time = start_time.timestamp()

            # Find nearest point
            start_pos = (np.abs(np.asarray(list(self.positions.keys())) - start_time)).argmin()

        try:
            end_pos = self.positions[end_time]  # Right on the value!
        except KeyError:
            # Find the closest best position
            # if timestamp < self.reftime:
            #    timestamp = self.reftime
            # start_timestamp = next(iter(self.positions))

            if isinstance(end_time, datetime.datetime):
                end_time = end_time.timestamp()

            # Find nearest point
            end_pos = (np.abs(np.asarray(list(self.positions.keys())) - end_time)).argmin()

        if start_pos is not None and end_pos is not None:
            if self.pageReady:
                for i in range(start_pos, end_pos):
                    self.page().runJavaScript('addSelectedPosition(' + str(list(self.positions.values())[i].x()) + ','
                                              + str(list(self.positions.values())[i].y()) + ');')

    @property
    def is_zoomed(self):
        return True

    @Slot(bool)
    def page_loaded(self, state):
        # print('page loaded:', state)

        if state is True:
            self.pageReady = True
            for coords in self.path:
                self.page().runJavaScript('addPosition(' + str(coords[0]) + ',' + str(coords[1]) + ');')
            if self.marker_position:
                self.page().runJavaScript('setMarkerPosition(' + str(self.marker_position[0]) + ',' + str(self.marker_position[1]) + ');')


# Testing app
if __name__ == '__main__':

    from PySide6.QtWidgets import QApplication
    from PySide6.QtWidgets import QMainWindow

    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle('GPSView - Test')
    window.resize(640, 480)

    view = GPSView(window)
    # view.setCurrentPosition(latitude=0, longitude=0)
    window.setCentralWidget(view)
    window.show()

    sys.exit(app.exec_())

