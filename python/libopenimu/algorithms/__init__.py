# All modules
__all__ = ['BaseAlgorithm', 'FreedsonAdult1998', 'Evenson2008']

# TODO Do something a little more dynamic
from .FreedsonAdult1998 import init as freedson1998_init
from .Evenson2008 import init as evenson2008_init

# Call all init
evenson2008_init()
freedson1998_init()

