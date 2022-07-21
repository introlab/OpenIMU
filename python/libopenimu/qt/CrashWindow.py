from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Slot
from resources.ui.python.CrashDialog_ui import Ui_CrashDialog

import traceback


class CrashWindow(QDialog):
    def __init__(self, error_trace: traceback, error_exception, parent=None):
        super().__init__(parent=parent)
        self.UI = Ui_CrashDialog()
        self.UI.setupUi(self)

        error_stack_str = traceback.format_tb(error_trace)
        error_exception_str = '<b>' + str(error_exception.with_traceback(error_trace)) + '</b>'
        self.UI.txtTraceback.setHtml(error_exception_str + '<hr><font color=red>' +
                                     '</font><hr><font color=red>'.join(error_stack_str))

        self.UI.btnOK.clicked.connect(self.ok_clicked)

    @Slot()
    def ok_clicked(self):
        self.accept()