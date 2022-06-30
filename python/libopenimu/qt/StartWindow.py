from resources.ui.python.StartDialog_ui import Ui_StartDialog

from libopenimu.qt.ImportWindow import ImportWindow

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDialog, QFileDialog, QApplication

from libopenimu.tools.Settings import OpenIMUSettings


class StartWindow(QDialog):

    fileName = ''
    importing = False

    def __init__(self, parent=None):
        super(StartWindow, self).__init__(parent)
        self.UI = Ui_StartDialog()
        self.UI.setupUi(self)

        # Signals
        self.UI.btnImport.clicked.connect(self.import_clicked)
        self.UI.btnOpen.clicked.connect(self.open_clicked)
        self.UI.btnNew.clicked.connect(self.new_clicked)
        self.UI.btnQuit.clicked.connect(self.quit_clicked)
        self.UI.cmbRecents.currentIndexChanged.connect(self.recent_clicked)

        # Check recent files list
        self.settings = OpenIMUSettings()
        self.UI.cmbRecents.clear()
        self.UI.cmbRecents.addItem("")
        self.UI.cmbRecents.addItems(self.settings.get_recent_files())

    @Slot()
    def import_clicked(self):
        importdialog = ImportWindow(parent=self)
        importdialog.showImport = True

        if importdialog.exec() == QDialog.Accepted:
            self.open_file(importdialog.fileName)

    @Slot()
    def open_clicked(self):
        file_diag = QFileDialog.getOpenFileName(caption=self.tr("Nom du fichier à ouvrir"), filter="*.oi")

        if file_diag[0] != '':
            self.open_file(file_diag[0])

    @Slot()
    def new_clicked(self):
        importdialog = ImportWindow(parent=self)
        importdialog.showImport = False

        if importdialog.exec() == QDialog.Accepted:
            self.open_file(importdialog.fileName)

    def open_file(self, filename: str):
        from os import path
        if not path.exists(filename):
            return

        self.fileName = filename
        self.settings.add_recent_file(self.fileName)
        if self.isVisible():
            self.accept()

    @staticmethod
    @Slot()
    def quit_clicked():
        QApplication.exit(0)

    @Slot()
    def recent_clicked(self):
        self.open_file(self.UI.cmbRecents.currentText())
