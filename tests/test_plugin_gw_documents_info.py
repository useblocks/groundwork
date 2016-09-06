import os
from click.testing import CliRunner
from groundwork.plugins import GwDocumentsInfo


def test_plugin_activation(basicApp):
    app = basicApp
    plugin = GwDocumentsInfo(app)
    plugin.activate()


def test_plugin_deactivation(basicApp):
    app = basicApp
    plugin = GwDocumentsInfo(app)
    plugin.activate()
    plugin.deactivate()


def test_plugin_list_docs(basicApp):
    app = basicApp
    plugin = GwDocumentsInfo(app)
    plugin.activate()
    runner = CliRunner()
    runner.invoke(app.commands.get("doc_list").click_command)


def test_plugin_show_docs(basicApp):
    app = basicApp
    plugin = GwDocumentsInfo(app)
    plugin.activate()
    runner = CliRunner()
    runner.invoke(app.commands.get("doc").click_command, input="x")


def test_plugin_store_docs(basicApp, tmpdir):
    app = basicApp
    plugin = GwDocumentsInfo(app)
    plugin.activate()

    output_folder = str(tmpdir.mkdir("output"))

    runner = CliRunner()
    runner.invoke(app.commands.get("doc_write").click_command, [output_folder], input="Y")

    runner.invoke(app.commands.get("doc_write").click_command, ["not_existing"])

    with open(os.path.join(output_folder, "test_file.txt"), "w") as file:
        file.write("content")
        runner.invoke(app.commands.get("doc_write").click_command, [output_folder])
