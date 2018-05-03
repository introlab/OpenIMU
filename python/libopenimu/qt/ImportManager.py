from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit, QFileDialog, QHBoxLayout
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal

from resources.ui.python.ImportManager_ui import Ui_frmImportManager

from libopenimu.importers.importer_types import ImporterTypes
from libopenimu.db.DBManager import DBManager

from libopenimu.qt.ParticipantWindow import ParticipantWindow


class ImportManager(QDialog):

    filename = ""
    filetype = ""
    participant = ""
    group = ""
    dbMan = None

    def __init__(self, dbManager, parent=None):
        super(QDialog, self).__init__(parent=parent)
        self.UI = Ui_frmImportManager()
        self.UI.setupUi(self)

        self.dbMan = dbManager

        # Load supported importers
        importers = ImporterTypes()
        for i in range(0, len(importers.value_types)):
            self.UI.cmbFileType.addItem(importers.value_names[i], importers.value_types[i])
        self.UI.cmbFileType.setCurrentIndex(-1)

        # Signals / Slots connections
        self.UI.btnCancel.clicked.connect(self.cancel_clicked)
        self.UI.btnImport.clicked.connect(self.ok_clicked)
        self.UI.btnBrowse.clicked.connect(self.browse_clicked)
        self.UI.btnAddPart.clicked.connect(self.new_participant_requested)
        self.UI.cmbParticipant.currentIndexChanged.connect(self.current_participant_changed)

        # Load participants
        self.load_participants()


    def load_participants(self):
        participants = self.dbMan.get_all_participants()
        self.UI.cmbParticipant.clear()

        for part in participants:
            self.UI.cmbParticipant.addItem(part.name, userData=part)

        self.UI.cmbParticipant.setCurrentIndex(-1)

    def validate(self):
        rval = True
        if self.UI.txtFileName.text()=='':
            self.UI.txtFileName.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.txtFileName.setStyleSheet('')

        if (self.UI.cmbFileType.currentText()==''):
            self.UI.cmbFileType.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.cmbFileType.setStyleSheet('')

        if (self.UI.cmbParticipant.currentText()==''):
            self.UI.cmbParticipant.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.cmbParticipant.setStyleSheet('')

        return rval

    @pyqtSlot()
    def ok_clicked(self):
        #Validate items
        if (self.validate()):
            self.filename = self.UI.txtFileName.text()
            self.filetype = self.UI.cmbFileType.currentText()
            self.participant = self.UI.cmbParticipant.currentData()
            self.accept()

    @pyqtSlot()
    def cancel_clicked(self):
        self.reject()

    @pyqtSlot()
    def browse_clicked(self):
        file = QFileDialog().getOpenFileName(caption="Sélectionnez le fichier à importer")

        if file[0]:
            self.UI.txtFileName.setText(file[0])

    @pyqtSlot()
    def new_participant_requested(self):
        self.part_diag = QDialog()
        layout = QHBoxLayout(self.part_diag)

        self.part_widget = ParticipantWindow(dbManager=self.dbMan)
        layout.addWidget(self.part_widget )

        self.part_widget.dataCancelled.connect(self.participant_cancelled)
        self.part_widget.dataSaved.connect(self.participant_saved)

        self.part_diag.exec()

    @pyqtSlot()
    def participant_cancelled(self):
        self.part_diag.reject()


    @pyqtSlot()
    def participant_saved(self):
        self.part_diag.accept()
        self.load_participants()

        self.UI.cmbParticipant.setCurrentText(self.part_widget.participant.name)

    @pyqtSlot()
    def current_participant_changed(self):
        if self.UI.cmbParticipant.currentIndex() == -1:
            self.UI.lblGroupName.setText("")
            return

        part = self.UI.cmbParticipant.currentData()
        if part.group is None:
            self.UI.lblGroupName.setText("Aucun")
        else:
            self.UI.lblGroupName.setText(self.UI.cmbParticipant.currentData().group.name)