from PyQt5 import Qt

from resources.ui.python.StartDialog_ui import Ui_StartDialog

from libopenimu.qt.ImportWindow import ImportWindow

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QFileDialog, QApplication


class StartWindow(QDialog):

    fileName = ''
    importing = False

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.UI = Ui_StartDialog()
        self.UI.setupUi(self)

        # Signals
        self.UI.btnImport.clicked.connect(self.import_clicked)
        self.UI.btnOpen.clicked.connect(self.open_clicked)
        self.UI.btnNew.clicked.connect(self.new_clicked)
        self.UI.btnQuit.clicked.connect(self.quit_clicked)

    @pyqtSlot()
    def import_clicked(self):
        importdialog = ImportWindow(parent=self)
        importdialog.showImport = True

        if importdialog.exec() == QDialog.Accepted:
            self.fileName = importdialog.fileName
            self.importing = True
            if self.isVisible():
                self.accept()

    @pyqtSlot()
    def open_clicked(self):
        file_diag = QFileDialog.getOpenFileName(caption="Nom du fichier à ouvrir", filter="*.oi")

        if file_diag[0] != '':
            self.fileName = file_diag[0]
            if self.isVisible():
                self.accept()

    @pyqtSlot()
    def new_clicked(self):
        importdialog = ImportWindow(parent=self)
        importdialog.showImport = False

        if importdialog.exec() == QDialog.Accepted:
            self.fileName = importdialog.fileName
            if self.isVisible():
                self.accept()

    @staticmethod
    @pyqtSlot()
    def quit_clicked():
        QApplication.quit()
