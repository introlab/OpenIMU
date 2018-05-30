from PyQt5.QtWidgets import QLineEdit, QWidget, QPushButton, QScrollArea, QVBoxLayout, QListWidgetItem
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon

from resources.ui.python.ResultWidget_ui import Ui_frmResult
from libopenimu.qt.Charts import OpenIMUBarGraphView

from libopenimu.db.DBManager import DBManager
from libopenimu.models.ProcessedData import ProcessedData
from libopenimu.models.ProcessedDataRef import ProcessedDataRef

from libopenimu.algorithms.BaseAlgorithm import BaseAlgorithmFactory

import pickle

class ResultWindow(QWidget):

    def __init__(self, manager:DBManager, results:ProcessedData, parent=None):
        super(QWidget, self).__init__(parent=parent)
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



"""
    def display_freedson_1998(self, results : list, recordsets : list):

        layout = QVBoxLayout()
        # Add Scroll area
        scroll = QScrollArea(parent=self.UI.centralWidget)
        self.UI.centralLayout.addWidget(scroll)

        scroll.setLayout(layout)
        layout.addWidget(scroll)
        view = OpenIMUBarGraphView(scroll)
        view.set_title('Active minutes')
        layout.addWidget(view)

        if len(results) == len(recordsets):
            for i in range(len(results)):
                view.set_category_axis(results[i].keys())
                values = []

                for key in results[i]:
                    values.append(results[i][key])

                label = recordsets[i].name
                view.add_set(label, values)

        # Update view
        view.update()


"""


