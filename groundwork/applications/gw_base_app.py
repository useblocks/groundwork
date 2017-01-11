"""
This is a small groundwork app, which can be started on command line by calling "groundwork".

It main function is to give an overview about already accessible plugins, signals and commands for the current
python environment.
"""
import os
from groundwork import App

main_content = """
{{ app.name }}
{{ "=" * app.name|length }}

Application overview
--------------------

Path: {{app.path}}

Active plugins: {{app.plugins.get()|count}}

Registered commands: {{app.commands.get()|count}}

Registered signals: {{app.signals.get()|count}}
Registered receivers: {{app.signals.get_receiver()|count}}

Registered documents: {{app.documents.get()|count}}

"""


def start_app():  # pragma: no cover
    app = register_app()
    app = configure_app(app)
    app.commands.start_cli()


def register_app():
    app = App([os.path.join(os.path.dirname(__file__), "configuration.py")])

    # The following used plugins are all part of groundwork and
    # therefore already registered via entry_point
    app.plugins.activate(["GwPluginsInfo", "GwSignalsInfo", "GwCommandsInfo", "GwDocumentsInfo",
                          "GwRecipesBuilder"])
    return app


def configure_app(app):
    # Let's register a main document, which is the entrance for the documentation and links
    # to all other documents.
    app.documents.register(name="main",
                                content=main_content,
                                description="Main document of application",
                                plugin=app)
    return app


if __name__ == "__main__":  # pragma: no cover
    start_app()
