import os

import pytest

from groundwork.patterns.gw_recipes_pattern import IncorrectParameterTypeException, \
    HooksException, RecipeMissingException


def test_recipe_plugin_activation(basicApp):
    plugin = basicApp.plugins.get("RecipePlugin")
    assert plugin is not None
    assert plugin.active is True


def test_recipe_registration(basicApp):
    basicApp.plugins.get("RecipePlugin")
    test_recipe = basicApp.recipes.get("test_recipe")
    assert test_recipe is not None


def test_recipe_registration_with_hooks(basicApp):
    plugin = basicApp.plugins.get("RecipePlugin")
    plugin.recipes.register("recipe_hooks",
                            os.path.join(os.path.dirname(__file__), "../recipes/gw_test_app"),
                            "test recipe", "Installation done", pre_hook=pre_hook_test_function_positive,
                            post_hook=post_hook_test_function_positive)
    test_recipe = basicApp.recipes.get("recipe_hooks")
    assert test_recipe is not None


def test_recipe_registration_with_hooks_parameter_none(basicApp):
    plugin = basicApp.plugins.get("RecipePlugin")
    plugin.recipes.register("recipe_hooks_none",
                            os.path.join(os.path.dirname(__file__), "../recipes/gw_test_app"),
                            "test recipe", "Installation done", pre_hook=None,
                            post_hook=None)
    test_recipe = basicApp.recipes.get("recipe_hooks_none")
    assert test_recipe is not None


def test_recipe_registration_with_hooks_incorrect_parameter_type_prehook(basicApp):
    basicApp.plugins.get("RecipePlugin")
    with pytest.raises(IncorrectParameterTypeException):
        basicApp.recipes.register("test",
                                  os.path.join(os.path.dirname(__file__), "../recipes/gw_test_app"),
                                  "test recipe", "Installation done", pre_hook="incorrect_parameter")


def test_recipe_registration_with_hooks_incorrect_parameter_type_posthook(basicApp):
    basicApp.plugins.get("RecipePlugin")
    with pytest.raises(IncorrectParameterTypeException):
        basicApp.recipes.register("test",
                                  os.path.join(os.path.dirname(__file__), "../recipes/gw_test_app"),
                                  "test recipe", "Installation done", post_hook="incorrect_parameter")


def test_recipe_build_with_pre_hook_return_false(basicApp, tmpdir):
    plugin = basicApp.plugins.get("RecipePlugin")
    plugin.recipes.register("recipe_hooks",
                            os.path.join(os.path.dirname(__file__), "recipes/gw_test_app"),
                            "test recipe", "Installation done", pre_hook=pre_hook_test_function_negative)
    test_recipe = plugin.recipes.get("recipe_hooks")
    output_folder = str(tmpdir.mkdir("output"))
    with pytest.raises(HooksException):
        test_recipe.build(output_folder, no_input=True, extra_context=None)


def test_recipe_build_with_post_hook_return_false(basicApp, tmpdir):
    plugin = basicApp.plugins.get("RecipePlugin")
    plugin.recipes.register("recipe_hooks",
                            os.path.abspath(os.path.join(os.path.dirname(__file__), "recipes/gw_test_app")),
                            "test recipe", "Installation done", post_hook=post_hook_test_function_negative)
    test_recipe = plugin.recipes.get("recipe_hooks")
    output_folder = str(tmpdir.mkdir("output"))
    with pytest.raises(HooksException):
        test_recipe.build(output_folder, no_input=True, extra_context=None)


def pre_hook_test_function_positive():
    return True


def post_hook_test_function_positive():
    return True


def pre_hook_test_function_negative():
    return False


def post_hook_test_function_negative():
    return False


def test_recipe_build(basicApp, tmpdir):
    basicApp.plugins.get("RecipePlugin")
    test_recipe = basicApp.recipes.get("test_recipe")
    output_folder = str(tmpdir.mkdir("output"))
    output_data = test_recipe.build(output_folder, no_input=True, extra_context=None)
    assert output_data == os.path.join(output_folder, "My Package")


def test_recipe_build_missing_extra_context_parameter(basicApp, tmpdir):
    basicApp.plugins.get("RecipePlugin")
    test_recipe = basicApp.recipes.get("test_recipe")
    output_folder = str(tmpdir.mkdir("output"))
    output_data = test_recipe.build(output_folder, no_input=True)
    assert output_data == os.path.join(output_folder, "My Package")


def test_recipe_build_extra_context_parameter_userdata(basicApp, tmpdir):
    basicApp.plugins.get("RecipePlugin")
    test_recipe = basicApp.recipes.get("test_recipe")
    output_folder = str(tmpdir.mkdir("output"))
    user_data = {'project_name': 'TestProject'}
    output_data = test_recipe.build(output_folder, no_input=True, extra_context=user_data)
    assert output_data == os.path.join(output_folder, "TestProject")


def test_recipe_build_no_input_incorrect_type(basicApp, tmpdir):
    basicApp.plugins.get("RecipePlugin")
    test_recipe = basicApp.recipes.get("test_recipe")
    output_folder = str(tmpdir.mkdir("output"))
    with pytest.raises(IncorrectParameterTypeException):
        assert test_recipe.build(output_folder, no_input="Test", extra_context=None)


def test_recipe_build_extra_context_incorrect_type(basicApp, tmpdir):
    basicApp.plugins.get("RecipePlugin")
    test_recipe = basicApp.recipes.get("test_recipe")
    output_folder = str(tmpdir.mkdir("output"))
    with pytest.raises(IncorrectParameterTypeException):
        assert test_recipe.build(output_folder, no_input=True, extra_context="Test")


def test_recipe_jinja(basicApp, tmpdir):
    basicApp.plugins.get("RecipePlugin")
    test_recipe = basicApp.recipes.get("test_recipe")
    output_folder = str(tmpdir.mkdir("output"))
    test_recipe.build(output_folder, no_input=True)
    assert "My Name" in open(os.path.join(output_folder, "My Package/README.rst")).read()


def test_rescipe_get(basicApp):
    plugin = basicApp.plugins.get("RecipePlugin")
    plugin.recipes.get("test_recipe")


def test_recipe_unregister(basicApp):
    plugin = basicApp.plugins.get("RecipePlugin")
    recipe = plugin.recipes.get("test_recipe")
    plugin.recipes.unregister(recipe.name)
    recipe = plugin.recipes.get("test_recipe")
    assert recipe is None


def test_recipe_registered_already(basicApp):
    plugin = basicApp.plugins.get("RecipePlugin")
    recipe = plugin.recipes.get("test_recipe")
    if recipe is not None:
        with pytest.raises(Exception) as e:
            plugin.recipes.register("test_recipe",
                                    os.path.join(os.path.dirname(__file__), "../recipes/gw_test_app"),
                                    "test recipe")
        assert str(e.value)


def test_missing_recipe(basicApp, tmpdir):
    output_dir = str(tmpdir.mkdir("output"))
    os.chdir(output_dir)
    plugin = basicApp.plugins.get("RecipePlugin")
    with pytest.raises(RecipeMissingException):
        plugin.recipes.build(recipe="missing_recipe")
