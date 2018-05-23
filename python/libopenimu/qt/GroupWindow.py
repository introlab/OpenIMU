from PyQt5.QtWidgets import QLineEdit, QWidget, QPushButton
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal

from resources.ui.python.GroupWidget_ui import Ui_frmGroup

from libopenimu.models.Group import Group
from libopenimu.qt.DataEditor import DataEditor

class GroupWindow(DataEditor):

    group = Group()
    dbMan = None

    def __init__(self, dbManager, group=None, parent=None):
        super(QWidget, self).__init__(parent=parent)
        self.UI = Ui_frmGroup()
        self.UI.setupUi(self)

        self.group = group
        self.dbMan = dbManager
        self.data_type = "group"

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
        self.UI.btnCancel.setEnabled(enable or self.group is None)
        self.UI.btnSave.setEnabled(enable)

    def update_modified_status(self):
        self.enable_buttons(
                            (self.group is not None and self.UI.txtName.text() != self.group.name) or
                            (self.group is None and self.UI.txtName.text() != "") or
                            (self.group is not None and self.UI.txtDesc.toPlainText() != self.group.description) or
                            (self.group is None and self.UI.txtDesc.toPlainText() != "")
                            )

    @pyqtSlot()
    def save_clicked(self):
        if self.validate():
            if self.group is None:
                self.group = Group()
            self.group.name = self.UI.txtName.text()
            self.group.description = self.UI.txtDesc.toPlainText()
            self.group = self.dbMan.update_group(self.group)
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

