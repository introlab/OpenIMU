"""

    Base Algorithm class
    @authors Dominic Létourneau
    @date 04/05/2018

"""

from abc import abstractmethod
from libopenimu.models.Recordset import Recordset
from libopenimu.db.DBManager import DBManager

from PyQt5.QtWidgets import QWidget


class BaseAlgorithm:
    def __init__(self, params: dict):
        self.configure(params)

    @abstractmethod
    def configure(self, params: dict):
        pass

    @abstractmethod
    def calculate(self, manager: DBManager, recordsets : list):
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
            print('factory info', factory.info())

    @staticmethod
    def get_factory_named(name):
        for factory in BaseAlgorithmFactory.factories:
            if factory.name() == name:
                return factory
        return None

    @staticmethod
    def get_factory_with_id(id):
        for factory in BaseAlgorithmFactory.factories:
            if factory.unique_id() == id:
                return factory
        return None

    @abstractmethod
    def create(self, params: dict):
        self.configure(params)
        return None

    @abstractmethod
    def params(self):
        pass

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def unique_id(self):
        pass

    @abstractmethod
    def info(self):
        '''
        Should return a dict with
        'description' : string
        'author' : string
        'version' : string
        'name' : string
        'reference': string
        '
        :return dict:
        '''
        pass

    @abstractmethod
    def required_sensors(self):
        return []

    @abstractmethod
    def build_display_widget(self, parent_widget:QWidget, results, recordsets):
        return QWidget()
