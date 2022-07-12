from PySide6.QtWidgets import QDialog, QTreeWidgetItem
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, Slot

from libopenimu.db.DBManager import DBManager
from libopenimu.models.Group import Group
from libopenimu.models.Participant import Participant
from libopenimu.models.Recordset import Recordset

from resources.ui.python.DataSelector_ui import Ui_DataSelector
from libopenimu.qt.TreeDataWidget import TreeDataWidget
import datetime


class DataSelector(QDialog):
    groups = {}
    participants = {}
    recordsets = {}
    dates = {}

    items_groups = {}
    items_participants = {}
    items_recordsets = {}
    items_dates = {}

    def __init__(self, db_manager: DBManager, parent=None):
        QDialog.__init__(self, parent=parent)
        self.UI = Ui_DataSelector()
        self.UI.setupUi(self)

        self.dbMan = db_manager
        self.load_data_from_dataset()
        self.update_buttons_states()
        self.loading = False

        self.UI.btnCancel.clicked.connect(self.cancel_clicked)
        self.UI.btnOK.clicked.connect(self.ok_clicked)
        self.UI.btnExpandAll.clicked.connect(self.expand_all_clicked)
        self.UI.btnCollapseAll.clicked.connect(self.collapse_all_clicked)
        self.UI.btnCheckAll.clicked.connect(self.check_all_clicked)
        self.UI.btnUncheckAll.clicked.connect(self.uncheck_all_clicked)
        self.UI.treeData.itemChanged.connect(self.item_changed)

    def load_data_from_dataset(self):
        self.UI.treeData.clear()

        # Groups
        groups = self.dbMan.get_all_groups()
        for group in groups:
            self.add_group(group)

        # Participants
        participants = self.dbMan.get_all_participants()
        for participant in participants:
            self.add_participant(participant)

        # Recordsets
        recordsets = self.dbMan.get_all_recordsets()
        for recordset in recordsets:
            self.add_recordset(recordset)

    def add_group(self, group: Group) -> QTreeWidgetItem:
        item = QTreeWidgetItem()
        item.setText(0, group.name)
        item.setIcon(0, QIcon(':/OpenIMU/icons/group.png'))
        item.setData(0, Qt.UserRole, group.id_group)
        item.setCheckState(0, Qt.Unchecked)

        self.UI.treeData.addTopLevelItem(item)
        self.groups[group.id_group] = group
        self.items_groups[group.id_group] = item

    def add_participant(self, part: Participant) -> QTreeWidgetItem:
        group_item = self.items_groups.get(part.id_group, None)

        item = QTreeWidgetItem()
        item.setText(0, part.name)
        item.setIcon(0, QIcon(':/OpenIMU/icons/participant.png'))
        item.setData(0, Qt.UserRole, part.id_participant)
        item.setCheckState(0, Qt.Unchecked)

        if group_item is None:  # Participant without a group
            self.UI.treeData.addTopLevelItem(item)
        else:
            group_item.addChild(item)

        self.participants[part.id_participant] = part
        self.items_participants[part.id_participant] = item

        return item

    def add_recordset(self, recordset: Recordset) -> QTreeWidgetItem:
        item = QTreeWidgetItem()
        item.setText(0, recordset.name)
        item.setIcon(0, QIcon(':/OpenIMU/icons/recordset.png'))
        item.setData(0, Qt.UserRole, recordset.id_recordset)
        item.setCheckState(0, Qt.Unchecked)

        date_item = self.items_dates.get(recordset.start_timestamp, None)
        if date_item is None:
            date_item = self.add_date(recordset.start_timestamp, recordset.id_participant)
        date_item.addChild(item)

        self.recordsets[recordset.id_recordset] = recordset
        self.items_recordsets[recordset.id_recordset] = item

        return item

    def add_date(self, date_update: datetime, id_parent_part: int) -> QTreeWidgetItem:
        date_text = date_update.strftime("%d-%m-%Y")
        date_text_id = TreeDataWidget.get_date_id(date_text=date_text, id_parent_part=id_parent_part)

        # Check if day item is already present for that date and returns it, if so.
        if date_text_id in self.items_dates:
            return self.items_dates[date_text_id]

        item = QTreeWidgetItem()
        item.setText(0, date_text)
        item.setIcon(0, QIcon(':/OpenIMU/icons/date.png'))
        item.setData(0, Qt.UserRole, 0)
        item.setCheckState(0, Qt.Unchecked)

        part_item = self.items_participants.get(id_parent_part, None)
        if part_item is not None:
            part_item.addChild(item)
        else:
            print('No participant found in treeview for participant id=' + str(id_parent_part))

        self.dates[date_text_id] = date_update.date()
        self.items_dates[date_text_id] = item

        return item

    @Slot()
    def cancel_clicked(self):
        self.reject()

    @Slot()
    def ok_clicked(self):
        self.accept()

    @Slot()
    def expand_all_clicked(self):
        self.UI.treeData.expandAll()

    @Slot()
    def collapse_all_clicked(self):
        self.UI.treeData.collapseAll()

    @Slot()
    def check_all_clicked(self):
        self.UI.treeData.expandAll()
        for i in range(self.UI.treeData.topLevelItemCount()):
            self.check_item(self.UI.treeData.topLevelItem(i), True)
        self.update_buttons_states()

    @Slot()
    def uncheck_all_clicked(self):
        self.UI.treeData.collapseAll()
        for i in range(self.UI.treeData.topLevelItemCount()):
            self.check_item(self.UI.treeData.topLevelItem(i), False)
        self.update_buttons_states()

    @Slot(QTreeWidgetItem, int)
    def item_changed(self, item: QTreeWidgetItem, col: int):
        if col != 0:
            return

        if self.loading:
            return

        self.loading = True

        if item.checkState(0) == Qt.Checked:
            # Must check all its children!
            for i in range(item.childCount()):
                self.check_item(item.child(i), True)
            item.setExpanded(True)

            # Check parents
            while item.parent():
                item.parent().setCheckState(0, Qt.Checked)
                item = item.parent()

        if item.checkState(0) == Qt.Unchecked:
            # Uncheck all childs
            for i in range(item.childCount()):
                self.check_item(item.child(i), False)

            # Unchecked, check if parent and, if all children are unchecked, uncheck the parent too!
            while item.parent():
                uncheck_count = 0
                for i in range(item.parent().childCount()):
                    if item.parent().child(i).checkState(0):
                        break
                    uncheck_count += 1

                if uncheck_count == item.parent().childCount():
                    item.parent().setCheckState(0, Qt.Unchecked)
                else:
                    break

                item = item.parent()

        self.loading = False
        self.update_buttons_states()

    def check_item(self, item: QTreeWidgetItem, check: bool):
        if check:
            item.setCheckState(0, Qt.Checked)
        else:
            item.setCheckState(0, Qt.Unchecked)

        for i in range(item.childCount()):
            self.check_item(item.child(i), check)

    def validate(self) -> bool:
        for i in range(self.UI.treeData.topLevelItemCount()):
            if self.UI.treeData.topLevelItem(i).checkState(0) == Qt.Checked:
                return True  # At least one item checked!
        return False

    def update_buttons_states(self):
        self.UI.btnOK.setEnabled(self.validate())

    def get_selected_recordsets(self) -> list[Recordset]:
        recordsets = []
        for id_recordset in self.recordsets:
            item = self.items_recordsets[id_recordset]
            if item:
                if item.checkState(0) == Qt.Checked:
                    recordsets.append(self.recordsets[id_recordset])

        return recordsets
