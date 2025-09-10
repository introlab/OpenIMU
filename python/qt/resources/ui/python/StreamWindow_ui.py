# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'StreamWindow.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractSpinBox, QApplication, QCheckBox,
    QDialog, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QTableWidget, QTableWidgetItem,
    QTextEdit, QToolButton, QVBoxLayout, QWidget)
import core_rc

class Ui_StreamWindow(object):
    def setupUi(self, StreamWindow):
        if not StreamWindow.objectName():
            StreamWindow.setObjectName(u"StreamWindow")
        StreamWindow.resize(807, 553)
        StreamWindow.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(StreamWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frameTitle = QFrame(StreamWindow)
        self.frameTitle.setObjectName(u"frameTitle")
        self.horizontalLayout_9 = QHBoxLayout(self.frameTitle)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.lblIcon = QLabel(self.frameTitle)
        self.lblIcon.setObjectName(u"lblIcon")
        self.lblIcon.setMaximumSize(QSize(48, 48))
        self.lblIcon.setPixmap(QPixmap(u":/OpenIMU/icons/transfer.png"))
        self.lblIcon.setScaledContents(True)

        self.horizontalLayout_9.addWidget(self.lblIcon)

        self.lblTitle = QLabel(self.frameTitle)
        self.lblTitle.setObjectName(u"lblTitle")
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        self.lblTitle.setFont(font)
        self.lblTitle.setAcceptDrops(False)

        self.horizontalLayout_9.addWidget(self.lblTitle)


        self.verticalLayout.addWidget(self.frameTitle)

        self.tabStreamers = QTabWidget(StreamWindow)
        self.tabStreamers.setObjectName(u"tabStreamers")
        self.tabStreamers.setIconSize(QSize(24, 24))
        self.tabAppleWatch = QWidget()
        self.tabAppleWatch.setObjectName(u"tabAppleWatch")
        self.verticalLayout_6 = QVBoxLayout(self.tabAppleWatch)
        self.verticalLayout_6.setSpacing(9)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frameInfos = QFrame(self.tabAppleWatch)
        self.frameInfos.setObjectName(u"frameInfos")
        self.frameInfos.setEnabled(True)
        self.frameInfos.setFrameShape(QFrame.Panel)
        self.frameInfos.setFrameShadow(QFrame.Plain)
        self.gridLayout = QGridLayout(self.frameInfos)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.lblIP = QLabel(self.frameInfos)
        self.lblIP.setObjectName(u"lblIP")
        self.lblIP.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblIP.sizePolicy().hasHeightForWidth())
        self.lblIP.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setBold(False)
        font1.setStyleStrategy(QFont.PreferDefault)
        self.lblIP.setFont(font1)
        self.lblIP.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblIP, 0, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.txtDataPath = QLineEdit(self.frameInfos)
        self.txtDataPath.setObjectName(u"txtDataPath")
        self.txtDataPath.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_4.addWidget(self.txtDataPath)

        self.btnBrowse = QPushButton(self.frameInfos)
        self.btnBrowse.setObjectName(u"btnBrowse")
        self.btnBrowse.setMinimumSize(QSize(100, 30))
        self.btnBrowse.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/OpenIMU/icons/browse.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnBrowse.setIcon(icon)
        self.btnBrowse.setIconSize(QSize(20, 20))

        self.horizontalLayout_4.addWidget(self.btnBrowse)


        self.gridLayout.addLayout(self.horizontalLayout_4, 2, 1, 1, 1)

        self.lblIPValue = QLabel(self.frameInfos)
        self.lblIPValue.setObjectName(u"lblIPValue")
        self.lblIPValue.setEnabled(False)
        self.lblIPValue.setMinimumSize(QSize(0, 25))
        font2 = QFont()
        font2.setBold(True)
        font2.setStyleStrategy(QFont.NoAntialias)
        self.lblIPValue.setFont(font2)
        self.lblIPValue.setText(u"0.0.0.0")
        self.lblIPValue.setMargin(0)

        self.gridLayout.addWidget(self.lblIPValue, 0, 1, 1, 1)

        self.lblDataPath = QLabel(self.frameInfos)
        self.lblDataPath.setObjectName(u"lblDataPath")
        self.lblDataPath.setFont(font1)

        self.gridLayout.addWidget(self.lblDataPath, 2, 0, 1, 1)

        self.chkDeleteFiles = QCheckBox(self.frameInfos)
        self.chkDeleteFiles.setObjectName(u"chkDeleteFiles")
        self.chkDeleteFiles.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout.addWidget(self.chkDeleteFiles, 3, 1, 1, 1)

        self.lblPort = QLabel(self.frameInfos)
        self.lblPort.setObjectName(u"lblPort")
        font3 = QFont()
        font3.setBold(False)
        self.lblPort.setFont(font3)
        self.lblPort.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblPort, 0, 2, 1, 1)

        self.spinPort = QSpinBox(self.frameInfos)
        self.spinPort.setObjectName(u"spinPort")
        self.spinPort.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.spinPort.sizePolicy().hasHeightForWidth())
        self.spinPort.setSizePolicy(sizePolicy1)
        self.spinPort.setMinimumSize(QSize(0, 25))
        font4 = QFont()
        font4.setBold(True)
        font4.setStyleStrategy(QFont.PreferDefault)
        self.spinPort.setFont(font4)
        self.spinPort.setMinimum(1024)
        self.spinPort.setMaximum(65534)
        self.spinPort.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.spinPort.setValue(8118)

        self.gridLayout.addWidget(self.spinPort, 0, 4, 1, 1)


        self.horizontalLayout_2.addWidget(self.frameInfos)

        self.btnEdit = QToolButton(self.tabAppleWatch)
        self.btnEdit.setObjectName(u"btnEdit")
        self.btnEdit.setMinimumSize(QSize(32, 32))
        self.btnEdit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/OpenIMU/icons/save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnEdit.setIcon(icon1)
        self.btnEdit.setIconSize(QSize(36, 36))
        self.btnEdit.setCheckable(False)
        self.btnEdit.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.btnEdit)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.frameEdit = QFrame(self.tabAppleWatch)
        self.frameEdit.setObjectName(u"frameEdit")
        sizePolicy.setHeightForWidth(self.frameEdit.sizePolicy().hasHeightForWidth())
        self.frameEdit.setSizePolicy(sizePolicy)
        self.frameEdit.setFrameShape(QFrame.StyledPanel)
        self.frameEdit.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frameEdit)
        self.horizontalLayout_8.setSpacing(6)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.btnSave = QPushButton(self.frameEdit)
        self.btnSave.setObjectName(u"btnSave")
        self.btnSave.setEnabled(True)
        self.btnSave.setMinimumSize(QSize(100, 35))
        self.btnSave.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/OpenIMU/icons/ok.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnSave.setIcon(icon2)
        self.btnSave.setIconSize(QSize(20, 20))

        self.horizontalLayout_8.addWidget(self.btnSave)

        self.btnCancel = QPushButton(self.frameEdit)
        self.btnCancel.setObjectName(u"btnCancel")
        self.btnCancel.setEnabled(True)
        self.btnCancel.setMinimumSize(QSize(100, 35))
        self.btnCancel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/OpenIMU/icons/undo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnCancel.setIcon(icon3)
        self.btnCancel.setIconSize(QSize(24, 24))

        self.horizontalLayout_8.addWidget(self.btnCancel)


        self.verticalLayout_6.addWidget(self.frameEdit)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label = QLabel(self.tabAppleWatch)
        self.label.setObjectName(u"label")
        font5 = QFont()
        font5.setBold(True)
        self.label.setFont(font5)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label)

        self.lstDevices = QListWidget(self.tabAppleWatch)
        self.lstDevices.setObjectName(u"lstDevices")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lstDevices.sizePolicy().hasHeightForWidth())
        self.lstDevices.setSizePolicy(sizePolicy2)
        self.lstDevices.setMaximumSize(QSize(150, 16777215))
        self.lstDevices.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.lstDevices.setSelectionMode(QAbstractItemView.NoSelection)
        self.lstDevices.setIconSize(QSize(30, 30))
        self.lstDevices.setWordWrap(True)

        self.verticalLayout_5.addWidget(self.lstDevices)


        self.horizontalLayout_3.addLayout(self.verticalLayout_5)

        self.tabInfos = QTabWidget(self.tabAppleWatch)
        self.tabInfos.setObjectName(u"tabInfos")
        self.tabFiles = QWidget()
        self.tabFiles.setObjectName(u"tabFiles")
        self.verticalLayout_3 = QVBoxLayout(self.tabFiles)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.tableFiles = QTableWidget(self.tabFiles)
        if (self.tableFiles.columnCount() < 3):
            self.tableFiles.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableFiles.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableFiles.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableFiles.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableFiles.setObjectName(u"tableFiles")
        self.tableFiles.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableFiles.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableFiles.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableFiles.setWordWrap(False)
        self.tableFiles.setCornerButtonEnabled(False)
        self.tableFiles.setRowCount(0)
        self.tableFiles.horizontalHeader().setDefaultSectionSize(125)
        self.tableFiles.horizontalHeader().setStretchLastSection(True)
        self.tableFiles.verticalHeader().setVisible(False)

        self.verticalLayout_3.addWidget(self.tableFiles)

        icon4 = QIcon()
        icon4.addFile(u":/OpenIMU/icons/transfer.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabInfos.addTab(self.tabFiles, icon4, "")
        self.tabReceived = QWidget()
        self.tabReceived.setObjectName(u"tabReceived")
        self.horizontalLayout_6 = QHBoxLayout(self.tabReceived)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(2, 2, 2, 2)
        self.tableReceived = QTableWidget(self.tabReceived)
        if (self.tableReceived.columnCount() < 3):
            self.tableReceived.setColumnCount(3)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableReceived.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableReceived.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableReceived.setHorizontalHeaderItem(2, __qtablewidgetitem5)
        self.tableReceived.setObjectName(u"tableReceived")
        self.tableReceived.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableReceived.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableReceived.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableReceived.setSortingEnabled(True)
        self.tableReceived.setWordWrap(False)
        self.tableReceived.horizontalHeader().setStretchLastSection(True)

        self.horizontalLayout_6.addWidget(self.tableReceived)

        self.tabInfos.addTab(self.tabReceived, icon2, "")
        self.tabErrors = QWidget()
        self.tabErrors.setObjectName(u"tabErrors")
        self.horizontalLayout_7 = QHBoxLayout(self.tabErrors)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(2, 2, 2, 2)
        self.tableErrors = QTableWidget(self.tabErrors)
        if (self.tableErrors.columnCount() < 2):
            self.tableErrors.setColumnCount(2)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableErrors.setHorizontalHeaderItem(0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableErrors.setHorizontalHeaderItem(1, __qtablewidgetitem7)
        self.tableErrors.setObjectName(u"tableErrors")
        self.tableErrors.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableErrors.setWordWrap(False)
        self.tableErrors.horizontalHeader().setDefaultSectionSize(250)
        self.tableErrors.horizontalHeader().setStretchLastSection(True)

        self.horizontalLayout_7.addWidget(self.tableErrors)

        icon5 = QIcon()
        icon5.addFile(u":/OpenIMU/icons/delete.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabInfos.addTab(self.tabErrors, icon5, "")
        self.tabLog = QWidget()
        self.tabLog.setObjectName(u"tabLog")
        self.verticalLayout_4 = QVBoxLayout(self.tabLog)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.txtLog = QTextEdit(self.tabLog)
        self.txtLog.setObjectName(u"txtLog")
        self.txtLog.setEnabled(True)
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.txtLog.sizePolicy().hasHeightForWidth())
        self.txtLog.setSizePolicy(sizePolicy3)
        self.txtLog.setReadOnly(True)

        self.verticalLayout_4.addWidget(self.txtLog)

        icon6 = QIcon()
        icon6.addFile(u":/OpenIMU/icons/log.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabInfos.addTab(self.tabLog, icon6, "")

        self.horizontalLayout_3.addWidget(self.tabInfos)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btnClose = QPushButton(self.tabAppleWatch)
        self.btnClose.setObjectName(u"btnClose")
        self.btnClose.setMinimumSize(QSize(150, 40))
        self.btnClose.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon7 = QIcon()
        icon7.addFile(u":/OpenIMU/icons/import.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnClose.setIcon(icon7)
        self.btnClose.setIconSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.btnClose)


        self.verticalLayout_6.addLayout(self.horizontalLayout)

        icon8 = QIcon()
        icon8.addFile(u":/OpenIMU/icons/sensor_watch.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabStreamers.addTab(self.tabAppleWatch, icon8, "")

        self.verticalLayout.addWidget(self.tabStreamers)


        self.retranslateUi(StreamWindow)

        self.tabStreamers.setCurrentIndex(0)
        self.tabInfos.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(StreamWindow)
    # setupUi

    def retranslateUi(self, StreamWindow):
        StreamWindow.setWindowTitle(QCoreApplication.translate("StreamWindow", u"Data transfer and import from a device", None))
        self.lblIcon.setText("")
        self.lblTitle.setText(QCoreApplication.translate("StreamWindow", u"Transfer data from devices", None))
        self.lblIP.setText(QCoreApplication.translate("StreamWindow", u"Server address:", None))
        self.btnBrowse.setText(QCoreApplication.translate("StreamWindow", u"Browse...", None))
        self.lblDataPath.setText(QCoreApplication.translate("StreamWindow", u"Data save folder:", None))
        self.chkDeleteFiles.setText(QCoreApplication.translate("StreamWindow", u"Delete raw data after transfer", None))
        self.lblPort.setText(QCoreApplication.translate("StreamWindow", u"Port", None))
#if QT_CONFIG(tooltip)
        self.btnEdit.setToolTip(QCoreApplication.translate("StreamWindow", u"Edit settings", None))
#endif // QT_CONFIG(tooltip)
        self.btnEdit.setText(QCoreApplication.translate("StreamWindow", u"Edit", None))
        self.btnSave.setText(QCoreApplication.translate("StreamWindow", u"Save", None))
        self.btnCancel.setText(QCoreApplication.translate("StreamWindow", u"Undo", None))
        self.label.setText(QCoreApplication.translate("StreamWindow", u"Active devices", None))
        ___qtablewidgetitem = self.tableFiles.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("StreamWindow", u"Progress", None));
        ___qtablewidgetitem1 = self.tableFiles.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("StreamWindow", u"Size", None));
        ___qtablewidgetitem2 = self.tableFiles.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("StreamWindow", u"Filename", None));
        self.tabInfos.setTabText(self.tabInfos.indexOf(self.tabFiles), QCoreApplication.translate("StreamWindow", u"In progress (0)", None))
        ___qtablewidgetitem3 = self.tableReceived.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("StreamWindow", u"Device", None));
        ___qtablewidgetitem4 = self.tableReceived.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("StreamWindow", u"Size", None));
        ___qtablewidgetitem5 = self.tableReceived.horizontalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("StreamWindow", u"Filename", None));
        self.tabInfos.setTabText(self.tabInfos.indexOf(self.tabReceived), QCoreApplication.translate("StreamWindow", u"Completed (0)", None))
        ___qtablewidgetitem6 = self.tableErrors.horizontalHeaderItem(0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("StreamWindow", u"Filename", None));
        ___qtablewidgetitem7 = self.tableErrors.horizontalHeaderItem(1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("StreamWindow", u"Error", None));
        self.tabInfos.setTabText(self.tabInfos.indexOf(self.tabErrors), QCoreApplication.translate("StreamWindow", u"Errors (0)", None))
        self.tabInfos.setTabText(self.tabInfos.indexOf(self.tabLog), QCoreApplication.translate("StreamWindow", u"Transfer log", None))
        self.btnClose.setText(QCoreApplication.translate("StreamWindow", u"Close and import data", None))
        self.tabStreamers.setTabText(self.tabStreamers.indexOf(self.tabAppleWatch), QCoreApplication.translate("StreamWindow", u"SensorLogger (Apple Watch)", None))
    # retranslateUi

