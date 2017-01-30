import types
from pathlib import Path
import logging
import os

from groundwork.configuration.exceptions import InvalidParameter
from groundwork.configuration.config import Config


class ConfigManager:
    """
    Loads different configuration files and sets their attributes as attributes of its own instance.

    A configuration file must be an importable python file.

    Only uppercase attributes are loaded. Everything else is ignored. Example::

        import os
        APP_NAME = "My APP"                     # Is used
        APP_PATH = os.path.abspath(".")         # Is used
        app_test = "test"                       # Is NOT used
        MY_OWN_VAR = "nice"                     # Is used
    """
    def __init__(self, config_files=[]):
        #: An instance of :class:`~groundwork.configuration.configmanager.Config` for storing all
        #: configuration parameters.
        self.config = None

        self.log = logging.getLogger(__name__)
        self.log.debug("Starting Configuration initialisation")
        self.invalid_parameters = ["FILES"]

        if isinstance(config_files, list):
            self.config_files = config_files
        else:
            raise TypeError("config_files must be a list of strings")

        absolute_files = []
        for file in config_files:
            if not isinstance(file, str):
                raise TypeError("config_files members must be strings")
            try:
                absolute_file = Path(file).resolve()
            except IOError:
                self.log.warning("Config-file not found %s" % file)
                continue
            else:
                absolute_files.append(str(absolute_file))

        self.config_files = absolute_files

    def load(self, config_files):
        """
        Creates a configuration instance from class :class:`~groundwork.configuration.configmanager.Config` from all
        files in self.files and set the dictionary items as attributes of of this instance.

        :return: Instance of :class:`~groundwork.configuration.configmanager.Config`
        """
        config = Config()

        for config_file in config_files:
            if not os.path.isabs(config_file):
                config_file = os.path.join(os.getcwd(), config_file)

            self.log.debug("Loading configuration from %s" % config_file)
            d = types.ModuleType('config')
            d.__file__ = config_file
            try:
                with open(config_file) as current_config_file:
                    exec(compile(current_config_file.read(), config_file, 'exec'), d.__dict__)
            except IOError as e:
                e.strerror = 'Unable to load configuration file (%s)' % e.strerror
                raise
            for key in dir(d):
                if key.isupper():
                    if key not in self.invalid_parameters:
                        setattr(config, key, getattr(d, key))
                    else:
                        raise InvalidParameter("%s is not allowed as name for a configuration parameter" % key)
        return config
