# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TableDataViewWidget.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)
import core_rc

class Ui_tableDataViewWidget(object):
    def setupUi(self, tableDataViewWidget):
        if not tableDataViewWidget.objectName():
            tableDataViewWidget.setObjectName(u"tableDataViewWidget")
        tableDataViewWidget.resize(400, 300)
        icon = QIcon()
        icon.addFile(u":/OpenIMU/icons/OpenIMU.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        tableDataViewWidget.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(tableDataViewWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frameChannels = QFrame(tableDataViewWidget)
        self.frameChannels.setObjectName(u"frameChannels")
        self.horizontalLayout = QHBoxLayout(self.frameChannels)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lblChannel = QLabel(self.frameChannels)
        self.lblChannel.setObjectName(u"lblChannel")

        self.horizontalLayout.addWidget(self.lblChannel)

        self.cmbChannels = QComboBox(self.frameChannels)
        self.cmbChannels.setObjectName(u"cmbChannels")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbChannels.sizePolicy().hasHeightForWidth())
        self.cmbChannels.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.cmbChannels)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.frameChannels)

        self.tableData = QTableWidget(tableDataViewWidget)
        self.tableData.setObjectName(u"tableData")
        self.tableData.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableData.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout.addWidget(self.tableData)


        self.retranslateUi(tableDataViewWidget)

        QMetaObject.connectSlotsByName(tableDataViewWidget)
    # setupUi

    def retranslateUi(self, tableDataViewWidget):
        tableDataViewWidget.setWindowTitle(QCoreApplication.translate("tableDataViewWidget", u"Data view", None))
        self.lblChannel.setText(QCoreApplication.translate("tableDataViewWidget", u"Channel:", None))
    # retranslateUi

