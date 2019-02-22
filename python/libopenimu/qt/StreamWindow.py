from resources.ui.python.StreamWindow_ui import Ui_StreamWindow

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QProgressBar, QApplication
from PyQt5.QtGui import QBrush

from libopenimu.streamers.streamer_types import StreamerTypes
from libopenimu.streamers.AppleWatchStreamer import AppleWatchStreamer

from libopenimu.models.LogTypes import LogTypes

from datetime import datetime


class StreamWindow(QDialog):

    streamer = None
    stream_path = ""
    file_rows = {}

    def __init__(self, stream_type, path, parent=None):
        super().__init__(parent=parent)
        self.UI = Ui_StreamWindow()
        self.UI.setupUi(self)
        self.setWindowFlags(Qt.WindowTitleHint)

        self.stream_path = path
        if stream_type == StreamerTypes.APPLEWATCH:
            self.streamer = AppleWatchStreamer(path=self.stream_path, parent=self)

        if self.streamer:
            self.streamer.add_log.connect(self.add_to_log)
            self.streamer.update_progress.connect(self.update_progress)
            self.streamer.finished.connect(self.streaming_server_finished)

        # Initial UI state
        self.UI.frameProgress.hide()
        infos = self.streamer.get_streamer_infos()
        row = 0
        self.UI.tableInfos.setRowCount(len(infos))
        for info_item, info_value in infos.items():
            item = QTableWidgetItem(info_item)
            item.setBackground(QBrush(Qt.lightGray))
            self.UI.tableInfos.setItem(row, 0, item)
            item = QTableWidgetItem(info_value)
            item.setBackground(QBrush(Qt.white))
            item.setForeground(QBrush(Qt.blue))
            self.UI.tableInfos.setItem(row, 1, item)
            row += 1

        # Signals / slots connection
        self.UI.btnClose.clicked.connect(self.close_requested)

    def exec(self):
        # Start server
        if self.streamer:
            self.streamer.start()
        else:
            self.add_to_log("Aucun serveur sélectionné!", LogTypes.LOGTYPE_ERROR)

        super().exec()

    @pyqtSlot('QString', int)
    def add_to_log(self, text, log_type):
        if text == ' ' or text == '\n':
            return

        log_format = ""
        if log_type == LogTypes.LOGTYPE_INFO:
            log_format = "<span style='color:black'>"
        if log_type == LogTypes.LOGTYPE_WARNING:
            log_format = "<span style='color:orange;font-style:italic'>"
        if log_type == LogTypes.LOGTYPE_ERROR:
            log_format = "<span style='color:red;font-weight:bold'>"
        if log_type == LogTypes.LOGTYPE_DEBUG:
            log_format = "<span style='color:grey;font-style:italic'>"
        if log_type == LogTypes.LOGTYPE_DONE:
            log_format = "<span style='color:green;font-weight:bold'>"

        self.UI.txtLog.append("<span style='color:grey'>" + datetime.now().strftime(
            "%H:%M:%S.%f") + " </span>" + log_format + text + "</span>")
        self.UI.txtLog.ensureCursorVisible()

    @pyqtSlot('QString', 'QString', int, int)
    def update_progress(self, filename, infos, value, max_value):
        # Ne need to display the progress bar anymore
        if value >= max_value:
            self.UI.frameProgress.hide()

        self.UI.lblProgress.setText(filename + " " + infos)
        if max_value != self.UI.prgTotal.maximum():
            self.UI.prgTotal.setMaximum(max_value)
        self.UI.prgTotal.setValue(value)
        self.UI.frameProgress.show()

        # Update file table
        if filename in self.file_rows:
            index = self.file_rows[filename]
        else:
            self.UI.tableFiles.setRowCount(self.UI.tableFiles.rowCount()+1)
            index = self.UI.tableFiles.rowCount()-1
            self.file_rows[filename] = index
            item = QTableWidgetItem(filename)
            item.setBackground(QBrush(Qt.white))
            self.UI.tableFiles.setItem(index, 1, item)
            prog = QProgressBar()
            prog.setAlignment(Qt.AlignCenter)
            self.UI.tableFiles.setCellWidget(index, 0, prog)

        if index >= 0:
            prog = self.UI.tableFiles.cellWidget(index, 0)
            if prog is not None:
                prog.setMaximum(max_value)
                prog.setValue(value)
                self.UI.tableFiles.scrollToBottom()
                self.UI.tableFiles.update()

        QApplication.processEvents()

    @pyqtSlot()
    def close_requested(self):
        if self.streamer:
            self.streamer.stop_server()
        else:
            self.accept()

    @pyqtSlot()
    def streaming_server_finished(self):
        self.accept()
