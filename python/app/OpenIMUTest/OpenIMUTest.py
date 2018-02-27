from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMdiSubWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtQuickWidgets import QQuickWidget

from PyQt5.QtCore import Qt, QUrl
from Charts import IMUChartView

import DataImporter as importer
import Algorithms as algo
import numpy as np
import Jupyter
import os
import signal

from PyQt5.QtCore import pyqtProperty, QCoreApplication, QObject
from PyQt5.QtQml import qmlRegisterType, QQmlComponent, QQmlEngine

# This is auto-generated from Qt .ui files
from MainWindow_ui import Ui_MainWindow

# This is auto-generated from Qt .qrc files
import core_rc

import sys

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow,self).__init__(parent=parent)
        self.UI = Ui_MainWindow()
        self.UI.setupUi(self)

        # Create chart and mdiWindow
        self.chartView = self.create_chart_view(test_data=False)
        self.add_mdi_widget(widget=self.chartView, title='QtChart')

        # Create WebEngineView
        self.jupyter_pid = Jupyter.start_jupyter()
        self.webView = QWebEngineView(self)
        self.webView.setUrl(QUrl('http://localhost:8888/'))
        self.add_mdi_widget(widget=self.webView, title='WebEngineView')

        # QML engine and widget
        self.quickWidget = QQuickWidget(self)
        self.quickWidget.setMinimumSize(400,200)
        self.quickWidget.setSource(QUrl.fromLocalFile("resources/test.qml"))
        self.add_mdi_widget(widget=self.quickWidget,title='QML widget')

        # Re-arrange subwindows
        self.UI.mdiArea.tileSubWindows()

        # Load test data
        self.rawData =  importer.load_mat_file('resources/test_data.mat')['data2']
        self.rawData[:, 0] = self.rawData[:, 0] * 24 * 60 * 60
        self.intData = algo.resample_data(self.rawData, 100)


        # Add to plot (accelerometer x)
        self.chartView.add_data(self.intData[:, 0], self.intData[:, 1], Qt.red)
        self.chartView.add_data(self.intData[:, 0], self.intData[:, 2], Qt.green)
        self.chartView.add_data(self.intData[:, 0], self.intData[:, 3], Qt.blue)
        self.chartView.set_title( ("Accelerometer data with %d points " \
         "(OpenGL Accelerated Series)" \
         % (len(self.intData))))

        # Add counts
        self.epoch_secs = 60
        self.sample_rate = 100
        [nb_epochs, counts] = algo.freedson_adult_1998(self.rawData,self.epoch_secs, self.sample_rate)
        self.chartView2 = self.create_chart_view(test_data=False)
        self.add_mdi_widget(widget=self.chartView2, title='QtChart')
        self.chartView2.add_data(np.array(range(0, int(nb_epochs))), counts, Qt.blue)
        self.chartView2.set_title(("Counts with epoch size %d secs" % self.epoch_secs))

        # Maximize window
        self.showMaximized()

    def __del__(self):
        print('stopping jupyter process ... pid:',self.jupyter_pid, 'kill', signal.SIGINT)
        os.kill(self.jupyter_pid, 2)  # or signal.SIGKILL


    def add_mdi_widget(self, widget=None, title=''):
        sub_window = QMdiSubWindow(self.UI.mdiArea)

        if widget is not None:
            widget.show()
            sub_window.setWidget(widget)
            sub_window.setWindowTitle(title)

        sub_window.resize(640,480)
        self.UI.mdiArea.addSubWindow(sub_window)
        return sub_window

    def create_chart_view(self, test_data=False):
        chart_view = IMUChartView(self)
        if test_data is True:
            chart_view.add_test_data()
        return chart_view


# Main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    window = MainWindow()
    sys.exit(app.exec_())