from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit, QFileDialog, QHBoxLayout
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal
from resources.ui.python.ExportCSV_ui import Ui_ExportCSV
from libopenimu.db.DBManager import DBManager


class ExportWindow(QDialog):
    def __init__(self, dataManager : DBManager, parent = None):
        super(QDialog, self).__init__(parent=parent)
        self.UI = Ui_ExportCSV()
        self.UI.setupUi(self)
        self.UI.dirButton.clicked.connect(self.directory_selection_clicked)
        self.UI.btnOK.clicked.connect(self.export)
        self.UI.btnCancel.clicked.connect(self.reject)
        self.dbMan = dataManager


    @pyqtSlot()
    def directory_selection_clicked(self):
        print('file selection')
        directory = QFileDialog().getExistingDirectory(caption="Sélectionnez le répertoire pour exporter")

        print(directory)

        if directory:
            self.UI.lineDir.setText(directory)

    @pyqtSlot()
    def export(self):
        directory = self.UI.lineDir.text()
        print('Should export in : ', directory)
        self.dbMan.export_csv(directory)
        self.accept()
