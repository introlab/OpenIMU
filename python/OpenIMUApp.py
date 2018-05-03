from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QTreeWidget, QTreeWidgetItem, QMessageBox
from PyQt5.QtGui import QIcon, QFont, QDragEnterEvent

# from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings
from PyQt5.QtQuickWidgets import QQuickWidget

from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal
from libopenimu.qt.Charts import IMUChartView

import numpy as np
import libopenimu.jupyter.Jupyter as Jupyter

from enum import Enum

# UI
from resources.ui.python.MainWindow_ui import Ui_MainWindow
from resources.ui.python.StartDialog_ui import Ui_StartDialog
from libopenimu.qt.ImportWindow import ImportWindow
from libopenimu.qt.GroupWindow import GroupWindow
from libopenimu.qt.ParticipantWindow import ParticipantWindow
from libopenimu.qt.RecordsetWindow import RecordsetWindow
from libopenimu.qt.ResultWindow import ResultWindow
from libopenimu.qt.StartWindow import StartWindow
from libopenimu.qt.ImportBrowser import ImportBrowser

# Models
from libopenimu.models.Group import Group
from libopenimu.models.Participant import Participant
from libopenimu.models.DataSet import DataSet

# Database
from libopenimu.db.DBManager import DBManager

# Python
import sys
from datetime import datetime


class LogTypes(Enum):
    LOGTYPE_INFO = 0
    LOGTYPE_WARNING = 1
    LOGTYPE_ERROR = 2
    LOGTYPE_DEBUG = 3
    LOGTYPE_DONE = 4


class MainWindow(QMainWindow):
    currentFileName = ''
    dbMan = []
    currentDataSet = DataSet()

    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent=parent)
        self.UI = Ui_MainWindow()
        self.UI.setupUi(self)

        self.add_to_log("OpenIMU - Prêt à travailler.", LogTypes.LOGTYPE_INFO)

        startWindow = StartWindow()

        if startWindow.exec() == QDialog.Rejected:
            # User closed the dialog - exits!
            exit(0)

        # Init database manager
        self.currentFileName = startWindow.fileName
        self.dbMan = DBManager(self.currentFileName)

        # Setup signals and slots
        self.setup_signals()

        # Maximize window
        self.showMaximized()

        # Load data
        self.add_to_log("Chargement des données...", LogTypes.LOGTYPE_INFO)
        self.currentDataSet = self.dbMan.get_dataset()
        self.load_data_from_dataset()
        self.UI.treeDataSet.setCurrentItem(None)

        # self.loadDemoData()
        self.add_to_log("Données chargées!", LogTypes.LOGTYPE_DONE)

        # If we need to import data, show the import dialog
        if startWindow.importing :
            self.importRequested()

    def setup_signals(self):
        self.UI.treeDataSet.itemClicked.connect(self.tree_item_clicked)
        self.UI.btnDataSetInfos.clicked.connect(self.infosRequested)
        self.UI.btnAddGroup.clicked.connect(self.newGroupRequested)
        self.UI.btnAddParticipant.clicked.connect(self.newParticipantRequested)
        self.UI.treeDataSet.participantDragged.connect(self.participant_was_dragged)
        self.UI.btnDelete.clicked.connect(self.delete_requested)
        self.UI.btnImport.clicked.connect(self.importRequested)

    def load_data_from_dataset(self):
        # Groups
        groups = self.dbMan.get_all_groups()
        for group in groups:
            self.UI.treeDataSet.update_group(group)
            participants = self.dbMan.get_participants_for_group(group)
            for participant in participants:
                self.UI.treeDataSet.update_participant(participant)

        # Participants without a group
        participants = self.dbMan.get_participants_for_group(None)
        for participant in participants:
            self.UI.treeDataSet.update_participant(participant)

    def loadDemoData(self):
        # Load demo structure
        new_group = Group(id_group=0, name="Groupe 1", description="Ceci est un premier groupe de démonstration")

        item = self.UI.treeDataSet.update_group(new_group)

        new_part = Participant(id_participant=1, name="Participant B", description="Participant dans un groupe",
                               group=new_group)
        item = self.UI.treeDataSet.update_participant(new_part)

        item2 = self.create_records_item()
        item.addChild(item2)

        item3 = self.create_record_item("Enregistrement 1 (27/03/2018)", 0)
        item2.addChild(item3)

        """ item5 = self.create_sensor_item("Accéléromètre", 0)
        item3.addChild(item5)

        item5 = self.create_sensor_item("Gyromètre", 1)
        item3.addChild(item5)

        item5 = self.create_sensor_item("GPS", 2)
        item3.addChild(item5)
        """
        item4 = self.create_subrecord_item("AM", 0)
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

        item3 = self.create_result_item("Nombre de pas (par enregistrement)", 0)
        item2.addChild(item3)

        item3 = self.create_result_item("Niveau d'activité (total)", 1)
        item2.addChild(item3)

        new_part = Participant(id_participant=2, name="Participant C", group=new_group)
        item = self.UI.treeDataSet.update_participant(new_part)

        parent = item
        item = self.create_records_item()
        parent.addChild(item)

        item3 = self.create_record_item("Enregistrement 1 (23/03/2018)", 3)
        item.addChild(item3)

        new_group = Group(id_group=1, name="Groupe 2", description="Ceci est un deuxième groupe de démonstration")

        item = self.UI.treeDataSet.update_group(new_group)

        parent = item
        new_part = Participant(id_participant=3, name="Participant D", group=new_group)
        item = self.UI.treeDataSet.update_participant(new_part)

        new_part = Participant(id_participant=0, name="Participant A", description="Participant sans groupe")
        item = self.UI.treeDataSet.update_participant(new_part)

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

    def create_record_item(self, name, id):
        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setIcon(0, QIcon(':/OpenIMU/icons/recordset.png'))
        item.setData(0, Qt.UserRole, id)
        item.setData(1, Qt.UserRole, 'recordset')
        item.setFont(0, QFont('Helvetica', 12, QFont.Bold))
        return item

    def create_subrecord_item(self, name, id):
        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setIcon(0, QIcon(':/OpenIMU/icons/subrecord.png'))
        item.setData(0, Qt.UserRole, id)
        item.setData(1, Qt.UserRole, 'subrecord')
        item.setFont(0, QFont('Helvetica', 12, QFont.Bold))
        return item

    def create_sensor_item(self, name, id):
        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setIcon(0, QIcon(':/OpenIMU/icons/sensor.png'))
        item.setData(0, Qt.UserRole, id)
        item.setData(1, Qt.UserRole, 'sensor')
        item.setFont(0, QFont('Helvetica', 12))
        return item

    def create_result_item(self, name, id):
        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setIcon(0, QIcon(':/OpenIMU/icons/result.png'))
        item.setData(0, Qt.UserRole, id)
        item.setData(1, Qt.UserRole, 'result')
        item.setFont(0, QFont('Helvetica', 12))
        return item

    def update_group(self, group):
        item = self.UI.treeDataSet.update_group(group)
        self.UI.treeDataSet.setCurrentItem(item)

    def update_participant(self, participant):
        item = self.UI.treeDataSet.update_participant(participant)
        self.UI.treeDataSet.setCurrentItem(item)

    def clear_main_widgets(self):
        for i in reversed(range(self.UI.frmMain.layout().count())):
            self.UI.frmMain.layout().itemAt(i).widget().setParent(None)

    def show_group(self, group=None):
        self.clear_main_widgets()

        groupWidget = GroupWindow(dbManager=self.dbMan, group=group)
        self.UI.frmMain.layout().addWidget(groupWidget)

        groupWidget.dataSaved.connect(self.dataWasSaved)
        groupWidget.dataCancelled.connect(self.dataWasCancelled)

    def show_participant(self, participant=None, base_group=None):
        self.clear_main_widgets()

        partWidget = ParticipantWindow(dbManager=self.dbMan, participant=participant, default_group=base_group)
        self.UI.frmMain.layout().addWidget(partWidget)

        partWidget.dataSaved.connect(self.dataWasSaved)
        partWidget.dataCancelled.connect(self.dataWasCancelled)

    def add_to_log(self, text, log_type):
        format = ""
        if log_type == LogTypes.LOGTYPE_INFO:
            format = "<span style='color:black'>"
        if log_type == LogTypes.LOGTYPE_WARNING:
            format = "<span style='color:orange;font-style:italic'>"
        if log_type == LogTypes.LOGTYPE_ERROR:
            format = "<span style='color:red;font-weight:bold'>"
        if log_type == LogTypes.LOGTYPE_DEBUG:
            format = "<span style='color:grey;font-style:italic'>"
        if log_type == LogTypes.LOGTYPE_DONE:
            format = "<span style='color:green;font-weight:bold'>"

        self.UI.txtLog.append("<span style='color:grey'>" + datetime.now().strftime(
            "%H:%M:%S.%f") + " </span>" + format + text + "</span>")
        self.UI.txtLog.ensureCursorVisible();

    def get_current_widget_data_type(self):
        # TODO: checks!
        return self.UI.frmMain.layout().itemAt(0).widget().data_type

    ######################
    @pyqtSlot(QUrl)
    def urlChanged(self, url):
        print('url: ', url)

    @pyqtSlot()
    def importRequested(self):
        importer = ImportBrowser(dataManager=self.dbMan)

        importer.exec()

    @pyqtSlot()
    def infosRequested(self):
        infosWindow = ImportWindow(dataset=self.currentDataSet, filename=self.currentFileName)
        infosWindow.noImportUI = True
        infosWindow.infosOnly = True

        if infosWindow.exec() != QDialog.Rejected:
            # TODO: Save data
            self.currentDataSet.name = infosWindow.dataSet.name

    @pyqtSlot()
    def newGroupRequested(self):
        self.show_group()

    @pyqtSlot()
    def newParticipantRequested(self):
        # Check if we can get a root item (group) for the current selected item or not
        item = self.UI.treeDataSet.currentItem()
        if item is not None:
            while item.parent() is not None:
                item = item.parent()

        default_group = None
        if self.UI.treeDataSet.get_item_type(item) == "group":
            default_group = self.UI.treeDataSet.groups[self.UI.treeDataSet.get_item_id(item)]

        self.show_participant(base_group=default_group)

    @pyqtSlot(Participant)
    def participant_was_dragged(self,participant):
        self.dbMan.update_participant(participant)
        self.update_participant(participant)

    @pyqtSlot(QTreeWidgetItem, int)
    def tree_item_clicked(self, item, column):
        # print(item.text(column))
        item_id = self.UI.treeDataSet.get_item_id(item)
        item_type = self.UI.treeDataSet.get_item_type(item)

        # Clear all widgets
        self.clear_main_widgets()

        if item_type == "group":
            self.show_group(self.UI.treeDataSet.groups[item_id])
            # groupWidget = GroupWindow(dbManager=self.dbMan, group = self.UI.treeDataSet.groups[item_id])
            # self.UI.frmMain.layout().addWidget(groupWidget)

        if item_type == "participant":
            self.show_participant(self.UI.treeDataSet.participants[item_id])

        if item_type == "recordsets" or item_type == "recordset" or item_type == "subrecord":
            recordsWidget = RecordsetWindow()
            self.UI.frmMain.layout().addWidget(recordsWidget)

        if item_type == "result":
            resultWidget = ResultWindow()
            self.UI.frmMain.layout().addWidget(resultWidget)

        self.UI.frmMain.update()

    @pyqtSlot()
    def dataWasSaved(self):
        item_type = self.get_current_widget_data_type()

        if item_type == "group":
            group = self.UI.frmMain.layout().itemAt(0).widget().group
            self.update_group(group)
            self.add_to_log("Groupe " + group.name + " mis à jour.", LogTypes.LOGTYPE_DONE)

        if item_type == "participant":
            part = self.UI.frmMain.layout().itemAt(0).widget().participant
            self.update_participant(part)
            self.add_to_log("Participant " + part.name + " mis à jour.", LogTypes.LOGTYPE_DONE)


    @pyqtSlot()
    def dataWasCancelled(self):
        item_type = self.get_current_widget_data_type()

        if item_type == "group":
            if self.UI.frmMain.layout().itemAt(0).widget().group is None:
                self.clear_main_widgets()

        if item_type == "participant":
            if self.UI.frmMain.layout().itemAt(0).widget().participant is None:
                self.clear_main_widgets()

    @pyqtSlot()
    def delete_requested(self):
        item_id = self.UI.treeDataSet.get_item_id(self.UI.treeDataSet.currentItem())
        item_type = self.UI.treeDataSet.get_item_type(self.UI.treeDataSet.currentItem())
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)

        msg.setText("Désirez-vous vraiment supprimer " + self.UI.treeDataSet.currentItem().text(0) + " et tous les éléments associés?")
        msg.setWindowTitle("Confirmation de suppression")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        rval = msg.exec()
        if rval == QMessageBox.Yes:
            item_name = self.UI.treeDataSet.currentItem().text(0)
            if item_type == "group":
                group = self.UI.treeDataSet.groups[item_id]
                self.dbMan.delete_group(group)
                self.UI.treeDataSet.remove_group(group)

            if item_type == "participant":
                part = self.UI.treeDataSet.participants[item_id]
                self.dbMan.delete_participant(part)
                self.UI.treeDataSet.remove_participant(part)

            self.add_to_log(item_name + " a été supprimé.", LogTypes.LOGTYPE_DONE)
            self.clear_main_widgets()

    def closeEvent(self, event):
        print('closeEvent')
        """self.jupyter.stop()
        del self.jupyter
        self.jupyter = None
        """

    def __del__(self):
        print('Done!')

    def create_chart_view(self, test_data=False):
        chart_view = IMUChartView(self)
        if test_data is True:
            chart_view.add_test_data()
        return chart_view


########################################################################################################################
class Treedatawidget(QTreeWidget):
    groups = {}
    participants = {}

    items_groups = {}
    items_participants = {}

    participantDragged = pyqtSignal(Participant)

    def __init__(self, parent=None):
        super(QTreeWidget, self).__init__(parent=parent)

    def remove_group(self,group):
        item = self.items_groups.get(group.id_group, None)
        for i in range(0, self.topLevelItemCount()):
            if self.topLevelItem(i) == item:
                self.takeTopLevelItem(i)
                self.groups[group.id_group] = None
                self.items_groups[group.id_group] = None
                break

    def remove_participant(self,participant):
        item = self.items_participants.get(participant.id_participant, None)
        if participant.id_group is None: # Participant without a group
            for i in range(0, self.topLevelItemCount()):
                if self.topLevelItem(i) == item:
                    self.takeTopLevelItem(i)
                    break
        else:
            for i in range(0, item.parent().childCount()):
                if item.parent().child(i) == item:
                    item.parent().takeChild(i)
                    break

        self.participants[participant.id_participant] = None
        self.items_participants[participant.id_participant] = None

    def update_group(self, group):
        item = self.items_groups.get(group.id_group, None)
        if item is None:
            item = QTreeWidgetItem()
            item.setText(0, group.name)
            item.setIcon(0, QIcon(':/OpenIMU/icons/group.png'))
            item.setData(0, Qt.UserRole, group.id_group)
            item.setData(1, Qt.UserRole, 'group')
            item.setFont(0, QFont('Helvetica', 14, QFont.Bold))

            self.addTopLevelItem(item)
            self.groups[group.id_group] = group
            self.items_groups[group.id_group] = item
        else:
            item.setText(0, group.name)

        return item

    def update_participant(self, part):
        item = self.items_participants.get(part.id_participant, None)
        group_item = self.items_groups.get(part.id_group, None)
        if item is None:
            item = QTreeWidgetItem()
            item.setText(0, part.name)
            item.setIcon(0, QIcon(':/OpenIMU/icons/participant.png'))
            item.setData(0, Qt.UserRole, part.id_participant)
            item.setData(1, Qt.UserRole, 'participant')
            item.setFont(0, QFont('Helvetica', 13, QFont.Bold))

            if group_item is None: #Participant without a group
                self.addTopLevelItem(item)
            else:
                group_item.addChild(item)

        else:
            item.setText(0, part.name)
            # Check if we must move it or not, if the group changed
            if item.parent() != group_item:
                # Old group - find and remove current item
                if item.parent() is None: # No parent...
                    for i in range(0, self.topLevelItemCount()):
                        if self.topLevelItem(i) == item:
                            item = self.takeTopLevelItem(i)
                            break
                else:
                    # Had a group...
                    for i in range(0, item.parent().childCount()):
                        if item.parent().child(i) == item:
                            item = item.parent().takeChild(i)
                            break

                # New group
                if group_item is None:  # Participant without a group
                    self.addTopLevelItem(item)
                else:
                    group_item.addChild(item)

        self.participants[part.id_participant] = part
        self.items_participants[part.id_participant] = item
        return item

    def get_item_type(self,item):
        if item is not None:
            return item.data(1, Qt.UserRole)
        else:
            return ""

    def get_item_id(self,item):
        if item is not None:
            return item.data(0, Qt.UserRole)
        else:
            return ""

    def dropEvent(self, event):

        index = self.indexAt(event.pos())

        source_item = self.currentItem()
        source_type = source_item.data(1, Qt.UserRole)
        source_id = source_item.data(0, Qt.UserRole)

        target_item = self.itemFromIndex(index)
        if target_item is not None:
            target_type = target_item.data(1, Qt.UserRole)
            target_id = target_item.data(0, Qt.UserRole)

        if source_type == "participant":
            # Participant can only be dragged over groups or no group at all
            if not index.isValid():
                # Clear source and set to no group
                self.participants[source_id].group = None
                self.participants[source_id].id_group = None
                #new_item = source_item.clone()
                #self.addTopLevelItem(new_item)
                self.participantDragged.emit(self.participants[source_id])
                event.accept()
                return
            else:

                if target_type == "group":
                    self.participants[source_id].group = self.groups[target_id]
                    self.participants[source_id].id_group = self.groups[target_id].id_group
                    #new_item = source_item.clone()
                    #target_item.addChild(new_item)
                    self.participantDragged.emit(self.participants[source_id])
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
