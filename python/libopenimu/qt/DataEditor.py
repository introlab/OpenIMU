from PyQt5.QtWidgets import  QWidget
from PyQt5.QtCore import pyqtSignal

class DataEditor(QWidget):

    dataSaved = pyqtSignal()
    dataCancelled = pyqtSignal()

    data_type = "none"