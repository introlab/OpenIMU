from PySide6.QtWidgets import QTableWidgetItem, QWidget
from PySide6.QtCore import Slot, Signal, Qt


class Evenson2008ConfigWidget(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent=parent)
