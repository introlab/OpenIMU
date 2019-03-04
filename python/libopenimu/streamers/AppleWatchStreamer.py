from libopenimu.streamers.BaseStreamer import BaseStreamer
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import QApplication

from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
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
        self.add_log.emit("Démarrage du serveur - utilisez 'Start python client' sur la montre pour transférer.",
                          LogTypes.LOGTYPE_INFO)

        self.request_handler = AppleWatchRequestHandler
        self.request_handler.streamer = self
        self.server = HTTPServer((self.get_local_ip_address(), self.server_port), self.request_handler)
        self.server_running = True
        self.server.serve_forever()
        self.server.server_close()
        # print('Server stopped')

    def get_streamer_infos(self):
        return {"Adresse IP": self.get_local_ip_address(),
                "Port": str(self.server_port),
                "Données": self.server_save_path}

    @pyqtSlot()
    def stop_server(self):
        # print ('Stop server request.')
        self.server_running = False
        self.server.shutdown()

    @staticmethod
    def get_local_ip_address():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_address = s.getsockname()[0]
        s.close()
        return local_address


class AppleWatchRequestHandler(BaseHTTPRequestHandler):
    streamer = None

    # Simple get to show what to do for file transfer
    def do_GET(self):

        # Ping requests can be answered directly
        content_type = self.headers['Content-Type']
        if content_type == 'cdrv-cmd/Connect':
            self.streamer.add_log.emit("Connexion de " + self.headers['Device-Name'], LogTypes.LOGTYPE_INFO)
            self.send_response(202)
            self.send_header('Content-type', 'cdrv-cmd/Connect')
            self.end_headers()
            return

        if content_type == 'cdrv-cmd/Disconnect':
            self.streamer.add_log.emit("Déconnexion de " + self.headers['Device-Name'], LogTypes.LOGTYPE_INFO)
            self.send_response(202)
            self.send_header('Content-type', 'cdrv-cmd/Connect')
            self.end_headers()
            return

        local_ip = AppleWatchStreamer.get_local_ip_address()

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes("""
               <html><body>
                   <h1> Enter following information on watch: </h1>
                   <ul>
                       <li>Host: %s</li>
                       <li>Port: %s</li>
                   </ul> 
               </html></body>
               """ % (local_ip, self.streamer.server_port), 'utf-8'))

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
            self.streamer.add_log.emit("Commande non-acceptée: " + content_type, LogTypes.LOGTYPE_WARNING)
            self.send_response(400)
            self.end_headers()
            return

        if None in [file_type, device_type, device_name, file_path, file_name]:
            self.streamer.add_log.emit("Requête mal-formattée. Refusée.", LogTypes.LOGTYPE_ERROR)
            self.streamer.file_error_occured.emit(file_name, "Requête mal formattée. Refusée.")
            self.send_response(400)
            self.end_headers()
            return

        destination_dir = (self.streamer.server_save_path + '/' + device_name + '/' + file_path + '/').replace('//', '/') \
            .replace('/', os.sep)
        destination_path = destination_dir + file_name

        file_name = device_name + file_path + '/' + file_name
        self.streamer.add_log.emit("Réception en cours: " + file_name + " (" + str(content_length) +
                                   " octets)", LogTypes.LOGTYPE_INFO)

        # Check if file exists and size matches
        file_infos = Path(destination_path)
        if file_infos.exists():
            file_infos = os.stat(destination_path)
            if file_infos.st_size < content_length:
                self.streamer.add_log.emit("Fichier existant, mais incomplet (" + str(file_infos.st_size) + "/" +
                                           str(content_length) + " octets) - retransfert.", LogTypes.LOGTYPE_WARNING)
            else:
                self.streamer.add_log.emit("Fichier existant - ignoré.", LogTypes.LOGTYPE_WARNING)
                self.streamer.update_progress.emit(file_name, "", 100, 100)
                self.send_response(200)
                self.send_header('Content-type', 'file-transfer/ack')
                self.end_headers()
                return

        # Destination directory if it doesn't exist
        Path(destination_dir).mkdir(parents=True, exist_ok=True)

        # Gets the data and save to file
        buffer_size = 4 * 1024
        content_size_remaining = content_length
        last_pc = -1

        # Supported file type?
        if file_type.lower() in ['data', 'dat', 'csv', 'txt', 'oimi']:

            if file_type.lower() in ['data', 'dat']:
                # Binary file
                fh = open(destination_path, 'wb')
                text_format = False
            else:
                # Text file
                fh = open(destination_path, 'w')
                text_format = True

            while content_size_remaining > 0 and self.streamer.server_running:
                QApplication.processEvents()
                if buffer_size > content_size_remaining:
                    buffer_size = content_size_remaining
                data = self.rfile.read(buffer_size)
                if text_format:
                    fh.write(data.decode())
                else:
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
            self.streamer.add_log.emit("Type de fichier non-supporté: " + file_type.lower(), LogTypes.LOGTYPE_ERROR)
            self.streamer.file_error_occured.emit(file_name, "Type de fichier non-supporté: " + file_type.lower())
            self.send_response(400)
            self.send_header('Content-type', 'file-transfer/invalid-file-type')
            self.end_headers()
            return

        # Check if everything was received correctly
        file_infos = os.stat(destination_path)
        if file_infos.st_size < content_length:
            # Missing data?!?!
            error = "Erreur de transmission:  " + str(file_infos.st_size) + " octets reçus sur " + str(content_length)
            self.streamer.add_log.emit(error, LogTypes.LOGTYPE_ERROR)
            self.streamer.file_error_occured.emit(file_name, error)
        else:
            # All is good!
            self.streamer.add_log.emit("Complété", LogTypes.LOGTYPE_DONE)
        self.send_response(200)
        self.send_header('Content-type', 'file-transfer/ack')
        self.end_headers()
