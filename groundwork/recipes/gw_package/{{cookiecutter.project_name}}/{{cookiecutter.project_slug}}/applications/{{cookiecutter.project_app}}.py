import os
from groundwork import App
from {{cookiecutter.project_slug}}.applications.configuration import APP_PATH


def start_app():
    # Let's be sure our APP_PATH really exists
    if not os.path.exists(APP_PATH):
        os.makedirs(APP_PATH)

    app = App([os.path.join(os.path.dirname(__file__), "configuration.py")])
    app.plugins.activate(app.config.get("PLUGINS", None))
    app.commands.start_cli()


if "main" in __name__:
    start_app()
