from PyQt5.QtCore import QThread, pyqtSignal


class BaseStreamer(QThread):
    add_log = pyqtSignal('QString', int)
    update_progress = pyqtSignal('QString', 'QString', int, int)

    server_save_path = './Files'
    server = None
    request_handler = None
    server_running = False

    def __init__(self, path='./Files', parent=None):
        super(BaseStreamer, self).__init__(parent)
        self.server_save_path = path
