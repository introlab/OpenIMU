from PySide6.QtWidgets import (
    QWidget,
)
from abc import abstractmethod


class BaseConfigWidget(QWidget):

    def __init__(self, params: dict, parent: QWidget = None):
        QWidget.__init__(self, parent=parent)
        self.params = params

    @abstractmethod
    def get_params(self):
        """Return the parameters for the algorithm."""
        pass
