from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit, QFileDialog, QHBoxLayout, QListWidgetItem
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal
from resources.ui.python.ProcessSelectDialog_ui import Ui_dlgProcessSelect
from libopenimu.db.DBManager import DBManager
from libopenimu.algorithms.BaseAlgorithm import BaseAlgorithmFactory


class ProcessSelectWindow(QDialog):
    def __init__(self, dataManager : DBManager, recordsets : list, parent=None):
        super(QDialog, self).__init__(parent=parent)
        self.UI = Ui_dlgProcessSelect()
        self.UI.setupUi(self)
        self.dbMan = dataManager
        print('recordsets: ', recordsets)
        self.fill_algorithms_list()


    def fill_algorithms_list(self):
        BaseAlgorithmFactory.print_factories()
        for factory in  BaseAlgorithmFactory.factories:
            # Add to list
            self.UI.listWidget.addItem(QListWidgetItem(factory.name()))


