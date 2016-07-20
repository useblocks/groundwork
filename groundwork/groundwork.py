import logging
import logging.config
import sys
import os

from .configuration import ConfigManager as ConfigManager
from .pluginmanager import PluginManager
from .sharedobject import SharedObjectManager


class App:
    """
    Application object for a groundwork app.
    Loads configurations, configures logs, initialize and activates plugins and provides managers for
    shared objects and functions.

    Performed steps during start up:
      1. load configuration
      2. configure logs
      3. get valid groundwork plugins
      4. activate configured plugins
    """

    def __init__(self, config_files=[], plugins=[], strict=False):
        self.log = logging.getLogger("groundwork")
        self._configure_logging()
        self.log.info("Initializing groundwork")
        self.log.info("Reading configuration")
        self.config = ConfigManager(config_files).load()
        self._configure_logging(self.config.get("GROUNDWORK_LOGGING"))
        self.path = os.path.abspath(self.config.get("BASE_PATH", None) or os.getcwd())

        self.plugins = PluginManager(app=self, plugins=plugins, strict=strict)
        self.shared_objects = SharedObjectManager()

    def _configure_logging(self, logger_dict=None):
        self.log.debug("Configure logging")
        if logger_dict is None:
            self.log.debug("No logger dictionary defined. Doing default logger configuration")
            formatter = logging.Formatter("%(name)s - %(asctime)s - [%(levelname)s] - %(module)s - %(message)s")
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setLevel(logging.DEBUG)
            stream_handler.setFormatter(formatter)
            self.log.addHandler(stream_handler)
            self.log.setLevel(logging.INFO)
        else:
            self.log.debug("Logger dictionary defined. Loading dictConfig for logging")
            logging.config.dictConfig(logger_dict)
            self.log.debug("dictConfig loaded")

    def load_plugins(self, plugins=[]):
        self.plugins.load(plugins)



