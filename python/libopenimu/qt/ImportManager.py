from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit, QFileDialog, QHBoxLayout
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal

from resources.ui.python.ImportManager_ui import Ui_ImportManager

from libopenimu.importers.importer_types import ImporterTypes
from libopenimu.db.DBManager import DBManager

from libopenimu.qt.ParticipantWindow import ParticipantWindow


class ImportManager(QDialog):

    filename = ""
    filetype = ""
    filetype_id = -1
    participant = ""
    group = ""
    dbMan = None
    import_dirs = False

    def __init__(self, dbManager, parent=None):
        super(QDialog, self).__init__(parent=parent)
        self.UI = Ui_ImportManager()
        self.UI.setupUi(self)

        self.dbMan = dbManager

        # Load supported importers
        importers = ImporterTypes()
        for i in range(0, len(importers.value_types)):
            # Ignore WIMU for now as Importers hasn't been updated yet.
            if importers.value_names[i] != 'WIMU':
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
        if self.UI.txtFileName.text() == '':
            self.UI.txtFileName.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.txtFileName.setStyleSheet('')

        if self.UI.cmbFileType.currentText() == '':
            self.UI.cmbFileType.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.cmbFileType.setStyleSheet('')

        if self.UI.cmbParticipant.currentText() == '':
            self.UI.cmbParticipant.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.cmbParticipant.setStyleSheet('')

        return rval

    def set_participant(self, name):
        self.UI.cmbParticipant.setCurrentText(name);

    def set_filetype(self, format_text):
        self.UI.cmbFileType.setCurrentText(format_text)

    @pyqtSlot()
    def ok_clicked(self):
        # Validate items
        if self.validate():
            self.filename = self.UI.txtFileName.text()
            self.filetype = self.UI.cmbFileType.currentText()
            self.filetype_id = self.UI.cmbFileType.currentData()
            self.participant = self.UI.cmbParticipant.currentData()
            self.accept()

    @pyqtSlot()
    def cancel_clicked(self):
        self.reject()

    @pyqtSlot()
    def browse_clicked(self):
        if not self.import_dirs:
            file = QFileDialog().getOpenFileNames(caption="Sélectionnez le(s) fichier(s) à importer")
        else:
            file = QFileDialog().getExistingDirectory(caption="Sélectionnez le répertoire à importer")

        if len(file) > 0:
            if not self.import_dirs:
                sep = ";"
                self.UI.txtFileName.setText(sep.join(file[0]))
            else:
                self.UI.txtFileName.setText(file)

    @pyqtSlot()
    def new_participant_requested(self):
        self.part_diag = QDialog()
        self.part_diag.setStyleSheet("QDialog{background-image:url(:/OpenIMU/background/dark_metal.jpg);}")
        layout = QHBoxLayout(self.part_diag)
        self.part_diag.setMinimumWidth(600)

        self.part_widget = ParticipantWindow(dbManager=self.dbMan)
        self.part_widget.setStyleSheet(self.styleSheet())

        #print(self.styleSheet())
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
