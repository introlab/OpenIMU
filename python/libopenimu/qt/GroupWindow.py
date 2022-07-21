from PySide6.QtCore import Slot

from resources.ui.python.GroupWidget_ui import Ui_frmGroup

from libopenimu.models.Group import Group
from libopenimu.qt.DataEditor import DataEditor


class GroupWindow(DataEditor):

    group = Group()
    dbMan = None

    def __init__(self, db_manager, group=None, parent=None, edit_mode=False):
        super().__init__(parent=parent)
        self.UI = Ui_frmGroup()
        self.UI.setupUi(self)

        self.group = group
        self.dbMan = db_manager
        self.data_type = "group"

        # Setup editing UI
        self.set_edit_mode(edit_mode)

        # Signals / Slots connections
        self.UI.btnCancel.clicked.connect(self.cancel_clicked)
        self.UI.btnSave.clicked.connect(self.save_clicked)
        self.UI.txtName.textEdited.connect(self.name_edited)
        self.UI.txtDesc.textChanged.connect(self.desc_edited)
        self.UI.btnEdit.clicked.connect(self.edit_clicked)
        self.dbMan.groupUpdated.connect(self.db_group_updated)

        # Update data
        self.update_data()

    def validate(self):
        rval = True
        if self.UI.txtName.text() == '':
            self.UI.txtName.setStyleSheet('background-color: #ffcccc;')
            rval = False
        else:
            self.UI.txtName.setStyleSheet('')

        return rval

    def update_data(self):
        if self.group is not None:
            self.UI.txtName.setText(self.group.name)
            self.UI.txtDesc.setPlainText(self.group.description)
        else:
            self.UI.txtName.setText("")
            self.UI.txtDesc.setPlainText("")
        self.validate()

    def update_modified_status(self):
        has_changes = (self.group is not None and self.UI.txtName.text() != self.group.name) or \
                      (self.group is None and self.UI.txtName.text() != "") or \
                      (self.group is not None and self.UI.txtDesc.toPlainText() != self.group.description) or \
                      (self.group is None and self.UI.txtDesc.toPlainText() != "")
        self.UI.btnSave.setEnabled(has_changes)
        self.validate()

    @Slot()
    def save_clicked(self):
        if self.validate():
            if self.group is None:
                self.group = Group()
            self.group.name = self.UI.txtName.text()
            self.group.description = self.UI.txtDesc.toPlainText()
            self.group = self.dbMan.update_group(self.group)
            self.dataSaved.emit()

            self.set_edit_mode(False)

    @Slot()
    def cancel_clicked(self):
        self.update_data()
        self.dataCancelled.emit()
        self.set_edit_mode(False)

    @Slot(str)
    def name_edited(self, new_value):
        self.update_modified_status()

    @Slot()
    def desc_edited(self):
        self.update_modified_status()

    @Slot()
    def edit_clicked(self):
        self.set_edit_mode(self.UI.btnEdit.isVisible())

    def set_edit_mode(self, editing: bool):
        if editing:
            self.UI.btnEdit.hide()
            self.UI.frameButtons.show()
        else:
            self.UI.btnEdit.show()
            self.UI.frameButtons.hide()

        self.UI.frameData.setEnabled(editing)
        self.dataEditing.emit(editing)
        self.UI.txtName.setEnabled(editing)

    @Slot(Group)
    def db_group_updated(self, group: Group):
        self.group = group
        self.update_data()

