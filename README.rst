.. image:: https://img.shields.io/pypi/l/groundwork.svg
   :target: https://pypi.python.org/pypi/groundwork
   :height: 20px
.. image:: https://img.shields.io/pypi/pyversions/groundwork.svg
   :target: https://pypi.python.org/pypi/groundwork
   :height: 20px
.. image:: https://readthedocs.org/projects/groundwork/badge/?version=latest
   :target: http://groundwork.readthedocs.io/
   :height: 20px
.. image:: https://travis-ci.org/useblocks/groundwork.svg?branch=master
   :target: https://travis-ci.org/useblocks/groundwork
   :height: 20px
.. image:: https://coveralls.io/repos/github/useblocks/groundwork/badge.svg?branch=master
   :target: https://coveralls.io/github/useblocks/groundwork?branch=master
   :height: 20px
.. image:: https://img.shields.io/pypi/dm/groundwork.svg?style=flat
   :target: https://pypi.python.org/pypi/groundwork
   :height: 20px
.. image:: https://img.shields.io/pypi/v/groundwork.svg
   :target: https://pypi.python.org/pypi/groundwork
   :height: 20px

**Full documentation at https://groundwork.readthedocs.io**

.. image:: https://raw.githubusercontent.com/useblocks/groundwork/master/docs/_static/gw_slogan_white.png


groundwork
----------

groundwork is a Python based microframework for highly reusable applications and their components.

Its functionality is based on exchangeable, documented and tested plugins and patterns.

It is designed to support any kind of Python application: command line scripts, desktop programs or web applications.

groundwork enables applications to activate and deactivate plugins during runtime and to control dynamic plugin
behaviors like plugin status, used signals, registered commands and much more.

The functionality of plugins can easily be extended by using inheritable patterns.
Thus, groundwork supports developers with time-saving solutions for:

    * Command line interfaces
    * Loose inter-plugin communication via signals and receivers
    * Shared objects to provide and request content to and from other plugins
    * Static and dynamic documents for an overall documentation

Examples
~~~~~~~~

Initial app
```````````

The following code defines a plugin with command line support and creates a groundwork application which activates
the plugin::

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
        my_app = App(plugins=[MyPlugin])        # Creates app and registers MyPlugin
        my_app.plugins.activate(["My Plugin"])  # Initialise and activates 'My Plugin'
        my_app.commands.start_cli()             # Starts the command line interface

The following commands can be used on a command line now::

    python my_app.py hello      # Prints 'Hello world'
    python my_app.py            # Prints a list of available commands
    python my_app.yp hello -h   # Prints syntax help for the hello command 


Weather Web App
```````````````
The following image shows the architecture of an imaginary weather service for the web. A detailed description can be
found on `groundwork's architecture page <http://groundwork.readthedocs.io/en/latest/architecture.html>`_.

.. image:: docs/_static/groundwork_architecture.png




