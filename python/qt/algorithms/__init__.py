# All modules
__all__ = [
    "AlgorithmWidgetsFactory",
    "Evenson2008WidgetsFactory",
    "Evenson2008ConfigWidget",
    "Evenson2008DisplayWidget",
    "FreedsonAdult1998WidgetsFactory",
    "FreedsonAdult1998ConfigWidget",
    "FreedsonAdult1998DisplayWidget",
]

from libopenimu.algorithms.BaseAlgorithm import BaseAlgorithmFactory
from qt.algorithms.AlgorithmWidgetsFactory import AlgorithmWidgetsFactory
from qt.algorithms.FreedsonAdult1998WidgetsFactory import (
    FreedsonAdult1998WidgetsFactory,
)
from qt.algorithms.Evenson2008WidgetsFactory import Evenson2008WidgetsFactory

# Register all factories
FreedsonAdult1998WidgetsFactory.register_factory(
    FreedsonAdult1998WidgetsFactory(
        BaseAlgorithmFactory.get_factory_named("Freedson Adult 1998")
    )
)

Evenson2008WidgetsFactory.register_factory(
    Evenson2008WidgetsFactory(BaseAlgorithmFactory.get_factory_named("Evenson 2008"))
)
