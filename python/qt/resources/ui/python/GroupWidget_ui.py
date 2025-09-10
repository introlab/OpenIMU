# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GroupWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QToolButton,
    QVBoxLayout, QWidget)
import core_rc

class Ui_frmGroup(object):
    def setupUi(self, frmGroup):
        if not frmGroup.objectName():
            frmGroup.setObjectName(u"frmGroup")
        frmGroup.resize(750, 480)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frmGroup.sizePolicy().hasHeightForWidth())
        frmGroup.setSizePolicy(sizePolicy)
        frmGroup.setMaximumSize(QSize(800, 16777215))
        frmGroup.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(frmGroup)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frameTitle = QFrame(frmGroup)
        self.frameTitle.setObjectName(u"frameTitle")
        self.horizontalLayout_2 = QHBoxLayout(self.frameTitle)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lblIcon = QLabel(self.frameTitle)
        self.lblIcon.setObjectName(u"lblIcon")
        self.lblIcon.setMaximumSize(QSize(48, 48))
        self.lblIcon.setPixmap(QPixmap(u":/OpenIMU/icons/group.png"))
        self.lblIcon.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.lblIcon)

        self.txtName = QLineEdit(self.frameTitle)
        self.txtName.setObjectName(u"txtName")
        self.txtName.setMinimumSize(QSize(0, 30))
        self.txtName.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.txtName.setFont(font)

        self.horizontalLayout_2.addWidget(self.txtName)

        self.btnEdit = QToolButton(self.frameTitle)
        self.btnEdit.setObjectName(u"btnEdit")
        self.btnEdit.setMinimumSize(QSize(48, 48))
        self.btnEdit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/OpenIMU/icons/save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnEdit.setIcon(icon)
        self.btnEdit.setIconSize(QSize(36, 36))
        self.btnEdit.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.btnEdit)


        self.verticalLayout.addWidget(self.frameTitle)

        self.frameData = QFrame(frmGroup)
        self.frameData.setObjectName(u"frameData")
        self.formLayout = QFormLayout(self.frameData)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.formLayout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.lblDesc = QLabel(self.frameData)
        self.lblDesc.setObjectName(u"lblDesc")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lblDesc)

        self.txtDesc = QPlainTextEdit(self.frameData)
        self.txtDesc.setObjectName(u"txtDesc")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.txtDesc.sizePolicy().hasHeightForWidth())
        self.txtDesc.setSizePolicy(sizePolicy1)
        self.txtDesc.setMaximumSize(QSize(16777215, 16777215))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.txtDesc)

        self.frameButtons = QFrame(self.frameData)
        self.frameButtons.setObjectName(u"frameButtons")
        self.horizontalLayout = QHBoxLayout(self.frameButtons)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btnSave = QPushButton(self.frameButtons)
        self.btnSave.setObjectName(u"btnSave")
        self.btnSave.setEnabled(True)
        self.btnSave.setMinimumSize(QSize(150, 40))
        self.btnSave.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/OpenIMU/icons/ok.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnSave.setIcon(icon1)
        self.btnSave.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.btnSave)

        self.btnCancel = QPushButton(self.frameButtons)
        self.btnCancel.setObjectName(u"btnCancel")
        self.btnCancel.setEnabled(True)
        self.btnCancel.setMinimumSize(QSize(150, 40))
        self.btnCancel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/OpenIMU/icons/undo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnCancel.setIcon(icon2)
        self.btnCancel.setIconSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.btnCancel)


        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.frameButtons)


        self.verticalLayout.addWidget(self.frameData)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(frmGroup)

        QMetaObject.connectSlotsByName(frmGroup)
    # setupUi

    def retranslateUi(self, frmGroup):
        frmGroup.setWindowTitle(QCoreApplication.translate("frmGroup", u"Group", None))
        self.lblIcon.setText("")
        self.btnEdit.setText(QCoreApplication.translate("frmGroup", u"Edit", None))
        self.lblDesc.setText(QCoreApplication.translate("frmGroup", u"Description", None))
        self.btnSave.setText(QCoreApplication.translate("frmGroup", u"Save", None))
        self.btnCancel.setText(QCoreApplication.translate("frmGroup", u"Cancel", None))
    # retranslateUi

