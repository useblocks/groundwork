.. revealjs::

    .. revealjs:: Extensive runtime information
       :subtitle: Know who did what in your application

       groundwork forces developers during registration of objects to provide:

       * A meaningful name
       * A description

       groundwork stores also:

       * plugin name
       * function name


    .. revealjs:: Retrieving runtime information
       :subtitle: In code

       On plugin level

       .. rv_code::

              from groundwork.patterns import GwCommandsPattern
              class MyPlugin(GwCommandsPattern):
                     def print_my_commands():
                            commands = self.commands.get()  # Gets commands for this plugin only
                            for command in commands:
                                   print("{command} registered by {plugin}".format(
                                         command.command, command.plugin.name))

       On application level

       .. rv_code::

              from groundwork import App

              my_app = App()
              my_app.plugins.activate("MyPlugin", "AnotherPlugin", "AwesomePlugin")
              commands = my_app.commands.get()  # Gets all commands of used app
              for command in commands:
                     print("{command} registered by {plugin}".format(command.command, command.plugin.name))

    .. revealjs:: Retrieving runtime information
        :subtitle: on cli

        With loaded plugin `GwDocumentsInfo <http://groundwork.readthedocs.io/en/latest/documents.html#live-example>`_

        .. rv_code::

            >>> my_app doc

        .. image:: _static/runtime_cli_doc.png



    .. revealjs:: Retrieving runtime information
        :subtitle: in browser

        Using GwWebManager of  `groundwork-web <https://groundwork-web.readthedocs.io>`_ package

        .. image:: _static/webmanager_overview.png
            :height: 250px

        .. image:: _static/webmanager_plugin.png
            :height: 250px

