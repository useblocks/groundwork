import os
from click.testing import CliRunner
from groundwork.plugins import GwRecipesBuilder


def test_plugin_activation(basicApp):
    app = basicApp
    plugin = GwRecipesBuilder(app)
    plugin.activate()


def test_plugin_deactivation(basicApp):
    app = basicApp
    plugin = GwRecipesBuilder(app)
    plugin.activate()
    plugin.deactivate()


def test_plugin_list_recipes(emptyApp):
    app = emptyApp
    plugin = GwRecipesBuilder(app)
    plugin.activate()
    runner = CliRunner()
    runner.invoke(app.commands.get("recipe_list").click_command)


def test_plugin_build_recipes(emptyApp, tmpdir):
    app = emptyApp
    plugin = GwRecipesBuilder(app)
    plugin.activate()

    output_folder = str(tmpdir.mkdir("output"))
    old_path = os.getcwd()
    os.chdir(output_folder)

    runner = CliRunner()
    runner.invoke(app.commands.get("recipe_build").click_command, ["gw_package"])

    os.chdir(old_path)

    runner.invoke(app.commands.get("recipe_build").click_command, ["not_existing"])
