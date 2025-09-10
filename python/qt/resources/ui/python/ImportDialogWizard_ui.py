# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ImportDialogWizard.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QHBoxLayout, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)
import core_rc

class Ui_dlgImportWizard(object):
    def setupUi(self, dlgImportWizard):
        if not dlgImportWizard.objectName():
            dlgImportWizard.setObjectName(u"dlgImportWizard")
        dlgImportWizard.resize(598, 202)
        self.verticalLayout = QVBoxLayout(dlgImportWizard)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.radioNewDataset = QRadioButton(dlgImportWizard)
        self.radioNewDataset.setObjectName(u"radioNewDataset")
        icon = QIcon()
        icon.addFile(u":/OpenIMU/icons/new.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.radioNewDataset.setIcon(icon)
        self.radioNewDataset.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.radioNewDataset)

        self.radioExistingDataset = QRadioButton(dlgImportWizard)
        self.radioExistingDataset.setObjectName(u"radioExistingDataset")
        icon1 = QIcon()
        icon1.addFile(u":/OpenIMU/icons/compact.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.radioExistingDataset.setIcon(icon1)
        self.radioExistingDataset.setIconSize(QSize(28, 28))

        self.verticalLayout.addWidget(self.radioExistingDataset)

        self.frameExisting = QFrame(dlgImportWizard)
        self.frameExisting.setObjectName(u"frameExisting")
        self.frameExisting.setFrameShape(QFrame.StyledPanel)
        self.frameExisting.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frameExisting)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(24, -1, -1, -1)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.cmbFilename = QComboBox(self.frameExisting)
        self.cmbFilename.setObjectName(u"cmbFilename")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbFilename.sizePolicy().hasHeightForWidth())
        self.cmbFilename.setSizePolicy(sizePolicy)
        self.cmbFilename.setMinimumSize(QSize(0, 30))
        self.cmbFilename.setEditable(True)

        self.horizontalLayout_2.addWidget(self.cmbFilename)

        self.btnBrowse = QPushButton(self.frameExisting)
        self.btnBrowse.setObjectName(u"btnBrowse")
        self.btnBrowse.setMinimumSize(QSize(100, 40))
        self.btnBrowse.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/OpenIMU/icons/browse.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnBrowse.setIcon(icon2)
        self.btnBrowse.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.btnBrowse)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addWidget(self.frameExisting)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btnNext = QPushButton(dlgImportWizard)
        self.btnNext.setObjectName(u"btnNext")
        self.btnNext.setMinimumSize(QSize(150, 40))
        self.btnNext.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/OpenIMU/icons/next.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnNext.setIcon(icon3)
        self.btnNext.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.btnNext)

        self.btnCancel = QPushButton(dlgImportWizard)
        self.btnCancel.setObjectName(u"btnCancel")
        self.btnCancel.setMinimumSize(QSize(150, 40))
        self.btnCancel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon4 = QIcon()
        icon4.addFile(u":/OpenIMU/icons/undo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnCancel.setIcon(icon4)

        self.horizontalLayout.addWidget(self.btnCancel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(dlgImportWizard)

        QMetaObject.connectSlotsByName(dlgImportWizard)
    # setupUi

    def retranslateUi(self, dlgImportWizard):
        dlgImportWizard.setWindowTitle(QCoreApplication.translate("dlgImportWizard", u"Data import wizard", None))
        self.radioNewDataset.setText(QCoreApplication.translate("dlgImportWizard", u"Create a new database", None))
        self.radioExistingDataset.setText(QCoreApplication.translate("dlgImportWizard", u"Use an existing database", None))
        self.btnBrowse.setText(QCoreApplication.translate("dlgImportWizard", u"Browse...", None))
        self.btnNext.setText(QCoreApplication.translate("dlgImportWizard", u"Next", None))
        self.btnCancel.setText(QCoreApplication.translate("dlgImportWizard", u"Cancel", None))
    # retranslateUi

