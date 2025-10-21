# All modules
__all__ = ['BaseAlgorithm', 'FreedsonAdult1998', 'Evenson2008', 'Fraysse2021']

# TODO Do something a little more dynamic
from .FreedsonAdult1998 import init as freedson1998_init
from .Evenson2008 import init as evenson2008_init
from .Fraysse2021 import init as fraysse2021_init

# Call all init
evenson2008_init()
freedson1998_init()
fraysse2021_init()

