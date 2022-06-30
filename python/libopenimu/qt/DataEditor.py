from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal


class DataEditor(QWidget):

    dataSaved = Signal()
    dataCancelled = Signal()
    data_type = "none"
