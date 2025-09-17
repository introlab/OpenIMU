from PySide6.QtCore import QThread, Signal


class BaseStreamer(QThread):
    add_log = Signal('QString', int)  # Msg, Logtype
    update_progress = Signal('QString', 'QString', int, int)  # File, Progress string, value, max_value
    file_error_occured = Signal('QString', 'QString', 'QString')  # Device, File, Error string

    device_connected = Signal('QString', bool)  # Device, Connected?
    transfer_completed = Signal('QString', 'QString', int)  # Device, Filename, file size
    transfer_started = Signal('QString', 'QString', int)  # Device, Filename, file size

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
