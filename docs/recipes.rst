Recipes
=======

Recipes are used to generate directories and files based on given user input.

They are most used to speed up the set up of

 * New Python packages
 * New groundwork projects
 * New groundwork applications, plugins or patterns.
 * New own projects

Besides folder structures and needed files, they can also be used to provide project/company specific values for
some preconfiguration. These values may be:

 * Contact details of project leader or IT administrators.
 * Common links to general documentation like IT security rules or project handbook.
 * Source and integrations of corporate designs like css files or office templates.
 * Company wide used libraries and their ready-to-use integration
 * Configurations for external IT services, like continuous integration systems and bug trackers.
 * Whatever is needed...

Recipes makes it possible to start relevant coding in less than 30 seconds after a new project was set up. Without
missing any rules, designs, integrations, checks or whatever is required for the current project.

.. note::

    groundwork recipes are based on `cookiecutter <https://cookiecutter.readthedocs.io/en/latest/>`_ and supports every
    function of it. To get a deep understandig of what is possible with groundwork recipes, you should take a look
    into `cookiecutter's documentation <https://cookiecutter.readthedocs.io/en/latest/>`_ as well.

Workflow
--------

So, what happens if a recipe gets executed? Here is the workflow:

 1. Run `groundwork recipe_build gw_package`.
    **gw_package** is provided by groundwork, but can be replaced by any other recipe.
 2. The user gets asked on command line interface for some variable inputs.
 3. The recipe gets executed and uses the user's input to create folders and files with input related names.
 4. In most cases the input is also used to become part of some files. For instance a README file may contain the
    author's name after generation.

List available recipes
----------------------

groundwork knows all available recipes of a groundwork application. And if this app has loaded the `Gw Recipe
Builder` plugin, it provides the command `recipe_list` to get a list of all registered recipes.

The groundwork application itself already has some usable recipes. Just execute the following to get a complete list::

 groundwork recipe_list

recipe gw_package
~~~~~~~~~~~~~~~~~
At least you can see a recipe called **gw_package**. This recipe creates a ready-to-use, groundwork based Python
package. Including an example groundwork application and plugin, configured
`sphinx project <http://www.sphinx-doc.org/en/stable/>`_ for documentation,
configured test cases with `pytest <http://doc.pytest.org/en/latest/>`_
and a test environment based on `tox <https://tox.readthedocs.io/en/latest/>`_,
`travis <https://travis-ci.org/>`_ support, ...

Building/Execute a recipe
-------------------------

To build/execute a recipe simply open a command line interface and move to the directory, where the initial recipe
folder shall be created. Then execute::

 groundwork recipe_build RECIPE_NAME

 # For instance
 groundwork recipe_build gw_package

Based on the recipe, you may get asked some questions, which mostly affects the naming of files and directories.

After the last question is answered, groundwork executes the recipe and everything gets created. After this there
should be a new folder inside your current working directory.

Creating own recipes
--------------------



Registration
~~~~~~~~~~~~

Structure
~~~~~~~~~

cookiecutter.json
~~~~~~~~~~~~~~~~~


Using Jinja
~~~~~~~~~~~

