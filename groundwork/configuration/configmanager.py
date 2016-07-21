import types
import errno
from pathlib import Path
import logging

from groundwork.configuration.exceptions import InvalidParameter
from groundwork.configuration.config import Config


class ConfigManager:

    def __init__(self, config_files=[]):
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
            except FileNotFoundError:
                self.log.warning("Config-file not found %s" % file)
                continue
            else:
                absolute_files.append(str(absolute_file))

        self.config_files = absolute_files

    def load(self):
        """
        Creates a configuration dictionary from all files in self.files and set the dictionary items as
        attributes of the class.
        """

        config = Config()

        for config_file in self.config_files:
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

