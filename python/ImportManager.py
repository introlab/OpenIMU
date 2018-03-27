from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal

from resources.ui.python.ImportManager_ui import Ui_frmImportManager


class ImportManager(QDialog):

    filename = ""
    filetype = ""
    participant = ""
    group = ""

    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent=parent)
        self.UI = Ui_frmImportManager()
        self.UI.setupUi(self)

        # Signals / Slots connections
        self.UI.btnCancel.clicked.connect(self.cancel_clicked)
        self.UI.btnImport.clicked.connect(self.ok_clicked)


    def validate(self):
        if (self.UI.txtFileName.text.isEmpty()):
            return False
        
        return True

    @pyqtSlot()
    def ok_clicked(self):
        #Validate items
        if (self.validate()):
            filename = self.UI.txtFileName.text
            filetype = QComboBox(self.UI.cmbFileType).currentText()
            participant = QComboBox(self.UI.cmbParticipant).currentText()
            group =  QComboBox(self.UI.cmbGroup).currentText()
            self.accept()

    @pyqtSlot()
    def cancel_clicked(self):
        self.reject()
