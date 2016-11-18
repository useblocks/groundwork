.. _cookiecutter: https://cookiecutter.readthedocs.io/en/latest/

.. _Jinja: http://jinja.pocoo.org/

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

    groundwork recipes are based on `cookiecutter`_ and supports every
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
Own recipes must be registered by a plugin, which needs to give the following data during registration:
 * name of the recipe
 * absolute path of the recipe directory
 * description of the recipe
 * final words, which will be printed after an recipe was executed (optional)

See the following code from the RecipeBuilder plugin to get an example::

 class GwRecipesBuilder(GwCommandsPattern, GwRecipesPattern):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def activate(self):
        ...
        self.recipes.register("gw_package",
                              os.path.abspath(os.path.join(os.path.dirname(__file__), "../recipes/gw_package")),
                              description="Groundwork basic package. Includes places for "
                                          "apps, plugins, patterns and recipes.",
                              final_words="Recipe Installation is done.\n\n"
                                          "For installation run: 'python setup.py develop' \n"
                                          "For documentation run: 'make html' inside doc folder "
                                          "(after installation!)\n\n"
                                          "For more information, please take a look into the README file "
                                          "to know how to go on.\n"
                                          "For help visit: https://groundwork.readthedocs.io\n\n"
                                          "Have fun with your groundwork package.")

Structure
~~~~~~~~~
A recipe must follow the rules of `cookiecutter`_. Therefore it needs to have the following structure::

    /
    |-- cookiecutter.json
    |
    |-- {{ cookiecutter.project_name}}
    |   |
    |   |-- other directories/files, which will be copied.
    |
    |-- other direcotries/files, which will NOT be copied


.. note::

    It is important to have a **cookiecutter.json** file, as well as a single root-directory, which name is surrounded by
    **{{ }}**.

cookiecutter.json
~~~~~~~~~~~~~~~~~
The **cookiecutter.json** file is used as configuration file and must hold a json string, which defines all needed
parameters for the recipe setup.

All these parameters can be used and access in directory / file names as well as in file content.

Structure
`````````
The following example for a **cookiecutter.json** file comes from the RecipeBuilder plugin::

 {
  "full_name": "My Name",
  "github_user" : "{{cookiecutter.full_name.lower().replace(' ', '_') }}",
  "email": "{{cookiecutter.github_user}}@provider.com",
  "project_name": "My Package",
  "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '_') }}",
  "github_project_name": "{{cookiecutter.project_slug}}",
  "project_app": "{{cookiecutter.project_slug}}_app",
  "project_plugin": "{{cookiecutter.project_slug}}_plugin",
  "project_short_description": "Package for hosting groundwork apps and plugins like {{cookiecutter.project_app}} or {{cookiecutter.project_plugin}}.",
  "test_folder": "tests",
  "test_prefix": "test_",
  "version": "0.1.0",
  "license": ["MIT license", "BSD license", "ISC license", "Apache Software License 2.0", "GNU General Public License v3", "Not open source"]
 }

Usage
`````
The parameters from the configuration files are all accessible by using **{{cookiecutter.PARAMETER}}**, wherever you
want to use this value:

 * Directory names
 * File names
 * File content
 * cookiecutter.json

.. note::
 As the parameters are also accessible in the **cookiecutter.json** file, you are free to manipulate an input and use
 it as default value for the next parameter. For instance: The project name can be used as python package name,
 by removing all whitespaces and make it lowercase. Example: "project_package":
 {{ cookiecutter.project_name.lower().replace(' ', '_')
 }}".

Using Jinja
~~~~~~~~~~~
`Jinja`_ statements can be used to manipulate/modify inputs or make decisions out of them.
For instance: Based on the chosen license, the content of a file called *LICENSE* could be changed by::

    {% if cookiecutter.license == MIT %}
    Using MTI license

    {% else if cookiecutter.license == BSD %}
    Using BSD license

    {% else %}
    Using a private license

    {% endif %}


