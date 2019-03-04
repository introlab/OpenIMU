from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtWidgets import QApplication, QDialog, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon, QFont
import PyQt5

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDir

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from libopenimu.qt.Charts import IMUChartView

from libopenimu.models.ProcessedData import ProcessedData
from libopenimu.models.Base import Base

import gc

# UI
from resources.ui.python.MainWindow_ui import Ui_MainWindow
from libopenimu.qt.ImportWindow import ImportWindow
from libopenimu.qt.GroupWindow import GroupWindow
from libopenimu.qt.ParticipantWindow import ParticipantWindow
from libopenimu.qt.RecordsetWindow import RecordsetWindow
from libopenimu.qt.ResultWindow import ResultWindow
from libopenimu.qt.StartWindow import StartWindow
from libopenimu.qt.ImportBrowser import ImportBrowser
from libopenimu.qt.ImportManager import ImportManager
from libopenimu.qt.ExportWindow import ExportWindow
from libopenimu.qt.StreamWindow import StreamWindow
from libopenimu.qt.BackgroundProcess import BackgroundProcess, SimpleTask, ProgressDialog
from libopenimu.qt.ProcessSelectWindow import ProcessSelectWindow

# Models
from libopenimu.models.Participant import Participant
from libopenimu.models.DataSet import DataSet
from libopenimu.models.LogTypes import LogTypes
from libopenimu.streamers.streamer_types import StreamerTypes

# Database
from libopenimu.db.DBManager import DBManager

# Python
import sys
from datetime import datetime


class MainWindow(QMainWindow):
    currentFileName = ''
    dbMan = []
    currentDataSet = DataSet()
    currentRecordsets = []

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.UI = Ui_MainWindow()
        self.UI.setupUi(self)
        self.UI.dockToolBar.setTitleBarWidget(QWidget())
        self.UI.dockLog.hide()

        self.add_to_log("OpenIMU - Prêt à travailler.", LogTypes.LOGTYPE_INFO)

        # Setup signals and slots
        self.setup_signals()

        self.show_start_window()

    def __del__(self):
        # Restore sys.stdout
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def show_start_window(self):
        self.clear_main_widgets()
        self.showMinimized()
        start_window = StartWindow(self)

        if start_window.exec() == QDialog.Rejected:
            # User closed the dialog - exits!
            sys.exit(0)

        # Init database manager
        self.currentFileName = start_window.fileName
        self.dbMan = DBManager(self.currentFileName)

        # Maximize window
        self.showMaximized()

        # Load data
        self.add_to_log("Chargement des données...", LogTypes.LOGTYPE_INFO)
        self.currentDataSet = self.dbMan.get_dataset()
        self.load_data_from_dataset()
        self.UI.treeDataSet.setCurrentItem(None)
        self.UI.treeDataSet.owner = self

        # self.loadDemoData()
        self.add_to_log("Données chargées!", LogTypes.LOGTYPE_DONE)

        # If we need to import data, show the import dialog
        if start_window.importing:
            self.importRequested()
            gc.collect()

    def setup_signals(self):
        self.UI.treeDataSet.itemClicked.connect(self.tree_item_clicked)
        self.UI.btnDataSetInfos.clicked.connect(self.infos_requested)
        self.UI.btnAddGroup.clicked.connect(self.new_group_requested)
        self.UI.btnAddParticipant.clicked.connect(self.new_participant_requested)
        self.UI.treeDataSet.participantDragged.connect(self.participant_was_dragged)
        self.UI.btnDelete.clicked.connect(self.delete_requested)
        self.UI.btnImport.clicked.connect(self.import_requested)
        self.UI.btnExportCSV.clicked.connect(self.export_csv_requested)
        self.UI.dockDataset.visibilityChanged.connect(self.UI.btnShowDataset.setChecked)
        self.UI.dockLog.visibilityChanged.connect(self.toggle_log)
        self.UI.btnShowDataset.clicked.connect(self.toggle_dataset)
        self.UI.btnShowLog.clicked.connect(self.toggle_log)
        self.UI.btnTransfer.clicked.connect(self.transfer_requested)
        self.UI.btnClose.clicked.connect(self.db_close_requested)
        self.UI.btnCompact.clicked.connect(self.db_compact_requested)
        self.UI.btnProcess.clicked.connect(self.process_data_requested)

    def console_log_normal(self, text):
        self.add_to_log(text, LogTypes.LOGTYPE_DEBUG)

    def console_log_error(self, text):
        self.add_to_log(text, LogTypes.LOGTYPE_ERROR)

    def load_data_from_dataset(self):
        self.UI.treeDataSet.clear()

        # Groups
        groups = self.dbMan.get_all_groups()
        for group in groups:
            self.UI.treeDataSet.update_group(group)

        # Participants
        participants = self.dbMan.get_all_participants()
        for participant in participants:
            self.UI.treeDataSet.update_participant(participant)

        # Recordsets
        recordsets = self.dbMan.get_all_recordsets()
        for recordset in recordsets:
            self.UI.treeDataSet.update_recordset(recordset)

        # Results
        results = self.dbMan.get_all_processed_data()
        for result in results:
            self.UI.treeDataSet.update_result(result)

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

        group_widget = GroupWindow(dbManager=self.dbMan, group=group)
        self.UI.frmMain.layout().addWidget(group_widget)

        group_widget.dataSaved.connect(self.data_was_saved)
        group_widget.dataCancelled.connect(self.data_was_cancelled)

    def show_participant(self, participant=None, base_group=None):
        self.clear_main_widgets()

        part_widget = ParticipantWindow(dbManager=self.dbMan, participant=participant, default_group=base_group)
        self.UI.frmMain.layout().addWidget(part_widget)

        part_widget.dataSaved.connect(self.data_was_saved)
        part_widget.dataCancelled.connect(self.data_was_cancelled)

    @pyqtSlot('QString', int)
    def add_to_log(self, text, log_type):
        if text == ' ' or text == '\n':
            return

        log_format = ""
        if log_type == LogTypes.LOGTYPE_INFO:
            log_format = "<span style='color:black'>"
        if log_type == LogTypes.LOGTYPE_WARNING:
            log_format = "<span style='color:orange;font-style:italic'>"
        if log_type == LogTypes.LOGTYPE_ERROR:
            log_format = "<span style='color:red;font-weight:bold'>"
        if log_type == LogTypes.LOGTYPE_DEBUG:
            log_format = "<span style='color:grey;font-style:italic'>"
        if log_type == LogTypes.LOGTYPE_DONE:
            log_format = "<span style='color:green;font-weight:bold'>"

        self.UI.txtLog.append("<span style='color:grey'>" + datetime.now().strftime(
            "%H:%M:%S.%f") + " </span>" + log_format + text + "</span>")
        self.UI.txtLog.ensureCursorVisible()
        QApplication.processEvents()

    def get_current_widget_data_type(self):
        # TODO: checks!
        return self.UI.frmMain.layout().itemAt(0).widget().data_type

    ######################
    @pyqtSlot(bool)
    def toggle_dataset(self, visibility):
        self.UI.dockDataset.setVisible(visibility)

    @pyqtSlot(bool)
    def toggle_log(self, visibility):
        self.UI.dockLog.setVisible(visibility)
        self.UI.btnShowLog.setChecked(visibility)

        if visibility:
            sys.stdout = EmittingStream(textWritten=self.console_log_normal)
            sys.stderr = EmittingStream(textWritten=self.console_log_error)
        else:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

    @pyqtSlot()
    def import_requested(self):
        importer = ImportBrowser(data_manager=self.dbMan)
        importer.log_request.connect(self.add_to_log)
        importer.setStyleSheet(self.styleSheet())
        if importer.exec() == QDialog.Accepted:
            self.load_data_from_dataset()
            gc.collect()

    @pyqtSlot()
    def export_csv_requested(self):
        exporter = ExportWindow(self.dbMan, self)
        exporter.setStyleSheet(self.styleSheet())
        if exporter.exec() == QDialog.Accepted:
            print("Accepted")

    @pyqtSlot()
    def infos_requested(self):
        infos_window = ImportWindow(dataset=self.currentDataSet, filename=self.currentFileName)
        infos_window.setStyleSheet(self.styleSheet())
        infos_window.noImportUI = True
        infos_window.infosOnly = True

        if infos_window.exec() != QDialog.Rejected:
            # TODO: Save data
            self.currentDataSet.name = infos_window.dataSet.name

    @pyqtSlot()
    def process_data_requested(self):
        if self.currentRecordsets:

            # Display Process Window
            proc_window = ProcessSelectWindow(data_manager=self.dbMan, recordsets=self.currentRecordsets, parent=self)

            if proc_window.exec() == QDialog.Accepted:
                self.UI.treeDataSet.update_item("result", proc_window.processed_data)
                self.UI.treeDataSet.select_item("result", proc_window.processed_data.id_processed_data)

    @pyqtSlot()
    def db_close_requested(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setStyleSheet("QPushButton{min-width: 100px; min-height: 40px;}")

        msg.setText("Cet ensemble de données sera fermé. Désirez-vous poursuivre?")
        msg.setWindowTitle("Fermeture?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        rval = msg.exec()
        if rval == QMessageBox.Yes:
            self.dbMan.close()
            self.add_to_log("Fichier " + self.currentFileName + " fermé.", LogTypes.LOGTYPE_INFO)
            self.hide()

            self.show_start_window()

    @pyqtSlot()
    def db_compact_requested(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setStyleSheet("QPushButton{min-width: 100px; min-height: 40px;}")

        msg.setText("Le fichier de données sera nettoyé. Ceci peut prendre un certain temps. \nDésirez-vous poursuivre?")
        msg.setWindowTitle("Compactage des données")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        rval = msg.exec()
        if rval == QMessageBox.Yes:
            task = SimpleTask("Compactage des données", self.dbMan.compact)
            process = BackgroundProcess([task])
            dialog = ProgressDialog(process, 'Nettoyage', self)
            process.start()
            dialog.exec()

    @pyqtSlot()
    def new_group_requested(self):
        self.show_group()

    @pyqtSlot()
    def new_participant_requested(self):
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
        self.UI.btnProcess.setEnabled(False)
        self.currentRecordsets = []

        if item_type == "group":
            self.show_group(self.UI.treeDataSet.groups[item_id])
            # groupWidget = GroupWindow(dbManager=self.dbMan, group = self.UI.treeDataSet.groups[item_id])
            # self.UI.frmMain.layout().addWidget(groupWidget)

        if item_type == "participant":
            self.show_participant(self.UI.treeDataSet.participants[item_id])

        if item_type == "recordsets" or item_type == "recordset" or item_type == "subrecord":
            if item_type == "recordsets":
                part = self.UI.treeDataSet.participants[self.UI.treeDataSet.get_item_id(item.parent())]
                self.currentRecordsets = self.dbMan.get_all_recordsets(part)
            else:
                self.currentRecordsets = [self.UI.treeDataSet.recordsets[item_id]]

            records_widget = RecordsetWindow(manager=self.dbMan, recordset=self.currentRecordsets, parent=self)
            # records_widget.setStyleSheet(self.styleSheet() + records_widget.styleSheet())
            self.UI.frmMain.layout().addWidget(records_widget)
            records_widget.dataDisplayRequest.connect(self.UI.treeDataSet.select_item)
            records_widget.dataUpdateRequest.connect(self.UI.treeDataSet.update_item)
            self.UI.btnProcess.setEnabled(True)

        if item_type == "result":
            result_widget = ResultWindow(manager=self.dbMan, results=self.UI.treeDataSet.results[item_id], parent=self)
            self.UI.frmMain.layout().addWidget(result_widget)

        self.UI.frmMain.update()

    @pyqtSlot()
    def data_was_saved(self):
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
    def data_was_cancelled(self):
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

        if item_type == "recordsets" or item_type == "results":
            return

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setStyleSheet("QPushButton{min-width: 100px; min-height: 40px;}")

        msg.setText("Désirez-vous vraiment supprimer \"" + self.UI.treeDataSet.currentItem().text(0) +
                    "\" et tous les éléments associés?")
        msg.setWindowTitle("Confirmation de suppression")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        rval = msg.exec()
        if rval == QMessageBox.Yes:
            item_name = self.UI.treeDataSet.currentItem().text(0)
            tasks = []

            if item_type == "group":
                group = self.UI.treeDataSet.groups[item_id]
                self.UI.treeDataSet.remove_group(group)
                task = SimpleTask("Suppression de '" + group.name + "'", self.dbMan.delete_group, group)
                tasks.append(task)

            if item_type == "participant":
                part = self.UI.treeDataSet.participants[item_id]
                self.UI.treeDataSet.remove_participant(part)
                task = SimpleTask("Suppression de '" + part.name + "'", self.dbMan.delete_participant, part)
                tasks.append(task)

            if item_type == "recordset":
                # Find and remove all related results
                for result in self.UI.treeDataSet.results.values():
                    if result is not None:
                        for ref in result.processed_data_ref:
                            if ref.recordset.id_recordset == item_id:
                                self.UI.treeDataSet.remove_result(result)
                                task = SimpleTask("Suppression de '" + result.name + "'",
                                                  self.dbMan.delete_processed_data, result)
                                tasks.append(task)
                                # self.dbMan.delete_processed_data(result)
                                break

                recordset = self.UI.treeDataSet.recordsets[item_id]
                task = SimpleTask("Suppression de '" + recordset.name + "'", self.dbMan.delete_recordset, recordset)
                tasks.append(task)
                # self.dbMan.delete_recordset(recordset)
                self.UI.treeDataSet.remove_recordset(recordset)

            if item_type == "result":
                result = self.UI.treeDataSet.results[item_id]
                task = SimpleTask("Suppression de '" + result.name + "'", self.dbMan.delete_processed_data, result)
                tasks.append(task)
                self.UI.treeDataSet.remove_result(result)
                # self.dbMan.delete_processed_data(result)

            if tasks:
                process = BackgroundProcess(tasks)
                # Create progress dialog
                dialog = ProgressDialog(process, 'Suppression', self)
                # Start tasks
                process.start()
                dialog.exec()

            self.add_to_log(item_name + " a été supprimé.", LogTypes.LOGTYPE_DONE)
            self.clear_main_widgets()

#    def closeEvent(self, event):
#        return

    def create_chart_view(self, test_data=False):
        chart_view = IMUChartView(self)
        if test_data is True:
            chart_view.add_test_data()
        return chart_view

    @pyqtSlot()
    def transfer_requested(self):
        import_man = ImportManager(dbmanager=self.dbMan, dirs=True, stream=True, parent=self)

        if import_man.exec() == QDialog.Accepted:
            stream_diag = StreamWindow(stream_type=import_man.filetype_id, path=import_man.filename, parent=self)
            stream_diag.exec()

            # Do the actual import
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Question)
            msg.setStyleSheet("QPushButton{min-width: 100px; min-height: 40px;}")

            msg.setText("Procéder à l'importation des données?")
            msg.setWindowTitle("Importer?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

            rval = msg.exec()
            if rval == QMessageBox.Yes:
                # Start import process
                import_browser = ImportBrowser(data_manager=self.dbMan, parent=self)
                import_browser.log_request.connect(self.add_to_log)

                # Build import list
                files = import_man.get_file_list()
                importer_id = StreamerTypes.value_importer_types[import_man.filetype_id]
                for file_name, file_part in files.items():
                    import_browser.add_file_to_list(file_name, import_man.filetype, importer_id, file_part)

                import_browser.ok_clicked()


########################################################################################################################
class Treedatawidget(QTreeWidget):
    groups = {}
    participants = {}
    recordsets = {}
    results = {}

    items_groups = {}
    items_participants = {}
    items_recordsets = {}
    items_results = {}

    participantDragged = pyqtSignal(Participant)

    owner = None

    def __init__(self, parent=None):
        super(Treedatawidget, self).__init__(parent=parent)

    def remove_group(self,group):
        item = self.items_groups.get(group.id_group, None)
        # Remove all participants items in that group
        for i in range(0, item.childCount()):
            child = item.child(i)
            child_id = self.get_item_id(child)
            self.remove_participant(self.participants[child_id])

        for i in range(0, self.topLevelItemCount()):
            if self.topLevelItem(i) == item:
                self.takeTopLevelItem(i)
                self.groups[group.id_group] = None
                self.items_groups[group.id_group] = None
                break

    def remove_participant(self,participant):
        item = self.items_participants.get(participant.id_participant, None)

        # Remove all recordsets and results items from participant
        for i in range(0, item.childCount()):
            child_type = self.get_item_type(item.child(i))
            for j in range(0, item.child(i).childCount()):
                child = item.child(i).child(j)
                child_id = self.get_item_id(child)
                if child_type == "recordsets":
                    try:
                        self.remove_recordset(self.recordsets[child_id])
                    except KeyError:
                        continue
                if child_type == "results":
                    try:
                        self.remove_result(self.results[child_id])
                    except KeyError:
                        continue

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

    def remove_recordset(self, recordset):
        item = self.items_recordsets.get(recordset.id_recordset, None)
        for i in range(0, item.parent().childCount()):
            if item.parent().child(i) == item:
                item.parent().takeChild(i)
                break

        self.recordsets[recordset.id_recordset] = None
        self.items_recordsets[recordset.id_recordset] = None

    def remove_result(self, result):
        item = self.items_results.get(result.id_processed_data, None)
        for i in range(0, item.parent().childCount()):
            if item.parent().child(i) == item:
                item.parent().takeChild(i)
                break

        self.results[result.id_processed_data] = None
        self.items_results[result.id_processed_data] = None

    def update_group(self, group):
        item = self.items_groups.get(group.id_group, None)
        if item is None:
            item = QTreeWidgetItem()
            item.setText(0, group.name)
            item.setIcon(0, QIcon(':/OpenIMU/icons/group.png'))
            item.setData(0, Qt.UserRole, group.id_group)
            item.setData(1, Qt.UserRole, 'group')
            item.setFont(0, QFont('Helvetica', 12, QFont.Bold))

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
            item.setFont(0, QFont('Helvetica', 12, QFont.Bold))

            if group_item is None: # Participant without a group
                self.addTopLevelItem(item)
            else:
                group_item.addChild(item)

            parent = item
            # Recordings
            item = QTreeWidgetItem()
            item.setText(0, 'Enregistrements')
            item.setIcon(0, QIcon(':/OpenIMU/icons/records.png'))
            item.setData(1, Qt.UserRole, 'recordsets')
            item.setFont(0, QFont('Helvetica', 11, QFont.Bold))
            parent.addChild(item)

            # Results
            item = QTreeWidgetItem()
            item.setText(0, 'Résultats')
            item.setIcon(0, QIcon(':/OpenIMU/icons/results.png'))
            item.setData(1, Qt.UserRole, 'results')
            item.setFont(0, QFont('Helvetica', 11, QFont.Bold))
            parent.addChild(item)

            item = parent
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

    def update_recordset(self, recordset):
        item = self.items_recordsets.get(recordset.id_recordset, None)
        if item is None:
            item = QTreeWidgetItem()
            item.setText(0, recordset.name)
            item.setIcon(0, QIcon(':/OpenIMU/icons/recordset.png'))
            item.setData(0, Qt.UserRole, recordset.id_recordset)
            item.setData(1, Qt.UserRole, 'recordset')
            item.setFont(0, QFont('Helvetica', 11, QFont.Bold))

            part_item = self.items_participants.get(recordset.id_participant,None)
            if part_item is not None:
                for i in range(0, part_item.childCount()):
                    if self.get_item_type(part_item.child(i)) == "recordsets":
                        part_item.child(i).addChild(item)

        else:
            item.setText(0, recordset.name)

        self.recordsets[recordset.id_recordset] = recordset
        self.items_recordsets[recordset.id_recordset] = item

        return item

    def update_result(self, result: ProcessedData):
        item = self.items_results.get(result.id_processed_data, None)
        if item is None:
            item = QTreeWidgetItem()
            item.setText(0, result.name)
            item.setIcon(0, QIcon(':/OpenIMU/icons/result.png'))
            item.setData(0, Qt.UserRole, result.id_processed_data)
            item.setData(1, Qt.UserRole, 'result')
            item.setFont(0, QFont('Helvetica', 11, QFont.Bold))

            part_item = None
            if len(result.processed_data_ref)>0:
                part_item = self.items_participants.get(result.processed_data_ref[0].recordset.id_participant,None)

            if part_item is not None:
                # TODO: subrecords...
                for i in range(0, part_item.childCount()):
                    if self.get_item_type(part_item.child(i)) == "results":
                        part_item.child(i).addChild(item)

        else:
            item.setText(0, result.name)

        self.results[result.id_processed_data] = result
        self.items_results[result.id_processed_data] = item

        return item

    @classmethod
    def get_item_type(cls, item):
        if item is not None:
            return item.data(1, Qt.UserRole)
        else:
            return ""

    @classmethod
    def get_item_id(cls, item):
        if item is not None:
            return item.data(0, Qt.UserRole)
        else:
            return ""

    @pyqtSlot(str, int)
    def select_item(self, item_type, item_id):
        # print ("Selecting " + item_type + ", ID " + str(item_id))
        item = None
        if item_type == "group":
            item = self.items_groups.get(item_id, None)

        if item_type == "participant":
            item = self.items_participants.get(item_id, None)

        if item_type == "recordset":
            item = self.items_recordsets.get(item_id, None)

        if item_type == "result":
            item = self.items_results.get(item_id, None)

        if item is not None:
            self.setCurrentItem(item)
            self.owner.tree_item_clicked(item, 0)

    @pyqtSlot(str, Base)
    def update_item(self, item_type, data):
        # print ("Selecting " + item_type + ", ID " + str(item_id))
        # item = None
        if item_type == "group":
            self.update_group(data)

        if item_type == "participant":
            self.update_participant(data)

        if item_type == "recordset":
            self.update_recordset(data)

        if item_type == "result":
            self.update_result(data)

    def clear(self):

        self.groups = {}
        self.participants = {}
        self.recordsets = {}
        self.results = {}

        self.items_groups = {}
        self.items_participants = {}
        self.items_recordsets = {}
        self.items_results = {}

        super().clear()

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
                # new_item = source_item.clone()
                # self.addTopLevelItem(new_item)
                self.participantDragged.emit(self.participants[source_id])
                event.accept()
                return
            else:

                if target_type == "group":
                    self.participants[source_id].group = self.groups[target_id]
                    self.participants[source_id].id_group = self.groups[target_id].id_group
                    # new_item = source_item.clone()
                    # target_item.addChild(new_item)
                    self.participantDragged.emit(self.participants[source_id])
                    event.accept()
                    return

            event.ignore()


class EmittingStream(PyQt5.QtCore.QObject):

    textWritten = PyQt5.QtCore.pyqtSignal(str)
    flushRequest = PyQt5.QtCore.pyqtSignal()

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass


# Main
if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setAttribute(Qt.AA_EnableHighDpiScaling)

    # qInstallMessageHandler(qt_message_handler)

    # Set current directory to home path
    QDir.setCurrent(QDir.homePath())

    print(PyQt5.__file__)
    # paths = [x for x in dir(QLibraryInfo) if x.endswith('Path')]
    # pprint({x: QLibraryInfo.location(getattr(QLibraryInfo, x)) for x in paths})

    # WebEngine settings
    # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
    # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
    # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
    # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls,True)
    # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)

    window = MainWindow()

    # Never executed (exec already in main)...

    sys.exit(app.exec_())

