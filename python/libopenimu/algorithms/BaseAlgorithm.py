"""

    Base Algorithm class
    @authors Dominic Létourneau
    @date 04/05/2018

"""

from abc import abstractmethod

class BaseAlgorithm:
    def __init__(self):
        pass


class BaseAlgorithmFactory:
    factories = list()

    def __init__(self):
        pass

    @staticmethod
    def register_factory(factory):
        BaseAlgorithmFactory.factories.append(factory)
        return factory

    @staticmethod
    def print_factories():
        for factory in BaseAlgorithmFactory.factories:
            print('factory name', factory.name())
            print('factory params', factory.params())

    def create(self, params: dict):
        return None

    @abstractmethod
    def params(self):
        pass

    @abstractmethod
    def name(self):
        pass
