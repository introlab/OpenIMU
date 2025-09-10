# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ExportDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
import core_rc

class Ui_ExportDialog(object):
    def setupUi(self, ExportDialog):
        if not ExportDialog.objectName():
            ExportDialog.setObjectName(u"ExportDialog")
        ExportDialog.resize(752, 471)
        ExportDialog.setStyleSheet(u"QLabel#label_2{color:yellow;}")
        self.verticalLayout_2 = QVBoxLayout(ExportDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frameTitle = QFrame(ExportDialog)
        self.frameTitle.setObjectName(u"frameTitle")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameTitle.sizePolicy().hasHeightForWidth())
        self.frameTitle.setSizePolicy(sizePolicy)
        self.horizontalLayout_5 = QHBoxLayout(self.frameTitle)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.lblIcon = QLabel(self.frameTitle)
        self.lblIcon.setObjectName(u"lblIcon")
        self.lblIcon.setMaximumSize(QSize(36, 36))
        self.lblIcon.setPixmap(QPixmap(u":/OpenIMU/icons/export.png"))
        self.lblIcon.setScaledContents(True)

        self.horizontalLayout_5.addWidget(self.lblIcon)

        self.lblInfos = QLabel(self.frameTitle)
        self.lblInfos.setObjectName(u"lblInfos")
        sizePolicy.setHeightForWidth(self.lblInfos.sizePolicy().hasHeightForWidth())
        self.lblInfos.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        self.lblInfos.setFont(font)
        self.lblInfos.setAcceptDrops(False)

        self.horizontalLayout_5.addWidget(self.lblInfos)


        self.verticalLayout_2.addWidget(self.frameTitle)

        self.wdgDataSelector = QWidget(ExportDialog)
        self.wdgDataSelector.setObjectName(u"wdgDataSelector")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.wdgDataSelector.sizePolicy().hasHeightForWidth())
        self.wdgDataSelector.setSizePolicy(sizePolicy1)
        self.verticalLayout = QVBoxLayout(self.wdgDataSelector)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.verticalLayout_2.addWidget(self.wdgDataSelector)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.lblDestDir = QLabel(ExportDialog)
        self.lblDestDir.setObjectName(u"lblDestDir")
        sizePolicy.setHeightForWidth(self.lblDestDir.sizePolicy().hasHeightForWidth())
        self.lblDestDir.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setBold(True)
        self.lblDestDir.setFont(font1)

        self.verticalLayout_4.addWidget(self.lblDestDir)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.txtDir = QLineEdit(ExportDialog)
        self.txtDir.setObjectName(u"txtDir")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.txtDir.sizePolicy().hasHeightForWidth())
        self.txtDir.setSizePolicy(sizePolicy2)
        self.txtDir.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.txtDir)

        self.btnBrowse = QPushButton(ExportDialog)
        self.btnBrowse.setObjectName(u"btnBrowse")
        self.btnBrowse.setMinimumSize(QSize(125, 40))
        self.btnBrowse.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/OpenIMU/icons/browse.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnBrowse.setIcon(icon)
        self.btnBrowse.setIconSize(QSize(24, 24))
        self.btnBrowse.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.btnBrowse)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lblFormat = QLabel(ExportDialog)
        self.lblFormat.setObjectName(u"lblFormat")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.lblFormat.sizePolicy().hasHeightForWidth())
        self.lblFormat.setSizePolicy(sizePolicy3)
        self.lblFormat.setFont(font1)

        self.horizontalLayout_2.addWidget(self.lblFormat)

        self.comboFormat = QComboBox(ExportDialog)
        self.comboFormat.setObjectName(u"comboFormat")
        self.comboFormat.setMinimumSize(QSize(300, 24))
        self.comboFormat.setIconSize(QSize(24, 24))

        self.horizontalLayout_2.addWidget(self.comboFormat)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.chkDatabaseDir = QCheckBox(ExportDialog)
        self.chkDatabaseDir.setObjectName(u"chkDatabaseDir")
        self.chkDatabaseDir.setChecked(True)

        self.verticalLayout_4.addWidget(self.chkDatabaseDir)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer = QSpacerItem(40, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.btnOK = QPushButton(ExportDialog)
        self.btnOK.setObjectName(u"btnOK")
        self.btnOK.setMinimumSize(QSize(150, 40))
        self.btnOK.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/OpenIMU/icons/ok.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnOK.setIcon(icon1)
        self.btnOK.setIconSize(QSize(20, 20))
        self.btnOK.setAutoDefault(False)

        self.horizontalLayout_3.addWidget(self.btnOK)

        self.btnCancel = QPushButton(ExportDialog)
        self.btnCancel.setObjectName(u"btnCancel")
        self.btnCancel.setMinimumSize(QSize(150, 40))
        self.btnCancel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/OpenIMU/icons/undo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnCancel.setIcon(icon2)
        self.btnCancel.setIconSize(QSize(24, 24))
        self.btnCancel.setAutoDefault(False)

        self.horizontalLayout_3.addWidget(self.btnCancel)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)


        self.verticalLayout_2.addLayout(self.verticalLayout_4)


        self.retranslateUi(ExportDialog)

        QMetaObject.connectSlotsByName(ExportDialog)
    # setupUi

    def retranslateUi(self, ExportDialog):
        ExportDialog.setWindowTitle(QCoreApplication.translate("ExportDialog", u"Data exporter", None))
        self.lblIcon.setText("")
        self.lblInfos.setText(QCoreApplication.translate("ExportDialog", u"Select data to export", None))
        self.lblDestDir.setText(QCoreApplication.translate("ExportDialog", u"Destination directory:", None))
        self.txtDir.setPlaceholderText(QCoreApplication.translate("ExportDialog", u"Directory that will contains exported data files", None))
        self.btnBrowse.setText(QCoreApplication.translate("ExportDialog", u"Browse...", None))
        self.lblFormat.setText(QCoreApplication.translate("ExportDialog", u"Format:", None))
        self.chkDatabaseDir.setText(QCoreApplication.translate("ExportDialog", u"Create a subfolder with the database name", None))
        self.btnOK.setText(QCoreApplication.translate("ExportDialog", u"OK", None))
        self.btnCancel.setText(QCoreApplication.translate("ExportDialog", u"Cancel", None))
    # retranslateUi

