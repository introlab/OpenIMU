from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QTableWidgetItem

from resources.ui.python.ImportBrowser_ui import Ui_ImportBrowser
from libopenimu.qt.ImportManager import ImportManager

from libopenimu.importers.importer_types import ImporterTypes
from libopenimu.importers.WIMUImporter import WIMUImporter
from libopenimu.importers.ActigraphImporter import ActigraphImporter
from libopenimu.importers.OpenIMUImporter import OpenIMUImporter
from libopenimu.importers.AppleWatchImporter import AppleWatchImporter
from libopenimu.qt.BackgroundProcess import BackgroundProcess, ProgressDialog, WorkerTask

from libopenimu.models.DataSource import DataSource
from libopenimu.models.LogTypes import LogTypes

import gc


class ImportBrowser(QDialog):
    dbMan = None
    log_request = pyqtSignal('QString', int)

    def __init__(self, data_manager, parent=None):
        super().__init__(parent=parent)
        self.UI = Ui_ImportBrowser()
        self.UI.setupUi(self)

        self.UI.btnCancel.clicked.connect(self.cancel_clicked)
        self.UI.btnOK.clicked.connect(self.ok_clicked)
        self.UI.btnAddFile.clicked.connect(self.add_clicked)
        self.UI.btnDelFile.clicked.connect(self.del_clicked)
        self.UI.btnAddDir.clicked.connect(self.add_dir_clicked)
        self.dbMan = data_manager

    @pyqtSlot()
    def ok_clicked(self):
        # Do the importation
        table = self.UI.tableFiles

        class Importer(WorkerTask):

            def __init__(self, filename, task_size, file_importer):
                super().__init__(filename, task_size)
                self.filename = filename
                self.importer = file_importer
                self.importer.update_progress.connect(self.update_progress)
                self.short_filename = DataSource.build_short_filename(self.filename)
                self.title = self.short_filename

            def process(self):
                file_md5 = DataSource.compute_md5(filename=self.filename).hexdigest()

                if not DataSource.datasource_exists_for_participant(filename=self.short_filename ,
                                                                    participant=self.importer.participant, md5=file_md5,
                                                                    db_session=self.importer.db.session):

                    self.log_request.emit("Chargement du fichier: '" + self.short_filename  + "'", LogTypes.LOGTYPE_INFO)

                    results = self.importer.load(self.filename)
                    if results is not None:
                        self.log_request.emit('Importation des données...', LogTypes.LOGTYPE_INFO)
                        self.importer.import_to_database(results)
                        results.clear()  # Needed to clear the dict cache and let the garbage collector delete it!
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
                        self.log_request.emit('Importation du fichier complétée!', LogTypes.LOGTYPE_DONE)
                    else:
                        self.log_request.emit('Erreur lors du chargement du fichier: ' + self.importer.last_error,
                                              LogTypes.LOGTYPE_ERROR)
                else:
                    self.log_request.emit("Données du fichier '" + self.filename + "' déjà présentes pour '" +
                                          self.importer.participant.name + "' - ignorées.",
                                          LogTypes.LOGTYPE_WARNING)

        importers = []

        for i in range(0, table.rowCount()):
            part = table.item(i, 1).data(Qt.UserRole)
            file_type = table.item(i, 2).data(Qt.UserRole)
            file_name = table.item(i, 3).text()
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
                # TODO: Error message
                self.reject()

        # Run in background all importers (in sequence)
        all_tasks = []
        for importer in importers:
            importer.log_request.connect(self.log_request)
            all_tasks.append(importer)

        process = BackgroundProcess(all_tasks)
        # Create progress dialog
        dialog = ProgressDialog(process, 'Importation des données', self)

        # Start tasks
        process.start()

        # Show progress dialog
        self.showMinimized()
        dialog.exec()

        gc.collect()
        self.accept()

    def add_file_to_list(self, filename, filetype, filetype_id, participant):
        table = self.UI.tableFiles

        row = table.rowCount()
        table.setRowCount(row + 1)
        cell = QTableWidgetItem()
        cell.setText(filename)
        table.setItem(row, 3, cell)
        cell = QTableWidgetItem()
        cell.setText(filetype)
        cell.setData(Qt.UserRole, filetype_id)
        table.setItem(row, 2, cell)
        cell = QTableWidgetItem()
        group = ""
        if participant.group is not None:
            group = participant.group.name
        cell.setText(group)
        table.setItem(row, 0, cell)
        cell = QTableWidgetItem()
        cell.setText(participant.name)
        cell.setData(Qt.UserRole, participant)
        table.setItem(row, 1, cell)

        table.resizeColumnsToContents()

    @pyqtSlot()
    def cancel_clicked(self):
        self.reject()

    @classmethod
    @pyqtSlot()
    def thread_finished(self):
        print('Thread Finished')

    @pyqtSlot()
    def add_clicked(self):
        importman = ImportManager(dbmanager=self.dbMan, dirs=False)
        importman.setStyleSheet(self.styleSheet())

        if self.UI.tableFiles.rowCount() > 0:
            # Copy informations into the dialog
            last_row = self.UI.tableFiles.rowCount() - 1
            importman.set_participant(self.UI.tableFiles.item(last_row, 1).text())
            importman.set_filetype(self.UI.tableFiles.item(last_row, 2).text())

        self.showMinimized()
        if importman.exec() == QDialog.Accepted:
            files = importman.filename.split(";")
            # Add file to list
            for file in files:
                self.add_file_to_list(file, importman.filetype, importman.filetype_id, importman.participant)
        self.showNormal()

    @pyqtSlot()
    def add_dir_clicked(self):
        importman = ImportManager(dbmanager=self.dbMan, dirs=True)
        importman.setStyleSheet(self.styleSheet())

        if self.UI.tableFiles.rowCount() > 0:
            # Copy informations into the dialog
            last_row = self.UI.tableFiles.rowCount() - 1
            importman.set_participant(self.UI.tableFiles.item(last_row, 1).text())
            importman.set_filetype(self.UI.tableFiles.item(last_row, 2).text())

        self.showMinimized()
        if importman.exec() == QDialog.Accepted:
            files = importman.get_file_list()
            for file_name, file_part in files.items():
                self.add_file_to_list(file_name, importman.filetype, importman.filetype_id, file_part)

        self.showNormal()

    @pyqtSlot()
    def del_clicked(self):
        if self.UI.tableFiles.selectedItems():
            # print(self.UI.tableFiles.selectedItems()[0].row())

            self.UI.tableFiles.removeRow(self.UI.tableFiles.selectedItems()[0].row())
