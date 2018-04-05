from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit, QFileDialog
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal

from resources.ui.python.ImportManager_ui import Ui_frmImportManager

from libopenimu.importers.importer_types import ImporterTypes


class ImportManager(QDialog):

    filename = ""
    filetype = ""
    participant = ""
    group = ""

    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent=parent)
        self.UI = Ui_frmImportManager()
        self.UI.setupUi(self)

        # Load supported importers
        importers = ImporterTypes()
        for i in range(0, len(importers.value_types)):
            self.UI.cmbFileType.addItem(importers.value_names[i], importers.value_types[i])

        # Signals / Slots connections
        self.UI.btnCancel.clicked.connect(self.cancel_clicked)
        self.UI.btnImport.clicked.connect(self.ok_clicked)
        self.UI.btnBrowse.clicked.connect(self.browse_clicked)

    def setParticipants(self, participants):
        self.UI.cmbParticipant.clear()

        for i in range(0, len(participants)):
            self.UI.cmbParticipant.addItem(participants[i])

    def setGroups(self,groups):
        self.UI.cmbGroup.clear()

        for i in range(0, len(groups)):
            self.UI.cmbGroup.addItem(groups[i])

    def validate(self):
        rval = True
        if (self.UI.txtFileName.text()==''):
            self.UI.txtFileName.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.txtFileName.setStyleSheet('background-color: white;')

        if (self.UI.cmbFileType.currentText()==''):
            self.UI.cmbFileType.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.cmbFileType.setStyleSheet('background-color: white;')

        if (self.UI.cmbParticipant.currentText()==''):
            self.UI.cmbParticipant.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.cmbParticipant.setStyleSheet('background-color: white;')

        return rval

    @pyqtSlot()
    def ok_clicked(self):
        #Validate items
        if (self.validate()):
            self.filename = self.UI.txtFileName.text()
            self.filetype = self.UI.cmbFileType.currentText()
            self.participant = self.UI.cmbParticipant.currentText()
            self.group =  self.UI.cmbGroup.currentText()
            self.accept()

    @pyqtSlot()
    def cancel_clicked(self):
        self.reject()

    @pyqtSlot()
    def browse_clicked(self):
        folder = QFileDialog().getExistingDirectory(caption="Sélectionnez le répertoire de données")

        if folder:
            self.UI.txtFileName.setText(folder)
