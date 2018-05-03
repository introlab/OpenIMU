from PyQt5.QtWidgets import QLineEdit, QWidget, QPushButton, QListWidget,QListWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal, QModelIndex

from resources.ui.python.RecordsetWidget_ui import Ui_frmRecordsets

from libopenimu.models.Recordset import Recordset
from libopenimu.db.DBManager import DBManager


class RecordsetWindow(QWidget):

    recordsets = []
    dbMan = None
    sensors = []

    def __init__(self, manager, recordset, parent=None):
        super(QWidget, self).__init__(parent=parent)
        self.UI = Ui_frmRecordsets()
        self.UI.setupUi(self)

        self.dbMan = manager
        self.recordsets = recordset

        # Load sensors for that recordset
        self.load_sensors()

    def load_sensors(self):
        self.UI.lstSensors.clear()

        for record in self.recordsets:
            self.sensors = self.dbMan.get_sensors(record)
            for sensor in self.sensors:
                index = -1
                location_item = self.UI.lstSensors.findItems(sensor.location, Qt.MatchExactly)
                if len(location_item) == 0:
                    item = QListWidgetItem(sensor.location)
                    item.setFlags(Qt.NoItemFlags)
                    self.UI.lstSensors.addItem(item)
                else:
                    self.UI.lstSensors.indexFromItem(location_item[0]).row()

                item = QListWidgetItem(QIcon(':/OpenIMU/icons/sensor.png'), sensor.name + " (" + sensor.hw_name + ")")
                item.setCheckState(Qt.Unchecked)
                if index == -1:
                    self.UI.lstSensors.addItem(item)
                else:
                    self.UI.lstSensors.insertItem(index+1,item)
