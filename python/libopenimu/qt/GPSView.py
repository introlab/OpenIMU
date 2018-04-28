import sys

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QDir, QUrl
# This will automatically load qrc
import core_rc

class GPSView(QWebEngineView):
    def __init__(self, parent):
        super(QWebEngineView, self).__init__(parent)

        # Load file from qrc
        self.setUrl(QUrl('qrc:/OpenIMU/html/map.html'))


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
    window.setCentralWidget(view)
    window.show()

    sys.exit(app.exec_())

