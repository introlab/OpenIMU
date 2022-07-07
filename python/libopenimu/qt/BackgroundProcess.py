from PySide6.QtCore import QThread, QCoreApplication, Signal, Slot, Qt, QObject, QThreadPool, QRunnable, QElapsedTimer
from PySide6.QtWidgets import QDialog, QApplication
from PySide6.QtGui import QMovie
from resources.ui.python.ProgressDialog_ui import Ui_ProgressDialog

import numpy as np
import gc
import string


class WorkerTask(QObject):

    update_progress = Signal(int)  # Current progress in %
    size_updated = Signal()
    log_request = Signal(str, int)
    results_ready = Signal('QVariant')

    def __init__(self, title: string, size: int, parent=None):
        super().__init__(parent)
        self.title = title
        self._size = size

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self.size_updated.emit()

    def process(self):
        print("Empty task - " + self.title + " - nothing to process!")


class SimpleTask(WorkerTask):  # A simple worker task without any progress reporting

    def __init__(self, title: string, task_func, func_arg=None, parent=None):
        super(SimpleTask, self).__init__(title, 0, parent)

        self.task_process = task_func
        self.task_parameters = func_arg

    def process(self):
        if self.task_parameters:
            self.task_process(self.task_parameters)
        else:
            self.task_process()


class BackgroundProcess(QThread):

    # Define a new signal called 'trigger' that has no arguments.
    task_completed = Signal()
    update_current_task_progress = Signal(int)

    def __init__(self, tasks: list, parent=None):
        super(BackgroundProcess, self).__init__(parent)
        self.tasks = tasks

    def run(self):
        # print('Run Starting!')
        for task in self.tasks:
            task.update_progress.connect(self.update_current_task_progress)
            task.process()
            self.task_completed.emit()
            del task
        # print('Run Done!')


# Testing parallel import (will require more ram)
class BackgroundProcessForImporters(BackgroundProcess):
    def __init__(self, tasks: list, parent=None):
        super(BackgroundProcessForImporters, self).__init__(tasks, parent)

    def run(self):
        class ProcessRunnable(QRunnable):
            def __init__(self, run_task):
                super().__init__()
                self.setAutoDelete(True)
                self.task = run_task
                self.results = []

            def run(self):
                print('processing...', self.task.filename)

                if self.task.load_data():
                    print('data loaded...', self.task.filename)
                else:
                    print('data not loaded...', self.task.filename)

                # Emit signal that task may have results
                self.task.results_ready.emit(self.task)

        print('BackgroundProcessForImporters starting load threads')
        pool = QThreadPool()

        # Disable expiration
        pool.setExpiryTimeout(-1)

        print('MaxThread count: ', pool.maxThreadCount())

        # Starting all threads for importation
        runnable_list = []
        for task in self.tasks:
            # Connect signals
            task.update_progress.connect(self.update_current_task_progress)
            # Add to list
            runnable_list.append(ProcessRunnable(task))
            # Connect results ready signals
            task.results_ready.connect(self.results_ready)
            # Start last inserted runnable
            pool.start(runnable_list[-1], priority=QThread.NormalPriority)

        # Wait for all runnable threads
        if pool.waitForDone():
            print('All threads done!')
            # for task in self.tasks:
            #     task.import_data()
            #     self.task_completed.emit()
            #     del task

    @Slot('QVariant')
    def results_ready(self, task):
        print('results_ready, importing to database', task.filename)

        task.import_data()

        print('completed...')
        self.task_completed.emit()

        # Destroy task
        del task


class ProgressDialog(QDialog):
    cancel_requested = Signal()

    def __init__(self, bg_process: BackgroundProcess, job_title: string, parent=None):
        QDialog.__init__(self, parent=parent)

        self.UI = Ui_ProgressDialog()
        self.UI.setupUi(self)
        self.setWindowFlags(Qt.SplashScreen)

        # self.UI.frameCancel.hide()  # Hide cancel frame

        self.tasks = bg_process.tasks
        self.UI.prgTotal.setMinimum(0)
        self.UI.prgTotal.setMaximum(len(self.tasks))
        self.count = -1
        self.next_task()

        self.time = QElapsedTimer()
        self.time.start()
        self.startTimer(1000)
        # self.setCancelButton(None)
        self.set_job_title(job_title)

        self.total_work_load = self.compute_workload()
        self.total_work_done = 0
        self.work_speed_estimates = []

        # Setup loading icon
        icon = QMovie(":/OpenIMU/icons/loading.gif")
        self.UI.icoWorking.setMovie(icon)
        icon.start()

        if len(self.tasks) < 2:
            self.UI.prgTotal.hide()
            self.UI.lblCurrentTask.hide()

        if self.total_work_load == 0 and len(self.tasks) > 1:
            self.UI.prgTask.hide()

        # Center dialog on screen
        if parent:
            screen_geometry = parent.window().windowHandle().screen().availableGeometry()
        else:
            screen_geometry = QApplication.primaryScreen().availableGeometry()

        x = (screen_geometry.width() - self.width()) / 2
        y = (screen_geometry.height() - self.height()) / 2
        self.move(x, y)

        # Connect signals
        bg_process.finished.connect(self.accept)
        bg_process.task_completed.connect(self.next_task)
        bg_process.update_current_task_progress.connect(self.update_current_task_progress)
        # self.UI.btnCancelTask.clicked.connect(self.cancel_clicked)

    def showEvent(self, event):
        self.display_current_task()

    def display_current_task(self):
        if self.count < len(self.tasks):
            self.UI.lblCurrentTaskValue.setText(self.tasks[self.count].title)

    def compute_workload(self):
        return sum(t.size for t in self.tasks)

    def set_job_title(self, title):
        self.setWindowTitle(title)
        self.UI.lblTitle.setText(title)

    @Slot()
    def current_task_size_updated(self):
        new_size = self.tasks[self.count].size
        if new_size < self.UI.prgTask.value():
            self.UI.prgTask.setValue(new_size)

        self.UI.prgTask.setMaximum(new_size)

        self.total_work_load = self.compute_workload()
        if self.total_work_done > self.total_work_load:
            self.total_work_done = self.total_work_load

    @Slot()
    def next_task(self):
        self.count = self.count + 1
        if self.count < len(self.tasks):
            self.display_current_task()
            self.UI.prgTotal.setValue(self.count)
            self.UI.prgTask.setValue(0)
            self.UI.prgTask.setMaximum(self.tasks[self.count].size)
            self.tasks[self.count].size_updated.connect(self.current_task_size_updated)

        gc.collect()

    @Slot(int)
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

    @Slot()
    def cancel_clicked(self):
        print('Cancel requested')
        self.cancel_requested.emit()


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
