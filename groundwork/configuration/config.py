import logging


class Config:
    """
    Stores all configuration parameters and handles access to it.

    Example::
        import groundwork
        my_app = groundwork.App(config_files=["my_config.py"])
        param = my_app.config.get("MY_PARAM", default="Not set")

        my_app.config.set("MY_PARAM_2, value=12345)
        param_2 = my_app.config.get("MY_PARAM_2")
    """
    def __init__(self):

        self._log = logging.getLogger(__name__)

    def get(self, name, default=None):
        """
        Returns an existing configuration parameter.
        If not available, the default value is used.

        :param name: Name of the configuration parameter
        :param default: Default value, if parameter is not set
        """
        return getattr(self, name, default)

    def set(self, name, value, overwrite=False):
        """
        Sets a new value for a given configuration parameter.

        If it already exists, an Exception is thrown.
        To overwrite an existing value, set overwrite to True.

        :param name: Unique name of the parameter
        :param value: Value of the configuration parameter
        :param overwrite: If true, an existing parameter of *name* gets overwritten without warning or exception.
        :type overwrite: boolean
        """
        if hasattr(self, name):
            if overwrite:
                setattr(self, name, value)
            else:
                self._log.warning("Configuration parameter %s exists and overwrite not allowed" % name)
                raise Exception("Configuration parameter %s exists and overwrite not allowed" % name)
        else:
            setattr(self, name, value)
        return getattr(self, name)
