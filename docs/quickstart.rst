Quickstart
==========

Applications
------------

Create an app
~~~~~~~~~~~~~
Create a file named **my_app.py** and add the following code::

    from groundwork import App

    if __name__ == "__main__":
        my_app = App()
        my_app.activate(["GwPluginInfo"])
        my_app.commands.start_cli()

This code performs the following actions:

 * It creates a groundwork application app via ``my_app = App()``
 * It activates the plugin :class:`~groundwork.plugins.gw_plugin_info.GwPluginInfo`, which is part of groundwork itself.
    * During activation, GWPluginInfo registers a command called :command:`plugin_list` by its own.
 * It starts the command line interface

Run an app
~~~~~~~~~~
Open a command line interface, change to folder, which contains **my_app.py**, and execute::

    python my_app.py

This will start groundwork and its command line interface.

Because no command was added as parameter, groundwork complains about it.
To change this, simply add the needed command ::

    python my_app.py plugin_list

This will print a list of all available plugins, including some helpful information about them.

Plugins
-------

Activate registered plugins
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Activating already registered plugins like :class:`~groundwork.plugins.gw_plugin_info.GwPluginInfo` is easy.
All you need to know is the name of a plugin.::

    my_app.activate(["GwPluginInfo", "GwCommandsInfo", "GwSignalInfo"])

groundwork knows these names, because it automatically scans the used python environment for packages, which are
providing groundwork plugins. See :ref:`plugin_registration` for more details or :ref:`packaging` for using
this mechanism for own plugins.

Create own plugins
~~~~~~~~~~~~~~~~~~

The easiest way of creating a groundwork plugin is by defining a class, which inherits from
:class:`~groundwork.patterns.gw_base_pattern.GwBasePattern`.
But before activation, it also needs to be registered, what can be done during application initialisation::

    from groundwork import App
    from groundwork.patterns import GwBasePattern

    class MyPlugin(GwBasePattern):
        def __init__(self, app, **kwargs):
            self.name = "My Plugin"
            super().__init__(app, **kwargs)

        def activate(self): pass

        def deactivate(self): pass


    my_app = App(plugins=[MyPlugin])    # Register your plugin class
    my_app.activate(["My Plugin"])      # And activate it

You can also use the plugin object itself to perform the activation::

    # Instead of
    # my_app = App(plugins=[MyPlugin])
    # my_app.activate(["My Plugin"])
    my_app = App()
    my_plugin = MyPlugin(app=my_app)
    my_plugin.activate()

.. note::
    If a plugin inherits from any pattern, :class:`~groundwork.patterns.gw_base_pattern.GwBasePattern` is no longer
    needed as the pattern itself does already inherit from this class.

.. warning::
    The ``__init__`` routine of a plugin class **must** always set a name and call the next ``__init__`` routine in the
    inheritance chain (in this order!).

    Also make sure that your ``__init__`` can handle **app** as the first argument and
    additional, optional keyword arguments.

    If this is missed, the patterns and their objects are not initialized and configured the right way.

    So always use::

        def __init__(self, app, **kwargs):
            self.name = "My Plugin"
            super().__init__(app, **kwargs)


Patterns
--------

Using patterns
~~~~~~~~~~~~~~
Patterns are used to inject new functionality to a plugin. There are patterns for registering commands, generating
different types of documentation, activating web support and much more.

A plugin can inherit multiple patterns::

    class MyPlugin(GwCommandPattern, GwDocumentPattern):
        def __init__(self, app, **kwargs):
            self.name = "My Plugin"
            super().__init__(app, **kwargs)

This code example gives MyPlugin functions to register new commands and new documents.

If your are using a coding environment with code completion, just type ``self.`` to see all available functions
, including the inherited ones.

Writing patterns
~~~~~~~~~~~~~~~~

A pattern is more or less a plugin without any **activation** or **deactivation** function. Like plugins, it must
also inherit from :class:`~groundwork.patterns.gw_base_pattern.GwBasePattern`.

A pattern is allowed to multiply inherit from other patterns as well.

You can find an example with multiple inheritance in the :ref:`Pattern Example Code <pattern_example>`.



