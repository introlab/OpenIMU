from PyQt5.QtCore import QThread, QCoreApplication, QTime, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QProgressDialog, QLabel
import numpy as np


class ProgressDialog(QProgressDialog):
    def __init__(self, count, parent=None):
        super(QProgressDialog, self).__init__(parent)
        self.total_count = count
        self.count = 0
        self.setMinimum(0)
        self.setMaximum(self.total_count)
        self.time = QTime.currentTime()
        self.time.start()
        self.startTimer(1000)
        self.setCancelButton(None)

        self.setStyleSheet("QProgressDialog{background-image:url(:/OpenIMU/background/dark_metal.jpg); border-radius:0px;}")

    @pyqtSlot()
    def trigger(self):
        self.count = self.count + 1
        self.setValue(self.count)

    def timerEvent(self, a0: 'QTimerEvent'):
        self.setLabelText('Temps : ' + str(np.floor(self.time.elapsed() / 1000)) + ' secondes')


class BackgroundProcess(QThread):

    # Define a new signal called 'trigger' that has no arguments.
    trigger = pyqtSignal()

    def __init__(self, functions: list, parent=None):
        super(QThread, self).__init__(parent)
        self.functions = functions

    def run(self):

        print('Run Starting!')
        for f in self.functions:
            f()
            self.trigger.emit()
        print('Run Done!')


# Main
if __name__ == '__main__':
    import sys
    app = QCoreApplication(sys.argv)

    def hello_world():
        print('Hello world')

    thread = BackgroundProcess(hello_world)
    thread.start()

    thread.finished.connect(app.quit)

    sys.exit(app.exec_())
