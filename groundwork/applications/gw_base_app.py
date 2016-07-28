"""
This is a small groundwork app, which can be started on command line by calling "groundwork".

It main function is to give an overview about already accessible plugins, signals and commands for the current
python environment.
"""

from groundwork import App


def start_app():
    app = App()

    # The following used plugins are all part of groundwork and
    # therefore already registered via entry_point
    app.plugins.activate(["GwPluginInfo", "GwSignalInfo", "GwCommandsInfo"])
    app.commands.start_cli()

if __name__ == "__main__":
    start_app()




