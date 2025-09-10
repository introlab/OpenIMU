# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DataInfosWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
import core_rc

class Ui_DataInfosWidget(object):
    def setupUi(self, DataInfosWidget):
        if not DataInfosWidget.objectName():
            DataInfosWidget.setObjectName(u"DataInfosWidget")
        DataInfosWidget.resize(400, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DataInfosWidget.sizePolicy().hasHeightForWidth())
        DataInfosWidget.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/OpenIMU/icons/OpenIMU.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        DataInfosWidget.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(DataInfosWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frameTitle = QFrame(DataInfosWidget)
        self.frameTitle.setObjectName(u"frameTitle")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frameTitle.sizePolicy().hasHeightForWidth())
        self.frameTitle.setSizePolicy(sizePolicy1)
        self.horizontalLayout_2 = QHBoxLayout(self.frameTitle)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lblIcon = QLabel(self.frameTitle)
        self.lblIcon.setObjectName(u"lblIcon")
        self.lblIcon.setMaximumSize(QSize(48, 48))
        self.lblIcon.setPixmap(QPixmap(u":/OpenIMU/icons/OpenIMU.png"))
        self.lblIcon.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.lblIcon)

        self.lblInfos = QLabel(self.frameTitle)
        self.lblInfos.setObjectName(u"lblInfos")
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        self.lblInfos.setFont(font)

        self.horizontalLayout_2.addWidget(self.lblInfos)


        self.verticalLayout.addWidget(self.frameTitle)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lblSensorName = QLabel(DataInfosWidget)
        self.lblSensorName.setObjectName(u"lblSensorName")
        sizePolicy.setHeightForWidth(self.lblSensorName.sizePolicy().hasHeightForWidth())
        self.lblSensorName.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setPointSize(10)
        self.lblSensorName.setFont(font1)
        self.lblSensorName.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lblSensorName)

        self.lblSensorNameValue = QLabel(DataInfosWidget)
        self.lblSensorNameValue.setObjectName(u"lblSensorNameValue")
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        self.lblSensorNameValue.setFont(font2)
        self.lblSensorNameValue.setText(u"(Sensor name)")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lblSensorNameValue)

        self.lblHW = QLabel(DataInfosWidget)
        self.lblHW.setObjectName(u"lblHW")
        sizePolicy.setHeightForWidth(self.lblHW.sizePolicy().hasHeightForWidth())
        self.lblHW.setSizePolicy(sizePolicy)
        self.lblHW.setFont(font1)
        self.lblHW.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lblHW)

        self.lblHWValue = QLabel(DataInfosWidget)
        self.lblHWValue.setObjectName(u"lblHWValue")
        self.lblHWValue.setFont(font2)
        self.lblHWValue.setText(u"(Device name)")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lblHWValue)

        self.lblHWID = QLabel(DataInfosWidget)
        self.lblHWID.setObjectName(u"lblHWID")
        sizePolicy.setHeightForWidth(self.lblHWID.sizePolicy().hasHeightForWidth())
        self.lblHWID.setSizePolicy(sizePolicy)
        self.lblHWID.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lblHWID)

        self.lblHWIDValue = QLabel(DataInfosWidget)
        self.lblHWIDValue.setObjectName(u"lblHWIDValue")
        font3 = QFont()
        font3.setBold(True)
        self.lblHWIDValue.setFont(font3)
        self.lblHWIDValue.setText(u"Hardware ID)")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lblHWIDValue)

        self.lblLocation = QLabel(DataInfosWidget)
        self.lblLocation.setObjectName(u"lblLocation")
        sizePolicy.setHeightForWidth(self.lblLocation.sizePolicy().hasHeightForWidth())
        self.lblLocation.setSizePolicy(sizePolicy)
        self.lblLocation.setFont(font1)
        self.lblLocation.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.lblLocation)

        self.lblLocationValue = QLabel(DataInfosWidget)
        self.lblLocationValue.setObjectName(u"lblLocationValue")
        self.lblLocationValue.setFont(font2)
        self.lblLocationValue.setText(u"(Position)")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.lblLocationValue)

        self.lblSamplingRate = QLabel(DataInfosWidget)
        self.lblSamplingRate.setObjectName(u"lblSamplingRate")
        sizePolicy.setHeightForWidth(self.lblSamplingRate.sizePolicy().hasHeightForWidth())
        self.lblSamplingRate.setSizePolicy(sizePolicy)
        self.lblSamplingRate.setFont(font1)
        self.lblSamplingRate.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.lblSamplingRate)

        self.lblSamplingRateValue = QLabel(DataInfosWidget)
        self.lblSamplingRateValue.setObjectName(u"lblSamplingRateValue")
        self.lblSamplingRateValue.setFont(font2)
        self.lblSamplingRateValue.setText(u"(Sampling rate)")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.lblSamplingRateValue)

        self.lblSamples = QLabel(DataInfosWidget)
        self.lblSamples.setObjectName(u"lblSamples")
        self.lblSamples.setFont(font1)

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.lblSamples)

        self.lblSamplesValue = QLabel(DataInfosWidget)
        self.lblSamplesValue.setObjectName(u"lblSamplesValue")
        self.lblSamplesValue.setFont(font2)
        self.lblSamplesValue.setText(u"(Samples num)")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.lblSamplesValue)

        self.lblChannels = QLabel(DataInfosWidget)
        self.lblChannels.setObjectName(u"lblChannels")
        self.lblChannels.setFont(font1)

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.lblChannels)

        self.lblChannelsValue = QLabel(DataInfosWidget)
        self.lblChannelsValue.setObjectName(u"lblChannelsValue")
        self.lblChannelsValue.setFont(font2)
        self.lblChannelsValue.setText(u"(Channels num)")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.lblChannelsValue)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btnOK = QPushButton(DataInfosWidget)
        self.btnOK.setObjectName(u"btnOK")
        self.btnOK.setMinimumSize(QSize(100, 40))
        self.btnOK.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/OpenIMU/icons/ok.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnOK.setIcon(icon1)
        self.btnOK.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.btnOK)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(DataInfosWidget)

        QMetaObject.connectSlotsByName(DataInfosWidget)
    # setupUi

    def retranslateUi(self, DataInfosWidget):
        DataInfosWidget.setWindowTitle(QCoreApplication.translate("DataInfosWidget", u"Data information", None))
        self.lblIcon.setText("")
        self.lblInfos.setText(QCoreApplication.translate("DataInfosWidget", u"Data information", None))
        self.lblSensorName.setText(QCoreApplication.translate("DataInfosWidget", u"Sensor", None))
        self.lblHW.setText(QCoreApplication.translate("DataInfosWidget", u"Hardware", None))
        self.lblHWID.setText(QCoreApplication.translate("DataInfosWidget", u"Hardware ID", None))
        self.lblLocation.setText(QCoreApplication.translate("DataInfosWidget", u"Position", None))
        self.lblSamplingRate.setText(QCoreApplication.translate("DataInfosWidget", u"Sampling rate", None))
        self.lblSamples.setText(QCoreApplication.translate("DataInfosWidget", u"Samples number", None))
        self.lblChannels.setText(QCoreApplication.translate("DataInfosWidget", u"Channels number", None))
        self.btnOK.setText(QCoreApplication.translate("DataInfosWidget", u"OK", None))
    # retranslateUi

