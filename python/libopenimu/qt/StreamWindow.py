from resources.ui.python.StreamWindow_ui import Ui_StreamWindow

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QProgressBar, QApplication, QFileDialog
from PyQt5.QtGui import QBrush

# from libopenimu.streamers.streamer_types import StreamerTypes
from libopenimu.streamers.AppleWatchStreamer import AppleWatchStreamer

from libopenimu.models.LogTypes import LogTypes

from datetime import datetime


class StreamWindow(QDialog):

    streamer = None
    stream_path = ""
    file_rows = {}
    folders_to_import = []

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.UI = Ui_StreamWindow()
        self.UI.setupUi(self)
        # self.setWindowFlags(Qt.WindowTitleHint)

        self.load_settings()
        self.init_streamer()
        self.set_edit_state(False)

        # Initial UI state
        self.UI.frameProgress.hide()
        # infos = self.streamer.get_streamer_infos()
        # row = 0
        # self.UI.tableInfos.setRowCount(len(infos))
        # for info_item, info_value in infos.items():
        #     item = QTableWidgetItem(info_item)
        #     item.setBackground(QBrush(Qt.lightGray))
        #     self.UI.tableInfos.setItem(row, 0, item)
        #     item = QTableWidgetItem(info_value)
        #     item.setBackground(QBrush(Qt.white))
        #     item.setForeground(QBrush(Qt.blue))
        #     self.UI.tableInfos.setItem(row, 1, item)
        #     row += 1

        # Signals / slots connection
        self.UI.btnClose.clicked.connect(self.close_requested)
        self.UI.btnEdit.clicked.connect(self.edit_requested)
        self.UI.btnBrowse.clicked.connect(self.browse_requested)

    @pyqtSlot()
    def browse_requested(self):
        file = QFileDialog().getExistingDirectory(caption="Sélectionnez le répertoire de destination")

        if len(file) > 0:
            self.UI.txtDataPath.setText(file)

    @pyqtSlot()
    def edit_requested(self):
        # self.UI.frameInfos.setEnabled(self.UI.btnEdit.isChecked())
        self.set_edit_state(self.UI.btnEdit.isChecked())

        if not self.UI.btnEdit.isChecked():
            # Save settings for further use
            self.save_settings()
            # Server settings changed - reinitialize!
            if self.streamer:
                self.streamer.stop_server()
                self.init_streamer()
                self.streamer.start()

    def set_edit_state(self, state: bool):
        self.UI.txtDataPath.setEnabled(state)
        self.UI.spinPort.setEnabled(state)
        self.UI.chkAutoImport.setEnabled(state)
        self.UI.chkDeleteFiles.setEnabled(state)
        self.UI.btnBrowse.setEnabled(state)

    def load_settings(self):
        from libopenimu.tools.Settings import OpenIMUSettings
        settings = OpenIMUSettings()
        self.UI.txtDataPath.setText(settings.data_save_path)
        self.UI.spinPort.setValue(settings.streamer_port)

    def save_settings(self):
        from libopenimu.tools.Settings import OpenIMUSettings
        settings = OpenIMUSettings()
        settings.streamer_port = self.UI.spinPort.value()
        settings.data_save_path = self.UI.txtDataPath.text()

    def init_streamer(self):
        if self.UI.cmbStreamType.currentIndex() == 0:  # Applewatch
            self.streamer = AppleWatchStreamer(port=self.UI.spinPort.value(), path=self.UI.txtDataPath.text(),
                                               parent=self)

        if self.streamer:
            self.UI.lblIPValue.setText(self.streamer.get_local_ip_address())
            self.streamer.add_log.connect(self.add_to_log)
            self.streamer.update_progress.connect(self.update_progress)
            self.streamer.finished.connect(self.streaming_server_finished)
            self.streamer.file_error_occured.connect(self.streaming_file_error)

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
        self.UI.txtLog.verticalScrollBar().setValue(self.UI.txtLog.verticalScrollBar().maximum())
        # self.UI.txtLog.ensureCursorVisible()

    def add_file_progress_bar(self, filename):
        self.UI.tableFiles.setRowCount(self.UI.tableFiles.rowCount() + 1)
        index = self.UI.tableFiles.rowCount() - 1
        self.file_rows[filename] = index
        item = QTableWidgetItem(filename)
        item.setBackground(QBrush(Qt.white))
        self.UI.tableFiles.setItem(index, 1, item)
        prog = QProgressBar()
        prog.setAlignment(Qt.AlignCenter)

        self.UI.tableFiles.setCellWidget(index, 0, prog)

        return index

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
            index = self.add_file_progress_bar(filename)

        if index >= 0:
            prog = self.UI.tableFiles.cellWidget(index, 0)
            if prog is not None:
                prog.setMaximum(max_value)
                prog.setValue(value)
                self.UI.tableFiles.scrollToBottom()
                self.UI.tableFiles.update()

        QApplication.processEvents()

    @pyqtSlot('QString', 'QString')
    def streaming_file_error(self, filename, error_str):
        # Update file table
        if filename in self.file_rows:
            index = self.file_rows[filename]
        else:
            index = self.add_file_progress_bar(filename)

        if index >= 0:
            prog = self.UI.tableFiles.cellWidget(index, 0)
            if prog is not None:
                prog.setStyleSheet("QProgressBar::chunk{background-color:qlineargradient(spread:reflect, x1:0.5, y1:0, "
                                   "x2:0.5, y2:0.5, stop:0 rgba(117, 0, 0, 255), stop:1 rgba(255, 153, 153, 255));}")

    def get_data_save_path(self) -> str:
        return self.UI.txtDataPath.text()

    def get_streamer_type(self) -> int:
        return self.UI.cmbStreamType.currentIndex()

    def closeEvent(self, _):
        self.close_requested()

    @pyqtSlot()
    def close_requested(self):
        if self.streamer:
            self.streamer.stop_server()

        # Build list of root folders to import
        import os
        self.folders_to_import = os.listdir(self.UI.txtDataPath.text())

        self.accept()

    @pyqtSlot()
    def streaming_server_finished(self):
        # self.accept()
        pass
