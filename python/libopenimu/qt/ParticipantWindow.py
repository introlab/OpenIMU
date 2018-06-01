from PyQt5.QtWidgets import QLineEdit, QWidget, QPushButton, QComboBox
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal

from resources.ui.python.ParticipantWidget_ui import Ui_frmParticipant
from libopenimu.models.Participant import Participant
from libopenimu.qt.DataEditor import DataEditor
from libopenimu.models.Group import Group

from libopenimu.db.DBManager import DBManager

class ParticipantWindow(DataEditor):

    participant = Participant()
    dbMan = None

    def __init__(self, dbManager, participant=None, parent=None, default_group = None):
        super(QWidget, self).__init__(parent=parent)
        self.UI = Ui_frmParticipant()
        self.UI.setupUi(self)

        self.participant = participant
        self.dbMan = dbManager
        self.data_type = "participant"

        # Signals / Slots connections
        self.UI.btnCancel.clicked.connect(self.cancel_clicked)
        self.UI.btnSave.clicked.connect(self.save_clicked)
        self.UI.txtName.textEdited.connect(self.name_edited)
        self.UI.txtDesc.textChanged.connect(self.desc_edited)
        self.UI.cmbGroups.currentIndexChanged.connect(self.group_edited)

        # Load groups
        groups = self.dbMan.get_all_groups()
        self.UI.cmbGroups.clear()
        self.UI.cmbGroups.addItem("Aucun",userData=None)

        for group in groups:
            self.UI.cmbGroups.addItem(group.name, userData=group.id_group)

        # Update data
        self.update_data()

        # Set default group for new participants
        if default_group is not None:
            self.UI.cmbGroups.setCurrentIndex(self.UI.cmbGroups.findData(default_group.id_group, Qt.UserRole))

        self.enable_buttons(False)

    def validate(self):
        rval = True
        if self.UI.txtName.text() == '':
            self.UI.txtName.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.txtName.setStyleSheet('background-color: rgba(226, 226, 226, 90%);')

        if self.UI.cmbGroups.currentIndex == -1:
            rval = False

        return rval

    def update_data(self):
        if self.participant is not None:
            self.UI.txtName.setText(self.participant.name)
            self.UI.txtDesc.setPlainText(self.participant.description)
            """if self.participant.group is not None and self.participant.group.name is not None:
                self.UI.lblGroupValue.setText(self.participant.group.name)
            else:
                self.UI.lblGroupValue.setText("Aucun")
            """
            self.UI.cmbGroups.setCurrentIndex(self.UI.cmbGroups.findData(self.participant.id_group))
        else:
            self.UI.txtName.setText("")
            self.UI.txtDesc.setPlainText("")
            self.UI.cmbGroups.setCurrentIndex(0)


    def enable_buttons(self, enable):
        self.UI.btnCancel.setEnabled(enable or self.participant is None)
        self.UI.btnSave.setEnabled(enable)

    def update_modified_status(self):
        self.enable_buttons(
                            (self.participant is not None and self.UI.txtName.text() != self.participant.name) or
                            (self.participant is None and self.UI.txtName.text() != "") or
                            (self.participant is not None and self.UI.txtDesc.toPlainText() != self.participant.description) or
                            (self.participant is None and self.UI.txtDesc.toPlainText() != "") or
                            (self.participant is not None and self.UI.cmbGroups.currentData() != self.participant.id_group)
                            )
    @pyqtSlot()
    def save_clicked(self):
        if self.validate():
            if self.participant is None:
                self.participant = Participant()
            self.participant.name = self.UI.txtName.text()
            self.participant.description = self.UI.txtDesc.toPlainText()
            self.participant.id_group = self.UI.cmbGroups.currentData()
            self.participant = self.dbMan.update_participant(self.participant)
            self.enable_buttons(False)
            self.dataSaved.emit()

    @pyqtSlot()
    def cancel_clicked(self):
        self.update_data()
        self.dataCancelled.emit()

    @pyqtSlot(str)
    def name_edited(self, new_value):
        self.update_modified_status()

    @pyqtSlot()
    def desc_edited(self):
        self.update_modified_status()

    @pyqtSlot()
    def group_edited(self):
        self.update_modified_status()