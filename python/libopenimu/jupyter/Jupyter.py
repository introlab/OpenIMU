import os
import sys
import signal
import platform

from threading import Thread


class JupyterNotebook2:
    def __init__(self):
        self.thread = None
        self.start_thread()

    def start_thread(self):
        self.thread = Thread(target=self.notebook_thread)
        print('Starting thread...')
        self.thread.start()

    def join_thread(self):
        self.thread.join()

    def wait_thread(self):
        pass

    @staticmethod
    def notebook_thread():
        # from jupyter_console.app import launch_new_instance
        # from IPython.terminal.ipapp import launch_new_instance
        # from IPython.lib import passwd
        from socket import gethostname
        import warnings

        warnings.filterwarnings("ignore", module="zmq.*")
        sys.argv.append("notebook")
        sys.argv.append("--IPKernelApp.pylab='inline'")
        sys.argv.append("--NotebookApp.ip=" + gethostname())
        sys.argv.append("--NotebookApp.open_browser=False")
        # sys.argv.append("--NotebookApp.password=" + passwd())
        # launch_new_instance()


class JupyterNotebook:
    def __init__(self):
        self.notebooks_directory = os.getcwd() + '/../../notebooks'
        print('OS Name:', platform.system())

        # Installation seems to differ from one platform to another.
        if platform.system() is 'Windows':
            self.working_directory = sys.exec_prefix + '/Scripts/'
            self.jupyter_executable = sys.exec_prefix + '/Scripts/jupyter.exe'
        else:
            self.working_directory = sys.exec_prefix + '/bin/'
            self.jupyter_executable = sys.exec_prefix + '/bin/jupyter'

        self.jupyter_pid = None
        print('notebooks directory: ', self.notebooks_directory)
        print('jupyter path:', self.jupyter_executable)

    def __del__(self):
        self.stop()

    def stop(self):
        if self.jupyter_pid is not None:
            print('Stopping Jupyter Notebook process ... pid:', self.jupyter_pid)
            os.kill(self.jupyter_pid, signal.SIGINT)  # or signal.SIGKILL
            self.jupyter_pid = None


def start():
    """ self.jupyter_pid = subprocess.Popen([self.jupyter_executable, 'notebook'
                           , "--NotebookApp.token=''"
                           , '--notebook-dir=' + self.notebooks_directory
                           , '--no-browser', '--port=8888'], cwd=self.working_directory).pid

    print('Jupyter Notebook started with pid: ', self.jupyter_pid)
    return self.jupyter_pid
    """
    return -1
