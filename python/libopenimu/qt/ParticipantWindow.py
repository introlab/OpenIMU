from PyQt5.QtWidgets import QLineEdit, QWidget, QPushButton
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal

from resources.ui.python.ParticipantWidget_ui import Ui_frmParticipant


class ParticipantWindow(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent=parent)
        self.UI = Ui_frmParticipant()
        self.UI.setupUi(self)

        # Signals / Slots connections
        self.UI.btnCancel.clicked.connect(self.cancel_clicked)
        self.UI.btnSave.clicked.connect(self.save_clicked)
        self.UI.txtName.textEdited.connect(self.name_edited)
        self.UI.txtDesc.textChanged.connect(self.desc_edited)

    def validate(self):
        rval = True
        if (self.UI.txtName.text() == ''):
            self.UI.txtName.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.txtName.setStyleSheet('background-color: white;')

        return rval

    @pyqtSlot()
    def save_clicked(self):
        if self.validate():
            print("TODO!")

    @pyqtSlot()
    def cancel_clicked(self):
        print("TODO!")

    @pyqtSlot(str)
    def name_edited(self, new_value):
        # TODO: Compare with values from model and set buttons accordingly
        self.UI.btnCancel.setEnabled(True)
        self.UI.btnSave.setEnabled(True)

    @pyqtSlot()
    def desc_edited(self):
        # TODO: Compare with values from model and set buttons accordingly
        self.UI.btnCancel.setEnabled(True)
        self.UI.btnSave.setEnabled(True)