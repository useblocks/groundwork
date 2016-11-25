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
   ``my_app.plugins.deactivate()``.
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
        def __init__(self, app, **kwargs):
            self.name = "My Plugin"
            super().__init__(app, **kwargs)

        def activate(self): pass

        def deactivate(self): pass


.. warning::

    It is very important to call the ``__init__`` routine of parent classes. Otherwise they can't deliver functions
    and objects, which you may need. Also no signals are registered, which inform interested functions when your
    plugin gets activated or deactivated. So no automatic cleanup would happen, like erasing all registered
    commands of your plugin.

    Also make sure that your ``__init__`` can handle **app** as the first argument and
    additional, optional keyword arguments.

Provided variables
~~~~~~~~~~~~~~~~~~~

The groundwork :class:`~groundwork.patterns.gw_base_pattern.GwBasePattern`:: creates the following variables for your
plugin and makes them directly available:

* **self.path**: The absolute path of the python-file, which contains your plugin (directory + file name)
* **self.dir**: The absolute directory, which contains your plugin (directory only)
* **self.file**: The name of the file, which contains your plugin (file name only)
* **self.version**: An initial version (0.0.1), if this was not set by your plugin during initialisation
* **self.active**: True, if the plugin got activated.
* **self.needed_plugins**: Empty tuple, if it was not set by your plugin during initialisation

Using signals and receivers
~~~~~~~~~~~~~~~~~~~~~~~~~~~
You are free to add signals or connect receivers to them::

    from groundwork.patterns import GwBasePattern

    class MyPlugin(GwBasePattern):
        def __init__(self, app, **kwargs):
            self.name = "My Plugin"
            super().__init__(app, **kwargs)

        def activate(self):
            self.signals.register(signal="My signal",
                                  description="Informing about something")

            self.signals.connect(receiver="My signal receiver",
                                 signal="My signal",
                                 function=self.fancy_stuff,
                                 description="Doing some fancy stuff")

        def fancy_stuff(plugin, **kwargs):
            print("FANCY STUFF!!! " * 50)

For more details about signals, please read :ref:`signals`.

.. note::
    Each plugin sends automatically signals when it gets activated or deactivated.
    The used signals are: plugin_activate_pre, plugin_activate_post, plugin_deactivate_pre and plugin_deactivate_post.

    Please see :ref:`signals` for more information.

.. _plugin_patterns:

Using patterns
--------------
:ref:`Patterns <patterns>` can be used to extend your plugin with new functions and objects.

groundwork itself provides 4 patterns:

    * :class:`~groundwork.patterns.gw_base_pattern.GwBasePattern`
    * :class:`~groundwork.patterns.gw_commands_pattern.GwCommandsPattern`
    * :class:`~groundwork.patterns.gw_documents_pattern.GwDocumentsPattern`
    * :class:`~groundwork.patterns.gw_shared_objects_pattern.GwSharedObjectsPattern`

You can load multiple patterns into your plugin::

    from groundwork.patterns import GwCommandsPattern, GwDocumentsPattern, GwSharedObjectsPattern

    # GwBasePattern is no longer needed, because the used patterns already inherit from it.
    class MyPlugin(GwCommandsPattern, GwDocumentsPattern, GwSharedObjectsPattern):
        def __init__(self, app, **kwargs):
            self.name = "My Plugin"
            super().__init__(app, **kwargs)

        def activate(self):
            self.commands.register(...)
            self.documents.register(...)
            self.shared_objects.register(...)

For more information about these patterns, please read the related chapters: :ref:`commands`, :ref:`documents`
and :ref:`shared_objects`.


.. _plugin_logging:

Logging
-------
Each plugin has its own logger, which name is the name of the plugin. It is accessible via ``self.log`` inside a plugin
class::

    from groundwork.patterns import GwBasePattern

    class MyPlugin(GwBasePattern):
        def __init__(self, app, **kwargs):
            self.name = "My Plugin"
            super().__init__(app, **kwargs)
            self.log.info("Initialisation done for %s" % self.name)

        def activate(self):
            self.log.debug("Starting activation")
            self.log.info("Activation done")

For each logger, and therefore for each plugin, it is possible to register handlers to monitor specific plugins
and log messages in detail.

For instance: Store all messages of "My Plugin" inside a file called "my_plugin.log".
All other messages go to "app.log".

For details how to configure groundworks logging, please see :ref:`logging configuration <logging_configuration>`.



.. _plugin_dependencies:

Plugin dependencies
-------------------

A plugin can have dependencies to other plugins and it needs to be sure that these plugins are activated in the current
app.

Therefore a plugin can specify the names of the needed plugins and groundwork cares about their activation::

    from groundwork.patterns import GwBasePattern

    class MyPlugin(GwBasePattern):
        def __init__(self, app, **kwargs):
            self.name = "My Plugin"
            self.needed_plugins = ("AnotherPlugin", "AndAnotherPlugin")
            super().__init__(app, **kwargs)

During plugin activation, groundwork does the following:

    * Read in ``self.needed_plugins``
    * For each plugin name

      * Check, if a plugin with this name exists in app.plugins

        * If yes: activate it (if not done yet)
        * If no: check for plugin classes with this name in app.plugin.classes

          * If yes: Initiated and activate it
          * If now: Throw error







