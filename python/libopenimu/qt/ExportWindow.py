from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit, QFileDialog, QHBoxLayout
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal
from resources.ui.python.ExportCSV_ui import Ui_ExportCSV


class ExportWindow(QDialog):
    def __init__(self, dataManager, parent = None):
        super(QDialog, self).__init__(parent=parent)
        self.UI = Ui_ExportCSV()
        self.UI.setupUi(self)
