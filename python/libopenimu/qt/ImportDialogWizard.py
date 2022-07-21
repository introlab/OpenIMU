from resources.ui.python.ImportDialogWizard_ui import Ui_dlgImportWizard

from PySide6.QtCore import Slot, QFileInfo
from PySide6.QtWidgets import QDialog, QFileDialog

from libopenimu.tools.Settings import OpenIMUSettings


class ImportDialogWizard(QDialog):
    useExisting = False
    databaseFilename: str = ''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.UI = Ui_dlgImportWizard()
        self.UI.setupUi(self)

        # Fill recent files
        self.settings = OpenIMUSettings()
        recent_files = self.settings.get_recent_files()
        self.UI.cmbFilename.addItems(recent_files)

        self.UI.frameExisting.hide()
        self.UI.radioNewDataset.setChecked(True)

        # Connect signals
        self.UI.radioExistingDataset.clicked.connect(self.radio_choice_changed)
        self.UI.radioNewDataset.clicked.connect(self.radio_choice_changed)
        self.UI.cmbFilename.currentTextChanged.connect(self.filename_changed)
        self.UI.btnBrowse.clicked.connect(self.browse_clicked)
        self.UI.btnNext.clicked.connect(self.next_clicked)
        self.UI.btnCancel.clicked.connect(self.cancel_clicked)

    @Slot()
    def radio_choice_changed(self):
        self.UI.frameExisting.setVisible(self.UI.radioExistingDataset.isChecked())
        self.useExisting = self.UI.radioExistingDataset.isChecked()
        if self.UI.radioExistingDataset.isChecked():
            self.UI.btnNext.setEnabled(self.UI.cmbFilename.currentText() != '')
        else:
            self.UI.btnNext.setEnabled(True)

    @Slot()
    def browse_clicked(self):

        file_diag = QFileDialog.getOpenFileName(parent=self, caption=self.tr('Dataset to import data into'),
                                                filter='*.oi', dir=self.settings.database_base_path)

        if file_diag[0] != '':
            self.UI.cmbFilename.setCurrentText(file_diag[0])
            self.settings.database_base_path = QFileInfo(file_diag[0]).path()

    @Slot()
    def filename_changed(self):
        self.UI.btnNext.setEnabled(self.UI.cmbFilename.currentText() != '')

    @Slot()
    def next_clicked(self):
        if self.useExisting:
            self.databaseFilename = self.UI.cmbFilename.currentText()

        self.accept()

    @Slot()
    def cancel_clicked(self):
        self.reject()
