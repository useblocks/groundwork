# -*- coding: utf-8 -*-

"""
groundwork recipe manager
-------------------------
Main entry point for the `groundwork recipe` command.

This code is hardly based on Cookiecutter's main.py file:
https://github.com/audreyr/cookiecutter/blob/master/cookiecutter/main.py
"""
import os
from click import Argument

from groundwork.patterns import GwCommandsPattern, GwRecipesPattern


class GwRecipesBuilder(GwCommandsPattern, GwRecipesPattern):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def activate(self):
        self.commands.register("recipe_list", "Lists all recipes", self._recipe_list)
        self.commands.register("recipe_build", "Builds a given recipe", self._recipe_build,
                               params=[Argument(("recipe",), required=True)])

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

    def _recipe_list(self):
        print("Recipes:")
        for key, recipe in self.app.recipes.get().items():
            print("  %s by plugin '%s' - %s" % (recipe.name, recipe.plugin.name, recipe.description))

    def _recipe_build(self, recipe):
        recipe_obj = self.app.recipes.get(recipe)
        if recipe_obj is None:
            print("Recipe %s not found." % recipe)
        else:
            recipe_obj.build()
