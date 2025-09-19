from PySide6.QtWidgets import QTableWidgetItem
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

from qt.algorithms.BaseConfigWidget import BaseConfigWidget


class Evenson2008ConfigWidget(BaseConfigWidget):

    def __init__(self, params, parent):
        BaseConfigWidget.__init__(self, params, parent=parent)

        # Initialize inputs
        self.config_preset_input = QComboBox(self)

        self.config_preset_input.addItem(
            self.tr("Default values"),
            [
                params["sedentary_cutoff"]["default_value"],
                params["light_cutoff"]["default_value"],
                params["moderate_cutoff"]["default_value"],
            ],
        )

        self.config_preset_input.addItem(self.tr("Custom values"), [-1, -1, -1])
        self.config_preset_input.currentIndexChanged.connect(self.config_preset_changed)

        base_layout = QVBoxLayout()
        preset_frame = QFrame()
        preset_frame.setStyleSheet(
            "QFrame{background-color: rgba(200,200,200,50%);}"
            "QLabel{background-color: rgba(0,0,0,0%);}"
        )
        preset_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        frame_layout = QGridLayout()
        item_label = QLabel(self.tr("Preset"))
        frame_layout.addWidget(item_label, 0, 0)
        frame_layout.addWidget(self.config_preset_input, 0, 1)
        # frame_layout.addRow('Preset', self.config_preset_input)
        preset_frame.setLayout(frame_layout)
        base_layout.addWidget(preset_frame)

        layout = QGridLayout()
        layout.setAlignment(Qt.AlignTop)
        self.config_sedentary_input = QSpinBox()
        self.config_sedentary_input.setRange(
            params["sedentary_cutoff"]["min_value"],
            params["sedentary_cutoff"]["max_value"],
        )
        self.config_sedentary_input.setValue(
            params["sedentary_cutoff"]["default_value"]
        )
        item_label = QLabel("Cut-off Sedentary")
        layout.addWidget(item_label, 0, 0)
        layout.addWidget(self.config_sedentary_input, 0, 1)

        self.config_light_input = QSpinBox()
        self.config_light_input.setRange(
            params["light_cutoff"]["min_value"], params["light_cutoff"]["max_value"]
        )
        self.config_light_input.setValue(params["light_cutoff"]["default_value"])
        item_label = QLabel("Cut-off Light")
        layout.addWidget(item_label, 1, 0)
        layout.addWidget(self.config_light_input, 1, 1)

        self.config_moderate_input = QSpinBox()
        self.config_moderate_input.setRange(
            params["moderate_cutoff"]["min_value"],
            params["moderate_cutoff"]["max_value"],
        )
        self.config_moderate_input.setValue(params["moderate_cutoff"]["default_value"])
        item_label = QLabel("Cut-off Moderate")
        layout.addWidget(item_label, 2, 0)
        layout.addWidget(self.config_moderate_input, 2, 1)

        base_layout.addLayout(layout)
        self.setLayout(base_layout)

        # Update presets
        self.config_preset_changed()

    def get_params(self):
        return {
            "sedentary_cutoff": self.config_sedentary_input.value(),
            "light_cutoff": self.config_light_input.value(),
            "moderate_cutoff": self.config_moderate_input.value(),
        }

    def config_preset_changed(self):
        params = self.config_preset_input.currentData()
        if params is not None and len(params) == 3:
            if params[0] != -1:
                self.config_sedentary_input.setValue(params[0])
                self.config_light_input.setValue(params[1])
                self.config_moderate_input.setValue(params[2])
            self.config_sedentary_input.setEnabled(params[0] == -1)
            self.config_light_input.setEnabled(params[0] == -1)
            self.config_moderate_input.setEnabled(params[0] == -1)
