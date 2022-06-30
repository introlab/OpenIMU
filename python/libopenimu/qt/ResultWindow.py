from PySide6.QtWidgets import QWidget, QListWidgetItem, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QIcon, QColor, QGuiApplication
from PySide6.QtCore import Qt

from resources.ui.python.ResultWidget_ui import Ui_frmResult

from libopenimu.db.DBManager import DBManager
from libopenimu.models.ProcessedData import ProcessedData

from libopenimu.algorithms.BaseAlgorithm import BaseAlgorithmFactory

import pickle


class ResultWindow(QWidget):

    def __init__(self, manager:DBManager, results:ProcessedData, parent=None):
        super().__init__(parent=parent)
        self.UI = Ui_frmResult()
        self.UI.setupUi(self)

        self.data = results
        self.dbMan = manager

        # Update display
        self.UI.lblNameValue.setText(self.data.name)
        self.UI.lblTimeValue.setText(str(self.data.processed_time.strftime("%d-%m-%Y %H:%M:%S")))

        self.UI.btnCopyData.clicked.connect(self.copy_data_to_clipboard)

        # Results sources
        self.recordsets = []
        for ref in self.data.processed_data_ref:
            #TODO: subrecords!
            item = QListWidgetItem()
            item.setText(ref.recordset.name)
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
                self.UI.tableData.setColumnCount(len(table_data['headers'])+1)
                self.UI.tableData.setRowCount(len(table_data['data_names'])+1)
                # self.UI.tableData.setHorizontalHeaderLabels(table_data['headers'])
                # self.UI.tableData.setVerticalHeaderLabels(table_data['data_names'])
                # self.UI.tableData.horizontalHeader().setVisible(True)
                # self.UI.tableData.verticalHeader().setVisible(True)
                # Headers
                for header_index, header in enumerate(table_data['headers'], start=1):
                    header_item = QTableWidgetItem(header)
                    header_item.setBackground(QColor(Qt.lightGray))
                    self.UI.tableData.setItem(0, header_index, header_item)

                for header_index, header in enumerate(table_data['data_names'], start=1):
                    header_item = QTableWidgetItem(header)
                    header_item.setBackground(QColor(Qt.lightGray))
                    self.UI.tableData.setItem(header_index, 0, header_item)

                header_item = QTableWidgetItem('')
                header_item.setBackground(QColor(Qt.lightGray))
                self.UI.tableData.setItem(0, 0, header_item)

                # Fill data
                for col_index, col in enumerate(table_data['data'], start=1):
                    for row_index, row in enumerate(col, start=1):
                        item_data = QTableWidgetItem(str(row))
                        item_data.setTextAlignment(Qt.AlignCenter)
                        self.UI.tableData.setItem(row_index, col_index, item_data)
                self.UI.tableData.horizontalHeader().resizeSections(QHeaderView.Stretch)
                self.UI.tableData.resizeColumnsToContents()

                # Parameters table
                if self.data.params:
                    import json
                    params = json.loads(self.data.params)
                    self.UI.tableParams.setColumnCount(len(params.keys()))
                    for header_index, header in enumerate(params.keys(), start=0):
                        header_item = QTableWidgetItem(header)
                        header_item.setBackground(QColor(Qt.lightGray))
                        self.UI.tableParams.setItem(0, header_index, header_item)
                        item_data = QTableWidgetItem(str(params[header]))
                        item_data.setTextAlignment(Qt.AlignCenter)
                        self.UI.tableParams.setItem(1, header_index, item_data)
                    self.UI.tableParams.resizeColumnsToContents()

    def copy_data_to_clipboard(self):
        clipboard = QGuiApplication.clipboard()

        output = ''
        for row in range(self.UI.tableData.rowCount()):
            for col in range(self.UI.tableData.columnCount()):
                output += self.UI.tableData.item(row, col).text()
                if col < self.UI.tableData.columnCount()-1:
                    output += '\t'
            if row < self.UI.tableData.rowCount()-1:
                output += '\n'
        clipboard.setText(output)

