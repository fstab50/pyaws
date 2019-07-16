import os
import inspect
from pyaws._version import __version__ as version
from pyaws import environment


__author__ = 'Blake Huber'
__version__ = version
__credits__ = []
__license__ = "GPL-3.0"
__maintainer__ = "Blake Huber"
__email__ = "blakeca00@gmail.com"
__status__ = "Development"

PACKAGE = 'pyaws'
enable_logging = True
log_mode = 'STREAM'          # log to cloudwatch logs
log_filename = 'pyaws.log'
log_dir = os.getenv('HOME') + '/logs'
log_path = log_dir + '/' + log_filename


log_config = {
    "PROJECT": {
        "PACKAGE": PACKAGE,
        "CONFIG_VERSION": __version__,
    },
    "LOGGING": {
        "ENABLE_LOGGING": enable_logging,
        "LOG_FILENAME": log_filename,
        "LOG_DIR": log_dir,
        "LOG_PATH": log_path,
        "LOG_MODE": log_mode,
        "SYSLOG_FILE": False
    }
}


## the following imports require __version__  ##

try:

    from libtools import Colors
    from libtools import logd

    # shared, global logger object
    logd.local_config = log_config
    logger = logd.getLogger(__version__)

    # stream logger
    log_config['LOGGING']['LOG_MODE'] = 'STREAM'
    logd.local_config = log_config
    streamlogger = logd.getLogger(__version__)

    from pyaws.core import exit_codes

except Exception as e:
    fx = inspect.stack()[0][3]
    streamlogger.exception('{}: Uknown failure during initialization of pyaws library: {e}'.format(fx, e))
