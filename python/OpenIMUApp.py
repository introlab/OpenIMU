from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMdiSubWindow, QMdiArea
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon, QFont, QDragEnterEvent

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

        self.loadDemoData()

        self.UI.mdiArea

    def loadDemoData(self):
        #Load demo structure
        item = self.create_group_item("Groupe 1", 0)
        self.UI.treeDataSet.addTopLevelItem(item)

        parent = item
        item = self.create_participant_item("Participant B",1)
        parent.addChild(item)

        item2 = self.create_records_item()
        item.addChild(item2)

        item3 = self.create_record_item("Enregistrement 1 (27/03/2018)",0)
        item2.addChild(item3)

        item5 = self.create_sensor_item("Accéléromètre", 0)
        item3.addChild(item5)

        item5 = self.create_sensor_item("Gyromètre", 1)
        item3.addChild(item5)

        item5 = self.create_sensor_item("GPS", 2)
        item3.addChild(item5)

        item4 = self.create_subrecord_item("AM",0)
        item3.addChild(item4)

        item5 = self.create_sensor_item("Accéléromètre", 0)
        item4.addChild(item5)

        item5 = self.create_sensor_item("Gyromètre", 1)
        item4.addChild(item5)

        item5 = self.create_sensor_item("GPS", 2)
        item4.addChild(item5)

        item4 = self.create_subrecord_item("PM", 1)
        item3.addChild(item4)

        item5 = self.create_sensor_item("Accéléromètre", 0)
        item4.addChild(item5)

        item5 = self.create_sensor_item("Gyromètre", 1)
        item4.addChild(item5)

        item5 = self.create_sensor_item("GPS", 2)
        item4.addChild(item5)


        item3 = self.create_record_item("Enregistrement 2 (29/03/2018)", 1)
        item2.addChild(item3)

        item2 = self.create_results_item()
        item.addChild(item2)

        item3 = self.create_result_item("Nombre de pas (par enregistrement)",0)
        item2.addChild(item3)

        item3 = self.create_result_item("Niveau d'activité (total)", 1)
        item2.addChild(item3)

        item = self.create_participant_item("Participant C", 2)
        parent.addChild(item)

        parent = item
        item = self.create_records_item()
        parent.addChild(item)

        item3 = self.create_record_item("Enregistrement 1 (23/03/2018)", 3)
        item.addChild(item3)

        item = self.create_group_item("Groupe 2", 1)
        self.UI.treeDataSet.addTopLevelItem(item)

        parent = item
        item = self.create_participant_item("Participant D", 3)
        parent.addChild(item)

        item = self.create_participant_item("Participant A", 0)
        self.UI.treeDataSet.addTopLevelItem(item)

    def create_group_item(self, name, id):
        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setIcon(0, QIcon(':/OpenIMU/icons/group.png'))
        item.setData(0, Qt.UserRole, id);
        item.setData(1, Qt.UserRole, 'group');
        item.setFont(0, QFont('Helvetica', 14, QFont.Bold))
        return item

    def create_participant_item(self,name,id):
        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setIcon(0, QIcon(':/OpenIMU/icons/participant.png'))
        item.setData(0, Qt.UserRole, id);
        item.setData(1, Qt.UserRole, 'participant');
        item.setFont(0, QFont('Helvetica', 13, QFont.Bold))
        return item

    def create_records_item(self):
        item = QTreeWidgetItem()
        item.setText(0, 'Enregistrements')
        item.setIcon(0, QIcon(':/OpenIMU/icons/records.png'))
        item.setData(1, Qt.UserRole, 'recordsets');
        item.setFont(0, QFont('Helvetica', 12, QFont.StyleItalic + QFont.Bold))
        return item

    def create_results_item(self):
        item = QTreeWidgetItem()
        item.setText(0, 'Résultats')
        item.setIcon(0, QIcon(':/OpenIMU/icons/results.png'))
        item.setData(1, Qt.UserRole, 'results');
        item.setFont(0, QFont('Helvetica', 12, QFont.StyleItalic + QFont.Bold))
        return item

    def create_record_item(self,name,id):
        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setIcon(0, QIcon(':/OpenIMU/icons/recordset.png'))
        item.setData(0, Qt.UserRole, id);
        item.setData(1, Qt.UserRole, 'recordset');
        item.setFont(0, QFont('Helvetica', 12, QFont.Bold))
        return item

    def create_subrecord_item(self,name,id):
        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setIcon(0, QIcon(':/OpenIMU/icons/subrecord.png'))
        item.setData(0, Qt.UserRole, id);
        item.setData(1, Qt.UserRole, 'subrecord');
        item.setFont(0, QFont('Helvetica', 12, QFont.Bold))
        return item

    def create_sensor_item(self,name,id):
        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setIcon(0, QIcon(':/OpenIMU/icons/sensor.png'))
        item.setData(0, Qt.UserRole, id);
        item.setData(1, Qt.UserRole, 'sensor');
        item.setFont(0, QFont('Helvetica', 12))
        return item

    def create_result_item(self,name,id):
        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setIcon(0, QIcon(':/OpenIMU/icons/result.png'))
        item.setData(0, Qt.UserRole, id);
        item.setData(1, Qt.UserRole, 'result');
        item.setFont(0, QFont('Helvetica', 12))
        return item

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

    """
    def dragEnterEvent(self, event):
        print (event.answerRect())
        print (self.UI.mdiArea.rect().adjusted(self.UI.mdiArea.x(),self.UI.mdiArea.y(),0,0))

        if (event.answerRect().intersects(self.UI.mdiArea.rect())):
            print("OK")
            #event.accept()
        else:
            print("Not OK")
            #event.refuse()

    def dropEvent(self, QDropEvent):
        print("DROP!")
    """
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