Architecture
============

A groundwork application knows 3 levels of abstraction: :ref:`applications <application>`, :ref:`plugins <plugins>` and
:ref:`patterns <patterns>`.

These three levels were chosen to reflect the need of functional and technical separation. And it allows the easy
reusing and recombination of written code.

Definitions
-----------

Application
~~~~~~~~~~~
An :ref:`application <application>` bundles several needed functions, which were provided by :ref:`plugins <plugins>`.

Therefore an :ref:`application <application>` is a package of :ref:`plugins <plugins>` and has one or several functional
focuses. Like a web app for weather services or a console script for text file manipulations.

Plugin
~~~~~~
A :ref:`plugin <plugins>` has a strong user oriented, functional focus. Like providing user account handling, error
monitoring or functions for viewing log files.

It is also responsible for providing some sort of an interface to the user, like console commands or web pages.

If a plugin needs technical resources like a database connection, a web server or command registration, it needs
to use related :ref:`patterns <patterns>`.

A plugin can be activated and deactivated during application runtime.

Pattern
~~~~~~~
A :ref:`pattern <patterns>` provides technical resources to :ref:`plugins <plugins>`.
They are responsible for setting up database connections, providing APIs for command registration or for web page
handling.

A pattern must be requested by the plugin itself by using class inheritance. Therefore the pattern functions are hardly
coupled with related plugins during application runtime.

A pattern gets automatically deactivated, if all plugins are deactivated, which inherit from the related
pattern.

Example
-------

The following image shows an application example for a weather web service. The service has 3 main features:

 * Providing weather information, which are stored inside a database.
 * Allowing user registration, where users are stored inside a database and are getting a welcome email
   after registration.
 * Error handling, which sends emails to service administrators.

.. image:: _static/groundwork_architecture.png
   :width: 100%
   :align: center
   :alt: groundwork architecture


The 3 features were separated into 3 plugins, which focus is strongly based on the related use case: weather storage,
user handling and error monitoring.

Overall the plugins need 2 technical resources: A database and a way to send emails.
These 2 technical resources are realised by providing 2 patterns: a database connection pattern and an email sending
pattern.

The application itself is configured to load the three plugins during startup. The related patterns are getting
loaded and configured automatically.

Pseudo code
~~~~~~~~~~~
The following code is just some sort of a pseudo code, to give a first impression how such an architecture can be
realised.

patterns.py
```````````
The following code defines the 2 needed patterns for database connections and email sending::

   from groundwork.patterns import GwBasePattern


   class DatabasePattern(GwBasePattern):
      def __init__(self):
         self.database = Database()  # Database has functions: store(), get()


   class EmailPattern(GwBasePattern):
      def __init__(self):
         self.email = Email()   # Email has functions: send()

plugins.py
``````````
The 3 features are realised by the following 3 plugins::

   from .patterns import DatabasePattern, EmailPattern


   class WeatherStorePlugin(DatabasePattern):
      def __init__(self, app, **kwargs):
        self.name = "Weather Store"
        super().__init__(app, **kwargs)

      def activate(self):
         self.database.store(MyWeatherData)

      def get_weather(location):
         return self.database.get(location)

      def deactivate(self): pass


   class UserHandling(DatabasePattern, EmailPattern):
      def __init__(self, app, **kwargs):
        self.name = "User Handling"
        super().__init__(app, **kwargs)

      def register_user(self, username, email):
         self.database.store(User(username, email))
         self.email.send(email, "Welcome %s" % username)

      def deactivate(self): pass


   class ErrorMonitoring(EmailPattern):
      def __init__(self, app, **kwargs):
         self.name = "Error Monitoring"
         super().__init__(app, **kwargs)

      def activate(self):
         self.admin = "admin@my_company.com"

      def error_detected(traceback):
         self.email.send(self.admin, "Error found! %s" % traceback)

      def deactivate(self): pass

app.py
``````
The application itself only needs to load the three needed plugins::

   from groundwork import App
   from .plugins import WeatherStorePlugin, UserHandling, ErrorMonitoring

   # Load application and register plugins
   my_app = App(plugins=[WeatherStorePlugin, UserHandling, ErrorMonitoring])

   # Activate plugins
   my_app.activate(["Weather Store", "User Handling", "Error Monitoring"])












