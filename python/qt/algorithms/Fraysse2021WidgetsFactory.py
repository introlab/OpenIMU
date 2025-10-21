from PySide6.QtWidgets import QTableWidgetItem, QWidget
from qt.algorithms.AlgorithmWidgetsFactory import AlgorithmWidgetsFactory
from qt.algorithms.Fraysse2021ConfigWidget import Fraysse2021ConfigWidget


class Fraysse2021WidgetsFactory(AlgorithmWidgetsFactory):

    def __init__(self, base_factory):
        AlgorithmWidgetsFactory.__init__(self, base_factory)

    def build_config_widget(self, parent: QWidget) -> QWidget:
        return Fraysse2021ConfigWidget(self.params(), parent)

    def build_display_widget(self, parent: QWidget, results, recordsets) -> QWidget:
        pass
