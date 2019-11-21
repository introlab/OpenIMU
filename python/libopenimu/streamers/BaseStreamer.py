from PyQt5.QtCore import QThread, pyqtSignal


class BaseStreamer(QThread):
    add_log = pyqtSignal('QString', int)
    update_progress = pyqtSignal('QString', 'QString', int, int)
    file_error_occured = pyqtSignal('QString', 'QString')

    server_save_path = './Files'
    server = None
    request_handler = None
    server_running = False

    def __init__(self, path='./Files', parent=None):
        super(BaseStreamer, self).__init__(parent)
        self.server_save_path = path

    @staticmethod
    def get_local_ip_address():
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_address = s.getsockname()[0]
        s.close()
        return local_address
