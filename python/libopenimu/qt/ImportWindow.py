from resources.ui.python.ImportDialog_ui import Ui_ImportDialog

from PySide6.QtCore import Slot, QFileInfo
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox

from libopenimu.db.DBManager import DBManager
from libopenimu.models.DataSet import DataSet
from libopenimu.tools.Settings import OpenIMUSettings

from sqlalchemy.exc import DBAPIError, DatabaseError, DataError

from datetime import datetime


class ImportWindow(QDialog):

    showImport = False
    infosOnly = False
    participants = []
    groups = []
    fileName = ''

    dataSet = None

    def __init__(self, dataset=None, parent=None, filename=None, show_import=False):
        super().__init__(parent=parent)
        self.UI = Ui_ImportDialog()
        self.UI.setupUi(self)

        # Manage data if present
        self.dataSet = dataset
        self.fileName = filename
        self.showImport = show_import
        self.update_data()

        # Signals / Slots connections
        self.UI.btnCancel.clicked.connect(self.cancel_clicked)
        self.UI.btnOK.clicked.connect(self.ok_clicked)
        self.UI.txtAuthor.textChanged.connect(self.validate)
        self.UI.txtName.textChanged.connect(self.validate)
        self.UI.txtFileName.textChanged.connect(self.validate)
        self.UI.dateData.dateChanged.connect(self.validate)
        # self.UI.btnAddFile.clicked.connect(self.addFile_clicked)
        # self.UI.btnDelFile.clicked.connect(self.removeFile_clicked)
        self.UI.btnBrowse.clicked.connect(self.browse_clicked)

    def exec(self):
        # self.UI.frameImport.setVisible(not self.showImport)
        # self.UI.splitter.setVisible(not self.noImportUI)
        if self.showImport:
            self.UI.btnOK.setText(self.tr("Next"))

        self.UI.btnBrowse.setVisible(not self.infosOnly)
        self.UI.txtFileName.setVisible(not self.infosOnly)
        self.UI.lblFile.setVisible(not self.infosOnly)

        return QDialog.exec(self)

    @Slot()
    def validate(self):
        rval = True
        if self.UI.txtFileName.text() == '' or self.UI.txtFileName.text()[-3:] != '.oi':
            self.UI.txtFileName.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.txtFileName.setStyleSheet('')

        if self.UI.txtName.text() == '':
            self.UI.txtName.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.txtName.setStyleSheet('')

        if self.UI.txtAuthor.text() == '':
            self.UI.txtAuthor.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.txtAuthor.setStyleSheet('')

        self.UI.btnOK.setEnabled(rval)
        return rval

    def update_data(self):
        if self.dataSet is not None:
            self.UI.txtAuthor.setText(self.dataSet.author)
            self.UI.txtDesc.setPlainText(self.dataSet.description)
            self.UI.txtName.setText(self.dataSet.name)
            self.UI.dateData.setDate(self.dataSet.upload_date)
        else:
            self.UI.dateData.setDate(datetime.now())
            import os
            self.UI.txtAuthor.setText(os.getlogin())
        self.UI.txtFileName.setText(self.fileName)
        self.validate()  # Show mandatory fields in red

    @Slot()
    def browse_clicked(self):
        settings = OpenIMUSettings()
        file_diag = QFileDialog.getSaveFileName(parent=self, caption=self.tr("Dataset filename"), filter="*.oi",
                                                dir=str(settings.database_base_path))

        if file_diag[0] != '':
            self.UI.txtFileName.setText(file_diag[0])
            ext = file_diag[1][-(len(file_diag[1]) - 1):]
            if file_diag[0][-len(ext):] != ext:
                self.UI.txtFileName.setText(self.UI.txtFileName.text() + ext)
            settings.database_base_path = QFileInfo(file_diag[0]).path()

    @Slot()
    def ok_clicked(self):
        # Only create file if validate
        if self.validate():

            try:
                # Create and save file
                db = DBManager(filename=self.UI.txtFileName.text(), newfile=True)

                if self.dataSet is None:
                    self.dataSet = DataSet()
                    self.dataSet.creation_date = datetime.now()

                self.dataSet.name = self.UI.txtName.text()
                self.dataSet.description = self.UI.txtDesc.toPlainText()
                self.dataSet.author = self.UI.txtAuthor.text()
                self.dataSet.upload_date = self.UI.dateData.date().toPython()

                db.set_dataset_infos(name=self.dataSet.name,
                                     desc=self.dataSet.description,
                                     author=self.dataSet.author,
                                     creation_date=self.dataSet.creation_date,
                                     upload_date=self.dataSet.upload_date)

                self.fileName = self.UI.txtFileName.text()

                self.accept()

            except (DBAPIError, DataError, DatabaseError):
                box = QMessageBox()
                box.setText(self.tr('Dataset file creation error - please choose a valid file and directory'))
                box.exec()

    @Slot()
    def cancel_clicked(self):
        self.reject()
