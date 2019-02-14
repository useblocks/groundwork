"""
groundwork
----------

groundwork is a Python based microframework for highly reusable applications and their components.

Its functionality is based on exchangeable, documented and tested plugins and patterns.

It is designed to support any kind of Python application: command line scripts, desktop programs or web applications.

groundwork enables applications to activate and deactivate plugins during runtime and to control dynamic plugin
behaviors like plugin status, used signals, registered commands and much more.

The functionality of plugins can easily be extended by the usage of inheritable patterns.
Thus, groundwork supports developers with time-saving solutions for:

    * Command line interfaces
    * Loose inter-plugin communication via signals and receivers
    * Shared objects to provide and request content to and from other plugins
    * Static and dynamic documents for an overall documentation

Example
~~~~~~~
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

"""
from setuptools import setup, find_packages
import re
import ast

_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('groundwork/version.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

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
    # package_data={'': ['*.conf'], 'groundwork/recipes': ['*']},
    package_data={'': ['*.conf'], 'groundwork/recipes': ['*']},
    platforms='any',
    setup_requires=[],
    tests_require=['pytest', 'pytest-flake8'],
    # TODO 17-10-11-mh Future is missing here
    install_requires=["pathlib", "click", "blinker", "jinja2", "cookiecutter", "docutils"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': ["groundwork = groundwork.applications.gw_base_app:start_app"],
        'groundwork.plugin': [
            'gw_plugins_info = groundwork.plugins.gw_plugins_info:GwPluginsInfo',
            'gw_signals_info = groundwork.plugins.gw_signals_info:GwSignalsInfo',
            'gw_commands_info = groundwork.plugins.gw_commands_info:GwCommandsInfo',
            'gw_documents_info = groundwork.plugins.gw_documents_info:GwDocumentsInfo',
            'gw_recipes_builder = groundwork.plugins.gw_recipes_builder:GwRecipesBuilder',
        ]
    }
)
