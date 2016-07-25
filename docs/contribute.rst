Contribute
**********

Running tests
=============

To run groundwork's own tests, open a command line interface, change to groundwork/tests and run::

    py.test --flake8


pytest and Flake8
-----------------
groundwork is using `pytest <http://docs.pytest.org/en/latest/>`_ for its tests.

For these tests, the following plugins are recommended:

 * `pytest-flake8 <https://pypi.python.org/pypi/flake8/1.6.1>`_
 * `pytest-sugar <https://pypi.python.org/pypi/pytest-sugar>`_

Deviations from common standards
--------------------------------

Maximum line length
^^^^^^^^^^^^^^^^^^^
The code of groundwork is written with a maximum line length of 120 characters per line.
This value is also used for flake8 configuration in the file *setup.cfg*.


Documentation
=============

groundwork is using sphinx for documentation building.

Just run the following inside groundwork/docs to get a html documentation::

    make html

groundwork sphinx theme
-----------------------

groundwork has its own theme for sphinx html documentations. It's free and was created to give
groundwork related packages a common look.

Code and some instructions can be found inside the `github project of gw-sphinx-themes <https://github
.com/useblocks/gw-sphinx-themes>`_.





