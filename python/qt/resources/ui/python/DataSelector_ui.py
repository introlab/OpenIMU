# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DataSelector.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QLabel, QSizePolicy, QSpacerItem, QToolButton,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)
import core_rc

class Ui_DataSelector(object):
    def setupUi(self, DataSelector):
        if not DataSelector.objectName():
            DataSelector.setObjectName(u"DataSelector")
        DataSelector.resize(657, 420)
        self.verticalLayout = QVBoxLayout(DataSelector)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lblOnlyOneParticipant = QLabel(DataSelector)
        self.lblOnlyOneParticipant.setObjectName(u"lblOnlyOneParticipant")
        font = QFont()
        font.setPointSize(11)
        self.lblOnlyOneParticipant.setFont(font)
        self.lblOnlyOneParticipant.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.lblOnlyOneParticipant)

        self.treeData = QTreeWidget(DataSelector)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeData.setHeaderItem(__qtreewidgetitem)
        self.treeData.setObjectName(u"treeData")
        self.treeData.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeData.setSelectionMode(QAbstractItemView.NoSelection)
        self.treeData.setIconSize(QSize(20, 20))
        self.treeData.header().setVisible(False)

        self.verticalLayout.addWidget(self.treeData)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btnCheckAll = QToolButton(DataSelector)
        self.btnCheckAll.setObjectName(u"btnCheckAll")
        self.btnCheckAll.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/OpenIMU/controls/check2_on.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnCheckAll.setIcon(icon)
        self.btnCheckAll.setIconSize(QSize(24, 24))
        self.btnCheckAll.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout.addWidget(self.btnCheckAll)

        self.btnUncheckAll = QToolButton(DataSelector)
        self.btnUncheckAll.setObjectName(u"btnUncheckAll")
        self.btnUncheckAll.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/OpenIMU/controls/check2_off.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnUncheckAll.setIcon(icon1)
        self.btnUncheckAll.setIconSize(QSize(24, 24))
        self.btnUncheckAll.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout.addWidget(self.btnUncheckAll)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.btnExpandAll = QToolButton(DataSelector)
        self.btnExpandAll.setObjectName(u"btnExpandAll")
        self.btnExpandAll.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/OpenIMU/icons/tree.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnExpandAll.setIcon(icon2)
        self.btnExpandAll.setIconSize(QSize(24, 24))
        self.btnExpandAll.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout.addWidget(self.btnExpandAll)

        self.btnCollapseAll = QToolButton(DataSelector)
        self.btnCollapseAll.setObjectName(u"btnCollapseAll")
        self.btnCollapseAll.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/OpenIMU/icons/tile_horizontal.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnCollapseAll.setIcon(icon3)
        self.btnCollapseAll.setIconSize(QSize(24, 24))
        self.btnCollapseAll.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout.addWidget(self.btnCollapseAll)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(DataSelector)

        QMetaObject.connectSlotsByName(DataSelector)
    # setupUi

    def retranslateUi(self, DataSelector):
        DataSelector.setWindowTitle(QCoreApplication.translate("DataSelector", u"Data Selector", None))
        self.lblOnlyOneParticipant.setText(QCoreApplication.translate("DataSelector", u"Only one participant can be selected", None))
        self.btnCheckAll.setText(QCoreApplication.translate("DataSelector", u"Select all", None))
        self.btnUncheckAll.setText(QCoreApplication.translate("DataSelector", u"Deselect all", None))
        self.btnExpandAll.setText(QCoreApplication.translate("DataSelector", u"Expand all", None))
        self.btnCollapseAll.setText(QCoreApplication.translate("DataSelector", u"Collapse all", None))
    # retranslateUi

