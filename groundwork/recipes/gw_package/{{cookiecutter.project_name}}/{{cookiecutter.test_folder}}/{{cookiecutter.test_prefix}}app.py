def test_import_{{cookiecutter.project_slug}}():
    import {{cookiecutter.project_slug}}
    assert {{cookiecutter.project_slug}} is not None


def test_{{cookiecutter.project_plugin}}_activation():
    from {{cookiecutter.project_slug}}.applications import {{cookiecutter.project_app|upper}}
    from {{cookiecutter.project_slug}}.plugins import {{cookiecutter.project_plugin}}

    my_app = {{cookiecutter.project_app|upper}}()
    app = my_app.app
    app.plugins.activate(["{{cookiecutter.project_plugin}}"])
    plugin = app.plugins.get("{{cookiecutter.project_plugin}}")
    assert plugin is not None
    assert isinstance(plugin, {{cookiecutter.project_plugin}})
