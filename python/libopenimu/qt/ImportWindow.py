from libopenimu.qt.ImportManager import ImportManager
from resources.ui.python.ImportDialog_ui import Ui_ImportDialog

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QPushButton, QPlainTextEdit, QFileDialog

from libopenimu.db.DBManager import DBManager
from libopenimu.models.DataSet import DataSet

from datetime import datetime


class ImportWindow(QDialog):

    showImport = False
    infosOnly = False
    participants = []
    groups = []
    fileName = ''

    dataSet = None

    def __init__(self, dataset=None, parent=None, filename = None, showImport = False):
        super(QDialog, self).__init__(parent=parent)
        self.UI = Ui_ImportDialog()
        self.UI.setupUi(self)

        # Manage data if present
        self.dataSet = dataset
        self.fileName = filename
        self.showImport = showImport
        self.update_data()

        # Signals / Slots connections
        self.UI.btnCancel.clicked.connect(self.cancel_clicked)
        self.UI.btnOK.clicked.connect(self.ok_clicked)
        # self.UI.btnAddFile.clicked.connect(self.addFile_clicked)
        # self.UI.btnDelFile.clicked.connect(self.removeFile_clicked)
        self.UI.btnBrowse.clicked.connect(self.browse_clicked)

    def exec(self):
        # self.UI.frameImport.setVisible(not self.showImport)
        # self.UI.splitter.setVisible(not self.noImportUI)
        if self.showImport:
            self.UI.btnOK.setText("Suivant")

        self.UI.btnBrowse.setVisible(not self.infosOnly)
        self.UI.txtFileName.setVisible(not self.infosOnly)
        self.UI.lblFile.setVisible(not self.infosOnly)

        return QDialog.exec(self)

    def validate(self):
        rval = True
        if self.UI.txtFileName.text() == '' or self.UI.txtFileName.text()[-3:] != '.oi':
            self.UI.txtFileName.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.txtFileName.setStyleSheet('background-color: rgba(226, 226, 226, 90%);')

        if self.UI.txtName.text() == '':
            self.UI.txtName.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.txtName.setStyleSheet('background-color: rgba(226, 226, 226, 90%);')

        if self.UI.txtAuthor.text() == '':
            self.UI.txtAuthor.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.txtAuthor.setStyleSheet('background-color: rgba(226, 226, 226, 90%);')

        return rval

    def update_data(self):
        if self.dataSet is not None:
            self.UI.txtAuthor.setText(self.dataSet.author)
            self.UI.txtDesc.setPlainText(self.dataSet.description)
            self.UI.txtName.setText(self.dataSet.name)
            self.UI.calendarUploadDate.setSelectedDate(self.dataSet.upload_date)
        self.UI.txtFileName.setText(self.fileName)

    @pyqtSlot()
    def browse_clicked(self):
        file_diag = QFileDialog.getSaveFileName(caption="Nom du fichier à enregistrer", filter=".oi")

        if file_diag[0] != '':
            self.UI.txtFileName.setText(file_diag[0])
            if file_diag[0][-len(file_diag[1]):] != file_diag[1]:
                self.UI.txtFileName.setText(self.UI.txtFileName.text() + file_diag[1])

    @pyqtSlot()
    def ok_clicked(self):
        # Only create file if validate
        if self.validate():
            # Create and save file
            db = DBManager(filename=self.UI.txtFileName.text())

            if self.dataSet is None:
                self.dataSet = DataSet()
                self.dataSet.creation_date = datetime.now()

            self.dataSet.name = self.UI.txtName.text()
            self.dataSet.description = self.UI.txtDesc.toPlainText()
            self.dataSet.author = self.UI.txtAuthor.text()

            self.dataSet.upload_date = self.UI.calendarUploadDate.selectedDate().toPyDate()

            db.set_dataset_infos(name=self.dataSet.name,
                                 desc=self.dataSet.description,
                                 author=self.dataSet.author,
                                 creation_date=self.dataSet.creation_date,
                                 upload_date=self.dataSet.upload_date)

            self.fileName = self.UI.txtFileName.text()

            self.accept()

    @pyqtSlot()
    def cancel_clicked(self):
        self.reject()
"""
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
"""
