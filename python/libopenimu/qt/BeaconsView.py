import sys
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QTabWidget
from PyQt5.QtCore import QUrl, pyqtSlot, pyqtSignal, QPointF

from libopenimu.qt.BaseGraph import BaseGraph
from datetime import datetime

import numpy as np
import datetime
import collections


class BeaconsView(QTabWidget, BaseGraph):

    # aboutToClose = pyqtSignal(QObject)
    cursorMoved = pyqtSignal(float)

    def __init__(self, parent):
        super().__init__(parent=parent)

        self.tabDict = {}

    def setCursorPositionFromTime(self, timestamp, emit_signal=False):
        pass

    def zoom_reset(self):
        pass

    def zoom_in(self):
        pass

    def zoom_out(self):
        pass

    def clearSelectionArea(self, emit_signal=False):
        pass

    def setSelectionAreaFromTime(self, start_time, end_time, emit_signal=False):
        self.clearSelectionArea()
        pass

    def add_tab(self, label, count):
        table_widget = QTableWidget(self)
        table_widget.setColumnCount(2)
        table_widget.setRowCount(count)
        table_widget.setAutoScroll(True)
        table_widget.setColumnWidth(0, 300)
        table_widget.setColumnWidth(1, 200)
        table_widget.setHorizontalHeaderItem(0, QTableWidgetItem('Time'))
        table_widget.setHorizontalHeaderItem(1, QTableWidgetItem('Value'))
        split_label = label.split('_')
        if len(split_label) == 3:
            self.addTab(table_widget, split_label[2] + ' [' + str(int(split_label[1])) + ']')
        else:
            self.addTab(table_widget, label)

        self.tabDict[label] = table_widget

    def add_row(self, row, time, value, label):
        if self.tabDict.__contains__(label):
            if row < self.tabDict[label].rowCount():
                # Time
                self.tabDict[label].setItem(row, 0, QTableWidgetItem(str(datetime.datetime.fromtimestamp(time))))

                # Value
                self.tabDict[label].setItem(row, 1, QTableWidgetItem(str(value)))
            else:
                print('out of range : ', row)

    @property
    def is_zoomed(self):
        return False
