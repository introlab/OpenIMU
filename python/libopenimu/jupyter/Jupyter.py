import os, time, sys, subprocess, signal, platform


class JupyterNotebook():
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

    def start(self):
        self.jupyter_pid = subprocess.Popen([self.jupyter_executable, 'notebook'
                               , "--NotebookApp.token=''"
                               , '--notebook-dir=' + self.notebooks_directory
                               , '--no-browser', '--port=8888'], cwd=self.working_directory).pid

        print('Jupyter Notebook started with pid: ', self.jupyter_pid)
        return self.jupyter_pid

    def stop(self):
        if self.jupyter_pid is not None:
            print('Stopping Jupyter Notebook process ... pid:', self.jupyter_pid)
            os.kill(self.jupyter_pid, signal.SIGINT)  # or signal.SIGKILL
            self.jupyter_pid = None


if __name__ == '__main__':
    import time
    nb = JupyterNotebook()
    pid = nb.start()
    time.sleep(100)

