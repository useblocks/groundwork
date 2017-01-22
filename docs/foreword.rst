Foreword
========

Challenges
----------
The initial version of groundwork was created inside an environment of cross-company development teams, with
very different skills on Python and its ecosystem.

Main challenges were the needed understanding of already existing code, missing responsibilities for artefacts besides
the code (like tests and documentation) and a tight project plan, which never contained time slots needed to teach and update team
members about important changes on the code.

Besides these challenges on the project level, there were also a lot of challenges on code level when it came to
understanding architecture, databases, algorithms, interactions and more of a running application with dynamic and
extensible behavior.

Goals
-----
groundwork was created to take most of these challenges and to provide easy, understandable and plugin-able solutions.

The groundwork team has defined goals, which shall be applicable for all groundwork based applications:

A plugin bundles everything
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Besides the code itself, a :ref:`plugin <plugins>` also provide tests, documentation and meta data for its functionality.

Like other application/plugin frameworks, groundwork is responsible to "glue" all plugin code together to a single
application.

But it also cares about test cases of a plugin and makes tests of all used plugins available inside a single
test suite. Furthermore, it also collects all plugin documentation and creates a single, overall documentation for
developers and users. The meta data of a plugin is collected as well and made available inside the documentation and - if
desired - also in the application.

Injections
~~~~~~~~~~
To lower the learning curve, commonly used libraries and their core functions can directly be injected into
groundwork plugins by using groundwork patterns.

For instance: Instead of initialising and configuring `Blinker <https://pythonhosted.org/blinker/>`_
for signals and `Click <http://click.pocoo.org/latest>`_ for command line interfaces by yourself, groundworks
provides ``self.signal.send("Yehaa")`` and ``self.commands.register(...)`` directly inside plugin classes.

By defining own :ref:`patterns <patterns>`, it is very easy to provide team members additional injected functions. E.g.
``self.web.route()`` for registering a web route or ``self.db.sql()`` to execute a SQL statement.

However, the library and its objects can still be made available and directly accessible to support uncommon or
not yet supported use cases.

Realtime documentation
~~~~~~~~~~~~~~~~~~~~~~
Nowadays it's really hard to get the big picture of an existing application. Normally only some kind of documentation
and the code itself are available as information source. However, the former is rarely well maintained and the
later gives you a structured, but too deep view which takes hours or even days to understand.

groundwork tries to retrieve and provide a lot of information from the executed code directly during runtime.
For instance, it is able to show registered and used signals or to create a list of available commands.

These information depends on the activated plugins, which may change during runtime and affect the
documentation as well.


Technical background
--------------------
groundwork was created to glue code-snippets from various developers together and make their nested functions
easily available.

In Python this is commonly achieved by importing modules, initialising a class of them and storing the class instance
in a local or global variable.
However, these mechanism aren't really dynamic and the relationship between different classes and objects is hard-coded,
without any chance to change it during runtime.

groundwork uses :ref:`plugins <plugins>`, based on cooperative-multi-inheritance to load and manage needed
attributes and functions from reusable :ref:`patterns <patterns>`.
It also enforces the usage of the groundwork :class:`~groundwork.patterns.gw_base_pattern.GwBasePattern` for all
plugins to make common attributes and functions available.

For more information about cooperative-multi-inheritance see:

 * `Raymond Hettinger - Super considered super! - PyCon 2015 <https://www.youtube.com/watch?v=EiOglTERPEo>`_
 * `Python docs for classes and inheritance <https://docs.python.org/3/tutorial/classes.html#multiple-inheritance>`_

