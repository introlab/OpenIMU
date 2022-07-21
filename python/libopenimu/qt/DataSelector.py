from PySide6.QtWidgets import QWidget, QTreeWidgetItem
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, Slot, Signal

from libopenimu.db.DBManager import DBManager
from libopenimu.models.Group import Group
from libopenimu.models.Participant import Participant
from libopenimu.models.Recordset import Recordset
from libopenimu.models.ProcessedData import ProcessedData

from resources.ui.python.DataSelector_ui import Ui_DataSelector
from libopenimu.qt.TreeDataWidget import TreeDataWidget
import datetime


class DataSelector(QWidget):

    dataIsValid = Signal(bool)

    def __init__(self, db_manager: DBManager, allow_only_one_participant=False, show_results=False, parent=None):
        QWidget.__init__(self, parent=parent)

        # Data holders
        self.groups = {}
        self.participants = {}
        self.recordsets = {}
        self.dates = {}
        self.results = {}

        self.items_groups = {}
        self.items_participants = {}
        self.items_recordsets = {}
        self.items_dates = {}
        self.items_results = {}

        self.UI = Ui_DataSelector()
        self.UI.setupUi(self)

        self.only_one_participant = allow_only_one_participant
        self.show_results = show_results

        self.dbMan = db_manager
        self.load_data_from_dataset()

        self.loading = False

        self.UI.lblOnlyOneParticipant.setVisible(self.only_one_participant)
        self.UI.btnCheckAll.setEnabled(not self.only_one_participant)

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

        # Results
        if self.show_results:
            for participant in participants:
                results = self.dbMan.get_all_processed_data(participant=participant)
                for result in results:
                    self.add_result(result, participant.id_participant)

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

    def add_result(self, result: ProcessedData, id_participant: int) -> QTreeWidgetItem:
        item = QTreeWidgetItem()
        item.setText(0, result.name)
        item.setIcon(0, QIcon(':/OpenIMU/icons/result.png'))
        item.setData(0, Qt.UserRole, result.id_processed_data)
        item.setCheckState(0, Qt.Unchecked)

        parent_item = self.items_participants[id_participant]
        if parent_item:
            parent_item.addChild(item)

        self.results[result.id_processed_data] = result
        self.items_results[result.id_processed_data] = item

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
        self.validate()

    @Slot()
    def uncheck_all_clicked(self):
        self.UI.treeData.collapseAll()
        for i in range(self.UI.treeData.topLevelItemCount()):
            self.check_item(self.UI.treeData.topLevelItem(i), False)
        self.validate()

    @Slot(QTreeWidgetItem, int)
    def item_changed(self, item: QTreeWidgetItem, col: int):
        if col != 0:
            return

        if self.loading:
            return

        self.loading = True
        check = item.checkState(0) == Qt.Checked

        if check:
            # Must check all its children!
            for i in range(item.childCount()):
                self.check_item(item.child(i), True)
            item.setExpanded(True)

            # Check parents
            while item.parent():
                item.parent().setCheckState(0, Qt.Checked)
                item = item.parent()

        else:
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

        if not item.parent():
            # Root item, manage only select one participant
            if self.only_one_participant:
                # Enable / disable all others
                for i in range(self.UI.treeData.topLevelItemCount()):
                    root_item = self.UI.treeData.topLevelItem(i)
                    if root_item != item:
                        if check:
                            root_item.setDisabled(True)
                        else:
                            root_item.setDisabled(False)

        self.loading = False
        self.validate()

    def check_item(self, item: QTreeWidgetItem, check: bool):
        if check:
            item.setCheckState(0, Qt.Checked)
        else:
            item.setCheckState(0, Qt.Unchecked)

        for i in range(item.childCount()):
            self.check_item(item.child(i), check)

    def validate(self) -> bool:
        rval = False
        for i in range(self.UI.treeData.topLevelItemCount()):
            if self.UI.treeData.topLevelItem(i).checkState(0) == Qt.Checked:
                rval = True  # At least one item checked!
                break
        self.dataIsValid.emit(rval)
        return rval

    def get_selected_recordsets(self) -> list[Recordset]:
        recordsets = []
        for id_recordset in self.recordsets:
            item = self.items_recordsets[id_recordset]
            if item:
                if item.checkState(0) == Qt.Checked:
                    recordsets.append(self.recordsets[id_recordset])

        return recordsets

    def get_selected_groups(self) -> list[Group]:
        groups = []
        for id_group in self.groups:
            item = self.items_groups[id_group]
            if item:
                if item.checkState(0) == Qt.Checked:
                    groups.append(self.groups[id_group])

        return groups

    def get_selected_participants(self) -> list[Participant]:
        participants = []
        for id_participant in self.participants:
            item = self.items_participants[id_participant]
            if item:
                if item.checkState(0) == Qt.Checked:
                    participants.append(self.participants[id_participant])

        return participants

    def get_selected_results(self) -> list[ProcessedData]:
        results = []
        for id_processed_data in self.results:
            item = self.items_results[id_processed_data]
            if item:
                if item.checkState(0) == Qt.Checked:
                    results.append(self.results[id_processed_data])

        return results

    def get_all_selected(self) -> dict:  # Return ids of selected items
        rval = {'groups': [group.id_group for group in self.get_selected_groups()],
                'participants': [part.id_participant for part in self.get_selected_participants()],
                'recordsets': [r.id_recordset for r in self.get_selected_recordsets()],
                'results': [r.id_processed_data for r in self.get_selected_results()]}
        return rval
