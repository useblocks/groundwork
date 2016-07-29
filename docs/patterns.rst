.. _patterns:

Patterns
========

Patterns are used to extend the functionality of a plugin. So most patterns provides use-case specific functions
like register commands, store users and more.

Using patterns
--------------

The usage of a pattern is defined by a plugin during its development.
The plugin itself decides to inherit from one or multiple patterns::

    from groundwork.patterns import GwCommandsPattern, GwDocumentsPattern, GwSharedObjects

    class MyPlugin(GwCommandsPattern, GwDocumentsPattern):          # Used Patterns
        def __init__(app, **kwargs):
            self.name = "My Plugin"
            self.super().__init__(app, **kwargs)

This inheritance can not be changed during runtime or via configuration. It's hard coded inside a plugins code.


Developing own patterns
-----------------------

A pattern is more or less a plugin without any **activation** or **deactivation** function. Like plugins, it must
also inherit from :class:`~groundwork.patterns.gw_base_pattern.GwBasePattern`.

.. _pattern_example:

A pattern is allowed to multiply inherit from other patterns as well. Example::

    from groundwork import App
    from groundwork.patterns import GwCommandPattern, GwDocumentPattern

    class MyPattern(GwCommandPattern, GwDocumentPattern):
        def __init__(app, **kwargs):
            super().__init__(app, **kwargs)

        def my_register(command_name, command_func):
        """ Registers and documents a new command"""
            self.commands.register(command_name, command_func, ...)
            self.documents.register(command_name, ...)

    class MyPlugin(MyPattern):
        def __init__(app, **kwargs):
            self.name = "My Plugin"
            super().__init__(app, **kwargs)

        def activate():
            # Your new function
            self.my_register(command_name = "print_me", command_func = self.print_me)

            # But you also have access to all functions from
            # GwCommandPattern and GwDocumentPattern
            self.commands.register(...)
            self.documents.register(...)

        def print_me():
            print("I'm %s." % self.name)

    my_app = App([MyPlugin])
    my_app.activate(["My Plugin"])


.. _pattern_logging:

Logging
-------

Patterns are using the same logger as the plugin, which has inherit from this pattern. Example::

    from groundwork import App
    from groundwork.patterns import GwBasePattern


    class MyPattern(GwBasePatter):
        def __init__(app, **kwargs):
            super().__init__(app, **kwargs)

            self.log.debug("Initialising pattern 'MyPattern'")


    class MyPlugin(MyPattern):
        def __init__(app, **kwargs):
            self.name = "My Plugin"
            super().__init__(app, **kwargs)

            self.log.info("Initialising MyPlugin")


    class AnotherPlugin(MyPattern):
        def __init__(app, **kwargs):
            self.name = "Another Plugin"
            super().__init__(app, **kwargs)

            self.log.info("Initialising AnotherPlugin")


    my_app = App(plugins=[MyPlugin, AnotherPlugin])
    my_app.plugins.activate(["My Plugin", "Another Plugin"])

    my_app.log.info("Start application")


The output of this would be like::

    MyPlugin        DEBUG   Initialising pattern 'MyPattern'
    MyPlugin        INFO    Initialising MyPlugin
    AnotherPlugin   DEBUG   Initialising pattern 'MyPattern'
    AnotherPlugin   INFO    Initialising MyPlugin
    groundwork      INFO    Start application

For more details about logging see :ref:`Plugin Logging <plugin_logging>`
and :ref:`Application Logging <application_logging>`
