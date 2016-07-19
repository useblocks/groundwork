Registered Commands
-------------------

.. contents:: 

plugin_list
~~~~~~~~~~~
| **Command name**: plugin_list
| **Command plugin**: GwPluginInfo

| **Command description**:
| List all plugins

doc_list
~~~~~~~~
| **Command name**: doc_list
| **Command plugin**: GwDocumentationBuilder

| **Command description**:
| Lists all registerd documents

test_2
~~~~~~
| **Command name**: test_2
| **Command plugin**: GwDomainManager

| **Command description**:
| my test desc

user_create
~~~~~~~~~~~
| **Command name**: user_create
| **Command plugin**: GwUserManager

| **Command description**:
| creates a new user

**Command parameters**:

* **--username, -u** : user name (**Required**)
* **--name, -n** : User's name (**Required**)
* **--email, -e** : User's eMail (**Required**)
* **--password, -p** : User's password (**Required**)
* **--admin, -a** : Makes user to administrator (**Flag**)
doc_build
~~~~~~~~~
| **Command name**: doc_build
| **Command plugin**: GwDocumentationBuilder

| **Command description**:
| Starts documentation creation process for sphinx project in doc-folder

**Command parameters**:

* **--builder, -b** : Set the builder/output format of the documentation. E.g.: html, text, pdf, pickle... See sphinx doc for more. 
* **--all, -a** : If given, always write all output files. The default is to only write output files for new and changed source files. (**Flag**)
* **--fetch, -f** : If given, a doc_fetch is started beforebuild. (**Flag**)
* **--show, -s** : Execute doc_show after build. (**Flag**)
test
~~~~
| **Command name**: test
| **Command plugin**: GwDomainManager

| **Command description**:
| my test desc

doc_init
~~~~~~~~
| **Command name**: doc_init
| **Command plugin**: GwDocumentationBuilder

| **Command description**:
| Initialize the documentation by creating needed folders and files

**Command parameters**:

* **--force, -f** : Will delete existing sphinx projects before create a new one. (**Flag**)
flask
~~~~~
| **Command name**: flask
| **Command plugin**: GwFlaskManager

| **Command description**:
| Starting flask

**Command parameters**:

* **--debug, -d** : Activates debug mode (**Flag**)
receiver_list
~~~~~~~~~~~~~
| **Command name**: receiver_list
| **Command plugin**: GwSignalInfo

| **Command description**:
| List of all signal receivers

doc_show
~~~~~~~~
| **Command name**: doc_show
| **Command plugin**: GwDocumentationBuilder

| **Command description**:
| Opens the generated documentation on console

**Command parameters**:

* **--html, -h** : Opens the generated html documentation in the system default browser. (**Flag**)
doc_fetch
~~~~~~~~~
| **Command name**: doc_fetch
| **Command plugin**: GwDocumentationBuilder

| **Command description**:
| Fetch documentation snippets and create all-in-one sphinx project

user_list
~~~~~~~~~
| **Command name**: user_list
| **Command plugin**: GwUserManager

| **Command description**:
| lists all users

signal_list
~~~~~~~~~~~
| **Command name**: signal_list
| **Command plugin**: GwSignalInfo

| **Command description**:
| List of all signals

