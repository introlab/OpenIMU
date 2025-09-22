"""

Base Algorithm class
@authors Dominic Létourneau
@date 04/05/2018

"""

from abc import abstractmethod, ABC
from libopenimu.db.DBManager import DBManager


class BaseAlgorithm(ABC):

    def __init__(self, params: dict):
        self.params = params
        self.configure(params)

    @abstractmethod
    def configure(self, params: dict):
        pass

    @abstractmethod
    def calculate(self, manager: DBManager, recordsets: list) -> dict:
        pass


class BaseAlgorithmFactory(ABC):  # (QObject):
    # Will hold all factories
    factories: list["BaseAlgorithmFactory"] = []

    def __init__(self):
        pass

    @staticmethod
    def factory_count() -> int:
        return len(BaseAlgorithmFactory.factories)

    @staticmethod
    def register_factory(factory) -> "BaseAlgorithmFactory":
        BaseAlgorithmFactory.factories.append(factory)
        return factory

    @staticmethod
    def print_factories() -> None:
        for factory in BaseAlgorithmFactory.factories:
            print("factory name", factory.name())
            print("factory params", factory.params())
            print("factory info", factory.info())

    @staticmethod
    def get_factory_named(name) -> "BaseAlgorithmFactory | None":
        """
        Get a factory with its name
        :param name: str
        :return BaseAlgorithmFactory | None:
        """
        for factory in BaseAlgorithmFactory.factories:
            if factory.name() == name:
                return factory
        return None

    @staticmethod
    def get_factory_with_id(unique_id) -> "BaseAlgorithmFactory | None":
        """
        Get a factory with its unique ID
        :param unique_id: int
        :return BaseAlgorithmFactory | None:
        """
        for factory in BaseAlgorithmFactory.factories:
            if factory.unique_id() == unique_id:
                return factory
        return None

    @abstractmethod
    def unique_key(self) -> str:
        """
        Should return a unique string key for that factory
        :return str:
        """
        pass

    @abstractmethod
    def create(self, params: dict) -> "BaseAlgorithm":
        pass

    @abstractmethod
    def params(self) -> dict:
        """
        Should return a dict with the parameters and their default values
        :return dict:
        """
        return {}

    @abstractmethod
    def results(self) -> list:
        """
        Should return a dict with the results structure
        :return dict:
        """
        return []

    @abstractmethod
    def name(self) -> str:
        """
        Should return the name of the algorithm
        :return str:
        """
        return "BaseAlgorithm"

    @abstractmethod
    def unique_id(self) -> int:
        """
        Should return a unique identifier for the algorithm
        :return int:
        """
        return 0

    @abstractmethod
    def info(self) -> dict:
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

    # This method is used to build a table of results
    # Returns a dictionary: "headers" -> List of headers (one per column)
    #                       "data_names" -> List of data names (one per row)
    #                       "data" -> List of list of data (one list per row, then one list by column)
    @abstractmethod
    def build_data_table(self, results):
        return {"headers": [], "data_names": [], "data": []}
