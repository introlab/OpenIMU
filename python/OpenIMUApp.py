from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMdiSubWindow
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton
# from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings
from PyQt5.QtQuickWidgets import QQuickWidget

from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal
from libopenimu.qt.Charts import IMUChartView

import libopenimu.importers.DataImporter as importer
import libopenimu.algorithms.Algorithms as algo
import numpy as np
import libopenimu.jupyter.Jupyter as Jupyter
import os
import signal

from PyQt5.QtCore import pyqtProperty, QCoreApplication, QObject
from PyQt5.QtQml import qmlRegisterType, QQmlComponent, QQmlEngine

# This is auto-generated from Qt .ui files
from resources.ui.python.MainWindow_ui import Ui_MainWindow
from resources.ui.python.StartDialog_ui import Ui_StartDialog
from ImportWindow import ImportWindow

# This is auto-generated from Qt .qrc files
import core_rc

import sys

import libopenimu


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow,self).__init__(parent=parent)
        self.UI = Ui_MainWindow()
        self.UI.setupUi(self)

        self.startWindow = QDialog()
        startdialog = Ui_StartDialog()
        startdialog.setupUi(self.startWindow)

        #Signals/Slots setup
        startdialog.btnImport.clicked.connect(self.import_clicked)
        startdialog.btnOpen.clicked.connect(self.open_clicked)
        startdialog.btnNew.clicked.connect(self.new_clicked)
        startdialog.btnQuit.clicked.connect(self.quit_clicked)

        if (self.startWindow.exec()==QDialog.Rejected):
            # User closed the dialog - exits!
            exit(0)


        """
        # Create chart and mdiWindow
        self.chartView = self.create_chart_view(test_data=False)
        self.add_mdi_widget(widget=self.chartView, title='QtChart')

        # Create WebEngineView
        self.jupyter = Jupyter.JupyterNotebook()
        self.jupyter.start()
        self.webView = QWebEngineView(self)
        self.webView.setUrl(QUrl('http://localhost:8888/notebooks/Notebook.ipynb'))
        # self.webView.setUrl(QUrl('http://google.ca/'))
        self.add_mdi_widget(widget=self.webView, title='WebEngineView')
        # Signals
        self.webView.urlChanged.connect(self.urlChanged)

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
        self.chartView.add_data(self.intData[:, 0], self.intData[:, 1], Qt.red, 'Accelerometer_X')
        self.chartView.add_data(self.intData[:, 0], self.intData[:, 2], Qt.green, 'Accelerometer_Y')
        self.chartView.add_data(self.intData[:, 0], self.intData[:, 3], Qt.blue, 'Accelerometer_Z')
        self.chartView.set_title( ("Accelerometer data with %d points " \
         "(OpenGL Accelerated Series)" \
         % (len(self.intData))))

        # Add counts
        self.epoch_secs = 60
        self.sample_rate = 100
        [nb_epochs, counts] = algo.freedson_adult_1998(self.rawData,self.epoch_secs, self.sample_rate)
        self.chartView2 = self.create_chart_view(test_data=False)
        self.add_mdi_widget(widget=self.chartView2, title='QtChart')
        self.chartView2.add_data(np.array(range(0, int(nb_epochs))), counts, Qt.blue, 'Counts')
        self.chartView2.set_title(("Counts with epoch size %d secs" % self.epoch_secs))
        """


        # Maximize window
        self.showMaximized()

    @pyqtSlot(QUrl)
    def urlChanged(self,url):
        print('url: ', url)

    @pyqtSlot()
    def import_clicked(self):
        importdialog = ImportWindow()

        if (importdialog.exec() == QDialog.Accepted):
            if (self.startWindow.isVisible()):
                self.startWindow.accept()


    @pyqtSlot()
    def open_clicked(self):
            if (self.startWindow.isVisible()):
                self.startWindow.accept()

    @pyqtSlot()
    def new_clicked(self):
        importdialog = ImportWindow()
        importdialog.noImportUI = True

        if (importdialog.exec() == QDialog.Accepted):
            if (self.startWindow.isVisible()):
                self.startWindow.accept()

    @pyqtSlot()
    def quit_clicked(self):
        exit(0)

    def closeEvent(self, event):
        print('closeEvent')
        """self.jupyter.stop()
        del self.jupyter
        self.jupyter = None
        """

    def __del__(self):
        print('Done!')

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

    # WebEngine settings
    # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
    # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
    # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
    # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls,True)
    # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)

    window = MainWindow()
    sys.exit(app.exec_())