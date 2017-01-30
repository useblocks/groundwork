"""
groundwork module provides mainly the App class, which is a container for all functions and
data related to plugins and their patterns.
"""
from __future__ import absolute_import
import logging
import logging.config
import sys
import os

from groundwork.configuration.configmanager import ConfigManager
from groundwork.pluginmanager import PluginManager
from groundwork.signals import SignalsApplication


class App(object):
    """
    Application object for a groundwork app.
    Loads configurations, configures logs, initialises and activates plugins and provides managers.

    Performed steps during start up:
      1. load configuration
      2. configure logs
      3. get valid groundwork plugins
      4. activate configured plugins

    :param config_files: List of config files, which shall be loaded
    :type config_files: list of str
    :param plugins: List of plugins, which shall be registered
    :type plugins: Plugin-Classes, based on :class:`~groundwork.patterns.gw_base_pattern.GwBasePattern`
    :param strict: If true, Exceptions are thrown, if a plugin can not be initialised or activated.
    """
    def __init__(self, config_files=None, plugins=None, strict=False):
        if config_files is None:
            config_files = []

        self.strict = strict

        #: logging object for sending log messages. Example::
        #:
        #:  from groundwork import App
        #:  my_app = App()
        #:  my_app.log.debug("Send debug message")
        #:  my_app.log.error("Send error....")
        self.log = logging.getLogger("groundwork")

        self._configure_logging()
        self.log.info("Initializing groundwork")
        self.log.info("Reading configuration")

        #: Instance of :class:`~groundwork.configuration.configmanager.ConfigManager`.
        #: Used to load different configuration files and create a common configuration object.
        self.config = ConfigManager().load(config_files)

        #: Absolute application path. Is configurable by parameter "APP_PATH" of a configuration file.
        #: If not given, the current working  directory is taken.
        #: The path is used to calculate absolute paths for tests, documentation and much more.
        self.path = self.config.get("APP_PATH", None)
        if self.path is None:
            self.path = os.getcwd()
        elif not os.path.isabs(self.path):
            self.path = os.path.abspath(self.path)
            self.log.warning("Given APP_PATH is relative, calculated following, absolute path: %s" % self.path)
        elif not os.path.exists(self.path):
            raise IOError("Given APP_PATH does not exist: %s" % self.path)

        self._configure_logging(self.config.get("GROUNDWORK_LOGGING"))

        #: Name of the application. Is configurable by parameter "APP_NAME" of a configuration file.
        self.name = self.config.get("APP_NAME", None) or "NoName App"

        #: Instance of :class:`~groundwork.signals.SignalsApplication`. Provides functions to register and fire
        # signals or receivers on application level.
        self.signals = SignalsApplication(app=self)

        self.signals.register("plugin_activate_pre", self,
                              "Gets send right before activation routine of a plugins will be executed")
        self.signals.register("plugin_activate_post", self,
                              "Gets send right after activation routine of a plugins was executed")
        self.signals.register("plugin_deactivate_pre", self,
                              "Gets send right before deactivation routine of a plugins will be executed")
        self.signals.register("plugin_deactivate_post", self,
                              "Gets send right after deactivation routine of a plugins was executed")

        #: Instance of :class:`~groundwork.pluginmanager.PluginManager`- Provides functions to load, activate and
        # deactivate plugins.
        self.plugins = PluginManager(app=self)

        if plugins is not None:
            self.plugins.classes.register(plugins)

    def _configure_logging(self, logger_dict=None):
        """
        Configures the logging module with a given dictionary, which in most cases was loaded from a configuration
        file.

        If no dictionary is provided, it falls back to a default configuration.

        See `Python docs
        <https://docs.python.org/3.5/library/logging.config.html#logging.config.dictConfig>`_ for more information.

        :param logger_dict: dictionary for logger.
        """
        self.log.debug("Configure logging")

        # Let's be sure, that for our log no handlers are registered anymore
        for handler in self.log.handlers:
            self.log.removeHandler(handler)
        if logger_dict is None:
            self.log.debug("No logger dictionary defined. Doing default logger configuration")
            formatter = logging.Formatter("%(name)s - %(asctime)s - [%(levelname)s] - %(module)s - %(message)s")
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setLevel(logging.WARNING)
            stream_handler.setFormatter(formatter)
            self.log.addHandler(stream_handler)
            self.log.setLevel(logging.WARNING)
        else:
            self.log.debug("Logger dictionary defined. Loading dictConfig for logging")
            logging.config.dictConfig(logger_dict)
            self.log.debug("dictConfig loaded")
