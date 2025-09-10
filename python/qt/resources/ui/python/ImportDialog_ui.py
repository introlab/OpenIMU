# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ImportDialog.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QDateEdit, QDateTimeEdit,
    QDialog, QGridLayout, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
import core_rc

class Ui_ImportDialog(object):
    def setupUi(self, ImportDialog):
        if not ImportDialog.objectName():
            ImportDialog.setObjectName(u"ImportDialog")
        ImportDialog.resize(906, 481)
        icon = QIcon()
        icon.addFile(u":/OpenIMU/icons/OpenIMU.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        ImportDialog.setWindowIcon(icon)
        ImportDialog.setAutoFillBackground(True)
        ImportDialog.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(ImportDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.lblName = QLabel(ImportDialog)
        self.lblName.setObjectName(u"lblName")
        font = QFont()
        font.setBold(True)
        self.lblName.setFont(font)
        self.lblName.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblName, 1, 0, 1, 1)

        self.lblAuthor = QLabel(ImportDialog)
        self.lblAuthor.setObjectName(u"lblAuthor")
        self.lblAuthor.setFont(font)
        self.lblAuthor.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblAuthor, 2, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.txtFileName = QLineEdit(ImportDialog)
        self.txtFileName.setObjectName(u"txtFileName")
        self.txtFileName.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_4.addWidget(self.txtFileName)

        self.btnBrowse = QPushButton(ImportDialog)
        self.btnBrowse.setObjectName(u"btnBrowse")
        self.btnBrowse.setMinimumSize(QSize(125, 40))
        self.btnBrowse.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/OpenIMU/icons/browse.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnBrowse.setIcon(icon1)
        self.btnBrowse.setIconSize(QSize(24, 24))
        self.btnBrowse.setAutoDefault(False)

        self.horizontalLayout_4.addWidget(self.btnBrowse)


        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 1, 1, 1)

        self.txtAuthor = QLineEdit(ImportDialog)
        self.txtAuthor.setObjectName(u"txtAuthor")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtAuthor.sizePolicy().hasHeightForWidth())
        self.txtAuthor.setSizePolicy(sizePolicy)
        self.txtAuthor.setMinimumSize(QSize(0, 0))

        self.gridLayout.addWidget(self.txtAuthor, 2, 1, 1, 1)

        self.lblFile = QLabel(ImportDialog)
        self.lblFile.setObjectName(u"lblFile")
        self.lblFile.setFont(font)
        self.lblFile.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblFile, 0, 0, 1, 1)

        self.txtName = QLineEdit(ImportDialog)
        self.txtName.setObjectName(u"txtName")
        sizePolicy.setHeightForWidth(self.txtName.sizePolicy().hasHeightForWidth())
        self.txtName.setSizePolicy(sizePolicy)
        self.txtName.setMinimumSize(QSize(0, 0))

        self.gridLayout.addWidget(self.txtName, 1, 1, 1, 1)

        self.lblDesc = QLabel(ImportDialog)
        self.lblDesc.setObjectName(u"lblDesc")
        self.lblDesc.setFont(font)
        self.lblDesc.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblDesc, 4, 0, 1, 1)

        self.txtDesc = QPlainTextEdit(ImportDialog)
        self.txtDesc.setObjectName(u"txtDesc")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.txtDesc.sizePolicy().hasHeightForWidth())
        self.txtDesc.setSizePolicy(sizePolicy1)
        self.txtDesc.setCenterOnScroll(False)

        self.gridLayout.addWidget(self.txtDesc, 4, 1, 1, 1)

        self.lblUploadDate = QLabel(ImportDialog)
        self.lblUploadDate.setObjectName(u"lblUploadDate")
        self.lblUploadDate.setFont(font)
        self.lblUploadDate.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblUploadDate, 3, 0, 1, 1)

        self.dateData = QDateEdit(ImportDialog)
        self.dateData.setObjectName(u"dateData")
        self.dateData.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.dateData.setAccelerated(True)
        self.dateData.setMinimumDateTime(QDateTime(QDate(2015, 9, 14), QTime(0, 0, 0)))
        self.dateData.setCurrentSection(QDateTimeEdit.DaySection)
        self.dateData.setDisplayFormat(u"dd/MM/yyyy")
        self.dateData.setCalendarPopup(True)

        self.gridLayout.addWidget(self.dateData, 3, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer = QSpacerItem(40, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.btnOK = QPushButton(ImportDialog)
        self.btnOK.setObjectName(u"btnOK")
        self.btnOK.setMinimumSize(QSize(150, 40))
        self.btnOK.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/OpenIMU/icons/ok.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnOK.setIcon(icon2)
        self.btnOK.setIconSize(QSize(20, 20))
        self.btnOK.setAutoDefault(False)

        self.horizontalLayout_3.addWidget(self.btnOK)

        self.btnCancel = QPushButton(ImportDialog)
        self.btnCancel.setObjectName(u"btnCancel")
        self.btnCancel.setMinimumSize(QSize(150, 40))
        self.btnCancel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/OpenIMU/icons/undo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnCancel.setIcon(icon3)
        self.btnCancel.setIconSize(QSize(20, 20))
        self.btnCancel.setAutoDefault(False)

        self.horizontalLayout_3.addWidget(self.btnCancel)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        QWidget.setTabOrder(self.txtFileName, self.btnOK)
        QWidget.setTabOrder(self.btnOK, self.btnCancel)
        QWidget.setTabOrder(self.btnCancel, self.btnBrowse)

        self.retranslateUi(ImportDialog)

        QMetaObject.connectSlotsByName(ImportDialog)
    # setupUi

    def retranslateUi(self, ImportDialog):
        ImportDialog.setWindowTitle(QCoreApplication.translate("ImportDialog", u"Dataset informations", None))
        self.lblName.setText(QCoreApplication.translate("ImportDialog", u"<font color=\"red\">*</font> Database title:", None))
        self.lblAuthor.setText(QCoreApplication.translate("ImportDialog", u"<font color=\"red\">*</font> Dataset author:", None))
        self.txtFileName.setInputMask("")
        self.txtFileName.setPlaceholderText(QCoreApplication.translate("ImportDialog", u".oi file that will store the data", None))
        self.btnBrowse.setText(QCoreApplication.translate("ImportDialog", u"Browse...", None))
        self.txtAuthor.setPlaceholderText(QCoreApplication.translate("ImportDialog", u"Author, data source, research team name, ...", None))
        self.lblFile.setText(QCoreApplication.translate("ImportDialog", u"<font color=\"red\">*</font> Database filename:", None))
        self.txtName.setPlaceholderText(QCoreApplication.translate("ImportDialog", u"Database name", None))
        self.lblDesc.setText(QCoreApplication.translate("ImportDialog", u"Description / context:", None))
        self.txtDesc.setDocumentTitle("")
        self.txtDesc.setPlaceholderText(QCoreApplication.translate("ImportDialog", u"Dataset description or data collection context", None))
        self.lblUploadDate.setText(QCoreApplication.translate("ImportDialog", u"<font color=\"red\">*</font> Dataset collection date:", None))
        self.btnOK.setText(QCoreApplication.translate("ImportDialog", u"OK", None))
        self.btnCancel.setText(QCoreApplication.translate("ImportDialog", u"Cancel", None))
    # retranslateUi

