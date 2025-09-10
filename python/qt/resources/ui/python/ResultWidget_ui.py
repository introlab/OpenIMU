# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ResultWidget.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QListView,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)
import core_rc

class Ui_frmResult(object):
    def setupUi(self, frmResult):
        if not frmResult.objectName():
            frmResult.setObjectName(u"frmResult")
        frmResult.resize(876, 536)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frmResult.sizePolicy().hasHeightForWidth())
        frmResult.setSizePolicy(sizePolicy)
        frmResult.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(frmResult)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frameTitle = QFrame(frmResult)
        self.frameTitle.setObjectName(u"frameTitle")
        self.horizontalLayout = QHBoxLayout(self.frameTitle)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lblIcon = QLabel(self.frameTitle)
        self.lblIcon.setObjectName(u"lblIcon")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lblIcon.sizePolicy().hasHeightForWidth())
        self.lblIcon.setSizePolicy(sizePolicy1)
        self.lblIcon.setMaximumSize(QSize(48, 48))
        self.lblIcon.setPixmap(QPixmap(u":/OpenIMU/icons/result.png"))
        self.lblIcon.setScaledContents(True)

        self.horizontalLayout.addWidget(self.lblIcon)

        self.lblNameValue = QLabel(self.frameTitle)
        self.lblNameValue.setObjectName(u"lblNameValue")
        sizePolicy1.setHeightForWidth(self.lblNameValue.sizePolicy().hasHeightForWidth())
        self.lblNameValue.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        self.lblNameValue.setFont(font)

        self.horizontalLayout.addWidget(self.lblNameValue)


        self.verticalLayout.addWidget(self.frameTitle)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(10)
        self.lblTime = QLabel(frmResult)
        self.lblTime.setObjectName(u"lblTime")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lblTime.sizePolicy().hasHeightForWidth())
        self.lblTime.setSizePolicy(sizePolicy2)
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.lblTime.setFont(font1)

        self.gridLayout.addWidget(self.lblTime, 1, 0, 1, 1)

        self.lblTimeValue = QLabel(frmResult)
        self.lblTimeValue.setObjectName(u"lblTimeValue")
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        self.lblTimeValue.setFont(font2)
        self.lblTimeValue.setText(u"(Date)")

        self.gridLayout.addWidget(self.lblTimeValue, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.tabResults = QTabWidget(frmResult)
        self.tabResults.setObjectName(u"tabResults")
        self.tabResults.setIconSize(QSize(24, 24))
        self.tabReport = QWidget()
        self.tabReport.setObjectName(u"tabReport")
        self.verticalLayout_2 = QVBoxLayout(self.tabReport)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, -1, 0)
        self.centralWidget = QWidget(self.tabReport)
        self.centralWidget.setObjectName(u"centralWidget")
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.centralWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")

        self.verticalLayout_2.addWidget(self.centralWidget)

        icon = QIcon()
        icon.addFile(u":/OpenIMU/icons/graph.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabResults.addTab(self.tabReport, icon, "")
        self.tabData = QWidget()
        self.tabData.setObjectName(u"tabData")
        self.verticalLayout_4 = QVBoxLayout(self.tabData)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.lblParams = QLabel(self.tabData)
        self.lblParams.setObjectName(u"lblParams")
        font3 = QFont()
        font3.setBold(True)
        self.lblParams.setFont(font3)

        self.verticalLayout_4.addWidget(self.lblParams)

        self.tableParams = QTableWidget(self.tabData)
        if (self.tableParams.rowCount() < 1):
            self.tableParams.setRowCount(1)
        self.tableParams.setObjectName(u"tableParams")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tableParams.sizePolicy().hasHeightForWidth())
        self.tableParams.setSizePolicy(sizePolicy3)
        self.tableParams.setMinimumSize(QSize(0, 0))
        self.tableParams.setMaximumSize(QSize(16777215, 70))
        self.tableParams.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableParams.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableParams.setRowCount(1)
        self.tableParams.horizontalHeader().setVisible(True)
        self.tableParams.verticalHeader().setVisible(False)

        self.verticalLayout_4.addWidget(self.tableParams)

        self.lblData = QLabel(self.tabData)
        self.lblData.setObjectName(u"lblData")
        self.lblData.setFont(font3)

        self.verticalLayout_4.addWidget(self.lblData)

        self.tableData = QTableWidget(self.tabData)
        self.tableData.setObjectName(u"tableData")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.tableData.sizePolicy().hasHeightForWidth())
        self.tableData.setSizePolicy(sizePolicy4)
        self.tableData.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableData.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableData.setSortingEnabled(True)
        self.tableData.horizontalHeader().setCascadingSectionResizes(False)
        self.tableData.horizontalHeader().setProperty(u"showSortIndicator", True)
        self.tableData.horizontalHeader().setStretchLastSection(False)
        self.tableData.verticalHeader().setProperty(u"showSortIndicator", False)
        self.tableData.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_4.addWidget(self.tableData)

        self.btnCopyData = QPushButton(self.tabData)
        self.btnCopyData.setObjectName(u"btnCopyData")
        self.btnCopyData.setMinimumSize(QSize(0, 40))
        self.btnCopyData.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/OpenIMU/icons/recordset.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnCopyData.setIcon(icon1)
        self.btnCopyData.setIconSize(QSize(24, 24))

        self.verticalLayout_4.addWidget(self.btnCopyData)

        icon2 = QIcon()
        icon2.addFile(u":/OpenIMU/icons/compact.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabResults.addTab(self.tabData, icon2, "")
        self.tabSources = QWidget()
        self.tabSources.setObjectName(u"tabSources")
        self.horizontalLayout_2 = QHBoxLayout(self.tabSources)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lstSources = QListWidget(self.tabSources)
        self.lstSources.setObjectName(u"lstSources")
        sizePolicy4.setHeightForWidth(self.lstSources.sizePolicy().hasHeightForWidth())
        self.lstSources.setSizePolicy(sizePolicy4)
        self.lstSources.setMaximumSize(QSize(16777215, 16777215))
        font4 = QFont()
        font4.setPointSize(12)
        self.lstSources.setFont(font4)
        self.lstSources.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.lstSources.setProperty(u"showDropIndicator", False)
        self.lstSources.setIconSize(QSize(24, 24))
        self.lstSources.setLayoutMode(QListView.SinglePass)
        self.lstSources.setViewMode(QListView.ListMode)
        self.lstSources.setWordWrap(True)

        self.horizontalLayout_2.addWidget(self.lstSources)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.tabResults.addTab(self.tabSources, icon1, "")

        self.verticalLayout.addWidget(self.tabResults)


        self.retranslateUi(frmResult)

        self.tabResults.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(frmResult)
    # setupUi

    def retranslateUi(self, frmResult):
        frmResult.setWindowTitle(QCoreApplication.translate("frmResult", u"Results display", None))
        self.lblIcon.setText("")
        self.lblNameValue.setText(QCoreApplication.translate("frmResult", u"Results display", None))
        self.lblTime.setText(QCoreApplication.translate("frmResult", u"Processing date:", None))
        self.tabResults.setTabText(self.tabResults.indexOf(self.tabReport), QCoreApplication.translate("frmResult", u"Results", None))
        self.lblParams.setText(QCoreApplication.translate("frmResult", u"Settings", None))
        self.lblData.setText(QCoreApplication.translate("frmResult", u"Data", None))
        self.btnCopyData.setText(QCoreApplication.translate("frmResult", u"Copy data to clipboard", None))
        self.tabResults.setTabText(self.tabResults.indexOf(self.tabData), QCoreApplication.translate("frmResult", u"Data", None))
        self.tabResults.setTabText(self.tabResults.indexOf(self.tabSources), QCoreApplication.translate("frmResult", u"Data Sources", None))
    # retranslateUi

