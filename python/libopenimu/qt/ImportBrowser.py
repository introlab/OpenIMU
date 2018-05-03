from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QTableWidget, QPushButton, QPlainTextEdit, QFileDialog

from libopenimu.db.DBManager import DBManager
from libopenimu.models.DataSet import DataSet

from resources.ui.python.ImportBrowser_ui import Ui_ImportBrowser
from libopenimu.qt.ImportManager import ImportManager

class ImportBrowser(QDialog):
    dbMan = None

    def __init__(self, dataManager, parent = None):
        super(QDialog, self).__init__(parent=parent)
        self.UI = Ui_ImportBrowser()
        self.UI.setupUi(self)

        self.UI.btnCancel.clicked.connect(self.cancel_clicked)
        self.UI.btnOK.clicked.connect(self.ok_clicked)
        self.UI.btnAddFile.clicked.connect(self.add_clicked)
        self.UI.btnDelFile.clicked.connect(self.del_clicked)

        self.dbMan = dataManager

    @pyqtSlot()
    def ok_clicked(self):
        self.accept()

    @pyqtSlot()
    def cancel_clicked(self):
        self.reject()

    @pyqtSlot()
    def add_clicked(self):
        importman = ImportManager(dbManager=self.dbMan)

        if importman.exec() == QDialog.Accepted:
            # Add file to list
            table = self.UI.tableFiles

            row = table.rowCount()
            table.setRowCount(row + 1)
            cell = QTableWidgetItem()
            cell.setText(importman.filename)
            table.setItem(row, 0, cell)
            cell = QTableWidgetItem()
            cell.setText(importman.filetype)
            table.setItem(row, 1, cell)
            cell = QTableWidgetItem()
            group = ""
            if importman.participant.group is not None:
                group = importman.participant.group.name
            cell.setText(group)
            table.setItem(row, 2, cell)
            cell = QTableWidgetItem()
            cell.setText(importman.participant.name)
            table.setItem(row, 3, cell)

            table.resizeColumnsToContents()

    @pyqtSlot()
    def del_clicked(self):
        if self.UI.tableFiles.selectedItems():
            # print(self.UI.tableFiles.selectedItems()[0].row())

            self.UI.tableFiles.removeRow(self.UI.tableFiles.selectedItems()[0].row())