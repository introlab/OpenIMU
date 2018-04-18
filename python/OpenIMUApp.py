from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon, QFont, QDragEnterEvent

# from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings
from PyQt5.QtQuickWidgets import QQuickWidget

from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal
from libopenimu.qt.Charts import IMUChartView

import numpy as np
import libopenimu.jupyter.Jupyter as Jupyter

# UI
from resources.ui.python.MainWindow_ui import Ui_MainWindow
from resources.ui.python.StartDialog_ui import Ui_StartDialog
from libopenimu.qt.ImportWindow import ImportWindow
from libopenimu.qt.GroupWindow import GroupWindow
from libopenimu.qt.ParticipantWindow import ParticipantWindow
from libopenimu.qt.RecordsetWindow import RecordsetWindow
from libopenimu.qt.ResultWindow import ResultWindow
from libopenimu.qt.StartWindow import StartWindow

# Models
from libopenimu.models.Group import Group
from libopenimu.models.Participant import Participant

# Database
from libopenimu.db.DBManager import DBManager

# This is auto-generated from Qt .qrc files

import sys

import libopenimu


class MainWindow(QMainWindow):

    currentFileName = ''
    dbMan = []

    def __init__(self, parent=None):
        super(QMainWindow,self).__init__(parent=parent)
        self.UI = Ui_MainWindow()
        self.UI.setupUi(self)

        startWindow = StartWindow()

        if (startWindow.exec()==QDialog.Rejected):
            # User closed the dialog - exits!
            exit(0)

        # Init database manager
        self.currentFileName = startWindow.fileName
        self.dbMan = DBManager(self.currentFileName)

        # Setup signals and slots
        self.setupSignals()

        # Maximize window
        self.showMaximized()

        # Load data
        self.loadDemoData()

    def setupSignals(self):
        self.UI.treeDataSet.itemClicked.connect(self.tree_item_clicked)


    def loadDemoData(self):
        #Load demo structure
        new_group = Group(id_group=0, name="Groupe 1", description="Ceci est un premier groupe de démonstration")

        item = self.create_group_item(new_group)
        self.UI.treeDataSet.addTopLevelItem(item)
        self.UI.treeDataSet.groups[new_group.id_group] = new_group

        parent = item
        new_part = Participant(id_participant=1, name="Participant B", description="Participant dans un groupe", group=new_group)
        item = self.create_participant_item(new_part)
        parent.addChild(item)
        self.UI.treeDataSet.participants[new_part.id_participant] = new_part

        item2 = self.create_records_item()
        item.addChild(item2)

        item3 = self.create_record_item("Enregistrement 1 (27/03/2018)",0)
        item2.addChild(item3)

        """ item5 = self.create_sensor_item("Accéléromètre", 0)
        item3.addChild(item5)

        item5 = self.create_sensor_item("Gyromètre", 1)
        item3.addChild(item5)

        item5 = self.create_sensor_item("GPS", 2)
        item3.addChild(item5)
        """
        item4 = self.create_subrecord_item("AM",0)
        item3.addChild(item4)
        """
        item5 = self.create_sensor_item("Accéléromètre", 0)
        item4.addChild(item5)

        item5 = self.create_sensor_item("Gyromètre", 1)
        item4.addChild(item5)

        item5 = self.create_sensor_item("GPS", 2)
        item4.addChild(item5)
        """
        item4 = self.create_subrecord_item("PM", 1)
        item3.addChild(item4)

        """ item5 = self.create_sensor_item("Accéléromètre", 0)
        item4.addChild(item5)

        item5 = self.create_sensor_item("Gyromètre", 1)
        item4.addChild(item5)

        item5 = self.create_sensor_item("GPS", 2)
        item4.addChild(item5)
        """

        item3 = self.create_record_item("Enregistrement 2 (29/03/2018)", 1)
        item2.addChild(item3)

        item2 = self.create_results_item()
        item.addChild(item2)

        item3 = self.create_result_item("Nombre de pas (par enregistrement)",0)
        item2.addChild(item3)

        item3 = self.create_result_item("Niveau d'activité (total)", 1)
        item2.addChild(item3)

        new_part = Participant(id_participant=2, name="Participant C", group=new_group)
        item = self.create_participant_item(new_part)
        parent.addChild(item)
        self.UI.treeDataSet.participants[new_part.id_participant] = new_part

        parent = item
        item = self.create_records_item()
        parent.addChild(item)

        item3 = self.create_record_item("Enregistrement 1 (23/03/2018)", 3)
        item.addChild(item3)

        new_group = Group(id_group=1, name="Groupe 2", description="Ceci est un deuxième groupe de démonstration")

        item = self.create_group_item(new_group)
        self.UI.treeDataSet.addTopLevelItem(item)
        self.UI.treeDataSet.groups[new_group.id_group] = new_group

        parent = item
        new_part = Participant(id_participant=3, name="Participant D", group=new_group)
        item = self.create_participant_item(new_part)
        parent.addChild(item)
        self.UI.treeDataSet.participants[new_part.id_participant] = new_part

        new_part = Participant(id_participant=0, name="Participant A", description="Participant sans groupe")
        item = self.create_participant_item(new_part)
        self.UI.treeDataSet.participants[new_part.id_participant] = new_part
        self.UI.treeDataSet.addTopLevelItem(item)

    def create_group_item(self, group):
        item = QTreeWidgetItem()
        item.setText(0, group.name)
        item.setIcon(0, QIcon(':/OpenIMU/icons/group.png'))
        item.setData(0, Qt.UserRole, group.id_group)
        item.setData(1, Qt.UserRole, 'group')
        item.setFont(0, QFont('Helvetica', 14, QFont.Bold))
        return item

    def create_participant_item(self,part):
        item = QTreeWidgetItem()
        item.setText(0, part.name)
        item.setIcon(0, QIcon(':/OpenIMU/icons/participant.png'))
        item.setData(0, Qt.UserRole, part.id_participant)
        item.setData(1, Qt.UserRole, 'participant')
        item.setFont(0, QFont('Helvetica', 13, QFont.Bold))
        return item

    def create_records_item(self):
        item = QTreeWidgetItem()
        item.setText(0, 'Enregistrements')
        item.setIcon(0, QIcon(':/OpenIMU/icons/records.png'))
        item.setData(1, Qt.UserRole, 'recordsets')
        item.setFont(0, QFont('Helvetica', 12, QFont.StyleItalic + QFont.Bold))
        return item

    def create_results_item(self):
        item = QTreeWidgetItem()
        item.setText(0, 'Résultats')
        item.setIcon(0, QIcon(':/OpenIMU/icons/results.png'))
        item.setData(1, Qt.UserRole, 'results')
        item.setFont(0, QFont('Helvetica', 12, QFont.StyleItalic + QFont.Bold))
        return item

    def create_record_item(self,name,id):
        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setIcon(0, QIcon(':/OpenIMU/icons/recordset.png'))
        item.setData(0, Qt.UserRole, id)
        item.setData(1, Qt.UserRole, 'recordset')
        item.setFont(0, QFont('Helvetica', 12, QFont.Bold))
        return item

    def create_subrecord_item(self,name,id):
        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setIcon(0, QIcon(':/OpenIMU/icons/subrecord.png'))
        item.setData(0, Qt.UserRole, id)
        item.setData(1, Qt.UserRole, 'subrecord')
        item.setFont(0, QFont('Helvetica', 12, QFont.Bold))
        return item

    def create_sensor_item(self,name,id):
        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setIcon(0, QIcon(':/OpenIMU/icons/sensor.png'))
        item.setData(0, Qt.UserRole, id)
        item.setData(1, Qt.UserRole, 'sensor')
        item.setFont(0, QFont('Helvetica', 12))
        return item

    def create_result_item(self,name,id):
        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setIcon(0, QIcon(':/OpenIMU/icons/result.png'))
        item.setData(0, Qt.UserRole, id)
        item.setData(1, Qt.UserRole, 'result')
        item.setFont(0, QFont('Helvetica', 12))
        return item

    @pyqtSlot(QUrl)
    def urlChanged(self,url):
        print('url: ', url)

    @pyqtSlot(QTreeWidgetItem, int)
    def tree_item_clicked(self, item, column):
        # print(item.text(column))
        item_id = item.data(0, Qt.UserRole)
        item_type = item.data(1, Qt.UserRole)

        # Clear all widgets
        for i in reversed(range(self.UI.frmMain.layout().count())):
            self.UI.frmMain.layout().itemAt(i).widget().setParent(None)

        if item_type == "group":
            groupWidget = GroupWindow(group = self.UI.treeDataSet.groups[item_id])
            self.UI.frmMain.layout().addWidget(groupWidget)

        if item_type == "participant":
            partWidget = ParticipantWindow(participant = self.UI.treeDataSet.participants[item_id])
            self.UI.frmMain.layout().addWidget(partWidget)

        if item_type == "recordsets" or item_type == "recordset" or item_type == "subrecord":
            recordsWidget = RecordsetWindow()
            self.UI.frmMain.layout().addWidget(recordsWidget)

        if item_type == "result":
            resultWidget = ResultWindow()
            self.UI.frmMain.layout().addWidget(resultWidget)

        self.UI.frmMain.update()

    def closeEvent(self, event):
        print('closeEvent')
        """self.jupyter.stop()
        del self.jupyter
        self.jupyter = None
        """

    def __del__(self):
        print('Done!')


    """ def dragEnterEvent(self, event):
        print (event.answerRect())
        #print (self.UI.mdiArea.rect().adjusted(self.UI.mdiArea.x(),self.UI.mdiArea.y(),0,0))
        print(self.UI.mdiArea.rect().adjusted(self.UI.dockDataset.width(), self.UI.dockDataset.y(), 0, 0))

        #if (event.answerRect().intersects(self.UI.mdiArea.rect())):
        if (self.UI.mdiArea.rect().adjusted(self.UI.dockDataset.width(),self.UI.dockDataset.y(),0,0).contains(event.answerRect())):
            print("OK")
            event.accept()
        else:
            print("Not OK")
            event.ignore()

    def dropEvent(self, event):
        print("DROP!")
    
    def add_mdi_widget(self, widget=None, title=''):
        sub_window = QMdiSubWindow(self.UI.mdiArea)

        if widget is not None:
            widget.show()
            sub_window.setWidget(widget)
            sub_window.setWindowTitle(title)

        sub_window.resize(640,480)
        self.UI.mdiArea.addSubWindow(sub_window)
        return sub_window
    """
    def create_chart_view(self, test_data=False):
        chart_view = IMUChartView(self)
        if test_data is True:
            chart_view.add_test_data()
        return chart_view


class Treedatawidget(QTreeWidget):

    groups = {}
    participants = {}

    def __init__(self, parent=None):
        super(QTreeWidget,self).__init__(parent=parent)


    def dropEvent(self,event):

        index = self.indexAt(event.pos())

        source_item = self.currentItem()
        source_type = source_item.data(1, Qt.UserRole)
        source_id = source_item.data(0,Qt.UserRole)

        target_item = self.itemFromIndex(index)
        if target_item is not None:
            target_type = target_item.data(1, Qt.UserRole)
            target_id = target_item.data(0, Qt.UserRole)

        if source_type == "participant":
            # Participant can only be dragged over groups or no group at all
            if not index.isValid():
                # Clear source and set to no group
                self.participants[source_id].group = None
                new_item = source_item.clone()
                self.addTopLevelItem(new_item)
                event.accept()
                return
            else:

                if target_type == "group":
                    self.participants[source_id].group = self.groups[target_id]
                    new_item = source_item.clone()
                    target_item.addChild(new_item)
                    event.accept()
                    return

            event.ignore()



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