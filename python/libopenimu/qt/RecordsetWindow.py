from PyQt5.QtWidgets import QLineEdit, QWidget, QPushButton, QListWidget, QListWidgetItem, QGraphicsScene, QGraphicsRectItem, QGraphicsItem, QGraphicsView, QGraphicsTextItem
from PyQt5.QtGui import QIcon, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal, QModelIndex

from resources.ui.python.RecordsetWidget_ui import Ui_frmRecordsets

from libopenimu.models.Recordset import Recordset
from libopenimu.db.DBManager import DBManager

from datetime import datetime,timedelta
from random import shuffle

class RecordsetWindow(QWidget):

    recordsets = []
    dbMan = None
    sensors = []
    sensors_colors = []

    #sensorsColor = ['e0c31e', '14148c', '006325', '6400aa', '14aaff', 'ae32a0', '80c342', '868482']

    def __init__(self, manager, recordset, parent=None):
        super(QWidget, self).__init__(parent=parent)
        self.UI = Ui_frmRecordsets()
        self.UI.setupUi(self)

        self.dbMan = manager
        self.recordsets = recordset

        # Init temporal browser
        self.timeScene = QGraphicsScene()
        self.UI.graphTimeline.setScene(self.timeScene)
        self.UI.graphTimeline.fitInView(self.timeScene.sceneRect(),Qt.KeepAspectRatio)
        """blackBrush = QBrush(Qt.black)
        blueBrush = QBrush(Qt.blue)
        blackPen = QPen(Qt.black)
        self.timeScene.addRect(100, 0, 80, 100, blackPen, blueBrush)
        rectangle = self.timeScene.addRect(100, 0, 80, 100, blackPen, blackBrush)
        rectangle.setFlag(QGraphicsItem.ItemIsMovable)"""

        # Update general informations about recordsets
        self.update_recordset_infos()

        # Load sensors for that recordset
        self.load_sensors()

    def paintEvent(self, QPaintEvent):
        self.draw_recordsets()
        self.draw_sensors()
        self.draw_dates()

    def load_sensors(self):
        self.UI.lstSensors.clear()
        self.sensors = []

        # Create sensor colors
        used_colors = []
        #colors = QColor.colorNames()
        colors = ['darkblue','darkcyan','darkgoldenrod','darkgreen','darkgrey','darkkhaki','darkmagenta','darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet']

        # Filter "bad" colors for sensors
        """colors.remove("white")
        colors.remove("black")
        colors.remove("transparent")
        colors.remove("red")
        colors.remove("green")"""

        # shuffle(colors)
        color_index = 0

        if len(self.recordsets) > 0:
            self.sensors += self.dbMan.get_sensors(self.recordsets[0])

        for sensor in self.sensors:
            index = -1
            location_item = self.UI.lstSensors.findItems(sensor.location, Qt.MatchExactly)
            if len(location_item) == 0:
                item = QListWidgetItem(sensor.location)
                item.setFlags(Qt.NoItemFlags)
                self.UI.lstSensors.addItem(item)
            else:
                index = self.UI.lstSensors.indexFromItem(location_item[0]).row()

            # Check if sensor is already there under that location item
            sensor_name = sensor.name + " (" + sensor.hw_name + ")"
            present = False
            if index != -1:
                for i in range(index, self.UI.lstSensors.count()):
                    if self.UI.lstSensors.item(i).text() == sensor_name:
                        present = True
                        break

            if not present:
                item = QListWidgetItem(QIcon(':/OpenIMU/icons/sensor.png'), sensor_name)
                item.setCheckState(Qt.Unchecked)
                item.setForeground(QColor(colors[color_index]))
                self.sensors_colors.append(colors[color_index])
                color_index += 1
                if color_index >= len(colors):
                    color_index = 0

                if index == -1:
                    self.UI.lstSensors.addItem(item)
                else:
                    self.UI.lstSensors.insertItem(index+1,item)

    def update_recordset_infos(self):
        if len(self.recordsets) == 0:
            self.UI.lblTotalValue.setText("Aucune donnée.")
            self.UI.lblDurationValue.setText("Aucune donnée.")
            return

        start_time = self.recordsets[0].start_timestamp
        end_time = self.recordsets[len(self.recordsets)-1].end_timestamp

        # Coverage
        self.UI.lblTotalValue.setText(str(start_time) + " @ " + str(end_time))

        # Duration
        self.UI.lblDurationValue.setText(str(end_time-start_time))

    def get_relative_timeview_pos(self, current_time):
        start_time = self.recordsets[0].start_timestamp
        end_time = self.recordsets[len(self.recordsets) - 1].end_timestamp
        time_span = (end_time - start_time).total_seconds()  # Total number of seconds in recordsets
        return (((current_time - self.recordsets[0].start_timestamp).total_seconds()) / time_span) * self.UI.graphTimeline.width()

    def draw_dates(self):
        if len(self.recordsets) == 0:
            return

        # Computations
        start_time = self.recordsets[0].start_timestamp
        end_time = self.recordsets[len(self.recordsets) - 1].end_timestamp
        time_span = (end_time-start_time).total_seconds() # Total number of seconds in recordsets
        current_time = (datetime(start_time.year,start_time.month,start_time.day,0,0,0) + timedelta(days=1))

        # Drawing tools
        whitePen = QPen(Qt.white)
        blackPen = QPen(Qt.black)
        blackBrush = QBrush(Qt.black)

        # Date background rectangle
        self.timeScene.addRect(0, 0, self.UI.graphTimeline.width(), self.UI.graphTimeline.height() / 4, blackPen, blackBrush);

        # First date
        date_text = self.timeScene.addText(start_time.strftime("%d-%m-%Y"))
        date_text.setPos(0, -5)
        date_text.setDefaultTextColor(Qt.white)
        self.timeScene.addLine(0, 0, 0, self.UI.graphTimeline.height(), whitePen)

        # Date separators
        while current_time <= end_time:
            pos = self.get_relative_timeview_pos(current_time)
            self.timeScene.addLine(pos, 0, pos, self.UI.graphTimeline.height(), whitePen)
            date_text = self.timeScene.addText(current_time.strftime("%d-%m-%Y"))
            date_text.setPos(pos, -5)
            date_text.setDefaultTextColor(Qt.white)
            current_time += timedelta(days=1)

    def draw_recordsets(self):
        greenBrush = QBrush(QColor(212, 247, 192))
        transPen = QPen(Qt.transparent)

        # Empty rectangle (background)
        self.timeScene.addRect(0,0,self.UI.graphTimeline.width(),self.UI.graphTimeline.height(),transPen,QBrush(Qt.red))
        self.timeScene.setBackgroundBrush(QBrush(Qt.red))


        # Recording length
        for record in self.recordsets:
            start_pos = self.get_relative_timeview_pos(record.start_timestamp)
            end_pos =  self.get_relative_timeview_pos(record.end_timestamp)
            span = end_pos - start_pos
            self.timeScene.addRect(start_pos, 0, span, self.UI.graphTimeline.height(), transPen, greenBrush)

    def draw_sensors(self):
        if len(self.sensors) == 0:
            return

        bar_height = (3*(self.UI.graphTimeline.height()/4))/len(self.sensors)
        # for sensor in self.sensors:
        for i in range(0, len(self.sensors)):
            sensor = self.sensors[i]
            sensorBrush = QBrush(QColor(self.sensors_colors[i]))
            # print (sensor.name + " = " + self.sensors_colors[i])
            sensorPen = QPen(Qt.transparent)
            for record in self.recordsets:
                datas = self.dbMan.get_all_sensor_data(sensor=sensor, recordset=record, channel=sensor.channels[0])
                for data in datas:
                    start_pos = self.get_relative_timeview_pos(data.start_timestamp)
                    end_pos = self.get_relative_timeview_pos(data.end_timestamp)
                    span = end_pos - start_pos
                    self.timeScene.addRect(start_pos, i*bar_height+(self.UI.graphTimeline.height()/4), span, bar_height, sensorPen, sensorBrush)


        return


