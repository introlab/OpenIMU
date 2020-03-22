from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import pyqtSlot
from resources.ui.python.ExportCSV_ui import Ui_ExportCSV
from libopenimu.db.DBManager import DBManager
from libopenimu.qt.BackgroundProcess import BackgroundProcess, ProgressDialog, WorkerTask


class ExportWindow(QDialog):
    def __init__(self, dataManager : DBManager, parent = None):
        super().__init__(parent=parent)
        self.UI = Ui_ExportCSV()
        self.UI.setupUi(self)
        self.UI.dirButton.clicked.connect(self.directory_selection_clicked)
        self.UI.btnOK.clicked.connect(self.export)
        self.UI.btnCancel.clicked.connect(self.reject)
        self.UI.lineDir.textChanged.connect(self.directory_changed)
        self.UI.btnOK.setEnabled(False)

        self.dbMan = dataManager

    @pyqtSlot()
    def directory_selection_clicked(self):
        print('file selection')
        directory = QFileDialog().getExistingDirectory(caption="Sélectionnez le répertoire pour exporter")

        print(directory)

        if directory:
            self.UI.lineDir.setText(directory)

    @pyqtSlot()
    def directory_changed(self):
        if self.UI.lineDir.text() != "":
            self.UI.btnOK.setEnabled(True)
        else:
            self.UI.btnOK.setEnabled(False)

    @pyqtSlot()
    def export(self):
        directory = self.UI.lineDir.text()
        file_format = self.UI.comboFormat.currentText()

        print('Should export in : ', directory)

        class FileExporter(WorkerTask):
            def __init__(self, _dbman, _format, _directory):
                super().__init__('Exportation :' + _format, 0)
                self.dbMan = _dbman
                self.directory = _directory
                self.format = _format

            def process(self):
                print('Exporting in :', self.directory)
                self.dbMan.export_file(self.format, self.directory)
                self.update_progress.emit(100)
                print('Exporting done!')

        exporter = FileExporter(self.dbMan, file_format, directory)

        process = BackgroundProcess([exporter])

        # Create progress dialog
        dialog = ProgressDialog(process, 'File Export to format: ' + file_format, self)
        process.finished.connect(dialog.accept)
        process.start()

        # Show dialog
        dialog.exec()

        # Done
        self.accept()
