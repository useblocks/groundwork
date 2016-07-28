.. _plugins:

Plugins
=======
Plugins are used by groundwork to load specific functions into a groundwork :ref:`application <application>`.

In most cases a plugin should have a functional focus, like providing some documentation about signals or providing
some commands to the user to handle specific tasks on data.

A plugin can be activated and deactivated during runtime. And it can be loaded from python packages or from own code.

The following rules apply for each groundwork plugin.

 * A plugin contains code, documentation and tests.
 * A plugin provides routines for activation and deactivation during runtime.
 * A plugin inherits directly or indirectly from :class:`~groundwork.patterns.gw_base_pattern.GwBasePattern`.

During development of a plugin, :ref:`patterns <patterns>` can be used to extend its functionality or grant access
to specific objects, like a database engine to perform database actions.

Registration
------------
The registration of a plugin must happen by using the application::

    from groundwork import App

    my_app = App()
    my_app.plugins.activate(["GwPluginInfo"])

For more information please read :ref:`plugin_registration` of the chapter :ref:`application`.

Activation and Deactivation
---------------------------

Plugins can be activated and deactivated during runtime. There are two ways of doing this:

 * By the :func:`~groundwork.pluginmanager.PluginManager.activate`/
   :func:`~groundwork.pluginmanager.PluginManager.deactivate` function, accessible by ``my_app.plugins.activate()`` or
   ``my_app_plugins.deactivate()``.
 * By the activation/deactivation function of the plugin itself, accessible by ``my_plugin.activate()`` or
   ``my_plugin.deactivate()``.

For a code example, please take a look into :ref:`plugin_activation` and :ref:`plugin_deactivation` of the application
documentation.

Development of own plugins
--------------------------

To start the development of own plugins, simply create a new class and inherit from
:class:`~groundwork.patterns.gw_base_pattern.GwBasePattern`::

    from groundwork.patterns import GwBasePattern

    class MyPlugin(GwBasePattern):
        def __init__(app, **kwargs):
            self.name = "My Plugin"
            super().__init__(app, **kwargs)

        def activate(): pass

        def deactivate(): pass


.. warning::

    It is very important to call the ``__init__`` routine of parent classes. Otherwise they can't deliver functions
    and objects, which you may need. Also no signals are registered, which inform interested functions when your
    plugin gets activated or deactivated. So no automatic cleanup would happen, like erasing all registered
    commands of your plugin.

    Also make sure that your ``__init__`` can handle **app** as the first argument and
    additional, optional keyword arguments.

.. _plugin_logging:

Logging
-------