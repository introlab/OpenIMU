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
        # print('recordsets: ', recordsets)
        self.recordsets = recordsets
        self.fill_algorithms_list()
        self.factory = None
        # Connect signals
        self.UI.btnProcess.clicked.connect(self.on_process_button_clicked)

    def fill_algorithms_list(self):
        # BaseAlgorithmFactory.print_factories()
        for factory in  BaseAlgorithmFactory.factories:
            # Add to list
            item = QListWidgetItem(factory.name())
            self.UI.listWidget.addItem(item)
            # Connect signals
            self.UI.listWidget.itemClicked.connect(self.on_list_widget_item_clicked)

    @pyqtSlot(QListWidgetItem)
    def on_list_widget_item_clicked(self, item : QListWidgetItem):
        # print('onListWidgetItemClicked')
        # Fill info
        self.factory = BaseAlgorithmFactory.get_factory_named(item.text())
        info = self.factory.info()
        if info.__contains__('author'):
            self.UI.lblAuthorValue.setText(info['author'])

        if info.__contains__('description'):
            self.UI.txtDesc.setPlainText(info['description'])

        if info.__contains__('name'):
            self.UI.lblNameValue.setText(info['name'])

        if info.__contains__('version'):
            self.UI.lblVersionValue.setText(info['version'])

        if info.__contains__('reference'):
            self.UI.lblRefValue.setText(info['reference'])

    @pyqtSlot()
    def on_process_button_clicked(self):
        print('on_process_button_clicked')
        if self.factory is not None:
            # For testing, should display a configuration GUI first
            params = {}
            algo = self.factory.create(params)
            results = algo.calculate(self.dbMan, self.recordsets)
            print('Algo results', results)
