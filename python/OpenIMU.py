import sys

from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QStyleFactory
from PySide6.QtCore import Qt, Slot, Signal, QFile


def except_hook(cls, exception, traceback):
    # Display error dialog
    from libopenimu.qt.CrashWindow import CrashWindow
    crash_dlg = CrashWindow(traceback, exception)
    crash_dlg.exec()
    sys.__excepthook__(cls, exception, traceback)


# Main
if __name__ == '__main__':
    from PySide6.QtCore import QDir
    from libopenimu.qt.OpenIMUApp import OpenIMUApp
    from libopenimu.qt.MainWindow import MainWindow

    app = OpenIMUApp()

    # Route errors to error dialog
    # sys.excepthook = except_hook

    # Set current directory to home path
    QDir.setCurrent(QDir.homePath())

    # print(PyQt5.__file__)
    # from pprint import pprint
    # from PyQt5.QtCore import QLibraryInfo
    # paths = [x for x in dir(QLibraryInfo) if x.endswith('Path')]
    # pprint({x: QLibraryInfo.location(getattr(QLibraryInfo, x)) for x in paths})

    # WebEngine settings
    # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
    # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
    # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
    # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls,True)
    # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)

    # Create Main Window
    # window = MainWindow()

    # Exec application
    exit_code = app.exec()
    sys.exit(exit_code)

