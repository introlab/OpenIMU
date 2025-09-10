# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AboutScreen.ui'
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
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)
import core_rc

class Ui_AboutScreen(object):
    def setupUi(self, AboutScreen):
        if not AboutScreen.objectName():
            AboutScreen.setObjectName(u"AboutScreen")
        AboutScreen.resize(861, 460)
        self.verticalLayout = QVBoxLayout(AboutScreen)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lblAboutTitle = QLabel(AboutScreen)
        self.lblAboutTitle.setObjectName(u"lblAboutTitle")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.lblAboutTitle.setFont(font)
        self.lblAboutTitle.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.lblAboutTitle.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.lblAboutTitle)

        self.stackedMain = QStackedWidget(AboutScreen)
        self.stackedMain.setObjectName(u"stackedMain")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedMain.sizePolicy().hasHeightForWidth())
        self.stackedMain.setSizePolicy(sizePolicy)
        self.pageBoring = QWidget()
        self.pageBoring.setObjectName(u"pageBoring")
        self.verticalLayout_2 = QVBoxLayout(self.pageBoring)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lblIntrolab = QLabel(self.pageBoring)
        self.lblIntrolab.setObjectName(u"lblIntrolab")
        self.lblIntrolab.setMinimumSize(QSize(280, 180))
        self.lblIntrolab.setMaximumSize(QSize(280, 180))
        self.lblIntrolab.setPixmap(QPixmap(u":/OpenIMU/LogoOpenIMU.png"))
        self.lblIntrolab.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.lblIntrolab)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lblAuthors = QLabel(self.pageBoring)
        self.lblAuthors.setObjectName(u"lblAuthors")
        font1 = QFont()
        font1.setBold(True)
        self.lblAuthors.setFont(font1)

        self.verticalLayout_3.addWidget(self.lblAuthors)

        self.txtAuthors = QPlainTextEdit(self.pageBoring)
        self.txtAuthors.setObjectName(u"txtAuthors")
        self.txtAuthors.setEnabled(False)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.txtAuthors.sizePolicy().hasHeightForWidth())
        self.txtAuthors.setSizePolicy(sizePolicy1)
        self.txtAuthors.setReadOnly(True)
        self.txtAuthors.setPlainText(u"Simon Bri\u00e8re, ing., M.Sc.A.\n"
"Dominic L\u00e9tourneau, ing., M.Sc.A.")

        self.verticalLayout_3.addWidget(self.txtAuthors)

        self.lblContrib = QLabel(self.pageBoring)
        self.lblContrib.setObjectName(u"lblContrib")
        self.lblContrib.setFont(font1)

        self.verticalLayout_3.addWidget(self.lblContrib)

        self.txtContrib = QPlainTextEdit(self.pageBoring)
        self.txtContrib.setObjectName(u"txtContrib")
        self.txtContrib.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.txtContrib.sizePolicy().hasHeightForWidth())
        self.txtContrib.setSizePolicy(sizePolicy1)
        self.txtContrib.setReadOnly(True)
        self.txtContrib.setPlainText(u"Gevrai Jodoin-Tremblay\n"
"Antoine Guillerand")

        self.verticalLayout_3.addWidget(self.txtContrib)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.frameLogos = QFrame(self.pageBoring)
        self.frameLogos.setObjectName(u"frameLogos")
        self.frameLogos.setFrameShape(QFrame.StyledPanel)
        self.frameLogos.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frameLogos)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lblLogoCdRv = QLabel(self.frameLogos)
        self.lblLogoCdRv.setObjectName(u"lblLogoCdRv")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lblLogoCdRv.sizePolicy().hasHeightForWidth())
        self.lblLogoCdRv.setSizePolicy(sizePolicy2)
        self.lblLogoCdRv.setMinimumSize(QSize(220, 64))
        self.lblLogoCdRv.setMaximumSize(QSize(220, 16777215))
        self.lblLogoCdRv.setPixmap(QPixmap(u":/OpenIMU/logo_CDRV.png"))
        self.lblLogoCdRv.setScaledContents(True)

        self.horizontalLayout_3.addWidget(self.lblLogoCdRv)

        self.lblLogoINTER = QLabel(self.frameLogos)
        self.lblLogoINTER.setObjectName(u"lblLogoINTER")
        sizePolicy2.setHeightForWidth(self.lblLogoINTER.sizePolicy().hasHeightForWidth())
        self.lblLogoINTER.setSizePolicy(sizePolicy2)
        self.lblLogoINTER.setMinimumSize(QSize(220, 64))
        self.lblLogoINTER.setMaximumSize(QSize(220, 16777215))
        self.lblLogoINTER.setPixmap(QPixmap(u":/OpenIMU/INTER.png"))
        self.lblLogoINTER.setScaledContents(True)

        self.horizontalLayout_3.addWidget(self.lblLogoINTER)

        self.lblLogoIntroLab = QLabel(self.frameLogos)
        self.lblLogoIntroLab.setObjectName(u"lblLogoIntroLab")
        sizePolicy2.setHeightForWidth(self.lblLogoIntroLab.sizePolicy().hasHeightForWidth())
        self.lblLogoIntroLab.setSizePolicy(sizePolicy2)
        self.lblLogoIntroLab.setMinimumSize(QSize(220, 64))
        self.lblLogoIntroLab.setMaximumSize(QSize(220, 16777215))
        self.lblLogoIntroLab.setPixmap(QPixmap(u":/OpenIMU/IntRoLab.png"))
        self.lblLogoIntroLab.setScaledContents(True)

        self.horizontalLayout_3.addWidget(self.lblLogoIntroLab)


        self.verticalLayout_2.addWidget(self.frameLogos)

        self.stackedMain.addWidget(self.pageBoring)
        self.pageFun = QWidget()
        self.pageFun.setObjectName(u"pageFun")
        self.verticalLayout_4 = QVBoxLayout(self.pageFun)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.lblFun = QLabel(self.pageFun)
        self.lblFun.setObjectName(u"lblFun")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.lblFun.sizePolicy().hasHeightForWidth())
        self.lblFun.setSizePolicy(sizePolicy3)
        self.lblFun.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.lblFun)

        self.wdgFun = QWidget(self.pageFun)
        self.wdgFun.setObjectName(u"wdgFun")
        sizePolicy2.setHeightForWidth(self.wdgFun.sizePolicy().hasHeightForWidth())
        self.wdgFun.setSizePolicy(sizePolicy2)
        self.wdgFun.setMinimumSize(QSize(300, 300))
        self.wdgFun.setMaximumSize(QSize(300, 300))
        self.verticalLayout_5 = QVBoxLayout(self.wdgFun)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")

        self.verticalLayout_4.addWidget(self.wdgFun, 0, Qt.AlignHCenter)

        self.stackedMain.addWidget(self.pageFun)

        self.verticalLayout.addWidget(self.stackedMain)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btnOK = QPushButton(AboutScreen)
        self.btnOK.setObjectName(u"btnOK")
        self.btnOK.setMinimumSize(QSize(200, 40))
        self.btnOK.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/OpenIMU/icons/participant.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnOK.setIcon(icon)
        self.btnOK.setIconSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.btnOK)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(AboutScreen)

        self.stackedMain.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(AboutScreen)
    # setupUi

    def retranslateUi(self, AboutScreen):
        AboutScreen.setWindowTitle(QCoreApplication.translate("AboutScreen", u"About OpenIMU", None))
        self.lblAboutTitle.setText(QCoreApplication.translate("AboutScreen", u"About OpenIMU", None))
        self.lblIntrolab.setText("")
        self.lblAuthors.setText(QCoreApplication.translate("AboutScreen", u"Authors", None))
        self.lblContrib.setText(QCoreApplication.translate("AboutScreen", u"Contributors", None))
        self.lblLogoCdRv.setText("")
        self.lblLogoINTER.setText("")
        self.lblLogoIntroLab.setText("")
        self.lblFun.setText(QCoreApplication.translate("AboutScreen", u"Have some fun!", None))
        self.btnOK.setText(QCoreApplication.translate("AboutScreen", u"Thank you!", None))
    # retranslateUi

