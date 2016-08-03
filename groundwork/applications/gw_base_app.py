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


def start_app():
    os.chdir(os.path.dirname(__file__))
    app = App(["gw_base_app.conf"])

    # The following used plugins are all part of groundwork and
    # therefore already registered via entry_point
    app.plugins.activate(["GwPluginsInfo", "GwSignalsInfo", "GwCommandsInfo", "GwDocumentsInfo"])

    # Let's register a main document, which is the entrance for the documentation and links
    # to all other documents.
    app.documents.register(name="main",
                                content=main_content,
                                description="Main document of application",
                                plugin=app)

    app.commands.start_cli()

if __name__ == "__main__":
    start_app()
