from PySide6.QtWidgets import QTableWidgetItem, QWidget
from PySide6.QtCore import Slot, Signal, Qt

from libopenimu.qt.BaseGraph import BaseGraph
from resources.ui.python.TableDataViewWidget_ui import Ui_tableDataViewWidget
import datetime


class BeaconsView(BaseGraph, QWidget):

    # aboutToClose = Signal(QObject)
    cursorMoved = Signal(float)

    def __init__(self, parent):
        QWidget.__init__(self, parent=parent)
        BaseGraph.__init__(self)
        self.UI = Ui_tableDataViewWidget()
        self.UI.setupUi(self)

        self.beaconData = dict()
        self.UI.tableData.setColumnCount(3)
        self.UI.tableData.setHorizontalHeaderLabels([self.tr('Timestamp'), self.tr('RSSI'), self.tr('TX Power')])

        self.UI.cmbChannels.currentIndexChanged.connect(self.on_channel_changed)

    def set_cursor_position_from_time(self, timestamp, emit_signal=False):
        # Select nearest item
        label = self.UI.cmbChannels.currentText()
        if not self.beaconData[label]:
            return

        self.UI.tableData.clearSelection()

        last_timestamp = list(self.beaconData[label].keys())[0]
        if isinstance(timestamp, datetime.datetime):
            timestamp = timestamp.timestamp()

        for index, data_timestamp in enumerate(self.beaconData[label]):
            if last_timestamp <= timestamp <= data_timestamp:
                # Found item!
                self.UI.tableData.selectRow(index)
                return
            last_timestamp = data_timestamp

    def clear_selection_area(self, emit_signal=False):
        pass

    def set_selection_area_from_time(self, start_time, end_time, emit_signal=False):
        self.clear_selection_area()
        pass

    def add_channel(self, label):
        if self.UI.cmbChannels.findText(label) < 0:
            self.UI.cmbChannels.addItem(label)
        # table_widget = QTableWidget(self)
        # table_widget.setColumnCount(2)
        # table_widget.setRowCount(count)
        # table_widget.setAutoScroll(True)
        # table_widget.setColumnWidth(0, 300)
        # table_widget.setColumnWidth(1, 200)
        # table_widget.setHorizontalHeaderItem(0, QTableWidgetItem('Time'))
        # table_widget.setHorizontalHeaderItem(1, QTableWidgetItem('Value'))
        # split_label = label.split('_')
        # if len(split_label) == 3:
        #     self.addTab(table_widget, split_label[2] + ' [' + str(split_label[1]) + ']')
        # else:
        #     self.addTab(table_widget, label)
        #
        # self.tabDict[label] = table_widget

    def add_data(self, label, timestamp, tx_power=None, rssi=None):
        self.add_channel(label)

        if label not in self.beaconData:
            self.beaconData[label] = {}

        if timestamp not in self.beaconData[label]:
            self.beaconData[label][timestamp] = {'tx_power': None, 'rssi': None}

        if tx_power:
            self.beaconData[label][timestamp]['tx_power'] = tx_power

        if rssi:
            self.beaconData[label][timestamp]['rssi'] = rssi

    @Slot()
    def on_channel_changed(self):
        beacon_id = self.UI.cmbChannels.currentText()
        self.UI.tableData.clearContents()

        if beacon_id in self.beaconData:
            self.UI.tableData.setRowCount(len(self.beaconData[beacon_id]))
            row = 0
            for timestamp in self.beaconData[beacon_id]:
                item = QTableWidgetItem(str(datetime.datetime.fromtimestamp(timestamp)))
                item.setBackground(Qt.white)
                self.UI.tableData.setItem(row, 0, item)
                item = QTableWidgetItem(str(self.beaconData[beacon_id][timestamp]['rssi']))
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(Qt.white)
                self.UI.tableData.setItem(row, 1, item)
                item = QTableWidgetItem(str(self.beaconData[beacon_id][timestamp]['tx_power']))
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(Qt.white)
                self.UI.tableData.setItem(row, 2, item)
                row += 1
            self.UI.tableData.resizeColumnsToContents()
            self.total_samples = row

    # def add_row(self, row, time, value, label):
    #     if self.tabDict.__contains__(label):
    #         if row < self.tabDict[label].rowCount():
    #             # Time
    #             self.tabDict[label].setItem(row, 0, QTableWidgetItem(str(datetime.datetime.fromtimestamp(time))))
    #
    #             # Value
    #             self.tabDict[label].setItem(row, 1, QTableWidgetItem(str(value)))
    #         else:
    #             print('out of range : ', row)


