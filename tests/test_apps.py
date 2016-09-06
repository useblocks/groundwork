# This file tests read-to-use applications, which are provided by groundwork.

from click.testing import CliRunner
from groundwork.applications import gw_base_app


def test_gw_app_start():
    runner = CliRunner()
    app = gw_base_app.register_app()
    app = gw_base_app.configure_app(app)
    runner.invoke(app.commands._click_root_command)
