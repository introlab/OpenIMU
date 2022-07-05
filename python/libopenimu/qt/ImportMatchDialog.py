from PySide6.QtWidgets import QDialog, QTableWidgetItem, QComboBox, QHBoxLayout
from PySide6.QtCore import Slot

from resources.ui.python.ImportMatchDialog_ui import Ui_ImportMatchDialog
from libopenimu.qt.ParticipantWindow import ParticipantWindow
from libopenimu.tools.FileManager import FileManager


class ImportMatchDialog(QDialog):

    data_match = {}
    dbMan = None
    participants = None
    part_diag = None
    part_widget = None

    def __init__(self, dbmanager, datas, parent=None):
        super().__init__(parent=parent)
        self.UI = Ui_ImportMatchDialog()
        self.UI.setupUi(self)

        for data in datas:
            self.data_match[data] = ""

        self.dbMan = dbmanager

        # Load participants
        self.participants = self.dbMan.get_all_participants()

        # Fill table with datas
        for data in datas:
            row = self.UI.tableMatch.rowCount()
            self.UI.tableMatch.setRowCount(row+1)
            item = QTableWidgetItem(data)
            self.UI.tableMatch.setItem(row, 0, item)
            item_combo = QComboBox()
            self.fill_participant_combobox(item_combo)
            item_combo.setCurrentIndex(item_combo.findText(data))
            self.UI.tableMatch.setCellWidget(row, 1, item_combo)

        # Connect signals / slots
        self.UI.btnOK.clicked.connect(self.ok_clicked)
        self.UI.btnCancel.clicked.connect(self.cancel_clicked)
        self.UI.btnAddParticipant.clicked.connect(self.new_participant_requested)

        # Init participant dialog
        self.part_diag = QDialog(parent=self)

    def validate(self):
        rval = True

        for i in range(0, self.UI.tableMatch.rowCount()):
            item_combo = self.UI.tableMatch.cellWidget(i, 1)
            index = item_combo.currentIndex()
            if index < 0:
                item_combo.setStyleSheet('background-color: #ffcccc;')
                rval = False
            else:
                item_combo.setStyleSheet('')

        return rval

    def fill_participant_combobox(self, combobox):
        combobox.clear()
        combobox.addItem("", -1)
        for participant in self.participants:
            combobox.addItem(participant.name, userData=participant)

    @Slot()
    def ok_clicked(self):
        # Validate items
        if self.validate():
            for i in range(0, self.UI.tableMatch.rowCount()):
                item_combo = self.UI.tableMatch.cellWidget(i, 1)
                part = item_combo.currentData()
                item_value = self.UI.tableMatch.item(i, 0).text()
                self.data_match[item_value] = part
            self.accept()

    @Slot()
    def cancel_clicked(self):
        self.reject()

    @Slot()
    def new_participant_requested(self):
        layout = QHBoxLayout(self.part_diag)
        self.part_diag.setMinimumWidth(600)

        self.part_widget = ParticipantWindow(db_manager=self.dbMan)
        self.part_widget.setStyleSheet(self.styleSheet())

        # print(self.styleSheet())
        layout.addWidget(self.part_widget)

        self.part_widget.dataCancelled.connect(self.participant_cancelled)
        self.part_widget.dataSaved.connect(self.participant_saved)

        self.part_diag.exec()

    @Slot()
    def participant_cancelled(self):
        self.part_diag.reject()

    @Slot()
    def participant_saved(self):
        self.part_diag.accept()
        self.participants = self.dbMan.get_all_participants()

        # Update all comboboxes in the table with the new participant
        for i in range(0, self.UI.tableMatch.rowCount()):
            item_combo = self.UI.tableMatch.cellWidget(i, 1)
            index = item_combo.currentIndex()
            self.fill_participant_combobox(item_combo)
            item_combo.setCurrentIndex(index)

    def get_files_match(self, base_path: str) -> dict:
        # Build file list
        file_list = FileManager.get_file_list(from_path=base_path)

        file_match = {}  # Dictionary - filename and participant
        for file_name, file_dataname in file_list.items():
            part = self.data_match[file_dataname]
            file_match[file_name] = part

        return file_match
