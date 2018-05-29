"""

    Base Algorithm class
    @authors Dominic Létourneau
    @date 04/05/2018

"""

from abc import abstractmethod
from libopenimu.models.Recordset import Recordset

class BaseAlgorithm:
    def __init__(self, params):
        self.configure(params)

    @abstractmethod
    def configure(self, params: dict):
        pass

    @abstractmethod
    def calculate(self, recordsets : list):
        pass


class BaseAlgorithmFactory:
    # Will hold all factories
    factories = list()

    def __init__(self):
        pass

    @staticmethod
    def factory_count():
        return len(BaseAlgorithmFactory.factories)

    @staticmethod
    def register_factory(factory):
        BaseAlgorithmFactory.factories.append(factory)
        return factory

    @staticmethod
    def print_factories():
        for factory in BaseAlgorithmFactory.factories:
            print('factory name', factory.name())
            print('factory params', factory.params())
            print('factory description', factory.description())

    @staticmethod
    def get_factory_named(name):
        for factory in BaseAlgorithmFactory.factories:
            if factory.name() == name:
                return factory
        return None

    @abstractmethod
    def create(self, params: dict):
        return None

    @abstractmethod
    def params(self):
        pass

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def required_sensors(self):
        return []
