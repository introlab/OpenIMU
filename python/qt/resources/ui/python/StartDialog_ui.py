# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'StartDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
import core_rc

class Ui_StartDialog(object):
    def setupUi(self, StartDialog):
        if not StartDialog.objectName():
            StartDialog.setObjectName(u"StartDialog")
        StartDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        StartDialog.resize(782, 452)
        StartDialog.setWindowTitle(u"OpenIMU")
        icon = QIcon()
        icon.addFile(u":/OpenIMU/icons/OpenIMU.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        StartDialog.setWindowIcon(icon)
        StartDialog.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(StartDialog)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)

        self.cmbLanguage = QComboBox(StartDialog)
        self.cmbLanguage.addItem(u"English")
        self.cmbLanguage.addItem(u"Fran\u00e7ais")
        self.cmbLanguage.setObjectName(u"cmbLanguage")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbLanguage.sizePolicy().hasHeightForWidth())
        self.cmbLanguage.setSizePolicy(sizePolicy)
        self.cmbLanguage.setMinimumSize(QSize(100, 0))
        self.cmbLanguage.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

        self.horizontalLayout_5.addWidget(self.cmbLanguage, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lblLogo = QLabel(StartDialog)
        self.lblLogo.setObjectName(u"lblLogo")
        self.lblLogo.setMaximumSize(QSize(280, 180))
        self.lblLogo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.lblLogo.setPixmap(QPixmap(u":/OpenIMU/LogoOpenIMU.png"))
        self.lblLogo.setScaledContents(True)

        self.horizontalLayout.addWidget(self.lblLogo)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(10, 20, 10, 10)
        self.btnNew = QPushButton(StartDialog)
        self.btnNew.setObjectName(u"btnNew")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btnNew.sizePolicy().hasHeightForWidth())
        self.btnNew.setSizePolicy(sizePolicy1)
        self.btnNew.setMinimumSize(QSize(200, 100))
        self.btnNew.setMaximumSize(QSize(16777215, 150))
        self.btnNew.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnNew.setAutoFillBackground(False)
        icon1 = QIcon()
        icon1.addFile(u":/OpenIMU/icons/database_new.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnNew.setIcon(icon1)
        self.btnNew.setIconSize(QSize(48, 48))
        self.btnNew.setAutoDefault(False)

        self.horizontalLayout_2.addWidget(self.btnNew)

        self.btnImport = QPushButton(StartDialog)
        self.btnImport.setObjectName(u"btnImport")
        sizePolicy1.setHeightForWidth(self.btnImport.sizePolicy().hasHeightForWidth())
        self.btnImport.setSizePolicy(sizePolicy1)
        self.btnImport.setMinimumSize(QSize(200, 0))
        self.btnImport.setMaximumSize(QSize(16777215, 150))
        self.btnImport.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/OpenIMU/icons/import.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnImport.setIcon(icon2)
        self.btnImport.setIconSize(QSize(40, 40))
        self.btnImport.setAutoDefault(False)

        self.horizontalLayout_2.addWidget(self.btnImport)

        self.btnOpen = QPushButton(StartDialog)
        self.btnOpen.setObjectName(u"btnOpen")
        sizePolicy1.setHeightForWidth(self.btnOpen.sizePolicy().hasHeightForWidth())
        self.btnOpen.setSizePolicy(sizePolicy1)
        self.btnOpen.setMinimumSize(QSize(200, 0))
        self.btnOpen.setMaximumSize(QSize(16777215, 150))
        self.btnOpen.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/OpenIMU/icons/compact.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnOpen.setIcon(icon3)
        self.btnOpen.setIconSize(QSize(48, 48))
        self.btnOpen.setAutoDefault(False)
        self.btnOpen.setFlat(False)

        self.horizontalLayout_2.addWidget(self.btnOpen)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.lblRecents = QLabel(StartDialog)
        self.lblRecents.setObjectName(u"lblRecents")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lblRecents.sizePolicy().hasHeightForWidth())
        self.lblRecents.setSizePolicy(sizePolicy2)
        self.lblRecents.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.lblRecents)

        self.cmbRecents = QComboBox(StartDialog)
        self.cmbRecents.setObjectName(u"cmbRecents")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.cmbRecents.sizePolicy().hasHeightForWidth())
        self.cmbRecents.setSizePolicy(sizePolicy3)
        self.cmbRecents.setMinimumSize(QSize(0, 22))

        self.horizontalLayout_3.addWidget(self.cmbRecents)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.btnQuit = QPushButton(StartDialog)
        self.btnQuit.setObjectName(u"btnQuit")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.btnQuit.sizePolicy().hasHeightForWidth())
        self.btnQuit.setSizePolicy(sizePolicy4)
        self.btnQuit.setMinimumSize(QSize(150, 50))
        self.btnQuit.setMaximumSize(QSize(150, 16777215))
        self.btnQuit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon4 = QIcon()
        icon4.addFile(u":/OpenIMU/icons/delete.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnQuit.setIcon(icon4)
        self.btnQuit.setIconSize(QSize(24, 24))
        self.btnQuit.setAutoDefault(False)

        self.horizontalLayout_4.addWidget(self.btnQuit)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.lblVersion = QLabel(StartDialog)
        self.lblVersion.setObjectName(u"lblVersion")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.lblVersion.sizePolicy().hasHeightForWidth())
        self.lblVersion.setSizePolicy(sizePolicy5)
        font = QFont()
        font.setBold(True)
        self.lblVersion.setFont(font)
        self.lblVersion.setTextFormat(Qt.TextFormat.PlainText)
        self.lblVersion.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.lblVersion)

        self.lblVersionValue = QLabel(StartDialog)
        self.lblVersionValue.setObjectName(u"lblVersionValue")
        font1 = QFont()
        font1.setBold(False)
        self.lblVersionValue.setFont(font1)
        self.lblVersionValue.setText(u"1.1.3")

        self.horizontalLayout_4.addWidget(self.lblVersionValue)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.retranslateUi(StartDialog)

        QMetaObject.connectSlotsByName(StartDialog)
    # setupUi

    def retranslateUi(self, StartDialog):

        self.lblLogo.setText("")
        self.btnNew.setText(QCoreApplication.translate("StartDialog", u"Create new database", None))
        self.btnImport.setText(QCoreApplication.translate("StartDialog", u"Import sensor data\n"
"in database", None))
        self.btnOpen.setText(QCoreApplication.translate("StartDialog", u"Open existing database", None))
        self.lblRecents.setText(QCoreApplication.translate("StartDialog", u"Open recent file:", None))
        self.btnQuit.setText(QCoreApplication.translate("StartDialog", u"Quit", None))
        self.lblVersion.setText(QCoreApplication.translate("StartDialog", u"Version", None))
        pass
    # retranslateUi

