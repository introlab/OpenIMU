import sys

from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QStyleFactory
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
# Models
from libopenimu.models.Participant import Participant
from libopenimu.models.Base import Base
from libopenimu.models.ProcessedData import ProcessedData

from datetime import datetime


class Treedatawidget(QTreeWidget):
    groups = {}
    participants = {}
    recordsets = {}
    results = {}
    dates = {}

    items_groups = {}
    items_participants = {}
    items_recordsets = {}
    items_results = {}
    items_dates = {}

    participantDragged = pyqtSignal(Participant)

    owner = None

    def __init__(self, parent=None):
        super(Treedatawidget, self).__init__(parent=parent)

    def remove_group(self, group):
        item = self.items_groups.get(group.id_group, None)
        # Remove all participants items in that group
        for i in range(0, item.childCount()):
            child = item.child(i)
            child_id = self.get_item_id(child)
            self.remove_participant(self.participants[child_id])

        for i in range(0, self.topLevelItemCount()):
            if self.topLevelItem(i) == item:
                self.takeTopLevelItem(i)
                self.groups[group.id_group] = None
                self.items_groups[group.id_group] = None
                break

    def remove_participant(self, participant):
        item = self.items_participants.get(participant.id_participant, None)

        # Remove all recordsets and results items from participant
        for i in range(0, item.childCount()):
            child_type = self.get_item_type(item.child(i))
            for j in range(0, item.child(i).childCount()):
                child = item.child(i).child(j)
                child_id = self.get_item_id(child)
                if child_type == "recordsets":
                    try:
                        self.remove_recordset(self.recordsets[child_id])
                    except KeyError:
                        continue
                if child_type == "results":
                    try:
                        self.remove_result(self.results[child_id])
                    except KeyError:
                        continue

        if participant.id_group is None: # Participant without a group
            for i in range(0, self.topLevelItemCount()):
                if self.topLevelItem(i) == item:
                    self.takeTopLevelItem(i)
                    break
        else:
            for i in range(0, item.parent().childCount()):
                if item.parent().child(i) == item:
                    item.parent().takeChild(i)
                    break

        self.participants[participant.id_participant] = None
        self.items_participants[participant.id_participant] = None

    def remove_recordset(self, recordset):
        item = self.items_recordsets.get(recordset.id_recordset, None)
        for i in range(0, item.parent().childCount()):
            if item.parent().child(i) == item:
                item.parent().takeChild(i)
                break

        self.recordsets[recordset.id_recordset] = None
        self.items_recordsets[recordset.id_recordset] = None

    def remove_result(self, result):
        item = self.items_results.get(result.id_processed_data, None)
        for i in range(0, item.parent().childCount()):
            if item.parent().child(i) == item:
                item.parent().takeChild(i)
                break

        self.results[result.id_processed_data] = None
        self.items_results[result.id_processed_data] = None

    def remove_date(self, date_text: str, id_parent_part: int):
        date_text_id = Treedatawidget.get_date_id(date_text, id_parent_part)

        item = self.items_dates.get(date_text_id, None)
        for i in range(0, item.parent().childCount()):
            if item.parent().child(i) == item:
                item.parent().takeChild(i)
                break

        self.dates[date_text_id] = None
        self.items_dates[date_text_id] = None

    def remove_dates_for_participant(self, id_part: int):
        search_part = "_" + str(id_part)
        for date_key in self.dates.keys():
            if date_key.endswith(search_part):
                self.remove_date(self.items_dates[date_key].text(0), id_part)

    def update_group(self, group) -> QTreeWidgetItem:
        item = self.items_groups.get(group.id_group, None)
        if item is None:
            item = QTreeWidgetItem()
            item.setText(0, group.name)
            item.setIcon(0, QIcon(':/OpenIMU/icons/group.png'))
            item.setData(0, Qt.UserRole, group.id_group)
            item.setData(1, Qt.UserRole, 'group')
            item.setFont(0, QFont('Helvetica', 12, QFont.Bold))

            self.addTopLevelItem(item)
            self.groups[group.id_group] = group
            self.items_groups[group.id_group] = item
        else:
            item.setText(0, group.name)

        return item

    def update_participant(self, part) -> QTreeWidgetItem:
        item = self.items_participants.get(part.id_participant, None)
        group_item = self.items_groups.get(part.id_group, None)
        if item is None:
            item = QTreeWidgetItem()
            item.setText(0, part.name)
            item.setIcon(0, QIcon(':/OpenIMU/icons/participant.png'))
            item.setData(0, Qt.UserRole, part.id_participant)
            item.setData(1, Qt.UserRole, 'participant')
            item.setFont(0, QFont('Helvetica', 12, QFont.Bold))

            if group_item is None: # Participant without a group
                self.addTopLevelItem(item)
            else:
                group_item.addChild(item)

            parent = item
            # Recordings
            item = QTreeWidgetItem()
            item.setText(0, 'Enregistrements')
            item.setIcon(0, QIcon(':/OpenIMU/icons/records.png'))
            item.setData(1, Qt.UserRole, 'recordsets')
            item.setFont(0, QFont('Helvetica', 11, QFont.Bold))
            parent.addChild(item)

            # Results
            item = QTreeWidgetItem()
            item.setText(0, 'Résultats')
            item.setIcon(0, QIcon(':/OpenIMU/icons/results.png'))
            item.setData(1, Qt.UserRole, 'results')
            item.setFont(0, QFont('Helvetica', 11, QFont.Bold))
            parent.addChild(item)

            item = parent
        else:
            item.setText(0, part.name)
            # Check if we must move it or not, if the group changed
            if item.parent() != group_item:
                # Old group - find and remove current item
                if item.parent() is None: # No parent...
                    for i in range(0, self.topLevelItemCount()):
                        if self.topLevelItem(i) == item:
                            item = self.takeTopLevelItem(i)
                            break
                else:
                    # Had a group...
                    for i in range(0, item.parent().childCount()):
                        if item.parent().child(i) == item:
                            item = item.parent().takeChild(i)
                            break

                # New group
                if group_item is None:  # Participant without a group
                    self.addTopLevelItem(item)
                else:
                    group_item.addChild(item)

        self.participants[part.id_participant] = part
        self.items_participants[part.id_participant] = item
        return item

    def update_recordset(self, recordset) -> QTreeWidgetItem:
        item = self.items_recordsets.get(recordset.id_recordset, None)
        if item is None:
            item = QTreeWidgetItem()
            item.setText(0, recordset.name)
            item.setIcon(0, QIcon(':/OpenIMU/icons/recordset.png'))
            item.setData(0, Qt.UserRole, recordset.id_recordset)
            item.setData(1, Qt.UserRole, 'recordset')
            item.setFont(0, QFont('Helvetica', 11, QFont.Bold))

            date_item = self.items_dates.get(recordset.start_timestamp, None)
            if date_item is None:
                date_item = self.update_date(recordset.start_timestamp, recordset.id_participant)
            date_item.addChild(item)
            # part_item = self.items_participants.get(recordset.id_participant, None)
            # if part_item is not None:
            #     for i in range(0, part_item.childCount()):
            #         if self.get_item_type(part_item.child(i)) == "recordsets":
            #             part_item.child(i).addChild(item)

        else:
            item.setText(0, recordset.name)

        self.recordsets[recordset.id_recordset] = recordset
        self.items_recordsets[recordset.id_recordset] = item

        return item

    def update_date(self, date_update: datetime, id_parent_part: int) -> QTreeWidgetItem:
        date_text = date_update.strftime("%d-%m-%Y")
        date_text_id = Treedatawidget.get_date_id(date_text=date_text, id_parent_part=id_parent_part)

        # Check if day item is already present for that date and returns it, if so.
        if date_text_id in self.items_dates:
            return self.items_dates[date_text_id]

        item = QTreeWidgetItem()
        item.setText(0, date_text)
        item.setIcon(0, QIcon(':/OpenIMU/icons/date.png'))
        item.setData(0, Qt.UserRole, 0)
        item.setData(1, Qt.UserRole, 'date')
        item.setFont(0, QFont('Helvetica', 11, QFont.Bold))

        part_item = self.items_participants.get(id_parent_part, None)
        if part_item is not None:
            for i in range(0, part_item.childCount()):
                if self.get_item_type(part_item.child(i)) == "recordsets":
                    part_item.child(i).addChild(item)
        else:
            print('No participant found in treeview for participant id=' + id_parent_part)

        self.dates[date_text_id] = date_update.date()
        self.items_dates[date_text_id] = item

        return item

    @staticmethod
    def get_date_id(date_text: str, id_parent_part: int) -> str:
        return date_text + "_" + str(id_parent_part)

    def update_result(self, result: ProcessedData) -> QTreeWidgetItem:
        item = self.items_results.get(result.id_processed_data, None)
        if item is None:
            item = QTreeWidgetItem()
            item.setText(0, result.name)
            item.setIcon(0, QIcon(':/OpenIMU/icons/result.png'))
            item.setData(0, Qt.UserRole, result.id_processed_data)
            item.setData(1, Qt.UserRole, 'result')
            item.setFont(0, QFont('Helvetica', 11, QFont.Bold))

            part_item = None
            if len(result.processed_data_ref) > 0:
                part_item = self.items_participants.get(result.processed_data_ref[0].recordset.id_participant,None)

            if part_item is not None:
                # TODO: subrecords...
                for i in range(0, part_item.childCount()):
                    if self.get_item_type(part_item.child(i)) == "results":
                        part_item.child(i).addChild(item)

        else:
            item.setText(0, result.name)

        self.results[result.id_processed_data] = result
        self.items_results[result.id_processed_data] = item

        return item

    @classmethod
    def get_item_type(cls, item):
        if item is not None:
            return item.data(1, Qt.UserRole)
        else:
            return ""

    @classmethod
    def get_item_id(cls, item):
        if item is not None:
            return item.data(0, Qt.UserRole)
        else:
            return ""

    @pyqtSlot(str, int)
    def select_item(self, item_type, item_id):
        # print ("Selecting " + item_type + ", ID " + str(item_id))
        item = None
        if item_type == "group":
            item = self.items_groups.get(item_id, None)

        if item_type == "participant":
            item = self.items_participants.get(item_id, None)

        if item_type == "recordset":
            item = self.items_recordsets.get(item_id, None)

        if item_type == "result":
            item = self.items_results.get(item_id, None)

        if item_type == "date":
            item = self.items_dates.get(item_id, None)

        if item is not None:
            self.setCurrentItem(item)
            self.owner.tree_item_clicked(item, 0)

    @pyqtSlot(str, Base)
    def update_item(self, item_type, data):
        # print ("Selecting " + item_type + ", ID " + str(item_id))
        # item = None
        if item_type == "group":
            self.update_group(data)

        if item_type == "participant":
            self.update_participant(data)

        if item_type == "recordset":
            self.update_recordset(data)

        if item_type == "result":
            self.update_result(data)

        if item_type == "date":
            self.update_date(data)

    def clear(self):

        self.groups = {}
        self.participants = {}
        self.recordsets = {}
        self.results = {}
        self.dates = {}

        self.items_groups = {}
        self.items_participants = {}
        self.items_recordsets = {}
        self.items_results = {}
        self.items_dates = {}

        super().clear()

    def dropEvent(self, event):

        index = self.indexAt(event.pos())

        source_item = self.currentItem()
        source_type = source_item.data(1, Qt.UserRole)
        source_id = source_item.data(0, Qt.UserRole)

        target_item = self.itemFromIndex(index)
        if target_item is not None:
            target_type = target_item.data(1, Qt.UserRole)
            target_id = target_item.data(0, Qt.UserRole)

        if source_type == "participant":
            # Participant can only be dragged over groups or no group at all
            if not index.isValid():
                # Clear source and set to no group
                self.participants[source_id].group = None
                self.participants[source_id].id_group = None
                # new_item = source_item.clone()
                # self.addTopLevelItem(new_item)
                self.participantDragged.emit(self.participants[source_id])
                event.accept()
                return
            else:

                if target_type == "group":
                    self.participants[source_id].group = self.groups[target_id]
                    self.participants[source_id].id_group = self.groups[target_id].id_group
                    # new_item = source_item.clone()
                    # target_item.addChild(new_item)
                    self.participantDragged.emit(self.participants[source_id])
                    event.accept()
                    return

            event.ignore()


def except_hook(cls, exception, traceback):
    # Display error dialog
    from libopenimu.qt.CrashWindow import CrashWindow
    crash_dlg = CrashWindow(traceback, exception)
    crash_dlg.exec()
    sys.__excepthook__(cls, exception, traceback)


# Main
if __name__ == '__main__':
    from PyQt5.QtCore import QDir
    from libopenimu.qt.MainWindow import MainWindow

    # Set Style
    QApplication.setStyle(QStyleFactory.create("Windows"))

    # Must be done before starting the app
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)

    sys.excepthook = except_hook
    # qInstallMessageHandler(qt_message_handler)

    # Set current directory to home path
    QDir.setCurrent(QDir.homePath())

    # print(PyQt5.__file__)
    # from pprint import pprint
    # from PyQt5.QtCore import QLibraryInfo
    # paths = [x for x in dir(QLibraryInfo) if x.endswith('Path')]
    # pprint({x: QLibraryInfo.location(getattr(QLibraryInfo, x)) for x in paths})

    # WebEngine settings
    # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
    # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
    # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
    # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls,True)
    # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)

    # Create Main Window
    window = MainWindow()

    # Exec application
    sys.exit(app.exec_())

