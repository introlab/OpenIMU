from ImportManager import ImportManager
from resources.ui.python.ImportDialog_ui import Ui_ImportDialog

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QTableWidget


class ImportWindow(QDialog):

    noImportUI = False

    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent=parent)
        self.UI = Ui_ImportDialog()
        self.UI.setupUi(self)

        # Signals / Slots connections
        self.UI.btnCancel.clicked.connect(self.cancel_clicked)
        self.UI.btnOK.clicked.connect(self.ok_clicked)
        self.UI.btnAddFile.clicked.connect(self.addFile_clicked)
        self.UI.btnDelFile.clicked.connect(self.removeFile_clicked)

    def exec(self):
        self.UI.frameImport.setVisible(not self.noImportUI)

        return QDialog.exec(self)

    @pyqtSlot()
    def ok_clicked(self):
        self.accept()

    @pyqtSlot()
    def cancel_clicked(self):
        self.reject()

    @pyqtSlot()
    def addFile_clicked(self):
        importman = ImportManager()

        if (importman.exec() == QDialog.Accepted):
            #Add file to list
            table = self.UI.tableFiles

            row = table.rowCount()
            table.setRowCount(row+1)
            cell = QTableWidgetItem()
            cell.setText(importman.filename)
            table.setItem(row,0,cell)




    @pyqtSlot()
    def removeFile_clicked(self):
        self.accept()

