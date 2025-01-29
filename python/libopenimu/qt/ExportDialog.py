from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, Slot, Signal, QCoreApplication

from resources.ui.python.ExportDialog_ui import Ui_ExportDialog

from libopenimu.db.DBManager import DBManager
from libopenimu.db.DBExporter import DBExporter, ExporterTypes

from libopenimu.models.LogTypes import LogTypes

from libopenimu.qt.BackgroundProcess import BackgroundProcess, ProgressDialog, WorkerTask
from libopenimu.qt.DataSelector import DataSelector

from libopenimu.tools.Settings import OpenIMUSettings
import os
import shutil


class ExportWindow(QDialog):
    log_request = Signal(str, int)

    def __init__(self, db_manager: DBManager, parent=None):
        super().__init__(parent=parent)
        self.UI = Ui_ExportDialog()
        self.UI.setupUi(self)

        self.dbMan = db_manager
        self.settings = OpenIMUSettings()
        self.UI.txtDir.setText(self.settings.data_export_path)

        self.data_selector = DataSelector(db_manager=self.dbMan, parent=self, show_results=True)
        self.UI.wdgDataSelector.layout().addWidget(self.data_selector)

        last_export_type_id = self.settings.data_export_type

        for exporter_id in ExporterTypes.value_types:
            self.UI.comboFormat.addItem(ExporterTypes.get_icon_for_type(exporter_id),
                                        ExporterTypes.value_names[exporter_id], exporter_id)
            if exporter_id == last_export_type_id:
                self.UI.comboFormat.setCurrentIndex(self.UI.comboFormat.count()-1)

        self.UI.btnBrowse.clicked.connect(self.directory_selection_clicked)
        self.UI.btnOK.clicked.connect(self.export)
        self.UI.btnCancel.clicked.connect(self.reject)
        self.UI.txtDir.textChanged.connect(self.directory_changed)
        self.data_selector.dataIsValid.connect(self.validate)

        self.UI.btnOK.setEnabled(False)

        self.has_export_errors = False

    @Slot()
    def directory_selection_clicked(self):
        directory = QFileDialog().getExistingDirectory(caption=self.tr('Select base folder for exported files'),
                                                       dir=self.UI.txtDir.text())
        if directory:
            self.settings.data_export_path = directory
            self.UI.txtDir.setText(directory)

    @Slot()
    def directory_changed(self):
        self.validate(self.UI.txtDir.text() != '')

    @Slot()
    def validate(self, valid: bool):
        if valid and self.UI.txtDir.text() != '':
            self.UI.btnOK.setEnabled(True)
        else:
            self.UI.btnOK.setEnabled(False)

    @Slot()
    def export(self):
        file_format = self.UI.comboFormat.currentText()
        file_format_id = self.UI.comboFormat.currentData()

        export_path = self.UI.txtDir.text()
        self.settings.data_export_type = file_format_id

        if self.UI.chkDatabaseDir.isChecked():
            # Create subfolder with database filename
            subfolder = os.path.basename(self.dbMan.dbFilename).split('.')[0]
            export_path += os.sep + DBExporter.clean_string(subfolder)

        if os.path.exists(export_path):
            # Path existing - warning
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Question)
            msg.setStyleSheet("QPushButton{min-width: 100px; min-height: 40px;}")

            msg.setText(self.tr('Export path') + ': ' + export_path + ' ' +
                        self.tr('already exists. Data will be overwritten.') + '\n' +
                        self.tr('Do you want to continue?'))
            msg.setWindowTitle(self.tr('Data overwrite'))
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

            rval = msg.exec()
            if rval == QMessageBox.No:
                return

            shutil.rmtree(export_path, ignore_errors=True)

        if not os.path.exists(export_path):
            #os.mkdir(export_path)
            os.makedirs(export_path)

        # print('Should export in : ', directory)

        class FileExporter(WorkerTask):
            def __init__(self, _dbexporter: DBExporter, _datatoexport: dict):
                self.dataList = _datatoexport
                self.total_count = len(self.dataList['groups']) + len(self.dataList['participants']) + \
                                   len(self.dataList['recordsets']) + len(self.dataList['results'])

                self.dbExporter = _dbexporter
                super().__init__(self.tr('Exporting to format') + ': ' +
                                 ExporterTypes.value_names[self.dbExporter.exportFormat], self.total_count)

            def process(self):
                # print('Exporting in :', self.directory)
                # self.dbMan.export_file(self.format, self.directory)
                current_count = 0

                # Export groups
                self.change_task_title.emit(self.tr('Exporting groups...'))
                for id_group in self.dataList['groups']:
                    self.dbExporter.export_group(id_group)
                    current_count += 1
                    self.update_progress.emit(current_count)

                # Export participants
                self.change_task_title.emit(self.tr('Exporting participants...'))
                for id_participant in self.dataList['participants']:
                    self.dbExporter.export_participant(id_participant)
                    current_count += 1
                    self.update_progress.emit(current_count)

                # Export recordsets (and data)
                title = self.tr('Exporting recordsets')
                current = 1
                total_count = len(self.dataList['recordsets'])
                for id_recordset in self.dataList['recordsets']:
                    self.change_task_title.emit(title + ' (' + str(current) + ' / ' + str(total_count) + ')')
                    self.dbExporter.export_recordset(id_recordset)
                    current_count += 1
                    current += 1
                    self.update_progress.emit(current_count)

                # Export results
                title = self.tr('Exporting processed data')
                current = 1
                total_count = len(self.dataList['results'])
                for id_result in self.dataList['results']:
                    self.change_task_title.emit(title + ' (' + str(current) + ' / ' + str(total_count) + ')')
                    self.dbExporter.export_processed_data(id_result)
                    current_count += 1
                    current += 1
                    self.update_progress.emit(current_count)

                # print('Exporting done!')

        exporter = DBExporter(db_manager=self.dbMan, export_path=export_path, export_format=file_format_id, parent=self)

        # TO HELP DEBUG, since Pycharm doesn't support breakpoints in PySide6 QThreads... yet.
        # data_list = self.data_selector.get_all_selected()
        # for id_group in data_list['groups']:
        #     exporter.export_group(id_group)
        #
        # # Export participants
        # for id_participant in data_list['participants']:
        #     exporter.export_participant(id_participant)

        # Export recordsets (and data)
        # for id_recordset in data_list['recordsets']:
        #     exporter.export_recordset(id_recordset)

        # Export results
        # for id_result in data_list['results']:
        #     exporter.export_processed_data(id_result)

        file_exporter = FileExporter(exporter, self.data_selector.get_all_selected())

        process = BackgroundProcess([file_exporter])
        process.task_error.connect(self.process_error_occurred)

        # Create progress dialog
        self.has_export_errors = False
        dialog = ProgressDialog(process, self.tr('Exporting to format') + ': ' + file_format, self)
        process.finished.connect(dialog.accept)
        process.start()

        # Show dialog
        self.hide()
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.open()
        while process.isRunning():
            QCoreApplication.processEvents()

        # Show warning if errors
        if self.has_export_errors:
            # Error occured while exporting
            QMessageBox.critical(self, self.tr('Error while exporting data'),
                                 self.tr('Error occurred while exporting data files. See logs for more information.'))
            self.has_export_errors = False

        # Done
        self.accept()

    @Slot(str, str)
    def process_error_occurred(self, context: str, error_msg: str):
        self.log_request.emit(self.tr('Error exporting data:') + ' "' + context + '" - ' + error_msg,
                              LogTypes.LOGTYPE_ERROR)
        self.has_export_errors = True
