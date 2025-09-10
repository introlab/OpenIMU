# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CrashDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTextEdit, QVBoxLayout, QWidget)
import core_rc

class Ui_CrashDialog(object):
    def setupUi(self, CrashDialog):
        if not CrashDialog.objectName():
            CrashDialog.setObjectName(u"CrashDialog")
        CrashDialog.resize(589, 256)
        icon = QIcon()
        icon.addFile(u":/OpenIMU/icons/OpenIMU.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        CrashDialog.setWindowIcon(icon)
        CrashDialog.setStyleSheet(u"QLabel#lblTitle{color: red;}\n"
"QLabel#lblInfos{background-color: white;color: black;}\n"
"\n"
"QDialog{background:qlineargradient(spread:pad, x1:0.483, y1:0, x2:0.511045, y2:1, stop:0 rgb(50, 50, 50), stop:1 rgb(153, 153, 153));border-radius:0px;}\n"
"\n"
"QPushButton:hover,QToolButton:hover{color:black;background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 grey, stop: 0.2  rgb(200,200, 200), stop:1 grey);border: 2px solid rgb(186, 186, 186);}\n"
"QPushButton,QToolButton{color:white; background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 black, stop: 0.2  rgb(200,200, 200), stop:1 black);border: 2px solid rgb(96, 96, 96);}\n"
"QPushButton:!enabled,QToolButton:!enabled{color: rgb(168, 168, 168); background-color: rgba(200,200,200,10%);border: 0px transparent}\n"
"QPushButton:checked,QToolButton:checked{color:black;border: 3px solid green;background-color:darkgreen;}\n"
"QPushButton[checkable=true]:!checked,QToolButton[checkable=true]:!checked{color:red;background-color:rgba(180,0,0,50%);bo"
                        "rder: 2px solid rgb(180,0,0);}\n"
"")
        self.verticalLayout = QVBoxLayout(CrashDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lblTitle = QLabel(CrashDialog)
        self.lblTitle.setObjectName(u"lblTitle")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTitle.sizePolicy().hasHeightForWidth())
        self.lblTitle.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.lblTitle.setFont(font)
        self.lblTitle.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.lblTitle)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.imgCrash = QLabel(CrashDialog)
        self.imgCrash.setObjectName(u"imgCrash")
        self.imgCrash.setMaximumSize(QSize(125, 125))
        self.imgCrash.setPixmap(QPixmap(u":/OpenIMU/icons/bug.png"))
        self.imgCrash.setScaledContents(True)

        self.horizontalLayout.addWidget(self.imgCrash)

        self.tabBug = QTabWidget(CrashDialog)
        self.tabBug.setObjectName(u"tabBug")
        self.tabGeneral = QWidget()
        self.tabGeneral.setObjectName(u"tabGeneral")
        self.horizontalLayout_2 = QHBoxLayout(self.tabGeneral)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lblInfos = QLabel(self.tabGeneral)
        self.lblInfos.setObjectName(u"lblInfos")
        self.lblInfos.setAlignment(Qt.AlignJustify|Qt.AlignTop)
        self.lblInfos.setWordWrap(True)
        self.lblInfos.setMargin(6)

        self.horizontalLayout_2.addWidget(self.lblInfos)

        self.tabBug.addTab(self.tabGeneral, "")
        self.tabTech = QWidget()
        self.tabTech.setObjectName(u"tabTech")
        self.verticalLayout_2 = QVBoxLayout(self.tabTech)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.txtTraceback = QTextEdit(self.tabTech)
        self.txtTraceback.setObjectName(u"txtTraceback")

        self.verticalLayout_2.addWidget(self.txtTraceback)

        self.tabBug.addTab(self.tabTech, "")

        self.horizontalLayout.addWidget(self.tabBug)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.btnOK = QPushButton(CrashDialog)
        self.btnOK.setObjectName(u"btnOK")
        self.btnOK.setMinimumSize(QSize(100, 40))
        self.btnOK.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/OpenIMU/icons/delete.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnOK.setIcon(icon1)
        self.btnOK.setIconSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.btnOK)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(CrashDialog)

        self.tabBug.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(CrashDialog)
    # setupUi

    def retranslateUi(self, CrashDialog):
        CrashDialog.setWindowTitle(QCoreApplication.translate("CrashDialog", u"Oh no...", None))
        self.lblTitle.setText(QCoreApplication.translate("CrashDialog", u"Oops... An error occurred!", None))
        self.imgCrash.setText("")
        self.lblInfos.setText(QCoreApplication.translate("CrashDialog", u"<html><head/><body><p>This software encountered an issue.<br/><br/>You can still continue to work, but<span style=\" font-weight:600;\"> it is possible that some features will not function properly</span>.<br/><br/>If possible, please <span style=\" font-weight:600;\">report the issue to the developpers</span> so it can be fixed. Don't forget to specify the steps you did to have this issue and include the technical report.<br/><br/></p></body></html>", None))
        self.tabBug.setTabText(self.tabBug.indexOf(self.tabGeneral), QCoreApplication.translate("CrashDialog", u"General", None))
        self.tabBug.setTabText(self.tabBug.indexOf(self.tabTech), QCoreApplication.translate("CrashDialog", u"Technical report", None))
        self.btnOK.setText(QCoreApplication.translate("CrashDialog", u"OK", None))
    # retranslateUi

