# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GraphWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QSizePolicy,
    QSpacerItem, QToolButton, QVBoxLayout, QWidget)
import core_rc

class Ui_frmGraphWidget(object):
    def setupUi(self, frmGraphWidget):
        if not frmGraphWidget.objectName():
            frmGraphWidget.setObjectName(u"frmGraphWidget")
        frmGraphWidget.resize(400, 542)
        frmGraphWidget.setMouseTracking(True)
        frmGraphWidget.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(frmGraphWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frameControls = QFrame(frmGraphWidget)
        self.frameControls.setObjectName(u"frameControls")
        self.verticalLayout_9 = QVBoxLayout(self.frameControls)
        self.verticalLayout_9.setSpacing(10)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(-1, -1, -1, 6)
        self.frameTools = QFrame(self.frameControls)
        self.frameTools.setObjectName(u"frameTools")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameTools.sizePolicy().hasHeightForWidth())
        self.frameTools.setSizePolicy(sizePolicy)
        self.frameTools.setMinimumSize(QSize(40, 0))
        self.frameTools.setFrameShape(QFrame.StyledPanel)
        self.frameTools.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frameTools)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btnMove = QToolButton(self.frameTools)
        self.btnMove.setObjectName(u"btnMove")
        self.btnMove.setMinimumSize(QSize(30, 30))
        self.btnMove.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/OpenIMU/icons/move.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnMove.setIcon(icon)
        self.btnMove.setIconSize(QSize(24, 24))
        self.btnMove.setCheckable(True)

        self.verticalLayout.addWidget(self.btnMove)

        self.btnSelect = QToolButton(self.frameTools)
        self.btnSelect.setObjectName(u"btnSelect")
        self.btnSelect.setMinimumSize(QSize(30, 30))
        self.btnSelect.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/OpenIMU/icons/select.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnSelect.setIcon(icon1)
        self.btnSelect.setIconSize(QSize(24, 24))
        self.btnSelect.setCheckable(True)
        self.btnSelect.setChecked(True)

        self.verticalLayout.addWidget(self.btnSelect)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.btnZoomIn = QToolButton(self.frameTools)
        self.btnZoomIn.setObjectName(u"btnZoomIn")
        self.btnZoomIn.setMinimumSize(QSize(30, 30))
        self.btnZoomIn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/OpenIMU/icons/zoom_in.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnZoomIn.setIcon(icon2)
        self.btnZoomIn.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btnZoomIn)

        self.btnZoomOut = QToolButton(self.frameTools)
        self.btnZoomOut.setObjectName(u"btnZoomOut")
        self.btnZoomOut.setMinimumSize(QSize(30, 30))
        self.btnZoomOut.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/OpenIMU/icons/zoom_out.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnZoomOut.setIcon(icon3)
        self.btnZoomOut.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btnZoomOut)

        self.btnZoomArea = QToolButton(self.frameTools)
        self.btnZoomArea.setObjectName(u"btnZoomArea")
        self.btnZoomArea.setMinimumSize(QSize(30, 30))
        self.btnZoomArea.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon4 = QIcon()
        icon4.addFile(u":/OpenIMU/icons/zoom_selection.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnZoomArea.setIcon(icon4)
        self.btnZoomArea.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btnZoomArea)

        self.btnZoomReset = QToolButton(self.frameTools)
        self.btnZoomReset.setObjectName(u"btnZoomReset")
        self.btnZoomReset.setMinimumSize(QSize(30, 30))
        self.btnZoomReset.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon5 = QIcon()
        icon5.addFile(u":/OpenIMU/icons/zoom_reset.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnZoomReset.setIcon(icon5)
        self.btnZoomReset.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btnZoomReset)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.btnClearSelection = QToolButton(self.frameTools)
        self.btnClearSelection.setObjectName(u"btnClearSelection")
        self.btnClearSelection.setMinimumSize(QSize(30, 30))
        self.btnClearSelection.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon6 = QIcon()
        icon6.addFile(u":/OpenIMU/icons/selection_clear.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnClearSelection.setIcon(icon6)
        self.btnClearSelection.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btnClearSelection, 0, Qt.AlignHCenter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.verticalLayout_9.addWidget(self.frameTools)

        self.btnDataInfos = QToolButton(self.frameControls)
        self.btnDataInfos.setObjectName(u"btnDataInfos")
        self.btnDataInfos.setMinimumSize(QSize(30, 30))
        self.btnDataInfos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon7 = QIcon()
        icon7.addFile(u":/OpenIMU/icons/info.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnDataInfos.setIcon(icon7)
        self.btnDataInfos.setIconSize(QSize(24, 24))

        self.verticalLayout_9.addWidget(self.btnDataInfos, 0, Qt.AlignHCenter|Qt.AlignBottom)


        self.horizontalLayout.addWidget(self.frameControls)

        self.wdgChart = QWidget(frmGraphWidget)
        self.wdgChart.setObjectName(u"wdgChart")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.wdgChart.sizePolicy().hasHeightForWidth())
        self.wdgChart.setSizePolicy(sizePolicy1)
        self.wdgChart.setMouseTracking(False)
        self.verticalLayout_3 = QVBoxLayout(self.wdgChart)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout.addWidget(self.wdgChart)


        self.retranslateUi(frmGraphWidget)

        QMetaObject.connectSlotsByName(frmGraphWidget)
    # setupUi

    def retranslateUi(self, frmGraphWidget):
        frmGraphWidget.setWindowTitle(QCoreApplication.translate("frmGraphWidget", u"Graph display", None))
#if QT_CONFIG(tooltip)
        self.btnMove.setToolTip(QCoreApplication.translate("frmGraphWidget", u"Move tool", None))
#endif // QT_CONFIG(tooltip)
        self.btnMove.setText(QCoreApplication.translate("frmGraphWidget", u"...", None))
#if QT_CONFIG(tooltip)
        self.btnSelect.setToolTip(QCoreApplication.translate("frmGraphWidget", u"Select tool", None))
#endif // QT_CONFIG(tooltip)
        self.btnSelect.setText(QCoreApplication.translate("frmGraphWidget", u"...", None))
#if QT_CONFIG(tooltip)
        self.btnZoomIn.setToolTip(QCoreApplication.translate("frmGraphWidget", u"Zoom in", None))
#endif // QT_CONFIG(tooltip)
        self.btnZoomIn.setText(QCoreApplication.translate("frmGraphWidget", u"...", None))
#if QT_CONFIG(tooltip)
        self.btnZoomOut.setToolTip(QCoreApplication.translate("frmGraphWidget", u"Zoom out", None))
#endif // QT_CONFIG(tooltip)
        self.btnZoomOut.setText(QCoreApplication.translate("frmGraphWidget", u"...", None))
#if QT_CONFIG(tooltip)
        self.btnZoomArea.setToolTip(QCoreApplication.translate("frmGraphWidget", u"Zoom on selection", None))
#endif // QT_CONFIG(tooltip)
        self.btnZoomArea.setText(QCoreApplication.translate("frmGraphWidget", u"...", None))
#if QT_CONFIG(tooltip)
        self.btnZoomReset.setToolTip(QCoreApplication.translate("frmGraphWidget", u"Initial zoom", None))
#endif // QT_CONFIG(tooltip)
        self.btnZoomReset.setText(QCoreApplication.translate("frmGraphWidget", u"...", None))
#if QT_CONFIG(tooltip)
        self.btnClearSelection.setToolTip(QCoreApplication.translate("frmGraphWidget", u"Clear selection", None))
#endif // QT_CONFIG(tooltip)
        self.btnClearSelection.setText(QCoreApplication.translate("frmGraphWidget", u"...", None))
#if QT_CONFIG(tooltip)
        self.btnDataInfos.setToolTip(QCoreApplication.translate("frmGraphWidget", u"Data informations", None))
#endif // QT_CONFIG(tooltip)
        self.btnDataInfos.setText(QCoreApplication.translate("frmGraphWidget", u"...", None))
    # retranslateUi

