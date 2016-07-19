groundwork
==========

groundwork is plugin framework for Python and enables an application to activate and deactivate plugins during
application runtime.

For plugins it provides some out-of-the box solutions for:

 * Registration of commands for command line interfaces.
 * Registration for signals and receivers for loose inter-plugin communication.
 * Registration of shared objects to provide and request any kind of shared content.
 * Registration of static and dynamic documents for documentation purposes.

groundwork and its plugins are highly expansible by the usage of existing patterns, like GwFlask and GwSqlAlchemy.


Example
-------

The following code creates a groundwork app and a single plugin.::

    from groundwork import GwApp
    from groundwork.patterns import GwCommandsPattern, GwSignalsPattern

    class MyPlugin(GwCommandsPattern, GwSignalsPattern):
        def _init_(self, *args, **kwargs):
            self.name = "My first plugin"
            super().__init__(*args, **kwargs)

        def activate(self):
            self.commands.register(name='hello',
                                   description='prints "hello world"',
                                   function=self.greetings)

            self.signals.register(signal='hi',
                                  description='Say "hi" to all interested plugins')

            self.signals.connect(receiver='hi receiver',
                                 signal='hi',
                                 function=self.greetings,
                                 description='prints "Hello world"')

        def greetings(self):
            print("Hello world")

    if __name__ == "__main__":
        my_app = GwApp('my_config.py')  # Creates the app and loads the config
        my_app.load_plugins(MyPlugin)   # Loads and activates 'MyPlugin'
        my_app.signals.send('hi')       # Will print 'Hello world'
        my_app.cli()                    # Starts the command line interface

Open a command line interface and make some tests::

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
   communication
   cli
   documentation

API Reference
-------------

.. toctree::
   :maxdepth: 2

   api

