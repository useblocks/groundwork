Installation
============

.. warning::

    | groundwork does currently support Python3.4 or higher only.
    | Python2.x is not supported!

System-wide installation
------------------------
You can use pip to install groundwork in your local python environment::

    sudo pip install groundwork

On windows system **sudo** is not needed.

Virtual environment
-------------------

If not done yet, use pip to install **virtualenv**::

   sudo pip install virtualenv

The create a virtual environment in your preferred folder with::

    virtualenv venv

To activate it, run::

    . venv/bin/activate

Or on windows::

    venv\scripts\activate

After that your virtual environment is installed and activated.
Now you can install groundwork::

    pip install groundwork
