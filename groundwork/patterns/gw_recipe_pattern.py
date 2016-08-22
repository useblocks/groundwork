"""
Groundwork recipe pattern.

Based on cookiecutter: https://github.com/audreyr/cookiecutter/
"""

import logging
from groundwork.patterns.gw_base_pattern import GwBasePattern


class GwRecipesPattern(GwBasePattern):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not hasattr(self.app, "recipes"):
            self.app.recipes = RecipesListApplication(self.app)

        #: Stores an instance of :class:`~groundwork.patterns.gw_recipes_pattern.RecipesListPlugin`
        self.recipes = RecipesListPlugin(self)

    # register new recipe (aka template)
    # get recipes


class RecipesListPlugin:
    pass


class RecipesListApplication:
    pass


class Recipe:
    """
    :param name: Name of the recipe
    :param location: Absolute path to the recipe folder
    :param plugin: Plugin which registers the recipe
    :param description: Meaningful description of the recipe
    """
    def __init__(self, name, location, plugin, description=""):
        self.name = name
        self.location = location
        self.plugin = plugin
        self.description = description
