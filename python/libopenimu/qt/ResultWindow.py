from PySide6.QtWidgets import QWidget, QListWidgetItem, QTableWidgetItem, QHeaderView, QTableWidget
from PySide6.QtGui import QIcon, QGuiApplication, QKeyEvent, QKeySequence
from PySide6.QtCore import Qt, QObject, QEvent, Slot

from resources.ui.python.ResultWidget_ui import Ui_frmResult

from libopenimu.db.DBManager import DBManager
from libopenimu.models.ProcessedData import ProcessedData

from libopenimu.algorithms.BaseAlgorithm import BaseAlgorithmFactory

import pickle


class ResultWindow(QWidget):

    def __init__(self, manager: DBManager, results: ProcessedData, parent=None):
        super().__init__(parent=parent)
        self.UI = Ui_frmResult()
        self.UI.setupUi(self)

        self.data = results
        self.dbMan = manager
        self.UI.tabResults.setCurrentIndex(0)
        self.data_type = 'result'

        self.recordsets = []
        self.factory = None

        self.UI.btnCopyData.clicked.connect(self.copy_data_to_clipboard)

        self.update_data()

        self.UI.tableData.installEventFilter(self)
        self.UI.tableParams.installEventFilter(self)

    def update_data(self):
        # Update display
        self.UI.lblNameValue.setText(self.data.name)
        self.UI.lblTimeValue.setText(str(self.data.processed_time.strftime("%d-%m-%Y %H:%M:%S")))

        # Results sources
        for ref in self.data.processed_data_ref:
            item = QListWidgetItem()
            date_text = ref.recordset.start_timestamp.strftime("%d-%m-%Y")
            item.setText(date_text + ' / ' + ref.recordset.name)
            item.setIcon(QIcon(':/OpenIMU/icons/recordset.png'))
            self.UI.lstSources.addItem(item)
            self.recordsets.append(ref.recordset)

        # Find correct factory and display results
        self.factory = BaseAlgorithmFactory.get_factory_with_id(self.data.id_data_processor)

        if self.factory is not None:
            cdata = pickle.loads(self.data.data)  # Unpacks data from blob in database

            display_widget = self.factory.build_display_widget(self.UI.centralWidget, cdata, self.recordsets)
            self.UI.centralWidget.layout().addWidget(display_widget)

            # Data table
            table_data = self.factory.build_data_table(cdata)
            if table_data:
                self.UI.tableData.setColumnCount(len(table_data['headers']))
                self.UI.tableData.setRowCount(len(table_data['data_names']))
                self.UI.tableData.setHorizontalHeaderLabels(table_data['headers'])
                self.UI.tableData.setVerticalHeaderLabels(table_data['data_names'])

                # Fill data
                for col_index, col in enumerate(table_data['data'], start=0):
                    for row_index, row in enumerate(col, start=0):
                        item_data = QTableWidgetItem(str(row))
                        item_data.setTextAlignment(Qt.AlignCenter)
                        item_data.setBackground(Qt.lightGray)
                        self.UI.tableData.setItem(row_index, col_index, item_data)
                self.UI.tableData.horizontalHeader().resizeSections(QHeaderView.Stretch)
                self.UI.tableData.resizeColumnsToContents()

                # Parameters table
                if self.data.params:
                    import json
                    params = json.loads(self.data.params)
                    self.UI.tableParams.setColumnCount(len(params.keys()))
                    self.UI.tableParams.setHorizontalHeaderLabels(params.keys())

                    for header_index, header in enumerate(params.keys(), start=0):
                        # header_item = QTableWidgetItem(header)
                        # header_item.setBackground(QColor(Qt.lightGray))
                        # self.UI.tableParams.setItem(0, header_index, header_item)
                        item_data = QTableWidgetItem(str(params[header]))
                        item_data.setTextAlignment(Qt.AlignCenter)
                        item_data.setBackground(Qt.lightGray)
                        self.UI.tableParams.setItem(0, header_index, item_data)
                    self.UI.tableParams.resizeColumnsToContents()

    @Slot()
    def copy_data_to_clipboard(self, selected_only=False):
        self.copy_to_clipboard(source_table=self.UI.tableData, selected_only=selected_only)

    @staticmethod
    def copy_to_clipboard(source_table: QTableWidget, selected_only: bool):
        if source_table.rowCount() == 0:
            return

        clipboard = QGuiApplication.clipboard()

        if source_table.verticalHeaderItem(0):
            output = '"Variable"\t'
        else:
            output = ''

        # Headers
        for col in range(source_table.horizontalHeader().count()):
            output += '"' + source_table.horizontalHeaderItem(col).text() + '"'
            if col < source_table.columnCount() - 1:
                output += '\t'
        output += '\r\n'

        # Data
        for row in range(source_table.rowCount()):
            if selected_only and not source_table.item(row, 0).isSelected():
                continue
            if source_table.verticalHeaderItem(row):
                output += '"' + source_table.verticalHeaderItem(row).text() + '"' + '\t'
            for col in range(source_table.columnCount()):
                output += source_table.item(row, col).text()
                if col < source_table.columnCount() - 1:
                    output += '\t'
            if row < source_table.rowCount() - 1:
                output += '\r\n'
        clipboard.setText(output)

    def eventFilter(self, target: QObject, event: QEvent) -> bool:
        if target == self.UI.tableData or target == self.UI.tableParams:
            if isinstance(event, QKeyEvent):
                if event.type() == QEvent.Type.KeyRelease and event.matches(QKeySequence.Copy):
                    self.copy_to_clipboard(source_table=target, selected_only=True)
                    return True

        return super().eventFilter(target, event)

