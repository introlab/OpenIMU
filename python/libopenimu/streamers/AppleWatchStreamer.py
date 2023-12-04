from libopenimu.streamers.BaseStreamer import BaseStreamer
from PySide6.QtCore import Slot, QObject

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
import math

from libopenimu.models.LogTypes import LogTypes


class AppleWatchStreamer(BaseStreamer):

    server_port = 8118

    def __init__(self, port=8118, path='./Files', parent=None):
        super(AppleWatchStreamer, self).__init__(path=path, parent=parent)
        self.server_port = port

    def run(self):
        self.add_log.emit(self.tr('Starting Sensorlogger (Apple Watch) server on port') + ' ' + str(self.server_port),
                          LogTypes.LOGTYPE_INFO)

        self.request_handler = AppleWatchRequestHandler
        self.request_handler.streamer = self
        self.server = ThreadingHTTPServer((self.get_local_ip_address(), self.server_port), self.request_handler)
        self.server_running = True
        self.server.timeout = 5  # 5 seconds timeout should be ok since we are usually on local network
        self.server.serve_forever()
        self.server.server_close()
        # print('Server stopped')
    #
    # def get_streamer_infos(self):
    #     return {"Adresse IP": self.get_local_ip_address(),
    #             "Port": str(self.server_port),
    #             "Données": self.server_save_path}

    @Slot()
    def stop_server(self):
        self.add_log.emit(self.tr('Stopping Sensorlogger (Apple Watch) server...'), LogTypes.LOGTYPE_INFO)
        self.server_running = False
        self.server.shutdown()


class AppleWatchRequestHandler(BaseHTTPRequestHandler, QObject):
    streamer: AppleWatchStreamer = None

    def setup(self):
        self.timeout = 5
        BaseHTTPRequestHandler.setup(self)

    # Simple get to show what to do for file transfer
    def do_GET(self):
        # Ping requests can be answered directly
        content_type = self.headers['Content-Type']
        if content_type == 'cdrv-cmd/Connect':
            # self.streamer.add_log.emit("Connexion de " + self.headers['Device-Name'], LogTypes.LOGTYPE_INFO)
            self.streamer.device_connected.emit(self.headers['Device-Name'], True)
            self.send_response(202)
            self.send_header('Content-type', 'cdrv-cmd/Connect')
            self.end_headers()
            return

        if content_type == 'cdrv-cmd/Disconnect':
            # self.streamer.add_log.emit("Déconnexion de " + self.headers['Device-Name'], LogTypes.LOGTYPE_INFO)
            self.streamer.device_connected.emit(self.headers['Device-Name'], False)
            self.send_response(202)
            self.send_header('Content-type', 'cdrv-cmd/Disconnect')
            self.end_headers()
            return

        local_ip = AppleWatchStreamer.get_local_ip_address()

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):

        # Unpack metadata
        content_type = self.headers['Content-Type']
        content_length = int(self.headers['Content-Length'])
        file_type = self.headers['File-Type']
        device_type = self.headers['Device-Type']
        device_name = self.headers['Device-Name']
        file_path = self.headers['File-Path']
        file_name = self.headers['File-Name']

        if content_type != 'cdrv-cmd/File-Upload':
            self.streamer.add_log.emit(self.tr('Command refused') + ': ' + content_type,
                                       LogTypes.LOGTYPE_WARNING)
            self.send_response(400)
            self.end_headers()
            return

        if None in [file_type, device_type, device_name, file_path, file_name]:
            self.streamer.add_log.emit(self.tr('Badly formatted request. Refused.'), LogTypes.LOGTYPE_ERROR)
            self.streamer.file_error_occured.emit(self.tr('Unknown'), file_name,
                                                  self.tr('Badly formatted request. Refused.'))
            self.send_response(400)
            self.end_headers()
            return

        destination_dir = (self.streamer.server_save_path + '/' + device_name + '/' + file_path + '/').replace('//', '/') \
            .replace('/', os.sep)
        destination_path = destination_dir + file_name

        file_name = device_name + file_path + '/' + file_name
        self.streamer.add_log.emit(self.tr('Receiving') + ': ' + file_name + " (" + str(content_length) +
                                   ' ' + self.tr('bytes') + ')', LogTypes.LOGTYPE_INFO)
        self.streamer.transfer_started.emit(device_name, file_name, content_length)

        # Check if file exists and size matches
        file_infos = Path(destination_path)
        if file_infos.exists():
            file_infos = os.stat(destination_path)
            if file_infos.st_size < content_length:
                self.streamer.add_log.emit(file_name + ' - ' + self.tr('Existing file, but incomplete') + ' ('
                                           + str(file_infos.st_size) + "/" +
                                           str(content_length) + ' ' + self.tr('bytes') + ' - ' +
                                           self.tr('retransferring'), LogTypes.LOGTYPE_WARNING)
            else:
                self.streamer.add_log.emit(file_name + ' - ' + self.tr('Existing file - overwriting'),
                                           LogTypes.LOGTYPE_WARNING)
                # self.streamer.add_log.emit("Fichier existant - ignoré.", LogTypes.LOGTYPE_WARNING)
                # self.streamer.update_progress.emit(file_name, "", 100, 100)
                # self.send_response(200)
                # self.send_header('Content-type', 'file-transfer/ack')
                # self.end_headers()
                # return

        # Destination directory if it doesn't exist
        Path(destination_dir).mkdir(parents=True, exist_ok=True)

        # Gets the data and save to file
        buffer_size = 4 * 1024
        content_size_remaining = content_length
        last_pc = -1

        # Supported file type?
        if file_type.lower() in ['data', 'dat', 'csv', 'txt', 'oimi']:
            # if file_type.lower() in ['data', 'dat']:
            # Binary file
            fh = open(destination_path, 'wb')
            text_format = False
            # else: # Text file
            #    fh = open(destination_path, 'w')
            #    text_format = True

            # print("About to receive: " + file_name + ": " + str(content_size_remaining) + " bytes.")
            while content_size_remaining > 0 and self.streamer.server_running:
                if buffer_size > content_size_remaining:
                    buffer_size = content_size_remaining
                try:
                    data = self.rfile.read(buffer_size)
                except OSError as err:
                    err_desc = err.strerror
                    if not err_desc and len(err.args) > 0:
                        err_desc = err.args[0]
                    self.streamer.file_error_occured.emit(device_name, file_name, str(err_desc))
                    return

                # if text_format:
                #     fh.write(data.decode(encoding='unicode'))
                # else:
                fh.write(data)
                content_size_remaining -= buffer_size
                content_received = (content_length - content_size_remaining)
                pc = math.floor((content_received / content_length) * 100)
                if pc != last_pc:
                    self.streamer.update_progress.emit(file_name, " (" + str(content_received) + "/ " +
                                                       str(content_length) + ")", (content_length -
                                                                                   content_size_remaining),
                                                       content_length)
                    last_pc = pc
            fh.close()
        else:
            # self.streamer.add_log.emit(device_name + ": " + file_name + " - Type de fichier non-supporté: " +
            #                            file_type.lower(), LogTypes.LOGTYPE_ERROR)
            self.streamer.file_error_occured.emit(device_name, file_name, self.tr('Unsupported file type') + ': ' +
                                                  file_type.lower())
            self.send_response(400)
            self.send_header('Content-type', 'file-transfer/invalid-file-type')
            self.end_headers()
            return

        # Check if everything was received correctly
        file_infos = os.stat(destination_path)
        if file_infos.st_size < content_length:
            # Missing data?!?!
            error = self.tr('Error receiving') + ': ' + str(file_infos.st_size) + ' ' + \
                    self.tr('bytes received, expected') + ' ' + str(content_length)
            # self.streamer.add_log.emit(error, LogTypes.LOGTYPE_ERROR)
            self.streamer.file_error_occured.emit(device_name, file_name, error)
        else:
            # All is good!
            self.streamer.add_log.emit(device_name + ": " + file_name + " - " + self.tr('Completed'),
                                       LogTypes.LOGTYPE_DONE)
            self.streamer.transfer_completed.emit(device_name, file_name, file_infos.st_size)
        self.send_response(200)
        self.send_header('Content-type', 'file-transfer/ack')
        self.end_headers()

    def log_request(self, code: int | str = ..., size: int | str = ...) -> None:
        # Suppress messages
        return
