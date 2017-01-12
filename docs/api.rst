API
===

Application Object
------------------
.. automodule:: groundwork

.. autoclass:: groundwork.App
   :members:
   :private-members:

SignalsApplication
------------------
.. autoclass:: groundwork.signals.SignalsApplication
   :members:

.. autoclass:: groundwork.signals.Signal
   :members:

.. autoclass:: groundwork.signals.Receiver
   :members:

Configuration
-------------

ConfigManager
~~~~~~~~~~~~~
.. autoclass:: groundwork.configuration.configmanager.ConfigManager
   :members:

Config
~~~~~~
.. autoclass:: groundwork.configuration.configmanager.Config
   :members:

PluginManagers
--------------
.. automodule:: groundwork.pluginmanager

.. currentmodule:: groundwork.pluginmanager

PluginManager
~~~~~~~~~~~~~

.. autoclass:: PluginManager
   :members:
   :inherited-members:
   :undoc-members:
   :private-members:

PluginClassManager
~~~~~~~~~~~~~~~~~~

.. autoclass:: PluginClassManager
   :members:
   :inherited-members:
   :undoc-members:
   :private-members:

Plugin Patterns
---------------

GwBasePattern
~~~~~~~~~~~~~
.. automodule::  groundwork.patterns.gw_base_pattern

.. currentmodule:: groundwork.patterns.gw_base_pattern

.. autoclass:: GwBasePattern
   :members:
   :inherited-members:
   :undoc-members:

.. autoclass:: SignalsPlugin
   :members:


GwCommandPattern
~~~~~~~~~~~~~~~~~
.. currentmodule:: groundwork.patterns.gw_commands_pattern

.. autoclass:: GwCommandsPattern
   :members:
   :inherited-members:
   :show-inheritance:
   :undoc-members:

.. data:: GwCommandsPattern.commands

.. autoclass:: CommandsListPlugin
   :members:
   :undoc-members:

.. autoclass:: CommandsListApplication
   :members:
   :undoc-members:

GwSharedObjectsPattern
~~~~~~~~~~~~~~~~~~~~~~
.. currentmodule:: groundwork.patterns.gw_shared_objects_pattern

.. autoclass:: GwSharedObjectsPattern
   :members:
   :show-inheritance:
   :undoc-members:

.. data:: GwSharedObjectsPattern.shared_objects

.. autoclass:: SharedObjectsListPlugin
   :members:
   :undoc-members:

.. autoclass:: SharedObjectsListApplication
   :members:
   :undoc-members:

GwDocumentsPattern
~~~~~~~~~~~~~~~~~~
.. currentmodule:: groundwork.patterns.gw_documents_pattern

.. autoclass:: GwDocumentsPattern
   :members:
   :inherited-members:
   :show-inheritance:
   :undoc-members:

.. autoclass:: DocumentsListPlugin
   :members:
   :undoc-members:

.. autoclass:: DocumentsListApplication
   :members:
   :undoc-members:

GwThreadsPattern
~~~~~~~~~~~~~~~~~~
.. currentmodule:: groundwork.patterns.gw_threads_pattern

.. autoclass:: GwThreadsPattern
   :members:
   :inherited-members:
   :show-inheritance:
   :undoc-members:

.. autoclass:: ThreadsListPlugin
   :members:
   :undoc-members:

.. autoclass:: ThreadsListApplication
   :members:
   :undoc-members:

.. autoclass:: Thread
   :members:
   :undoc-members:

.. autoclass:: ThreadWrapper
   :members:
   :undoc-members:

GwRecipePattern
~~~~~~~~~~~~~~~
.. automodule::  groundwork.patterns.gw_recipes_pattern

.. currentmodule:: groundwork.patterns.gw_recipes_pattern

.. autoclass:: GwRecipesPattern
   :members:
   :inherited-members:
   :undoc-members:

.. autoclass:: RecipesListPlugin
   :members:
   :undoc-members:

.. autoclass:: RecipesListApplication
   :members:
   :undoc-members:

.. autoclass:: Recipe
   :members:
   :undoc-members:


Plugins
-------

GwDocumentsInfo
~~~~~~~~~~~~~~~

.. autoclass:: groundwork.plugins.gw_documents_info.GwDocumentsInfo
   :show-inheritance:


GwPluginInfo
~~~~~~~~~~~~

.. autoclass:: groundwork.plugins.gw_plugins_info.GwPluginsInfo
   :show-inheritance:

GwSignalInfo
~~~~~~~~~~~~

.. autoclass:: groundwork.plugins.gw_signals_info.GwSignalsInfo
   :show-inheritance:

GwCommandslInfo
~~~~~~~~~~~~~~~

.. autoclass:: groundwork.plugins.gw_commands_info.GwCommandsInfo
   :show-inheritance:

GwRecipesBuilder
~~~~~~~~~~~~~~~~

.. autoclass:: groundwork.plugins.gw_recipes_builder.GwRecipesBuilder
   :show-inheritance:
