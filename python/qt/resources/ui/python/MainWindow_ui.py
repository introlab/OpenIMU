# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
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
    QAction,
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
    QAbstractItemView,
    QApplication,
    QDockWidget,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QSizePolicy,
    QSpacerItem,
    QTextEdit,
    QToolButton,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from qt.TreeDataWidget import TreeDataWidget
import core_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1119, 593)
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setAcceptDrops(True)
        MainWindow.setWindowTitle("OpenIMU")
        icon = QIcon()
        icon.addFile(
            ":/OpenIMU/icons/OpenIMU.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        MainWindow.setWindowIcon(icon)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.frmMain = QWidget(MainWindow)
        self.frmMain.setObjectName("frmMain")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frmMain.sizePolicy().hasHeightForWidth())
        self.frmMain.setSizePolicy(sizePolicy1)
        self.horizontalLayout = QHBoxLayout(self.frmMain)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        MainWindow.setCentralWidget(self.frmMain)
        self.dockDataset = QDockWidget(MainWindow)
        self.dockDataset.setObjectName("dockDataset")
        sizePolicy2 = QSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum
        )
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.dockDataset.sizePolicy().hasHeightForWidth())
        self.dockDataset.setSizePolicy(sizePolicy2)
        self.dockDataset.setMinimumSize(QSize(280, 182))
        self.dockDataset.setFloating(False)
        self.dockDataset.setFeatures(QDockWidget.DockWidgetClosable)
        self.dockDataset.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.dockWidgetTreeContents = QWidget()
        self.dockWidgetTreeContents.setObjectName("dockWidgetTreeContents")
        sizePolicy1.setHeightForWidth(
            self.dockWidgetTreeContents.sizePolicy().hasHeightForWidth()
        )
        self.dockWidgetTreeContents.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.dockWidgetTreeContents)
        self.verticalLayout_2.setSpacing(1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.treeDataSet = TreeDataWidget(self.dockWidgetTreeContents)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, "1")
        self.treeDataSet.setHeaderItem(__qtreewidgetitem)
        self.treeDataSet.setObjectName("treeDataSet")
        sizePolicy3 = QSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.treeDataSet.sizePolicy().hasHeightForWidth())
        self.treeDataSet.setSizePolicy(sizePolicy3)
        self.treeDataSet.setEditTriggers(
            QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed
        )
        self.treeDataSet.setProperty("showDropIndicator", True)
        self.treeDataSet.setDragEnabled(True)
        self.treeDataSet.setDragDropMode(QAbstractItemView.DragDrop)
        self.treeDataSet.setDefaultDropAction(Qt.IgnoreAction)
        self.treeDataSet.setAlternatingRowColors(False)
        self.treeDataSet.setIconSize(QSize(24, 24))
        self.treeDataSet.setIndentation(20)
        self.treeDataSet.setUniformRowHeights(False)
        self.treeDataSet.setAnimated(True)
        self.treeDataSet.setExpandsOnDoubleClick(False)
        self.treeDataSet.header().setVisible(False)

        self.verticalLayout_2.addWidget(self.treeDataSet)

        self.frameButtons = QFrame(self.dockWidgetTreeContents)
        self.frameButtons.setObjectName("frameButtons")
        sizePolicy4 = QSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Maximum
        )
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(
            self.frameButtons.sizePolicy().hasHeightForWidth()
        )
        self.frameButtons.setSizePolicy(sizePolicy4)
        self.horizontalLayout_3 = QHBoxLayout(self.frameButtons)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnAddGroup = QToolButton(self.frameButtons)
        self.btnAddGroup.setObjectName("btnAddGroup")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.btnAddGroup.sizePolicy().hasHeightForWidth())
        self.btnAddGroup.setSizePolicy(sizePolicy5)
        self.btnAddGroup.setMinimumSize(QSize(40, 40))
        self.btnAddGroup.setMaximumSize(QSize(40, 40))
        self.btnAddGroup.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(
            ":/OpenIMU/icons/group_new.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btnAddGroup.setIcon(icon1)
        self.btnAddGroup.setIconSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.btnAddGroup)

        self.btnAddParticipant = QToolButton(self.frameButtons)
        self.btnAddParticipant.setObjectName("btnAddParticipant")
        sizePolicy5.setHeightForWidth(
            self.btnAddParticipant.sizePolicy().hasHeightForWidth()
        )
        self.btnAddParticipant.setSizePolicy(sizePolicy5)
        self.btnAddParticipant.setMinimumSize(QSize(40, 40))
        self.btnAddParticipant.setMaximumSize(QSize(40, 40))
        self.btnAddParticipant.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(
            ":/OpenIMU/icons/participant_new.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.btnAddParticipant.setIcon(icon2)
        self.btnAddParticipant.setIconSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.btnAddParticipant)

        self.horizontalSpacer_2 = QSpacerItem(
            10, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.btnRename = QToolButton(self.frameButtons)
        self.btnRename.setObjectName("btnRename")
        self.btnRename.setEnabled(False)
        self.btnRename.setMinimumSize(QSize(40, 40))
        self.btnRename.setMaximumSize(QSize(40, 40))
        self.btnRename.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(
            ":/OpenIMU/icons/save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btnRename.setIcon(icon3)
        self.btnRename.setIconSize(QSize(28, 28))

        self.horizontalLayout_3.addWidget(self.btnRename)

        self.btnDelete = QToolButton(self.frameButtons)
        self.btnDelete.setObjectName("btnDelete")
        self.btnDelete.setEnabled(False)
        self.btnDelete.setMinimumSize(QSize(40, 40))
        self.btnDelete.setMaximumSize(QSize(40, 40))
        self.btnDelete.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon4 = QIcon()
        icon4.addFile(
            ":/OpenIMU/icons/delete.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btnDelete.setIcon(icon4)
        self.btnDelete.setIconSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.btnDelete)

        self.verticalLayout_2.addWidget(self.frameButtons)

        self.dockDataset.setWidget(self.dockWidgetTreeContents)
        MainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockDataset)
        self.dockLog = QDockWidget(MainWindow)
        self.dockLog.setObjectName("dockLog")
        sizePolicy6 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum
        )
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.dockLog.sizePolicy().hasHeightForWidth())
        self.dockLog.setSizePolicy(sizePolicy6)
        self.dockLog.setMinimumSize(QSize(102, 230))
        self.dockWidgetLogContents = QWidget()
        self.dockWidgetLogContents.setObjectName("dockWidgetLogContents")
        self.verticalLayout_3 = QVBoxLayout(self.dockWidgetLogContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.txtLog = QTextEdit(self.dockWidgetLogContents)
        self.txtLog.setObjectName("txtLog")
        sizePolicy7 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding
        )
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.txtLog.sizePolicy().hasHeightForWidth())
        self.txtLog.setSizePolicy(sizePolicy7)

        self.verticalLayout_3.addWidget(self.txtLog)

        self.dockLog.setWidget(self.dockWidgetLogContents)
        MainWindow.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.dockLog)
        self.dockToolBar = QDockWidget(MainWindow)
        self.dockToolBar.setObjectName("dockToolBar")
        sizePolicy8 = QSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred
        )
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.dockToolBar.sizePolicy().hasHeightForWidth())
        self.dockToolBar.setSizePolicy(sizePolicy8)
        self.dockToolBar.setMinimumSize(QSize(1119, 50))
        self.dockToolBar.setMaximumSize(QSize(524287, 50))
        self.dockToolBar.setStyleSheet(
            "QDockWidget::title{background-color:rgba(0,0,0,0%);}"
        )
        self.dockToolBar.setFloating(False)
        self.dockToolBar.setFeatures(QDockWidget.DockWidgetVerticalTitleBar)
        self.dockToolBar.setAllowedAreas(Qt.TopDockWidgetArea)
        self.dockWidgetToolsContents = QWidget()
        self.dockWidgetToolsContents.setObjectName("dockWidgetToolsContents")
        sizePolicy9 = QSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding
        )
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(
            self.dockWidgetToolsContents.sizePolicy().hasHeightForWidth()
        )
        self.dockWidgetToolsContents.setSizePolicy(sizePolicy9)
        self.horizontalLayout_2 = QHBoxLayout(self.dockWidgetToolsContents)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(10, 0, 6, 0)
        self.lblLogo = QLabel(self.dockWidgetToolsContents)
        self.lblLogo.setObjectName("lblLogo")
        self.lblLogo.setMaximumSize(QSize(60, 40))
        self.lblLogo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.lblLogo.setPixmap(QPixmap(":/OpenIMU/LogoOpenIMU.png"))
        self.lblLogo.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.lblLogo)

        self.line_4 = QFrame(self.dockWidgetToolsContents)
        self.line_4.setObjectName("line_4")
        self.line_4.setFrameShape(QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_2.addWidget(self.line_4)

        self.btnShowDataset = QToolButton(self.dockWidgetToolsContents)
        self.btnShowDataset.setObjectName("btnShowDataset")
        sizePolicy10 = QSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed
        )
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(
            self.btnShowDataset.sizePolicy().hasHeightForWidth()
        )
        self.btnShowDataset.setSizePolicy(sizePolicy10)
        self.btnShowDataset.setMinimumSize(QSize(0, 40))
        self.btnShowDataset.setMaximumSize(QSize(45, 16777215))
        self.btnShowDataset.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon5 = QIcon()
        icon5.addFile(
            ":/OpenIMU/icons/tree.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btnShowDataset.setIcon(icon5)
        self.btnShowDataset.setIconSize(QSize(32, 32))
        self.btnShowDataset.setCheckable(True)
        self.btnShowDataset.setChecked(True)
        self.btnShowDataset.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.btnShowDataset.setAutoRaise(False)
        self.btnShowDataset.setArrowType(Qt.NoArrow)

        self.horizontalLayout_2.addWidget(self.btnShowDataset)

        self.btnShowLog = QToolButton(self.dockWidgetToolsContents)
        self.btnShowLog.setObjectName("btnShowLog")
        sizePolicy10.setHeightForWidth(self.btnShowLog.sizePolicy().hasHeightForWidth())
        self.btnShowLog.setSizePolicy(sizePolicy10)
        self.btnShowLog.setMinimumSize(QSize(0, 40))
        self.btnShowLog.setMaximumSize(QSize(45, 16777215))
        self.btnShowLog.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon6 = QIcon()
        icon6.addFile(
            ":/OpenIMU/icons/log.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btnShowLog.setIcon(icon6)
        self.btnShowLog.setIconSize(QSize(32, 32))
        self.btnShowLog.setCheckable(True)
        self.btnShowLog.setChecked(False)

        self.horizontalLayout_2.addWidget(self.btnShowLog)

        self.line_3 = QFrame(self.dockWidgetToolsContents)
        self.line_3.setObjectName("line_3")
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.line_3.setFrameShape(QFrame.Shape.VLine)

        self.horizontalLayout_2.addWidget(self.line_3)

        self.btnImport = QToolButton(self.dockWidgetToolsContents)
        self.btnImport.setObjectName("btnImport")
        self.btnImport.setMinimumSize(QSize(100, 40))
        font = QFont()
        font.setPointSize(10)
        self.btnImport.setFont(font)
        self.btnImport.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon7 = QIcon()
        icon7.addFile(
            ":/OpenIMU/icons/import.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btnImport.setIcon(icon7)
        self.btnImport.setIconSize(QSize(24, 24))
        self.btnImport.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.btnImport)

        self.btnTransfer = QToolButton(self.dockWidgetToolsContents)
        self.btnTransfer.setObjectName("btnTransfer")
        self.btnTransfer.setMinimumSize(QSize(100, 40))
        self.btnTransfer.setFont(font)
        self.btnTransfer.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnTransfer.setMouseTracking(True)
        icon8 = QIcon()
        icon8.addFile(
            ":/OpenIMU/icons/transfer.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btnTransfer.setIcon(icon8)
        self.btnTransfer.setIconSize(QSize(24, 24))
        self.btnTransfer.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.btnTransfer)

        self.line = QFrame(self.dockWidgetToolsContents)
        self.line.setObjectName("line")
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setMidLineWidth(0)
        self.line.setFrameShape(QFrame.Shape.VLine)

        self.horizontalLayout_2.addWidget(self.line)

        self.btnProcess = QToolButton(self.dockWidgetToolsContents)
        self.btnProcess.setObjectName("btnProcess")
        self.btnProcess.setEnabled(True)
        self.btnProcess.setMinimumSize(QSize(100, 40))
        self.btnProcess.setFont(font)
        self.btnProcess.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon9 = QIcon()
        icon9.addFile(
            ":/OpenIMU/icons/result.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btnProcess.setIcon(icon9)
        self.btnProcess.setIconSize(QSize(24, 24))
        self.btnProcess.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.btnProcess)

        self.btnExportCSV = QToolButton(self.dockWidgetToolsContents)
        self.btnExportCSV.setObjectName("btnExportCSV")
        sizePolicy5.setHeightForWidth(
            self.btnExportCSV.sizePolicy().hasHeightForWidth()
        )
        self.btnExportCSV.setSizePolicy(sizePolicy5)
        self.btnExportCSV.setMinimumSize(QSize(100, 40))
        self.btnExportCSV.setFont(font)
        self.btnExportCSV.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon10 = QIcon()
        icon10.addFile(
            ":/OpenIMU/icons/export.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btnExportCSV.setIcon(icon10)
        self.btnExportCSV.setIconSize(QSize(24, 24))
        self.btnExportCSV.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.btnExportCSV.setAutoRaise(False)
        self.btnExportCSV.setArrowType(Qt.NoArrow)

        self.horizontalLayout_2.addWidget(self.btnExportCSV)

        self.line_2 = QFrame(self.dockWidgetToolsContents)
        self.line_2.setObjectName("line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_2.addWidget(self.line_2)

        self.btnCompact = QToolButton(self.dockWidgetToolsContents)
        self.btnCompact.setObjectName("btnCompact")
        self.btnCompact.setMinimumSize(QSize(110, 40))
        self.btnCompact.setFont(font)
        self.btnCompact.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon11 = QIcon()
        icon11.addFile(
            ":/OpenIMU/icons/compact.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btnCompact.setIcon(icon11)
        self.btnCompact.setIconSize(QSize(24, 24))
        self.btnCompact.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.btnCompact)

        self.btnDataSetInfos = QToolButton(self.dockWidgetToolsContents)
        self.btnDataSetInfos.setObjectName("btnDataSetInfos")
        self.btnDataSetInfos.setMinimumSize(QSize(110, 40))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.btnDataSetInfos.setFont(font1)
        self.btnDataSetInfos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon12 = QIcon()
        icon12.addFile(
            ":/OpenIMU/icons/info.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btnDataSetInfos.setIcon(icon12)
        self.btnDataSetInfos.setIconSize(QSize(24, 24))
        self.btnDataSetInfos.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.btnDataSetInfos)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btnClose = QToolButton(self.dockWidgetToolsContents)
        self.btnClose.setObjectName("btnClose")
        self.btnClose.setEnabled(True)
        self.btnClose.setMinimumSize(QSize(75, 40))
        self.btnClose.setMaximumSize(QSize(16777215, 16777215))
        self.btnClose.setFont(font)
        self.btnClose.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnClose.setIcon(icon4)
        self.btnClose.setIconSize(QSize(24, 24))
        self.btnClose.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.btnClose)

        self.dockToolBar.setWidget(self.dockWidgetToolsContents)
        MainWindow.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.dockToolBar)
        self.dockToolBar.raise_()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", "Quit", None))
        self.dockDataset.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Data structure", None)
        )
        # if QT_CONFIG(tooltip)
        self.btnAddGroup.setToolTip(
            QCoreApplication.translate("MainWindow", "New group", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.btnAddGroup.setText("")
        # if QT_CONFIG(tooltip)
        self.btnAddParticipant.setToolTip(
            QCoreApplication.translate("MainWindow", "New participant", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.btnAddParticipant.setText("")
        # if QT_CONFIG(tooltip)
        self.btnRename.setToolTip(
            QCoreApplication.translate("MainWindow", "Rename", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.btnRename.setText("")
        # if QT_CONFIG(tooltip)
        self.btnDelete.setToolTip(
            QCoreApplication.translate("MainWindow", "Delete", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.btnDelete.setText("")
        self.dockLog.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Logs", None)
        )
        self.dockToolBar.setWindowTitle("")
        self.lblLogo.setText("")
        # if QT_CONFIG(tooltip)
        self.btnShowDataset.setToolTip(
            QCoreApplication.translate("MainWindow", "Data structure", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.btnShowDataset.setText("")
        # if QT_CONFIG(tooltip)
        self.btnShowLog.setToolTip(
            QCoreApplication.translate("MainWindow", "Logs", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.btnShowLog.setText("")
        # if QT_CONFIG(tooltip)
        self.btnImport.setToolTip(
            QCoreApplication.translate(
                "MainWindow", "Import new data into this database", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btnImport.setText(QCoreApplication.translate("MainWindow", "Import", None))
        # if QT_CONFIG(tooltip)
        self.btnTransfer.setToolTip(
            QCoreApplication.translate(
                "MainWindow", "Transfer data from a device", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btnTransfer.setText(
            QCoreApplication.translate("MainWindow", "Transfer from device", None)
        )
        # if QT_CONFIG(tooltip)
        self.btnProcess.setToolTip(
            QCoreApplication.translate(
                "MainWindow", "Process data with available algorithms", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btnProcess.setText(
            QCoreApplication.translate("MainWindow", "Process", None)
        )
        # if QT_CONFIG(tooltip)
        self.btnExportCSV.setToolTip(
            QCoreApplication.translate(
                "MainWindow", "Export data to external formats", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btnExportCSV.setText(
            QCoreApplication.translate("MainWindow", "Export", None)
        )
        # if QT_CONFIG(tooltip)
        self.btnCompact.setToolTip(
            QCoreApplication.translate(
                "MainWindow", "Compact and optimize database structure", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btnCompact.setText(
            QCoreApplication.translate("MainWindow", "Compact", None)
        )
        # if QT_CONFIG(tooltip)
        self.btnDataSetInfos.setToolTip(
            QCoreApplication.translate("MainWindow", "Database information", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.btnDataSetInfos.setText(
            QCoreApplication.translate("MainWindow", "Informations", None)
        )
        # if QT_CONFIG(tooltip)
        self.btnClose.setToolTip(
            QCoreApplication.translate("MainWindow", "Close the current dataset", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.btnClose.setText(QCoreApplication.translate("MainWindow", "Close", None))
        pass

    # retranslateUi
