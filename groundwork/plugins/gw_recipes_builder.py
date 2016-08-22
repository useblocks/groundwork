# -*- coding: utf-8 -*-

"""
groundwork recipe manager
-------------------------
Main entry point for the `groundwork recipe` command.

This code is hardly based on Cookiecutter's main.py file:
https://github.com/audreyr/cookiecutter/blob/master/cookiecutter/main.py
"""
from click import Argument

from groundwork.patterns import GwDocumentsPattern, GwCommandsPattern, GwRecipesPattern


class GwRecipesBuilder(GwCommandsPattern, GwRecipesPattern):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def activate(self):
        self.commands.register("recipe_list", "Lists all recipes", self._recipe_list)
        self.commands.register("recipe_build", "Builds a given recipe", self._recipe_build,
                               params=Argument(("recipe",), required=True))

        self.recipes.register("MyRecipe", "somewhere", description="Test recipes")

    def _recipe_list(self):
        print("Recipes:")
        for key, recipe in self.app.recipes.get().items():
            print("  %s by plugin '%s' - %s" % (recipe.name, recipe.plugin.name, recipe.description))

    def _recipe_build(self, recipe):
        try:
            recipe_obj = self.app.recipes.get(recipe)
            recipe_obj.build()
        except Exception as e:
            print("Error during recipe build. Error: %s" % e)




