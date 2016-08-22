"""
Groundwork recipe pattern.

Based on cookiecutter: https://github.com/audreyr/cookiecutter/
"""
import os
import logging

from cookiecutter.config import get_user_config, USER_CONFIG_PATH
from cookiecutter.generate import generate_context, generate_files
from cookiecutter.exceptions import InvalidModeException
from cookiecutter.prompt import prompt_for_config
from cookiecutter.replay import dump, load
from cookiecutter.repository import determine_repo_dir

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

    def __deactivate_documents(self, plugin, *args, **kwargs):
        recipes = self.get()
        for recipe in recipes.keys():
            self.unregister(recipe)

    def register(self, name, path, description):
        return self.__app.recipes.register(name, path, self._plugin, description)

    def unregister(self, recipe):
        return self.__app.recipes.unregister(recipe)

    def get(self, name=None):
        return self.__app.recipes.get(name, self._plugin)

    def __getattr__(self, item):
        """
        Catches unknown function/attribute calls and delegates them to RecipesListApplication
        """
        def method(*args, **kwargs):
            func = getattr(self.__app.recipes, item, None)
            if func is None:
                raise AttributeError("RecipesistApplication does not have an attribute called %s" % item)
            return func(*args, plugin=self._plugin, **kwargs)

        return method


class RecipesListApplication:
    def __init__(self, app):
        self.__app = app
        self.recipes = {}
        self.__log = logging.getLogger(__name__)
        self.__log.info("Application recipes initialised")

    def register(self, name, path, plugin, description=None):
        """
        Registers a new recipe.
        """
        if name in self.recipes.keys():
            raise RecipeExistsException("Recipe %s was already registered by %s" %
                                        (name, self.recipes["name"].plugin.name))

        self.recipes[name] = Recipe(name, path, plugin, description)
        self.__log.debug("Recipe %s registered by %s" % (name, plugin.name))
        return self.recipes[name]

    def unregister(self, recipe):
        """
        Unregisters an existing recipe, so that this recipe is no longer available.

        This function is mainly used during plugin deactivation.

        :param recipe: Name of the recipe
        """
        if recipe not in self.recipes.keys():
            self.log.warning("Can not unregister recipe %s" % recipe)
        else:
            del (self.recipes[recipe])
            self.__log.debug("Recipe %s got unregistered" % recipe)

    def get(self, recipe=None, plugin=None):
        """
        Get one or more recipes.

        :param recipe: Name of the recipe
        :type recipe: str
        :param plugin: Plugin object, under which the recipe where registered
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

    def create(self, recipe):
        """
        Execute a recipe and creates new folder and files.

        :param recipe: Name of the recipe
        """
        if recipe not in self.recipes.keys():
            raise RecipeMissingException("Recipe %s unknown." % recipe)

        recipe_obj = self.recipes[recipe]
        recipe_obj.create()


class Recipe:
    """
    A recipe is an existing folder, which will be handled by the underlying cookiecutter library as template folder.

    :param name: Name of the recipe
    :param location: Absolute path to the recipe folder
    :param plugin: Plugin which registers the recipe
    :param description: Meaningful description of the recipe
    """
    def __init__(self, name, path, plugin, description="", config_file="recipe.json"):
        self.name = name
        self.path = path
        self.plugin = plugin
        self.description = description
        self.config_file = config_file

    def create(self, checkout=None, no_input=False, extra_context=None,
               replay=False, overwrite_if_exists=False, output_dir='.',
               config_file=USER_CONFIG_PATH):
        """
        Creates/Builds/Cakes/Backs this recipe.
        This normally will create new folder and files

        API equivalent to using Cookiecutter at the command line.
        :param overwrite_if_exists:
        :param replay:
        :param checkout: The branch, tag or commit ID to checkout after clone.
        :param no_input: Prompt the user at command line for manual configuration?
        :param extra_context: A dictionary of context that overrides default
            and user configuration.
        :param: overwrite_if_exists: Overwrite the contents of output directory
            if it exists
        :param output_dir: Where to output the generated project dir into.
        :param config_file: User configuration file path.
        """

        # Lets use as much original code from cookiecutter as possible
        # Therefore we use its variable names and map our internal names to it
        template = self.path
        template_name = self.name
        # template_name = os.path.basename(os.path.abspath(template))

        if replay and ((no_input is not False) or (extra_context is not None)):
            err_msg = "You can not use both replay and no_input or extra_context at the same time."
            raise InvalidModeException(err_msg)

        # Get user config from ~/.cookiecutterrc or equivalent
        # If no config file, sensible defaults from config.DEFAULT_CONFIG are used
        config_dict = get_user_config(config_file=config_file)

        repo_dir = determine_repo_dir(
            template=template,
            abbreviations=config_dict['abbreviations'],
            clone_to_dir=config_dict['cookiecutters_dir'],
            checkout=checkout,
            no_input=no_input,
        )

        if replay:
            context = load(config_dict['replay_dir'], template_name)
        else:

            # Normally cookiecutter wants a cookcutter.json file.
            # We changed this to use a dynamic value instead
            context_file = os.path.join(repo_dir, self.config_file)
            logging.debug('context_file is {0}'.format(context_file))

            context = generate_context(
                context_file=context_file,
                default_context=config_dict['default_context'],
                extra_context=extra_context,
            )

            # prompt the user to manually configure at the command line.
            # except when 'no-input' flag is set
            context['cookiecutter'] = prompt_for_config(context, no_input)

            dump(config_dict['replay_dir'], template_name, context)

        # Create project from local context and project template.
        return generate_files(
            repo_dir=repo_dir,
            context=context,
            overwrite_if_exists=overwrite_if_exists,
            output_dir=output_dir
        )


class RecipeExistsException(BaseException):
    pass


class RecipeMissingException(BaseException):
    pass
