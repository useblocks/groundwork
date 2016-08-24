"""
Groundwork recipe pattern.

Based on cookiecutter: https://github.com/audreyr/cookiecutter/
"""
import os
import logging

# The following imports are needed by our cookiecutter changes to support recipe.json instead of cookiecutter.json
# That's to much and is not really maintainable.
# We should try to update cookiecutter to allow custom config_file names and context keys
# (They should not hardcode "cookiecutter" or "cookiecutter.json everywhere)
from cookiecutter.config import get_user_config, USER_CONFIG_PATH
from cookiecutter.generate import _run_hook_from_repo_dir
from cookiecutter.generate import *
from cookiecutter.exceptions import InvalidModeException, UndefinedVariableInTemplate
from cookiecutter.prompt import render_variable,prompt_choice_for_config, read_user_variable
from cookiecutter.replay import dump, load, get_file_name
from cookiecutter.exceptions import RepositoryNotFound
from cookiecutter.vcs import clone
from cookiecutter.environment import StrictEnvironment
from cookiecutter.utils import make_sure_path_exists
import re
from future.utils import iteritems
from jinja2.exceptions import UndefinedError
import json
from past.builtins import basestring

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
        recipe_obj.build()


class Recipe:
    """
    A recipe is an existing folder, which will be handled by the underlying cookiecutter library as template folder.

    :param name: Name of the recipe
    :param path: Absolute path to the recipe folder
    :param plugin: Plugin which registers the recipe
    :param description: Meaningful description of the recipe
    :param config_json: Name if the cookiecutter template configuration file (default: recipe.json)
    """
    def __init__(self, name, path, plugin, description="", config_json="recipe.json"):
        self.name = name
        if os.path.isabs(path):
            self.path = path
        else:
            raise FileNotFoundError("Path of recipe must be absolute. Got %s" % path)
        self.plugin = plugin
        self.description = description
        self.config_json = config_json

    def build(self, output_dir=os.getcwd()):
        return self.cookiecutter_build(config_json="recipe.json", output_dir=output_dir)

    # the original cookiecutter cookiecutter() command from main.py. Added only param config_json.
    def cookiecutter_build(self, checkout=None, no_input=False, extra_context=None,
              replay=False, overwrite_if_exists=False, output_dir='.',
              config_file=USER_CONFIG_PATH, config_json='cookiecutter.json'):
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
        :param config_json: Name of the repository configuration file. Default: cookiecutter.json
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
            config_json=config_json
        )

        if replay:
            context = load(config_dict['replay_dir'], template_name)
        else:
            # Normally cookiecutter wants a cookiecutter.json file.
            # We changed this to use a dynamic value instead
            context_file = os.path.join(repo_dir, self.config_json)
            logging.debug('context_file is {0}'.format(context_file))

            context = generate_context(
                context_file=context_file,
                default_context=config_dict['default_context'],
                extra_context=extra_context,
            )
            # We need to recalculate our context_key, as cookiecutter normally uses "cookeicutter",
            # but in generate_context() the key gets calculated based on the config_filename
            context_key = self.config_json.split('.')[0]

            # prompt the user to manually configure at the command line.
            # except when 'no-input' flag is set
            context[context_key] = prompt_for_config(context, no_input, config_key=context_key)

            dump(config_dict['replay_dir'], template_name, context, context_key)

        # Create project from local context and project template.
        return generate_files(
            repo_dir=repo_dir,
            context=context,
            overwrite_if_exists=overwrite_if_exists,
            output_dir=output_dir,
            context_key=context_key
        )


class RecipeExistsException(BaseException):
    pass


class RecipeMissingException(BaseException):
    pass

#######################################################################################################
# The following code is taken from cookiecutter nightly build.
# The orignal code is taken from # cookiecutter/repository.py
#
# We need to make some change here, so that also other config files like recipe.json instead of
# cookiecutter.json are supported.
#######################################################################################################

REPO_REGEX = re.compile(r"""
(?x)
((((git|hg)\+)?(git|ssh|https?):(//)?)  # something like git:// ssh:// etc.
 |                                      # or
 (\w+@[\w\.]+)                          # something like user@...
)
""")


def is_repo_url(value):
    """Return True if value is a repository URL."""
    return bool(REPO_REGEX.match(value))


def expand_abbreviations(template, abbreviations):
    """
    Expand abbreviations in a template name.

    :param template: The project template name.
    :param abbreviations: Abbreviation definitions.
    """
    if template in abbreviations:
        return abbreviations[template]

    # Split on colon. If there is no colon, rest will be empty
    # and prefix will be the whole template
    prefix, sep, rest = template.partition(':')
    if prefix in abbreviations:
        return abbreviations[prefix].format(rest)

    return template


def repository_has_cookiecutter_json(repo_directory, config_json="cookiecutter.json"):
    """Determines if `repo_directory` contains a `cookiecutter.json` file.

    :param repo_directory: The candidate repository directory.
    :param config_json: File, which shall be used as template configuration file. (Default: cookiecutter.json)
    :return: True if the `repo_directory` is valid, else False.
    """
    repo_directory_exists = os.path.isdir(repo_directory)

    repo_config_exists = os.path.isfile(
        os.path.join(repo_directory, config_json)
        # was: os.path.join(repo_directory, 'cookiecutter.json')
    )
    return repo_directory_exists and repo_config_exists


def determine_repo_dir(template, abbreviations, clone_to_dir, checkout,
                       no_input, config_json="cookiecutter.json"):
    """
    Locate the repository directory from a template reference.

    Applies repository abbreviations to the template reference.
    If the template refers to a repository URL, clone it.
    If the template is a path to a local repository, use it.

    :param template: A directory containing a project template directory,
        or a URL to a git repository.
    :param abbreviations: A dictionary of repository abbreviation
        definitions.
    :param clone_to_dir: The directory to clone the repository into.
    :param checkout: The branch, tag or commit ID to checkout after clone.
    :param no_input: Prompt the user at command line for manual configuration?
    :param config_json: File, which shall be used as template configuration file. (Default: cookiecutter.json)
    :return: The cookiecutter template directory
    :raises: `RepositoryNotFound` if a repository directory could not be found.
    """
    template = expand_abbreviations(template, abbreviations)

    if is_repo_url(template):
        repo_dir = clone(
            repo_url=template,
            checkout=checkout,
            clone_to_dir=clone_to_dir,
            no_input=no_input,
        )
    else:
        # If it's a local repo, no need to clone or copy to your
        # cookiecutters_dir
        repo_dir = template

    if repository_has_cookiecutter_json(repo_dir, config_json):
        return repo_dir

    raise RepositoryNotFound(
        'The repository {} could not be located or does not contain '
        'a "cookiecutter.json" file.'.format(repo_dir)
    )


# cookiecutter source: prompt.py
def prompt_for_config(context, no_input=False, config_key=u"cookiecutter"):
    """
    Prompts the user to enter new config, using context as a source for the
    field names and sample values.

    :param no_input: Prompt the user at command line for manual configuration?
    """
    cookiecutter_dict = {}
    env = StrictEnvironment(context=context)

    for key, raw in iteritems(context[config_key]):
        if key.startswith(u'_'):
            cookiecutter_dict[key] = raw
            continue

        try:
            if isinstance(raw, list):
                # We are dealing with a choice variable
                val = prompt_choice_for_config(
                    cookiecutter_dict, env, key, raw, no_input
                )
            else:
                # We are dealing with a regular variable
                val = render_variable(env, raw, cookiecutter_dict)

                if not no_input:
                    val = read_user_variable(key, val)
        except UndefinedError as err:
            msg = "Unable to render variable '{}'".format(key)
            raise UndefinedVariableInTemplate(msg, err, context)

        cookiecutter_dict[key] = val
    return cookiecutter_dict


# cookiecutter source: replay.py
def dump(replay_dir, template_name, context, context_key):
    if not make_sure_path_exists(replay_dir):
        raise IOError('Unable to create replay dir at {}'.format(replay_dir))

    if not isinstance(template_name, basestring):
        raise TypeError('Template name is required to be of type str')

    if not isinstance(context, dict):
        raise TypeError('Context is required to be of type dict')

    if context_key not in context:
        raise ValueError('Context is required to contain a %s key' % context_key)

    replay_file = get_file_name(replay_dir, template_name)

    with open(replay_file, 'w') as outfile:
        json.dump(context, outfile)


# cookiecutter source: generate.py
def generate_files(repo_dir, context=None, output_dir='.',
                   overwrite_if_exists=False, context_key='cookiecutter'):
    """Render the templates and saves them to files.

    :param repo_dir: Project template input directory.
    :param context: Dict for populating the template's variables.
    :param output_dir: Where to output the generated project dir into.
    :param overwrite_if_exists: Overwrite the contents of the output directory
        if it exists.
    """
    template_dir = find_template(repo_dir, context_key)
    logging.debug('Generating project from {0}...'.format(template_dir))
    context = context or {}

    unrendered_dir = os.path.split(template_dir)[1]
    ensure_dir_is_templated(unrendered_dir)
    env = StrictEnvironment(
        context=context,
        keep_trailing_newline=True,
    )
    try:
        project_dir = render_and_create_dir(
            unrendered_dir,
            context,
            output_dir,
            env,
            overwrite_if_exists
        )
    except UndefinedError as err:
        msg = "Unable to create project directory '{}'".format(unrendered_dir)
        raise UndefinedVariableInTemplate(msg, err, context)

    # We want the Jinja path and the OS paths to match. Consequently, we'll:
    #   + CD to the template folder
    #   + Set Jinja's path to '.'
    #
    #  In order to build our files to the correct folder(s), we'll use an
    # absolute path for the target folder (project_dir)

    project_dir = os.path.abspath(project_dir)
    logging.debug('project_dir is {0}'.format(project_dir))

    _run_hook_from_repo_dir(repo_dir, 'pre_gen_project', project_dir, context)

    with work_in(template_dir):
        env.loader = FileSystemLoader('.')

        for root, dirs, files in os.walk('.'):
            # We must separate the two types of dirs into different lists.
            # The reason is that we don't want ``os.walk`` to go through the
            # unrendered directories, since they will just be copied.
            copy_dirs = []
            render_dirs = []

            for d in dirs:
                d_ = os.path.normpath(os.path.join(root, d))
                # We check the full path, because that's how it can be
                # specified in the ``_copy_without_render`` setting, but
                # we store just the dir name
                if copy_without_render(d_, context):
                    copy_dirs.append(d)
                else:
                    render_dirs.append(d)

            for copy_dir in copy_dirs:
                indir = os.path.normpath(os.path.join(root, copy_dir))
                outdir = os.path.normpath(os.path.join(project_dir, indir))
                logging.debug(
                    'Copying dir {0} to {1} without rendering'
                    ''.format(indir, outdir)
                )
                shutil.copytree(indir, outdir)

            # We mutate ``dirs``, because we only want to go through these dirs
            # recursively
            dirs[:] = render_dirs
            for d in dirs:
                unrendered_dir = os.path.join(project_dir, root, d)
                try:
                    render_and_create_dir(
                        unrendered_dir,
                        context,
                        output_dir,
                        env,
                        overwrite_if_exists
                    )
                except UndefinedError as err:
                    rmtree(project_dir)
                    _dir = os.path.relpath(unrendered_dir, output_dir)
                    msg = "Unable to create directory '{}'".format(_dir)
                    raise UndefinedVariableInTemplate(msg, err, context)

            for f in files:
                infile = os.path.normpath(os.path.join(root, f))
                if copy_without_render(infile, context):
                    outfile_tmpl = env.from_string(infile)
                    outfile_rendered = outfile_tmpl.render(**context)
                    outfile = os.path.join(project_dir, outfile_rendered)
                    logging.debug(
                        'Copying file {0} to {1} without rendering'
                        ''.format(infile, outfile)
                    )
                    shutil.copyfile(infile, outfile)
                    shutil.copymode(infile, outfile)
                    continue
                logging.debug('f is {0}'.format(f))
                try:
                    generate_file(project_dir, infile, context, env)
                except UndefinedError as err:
                    rmtree(project_dir)
                    msg = "Unable to create file '{}'".format(infile)
                    raise UndefinedVariableInTemplate(msg, err, context)

    _run_hook_from_repo_dir(repo_dir, 'post_gen_project', project_dir, context)

    return project_dir


# cookiecutter source: find.py
def find_template(repo_dir, context_key='cookiecutter'):
    """Determine which child directory of `repo_dir` is the project template.

    :param repo_dir: Local directory of newly cloned repo.
    :returns project_template: Relative path to project template.
    """
    logging.debug('Searching {0} for the project template.'.format(repo_dir))

    repo_dir_contents = os.listdir(repo_dir)

    project_template = None
    for item in repo_dir_contents:
        if context_key in item and '{{' in item and '}}' in item:
            project_template = item
            break

    if project_template:
        project_template = os.path.join(repo_dir, project_template)
        logging.debug(
            'The project template appears to be {0}'.format(project_template)
        )
        return project_template
    else:
        raise NonTemplatedInputDirException