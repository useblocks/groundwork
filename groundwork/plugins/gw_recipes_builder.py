# -*- coding: utf-8 -*-
import os
from click import Argument

from groundwork.patterns import GwCommandsPattern, GwRecipesPattern


class GwRecipesBuilder(GwCommandsPattern, GwRecipesPattern):
    """
    Provides commands for listing and building recipes via command line interface.

    Provided commands:

     * recipe_list
     * recipe_build

    Provides also the recipe **gw_package**, which can be used to setup a groundwork related python package.
    Content of the package:

     * setup.py: Preconfigured and ready to use.
     * groundwork package structure: Directories for applications, patterns, plugins and recipes.
     * Simple, runnable example of a groundwork application and plugins.
     * usable test, supported by py.test and tox.
     * expandable documentation, supported by sphinx and the groundwork sphinx template.
     * .gitignore


    This code is hardly based on Cookiecutter's main.py file:
    https://github.com/audreyr/cookiecutter/blob/master/cookiecutter/main.py
    """
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", self.__class__.__name__)
        super(GwRecipesBuilder, self).__init__(*args, **kwargs)

    def activate(self):
        self.commands.register("recipe_list", "Lists all recipes", self._recipe_list)
        self.commands.register("recipe_build", "Builds a given recipe", self._recipe_build,
                               params=[Argument(("recipe",), required=True)])

        self.recipes.register("gw_package",
                              os.path.abspath(os.path.join(os.path.dirname(__file__), "../recipes/gw_package")),
                              description="Groundwork basic package. Includes places for "
                                          "apps, plugins, patterns and recipes.",
                              final_words="Recipe Installation is done.\n\n"
                                          "During development use buildout:\n"
                                          "Run: python bootstrap.py\n"
                                          "Then: bin/buildout\n"
                                          "Start the app: bin/app\n\n"
                                          "For installation run: 'python setup.py install' \n"
                                          "For documentation run: 'make html' inside doc folder "
                                          "(after installation!)\n\n"
                                          "For more information, please take a look into the README file "
                                          "to know how to go on.\n"
                                          "For help visit: https://groundwork.readthedocs.io\n\n"
                                          "Have fun with your groundwork package.")

    def deactivate(self):
        pass

    def _recipe_list(self):
        print("Recipes:")
        for key, recipe in self.app.recipes.get().items():
            print("  %s by plugin '%s' - %s" % (recipe.name, recipe.plugin.name, recipe.description))

    def _recipe_build(self, recipe):
        recipe_obj = self.app.recipes.get(recipe)
        if recipe_obj is None:
            print("Recipe %s not found." % recipe)
        else:
            recipe_obj.build(no_input=False, extra_context=None)
