from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtWidgets import QApplication, QDialog, QTreeWidgetItem
import PyQt5

from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtCore import pyqtSlot
from libopenimu.qt.Charts import IMUChartView
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
from libopenimu.qt.ExportWindow import ExportWindow
from libopenimu.qt.StreamWindow import StreamWindow
from libopenimu.qt.ImportMatchDialog import ImportMatchDialog
from libopenimu.qt.BackgroundProcess import BackgroundProcess, SimpleTask, ProgressDialog
from libopenimu.qt.ProcessSelectWindow import ProcessSelectWindow
from libopenimu.streamers.streamer_types import StreamerTypes
from libopenimu.importers.importer_types import ImporterTypes

from OpenIMUApp import Treedatawidget

# Models
from libopenimu.models.Participant import Participant
from libopenimu.models.DataSet import DataSet
from libopenimu.models.LogTypes import LogTypes

# Database
from libopenimu.db.DBManager import DBManager

# Tools
from libopenimu.tools.FileManager import FileManager

# Python
import sys
from datetime import datetime


class MainWindow(QMainWindow):
    currentFileName = ''
    dbMan = []
    currentDataSet = DataSet()
    currentRecordsets = []

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
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
            self.import_requested()
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
        # self.UI.dockLog.visibilityChanged.connect(self.toggle_log)
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

    @pyqtSlot()
    def load_data_from_dataset(self):
        self.UI.treeDataSet.clear()
        self.clear_main_widgets()

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
        # self.UI.btnShowLog.setChecked(visibility)

        if visibility:
            sys.stdout = StdConsoleLogger(self.console_log_normal)
            sys.stderr = StdConsoleLogger(self.console_log_error)
        else:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

        # print("Test!")

    @pyqtSlot()
    def import_requested(self):
        importer = ImportBrowser(data_manager=self.dbMan)
        importer.participant_added.connect(self.load_data_from_dataset)
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

        msg.setText("Le fichier de données sera nettoyé. Ceci peut prendre un certain temps. \n"
                    "Désirez-vous poursuivre?")
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
    def participant_was_dragged(self, participant):
        self.dbMan.update_participant(participant)
        self.update_participant(participant)

    @pyqtSlot(QTreeWidgetItem, int)
    def tree_item_clicked(self, item: QTreeWidgetItem, _: int):
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

        if item_type == "recordsets" or item_type == "recordset" or item_type == "subrecord" or item_type == "date":
            if item_type == "recordsets":
                part = self.UI.treeDataSet.participants[self.UI.treeDataSet.get_item_id(item.parent())]
                self.currentRecordsets = self.dbMan.get_all_recordsets(participant=part)
            elif item_type == "date":
                # Find associated participant
                id_participant = self.UI.treeDataSet.get_item_id(item.parent().parent())
                part = self.UI.treeDataSet.participants[id_participant]
                search_date = self.UI.treeDataSet.dates[Treedatawidget.get_date_id(item.text(0), id_participant)]
                self.currentRecordsets = self.dbMan.get_all_recordsets(participant=part, start_date=search_date)
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

        item.setExpanded(True)
        # self.UI.frmMain.update()

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

        # if item_type == "recordsets" or item_type == "results":
        #     return

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

            if item_type == "date":
                # Delete all recordsets related to that date
                id_participant = self.UI.treeDataSet.get_item_id(self.UI.treeDataSet.currentItem().parent().parent())
                search_date = self.UI.treeDataSet.dates[Treedatawidget.get_date_id(self.UI.treeDataSet.currentItem()
                                                                                   .text(0), id_participant)]
                recordsets = self.dbMan.get_all_recordsets(start_date=search_date)
                part_id = None
                for recordset in recordsets:
                    if part_id is None:
                        part_id = recordset.id_participant
                    task = SimpleTask("Suppression de '" + recordset.name + "'",
                                      self.dbMan.delete_recordset, recordset)
                    tasks.append(task)
                    self.UI.treeDataSet.remove_recordset(recordset)
                self.UI.treeDataSet.remove_date(self.UI.treeDataSet.currentItem().text(0), part_id)

            if item_type == "recordsets":
                # Delete all recordsets for that participant
                participant = self.UI.treeDataSet.participants[self.UI.treeDataSet.get_item_id(self.UI.treeDataSet
                                                                                               .currentItem().parent())]
                recordsets = self.dbMan.get_all_recordsets(participant=participant)
                for recordset in recordsets:
                    task = SimpleTask("Suppression de '" + recordset.name + "'",
                                      self.dbMan.delete_recordset, recordset)
                    tasks.append(task)
                    self.UI.treeDataSet.remove_recordset(recordset)

                # Remove all dates from the view
                self.UI.treeDataSet.remove_dates_for_participant(participant.id_participant)

            if item_type == "results":
                pass

            if tasks:
                process = BackgroundProcess(tasks)
                # Create progress dialog
                dialog = ProgressDialog(process, 'Suppression', self)
                # Start tasks
                process.start()
                dialog.exec()
                # self.dbMan.clean_db()

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
        # import_man = ImportManager(dbmanager=self.dbMan, dirs=True, stream=True, parent=self)
        # # TODO: More intelligent refresh!
        # import_man.participant_added.connect(self.load_data_from_dataset)
        #
        # if import_man.exec() == QDialog.Accepted:
        stream_diag = StreamWindow(parent=self)
        stream_diag.exec()

        # Do the actual import
        # msg = QMessageBox(self)
        # msg.setIcon(QMessageBox.Question)
        # msg.setStyleSheet("QPushButton{min-width: 100px; min-height: 40px;}")
        #
        # msg.setText("Procéder à l'importation des données?")
        # msg.setWindowTitle("Importer?")
        # msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        #
        # rval = msg.exec()
        # if rval == QMessageBox.Yes:

        if stream_diag.folders_to_import:
            # Match windows
            matcher = ImportMatchDialog(dbmanager=self.dbMan, datas=stream_diag.folders_to_import, parent=self)
            if matcher.exec() == QDialog.Accepted:
                # for file_name, file_dataname in file_list.items():
                #     part = matcher.data_match[file_dataname]
                #     file_match[file_name] = part

                # Build import list
                files = matcher.get_files_match(stream_diag.get_data_save_path())

                # Start import process
                import_browser = ImportBrowser(data_manager=self.dbMan, parent=self)
                import_browser.log_request.connect(self.add_to_log)

                importer_id = StreamerTypes.value_importer_types[stream_diag.get_streamer_type()]
                importer_name = ImporterTypes.value_names[importer_id]
                for file_name, file_part in files.items():
                    import_browser.add_file_to_list(file_name, importer_name, importer_id, file_part)

                import_browser.ok_clicked()

                # Delete files after transfer?
                import shutil
                if not stream_diag.get_delete_files_after_import():
                    # Move files to "Imported" folder
                    import os
                    target_dir = stream_diag.get_base_data_save_path() + os.sep + "Imported"
                    FileManager.merge_folders(stream_diag.get_data_save_path(), target_dir)

                # Remove transfered files
                shutil.rmtree(stream_diag.get_data_save_path())
                self.load_data_from_dataset()


class StdConsoleLogger:
    def __init__(self, callable_method):
        self.callback = callable_method

    def write(self, text):
        self.callback(text)

