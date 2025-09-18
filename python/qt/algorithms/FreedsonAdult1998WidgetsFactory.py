from PySide6.QtWidgets import QTableWidgetItem, QWidget
from qt.algorithms.AlgorithmWidgetsFactory import AlgorithmWidgetsFactory
from qt.algorithms.FreedsonAdult1998ConfigWidget import FreedsonAdult1998ConfigWidget
from qt.algorithms.FreedsonAdult1998DisplayWidget import FreedsonAdult1998DisplayWidget


class FreedsonAdult1998WidgetsFactory(AlgorithmWidgetsFactory):

    def __init__(self, base_factory):
        AlgorithmWidgetsFactory.__init__(self, base_factory)

    def build_config_widget(self, parent) -> QWidget:
        return FreedsonAdult1998ConfigWidget(parent)

    def build_display_widget(self, parent, data, recordsets) -> QWidget:
        # TODO ARGS
        return FreedsonAdult1998DisplayWidget(parent)
