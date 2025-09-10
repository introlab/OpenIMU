# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ImportBrowser.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QComboBox,
    QFrame, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)
import core_rc

class Ui_ImportBrowser(object):
    def setupUi(self, ImportBrowser):
        if not ImportBrowser.objectName():
            ImportBrowser.setObjectName(u"ImportBrowser")
        ImportBrowser.resize(985, 570)
        ImportBrowser.setAcceptDrops(True)
        icon = QIcon()
        icon.addFile(u":/OpenIMU/icons/OpenIMU.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        ImportBrowser.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(ImportBrowser)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.stackMain = QStackedWidget(ImportBrowser)
        self.stackMain.setObjectName(u"stackMain")
        self.pageFiles = QWidget()
        self.pageFiles.setObjectName(u"pageFiles")
        self.verticalLayout_3 = QVBoxLayout(self.pageFiles)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frameImport = QFrame(self.pageFiles)
        self.frameImport.setObjectName(u"frameImport")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameImport.sizePolicy().hasHeightForWidth())
        self.frameImport.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.frameImport)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frameTitle = QFrame(self.frameImport)
        self.frameTitle.setObjectName(u"frameTitle")
        self.horizontalLayout_4 = QHBoxLayout(self.frameTitle)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.lblIcon = QLabel(self.frameTitle)
        self.lblIcon.setObjectName(u"lblIcon")
        self.lblIcon.setMaximumSize(QSize(48, 48))
        self.lblIcon.setPixmap(QPixmap(u":/OpenIMU/icons/import.png"))
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


        self.verticalLayout_2.addWidget(self.frameTitle)

        self.frameParticipant = QFrame(self.frameImport)
        self.frameParticipant.setObjectName(u"frameParticipant")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frameParticipant.sizePolicy().hasHeightForWidth())
        self.frameParticipant.setSizePolicy(sizePolicy1)
        self.verticalLayout_6 = QVBoxLayout(self.frameParticipant)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(10)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lblParticipant = QLabel(self.frameParticipant)
        self.lblParticipant.setObjectName(u"lblParticipant")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lblParticipant.sizePolicy().hasHeightForWidth())
        self.lblParticipant.setSizePolicy(sizePolicy2)
        self.lblParticipant.setMinimumSize(QSize(0, 40))
        self.lblParticipant.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_5.addWidget(self.lblParticipant)

        self.cmbParticipant = QComboBox(self.frameParticipant)
        self.cmbParticipant.setObjectName(u"cmbParticipant")
        self.cmbParticipant.setMinimumSize(QSize(300, 40))
        self.cmbParticipant.setEditable(False)

        self.horizontalLayout_5.addWidget(self.cmbParticipant)

        self.btnAddPart = QPushButton(self.frameParticipant)
        self.btnAddPart.setObjectName(u"btnAddPart")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.btnAddPart.sizePolicy().hasHeightForWidth())
        self.btnAddPart.setSizePolicy(sizePolicy3)
        self.btnAddPart.setMinimumSize(QSize(150, 25))
        self.btnAddPart.setMaximumSize(QSize(200, 40))
        self.btnAddPart.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/OpenIMU/icons/participant_new.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnAddPart.setIcon(icon1)
        self.btnAddPart.setIconSize(QSize(20, 20))
        self.btnAddPart.setAutoDefault(False)

        self.horizontalLayout_5.addWidget(self.btnAddPart)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.lblWarning = QLabel(self.frameParticipant)
        self.lblWarning.setObjectName(u"lblWarning")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.lblWarning.setFont(font1)

        self.verticalLayout_6.addWidget(self.lblWarning)


        self.verticalLayout_2.addWidget(self.frameParticipant)

        self.frameButtons = QFrame(self.frameImport)
        self.frameButtons.setObjectName(u"frameButtons")
        self.horizontalLayout = QHBoxLayout(self.frameButtons)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lblDragDrop = QLabel(self.frameButtons)
        self.lblDragDrop.setObjectName(u"lblDragDrop")
        font2 = QFont()
        font2.setPointSize(12)
        self.lblDragDrop.setFont(font2)
        self.lblDragDrop.setTextFormat(Qt.PlainText)
        self.lblDragDrop.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.lblDragDrop)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.btnAddFile = QPushButton(self.frameButtons)
        self.btnAddFile.setObjectName(u"btnAddFile")
        self.btnAddFile.setMinimumSize(QSize(250, 40))
        self.btnAddFile.setMaximumSize(QSize(16777215, 40))
        self.btnAddFile.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/OpenIMU/icons/new.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnAddFile.setIcon(icon2)
        self.btnAddFile.setIconSize(QSize(20, 20))
        self.btnAddFile.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.btnAddFile)

        self.btnAddDir = QPushButton(self.frameButtons)
        self.btnAddDir.setObjectName(u"btnAddDir")
        self.btnAddDir.setMinimumSize(QSize(250, 40))
        self.btnAddDir.setMaximumSize(QSize(16777215, 40))
        self.btnAddDir.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/OpenIMU/icons/browse.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnAddDir.setIcon(icon3)
        self.btnAddDir.setIconSize(QSize(20, 20))
        self.btnAddDir.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.btnAddDir)


        self.verticalLayout_2.addWidget(self.frameButtons)

        self.tableFiles = QTableWidget(self.frameImport)
        if (self.tableFiles.columnCount() < 3):
            self.tableFiles.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableFiles.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableFiles.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableFiles.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableFiles.setObjectName(u"tableFiles")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.tableFiles.sizePolicy().hasHeightForWidth())
        self.tableFiles.setSizePolicy(sizePolicy4)
        self.tableFiles.setMaximumSize(QSize(16777215, 16777215))
        self.tableFiles.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableFiles.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.tableFiles.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableFiles.setProperty(u"showDropIndicator", False)
        self.tableFiles.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableFiles.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableFiles.setIconSize(QSize(16, 16))
        self.tableFiles.setTextElideMode(Qt.ElideNone)
        self.tableFiles.setWordWrap(False)
        self.tableFiles.setColumnCount(3)
        self.tableFiles.horizontalHeader().setVisible(True)
        self.tableFiles.horizontalHeader().setDefaultSectionSize(200)
        self.tableFiles.horizontalHeader().setStretchLastSection(True)
        self.tableFiles.verticalHeader().setVisible(False)
        self.tableFiles.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_2.addWidget(self.tableFiles)

        self.frameTools = QFrame(self.frameImport)
        self.frameTools.setObjectName(u"frameTools")
        self.horizontalLayout_2 = QHBoxLayout(self.frameTools)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.btnDelFile = QPushButton(self.frameTools)
        self.btnDelFile.setObjectName(u"btnDelFile")
        self.btnDelFile.setEnabled(False)
        self.btnDelFile.setMinimumSize(QSize(150, 40))
        self.btnDelFile.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon4 = QIcon()
        icon4.addFile(u":/OpenIMU/icons/delete.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnDelFile.setIcon(icon4)
        self.btnDelFile.setIconSize(QSize(20, 20))
        self.btnDelFile.setAutoDefault(False)

        self.horizontalLayout_2.addWidget(self.btnDelFile)


        self.verticalLayout_2.addWidget(self.frameTools)

        self.progAdding = QProgressBar(self.frameImport)
        self.progAdding.setObjectName(u"progAdding")
        self.progAdding.setValue(0)

        self.verticalLayout_2.addWidget(self.progAdding)

        self.frameFormButtons = QFrame(self.frameImport)
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
        icon5 = QIcon()
        icon5.addFile(u":/OpenIMU/icons/import.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnOK.setIcon(icon5)
        self.btnOK.setIconSize(QSize(24, 24))
        self.btnOK.setAutoDefault(False)

        self.horizontalLayout_3.addWidget(self.btnOK)

        self.btnCancel = QPushButton(self.frameFormButtons)
        self.btnCancel.setObjectName(u"btnCancel")
        self.btnCancel.setMinimumSize(QSize(150, 40))
        self.btnCancel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon6 = QIcon()
        icon6.addFile(u":/OpenIMU/icons/undo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnCancel.setIcon(icon6)
        self.btnCancel.setIconSize(QSize(24, 24))
        self.btnCancel.setAutoDefault(False)

        self.horizontalLayout_3.addWidget(self.btnCancel)


        self.verticalLayout_2.addWidget(self.frameFormButtons)


        self.verticalLayout_3.addWidget(self.frameImport)

        self.stackMain.addWidget(self.pageFiles)
        self.pageDropFiles = QWidget()
        self.pageDropFiles.setObjectName(u"pageDropFiles")
        self.verticalLayout_4 = QVBoxLayout(self.pageDropFiles)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.frameDropFiles = QFrame(self.pageDropFiles)
        self.frameDropFiles.setObjectName(u"frameDropFiles")
        self.frameDropFiles.setFrameShape(QFrame.Box)
        self.frameDropFiles.setFrameShadow(QFrame.Plain)
        self.verticalLayout_5 = QVBoxLayout(self.frameDropFiles)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)

        self.lblDropFiles = QLabel(self.frameDropFiles)
        self.lblDropFiles.setObjectName(u"lblDropFiles")
        sizePolicy1.setHeightForWidth(self.lblDropFiles.sizePolicy().hasHeightForWidth())
        self.lblDropFiles.setSizePolicy(sizePolicy1)
        font3 = QFont()
        font3.setPointSize(22)
        self.lblDropFiles.setFont(font3)
        self.lblDropFiles.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.lblDropFiles)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lblDropParticipant = QLabel(self.frameDropFiles)
        self.lblDropParticipant.setObjectName(u"lblDropParticipant")
        sizePolicy1.setHeightForWidth(self.lblDropParticipant.sizePolicy().hasHeightForWidth())
        self.lblDropParticipant.setSizePolicy(sizePolicy1)
        font4 = QFont()
        font4.setPointSize(12)
        font4.setBold(False)
        self.lblDropParticipant.setFont(font4)
        self.lblDropParticipant.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.lblDropParticipant)

        self.lblDropParticipantName = QLabel(self.frameDropFiles)
        self.lblDropParticipantName.setObjectName(u"lblDropParticipantName")
        font5 = QFont()
        font5.setPointSize(12)
        font5.setBold(True)
        self.lblDropParticipantName.setFont(font5)

        self.horizontalLayout_6.addWidget(self.lblDropParticipantName)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)


        self.verticalLayout_4.addWidget(self.frameDropFiles)

        self.stackMain.addWidget(self.pageDropFiles)

        self.verticalLayout.addWidget(self.stackMain)


        self.retranslateUi(ImportBrowser)

        self.stackMain.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ImportBrowser)
    # setupUi

    def retranslateUi(self, ImportBrowser):
        ImportBrowser.setWindowTitle(QCoreApplication.translate("ImportBrowser", u"Data file importer", None))
        self.lblIcon.setText("")
        self.lblInfos.setText(QCoreApplication.translate("ImportBrowser", u"Import data files", None))
        self.lblParticipant.setText(QCoreApplication.translate("ImportBrowser", u"Target participant:", None))
        self.btnAddPart.setText(QCoreApplication.translate("ImportBrowser", u"Add participant", None))
        self.lblWarning.setText(QCoreApplication.translate("ImportBrowser", u"Warning: no target participant selected. Added files will need to be manually assigned to a participant.", None))
        self.lblDragDrop.setText(QCoreApplication.translate("ImportBrowser", u"Drag & Drop files to import or use one of the import button", None))
        self.btnAddFile.setText(QCoreApplication.translate("ImportBrowser", u"Add files", None))
        self.btnAddDir.setText(QCoreApplication.translate("ImportBrowser", u"Add folder", None))
        ___qtablewidgetitem = self.tableFiles.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("ImportBrowser", u"File", None));
        ___qtablewidgetitem1 = self.tableFiles.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("ImportBrowser", u"File format", None));
        ___qtablewidgetitem2 = self.tableFiles.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("ImportBrowser", u"Participant", None));
        self.btnDelFile.setText(QCoreApplication.translate("ImportBrowser", u"Remove from list", None))
        self.progAdding.setFormat(QCoreApplication.translate("ImportBrowser", u"Adding file: %v / %m", None))
        self.btnOK.setText(QCoreApplication.translate("ImportBrowser", u"Import data", None))
        self.btnCancel.setText(QCoreApplication.translate("ImportBrowser", u"Cancel", None))
        self.lblDropFiles.setText(QCoreApplication.translate("ImportBrowser", u"Drag & drop files to import here", None))
        self.lblDropParticipant.setText(QCoreApplication.translate("ImportBrowser", u"Target participant:", None))
        self.lblDropParticipantName.setText(QCoreApplication.translate("ImportBrowser", u"Unspecified", None))
    # retranslateUi

