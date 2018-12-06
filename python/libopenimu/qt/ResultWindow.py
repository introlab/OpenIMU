from PyQt5.QtWidgets import QWidget, QListWidgetItem
from PyQt5.QtGui import QIcon

from resources.ui.python.ResultWidget_ui import Ui_frmResult

from libopenimu.db.DBManager import DBManager
from libopenimu.models.ProcessedData import ProcessedData

from libopenimu.algorithms.BaseAlgorithm import BaseAlgorithmFactory

import pickle


class ResultWindow(QWidget):

    def __init__(self, manager:DBManager, results:ProcessedData, parent=None):
        super().__init__(parent=parent)
        self.UI = Ui_frmResult()
        self.UI.setupUi(self)

        self.data = results
        self.dbMan = manager

        # Update display
        self.UI.lblNameValue.setText(self.data.name)
        self.UI.lblTimeValue.setText(str(self.data.processed_time.strftime("%d-%m-%Y %H:%M:%S")))

        self.recordsets = []
        for ref in self.data.processed_data_ref:
            #TODO: subrecords!
            item = QListWidgetItem()
            item.setText(ref.recordset.name)
            item.setIcon(QIcon(':/OpenIMU/icons/recordset.png'))
            self.UI.lstSources.addItem(item)
            self.recordsets.append(ref.recordset)

        # Find correct factory and display results
        self.factory = BaseAlgorithmFactory.get_factory_with_id(self.data.id_data_processor)

        if self.factory is not None:
            cdata = pickle.loads(self.data.data) # Unpacks data from blob in database

            display_widget = self.factory.build_display_widget(self.UI.centralWidget, cdata, self.recordsets)
            self.UI.centralWidget.layout().addWidget(display_widget)



