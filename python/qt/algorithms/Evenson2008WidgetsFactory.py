from PySide6.QtWidgets import QTableWidgetItem, QWidget
from qt.algorithms.AlgorithmWidgetsFactory import AlgorithmWidgetsFactory
from qt.algorithms.Evenson2008ConfigWidget import Evenson2008ConfigWidget
from qt.algorithms.Evenson2008DisplayWidget import Evenson2008DisplayWidget

from qt.algorithms.BaseConfigWidget import BaseConfigWidget


class Evenson2008WidgetsFactory(AlgorithmWidgetsFactory):

    def __init__(self, base_factory):
        AlgorithmWidgetsFactory.__init__(self, base_factory)

    def build_config_widget(self, parent: QWidget) -> BaseConfigWidget:
        return Evenson2008ConfigWidget(self.params(), parent)

    def build_display_widget(self, parent: QWidget, results, recordsets) -> QWidget:
        return Evenson2008DisplayWidget(results, recordsets, parent)
