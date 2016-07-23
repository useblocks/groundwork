groundwork
==========

groundwork is a plugin framework for Python.

It  enables an application to activate and deactivate plugins during runtime and to control dynamic plugin
behaviors like plugin status, used signals, registered commands and much more.

groundwork is designed to support any kind of application: command line scripts, desktop programs or web applications.
This is achieved by handling library functions and their dependencies inside plugins and their patterns.

The functionality of a plugin can be easily extended by the usage of inheritable patterns.
Based on this,  groundwork supports developers with time-saving out-of-the box solutions for own plugins:

 * Registration of commands for command line interfaces.
 * Registration of signals and receivers for loose inter-plugin communication.
 * Registration of shared objects to provide and request any kind of shared content.
 * Registration of static and dynamic documents for documentation purposes.




Example
-------

The following code defines a plugin with command line support and creates a groundwork application, which activates
this plugin: ::

    from groundwork import App
    from groundwork.patterns import GwCommandsPattern

    class MyPlugin(GwCommandsPattern):
        def _init_(self, *args, **kwargs):
            self.name = "My Plugin"
            super().__init__(*args, **kwargs)

        def activate(self):
            self.commands.register(command='hello',
                                   description='prints "hello world"',
                                   function=self.greetings)

        def greetings(self):
            print("Hello world")

    if __name__ == "__main__":
        my_app = App(plugins=[MyPlugin])        # Creates application and registers MyPlugin
        my_app.plugins.activate(["My Plugin"])  # Initialise and activates 'My Plugin'
        my_app.commands.start_cli()             # Starts the command line interface

On a command line the following commands can be used now: ::

    python my_app.py hello      # Prints 'Hello world'
    python my_app.py            # Prints a list of available commands
    python my_app.yp hello -h   # Prints some help text for the command hello

User's Guide
------------

.. toctree::
   :maxdepth: 2

   foreword
   installation
   quickstart
   tutorial
   plugins_patterns
   signals
   shared_objects
   cli
   documentation
   contribute

API Reference
-------------

.. toctree::
   :maxdepth: 2

   api

