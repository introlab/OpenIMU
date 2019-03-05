from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from libopenimu.models.Sensor import Sensor

from resources.ui.python.DataInfosWidget_ui import Ui_DataInfosWidget


class DataInfosWidget(QDialog):

    def __init__(self, sensor=Sensor, sample_num=int, parent=None):
        super(DataInfosWidget, self).__init__(parent=parent)
        self.UI = Ui_DataInfosWidget()
        self.UI.setupUi(self)

        self.sensor = sensor
        self.sample_num = sample_num
        self.update_display()

        self.UI.btnOK.clicked.connect(self.close_requested)

    def update_display(self):
        self.UI.lblSensorNameValue.setText(self.sensor.name)
        self.UI.lblHWValue.setText(self.sensor.hw_name)
        self.UI.lblHWIDValue.setText(self.sensor.hw_id)
        self.UI.lblLocationValue.setText(self.sensor.location)
        self.UI.lblSamplingRateValue.setText(str(self.sensor.sampling_rate) + " Hz")
        self.UI.lblSamplesValue.setText(str(self.sample_num))
        self.UI.lblChannelsValue.setText(str(len(self.sensor.channels)))

    @pyqtSlot()
    def close_requested(self):
        self.accept()
