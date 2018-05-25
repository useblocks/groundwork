.. _application:

Application
===========
The groundwork :class:`~groundwork.App` is a container mostly for configurations, plugins/patterns and
their needed objects.

Most attributes are added during runtime by patterns, which need a single instance of an object per application.
For instance: A list of registered commands, a database connection object, a web application.

To initialise a groundwork application, simply do::

    from groundwork import App

    my_app = App()

.. _configuration:

Configuration
-------------

groundwork can load multiple configuration files during application initialisation. These values are available via
``my_app.config.get("MY_CONFIG_PARAMETER")``.

It is also possible to reload the configuration or to extend it by additional configuration files during runtime::

    from groundwork import App

    my_app = App(config_files=["config1.py", "config2.py"])     # Load 2 config files
    my_app.config.load(["config3.py"])                          # Load a third config file

A configuration file must be python file, which defines variables on root level. Only variables with an uppercase name
are used for the groundwork configuration::

    # config1.py

    import os

    APP_NAME = "My awesome application"                 # Is used as config parameter

    config_file_location = __file__                     # Is not used as config parameter
    APP_PATH = os.path.dirname(config_file_location)    # Is used as config parameter

    APP_PLUGINS = [ "My Plugin",                        # Is used as config parameter
                    "GwPluginInfo",
                    "GwCommandInfo]


After application initialisation, the configuration can be used. For instance to activate needed plugins::

    from groundwork import APP

    my_app = App(config_files=["config1.py"])
    my_app.plugins.activate(my_app.config.get("APP_PLUGINS"))



.. _plugin_registration:

Plugin registration
-------------------

Before a plugin can be activated for a groundwork application, it must be registered.

groundwork does this registration automatically for all python packages in the current python environment.
For not-packaged plugins, they must be registered by the application developer her/himself.

Packaged plugins
~~~~~~~~~~~~~~~~
A packaged plugin is part of a python package, which provides a setup.py and was installed via
``python setup.py install`` or related pip/easy_install commands in the current python environment.

The package must use the entry_point **groundwork.plugin** and provide a class for each entry_point. Example from
the groundwork package itself::

    setup(
        name='groundwork',

        # A lot of other information....

        entry_points={
            'groundwork.plugin': [
                'gw_plugin_info = groundwork.plugins.gw_plugin_info:GwPluginInfo',
                'gw_signal_info = groundwork.plugins.gw_signal_info:GwSignalInfo',
                'gw_command_info = groundwork.plugins.gw_commands_info:GwCommandInfo'
            ]
        }
    )

During application initialisation, groundwork registers all plugins, which are provided by this way automatically.
They can be activated after app initialisation::

  from groundwork import App

  my_app = App()
  my_app.plugins.activate(["GwPluginInfo", "GwSignalInfo"])


Registration of own plugins
~~~~~~~~~~~~~~~~~~~~~~~~~~~
If a groundwork plugin is not part of a package and not made available via entry_point, it must be registered by
the application developer. This can be done during application initialisation or later::

    from groundwork import App
    from groundwork.patterns import GwBasePattern

    class MyPlugin(GwBasePattern):
        def __init__(self, app, **kwargs):
            self.name = "My Plugin"
            super().__init__(app, **kwargs)

        def activate(self): pass

        def deactivate(self): pass


    # Registration during initialisation
    my_app = App(plugins=[MyPlugin])

    # Registration after initialisation
    from my_module import AnotherPlugin
    my_app.plugins.classes.register([AnotherPlugin])

    # Activation
    my_app.plugins.activate(["My Plugin", "AnotherPlugin"])



.. _plugin_activation:

Plugin activation
-----------------

Before a plugin registers its commands, signals or anything else, it must be activated.

groundwork supports two ways of activation:

 * Activation by application
 * Activation by plugin

Here is an example, which demonstrates both ways::

    from groundwork import App
    from groundwork.patterns import GwBasePattern

    class MyPlugin(GwBasePattern):
        def __init__(self, app, **kwargs):
            self.name = "My Plugin"
            super().__init__(app, **kwargs)

        def activate(self): pass

        def deactivate(self): pass

    # Activation by application
    my_app = App(plugins=[MyPlugin])                        # Registration
    my_app.plugins.activate(["My Plugin"])                  # Activation

    # Activation by plugin
    my_plugin2 = MyPlugin(app=my_app, name="MyPlugin2")     # Registration
    my_plugin2.activate()                                   # Activation


.. _plugin_deactivation:

Plugin deactivation
-------------------
Like for plugin activation, also the plugin deactivation supports two ways of deactivating a plugin::

    # Follow up of the plugin activation example...

    # Deactivation by application
    my_app.deactivate(["MyPlugin"])

    # Deactivation by plugin
    my_plugin2.deactivate()

Handling errors
---------------

A plugin registration or activation can easily fail. Reasons may be bad code, missing dependencies,
already registered classes and more.

By default groundwork logs only a warning if a registration or activation fails.

You can ask groundwork to throw also an exception, if problems occur. This behavior can be activated by setting the
parameter ``strict=True`` during application initialisation::

    from groundwork import App

    class MyBadPlugin():
        pass

    my_app = App(strict=True)
    my_app.registers([MyBadPlugin])     # will throw an exception

    my_app.strict = False
    my_app.registers([MyBadPlugin])     # will log a warning only

.. _application_logging:

Logging
-------

A groundwork application provides its own logger object, which is available under ``my_app.log``::

    from groundwork import App

    my_app = App()
    my_app.log.info("Loading plugins")
    my_app.log.debug("Activating Plugin X")

This logger is used by most application related objects. Plugins have their own logger, which is available
under ``self.log`` inside an plugin class.

.. _logging_configuration:

Configuration
~~~~~~~~~~~~~

All loggers (application and plugins) can be configured by a configuration parameter called **GROUNDWORK_LOGGING**
inside a used configuration file.

The value of this parameter must be a dictionary. Its structure is described in the
`python documentation for logging <https://docs.python.org/3.5/library/logging.config.html#logging.config.dictConfig>`_.

Example of a configuration for groundwork logs::

    GROUNDWORK_LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'extended': {
                'format': "%(levelname)-8s %(name)-40s - %(asctime)s - %(message)s"
            },
            'debug': {
                'format': "%(name)s - %(asctime)s - [%(levelname)s] - %(module)s:%(funcName)s(%(lineno)s) - %(message)s"
            },
        },
        'handlers': {
            'default': {
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'level': 'DEBUG'
            },
            'console_stdout': {
                'formatter': 'extended',
                'class': 'logging.StreamHandler',
                'stream': sys.stdout,
                'level': 'DEBUG'
            },
            'file': {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "debug",
                "filename": "logs/app.log",
                "maxBytes": 1024000,
                "backupCount": 3,
                'level': 'DEBUG'
            },
            'file_my_plugin': {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "debug",
                "filename": "logs/my_plugin.log",
                "maxBytes": 1024000,
                "backupCount": 3,
                'level': 'DEBUG'
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': 'WARNING',
                'propagate': True
            },
            'groundwork': {
                'handlers': ['console_stdout', 'file'],
                'level': 'INFO',
                'propagate': False
            },
            'MyPlugin': {
                'handlers': ['console_stdout', 'file_my_plugin'],
                'level': 'DEBUG',
                'propagate': False
            },
        }
    }




