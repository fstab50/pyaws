from pyaws._version import __version__ as version


__author__ = 'Blake Huber'
__version__ = version
__credits__ = []
__license__ = "GPL-3.0"
__maintainer__ = "Blake Huber"
__email__ = "blakeca00@gmail.com"
__status__ = "Development"


# the following imports require __version__  #

try:
    import logging

    # shared, global logger object
    logger = logging.getLogger(__version__)

except Exception:
    pass
