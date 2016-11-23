Contribute
**********

Running tests
=============
Before tests can be executed, you have to install the test dependencies of groundwork::

    pip install -r test-requirements.txt

Then to run groundwork's own tests, open a command line interface, change to groundwork/tests and run::

    py.test --flake8


pytest and Flake8
-----------------
groundwork is using `pytest <http://docs.pytest.org/en/latest/>`_ for its tests.

For these tests, the following plugins are recommended:

 * `pytest-flake8 <https://pypi.python.org/pypi/flake8/1.6.1>`_
 * `pytest-sugar <https://pypi.python.org/pypi/pytest-sugar>`_


pytest and exception chains
---------------------------

pytest seems to show the traceback of last raised exception only.
In some cases this is not really helpful, as the location of last raised exception may not be place, where you need
to fix something.

E.g. if a plugin raises an exception during plugin activation, the pluginmanager will catch this and raises
it's own exception. pytest will only guide you to the pluginmanager, but not to the plugin activation routine itself.

groundwork raises exceptions always with the "from e" statement (e.g. raise Exception("Ohh no") from e).
A normal python traceback would show this exception chain. pytest unluckily does not, if it is not configured to do so.

To activate the default python traceback, start pytest with the following parameter::

    py.test --tb=native



Deviations from common standards
--------------------------------

Maximum line length
^^^^^^^^^^^^^^^^^^^
The code of groundwork is written with a maximum line length of 120 characters per line.
This value is also used for flake8 configuration in the file *setup.cfg*.


Documentation
=============
groundwork is using sphinx for documentation building.

To build the documentation you need to have all documentation requirements installed::

    pip install -r doc-requirements.txt

Then just run the following inside groundwork/docs to get a html documentation::

    make html

groundwork sphinx theme
-----------------------

groundwork has its own theme for sphinx html documentations. It's free and was created to give
groundwork related packages a common look.

Code and some instructions can be found inside the `github project of gw-sphinx-themes <https://github
.com/useblocks/gw-sphinx-themes>`_.





