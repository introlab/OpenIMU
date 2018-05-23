import sys
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl, pyqtSlot, pyqtSignal, Qt, QObject, QDateTime, QPointF

import datetime

# This will automatically load qrc
import core_rc

class GPSView(QWebEngineView):

    aboutToClose = pyqtSignal(QObject)
    cursorMoved = pyqtSignal(datetime.datetime)

    def __init__(self, parent):

        self.path = []
        self.marker_position = []
        self.positions = {}

        self.reftime = datetime.datetime.now()

        super(QWebEngineView, self).__init__(parent)

        self.pageReady = False

        # Settings
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)

        self.loadFinished.connect(self.pageLoaded)

        # Load file from qrc
        self.setUrl(QUrl('qrc:/OpenIMU/html/map.html'))

        # 3IT = 45.3790193,-71.9430778
        # self.setCurrentPosition(45.3790193, -71.9430778)

    def closeEvent(self, QCloseEvent):
        self.aboutToClose.emit(self)

    def addPosition(self, timestamp, latitude, longitude):
        if timestamp < self.reftime:
            self.reftime = timestamp

        self.positions[timestamp] = QPointF(latitude, longitude)
        if self.pageReady is True:
            self.page().runJavaScript('addPosition(' + str(latitude) + ',' + str(longitude) + ');')
        else:
            # print('Cannot set position, page not ready, saving for later')
            self.path.append([latitude, longitude])

    def setCursorPositionFromTime(self, timestamp, emit_signal=False):

        timestamp -= datetime.timedelta(microseconds=timestamp.microsecond)
        position = None

        try:
            position = self.positions[timestamp]
        except KeyError:
            # Find the closest best position
            if timestamp < self.reftime:
                timestamp = self.reftime

            while timestamp >= self.reftime:
                timestamp = timestamp - datetime.timedelta(seconds=1)
                try:
                    position = self.positions[timestamp]
                    break
                except KeyError:
                    continue

        if position is not None:
            self.marker_position = [position.x(), position.y()]
            if self.pageReady:
                self.page().runJavaScript('setMarkerPosition(' + str(position.x()) + ',' + str(position.y()) + ');')

        #if emit_signal:
        #    self.cursorMoved.emit(timestamp)

    """
    def setCurrentPosition(self, latitude, longitude):
        if self.pageReady is True:
            self.page().runJavaScript('setCurrentPosition(' + str(latitude) + ',' + str(longitude) + ');')
        else:
            # print('Cannot set position, page not ready, saving for later')
            self.path.append([latitude, longitude])
    """
    def clearMap(self):
        if self.pageReady is True:
            self.page().runJavaScript('clearMap();')

    @pyqtSlot(bool)
    def pageLoaded(self, state):
        print('page loaded:', state)

        if state is True:
            self.pageReady = True
            for coords in self.path:
                self.page().runJavaScript('addPosition(' + str(coords[0]) + ',' + str(coords[1]) + ');')
            if self.marker_position != []:
                self.page().runJavaScript('setMarkerPosition(' + str(self.marker_position[0]) + ',' + str(self.marker_position[1]) + ');')



# Testing app
if __name__ == '__main__':

    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWidgets import QMainWindow, QPushButton
    from PyQt5.QtCore import Qt

    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle('GPSView - Test')
    window.resize(640, 480)

    view = GPSView(window)
    # view.setCurrentPosition(latitude=0, longitude=0)
    window.setCentralWidget(view)
    window.show()

    sys.exit(app.exec_())

