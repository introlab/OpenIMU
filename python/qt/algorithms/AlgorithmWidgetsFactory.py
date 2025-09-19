from abc import ABC, abstractmethod
from PySide6.QtWidgets import QTableWidgetItem, QWidget
from PySide6.QtCore import Slot, Signal, Qt
from libopenimu.algorithms.BaseAlgorithm import BaseAlgorithmFactory


class AlgorithmWidgetsFactory(ABC):

    # Will hold all factories
    factories: list["AlgorithmWidgetsFactory"] = []

    def __init__(self, base_factory: BaseAlgorithmFactory):
        self.base_factory = base_factory

    def name(self):
        return self.base_factory.name()

    def unique_id(self):
        return self.base_factory.unique_id()

    def params(self):
        return self.base_factory.params()

    def info(self):
        return self.base_factory.info()

    @staticmethod
    def register_factory(factory) -> "AlgorithmWidgetsFactory":
        AlgorithmWidgetsFactory.factories.append(factory)
        return factory

    @staticmethod
    def print_factories() -> None:
        for factory in AlgorithmWidgetsFactory.factories:
            print("factory name", factory.name())
            print("factory params", factory.params())
            print("factory info", factory.info())

    @staticmethod
    def get_factory_named(name) -> "AlgorithmWidgetsFactory | None":
        for factory in AlgorithmWidgetsFactory.factories:
            if factory.name() == name:
                return factory
        return None

    @staticmethod
    def get_factory_with_id(unique_id) -> "AlgorithmWidgetsFactory | None":
        for factory in AlgorithmWidgetsFactory.factories:
            if factory.unique_id() == unique_id:
                return factory
        return None

    @abstractmethod
    def build_config_widget(self, parent: QWidget) -> QWidget:
        pass

    @abstractmethod
    def build_display_widget(self, parent: QWidget, results, recordsets) -> QWidget:
        pass

    def build_data_table(self, results: dict):
        return self.base_factory.build_data_table(results)
