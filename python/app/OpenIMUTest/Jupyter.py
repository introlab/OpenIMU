import os, time, sys, subprocess


def start_jupyter():

    notebooks_directory = os.getcwd() + '/notebooks'
    jupyter_executable = sys.exec_prefix +'/bin/jupyter'
    print('notebooks directory: ',notebooks_directory)
    print('jupyter path:', jupyter_executable)

    #Launch the jupyter executable
    pid = subprocess.Popen([jupyter_executable, 'notebook'
                               , "--NotebookApp.token=''"
                               , '--notebook-dir=' + notebooks_directory
                               , '--no-browser', '--port=8888']).pid
    return pid


if __name__ == '__main__':
    pid = start_jupyter()

