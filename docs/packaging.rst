.. _packaging:

Packaging and Installation
==========================

The distribution of :ref:`plugins <plugins>`, :ref:`patterns <patterns>` and even :ref:`applications <application>`
can easily be done by using
solutions from `Python's packaging ecosystem <https://packaging.python.org/>`_.
For packaging the library `setuptools <https://setuptools.readthedocs.io/en/latest/>`_ is recommend.
For package installation, the wide known tool `pip <https://pip.pypa.io/en/stable/>`_ should be used.

Create a package
----------------

You can add as many plugins, patterns and even applications to a single python package as you like.

All you need is a file called **setup.py** in the root folder of your package. Example::

    from setuptools import setup, find_packages

    setup(
        name='my_package',
        version="0.1,
        url='http://my_package.readthedocs.org',
        license='MIT',
        author='me',
        author_email='me@me.com',
        description="My awesome package for doing hot stuff",
        long_description="A longer description of my awesome package",
        packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
        include_package_data=True,
        platforms='any',
        install_requires=["groundwork", "Another_Package"],
        entry_points={
            'console_scripts': ["my_app my_package.my_app:start_app"],
            'groundwork.plugin': [
                'my_plugin = my_package.my_plugin:MyPlugin',
                'my_plugin_2" = my_package.my_plugin_2:MyPlugin2']
        }
    )

For more details, take a look into the
`Developer's Guide of setuptools <https://setuptools.readthedocs.io/en/latest/setuptools.html#developer-s-guide>`_
or read one of the many tutorials about setup.py on the internet.

entry_points
~~~~~~~~~~~~

`Entry points <http://setuptools.readthedocs.io/en/latest/pkg_resources.html?highlight=entry_point#entry-points>`_ are
used to "advertise" Python objects for use by other distributions.

groundwork uses them to find plugins in installed packages, without the need to use some hard coded imports like
``from another_package import PluginX``.

Therefore groundwork knows all packaged plugins, which are available in system path of the currently used python
interpreter. These plugins can be used by activation, without any need to register or import them::

    from groundwork import App

    my_app = App()

    my_app.activate("GwPluginsInfo")
    # GwPluginsInfo is provided by an entry_point inside the groundwork package

.. note::
    During activation, the plugins are identified by their names. So the plugin name must be known, which is not
    necessarily the plugin class name.

The entry_point of a plugin must provide a class, which inherits directly or indirectly from
:class:`~groundwork.patterns.gw_base_pattern.GwBasePattern`::

    # setup.py from groundwork package

    from setuptools import setup, find_packages

    setup(
        name='groundwork',
        ...
        entry_points={
           'groundwork.plugin': [
                'gw_plugins_info = groundwork.plugins.gw_plugins_info:GwPluginsInfo',
            ]
        }
    )

Package structure
~~~~~~~~~~~~~~~~~

The following structure is recommended for packaging multiple plugins, patters and applications::

    my_package
    |
    |-- setup.py
    |
    |-- my_package
    |   |
    |   |-- applications
    |   |   |-- my_app
    |   |       |-- my_app.py
    |   |
    |   |-- patterns
    |   |   |-- my_pattern
    |   |       |-- my_pattern.py
    |   |
    |   |-- plugins
    |       |-- my_plugin
    |       |   |-- my_plugin.py
    |       |
    |       |-- my_plugin_2
    |           |-- my_plugin_2.py
    |
    |-- docs
    |   |-- index.rst
    |   |-- my_app.rst
    |   |-- my_pattern.rst
    |   |-- my_plugin.rst
    |   |-- my_plugin_2.rst
    |
    |-- tests
        |-- test_my_app.py
        |-- test_my_pattern.py
        |-- test_my_plugin.py
        |-- test_my_plugin_2.py




Install a package
-----------------

Local packages
~~~~~~~~~~~~~~
If you store your package locally and do not use `PyPI <https://pypi.python.org/pypi>`_ for distribution,
you need to use your **setup.py** file for all installation scenarios.

During development
^^^^^^^^^^^^^^^^^^
During development it is recommend to install a package in development mode on your current virtual environment::

    python setup.py develop

This lets you make changes on your code without the need to reinstall your package after each code change.
This must be done only, if you make some changes to the **setup.py** file.

Final installation
^^^^^^^^^^^^^^^^^^
To finally install your package inside the current used python environment, use **install**::

    python setup.py install

This will copy all files to your python environment and new changes on your plugin do not have any impact on the
installed package.

PyPi
~~~~
`PyPI <https://pypi.python.org/pypi>`_ can be used to share your package globally and allows users to use
`pip <https://pip.pypa.io/en/stable/>`_  for installation::

    pip install my_package

The usage of PyPi is already explained in some great tutorials. A short selection:

    * `Python Packaging: Publishing on PyPi <http://python-packaging.readthedocs.io/en/latest/minimal.html>`_
    * `Peter Downs: How to submit a package to PyPI <http://peterdowns.com/posts/first-time-with-pypi.html>`_




