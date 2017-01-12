"""
Groundwork recipe pattern.

Provides function to register, get and build recipes.

Recipes are used create directories and files based on a given template and some user input.
It is mostly used to speed up the set up of new python packages, groundwork applications or projects.

Based on cookiecutter: https://github.com/audreyr/cookiecutter/
"""
import os
import logging
from cookiecutter.main import cookiecutter

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
    """
    Cares about the recipe management on plugin level.
    Allows to register, get and build recipes in the context of the current plugin.

    :param plugin: plugin, which shall be used as contxt.
    """
    def __init__(self, plugin):
        self._plugin = plugin
        self.__app = plugin.app
        self.__log = plugin.log

        # Let's register a receiver, which cares about the deactivation process of recipes for this plugin.
        # We do it after the original plugin deactivation, so we can be sure that the registered function is the last
        # one which cares about recipes for this plugin.
        self._plugin.signals.connect(receiver="%s_recipes_deactivation" % self._plugin.name,
                                     signal="plugin_deactivate_post",
                                     function=self.__deactivate_recipes,
                                     description="Deactivate recipes for %s" % self._plugin.name,
                                     sender=self._plugin)
        self.__log.debug("Plugin recipes initialised")

    def __deactivate_recipes(self, plugin, *args, **kwargs):
        """
        Deactivates/unregisters all recipes of the current plugin, if this plugin gets deactivated.
        """
        recipes = self.get()
        for recipe in recipes.keys():
            self.unregister(recipe)

    def register(self, name, path, description, final_words=None):
        """
        Registers a new recipe in the context of the current plugin.

        :param name: Name of the recipe
        :param path: Absolute path of the recipe folder
        :param description: A meaningful description of the recipe
        :param final_words: A string, which gets printed after the recipe was build.
        """
        return self.__app.recipes.register(name, path, self._plugin, description, final_words)

    def unregister(self, recipe):
        """
        Unregister a recipe of the current plugin.

        :param recipe: Name of the recipe.
        """
        return self.__app.recipes.unregister(recipe)

    def get(self, name=None):
        """
        Gets a list of all recipes, which are registered by the current plugin.
        If a name is provided, only the requested recipe is returned or None.

        :param: name: Name of the recipe
        """
        return self.__app.recipes.get(name, self._plugin)

    def build(self, recipe):
        """
        Builds a recipe

        :param recipe: Name of the recipe to build.
        """
        return self.__app.recipes.build(recipe, self._plugin)


class RecipesListApplication:
    """
    Cares about the recipe management on application level.
    Allows to register, get and build recipes.

    :param app: groundwork application instance
    """
    def __init__(self, app):
        self.__app = app
        self.recipes = {}
        self.__log = logging.getLogger(__name__)
        self.__log.info("Application recipes initialised")

    def register(self, name, path, plugin, description=None, final_words=None):
        """
        Registers a new recipe.
        """
        if name in self.recipes.keys():
            raise RecipeExistsException("Recipe %s was already registered by %s" %
                                        (name, self.recipes["name"].plugin.name))

        self.recipes[name] = Recipe(name, path, plugin, description, final_words)
        self.__log.debug("Recipe %s registered by %s" % (name, plugin.name))
        return self.recipes[name]

    def unregister(self, recipe):
        """
        Unregisters an existing recipe, so that this recipe is no longer available.

        This function is mainly used during plugin deactivation.

        :param recipe: Name of the recipe
        """
        if recipe not in self.recipes.keys():
            self.__log.warning("Can not unregister recipe %s" % recipe)
        else:
            del (self.recipes[recipe])
            self.__log.debug("Recipe %s got unregistered" % recipe)

    def get(self, recipe=None, plugin=None):
        """
        Get one or more recipes.

        :param recipe: Name of the recipe
        :type recipe: str
        :param plugin: Plugin object, under which the recipe was registered
        :type plugin: GwBasePattern
        """
        if plugin is not None:
            if recipe is None:
                recipes_list = {}
                for key in self.recipes.keys():
                    if self.recipes[key].plugin == plugin:
                        recipes_list[key] = self.recipes[key]
                return recipes_list
            else:
                if recipe in self.recipes.keys():
                    if self.recipes[recipe].plugin == plugin:
                        return self.recipes[recipe]
                    else:
                        return None
                else:
                    return None
        else:
            if recipe is None:
                return self.recipes
            else:
                if recipe in self.recipes.keys():
                    return self.recipes[recipe]
                else:
                    return None

    def build(self, recipe, plugin=None):
        """
        Execute a recipe and creates new folder and files.

        :param recipe: Name of the recipe
        :param plugin: Name of the plugin, to which the recipe must belong.
        """
        if recipe not in self.recipes.keys():
            raise RecipeMissingException("Recipe %s unknown." % recipe)

        recipe_obj = self.recipes[recipe]

        if plugin is not None:
            if recipe_obj.plugin != plugin:
                raise RecipeWrongPluginException("The requested recipe does not belong to the given plugin. Use"
                                                 "the app object, to retrieve the requested recipe: "
                                                 "my_app.recipes.get(%s)" % recipe)

        recipe_obj.build()


class Recipe:
    """
    A recipe is an existing folder, which will be handled by the underlying cookiecutter library as template folder.

    :param name: Name of the recipe
    :param path: Absolute path to the recipe folder
    :param plugin: Plugin which registers the recipe
    :param description: Meaningful description of the recipe
    :param final_words: String, which gets printed after a recipe was successfully build.
    """
    def __init__(self, name, path, plugin, description="", final_words=""):
        self.name = name
        if os.path.isabs(path):
            self.path = path
        else:
            raise FileNotFoundError("Path of recipe must be absolute. Got %s" % path)
        self.plugin = plugin
        self.description = description
        self.final_words = final_words

    def build(self, output_dir=None, **kwargs):
        """
        Buildes the recipe and creates needed folder and files.
        May ask the user for some parameter inputs.

        :param output_dir: Path, where the recipe shall be build. Default is the current working directory
        :return: location of the installed recipe
        """
        if output_dir is None:
            output_dir = os.getcwd()

        target = cookiecutter(self.path, output_dir=output_dir, **kwargs)

        if self.final_words is not None and len(self.final_words) > 0:
            print("")
            print(self.final_words)
        return target


class RecipeExistsException(BaseException):
    pass


class RecipeMissingException(BaseException):
    pass


class RecipeWrongPluginException(BaseException):
    pass
