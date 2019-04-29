import os


def test_recipe_plugin_activation(basicApp):
    plugin = basicApp.plugins.get("RecipePlugin")
    assert plugin is not None
    assert plugin.active is True


def test_recipe_registration(basicApp):
    basicApp.plugins.get("RecipePlugin")
    test_recipe = basicApp.recipes.get("test_recipe")
    assert test_recipe is not None


def test_recipe_build(basicApp, tmpdir):
    basicApp.plugins.get("RecipePlugin")
    test_recipe = basicApp.recipes.get("test_recipe")
    output_folder = str(tmpdir.mkdir("output"))
    output_data = test_recipe.build(output_dir=output_folder, no_input=True, extra_context=None)
    assert output_data == os.path.join(output_folder, "My Package")


def test_recipe_build_missing_extra_context_parameter(basicApp, tmpdir):
    basicApp.plugins.get("RecipePlugin")
    test_recipe = basicApp.recipes.get("test_recipe")

    output_folder = str(tmpdir.mkdir("output"))
    output_data = test_recipe.build(output_dir=output_folder, no_input=True)

    assert output_data == os.path.join(output_folder, "My Package")


def test_recipe_build_extra_context_parameter_userdata(basicApp, tmpdir):
    basicApp.plugins.get("RecipePlugin")
    test_recipe = basicApp.recipes.get("test_recipe")

    output_folder = str(tmpdir.mkdir("output"))
    user_data = {'project_name': 'TestProject'}
    output_data = test_recipe.build(output_dir=output_folder, no_input=True, extra_context=user_data)

    assert output_data == os.path.join(output_folder, "TestProject")


def test_recipe_jinja(basicApp, tmpdir):
    basicApp.plugins.get("RecipePlugin")
    test_recipe = basicApp.recipes.get("test_recipe")

    output_folder = str(tmpdir.mkdir("output"))
    test_recipe.build(output_dir=output_folder, no_input=True, extra_context=None)
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
