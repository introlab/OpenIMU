from PyQt5.QtWidgets import QLineEdit, QWidget, QPushButton
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal

from resources.ui.python.GroupWidget_ui import Ui_frmGroup

from libopenimu.models.Group import Group


class GroupWindow(QWidget):

    group = Group()

    def __init__(self, group=None, parent=None):
        super(QWidget, self).__init__(parent=parent)
        self.UI = Ui_frmGroup()
        self.UI.setupUi(self)

        self.group = group

        # Signals / Slots connections
        self.UI.btnCancel.clicked.connect(self.cancel_clicked)
        self.UI.btnSave.clicked.connect(self.save_clicked)
        self.UI.txtName.textEdited.connect(self.name_edited)
        self.UI.txtDesc.textChanged.connect(self.desc_edited)

        # Update data
        self.update_data()

        self.enable_buttons(False)

    def validate(self):
        rval = True
        if self.UI.txtName.text() == '':
            self.UI.txtName.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.txtName.setStyleSheet('background-color: white;')

        return rval

    def update_data(self):
        if self.group is not None:
            self.UI.txtName.setText(self.group.name)
            self.UI.txtDesc.setPlainText(self.group.description)
        else:
            self.UI.txtName.setText("")
            self.UI.txtDesc.setPlainText("")

    def enable_buttons(self, enable):
        self.UI.btnCancel.setEnabled(enable)
        self.UI.btnSave.setEnabled(enable)

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
        self.enable_buttons(True)

    @pyqtSlot()
    def desc_edited(self):
        # TODO: Compare with values from model and set buttons accordingly
        self.enable_buttons(True)