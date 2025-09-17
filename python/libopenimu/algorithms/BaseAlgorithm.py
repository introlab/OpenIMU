"""

Base Algorithm class
@authors Dominic Létourneau
@date 04/05/2018

"""

from abc import abstractmethod, ABC
from libopenimu.db.DBManager import DBManager

# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
# from PySide6.QtCore import QObject


class BaseAlgorithm(ABC):

    def __init__(self, params: dict):
        self.params = params
        self.configure(params)

    @abstractmethod
    def configure(self, params: dict):
        pass

    @abstractmethod
    def calculate(self, manager: DBManager, recordsets: list):
        pass


class BaseAlgorithmFactory(ABC):  # (QObject):
    # Will hold all factories
    factories: list["BaseAlgorithmFactory"] = []

    def __init__(self):
        pass
        # QObject.__init__(self)

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
            print("factory name", factory.name())
            print("factory params", factory.params())
            print("factory info", factory.info())

    @staticmethod
    def get_factory_named(name):
        for factory in BaseAlgorithmFactory.factories:
            if factory.name() == name:
                return factory
        return None

    @staticmethod
    def get_factory_id(unique_id):
        for factory in BaseAlgorithmFactory.factories:
            if factory.unique_id() == unique_id:
                return factory
        return None

    @abstractmethod
    def create(self, params: dict):
        pass

    @abstractmethod
    def params(self):
        return {}

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def unique_id(self):
        pass

    @abstractmethod
    def info(self):
        """
        Should return a dict with
        'description' : string
        'author' : string
        'version' : string
        'name' : string
        'reference': string
        '
        :return dict:
        """
        pass

    @abstractmethod
    def required_sensors(self):
        return []

    @abstractmethod
    def build_data_table(self, results):
        return {"headers": [], "data_names": [], "data": []}

    # @abstractmethod
    # def build_display_widget(self, parent_widget: QWidget, results, recordsets):
    #     return QWidget()

    # @abstractmethod
    # def build_config_widget(self, parent_widget: QWidget, default_params: dict = None):
    #     layout = QVBoxLayout()
    #     label = QLabel(self.tr("No settings available for that algorithm"))
    #     layout.addWidget(label)

    #     base_widget = QWidget(parent_widget)
    #     base_widget.setLayout(layout)
    #     return base_widget

    # # This method is used to build a table of results
    # # Returns a dictionary: "headers" -> List of headers (one per column)
    # #                       "data_names" -> List of data names (one per row)
    # #                       "data" -> List of list of data (one list per row, then one list by column)
