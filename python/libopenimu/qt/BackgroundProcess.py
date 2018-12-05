from PyQt5.QtCore import QThread, QCoreApplication, QTime, pyqtSignal, pyqtSlot, Qt, QObject
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QMovie, QDesktopServices
from resources.ui.python.ProgressDialog_ui import Ui_ProgressDialog

import numpy as np
import gc
import string


class WorkerTask(QObject):

    update_progress = pyqtSignal(int)  # Current progress in %

    def __init__(self, title: string, size: int, parent=None):
        super().__init__(parent)
        self.title = title
        self.size = size

    @staticmethod
    def process(self):
        print("Empty task - nothing to process!")


class SimpleTask(QObject):  # A simple worker task without any progress reporting

    def __init__(self, title: string, task_func, parent=None):
        super().__init(title, 0, parent)

        self.task_process = task_func

    def process(self):
        self.task_process()


class BackgroundProcess(QThread):

    # Define a new signal called 'trigger' that has no arguments.
    task_completed = pyqtSignal()
    update_current_task_progress = pyqtSignal(int)

    def __init__(self, tasks: list, parent=None):
        super(BackgroundProcess, self).__init__(parent)
        self.tasks = tasks

    def run(self):
        print('Run Starting!')
        for task in self.tasks:
            task.update_progress.connect(self.update_current_task_progress)
            task.process()
            self.task_completed.emit()
            del task
        print('Run Done!')


class ProgressDialog(QDialog):
    def __init__(self, bg_process: BackgroundProcess, job_title: string, parent=None):
        super(ProgressDialog, self).__init__(parent)

        self.UI = Ui_ProgressDialog()
        self.UI.setupUi(self)
        self.setWindowFlags(Qt.SplashScreen)

        self.tasks = bg_process.tasks
        self.count = 0
        self.UI.prgTotal.setMinimum(0)
        self.UI.prgTotal.setMaximum(len(self.tasks))
        self.time = QTime.currentTime()
        self.startTimer(1000)
        # self.setCancelButton(None)
        self.set_job_title(job_title)

        self.total_work_load = sum(t.size for t in self.tasks)
        self.total_work_done = 0
        self.work_speed_estimates = []

        # Setup loading icon
        icon = QMovie(":/OpenIMU/icons/loading.gif")
        self.UI.icoWorking.setMovie(icon)
        icon.start()

        # Center dialog on screen
        screen_geometry =  QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) / 2
        y = (screen_geometry.height() - self.height()) / 2;
        self.move(x, y);

        # Connect signals
        bg_process.finished.connect(self.accept)
        bg_process.task_completed.connect(self.next_job)
        bg_process.update_current_task_progress.connect(self.update_current_task_progress)

    def showEvent(self, event):
        self.display_current_task()

    def display_current_task(self):
        if self.count < len(self.tasks):
            self.UI.lblCurrentTaskValue.setText(self.tasks[self.count].title)

    def set_job_title(self, title):
        self.setWindowTitle(title)
        self.UI.lblTitle.setText(title)

    @pyqtSlot()
    def next_job(self):
        self.count = self.count + 1
        if self.count < len(self.tasks):
            self.display_current_task()
            self.UI.prgTotal.setValue(self.count)
            self.UI.prgTask.setValue(0)
            self.UI.prgTask.setMaximum(self.tasks[self.count].size)

        gc.collect()

    @pyqtSlot(int)
    def update_current_task_progress(self, value: int):
        self.total_work_done += (value - self.UI.prgTask.value())
        self.UI.prgTask.setValue(value)

    def timerEvent(self, a0: 'QTimerEvent'):
        # self.setLabelText('Temps : ' + str(np.floor(self.time.elapsed() / 1000)) + ' secondes')
        elapsed_time = self.time.elapsed()
        self.UI.lblElapsedValue.setText(self.format_time_display(elapsed_time))

        # Estimate remaining time
        # TODO: Improve!!
        if self.total_work_done > 0:
            instant_speed = int(elapsed_time / self.total_work_done)
            self.work_speed_estimates.append(instant_speed)
            if len(self.work_speed_estimates) > min(10, int(self.total_work_load / 25)):
                mean_speed = sum(self.work_speed_estimates) / len(self.work_speed_estimates)
                remaining_time = int(mean_speed) * (self.total_work_load - self.total_work_done)
                self.work_speed_estimates.pop(0)
                self.UI.lblRemainingValue.setText(self.format_time_display(remaining_time))

    @staticmethod
    def format_time_display(display_time: int):
        h = np.floor(display_time / 3600000)
        m = np.floor((display_time - h * 3600000) / 60000)
        s = np.floor((display_time - h * 3600000 - m * 60000) / 1000)
        return "%02d:%02d:%02d" % (h, m, s)


# Main
if __name__ == '__main__':
    import sys
    app = QCoreApplication(sys.argv)

    def hello_world():
        print('Hello world')

    thread = BackgroundProcess([hello_world])
    thread.start()

    thread.finished.connect(app.quit)

    sys.exit(app.exec_())
