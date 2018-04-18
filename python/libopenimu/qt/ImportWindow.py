from libopenimu.qt.ImportManager import ImportManager
from resources.ui.python.ImportDialog_ui import Ui_ImportDialog

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QPushButton, QPlainTextEdit, QFileDialog

from libopenimu.db.DBManager import DBManager

import datetime

class ImportWindow(QDialog):

    noImportUI = False
    participants = []
    groups = []

    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent=parent)
        self.UI = Ui_ImportDialog()
        self.UI.setupUi(self)

        # Signals / Slots connections
        self.UI.btnCancel.clicked.connect(self.cancel_clicked)
        self.UI.btnOK.clicked.connect(self.ok_clicked)
        self.UI.btnAddFile.clicked.connect(self.addFile_clicked)
        self.UI.btnDelFile.clicked.connect(self.removeFile_clicked)
        self.UI.btnBrowse.clicked.connect(self.browse_clicked)


    def exec(self):
        self.UI.frameImport.setVisible(not self.noImportUI)

        return QDialog.exec(self)

    def validate(self):
        rval = True
        if self.UI.txtFileName.text() == '' or self.UI.txtFileName.text()[-3:] != '.oi':
            self.UI.txtFileName.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.txtFileName.setStyleSheet('background-color: white;')

        if self.UI.txtName.text() == '':
            self.UI.txtName.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.txtName.setStyleSheet('background-color: white;')

        if self.UI.txtAuthor.text() == '':
            self.UI.txtAuthor.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.txtAuthor.setStyleSheet('background-color: white;')

        return rval

    @pyqtSlot()
    def browse_clicked(self):
        file_diag = QFileDialog.getSaveFileName(caption="Nom du fichier à enregistrer",filter=".oi")

        if file_diag[0] != '':
            self.UI.txtFileName.setText(file_diag[0])
            if file_diag[0][-len(file_diag[1]):] != file_diag[1]:
                self.UI.txtFileName.setText(self.UI.txtFileName.text() + file_diag[1])

    @pyqtSlot()
    def ok_clicked(self):
        # Create and save new file
        db = DBManager(filename=self.UI.txtFileName.text())

        db.set_dataset_infos(name = self.UI.txtName.text(),
                             desc = self.UI.txtDesc.toPlainText(),
                             author = self.UI.txtAuthor.text(),
                             creation_date=datetime.datetime.now(),
                             upload_date=self.UI.calendarUploadDate.selectedDate().toPyDate())

        if self.validate():
            self.accept()

    @pyqtSlot()
    def cancel_clicked(self):
        self.reject()

    @pyqtSlot()
    def addFile_clicked(self):
        importman = ImportManager()
        importman.setParticipants(self.participants)
        importman.setGroups(self.groups)

        if (importman.exec() == QDialog.Accepted):
            #Add file to list
            table = self.UI.tableFiles

            row = table.rowCount()
            table.setRowCount(row+1)
            cell = QTableWidgetItem()
            cell.setText(importman.filename)
            table.setItem(row,0,cell)
            cell = QTableWidgetItem()
            cell.setText(importman.filetype)
            table.setItem(row, 1, cell)
            cell = QTableWidgetItem()
            cell.setText(importman.group)
            table.setItem(row, 2, cell)
            cell = QTableWidgetItem()
            cell.setText(importman.participant)
            table.setItem(row, 3, cell)

            if importman.participant not in self.participants:
                self.participants.append(importman.participant)

            if importman.group not in self.groups:
                self.groups.append(importman.group)


    @pyqtSlot()
    def removeFile_clicked(self):

        if self.UI.tableFiles.selectedItems():
            #print(self.UI.tableFiles.selectedItems()[0].row())

            self.UI.tableFiles.removeRow(self.UI.tableFiles.selectedItems()[0].row())

