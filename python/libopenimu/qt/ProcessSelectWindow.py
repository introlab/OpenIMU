from PySide6.QtWidgets import QDialog, QListWidgetItem, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, Slot, QCoreApplication
from PySide6.QtGui import QIcon
from resources.ui.python.ProcessSelectDialog_ui import Ui_dlgProcessSelect

from libopenimu.db.DBManager import DBManager
from libopenimu.models.Recordset import Recordset

from libopenimu.algorithms.BaseAlgorithm import BaseAlgorithmFactory

from libopenimu.qt.BackgroundProcess import BackgroundProcess, ProgressDialog, WorkerTask


class ProcessSelectWindow(QDialog):
    processed_data = None

    def __init__(self, data_manager: DBManager, recordsets: list[Recordset], parent=None):
        super(ProcessSelectWindow, self).__init__(parent=parent)
        self.UI = Ui_dlgProcessSelect()
        self.UI.setupUi(self)
        self.dbMan = data_manager

        self.UI.tabAlgo.hide()

        # print('recordsets: ', recordsets)
        self.UI.btnProcess.setEnabled(False)
        self.recordsets = recordsets
        self.factory = None
        self.fill_algorithms_list()

        # Connect signals
        self.UI.btnProcess.clicked.connect(self.on_process_button_clicked)

    def fill_algorithms_list(self):
        # BaseAlgorithmFactory.print_factories()
        for factory in BaseAlgorithmFactory.factories:
            # Add to list
            item = QListWidgetItem(factory.name())
            item.setIcon(QIcon(':/OpenIMU/icons/result.png'))
            self.UI.listWidget.addItem(item)
            # Connect signals
            self.UI.listWidget.itemClicked.connect(self.on_list_widget_item_clicked)

        if self.UI.listWidget.count() > 0:
            self.UI.listWidget.setCurrentRow(0)
            self.on_list_widget_item_clicked(item=self.UI.listWidget.currentItem())

    @Slot(QListWidgetItem)
    def on_list_widget_item_clicked(self, item: QListWidgetItem):
        # print('onListWidgetItemClicked')
        # Fill info
        self.factory = BaseAlgorithmFactory.get_factory_named(item.text())
        info = self.factory.info()
        if info.__contains__('author'):
            self.UI.lblAuthorValue.setText(info['author'])

        if info.__contains__('description'):
            self.UI.txtDesc.setPlainText(info['description'].replace('\t', "").replace("        ",""))

        if info.__contains__('name'):
            self.UI.lblNameValue.setText(info['name'])

        if info.__contains__('version'):
            self.UI.lblVersionValue.setText(info['version'])

        if info.__contains__('reference'):
            self.UI.lblRefValue.setText(info['reference'])

        self.UI.tabAlgo.show()

        # Display params
        if self.UI.tabParams.layout():
            # Remove current layout by setting it to a temporary object
            QWidget().setLayout(self.UI.tabParams.layout())

        param_layout = QVBoxLayout()
        param_widget = self.factory.build_config_widget(self.UI.tabParams)
        param_layout.addWidget(param_widget)
        self.UI.tabParams.setLayout(param_layout)

        self.UI.btnProcess.setEnabled(True)
        self.UI.tabAlgo.setCurrentIndex(0)

    @Slot()
    def on_process_button_clicked(self):
        if self.factory is not None:

            class Processor(WorkerTask):
                def __init__(self, title, algor, dbmanager, recordsets, parent=None):
                    super(Processor, self).__init__(title, 0, parent)
                    self.algo = algor
                    self.dbMan = dbmanager
                    self.recordsets = recordsets
                    self.results = {}

                def process(self):
                    # print('Processor starting')
                    self.results = algo.calculate(self.dbMan, self.recordsets)
                    # print('results:', self.results)
                    # print('Processor done!')

                def get_results(self):
                    # print('getting results')
                    return self.results

            # Initialize processor
            params = self.factory.params()
            algo = self.factory.create(params)

            # Remove recordsets that don't have the required sensors
            required_sensors = self.factory.required_sensors()
            for recordset in self.recordsets:
                sensors = self.dbMan.get_sensors(recordset)
                sensors_types = []
                for sensor in sensors:
                    sensors_types.append(sensor.id_sensor_type)
                ok = all(elem in sensors_types for elem in required_sensors)
                if not ok:
                    self.recordsets.remove(recordset)

            # Create background process
            processor = Processor(title=self.UI.lblNameValue.text(), algor=algo, dbmanager=self.dbMan,
                                  recordsets=self.recordsets)
            process = BackgroundProcess([processor])

            # Create progress dialog
            dialog = ProgressDialog(process, self.tr('Data processing'), self)

            # process.finished.connect(dialog.accept)
            # process.trigger.connect(dialog.trigger)
            process.start()

            # dialog.exec()
            dialog.show()
            while process.isRunning():
                QCoreApplication.processEvents()

            results = processor.get_results()

            # results = algo.calculate(self.dbMan, self.recordsets)
            # print('Algo results', results)

            # window = QMainWindow(self)
            # window.setWindowTitle('Results: ' + self.factory.info()['name'])
            # widget = ResultWindow(self)
            # widget.display_freedson_1998(results, self.recordsets)
            # window.setCentralWidget(widget)
            # window.resize(800, 600)
            # window.show()

            # Save to database
            name = self.factory.info()['name'] + " - " + self.recordsets[0].name
            if len(self.recordsets) > 1:
                name += " @ " + self.recordsets[len(self.recordsets) - 1].name

            self.processed_data = self.dbMan.add_processed_data(self.factory.info()['unique_id'], name, results,
                                                                self.recordsets, params)

            self.accept()
