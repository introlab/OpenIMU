# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ProcessSelectDialog.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QDialog, QFormLayout,
    QFrame, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPlainTextEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QVBoxLayout, QWidget)
import core_rc

class Ui_dlgProcessSelect(object):
    def setupUi(self, dlgProcessSelect):
        if not dlgProcessSelect.objectName():
            dlgProcessSelect.setObjectName(u"dlgProcessSelect")
        dlgProcessSelect.resize(760, 500)
        dlgProcessSelect.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(dlgProcessSelect)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frameTitle = QFrame(dlgProcessSelect)
        self.frameTitle.setObjectName(u"frameTitle")
        self.horizontalLayout_2 = QHBoxLayout(self.frameTitle)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lblIcon = QLabel(self.frameTitle)
        self.lblIcon.setObjectName(u"lblIcon")
        self.lblIcon.setMaximumSize(QSize(48, 48))
        self.lblIcon.setPixmap(QPixmap(u":/OpenIMU/icons/results.png"))
        self.lblIcon.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.lblIcon)

        self.lblInfos = QLabel(self.frameTitle)
        self.lblInfos.setObjectName(u"lblInfos")
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        self.lblInfos.setFont(font)

        self.horizontalLayout_2.addWidget(self.lblInfos)


        self.verticalLayout.addWidget(self.frameTitle)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.listWidget = QListWidget(dlgProcessSelect)
        self.listWidget.setObjectName(u"listWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setMaximumSize(QSize(200, 16777215))
        self.listWidget.setIconSize(QSize(20, 20))

        self.horizontalLayout_3.addWidget(self.listWidget)

        self.tabAlgo = QTabWidget(dlgProcessSelect)
        self.tabAlgo.setObjectName(u"tabAlgo")
        self.tabAlgo.setIconSize(QSize(20, 20))
        self.tabInfos = QWidget()
        self.tabInfos.setObjectName(u"tabInfos")
        self.formLayout = QFormLayout(self.tabInfos)
        self.formLayout.setObjectName(u"formLayout")
        self.lblName = QLabel(self.tabInfos)
        self.lblName.setObjectName(u"lblName")
        font1 = QFont()
        font1.setBold(False)
        self.lblName.setFont(font1)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lblName)

        self.lblNameValue = QLabel(self.tabInfos)
        self.lblNameValue.setObjectName(u"lblNameValue")
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        self.lblNameValue.setFont(font2)
        self.lblNameValue.setText(u"(Name)")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lblNameValue)

        self.lblAuthor = QLabel(self.tabInfos)
        self.lblAuthor.setObjectName(u"lblAuthor")
        self.lblAuthor.setFont(font1)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lblAuthor)

        self.lblAuthorValue = QLabel(self.tabInfos)
        self.lblAuthorValue.setObjectName(u"lblAuthorValue")
        font3 = QFont()
        font3.setBold(True)
        self.lblAuthorValue.setFont(font3)
        self.lblAuthorValue.setText(u"(Auteur)")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lblAuthorValue)

        self.lblProcessVersion = QLabel(self.tabInfos)
        self.lblProcessVersion.setObjectName(u"lblProcessVersion")
        self.lblProcessVersion.setFont(font1)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lblProcessVersion)

        self.lblVersionValue = QLabel(self.tabInfos)
        self.lblVersionValue.setObjectName(u"lblVersionValue")
        self.lblVersionValue.setFont(font3)
        self.lblVersionValue.setText(u"(Version)")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lblVersionValue)

        self.lblDesc = QLabel(self.tabInfos)
        self.lblDesc.setObjectName(u"lblDesc")
        self.lblDesc.setFont(font1)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.lblDesc)

        self.txtDesc = QPlainTextEdit(self.tabInfos)
        self.txtDesc.setObjectName(u"txtDesc")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.txtDesc.sizePolicy().hasHeightForWidth())
        self.txtDesc.setSizePolicy(sizePolicy1)
        self.txtDesc.setFont(font1)
        self.txtDesc.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.txtDesc.setReadOnly(True)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.txtDesc)

        self.lblRef = QLabel(self.tabInfos)
        self.lblRef.setObjectName(u"lblRef")
        self.lblRef.setFont(font1)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.lblRef)

        self.lblRefValue = QLabel(self.tabInfos)
        self.lblRefValue.setObjectName(u"lblRefValue")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lblRefValue.sizePolicy().hasHeightForWidth())
        self.lblRefValue.setSizePolicy(sizePolicy2)
        self.lblRefValue.setFont(font3)
        self.lblRefValue.setText(u"(Reference)")
        self.lblRefValue.setTextFormat(Qt.AutoText)
        self.lblRefValue.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.lblRefValue.setWordWrap(True)
        self.lblRefValue.setOpenExternalLinks(True)
        self.lblRefValue.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.lblRefValue)

        icon = QIcon()
        icon.addFile(u":/OpenIMU/icons/info.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabAlgo.addTab(self.tabInfos, icon, "")
        self.tabParams = QWidget()
        self.tabParams.setObjectName(u"tabParams")
        icon1 = QIcon()
        icon1.addFile(u":/OpenIMU/icons/graph.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabAlgo.addTab(self.tabParams, icon1, "")

        self.horizontalLayout_3.addWidget(self.tabAlgo)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btnProcess = QPushButton(dlgProcessSelect)
        self.btnProcess.setObjectName(u"btnProcess")
        self.btnProcess.setMinimumSize(QSize(150, 40))
        self.btnProcess.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/OpenIMU/icons/process.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnProcess.setIcon(icon2)
        self.btnProcess.setIconSize(QSize(30, 30))
        self.btnProcess.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.btnProcess)

        self.btnCancel = QPushButton(dlgProcessSelect)
        self.btnCancel.setObjectName(u"btnCancel")
        self.btnCancel.setMinimumSize(QSize(150, 40))
        self.btnCancel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/OpenIMU/icons/undo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnCancel.setIcon(icon3)
        self.btnCancel.setIconSize(QSize(20, 20))
        self.btnCancel.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.btnCancel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(dlgProcessSelect)
        self.btnCancel.clicked.connect(dlgProcessSelect.close)

        self.tabAlgo.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(dlgProcessSelect)
    # setupUi

    def retranslateUi(self, dlgProcessSelect):
        dlgProcessSelect.setWindowTitle(QCoreApplication.translate("dlgProcessSelect", u"Processing algorithm selection", None))
        self.lblIcon.setText("")
        self.lblInfos.setText(QCoreApplication.translate("dlgProcessSelect", u"Processing algorithms", None))
        self.lblName.setText(QCoreApplication.translate("dlgProcessSelect", u"Name", None))
        self.lblAuthor.setText(QCoreApplication.translate("dlgProcessSelect", u"Author", None))
        self.lblProcessVersion.setText(QCoreApplication.translate("dlgProcessSelect", u"Version", None))
        self.lblDesc.setText(QCoreApplication.translate("dlgProcessSelect", u"Description", None))
        self.lblRef.setText(QCoreApplication.translate("dlgProcessSelect", u"Reference", None))
        self.tabAlgo.setTabText(self.tabAlgo.indexOf(self.tabInfos), QCoreApplication.translate("dlgProcessSelect", u"Informations", None))
        self.tabAlgo.setTabText(self.tabAlgo.indexOf(self.tabParams), QCoreApplication.translate("dlgProcessSelect", u"Settings", None))
        self.btnProcess.setText(QCoreApplication.translate("dlgProcessSelect", u"Process", None))
        self.btnCancel.setText(QCoreApplication.translate("dlgProcessSelect", u"Cancel", None))
    # retranslateUi

