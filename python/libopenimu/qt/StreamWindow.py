from resources.ui.python.StreamWindow_ui import Ui_StreamWindow

from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QDialog, QTableWidgetItem, QProgressBar, QListWidgetItem, QFileDialog
from PySide6.QtGui import QBrush, QIcon, QColor

# from libopenimu.streamers.streamer_types import StreamerTypes
from libopenimu.streamers.AppleWatchStreamer import AppleWatchStreamer

from libopenimu.models.LogTypes import LogTypes

from libopenimu.tools.FileManager import FileManager

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
        self.UI.chkAutoImport.hide()  # For now...

        # Signals / slots connection
        self.UI.btnClose.clicked.connect(self.close_requested)
        self.UI.btnEdit.clicked.connect(self.edit_requested)
        self.UI.btnBrowse.clicked.connect(self.browse_requested)
        self.UI.btnSave.clicked.connect(self.save_requested)
        self.UI.btnCancel.clicked.connect(self.undo_requested)

    @Slot(name='browse_requested')
    def browse_requested(self):
        file = QFileDialog().getExistingDirectory(caption="Sélectionnez le répertoire de destination")

        if len(file) > 0:
            self.UI.txtDataPath.setText(file)

    @Slot(name='edit_requested')
    def edit_requested(self):
        from PySide6.QtWidgets import QMessageBox
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setStyleSheet("QPushButton{min-width: 100px; min-height: 40px;}")

        msg.setText("Le serveur sera arrêté pour l'édition et les transferts en cours seront arrêtés.\n"
                    "Voulez-vous continuer?")
        msg.setWindowTitle("Éditer")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        rval = msg.exec()
        if rval == QMessageBox.Yes:
            # self.UI.frameInfos.setEnabled(self.UI.btnEdit.isChecked())
            if self.streamer:
                self.streamer.stop_server()
            self.set_edit_state(True)

    @Slot(name='save_requested')
    def save_requested(self):
        self.set_edit_state(False)
        # Save settings for further use
        self.save_settings()
        # Server settings changed - reinitialize!
        if self.streamer:
            self.init_streamer()
            self.streamer.start()

    @Slot(name='undo_requested')
    def undo_requested(self):
        self.set_edit_state(False)
        self.load_settings()
        # Restart server
        if self.streamer:
            self.streamer.start()

    def set_edit_state(self, state: bool):
        self.UI.txtDataPath.setReadOnly(not state)
        self.UI.spinPort.setEnabled(state)
        self.UI.chkAutoImport.setEnabled(state)
        self.UI.chkDeleteFiles.setEnabled(state)
        self.UI.btnBrowse.setEnabled(state)
        self.UI.btnEdit.setDisabled(state)
        self.UI.frameEdit.setVisible(state)

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
        # Create path with subfolder "ToImport"
        save_path = self.get_data_save_path()

        # Clear all received file list and update with "real" files
        self.UI.tableReceived.clearContents()
        self.UI.tableReceived.setRowCount(0)

        for file in FileManager.get_file_list(from_path=save_path):
            import os
            device_name = 'Inconnu'
            filename = file[len(self.get_data_save_path())+1:]
            path_parts = filename.split(os.sep)
            if len(path_parts) > 1:
                device_name = path_parts[0]
            file_size = os.path.getsize(file)
            self.add_file_completed(device_name=device_name, filename=filename, filesize=file_size)

        if self.UI.cmbStreamType.currentIndex() == 0:  # Applewatch
            self.streamer = AppleWatchStreamer(port=self.UI.spinPort.value(), path=save_path,
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

    @Slot('QString', int, name='add_to_log')
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

    def add_file_progress_bar(self, filename: str, filesize: int):
        self.UI.tableFiles.setRowCount(self.UI.tableFiles.rowCount() + 1)
        index = self.UI.tableFiles.rowCount() - 1

        prog = QProgressBar()
        prog.setAlignment(Qt.AlignCenter)
        self.UI.tableFiles.setCellWidget(index, 0, prog)

        item = QTableWidgetItem(FileManager.format_file_size(filesize))
        item.setBackground(QBrush(Qt.white))
        item.setTextAlignment(Qt.AlignCenter)
        self.UI.tableFiles.setItem(index, 1, item)

        item = QTableWidgetItem(filename)
        self.file_rows[filename] = item
        item.setBackground(QBrush(Qt.white))
        self.UI.tableFiles.setItem(index, 2, item)

        self.update_current_transfer_tab()
        return index

    def update_current_transfer_tab(self):
        self.UI.tabInfos.setTabText(0, "Transferts en cours (" + str(self.UI.tableFiles.rowCount()) + ")")

    def remove_file_progress_bar(self, filename: str):
        self.UI.tableFiles.removeRow(self.UI.tableFiles.row(self.file_rows[filename]))
        self.file_rows[filename] = None
        self.update_current_transfer_tab()

    def add_file_completed(self, device_name: str, filename: str, filesize: int):
        # Check if file is already present
        if len(self.UI.tableReceived.findItems(filename, Qt.MatchExactly)) > 0:
            return

        self.UI.tableReceived.setRowCount(self.UI.tableReceived.rowCount() + 1)
        index = self.UI.tableReceived.rowCount() - 1

        item = QTableWidgetItem(device_name)
        item.setBackground(QBrush(Qt.white))
        self.UI.tableReceived.setItem(index, 0, item)

        item = QTableWidgetItem(FileManager.format_file_size(filesize))
        item.setBackground(QBrush(Qt.white))
        item.setTextAlignment(Qt.AlignCenter)
        self.UI.tableReceived.setItem(index, 1, item)

        item = QTableWidgetItem(filename)
        item.setBackground(QBrush(Qt.white))
        item.setForeground(QColor(Qt.darkGreen))
        self.UI.tableReceived.setItem(index, 2, item)

        self.UI.tabInfos.setTabText(1, "Fichiers reçus (" + str(self.UI.tableReceived.rowCount()) + ")")
        self.UI.tableReceived.scrollToBottom()

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

    @Slot('QString', 'QString', int, int, name='update_progress')
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
                # self.UI.tableFiles.update(index)

            size_cell = self.UI.tableFiles.item(index, 1)
            size_cell.setText(FileManager.format_file_size(file_size=value, no_suffix=True, ref_size=max_value) + " / "
                              + FileManager.format_file_size(file_size=max_value))

        # QApplication.processEvents()

    @Slot('QString', 'QString', 'QString', name='streaming_file_error')
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
        device_item = None
        for index in range(self.UI.lstDevices.count()):
            if self.UI.lstDevices.item(index).text() == device_name:
                device_item = self.UI.lstDevices.item(index)
                break

        if not device_item and create_if_absent:
            device_item = QListWidgetItem(device_name)
            device_item.setIcon(QIcon(":/OpenIMU/icons/sensor.png"))
            self.UI.lstDevices.addItem(device_item)

        return device_item

    @Slot('QString', bool, name='device_connected')
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

    @Slot('QString', 'QString', int, name='streaming_file_completed')
    def streaming_file_completed(self, device_name: str, file_name: str, file_size: int):
        # Remove file from current list
        self.remove_file_progress_bar(file_name)

        # Add to completed list
        import os
        self.add_file_completed(device_name=device_name, filename=file_name.replace("/", os.sep), filesize=file_size)

        # Update device list
        device_item = self.get_device_item(device_name=device_name, create_if_absent=False)
        if device_item:
            self.UI.lstDevices.takeItem(self.UI.lstDevices.row(device_item))

    @Slot('QString', 'QString', int, name='streaming_file_started')
    def streaming_file_started(self, device_name: str, file_name: str, file_size: int):
        self.add_file_progress_bar(file_name, file_size)
        self.get_device_item(device_name=device_name, create_if_absent=True)

    def get_data_save_path(self) -> str:
        import os
        return self.UI.txtDataPath.text() + os.sep + "ToImport"

    def get_base_data_save_path(self) -> str:
        return self.UI.txtDataPath.text()

    def get_streamer_type(self) -> int:
        return self.UI.cmbStreamType.currentIndex()

    def get_delete_files_after_import(self) -> bool:
        return self.UI.chkDeleteFiles.isChecked()

    def closeEvent(self, _):
        self.close_requested()

    @Slot(name='close_requested')
    def close_requested(self):
        if self.streamer:
            self.streamer.stop_server()

        # Build list of root folders to import
        import os
        if os.path.isdir(self.get_data_save_path()):
            self.folders_to_import = os.listdir(self.get_data_save_path())

        self.accept()

    @Slot(name='streaming_server_finished')
    def streaming_server_finished(self):
        # self.accept()
        pass
