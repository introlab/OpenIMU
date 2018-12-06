from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import pyqtSlot
from resources.ui.python.ExportCSV_ui import Ui_ExportCSV
from libopenimu.db.DBManager import DBManager
from libopenimu.qt.BackgroundProcess import BackgroundProcess, ProgressDialog


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
        print('Should export in : ', directory)

        # Create progress dialog
        dialog = ProgressDialog(1, self)
        dialog.setWindowTitle('Exportation CSV...')

        class CSVExporter:
            def __init__(self, dbmanager, directory):
                self.dbMan = dbmanager
                self.directory = directory

            def process(self):
                print('Exporting in :', self.directory)
                self.dbMan.export_csv(directory)
                print('Exporting done!')

        exporter = CSVExporter(self.dbMan, directory)

        process = BackgroundProcess([exporter.process])
        process.finished.connect(dialog.accept)
        process.trigger.connect(dialog.trigger)
        process.start()

        # Show dialog
        dialog.exec()

        # Done
        self.accept()
