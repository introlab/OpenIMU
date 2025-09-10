# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RecordsetWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QAbstractScrollArea,
    QApplication,
    QFrame,
    QGraphicsView,
    QHBoxLayout,
    QLabel,
    QLayout,
    QMdiArea,
    QPushButton,
    QScrollBar,
    QSizePolicy,
    QSpacerItem,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from qt.TimeView import TimeView
import core_rc


class Ui_frmRecordsets(object):
    def setupUi(self, frmRecordsets):
        if not frmRecordsets.objectName():
            frmRecordsets.setObjectName("frmRecordsets")
        frmRecordsets.resize(2560, 887)
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frmRecordsets.sizePolicy().hasHeightForWidth())
        frmRecordsets.setSizePolicy(sizePolicy)
        frmRecordsets.setStyleSheet("")
        self.verticalLayout_3 = QVBoxLayout(frmRecordsets)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frameTop = QFrame(frmRecordsets)
        self.frameTop.setObjectName("frameTop")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frameTop.sizePolicy().hasHeightForWidth())
        self.frameTop.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.frameTop)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(3, 0, 3, 0)
        self.frameInfos = QFrame(self.frameTop)
        self.frameInfos.setObjectName("frameInfos")
        self.frameInfos.setEnabled(True)
        sizePolicy2 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed
        )
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frameInfos.sizePolicy().hasHeightForWidth())
        self.frameInfos.setSizePolicy(sizePolicy2)
        self.frameInfos.setMinimumSize(QSize(0, 20))
        self.frameInfos.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_5 = QHBoxLayout(self.frameInfos)
        self.horizontalLayout_5.setSpacing(5)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(5, 6, 6, 6)
        self.lblTotal = QLabel(self.frameInfos)
        self.lblTotal.setObjectName("lblTotal")
        sizePolicy3 = QSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred
        )
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.lblTotal.sizePolicy().hasHeightForWidth())
        self.lblTotal.setSizePolicy(sizePolicy3)
        font = QFont()
        font.setBold(False)
        self.lblTotal.setFont(font)

        self.horizontalLayout_5.addWidget(self.lblTotal)

        self.lblTotalValue = QLabel(self.frameInfos)
        self.lblTotalValue.setObjectName("lblTotalValue")
        sizePolicy4 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum
        )
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(
            self.lblTotalValue.sizePolicy().hasHeightForWidth()
        )
        self.lblTotalValue.setSizePolicy(sizePolicy4)
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.lblTotalValue.setFont(font1)
        self.lblTotalValue.setText("29/03/2018 11:45:04 - 03/04/2018 09:37:56")

        self.horizontalLayout_5.addWidget(self.lblTotalValue)

        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.lblDuration = QLabel(self.frameInfos)
        self.lblDuration.setObjectName("lblDuration")
        sizePolicy3.setHeightForWidth(self.lblDuration.sizePolicy().hasHeightForWidth())
        self.lblDuration.setSizePolicy(sizePolicy3)
        self.lblDuration.setFont(font)

        self.horizontalLayout_5.addWidget(self.lblDuration)

        self.lblDurationValue = QLabel(self.frameInfos)
        self.lblDurationValue.setObjectName("lblDurationValue")
        sizePolicy4.setHeightForWidth(
            self.lblDurationValue.sizePolicy().hasHeightForWidth()
        )
        self.lblDurationValue.setSizePolicy(sizePolicy4)
        self.lblDurationValue.setFont(font1)
        self.lblDurationValue.setText("5 jours, 22 heures 52 minutes et 50 secondes")

        self.horizontalLayout_5.addWidget(self.lblDurationValue)

        self.verticalLayout_2.addWidget(self.frameInfos)

        self.frameTimeline = QFrame(self.frameTop)
        self.frameTimeline.setObjectName("frameTimeline")
        sizePolicy1.setHeightForWidth(
            self.frameTimeline.sizePolicy().hasHeightForWidth()
        )
        self.frameTimeline.setSizePolicy(sizePolicy1)
        self.verticalLayout_4 = QVBoxLayout(self.frameTimeline)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frameTimelineControls = QFrame(self.frameTimeline)
        self.frameTimelineControls.setObjectName("frameTimelineControls")
        sizePolicy3.setHeightForWidth(
            self.frameTimelineControls.sizePolicy().hasHeightForWidth()
        )
        self.frameTimelineControls.setSizePolicy(sizePolicy3)
        self.frameTimelineControls.setMinimumSize(QSize(40, 0))
        self.frameTimelineControls.setFrameShape(QFrame.StyledPanel)
        self.frameTimelineControls.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frameTimelineControls)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.btnZoomReset = QToolButton(self.frameTimelineControls)
        self.btnZoomReset.setObjectName("btnZoomReset")
        self.btnZoomReset.setMinimumSize(QSize(30, 30))
        self.btnZoomReset.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(
            ":/OpenIMU/icons/zoom_reset.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.btnZoomReset.setIcon(icon)
        self.btnZoomReset.setIconSize(QSize(24, 24))

        self.verticalLayout_6.addWidget(self.btnZoomReset, 0, Qt.AlignHCenter)

        self.btnTimeZoomSelection = QToolButton(self.frameTimelineControls)
        self.btnTimeZoomSelection.setObjectName("btnTimeZoomSelection")
        self.btnTimeZoomSelection.setMinimumSize(QSize(30, 30))
        self.btnTimeZoomSelection.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(
            ":/OpenIMU/icons/zoom_selection.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.btnTimeZoomSelection.setIcon(icon1)
        self.btnTimeZoomSelection.setIconSize(QSize(24, 24))

        self.verticalLayout_6.addWidget(self.btnTimeZoomSelection, 0, Qt.AlignHCenter)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_6.addItem(self.verticalSpacer)

        self.btnClearSelection = QToolButton(self.frameTimelineControls)
        self.btnClearSelection.setObjectName("btnClearSelection")
        self.btnClearSelection.setMinimumSize(QSize(30, 30))
        self.btnClearSelection.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(
            ":/OpenIMU/icons/selection_clear.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.btnClearSelection.setIcon(icon2)
        self.btnClearSelection.setIconSize(QSize(24, 24))

        self.verticalLayout_6.addWidget(self.btnClearSelection, 0, Qt.AlignHCenter)

        self.horizontalLayout_4.addWidget(self.frameTimelineControls)

        self.graphSensorsTimeline = QGraphicsView(self.frameTimeline)
        self.graphSensorsTimeline.setObjectName("graphSensorsTimeline")
        sizePolicy5 = QSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(
            self.graphSensorsTimeline.sizePolicy().hasHeightForWidth()
        )
        self.graphSensorsTimeline.setSizePolicy(sizePolicy5)
        self.graphSensorsTimeline.setMaximumSize(QSize(16777215, 16777215))
        self.graphSensorsTimeline.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphSensorsTimeline.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphSensorsTimeline.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop
        )
        self.graphSensorsTimeline.setCacheMode(QGraphicsView.CacheBackground)
        self.graphSensorsTimeline.setViewportUpdateMode(
            QGraphicsView.FullViewportUpdate
        )

        self.horizontalLayout_4.addWidget(self.graphSensorsTimeline)

        self.graphTimeline = TimeView(self.frameTimeline)
        self.graphTimeline.setObjectName("graphTimeline")
        sizePolicy.setHeightForWidth(
            self.graphTimeline.sizePolicy().hasHeightForWidth()
        )
        self.graphTimeline.setSizePolicy(sizePolicy)
        self.graphTimeline.setMaximumSize(QSize(16777215, 16777215))
        self.graphTimeline.viewport().setProperty(
            "cursor", QCursor(Qt.CursorShape.IBeamCursor)
        )
        self.graphTimeline.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphTimeline.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphTimeline.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.graphTimeline.setInteractive(True)
        self.graphTimeline.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.graphTimeline.setDragMode(QGraphicsView.RubberBandDrag)
        self.graphTimeline.setCacheMode(QGraphicsView.CacheBackground)
        self.graphTimeline.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.horizontalLayout_4.addWidget(self.graphTimeline)

        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(9, -1, -1, -1)
        self.frameScrollSpacer = QFrame(self.frameTimeline)
        self.frameScrollSpacer.setObjectName("frameScrollSpacer")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(
            self.frameScrollSpacer.sizePolicy().hasHeightForWidth()
        )
        self.frameScrollSpacer.setSizePolicy(sizePolicy6)
        self.frameScrollSpacer.setFrameShape(QFrame.StyledPanel)
        self.frameScrollSpacer.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frameScrollSpacer)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.horizontalLayout_6.addWidget(self.frameScrollSpacer)

        self.scrollTimeline = QScrollBar(self.frameTimeline)
        self.scrollTimeline.setObjectName("scrollTimeline")
        sizePolicy2.setHeightForWidth(
            self.scrollTimeline.sizePolicy().hasHeightForWidth()
        )
        self.scrollTimeline.setSizePolicy(sizePolicy2)
        self.scrollTimeline.setOrientation(Qt.Horizontal)

        self.horizontalLayout_6.addWidget(self.scrollTimeline)

        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.verticalLayout_2.addWidget(self.frameTimeline)

        self.frameCursor = QFrame(self.frameTop)
        self.frameCursor.setObjectName("frameCursor")
        sizePolicy2.setHeightForWidth(self.frameCursor.sizePolicy().hasHeightForWidth())
        self.frameCursor.setSizePolicy(sizePolicy2)
        self.frameCursor.setMinimumSize(QSize(0, 34))
        self.frameCursor.setMaximumSize(QSize(16777215, 34))
        self.horizontalLayout = QHBoxLayout(self.frameCursor)
        self.horizontalLayout.setSpacing(9)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(6, 2, 9, 2)
        self.horizontalSpacer_4 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.btnDisplayTimeline = QPushButton(self.frameCursor)
        self.btnDisplayTimeline.setObjectName("btnDisplayTimeline")
        self.btnDisplayTimeline.setMinimumSize(QSize(100, 30))
        self.btnDisplayTimeline.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(
            ":/OpenIMU/icons/show_hide.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btnDisplayTimeline.setIcon(icon3)
        self.btnDisplayTimeline.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.btnDisplayTimeline)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.lblCursorTime = QLabel(self.frameCursor)
        self.lblCursorTime.setObjectName("lblCursorTime")
        self.lblCursorTime.setFont(font1)
        self.lblCursorTime.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )

        self.horizontalLayout.addWidget(self.lblCursorTime)

        self.verticalLayout_2.addWidget(self.frameCursor, 0, Qt.AlignTop)

        self.verticalLayout_3.addWidget(self.frameTop, 0, Qt.AlignTop)

        self.frmSensors = QFrame(frmRecordsets)
        self.frmSensors.setObjectName("frmSensors")
        sizePolicy1.setHeightForWidth(self.frmSensors.sizePolicy().hasHeightForWidth())
        self.frmSensors.setSizePolicy(sizePolicy1)
        self.frmSensors.setFrameShape(QFrame.StyledPanel)
        self.frmSensors.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frmSensors)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.frameSensorsTools = QFrame(self.frmSensors)
        self.frameSensorsTools.setObjectName("frameSensorsTools")
        sizePolicy7 = QSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
        )
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(
            self.frameSensorsTools.sizePolicy().hasHeightForWidth()
        )
        self.frameSensorsTools.setSizePolicy(sizePolicy7)
        self.frameSensorsTools.setMinimumSize(QSize(40, 0))
        self.frameSensorsTools.setFrameShape(QFrame.StyledPanel)
        self.frameSensorsTools.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frameSensorsTools)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(3, 0, 3, 0)
        self.btnNewGraph = QToolButton(self.frameSensorsTools)
        self.btnNewGraph.setObjectName("btnNewGraph")
        self.btnNewGraph.setMinimumSize(QSize(30, 30))
        self.btnNewGraph.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon4 = QIcon()
        icon4.addFile(
            ":/OpenIMU/icons/graph.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btnNewGraph.setIcon(icon4)
        self.btnNewGraph.setIconSize(QSize(26, 26))
        self.btnNewGraph.setPopupMode(QToolButton.InstantPopup)

        self.verticalLayout.addWidget(self.btnNewGraph)

        self.btnTileHorizontal = QToolButton(self.frameSensorsTools)
        self.btnTileHorizontal.setObjectName("btnTileHorizontal")
        self.btnTileHorizontal.setMinimumSize(QSize(30, 30))
        self.btnTileHorizontal.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon5 = QIcon()
        icon5.addFile(
            ":/OpenIMU/icons/tile_horizontal.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.btnTileHorizontal.setIcon(icon5)
        self.btnTileHorizontal.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btnTileHorizontal)

        self.btnTileVertical = QToolButton(self.frameSensorsTools)
        self.btnTileVertical.setObjectName("btnTileVertical")
        self.btnTileVertical.setMinimumSize(QSize(30, 30))
        self.btnTileVertical.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon6 = QIcon()
        icon6.addFile(
            ":/OpenIMU/icons/tile_vertical.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.btnTileVertical.setIcon(icon6)
        self.btnTileVertical.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btnTileVertical)

        self.btnTileAuto = QToolButton(self.frameSensorsTools)
        self.btnTileAuto.setObjectName("btnTileAuto")
        self.btnTileAuto.setMinimumSize(QSize(30, 30))
        self.btnTileAuto.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon7 = QIcon()
        icon7.addFile(
            ":/OpenIMU/icons/tile_auto.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btnTileAuto.setIcon(icon7)
        self.btnTileAuto.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btnTileAuto)

        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout_7.addWidget(self.frameSensorsTools, 0, Qt.AlignHCenter)

        self.mdiArea = QMdiArea(self.frmSensors)
        self.mdiArea.setObjectName("mdiArea")
        sizePolicy8 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored
        )
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.mdiArea.sizePolicy().hasHeightForWidth())
        self.mdiArea.setSizePolicy(sizePolicy8)
        self.mdiArea.setStyleSheet("")
        brush = QBrush(QColor(99, 99, 99, 255))
        brush.setStyle(Qt.NoBrush)
        self.mdiArea.setBackground(brush)

        self.horizontalLayout_7.addWidget(self.mdiArea)

        self.verticalLayout_3.addWidget(self.frmSensors)

        self.retranslateUi(frmRecordsets)

        QMetaObject.connectSlotsByName(frmRecordsets)

    # setupUi

    def retranslateUi(self, frmRecordsets):
        frmRecordsets.setWindowTitle(
            QCoreApplication.translate("frmRecordsets", "Recordset display", None)
        )
        self.lblTotal.setText(
            QCoreApplication.translate("frmRecordsets", "Data range: ", None)
        )
        self.lblDuration.setText(
            QCoreApplication.translate("frmRecordsets", "Total time:", None)
        )
        # if QT_CONFIG(tooltip)
        self.btnZoomReset.setToolTip(
            QCoreApplication.translate("frmRecordsets", "Initial zoom", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.btnZoomReset.setText(
            QCoreApplication.translate("frmRecordsets", "...", None)
        )
        # if QT_CONFIG(tooltip)
        self.btnTimeZoomSelection.setToolTip(
            QCoreApplication.translate("frmRecordsets", "Zoom on selection", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.btnTimeZoomSelection.setText(
            QCoreApplication.translate("frmRecordsets", "...", None)
        )
        # if QT_CONFIG(tooltip)
        self.btnClearSelection.setToolTip(
            QCoreApplication.translate("frmRecordsets", "Clear selection", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.btnClearSelection.setText(
            QCoreApplication.translate("frmRecordsets", "...", None)
        )
        # if QT_CONFIG(tooltip)
        self.btnDisplayTimeline.setToolTip(
            QCoreApplication.translate(
                "frmRecordsets", "Show / hide temporal view", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btnDisplayTimeline.setText("")
        self.lblCursorTime.setText(
            QCoreApplication.translate("frmRecordsets", "Unknown date / time", None)
        )
        # if QT_CONFIG(tooltip)
        self.btnNewGraph.setToolTip(
            QCoreApplication.translate("frmRecordsets", "New graph", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.btnNewGraph.setText(
            QCoreApplication.translate("frmRecordsets", "...", None)
        )
        # if QT_CONFIG(tooltip)
        self.btnTileHorizontal.setToolTip(
            QCoreApplication.translate("frmRecordsets", "Tile horizontally", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.btnTileHorizontal.setText(
            QCoreApplication.translate("frmRecordsets", "...", None)
        )
        # if QT_CONFIG(tooltip)
        self.btnTileVertical.setToolTip(
            QCoreApplication.translate("frmRecordsets", "Tile vertically", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.btnTileVertical.setText(
            QCoreApplication.translate("frmRecordsets", "...", None)
        )
        # if QT_CONFIG(tooltip)
        self.btnTileAuto.setToolTip(
            QCoreApplication.translate("frmRecordsets", "Auto tile", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.btnTileAuto.setText(
            QCoreApplication.translate("frmRecordsets", "...", None)
        )

    # retranslateUi
