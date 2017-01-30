import os
from groundwork.patterns import GwRecipesPattern


class RecipePlugin(GwRecipesPattern):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super(RecipePlugin, self).__init__(*args, **kwargs)

    def activate(self):
        self.recipes.register("test_recipe",
                              os.path.join(os.path.dirname(__file__), "../recipes/gw_test_app"),
                              "test recipe")

    def deactivate(self):
        pass
