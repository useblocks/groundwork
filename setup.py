"""
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
"""
import re
from setuptools import setup, find_packages

version = "0.1.1a3"

setup(
    name='groundwork',
    version=version,
    url='http://groundwork.readthedocs.org',
    license='MIT',
    author='team useblocks',
    author_email='info@useblocks.com',
    description="A plugin-based microframework for highly reusable applications and their components",
    long_description=__doc__,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    platforms='any',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-flake8'],
    install_requires=["click", "blinker"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'console_scripts': ["groundwork = groundwork.applications.gw_base_app:start_app"],
        'groundwork.plugin': [
            'gw_plugin_info = groundwork.plugins.gw_plugin_info:GwPluginInfo',
            'gw_signal_info = groundwork.plugins.gw_signal_info:GwSignalInfo',
            'gw_command_info = groundwork.plugins.gw_commands_info:GwCommandsInfo'
        ]
    }
)
