# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ImportMatchDialog.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)
import core_rc

class Ui_ImportMatchDialog(object):
    def setupUi(self, ImportMatchDialog):
        if not ImportMatchDialog.objectName():
            ImportMatchDialog.setObjectName(u"ImportMatchDialog")
        ImportMatchDialog.resize(522, 428)
        self.verticalLayout = QVBoxLayout(ImportMatchDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lblInstructions = QLabel(ImportMatchDialog)
        self.lblInstructions.setObjectName(u"lblInstructions")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.lblInstructions.setFont(font)
        self.lblInstructions.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.lblInstructions)

        self.tableMatch = QTableWidget(ImportMatchDialog)
        if (self.tableMatch.columnCount() < 2):
            self.tableMatch.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableMatch.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableMatch.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableMatch.setObjectName(u"tableMatch")
        self.tableMatch.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableMatch.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableMatch.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableMatch.horizontalHeader().setMinimumSectionSize(50)
        self.tableMatch.horizontalHeader().setDefaultSectionSize(225)
        self.tableMatch.horizontalHeader().setStretchLastSection(True)
        self.tableMatch.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.tableMatch)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.btnAddParticipant = QPushButton(ImportMatchDialog)
        self.btnAddParticipant.setObjectName(u"btnAddParticipant")
        self.btnAddParticipant.setMinimumSize(QSize(150, 40))
        self.btnAddParticipant.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/OpenIMU/icons/participant_new.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnAddParticipant.setIcon(icon)
        self.btnAddParticipant.setIconSize(QSize(24, 24))

        self.horizontalLayout_2.addWidget(self.btnAddParticipant)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btnOK = QPushButton(ImportMatchDialog)
        self.btnOK.setObjectName(u"btnOK")
        self.btnOK.setMinimumSize(QSize(150, 40))
        self.btnOK.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/OpenIMU/icons/ok.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnOK.setIcon(icon1)
        self.btnOK.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.btnOK)

        self.btnCancel = QPushButton(ImportMatchDialog)
        self.btnCancel.setObjectName(u"btnCancel")
        self.btnCancel.setMinimumSize(QSize(150, 40))
        self.btnCancel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/OpenIMU/icons/undo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnCancel.setIcon(icon2)
        self.btnCancel.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.btnCancel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(ImportMatchDialog)

        QMetaObject.connectSlotsByName(ImportMatchDialog)
    # setupUi

    def retranslateUi(self, ImportMatchDialog):
        ImportMatchDialog.setWindowTitle(QCoreApplication.translate("ImportMatchDialog", u"Data / participant matching", None))
        self.lblInstructions.setText(QCoreApplication.translate("ImportMatchDialog", u"Please assign the following data to the correct participant", None))
        ___qtablewidgetitem = self.tableMatch.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("ImportMatchDialog", u"Data", None));
        ___qtablewidgetitem1 = self.tableMatch.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("ImportMatchDialog", u"Participant", None));
        self.btnAddParticipant.setText(QCoreApplication.translate("ImportMatchDialog", u"Add participant", None))
        self.btnOK.setText(QCoreApplication.translate("ImportMatchDialog", u"OK", None))
        self.btnCancel.setText(QCoreApplication.translate("ImportMatchDialog", u"Cancel", None))
    # retranslateUi

