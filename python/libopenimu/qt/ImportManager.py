from PyQt5.QtWidgets import QDialog, QFileDialog, QHBoxLayout
from PyQt5.QtCore import pyqtSlot, Qt

from resources.ui.python.ImportManager_ui import Ui_ImportManager

from libopenimu.importers.importer_types import ImporterTypes
from libopenimu.streamers.streamer_types import StreamerTypes

from libopenimu.qt.ParticipantWindow import ParticipantWindow
from libopenimu.qt.ImportMatchDialog import ImportMatchDialog

import tempfile
import os
import glob


class ImportManager(QDialog):

    filename = ""
    filetype = ""
    filetype_id = -1
    participant = ""
    group = ""
    dbMan = None
    import_dirs = False
    import_stream = False
    part_widget = None
    participant_multi = False

    def __init__(self, dbmanager, dirs, stream=False, parent=None):
        super(ImportManager, self).__init__(parent=parent)
        self.UI = Ui_ImportManager()
        self.UI.setupUi(self)

        self.import_dirs = dirs
        self.import_stream = stream

        self.dbMan = dbmanager

        # Load supported importers
        if not self.import_stream:
            importers = ImporterTypes()
            for i in range(0, len(importers.value_types)):
                # Ignore WIMU for now as Importers hasn't been updated yet.
                if importers.value_names[i] != 'WIMU':
                    self.UI.cmbFileType.addItem(importers.value_names[i], importers.value_types[i])
        else:
            streamers = StreamerTypes()
            for i in range(0, len(streamers.value_types)):
                self.UI.cmbFileType.addItem(streamers.value_names[i], streamers.value_types[i])

        if self.UI.cmbFileType.count() == 1:
            self.UI.cmbFileType.setCurrentIndex(0)
        else:
            self.UI.cmbFileType.setCurrentIndex(-1)

        if self.import_stream:
            self.UI.lblFileName.setText("Destination des données")
            self.UI.btnImport.setText("Transférer")
            self.import_dirs = True
            self.UI.txtFileName.setText(tempfile.gettempdir() + os.sep + "OpenIMU")

        self.UI.chkMultiParticipants.setVisible(self.import_dirs)

        # Signals / Slots connections
        self.UI.btnCancel.clicked.connect(self.cancel_clicked)
        self.UI.btnImport.clicked.connect(self.ok_clicked)
        self.UI.btnBrowse.clicked.connect(self.browse_clicked)
        self.UI.btnAddPart.clicked.connect(self.new_participant_requested)
        self.UI.cmbParticipant.currentIndexChanged.connect(self.current_participant_changed)
        self.UI.chkMultiParticipants.stateChanged.connect(self.multi_participants_check)

        # Load participants
        self.load_participants()

        self.part_diag = QDialog()
        # self.part_diag.setStyleSheet("QDialog{background-image:url(:/OpenIMU/background/dark_metal.jpg);}")
        self.part_diag.setStyleSheet("QDialog{background:qlineargradient(spread:pad, x1:0.483, y1:0, x2:0.511045, y2:1,"
                                     " stop:0 rgba(50, 50, 50, 255), stop:1 rgba(203, 203, 203, 255));"
                                     "border-radius:0px;}")

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

        if self.UI.frameParticipant.isVisible():
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

        layout = QHBoxLayout(self.part_diag)
        self.part_diag.setMinimumWidth(600)

        self.part_widget = ParticipantWindow(dbManager=self.dbMan)
        self.part_widget.setStyleSheet(self.styleSheet())

        # print(self.styleSheet())
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

    @pyqtSlot(int)
    def multi_participants_check(self, check_value):
        self.participant_multi = (check_value == Qt.Checked)
        self.UI.frameParticipant.setVisible(not self.participant_multi)

    def get_file_list(self):
        # Build file list
        file_list = {}  # Dictionary: file and base_data_folder (data participant ID)

        # Add files to list
        files = glob.glob(self.filename + "/**/*.*", recursive=True)  # Files in sub folders
        for file in files:
            file = file.replace("/", os.sep)
            data_name = os.path.split(file)[0].replace(self.filename, "")
            data_name = data_name.split(os.sep)[1]
            if file not in file_list:
                file_list[file] = data_name

        file_match = {}  # Dictionary - filename and participant
        if not self.participant_multi:
            for file in file_list.keys():
                file_match[file] = self.participant
        else:
            # Multiple participant - must show dialog and match.
            matcher = ImportMatchDialog(dbmanager=self.dbMan, datas=list(set(file_list.values())), parent=self)
            if matcher.exec() == QDialog.Accepted:
                for file_name, file_dataname in file_list.items():
                    part = matcher.data_match[file_dataname]
                    file_match[file_name] = part

        return file_match

