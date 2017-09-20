.. revealjs::

    .. revealjs:: groundwork extensions
        :subtitle: Some examples

        groundwork-database

        groundwork-web

        groundwork-users

        groundwork-validation

        groundwork-spreadsheets


    .. revealjs:: groundwork-database

        Based on `SQLAlchemy <https://www.sqlalchemy.org/>`_

        Documentation: `groundwork-database.readthedocs.io <https://groundwork-database.readthedocs.io>`_

        .. rv_code::

            from groundwork import App
            from groundwork_database.patterns import GwSqlPattern

            class MyPlugin(GwSqlPattern):
                def _init_(self, app, *args, **kwargs):
                    self.name = "My Plugin"
                    super().__init__(app, *args, **kwargs)

                def activate(self):
                    name = "my_db"
                    database_url = "sqlite:///:memory:"
                    description = "My personal test database"
                    db = self.databases.register(name, database_url, description)

                    User = _get_user_class(db.Base)
                    my_user = User(name="Me")
                    db.add(my_user)
                    db.commit()

                def print_user(name):
                    db = self.databases.get("my_db")
                    user = db.query(User).filter_by(name=name).first()
                    if user is not None:
                        print(user.name)
                    else:
                        print("User %s not found." % name)

                def _get_user_class(base):
                    class User(base):
                        id = Column(Integer, primary_key=True)
                        name = Column(String)
                    return User


            if __name__ == "__main__":
                my_app = App()
                my_plugin = MyPlugin(my_app)
                my_plugin.activate()
                my_plugin.print_user("me")

    .. revealjs:: groundwork-web

        Based on `Flask <http://flask.pocoo.org>`_

        Documentation: `groundwork-web.readthedocs.io <https://groundwork-web.readthedocs.io>`_

        .. rv_code::

            self.web.contexts.register("webmanager",
                                       template_folder=template_folder,
                                       static_folder=static_folder,
                                       url_prefix="/webmanager",
                                       description="context for web manager urls")

            self.web.routes.register("/<my_object>", ["GET"], self.__manager_view, context="webmanager",
                                     name="manager_view", description="Entry-Page for the webmanager")

            def __manager_view(self, my_object):
                return self.web.render("manager.html", me=my_object)

    .. revealjs:: groundwork-users

        Based on `Flask-Security <https://pythonhosted.org/Flask-Security/>`_

        Documentation: `groundwork-users.readthedocs.io <https://groundwork-users.readthedocs.io/en/latest/>`_

        .. image:: _static/web_user_example.png
            :height: 400px


    .. revealjs:: groundwork-validation

        Documentation: `groundwork-validation.readthedocs.io <https://groundwork-validation.readthedocs.io/en/latest/>`_

        Validates interactions with files, folders, databases or applications

        Validations can be based on hashes or expected content of return values

        Developed to support `ISO 26262 <https://en.wikipedia.org/wiki/ISO_26262>`_


    .. revealjs:: groundwork-spreadsheets

        Documentation: `groundwork-spreadsheets.readthedocs.io <https://groundwork-spreadsheets.readthedocs.io/en/latest/>`_

        Reads and validates Excel documents and provides its data as easy accessible dictionary