.. revealjs::

    .. revealjs:: Batteries included
       :subtitle: Common solutions for common problems

       Command line interface

       Signals and Receivers

       Threads

       Shared objects

       Recipes

       Documents


    .. revealjs:: Command line interface

        Based on `Click <http://click.pocoo.org>`_

        Application: Start cli

        .. rv_code::

            from groundwork import App
            my_app = App()
            my_app.plugins.activate(["MyPlugin"])
            my_app.commands.start_cli()

        Plugin: Register command

        .. rv_code::

            from groundwork.patterns import GwCommandsPattern

            class MyPlugin(GwCommandsPattern):
                def activate(self):
                    self.commands.register(command="my_command",
                                           description="executes something",
                                           function=self.my_command,
                                           params=[])

                def my_command(self, plugin, **kwargs):
                    print("Yehaaa")

        .. rv_small:: groundwork documentation: `Commands <http://groundwork.readthedocs.io/en/latest/commands.html>`_

    .. revealjs:: Signals and Receivers

        Based on `Blinker <https://pythonhosted.org/blinker/>`_


        Sending a signal

        .. rv_code::

            class MyPlugin(GwBasePattern):
                def activate(self):
                    self.signals.register(signal ="my_signal",
                                          description="this is my first signal")

                    self.signals.send("my_signal")

        Receive a signal

        .. rv_code::

            class MyPlugin_2(GwBasePattern):
                def activate(self):
                    self.signals.connect(receiver="My signal receiver",
                                         signal="my_signal",
                                         function=self.fancy_stuff,
                                         description="Doing some fancy")

                def fancy_stuff(plugin, **kwargs):
                    print("FANCY STUFF!!! " * 50)

        .. rv_small:: groundwork documentation: `Signals and Receivers <http://groundwork.readthedocs.io/en/latest/signals.html>`_

    .. revealjs:: Threads

        Based on `Python Threading <https://docs.python.org/3.5/library/threading.html>`_

        .. rv_code::

            from groundwork.patterns import GwThreadsPattern

            class MyPlugin(GwThreadsPattern):
                def activate(self):
                    my_thread = self.threads.register(name="my_thread",
                                                      description="run something",
                                                      function=self.my_thread)
                    my_thread.run()

                def my_thread(self, plugin, **kwargs):
                    print("Yehaaa")

        .. rv_small:: groundwork documentation: `Threading <http://groundwork.readthedocs.io/en/latest/threads.html>`_

    .. revealjs:: Shared objects

        Provide a shared objects

        .. rv_code::

            from groundwork.patterns import GwSharedObjectsPattern

            class MyPlugin(GwSharedObjectsPattern):
                def activate(self):
                    self.my_shared_object = {"name": "shared"
                                             "name2": "object"}
                    self.shared_objects.register(name="my_shared_object",
                                                 description="A shared object of My Plugin",
                                                 obj=self.my_shared_object)


        Access a shared object

        .. rv_code::

            class MyPlugin2(GwSharedObjectsPattern)
                def some_function(self):
                    obj = self.shared_objects.access("my_shared_object")

        .. rv_small:: groundwork documentation: `Shared Objects <http://groundwork.readthedocs.io/en/latest/shared_objects.html>`_

    .. revealjs:: Recipes

        Based on `Cookiecutter <https://cookiecutter.readthedocs.io/en/latest/>`_

        Register a recipe

        .. rv_code::

            class My_Plugin(GwRecipesPattern):
               def activate(self):
                   ...
                   self.recipes.register("my_recipe",
                                         os.path.abspath("path/to/recipe/folder"),
                                         description="An awesome recipe",
                                         final_words="Yehaa, installation is done")

        Recipe folder structure

        .. rv_code::

            /
            |-- cookiecutter.json
            |
            |-- {{ cookiecutter.project_name}}
                |
                |-- other directories/files, which will be copied.


        Using recipe

        .. rv_code::

            groundwork recipe_build my_recipe

        .. rv_small:: groundwork documentation: `Recipes <http://groundwork.readthedocs.io/en/latest/recipes.html>`_


    .. revealjs:: Documents

        Based on `Jinja <http://jinja.pocoo.org>`_ and `RestructuredText <http://docutils.sourceforge.net/rst.html>`_

        Register a document

        .. rv_code::

            from groundwork.patterns import GwDocumentsPattern

            class My_Plugin(GwDocumentsPattern):
                def activate(self):
                    my_content = """
                    My Plugin
                    =========
                    Application name: {{app.name}}
                    Plugin name: {{plugin.name}}
                    """
                    self.documents.register(name="my_document",
                                            content=my_content,
                                            description="Provides information about 'My Plugin'")

        .. rv_small:: groundwork documentation: `Documents <http://groundwork.readthedocs.io/en/latest/documents.html>`_


