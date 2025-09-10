# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DataSelectorDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLayout, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
import core_rc

class Ui_DataSelectorDialog(object):
    def setupUi(self, DataSelectorDialog):
        if not DataSelectorDialog.objectName():
            DataSelectorDialog.setObjectName(u"DataSelectorDialog")
        DataSelectorDialog.resize(675, 473)
        self.verticalLayout = QVBoxLayout(DataSelectorDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frameTitle = QFrame(DataSelectorDialog)
        self.frameTitle.setObjectName(u"frameTitle")
        self.horizontalLayout_4 = QHBoxLayout(self.frameTitle)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.lblIcon = QLabel(self.frameTitle)
        self.lblIcon.setObjectName(u"lblIcon")
        self.lblIcon.setMaximumSize(QSize(48, 48))
        self.lblIcon.setPixmap(QPixmap(u":/OpenIMU/icons/newdataset.png"))
        self.lblIcon.setScaledContents(True)

        self.horizontalLayout_4.addWidget(self.lblIcon)

        self.lblInfos = QLabel(self.frameTitle)
        self.lblInfos.setObjectName(u"lblInfos")
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        self.lblInfos.setFont(font)
        self.lblInfos.setAcceptDrops(False)

        self.horizontalLayout_4.addWidget(self.lblInfos)


        self.verticalLayout.addWidget(self.frameTitle)

        self.wdgDataSelector = QWidget(DataSelectorDialog)
        self.wdgDataSelector.setObjectName(u"wdgDataSelector")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wdgDataSelector.sizePolicy().hasHeightForWidth())
        self.wdgDataSelector.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.wdgDataSelector)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.verticalLayout.addWidget(self.wdgDataSelector)

        self.frameFormButtons = QFrame(DataSelectorDialog)
        self.frameFormButtons.setObjectName(u"frameFormButtons")
        self.horizontalLayout_3 = QHBoxLayout(self.frameFormButtons)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalLayout_3.setContentsMargins(-1, -1, 0, -1)
        self.horizontalSpacer = QSpacerItem(40, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.btnOK = QPushButton(self.frameFormButtons)
        self.btnOK.setObjectName(u"btnOK")
        self.btnOK.setMinimumSize(QSize(150, 40))
        self.btnOK.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/OpenIMU/icons/next.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnOK.setIcon(icon)
        self.btnOK.setIconSize(QSize(24, 24))
        self.btnOK.setAutoDefault(False)

        self.horizontalLayout_3.addWidget(self.btnOK)

        self.btnCancel = QPushButton(self.frameFormButtons)
        self.btnCancel.setObjectName(u"btnCancel")
        self.btnCancel.setMinimumSize(QSize(150, 40))
        self.btnCancel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/OpenIMU/icons/undo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnCancel.setIcon(icon1)
        self.btnCancel.setIconSize(QSize(24, 24))
        self.btnCancel.setAutoDefault(False)

        self.horizontalLayout_3.addWidget(self.btnCancel)


        self.verticalLayout.addWidget(self.frameFormButtons)


        self.retranslateUi(DataSelectorDialog)

        QMetaObject.connectSlotsByName(DataSelectorDialog)
    # setupUi

    def retranslateUi(self, DataSelectorDialog):
        DataSelectorDialog.setWindowTitle(QCoreApplication.translate("DataSelectorDialog", u"Data Selector Dialog", None))
        self.lblIcon.setText("")
        self.lblInfos.setText(QCoreApplication.translate("DataSelectorDialog", u"Select data files", None))
        self.btnOK.setText(QCoreApplication.translate("DataSelectorDialog", u"Next", None))
        self.btnCancel.setText(QCoreApplication.translate("DataSelectorDialog", u"Cancel", None))
    # retranslateUi

