from PySide6.QtCore import Slot, Qt, Signal, QObject, QEvent, QFileInfo, QDirIterator, QDir, QCoreApplication
from PySide6.QtWidgets import QDialog, QTableWidgetItem, QComboBox, QApplication, QHBoxLayout, QFileDialog, QMessageBox
from PySide6.QtGui import QDropEvent, QDragEnterEvent, QDragMoveEvent, QDragLeaveEvent, QIcon, QKeyEvent

from resources.ui.python.ImportBrowser_ui import Ui_ImportBrowser

from libopenimu.importers.importer_types import ImporterTypes
from libopenimu.importers.WIMUImporter import WIMUImporter
from libopenimu.importers.ActigraphImporter import ActigraphImporter
from libopenimu.importers.OpenIMUImporter import OpenIMUImporter
from libopenimu.importers.AppleWatchImporter import AppleWatchImporter
from libopenimu.qt.BackgroundProcess import BackgroundProcess, ProgressDialog, WorkerTask
from libopenimu.qt.ParticipantWindow import ParticipantWindow

from libopenimu.models.DataSource import DataSource
from libopenimu.models.Participant import Participant
from libopenimu.models.LogTypes import LogTypes
from libopenimu.tools.timing import timing
from libopenimu.tools.Settings import OpenIMUSettings

import os
import platform


class ImportBrowser(QDialog):
    dbMan = None
    log_request = Signal(str, int)
    participant_added = Signal()
    part_widget = None
    has_error = False

    def __init__(self, data_manager, parent=None):
        super().__init__(parent=parent)
        self.UI = Ui_ImportBrowser()
        self.UI.setupUi(self)
        self.part_diag = QDialog()

        self.UI.stackMain.setCurrentIndex(0)
        self.UI.progAdding.hide()

        self.UI.btnCancel.clicked.connect(self.cancel_clicked)
        self.UI.btnOK.clicked.connect(self.ok_clicked)
        self.UI.btnAddFile.clicked.connect(self.add_file_clicked)
        self.UI.btnDelFile.clicked.connect(self.del_clicked)
        self.UI.btnAddDir.clicked.connect(self.add_dir_clicked)
        self.UI.cmbParticipant.currentIndexChanged.connect(self.on_participant_combobox_changed)
        self.UI.btnAddPart.clicked.connect(self.on_add_participant_clicked)
        self.UI.tableFiles.itemSelectionChanged.connect(self.update_buttons_states)

        self.installEventFilter(self)
        self.UI.tableFiles.installEventFilter(self)

        self.dbMan = data_manager

        # Load participants
        self.participants = self.dbMan.get_all_participants()

        # Load participants combo box
        self.fill_participant_combobox(self.UI.cmbParticipant, include_group=True)

        # Invalid fields list
        self.invalid_controls = []

        # Disable "OK" button by default
        self.UI.btnOK.setEnabled(False)

    def do_import(self, file_list: list[dict]):
        class Importer(WorkerTask):

            def __init__(self, filename, task_size, file_importer):
                super().__init__(filename, task_size)
                self.filename = filename
                self.importer = file_importer
                self.importer.update_progress.connect(self.update_progress)
                self.short_filename = DataSource.build_short_filename(self.filename)
                self.title = self.short_filename
                self.results = []

            # For testing only
            @timing
            def load_data(self):
                file_md5 = DataSource.compute_md5(filename=self.filename).hexdigest()

                if not DataSource.datasource_exists_for_participant(filename=self.short_filename,
                                                                    participant=self.importer.participant, md5=file_md5,
                                                                    db_session=self.importer.db.session):
                    self.results = self.importer.load(self.filename)
                    return True
                return False

            # @timing
            def process(self):
                file_md5 = DataSource.compute_md5(filename=self.filename).hexdigest()

                if not DataSource.datasource_exists_for_participant(filename=self.short_filename,
                                                                    participant=self.importer.participant, md5=file_md5,
                                                                    db_session=self.importer.db.session):

                    self.log_request.emit(self.tr('Loading file:') + ' "' + self.short_filename + '"',
                                          LogTypes.LOGTYPE_INFO)

                    self.results = self.importer.load(self.filename)
                    if self.results is not None:
                        self.log_request.emit(self.tr('Importing data...'), LogTypes.LOGTYPE_INFO)
                        self.importer.import_to_database(self.results)
                        self.results.clear()  # Needed to clear the dict cache and let the garbage collector delete it!
                        # Add datasources for that file
                        for recordset in self.importer.recordsets:
                            if not DataSource.datasource_exists_for_recordset(filename=self.short_filename ,
                                                                              recordset=recordset, md5=file_md5,
                                                                              db_session=self.importer.db.session):
                                ds = DataSource()
                                ds.recordset = recordset
                                ds.file_md5 = file_md5
                                ds.file_name = self.short_filename
                                ds.update_datasource(db_session=self.importer.db.session)

                        self.importer.clear_recordsets()
                        self.log_request.emit(self.tr('File import completed.'), LogTypes.LOGTYPE_DONE)
                    else:
                        self.log_request.emit(self.tr('Error loading file:') + ' ' + self.importer.last_error,
                                              LogTypes.LOGTYPE_ERROR)
                else:
                    self.log_request.emit(self.tr('Data from file') + ' "' + self.short_filename + '" ' +
                                          self.tr('already in the database for participant') + ' "' +
                                          self.importer.participant.name + '" - ' + self.tr('ignored.'),
                                          LogTypes.LOGTYPE_WARNING)

        importers = []

        for to_import in file_list:
            if 'participant' not in to_import or 'file_type' not in to_import or 'file_name' not in to_import:
                self.log_request.emit(self.tr('Invalid import structure') + ': ' + str(to_import),
                                      LogTypes.LOGTYPE_WARNING)
                continue
            part = to_import['participant']
            file_type = to_import['file_type']
            file_name = to_import['file_name']
            data_importer = None
            if file_type == ImporterTypes.ACTIGRAPH:
                data_importer = ActigraphImporter(manager=self.dbMan, participant=part)

            if file_type == ImporterTypes.WIMU:
                data_importer = WIMUImporter(manager=self.dbMan, participant=part)

            if file_type == ImporterTypes.OPENIMU:
                data_importer = OpenIMUImporter(manager=self.dbMan, participant=part)

            if file_type == ImporterTypes.APPLEWATCH:
                data_importer = AppleWatchImporter(manager=self.dbMan, participant=part)

            if data_importer is not None:
                # importers.append(Importer(file_name, os.stat(file_name).st_size, data_importer))
                importers.append(Importer(file_name, 100, data_importer))

                # results = data_importer.load(file_name)
                # data_importer.import_to_database(results)
            else:
                self.log_request.emit(self.tr('Unknown file type') + ': ' + str(file_type) + ' - ' +
                                      self.tr('Skipping file') + ' ' + file_name, LogTypes.LOGTYPE_ERROR)
                continue

        self.hide()  # Hide self

        # Run in background all importers (in sequence)
        all_tasks = []
        for importer in importers:
            importer.log_request.connect(self.log_request)
            all_tasks.append(importer)

        # Try loading in parallel (RAM INTENSIVE!)
        # process = BackgroundProcessForImporters(all_tasks)

        # For now process in series...
        self.has_error = False
        process = BackgroundProcess(all_tasks)
        # process.finished.connect(self.process_finished)
        process.task_error.connect(self.process_error_occurred)

        # Create progress dialog
        parent = self
        from libopenimu.qt.MainWindow import MainWindow
        if self.parent() and isinstance(self.parent(), MainWindow):
            parent = self.parent()  # If possible, use MainWindow as parent
        dialog = ProgressDialog(process, self.tr('Data importation'), parent)

        # Start tasks
        process.start()

        # Show progress dialog
        # self.showMinimized()
        # dialog.exec()
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.open()
        while process.isRunning():
            QCoreApplication.processEvents()

        if self.has_error:
            # Error occured while importing
            QMessageBox.critical(self, self.tr('Error while importing data'),
                                 self.tr('Error occured while importing data files. See logs for more information.'))
            self.has_error = False

        # gc.collect()
        self.accept()

    @Slot()
    def ok_clicked(self):
        # Do the importation
        table = self.UI.tableFiles

        # Create list of files to import
        imports = []
        for i in range(0, table.rowCount()):

            part = table.cellWidget(i, 2).currentData()
            file_type = table.cellWidget(i, 1).currentData()
            file_name = table.item(i, 0).text()
            file_info = {'participant': part, 'file_type': file_type, 'file_name': file_name}
            imports.append(file_info)

        # Do the import itself!
        self.do_import(imports)

    # def process_finished(self):
    #     print('Import process finished')

    def process_error_occurred(self, filename: str, error_msg: str):
        self.log_request.emit(self.tr('Error importing file:') + ' "' + filename + '" - ' + error_msg,
                              LogTypes.LOGTYPE_ERROR)
        self.has_error = True

    def add_file_to_list(self, filename: str, filetype_id: int = -1, file_participant=None):
        table = self.UI.tableFiles
        count = self.UI.progAdding.value()
        if count+1 <= self.UI.progAdding.maximum():
            self.UI.progAdding.setValue(count+1)

        if table.findItems(filename, Qt.MatchExactly):
            return  # Already there!

        ignore_list = ['session.oimi', 'watch_logs.txt']  # filename that are ignored
        filename_name = filename.split(os.pathsep)[-1]
        if any(name in filename_name.lower() for name in ignore_list):
            return  # Ignored

        # Get type if not specified
        if filetype_id == -1:
            filetype_id, file_type_name = ImporterTypes.detect_type_from_file(filename)

        row = table.rowCount()
        table.setRowCount(row + 1)

        # File name
        cell = QTableWidgetItem()
        cell.setText(filename)
        table.setItem(row, 0, cell)

        # File format
        item_combo = QComboBox()
        self.fill_importers_combobox(item_combo)
        item_combo.currentTextChanged.connect(self.row_combobox_changed)
        table.setCellWidget(row, 1, item_combo)
        item_combo.setCurrentIndex(item_combo.findData(filetype_id))
        self.validate_row_combobox(item_combo)

        # Participant (and group)
        item_combo = QComboBox()
        self.fill_participant_combobox(combobox=item_combo, include_group=True)
        item_combo.currentIndexChanged.connect(self.row_combobox_changed)
        table.setCellWidget(row, 2, item_combo)
        if file_participant:
            item_combo.setCurrentIndex(item_combo.findText(file_participant.name))
        else:
            item_combo.setCurrentIndex(item_combo.findText(self.UI.cmbParticipant.currentText()))
        self.validate_row_combobox(item_combo)

        # table.resizeColumnsToContents()
        QApplication.processEvents()

    def add_dir_to_list(self, dir_path: str):
        # Browse all files in directory
        dir_browser = QDirIterator(dir_path, [], QDir.Files | QDir.NoDotAndDotDot, QDirIterator.Subdirectories)
        files = []
        while dir_browser.hasNext():
            files.append(dir_browser.next())
        prog_max = self.UI.progAdding.maximum()
        self.UI.progAdding.setMaximum(prog_max + len(files))
        while files:
            self.add_file_to_list(files.pop())

    @staticmethod
    def fill_importers_combobox(combobox: QComboBox):
        combobox.clear()
        combobox.addItem('', ImporterTypes.UNKNOWN)
        for importer in ImporterTypes.value_types:
            if importer != ImporterTypes.WIMU:  # Ignore WIMU for now...
                icon = QIcon(':/OpenIMU/icons/sensor.png')
                if importer == ImporterTypes.OPENIMU:
                    icon = QIcon(':/OpenIMU/icons/sensor_minilogger.png')
                if importer == ImporterTypes.ACTIGRAPH:
                    icon = QIcon(':/OpenIMU/icons/sensor_actigraph.png')
                if importer == ImporterTypes.APPLEWATCH:
                    icon = QIcon(':/OpenIMU/icons/sensor_watch.png')
                combobox.addItem(icon, ImporterTypes.value_names[importer], importer)

    def fill_participant_combobox(self, combobox: QComboBox, include_group=False):
        combobox.clear()
        combobox.addItem('', None)
        for participant in self.participants:
            self.add_participant_in_combobox(participant, combobox, include_group)

    @staticmethod
    def add_participant_in_combobox(participant: Participant, combobox: QComboBox, include_group=False):
        name = participant.name
        if include_group:
            if participant.group:
                name = participant.group.name + '/' + participant.name
        combobox.addItem(QIcon(':/OpenIMU/icons/participant.png'), name, participant)

    @Slot()
    def cancel_clicked(self):
        self.reject()

    @classmethod
    @Slot()
    def thread_finished(self):
        # print('Thread Finished')
        pass

    @Slot()
    def add_file_clicked(self):
        settings = OpenIMUSettings()
        files = QFileDialog.getOpenFileNames(parent=self, caption=self.tr('Select file(s) to import'),
                                             dir=settings.data_load_path)
        files = files[0]
        if not files:
            return

        self.show_progress_bar(True)
        self.UI.progAdding.setMaximum(len(files))
        self.UI.progAdding.setValue(0)

        for file in files:
            self.add_file_to_list(file)

        self.show_progress_bar(False)
        self.UI.tableFiles.resizeColumnsToContents()

        settings.data_load_path = QFileInfo(files[0]).path()

    @Slot()
    def add_dir_clicked(self):
        settings = OpenIMUSettings()
        dirs = QFileDialog.getExistingDirectory(parent=self, caption=self.tr('Select folder to import'),
                                                dir=settings.data_load_path)
        if not dirs:
            return

        self.show_progress_bar(True)
        self.UI.progAdding.setMaximum(0)
        self.UI.progAdding.setValue(0)

        self.add_dir_to_list(dirs)

        self.show_progress_bar(False)
        self.UI.tableFiles.resizeColumnsToContents()

        settings.data_load_path = dirs

    @Slot()
    def del_clicked(self):
        # if self.UI.tableFiles.selectedItems():
        for item in self.UI.tableFiles.selectedItems():
            type_combo = self.UI.tableFiles.cellWidget(item.row(), 1)
            if type_combo in self.invalid_controls:
                self.invalid_controls.remove(type_combo)
            part_combo = self.UI.tableFiles.cellWidget(item.row(), 2)
            if part_combo in self.invalid_controls:
                self.invalid_controls.remove(part_combo)

            self.UI.tableFiles.removeRow(item.row())
            self.update_buttons_states()
            # self.UI.tableFiles.removeRow(self.UI.tableFiles.selectedItems()[0].row())

    def eventFilter(self, target: QObject, event: QEvent) -> bool:
        # print(event)
        if target == self:
            if isinstance(event, QDragEnterEvent):
                # print('DragEnterEvent')
                self.UI.stackMain.setCurrentWidget(self.UI.pageDropFiles)
                event.acceptProposedAction()
                return True

            if isinstance(event, QDragMoveEvent):
                event.acceptProposedAction()
                return True

            if isinstance(event, QDragLeaveEvent):
                self.UI.stackMain.setCurrentWidget(self.UI.pageFiles)
                return True

            if isinstance(event, QDropEvent):
                # print('DropEvent')
                # Process files
                mime_data = event.mimeData()
                self.UI.stackMain.setCurrentWidget(self.UI.pageFiles)
                if mime_data.hasUrls():
                    files = mime_data.urls()
                    self.show_progress_bar(True)
                    self.UI.progAdding.setMaximum(len(files))
                    self.UI.progAdding.setValue(0)
                    for file in files:
                        if file.isLocalFile():  # Support only local files
                            # Get full file name
                            filename = file.path()
                            if platform.system() == 'Windows' and filename.startswith('/'):
                                # Remove / that appears at the start of the file on Windows
                                filename = filename.removeprefix('/')
                            # Check if we have a directory
                            info = QFileInfo(filename)
                            if info.isFile():
                                self.add_file_to_list(filename)
                            elif info.isDir():
                                self.add_dir_to_list(filename)
                    self.show_progress_bar(False)
                    self.UI.tableFiles.resizeColumnsToContents()
                event.acceptProposedAction()
                return True

        if target == self.UI.tableFiles:
            if isinstance(event, QKeyEvent):
                if event.key() == Qt.Key_Delete and event.type() == QEvent.Type.KeyPress:
                    self.del_clicked()
                    event.accept()
                    return True

        return super().eventFilter(target, event)

    @Slot()
    def row_combobox_changed(self):
        sender = self.sender()
        self.validate_row_combobox(sender)

    def validate_row_combobox(self, combobox: QComboBox):
        if combobox.currentIndex() == 0 or not combobox.currentText():
            combobox.setStyleSheet('background: #ffcccc;')
            if combobox not in self.invalid_controls:
                self.invalid_controls.append(combobox)
        else:
            combobox.setStyleSheet('')
            if combobox in self.invalid_controls:
                self.invalid_controls.remove(combobox)

        self.update_buttons_states()

    @Slot()
    def on_participant_combobox_changed(self):
        self.update_current_participant_name()
        self.UI.lblWarning.setVisible(self.UI.cmbParticipant.currentIndex() <= 0)

    def update_current_participant_name(self):
        if self.UI.cmbParticipant.currentText():
            self.UI.lblDropParticipantName.setText(self.UI.cmbParticipant.currentText())
        else:
            self.UI.lblDropParticipantName.setText(self.tr('Unspecified'))

    def show_progress_bar(self, show: bool):
        self.UI.frameParticipant.setEnabled(not show)
        self.UI.frameButtons.setEnabled(not show)
        self.UI.frameTools.setEnabled(not show)
        if show:
            self.UI.progAdding.show()
        else:
            self.UI.progAdding.hide()

    @Slot()
    def on_add_participant_clicked(self):
        layout = QHBoxLayout(self.part_diag)
        self.part_diag.setMinimumWidth(600)

        self.part_widget = ParticipantWindow(db_manager=self.dbMan, edit_mode=True)
        layout.addWidget(self.part_widget)

        self.part_widget.dataCancelled.connect(self.part_diag.reject)
        self.part_widget.dataSaved.connect(self.part_diag.accept)
        self.part_diag.setWindowTitle(self.tr('New participant'))
        if self.part_diag.exec() == QDialog.Accepted:
            # Add data
            part = self.part_widget.participant
            self.participants.append(part)
            self.add_participant_in_combobox(part, self.UI.cmbParticipant, include_group=True)

            # Add to each combo box in each table line...
            for i in range(self.UI.tableFiles.rowCount()):
                combobox = self.UI.tableFiles.cellWidget(i, 2)
                self.add_participant_in_combobox(participant=part, combobox=combobox, include_group=True)

    @Slot()
    def update_buttons_states(self):
        self.UI.btnOK.setEnabled(len(self.invalid_controls) == 0 and self.UI.tableFiles.rowCount() > 0)
        self.UI.btnDelFile.setEnabled(self.UI.tableFiles.rowCount() > 0 and len(self.UI.tableFiles.selectedItems()) > 0)

    def select_participant(self, participant_id: int):
        for i in range(1, self.UI.cmbParticipant.count()):
            if self.UI.cmbParticipant.itemData(i).id_participant == participant_id:
                self.UI.cmbParticipant.setCurrentIndex(i)
                return
