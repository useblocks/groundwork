groundwork
----------

groundwork is a python based microframework for highly reusable applications and their components.

It’s functionality is based on exchangeable, documented and tested plugins and patterns.

It is designed to support any kind of application: command line scripts, desktop programs or web applications.

groundwork enables applications to activate and deactivate plugins during runtime and to control dynamic plugin
behaviors like plugin status, used signals, registered commands and much more.

The functionality of plugins can be easily extended by the usage of inheritable patterns.
Based on this, groundwork supports developers with time-saving solutions for:

    * Command line interfaces
    * Loose inter-plugin communication via signals and receivers
    * Shared objects to provide and request content to and from other plugins
    * Static and dynamic documents for an overall documentation

Example
~~~~~~~
The following code defines a plugin with command line support and creates a groundwork application, which activates
this plugin::

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

On a command line the following commands can be used now::

    python my_app.py hello      # Prints 'Hello world'
    python my_app.py            # Prints a list of available commands
    python my_app.yp hello -h   # Prints some help text for the command hello
