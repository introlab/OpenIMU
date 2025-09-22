from PySide6.QtWidgets import QTableWidgetItem, QWidget
from PySide6.QtCore import Slot, Signal, Qt

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QGridLayout,
    QSpinBox,
    QComboBox,
    QFrame,
    QSizePolicy,
    QLabel,
)


from qt.Charts import OpenIMUBarGraphView


class FreedsonAdult1998DisplayWidget(QWidget):

    def __init__(self, results: dict, recordsets: list, parent: QWidget):
        QWidget.__init__(self, parent=parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Add Scroll area
        scroll = QScrollArea()
        view = OpenIMUBarGraphView()
        scroll.setWidget(view)
        scroll.setWidgetResizable(True)

        # Set minimum size to prevent tiny display
        view.setMinimumSize(600, 400)

        view.set_title(self.tr("Active minutes"))
        layout.addWidget(scroll)

        for result in results:
            data = result["result"]
            view.set_category_axis(data.keys())
            values = []

            for key in data:
                values.append(data[key])

            label = result["result_name"]
            view.add_set(label, values)
        # Update view
        view.update()
