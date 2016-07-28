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
~~~~~~~~~~~~~~~
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

GwDocumentsPattern
~~~~~~~~~~~~~~~~~~
.. currentmodule:: groundwork.patterns.gw_documents_pattern

.. autoclass:: GwDocumentsPattern
   :members:
   :inherited-members:
   :show-inheritance:
   :undoc-members:

Plugins
-------

GwPluginInfo
~~~~~~~~~~~~

.. autoclass:: groundwork.plugins.gw_plugin_info.GwPluginInfo
   :members:
   :show-inheritance:
   :inherited-members:
   :undoc-members:

GwSignalInfo
~~~~~~~~~~~~

.. autoclass:: groundwork.plugins.gw_signal_info.GwSignalInfo
   :members:
   :show-inheritance:
   :inherited-members:
   :undoc-members:

GwCommandslInfo
~~~~~~~~~~~~~~~

.. autoclass:: groundwork.plugins.gw_commands_info.GwCommandsInfo
   :members:
   :show-inheritance:
   :inherited-members:
   :undoc-members:
