from resources.ui.python.StreamWindow_ui import Ui_StreamWindow

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QProgressBar, QListWidgetItem, QFileDialog
from PyQt5.QtGui import QBrush, QIcon, QColor

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
        self.UI.txtDataPath.setReadOnly(not state)
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
            self.streamer.transfer_started.connect(self.streaming_file_started)
            self.streamer.transfer_completed.connect(self.streaming_file_completed)
            self.streamer.device_connected.connect(self.device_connected)

    def exec(self):
        # Start server
        if self.streamer:
            self.streamer.start()
        else:
            self.add_to_log("Aucun serveur sélectionné!", LogTypes.LOGTYPE_ERROR)

        super().exec()

    @pyqtSlot('QString', int)
    def add_to_log(self, text: str, log_type: LogTypes):
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

    def add_file_progress_bar(self, filename: str):
        self.UI.tableFiles.setRowCount(self.UI.tableFiles.rowCount() + 1)
        index = self.UI.tableFiles.rowCount() - 1
        item = QTableWidgetItem(filename)
        self.file_rows[filename] = item
        item.setBackground(QBrush(Qt.white))
        self.UI.tableFiles.setItem(index, 1, item)
        prog = QProgressBar()
        prog.setAlignment(Qt.AlignCenter)
        self.UI.tableFiles.setCellWidget(index, 0, prog)
        self.update_current_transfer_tab()
        return index

    def update_current_transfer_tab(self):
        self.UI.tabInfos.setTabText(0, "Transferts en cours (" + str(self.UI.tableFiles.rowCount()) + ")")

    def remove_file_progress_bar(self, filename: str):
        self.UI.tableFiles.removeRow(self.UI.tableFiles.row(self.file_rows[filename]))
        self.file_rows[filename] = None
        self.update_current_transfer_tab()

    def add_file_completed(self, device_name: str, filename: str):
        self.UI.tableReceived.setRowCount(self.UI.tableReceived.rowCount() + 1)
        index = self.UI.tableReceived.rowCount() - 1
        item = QTableWidgetItem(device_name)
        item.setBackground(QBrush(Qt.white))
        self.UI.tableReceived.setItem(index, 0, item)
        item = QTableWidgetItem(filename)
        item.setBackground(QBrush(Qt.white))
        item.setForeground(QColor(Qt.darkGreen))
        self.UI.tableReceived.setItem(index, 1, item)

        self.UI.tabInfos.setTabText(1, "Fichiers reçus (" + str(self.UI.tableReceived.rowCount()) + ")")

    def add_file_error(self, filename: str, errorstr: str):
        self.UI.tableErrors.setRowCount(self.UI.tableErrors.rowCount() + 1)
        index = self.UI.tableErrors.rowCount() - 1
        item = QTableWidgetItem(filename)
        item.setBackground(QBrush(Qt.white))
        self.UI.tableErrors.setItem(index, 0, item)
        item = QTableWidgetItem(errorstr)
        item.setBackground(QBrush(Qt.white))
        item.setForeground(QColor(Qt.red))
        self.UI.tableErrors.setItem(index, 1, item)

        self.UI.tabInfos.setTabText(2, "Erreurs (" + str(self.UI.tableErrors.rowCount()) + ")")

    @pyqtSlot('QString', 'QString', int, int)
    def update_progress(self, filename: str, infos: str, value: int, max_value: int):
        # Update file table
        if filename in self.file_rows:
            index = self.UI.tableFiles.row(self.file_rows[filename])
        else:
            return

        if index >= 0:
            prog = self.UI.tableFiles.cellWidget(index, 0)
            if prog is not None:
                prog.setMaximum(max_value)
                prog.setValue(value)
                self.UI.tableFiles.scrollToBottom()
                self.UI.tableFiles.update()

        # QApplication.processEvents()

    @pyqtSlot('QString', 'QString', 'QString')
    def streaming_file_error(self, device_name: str, filename: str, error_str: str):
        # Remove file from current list
        self.remove_file_progress_bar(filename)

        # Add to completed list
        self.add_file_error(filename=filename, errorstr=error_str)

        # Update device list
        device_item = self.get_device_item(device_name=device_name, create_if_absent=False)
        if device_item:
            self.UI.lstDevices.takeItem(self.UI.lstDevices.row(device_item))
        self.add_to_log(filename + " - " + error_str, LogTypes.LOGTYPE_ERROR)

    def get_device_item(self, device_name: str, create_if_absent: bool) -> QListWidgetItem:
        device_item: QListWidgetItem = None
        for index in range(self.UI.lstDevices.count()):
            if self.UI.lstDevices.item(index).text() == device_name:
                device_item = self.UI.lstDevices.item(index)
                break

        if not device_item and create_if_absent:
            device_item = QListWidgetItem(device_name)
            device_item.setIcon(QIcon(":/OpenIMU/icons/sensor.png"))
            self.UI.lstDevices.addItem(device_item)

        return device_item

    @pyqtSlot('QString', bool)
    def device_connected(self, device_name: str, state: bool):
        if state:
            self.add_to_log(device_name + ": Connecté", LogTypes.LOGTYPE_INFO)
            # Find and adds the device into the connected device list
            self.get_device_item(device_name=device_name, create_if_absent=True)
        else:
            # Find and removes the device into the connected device list
            self.add_to_log(device_name + ": Déconnecté", LogTypes.LOGTYPE_INFO)

            device_item = self.get_device_item(device_name=device_name, create_if_absent=False)
            if device_item:
                self.UI.lstDevices.takeItem(self.UI.lstDevices.row(device_item))

    @pyqtSlot('QString', 'QString')
    def streaming_file_completed(self, device_name: str, file_name: str):
        # Remove file from current list
        self.remove_file_progress_bar(file_name)

        # Add to completed list
        self.add_file_completed(device_name=device_name, filename=file_name)

        # Update device list
        device_item = self.get_device_item(device_name=device_name, create_if_absent=False)
        if device_item:
            self.UI.lstDevices.takeItem(self.UI.lstDevices.row(device_item))

    @pyqtSlot('QString', 'QString')
    def streaming_file_started(self, device_name: str, file_name: str):
        self.add_file_progress_bar(file_name)
        self.get_device_item(device_name=device_name, create_if_absent=True)

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
