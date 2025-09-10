# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ProgressDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QLabel, QProgressBar, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
import core_rc

class Ui_ProgressDialog(object):
    def setupUi(self, ProgressDialog):
        if not ProgressDialog.objectName():
            ProgressDialog.setObjectName(u"ProgressDialog")
        ProgressDialog.resize(640, 188)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ProgressDialog.sizePolicy().hasHeightForWidth())
        ProgressDialog.setSizePolicy(sizePolicy)
        ProgressDialog.setStyleSheet(u"QDialog{background-color:rgb(130,130,130);border-style:solid; border-color: black; border-width: 5px;}\n"
"\n"
"QLabel#lblTitle{color:black;}\n"
"QLabel#lblCurrentTaskValue{color:blue;}\n"
"\n"
"QProgressBar#prgTask::chunk {\n"
"    background-color:qlineargradient(spread:reflect, x1:0.5, y1:0, x2:0.5, y2:0.5, stop:0 rgba(0, 0, 127, 255), stop:1 rgba(114, 114, 255, 255));\n"
"    width: 20px;\n"
"}\n"
"QProgressBar#prgTotal::chunk{\n"
"	background-color:qlineargradient(spread:reflect, x1:0.5, y1:0, x2:0.5, y2:0.5, stop:0 rgba(0, 127, 0, 255), stop:1 rgba(114, 255, 114, 255));\n"
"    width: 20px;\n"
"}")
        ProgressDialog.setModal(True)
        self.verticalLayout_2 = QVBoxLayout(ProgressDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.icoWorking = QLabel(ProgressDialog)
        self.icoWorking.setObjectName(u"icoWorking")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.icoWorking.sizePolicy().hasHeightForWidth())
        self.icoWorking.setSizePolicy(sizePolicy1)
        self.icoWorking.setMinimumSize(QSize(30, 30))
        self.icoWorking.setMaximumSize(QSize(30, 30))
        self.icoWorking.setPixmap(QPixmap(u":/OpenIMU/icons/loading.gif"))
        self.icoWorking.setScaledContents(True)

        self.horizontalLayout.addWidget(self.icoWorking)

        self.lblTitle = QLabel(ProgressDialog)
        self.lblTitle.setObjectName(u"lblTitle")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lblTitle.sizePolicy().hasHeightForWidth())
        self.lblTitle.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.lblTitle.setFont(font)
        self.lblTitle.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.lblTitle)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.prgTotal = QProgressBar(ProgressDialog)
        self.prgTotal.setObjectName(u"prgTotal")
        self.prgTotal.setMinimumSize(QSize(0, 26))
        self.prgTotal.setValue(24)
        self.prgTotal.setAlignment(Qt.AlignCenter)
        self.prgTotal.setTextVisible(True)
        self.prgTotal.setInvertedAppearance(False)

        self.verticalLayout_2.addWidget(self.prgTotal)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lblCurrentTask = QLabel(ProgressDialog)
        self.lblCurrentTask.setObjectName(u"lblCurrentTask")
        sizePolicy2.setHeightForWidth(self.lblCurrentTask.sizePolicy().hasHeightForWidth())
        self.lblCurrentTask.setSizePolicy(sizePolicy2)
        font1 = QFont()
        font1.setItalic(True)
        self.lblCurrentTask.setFont(font1)

        self.verticalLayout.addWidget(self.lblCurrentTask)

        self.lblCurrentTaskValue = QLabel(ProgressDialog)
        self.lblCurrentTaskValue.setObjectName(u"lblCurrentTaskValue")
        font2 = QFont()
        font2.setBold(True)
        self.lblCurrentTaskValue.setFont(font2)
        self.lblCurrentTaskValue.setText(u"(Task text)")
        self.lblCurrentTaskValue.setAlignment(Qt.AlignCenter)
        self.lblCurrentTaskValue.setWordWrap(True)

        self.verticalLayout.addWidget(self.lblCurrentTaskValue)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.prgTask = QProgressBar(ProgressDialog)
        self.prgTask.setObjectName(u"prgTask")
        self.prgTask.setMaximumSize(QSize(16777215, 16))
        self.prgTask.setValue(40)
        self.prgTask.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.prgTask)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.lblElapsedValue = QLabel(ProgressDialog)
        self.lblElapsedValue.setObjectName(u"lblElapsedValue")
        self.lblElapsedValue.setFont(font2)
        self.lblElapsedValue.setText(u"00:00:00")

        self.gridLayout.addWidget(self.lblElapsedValue, 0, 1, 1, 1)

        self.lblRemainingValue = QLabel(ProgressDialog)
        self.lblRemainingValue.setObjectName(u"lblRemainingValue")
        self.lblRemainingValue.setFont(font2)

        self.gridLayout.addWidget(self.lblRemainingValue, 0, 4, 1, 1)

        self.lblRemaining = QLabel(ProgressDialog)
        self.lblRemaining.setObjectName(u"lblRemaining")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.lblRemaining.sizePolicy().hasHeightForWidth())
        self.lblRemaining.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.lblRemaining, 0, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.lblElapsed = QLabel(ProgressDialog)
        self.lblElapsed.setObjectName(u"lblElapsed")
        sizePolicy3.setHeightForWidth(self.lblElapsed.sizePolicy().hasHeightForWidth())
        self.lblElapsed.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.lblElapsed, 0, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)


        self.retranslateUi(ProgressDialog)

        QMetaObject.connectSlotsByName(ProgressDialog)
    # setupUi

    def retranslateUi(self, ProgressDialog):
        ProgressDialog.setWindowTitle(QCoreApplication.translate("ProgressDialog", u"Progress Display", None))
        self.icoWorking.setText("")
        self.lblTitle.setText(QCoreApplication.translate("ProgressDialog", u"Work in progress...", None))
        self.lblCurrentTask.setText(QCoreApplication.translate("ProgressDialog", u"Processing:", None))
        self.lblRemainingValue.setText(QCoreApplication.translate("ProgressDialog", u"Unknown", None))
        self.lblRemaining.setText(QCoreApplication.translate("ProgressDialog", u"Remaining time:", None))
        self.lblElapsed.setText(QCoreApplication.translate("ProgressDialog", u"Elapsed time:", None))
    # retranslateUi

