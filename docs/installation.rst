Installation
============

.. TODO 17-10-mh This has changed

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

A virtual environment allows you to install and test python packages without any affect on a system-wide installation.

If not done yet, use pip to install **virtualenv**::

   sudo pip install virtualenv

Create a virtual environment in your preferred folder with::

    virtualenv venv     # venv will be the name of the folder. You may change it.

To activate it, run::

    . venv/bin/activate

Or on windows::

    venv\scripts\activate

After that your virtual environment is installed and activated.
Now you can install groundwork::

    pip install groundwork

