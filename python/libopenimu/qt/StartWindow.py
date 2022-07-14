from resources.ui.python.StartDialog_ui import Ui_StartDialog

from libopenimu.qt.ImportWindow import ImportWindow
from libopenimu.qt.ImportDialogWizard import ImportDialogWizard
from libopenimu.qt.AboutScreen import AboutScreen

from PySide6.QtCore import Slot, Signal, QLocale, QFileInfo
from PySide6.QtWidgets import QDialog, QFileDialog, QApplication, QMessageBox
from PySide6.QtGui import QMouseEvent

from libopenimu.tools.Settings import OpenIMUSettings


class StartWindow(QDialog):

    filename = ''
    importing = False
    request_language_change = Signal(str)
    loading = True

    def __init__(self, parent=None):
        super(StartWindow, self).__init__(parent)
        self.UI = Ui_StartDialog()
        self.UI.setupUi(self)

        # Set current language
        if QLocale() == QLocale.French:
            self.UI.cmbLanguage.setCurrentIndex(1)
        else:
            self.UI.cmbLanguage.setCurrentIndex(0)

        # Check recent files list
        self.settings = OpenIMUSettings()
        self.UI.cmbRecents.clear()
        self.UI.cmbRecents.addItem("")
        recent_files = self.settings.get_recent_files()
        self.UI.cmbRecents.addItems(recent_files)

        # Signals
        self.UI.btnImport.clicked.connect(self.import_clicked)
        self.UI.btnOpen.clicked.connect(self.open_clicked)
        self.UI.btnNew.clicked.connect(self.new_clicked)
        self.UI.btnQuit.clicked.connect(self.quit_clicked)
        self.UI.cmbRecents.currentIndexChanged.connect(self.recent_clicked)
        self.UI.cmbLanguage.currentIndexChanged.connect(self.language_changed)
        self.UI.lblLogo.mouseReleaseEvent = self.logo_clicked

        self.loading = False

    @Slot()
    def import_clicked(self):
        importdialog = ImportDialogWizard(parent=self)  # ImportWindow(parent=self)
        # importdialog.showImport = True

        if importdialog.exec() == QDialog.Accepted:
            self.importing = True
            if importdialog.useExisting:
                self.open_file(importdialog.databaseFilename)
            else:
                importdialog = ImportWindow(parent=self)
                if importdialog.exec() == QDialog.Accepted:
                    self.open_file(importdialog.fileName)

    @Slot()
    def open_clicked(self):
        file_diag = QFileDialog.getOpenFileName(caption=self.tr('Filename to open'), filter='*.oi',
                                                dir=self.settings.database_base_path)

        if file_diag[0] != '':
            self.open_file(file_diag[0])
            self.settings.database_base_path = QFileInfo(file_diag[0]).path()

    @Slot()
    def new_clicked(self):
        importdialog = ImportWindow(parent=self)
        importdialog.showImport = False

        if importdialog.exec() == QDialog.Accepted:
            self.open_file(importdialog.fileName)

    def open_file(self, filename: str) -> bool:
        from os import path
        if not filename:
            return True

        if not path.exists(filename):
            QMessageBox.warning(self, self.tr('File missing'),
                                filename + ' ' + self.tr('doesn\'t exist. Perhaps it has been moved, deleted or '
                                                         'renamed?'))
            return False

        self.filename = filename
        self.settings.add_recent_file(self.filename)
        if self.isVisible():
            self.accept()
        return True

    @staticmethod
    @Slot()
    def quit_clicked():
        QApplication.exit(0)

    @Slot()
    def recent_clicked(self):
        if self.loading:
            return

        if not self.open_file(self.UI.cmbRecents.currentText()):
            # Unable to open - remove from recents!
            self.loading = True
            self.settings.remove_recent_file(self.UI.cmbRecents.currentText())
            index = self.UI.cmbRecents.currentIndex()
            self.UI.cmbRecents.setCurrentIndex(0)
            self.UI.cmbRecents.removeItem(index)
            self.loading = False

    @Slot()
    def language_changed(self, index: int):
        current_lang = 'en'
        # if index == 0:  # English
        #     current_lang = 'en'
        if index == 1:  # French
            current_lang = 'fr'

        self.request_language_change.emit(current_lang)

    def logo_clicked(self, _: QMouseEvent):
        about_diag = AboutScreen(self)
        about_diag.exec()

