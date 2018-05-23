# All modules
__all__ = ['BaseAlgorithm', 'FreedsonAdult1998']

# TODO Do something a little more dynamic
from .FreedsonAdult1998 import init as freedson1998_init

# Call all init
freedson1998_init()