Foreword
========

Challenges
----------
The initial version of groundwork was created inside an environment of cross-company development teams, with
very different skills on python and its ecosystem.

Main challenges were the needed understanding of already existing code, missing responsibilities for objects beside
the code (like tests and documentation) and a tight project plan, which wasn't really made to teach and update team
members about important changes on the code.

Beside these challenges on project level, there were also a lot of challenges on code level when it cames to
understanding architecture, databases, algorithms, interactions and more of a running application with a dynamic and
extensible behavior.

Goals
-----

groundwork was created to take most of these challenges and to provide easy, understandable and plugin-able solutions
for them.

The groundwork team has defined some goals, which shall be applicable for all groundwork based applications:

A Plugin bundles everything
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Beside the code itself, a plugin must also provide tests, documentation and meta data for its functionality.

As other application/plugin frameworks, groundwork is responsible to "clue" all plugin code together to a single
application.

But it also cares about the test cases of a plugin and makes tests of all used plugins available inside a single
test suite. Furthermore it also collects all plugin documentations and creates a single, overall documentation for
developers and users. The meta data of a plugin is collected as well and made available inside documentation and if
wished also in the
application as well.

Injections
~~~~~~~~~~
To lower the learning curve, heavily used libraries and their core functions shall be injected directly into
groundwork plugins by the usage of groundwork patterns.

For instance: Instead of initialising and configure Blinker for signals and Click for commands by yourself.
groundworks provides ``self.signal.send("Yehaa")`` and ``self.commands.register(...)`` directly inside plugin classes.

By defining own patterns, it is very easy to provide team members additional injected functions as well. E.g.
``self.web.route()`` for registering a web route or ``self.db.sql()`` to execute a SQL statement.

However, the library and its objects itself shall still be available and directly accessible to support uncommon or
not yet supporteded use cases.

Realtime documentation
~~~~~~~~~~~~~~~~~~~~~~
Nowadays it's really hard to get the big picture of an existing application. Normally only some kind of documentation
and the code itself are available as information source. However, the first one isn't often really maintained and the
other one gives you a really deep view only, which takes hours or even days to get it.

groundwork tries to retrieve and provide a lot of information from the executed code directly during runtime.
For instance, it is able to show registered and used signals or to create a list of available commands.

These kind of information depends hardly on activated plugins, which may change during runtime and affect the
documentation as well.





