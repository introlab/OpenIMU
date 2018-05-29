from PyQt5.QtWidgets import QLineEdit, QWidget, QPushButton, QScrollArea, QVBoxLayout
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, pyqtSignal

from resources.ui.python.ResultWidget_ui import Ui_frmResult
from libopenimu.qt.Charts import OpenIMUBarGraphView


class ResultWindow(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent=parent)
        self.UI = Ui_frmResult()
        self.UI.setupUi(self)
        self.resize(800, 600)


    def display_freedson_1998(self, results : list, recordsets : list):

        layout = QVBoxLayout()
        # Add Scroll area
        scroll = QScrollArea(parent=self.UI.centralWidget)
        self.UI.centralLayout.addWidget(scroll)

        scroll.setLayout(layout)
        layout.addWidget(scroll)
        view = OpenIMUBarGraphView(scroll)
        view.set_title('Active minutes')
        layout.addWidget(view)

        if len(results) == len(recordsets):
            for i in range(len(results)):
                view.set_category_axis(results[i].keys())
                values = []

                for key in results[i]:
                    values.append(results[i][key])

                label = recordsets[i].name
                view.add_set(label, values)

        # Update view
        view.update()





