import os, time, sys, subprocess, signal


class JupyterNotebook():
    def __init__(self):
        self.notebooks_directory = os.getcwd() + '/notebooks'
        self.jupyter_executable = sys.exec_prefix +'/bin/jupyter'
        self.jupyter_pid = None
        print('notebooks directory: ', self.notebooks_directory)
        print('jupyter path:', self.jupyter_executable)

    def __del__(self):
        self.stop()

    def start(self):
        self.jupyter_pid = subprocess.Popen([self.jupyter_executable, 'notebook'
                               , "--NotebookApp.token=''"
                               , '--notebook-dir=' + self.notebooks_directory
                               , '--no-browser', '--port=8888']).pid
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
    time.sleep(10)

