from PyQt5.QtWidgets import QLineEdit, QWidget, QPushButton
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal

from resources.ui.python.ResultWidget_ui import Ui_frmResult


class ResultWindow(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent=parent)
        self.UI = Ui_frmResult()
        self.UI.setupUi(self)
