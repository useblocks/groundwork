groundwork
==========

.. revealjs::

    .. image:: _static/gw_slogan.png

    .. rv_small::

        | Press **s** to open speaker notes view or **ESC** for slides overview.
        | For well phrased, technical details please visit http://groundwork.rtfd.io

        Presentation can be freely used for meetups and co.

.. revealjs::

    .. revealjs:: Python Plugin Framework
        :subtitle: for fast development and high functional quality

    .. revealjs:: How groundwork supports you

        Support for command line, web, desktop

        Existing groundwork extensions

        Clean, focused architecture

        Common techniques for common problems

        Focused on functions, not on layout or design


.. revealjs::

    .. revealjs:: Clean architecture, reusable components
       :subtitle: Stop starting from scratch

    .. revealjs:: How groundwork structures your code

        .. list-table::
            :header-rows: 0

            * - Application
              - Bundles plugins to an usable function set
            * - Plugins
              - Provides use case specific functions
            * - Patterns
              - Provides technical interfaces

        Example:

        .. uml::

            @startuml
            skinparam backgroundColor transparent
            skinparam arrowColor #ffffff
            skinparam objectBackgroundColor #333
            skinparam objectBorderColor #fff
            skinparam objectAttributeFontColor #fff
            skinparam objectFontColor #fff
            skinparam shadowing false

            scale 1000 width

            object "Application JenkinsGate" as app

            object "plugin ViewDatabase" as pa
            object "plugin ViewJenkinsData" as pb
            object "plugin InformTeam" as pc

            object "pattern GwSqlPattern" as pta
            object "pattern MyJenkins" as ptb

            app : Provides easy overviews for Jenkins job data

            pa : View raw database data
            pb : Store and view data from jenkins
            pc : Inform teams on Jenkins changes

            pta : Connection to SQL-DB\nfrom groundwork-database
            ptb : Connection to internal Jenkins server

            app <-- pa
            app <-- pb
            app <-- pc

            pa <-- pta
            pb <-- pta
            pb <-- ptb
            pc <-- ptb
            @enduml

        .. rv_note::

            Diagram is generated using PlantUML.

    .. revealjs:: Example code

        Example: Application JenkinsGate

        .. rv_code::

            from groundwork import App

            class JenkinsGate:
                def __init__(self):
                    self.app = App()

                def start(self):
                    my_plugins = ["ViewDatabase", "ViewJenkinsData", "InformTeam"]
                    # Knowing plugin name is enough for activation
                    self.app.plugins.activate(my_plugins)

                    # Finally start the interface of choice, here a cli
                    self.app.commands.start_cli()

    .. revealjs:: Example code

        Example: Plugin ViewJenkinsData

        .. rv_code::

            from groundwork_database.patterns import GwSqlPattern
            from .patterns import MyJenkins

            class ViewJenkinsData(GwSqlPattern, MyJenkins):
                def __init__(self, app, **kwargs):
                    self.name = "ViewJenkinsData"
                    super().__init__(app, **kwargs)

                def activate(self):
                    self.db = self.databases.register("jenkins", "sqlite:///",
                                                      "database for jenkins data")

                    # Get and store first data already on activation
                    data = self.get_jenkins_data()
                    self.store_jenkins_data(data)

                def deactivate(self):
                    pass

                def get_jenkins_data(self):
                    data = self.jenkins.get_job("MyJob")
                    return data

                def store_jenkins_data(self, data)
                    self.db.add(data)
                    self.db.commit()

    .. revealjs:: Example code

        Example: Pattern MyJenkins

        .. rv_code::

            from groundwork.patterns import GwBasePattern

            class MyJenkins(GwBasePattern):
                def _init_(self, app, *args, **kwargs):
                    super().__init__(app, *args, **kwargs)
                    self.jenkins = Jenkins()

            class Jenkins:
                def get_job(self, job):
                    req =  requests.get("http://my_jenkins.com/{0}".format(job))
                    if req.status_code < 300:
                        return req.json()
                    else:
                        raise Exception("Ups, error happened!")

.. revealjs:: Thanks for your attention ...

    **... and see you on groundwork's issue tracker :)**

    .. list-table::
        :header-rows: 0

        * - github
          - `github.com/useblocks/groundwork <https://github.com/useblocks/groundwork>`_
        * - One-pager
          - `groundwork.useblocks.com <http://groundwork.useblocks.com>`_
        * - Technical documentation
          - `groundwork.rtfd.io <http://groundwork.rtfd.io>`_
        * - Tutorial
          - `useblocks.github.io/groundwork-tutorial <https://useblocks.github.io/groundwork-tutorial>`_
        * - This presentation
          - `groundwork-presentation.rtfd.io <http://groundwork-presentation.rtfd.io>`_



