from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit, QFileDialog, QHBoxLayout, QListWidgetItem, QMainWindow
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal
from resources.ui.python.ProcessSelectDialog_ui import Ui_dlgProcessSelect
from libopenimu.db.DBManager import DBManager
from libopenimu.algorithms.BaseAlgorithm import BaseAlgorithmFactory
from libopenimu.qt.ResultWindow import ResultWindow

from libopenimu.models.ProcessedData import ProcessedData
from libopenimu.models.Recordset import Recordset


class ProcessSelectWindow(QDialog):
    id_result = -1
    def __init__(self, dataManager : DBManager, recordsets : list, parent=None):
        super(QDialog, self).__init__(parent=parent)
        self.UI = Ui_dlgProcessSelect()
        self.UI.setupUi(self)
        self.dbMan = dataManager

        self.UI.frameInfos.hide()

        # print('recordsets: ', recordsets)
        self.recordsets = recordsets
        self.fill_algorithms_list()
        self.factory = None

        self.UI.btnProcess.setEnabled(False)
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
            self.UI.txtDesc.setPlainText(info['description'].replace('\t',"").replace("        ",""))

        if info.__contains__('name'):
            self.UI.lblNameValue.setText(info['name'])

        if info.__contains__('version'):
            self.UI.lblVersionValue.setText(info['version'])

        if info.__contains__('reference'):
            self.UI.lblRefValue.setText(info['reference'])

        self.UI.frameInfos.show()
        self.UI.btnProcess.setEnabled(True)

    @pyqtSlot()
    def on_process_button_clicked(self):
        print('on_process_button_clicked')
        if self.factory is not None:
            # For testing, should display a configuration GUI first
            params = {}
            algo = self.factory.create(params)
            results = algo.calculate(self.dbMan, self.recordsets)
            print('Algo results', results)
            """window = QMainWindow(self)
            window.setWindowTitle('Results: ' + self.factory.info()['name'])
            widget = ResultWindow(self)
            widget.display_freedson_1998(results, self.recordsets)
            window.setCentralWidget(widget)
            window.resize(800, 600)
            window.show()"""

            #Save to database
            name = self.factory.info()['name'] + " - " + self.recordsets[0].name
            if len(self.recordsets) > 1:
                name += " @ " + self.recordsets[len(self.recordsets) - 1].name

            added = self.dbMan.add_processed_data(self.factory.info()['unique_id'], name, results, self.recordsets)
            self.id_result = added.id_processed_data

            self.accept()

