Python Client for Google Cloud Resource Manager
===============================================

|alpha| |pypi| |versions| 

`Google Cloud Resource Manager`_ API provides methods that you can use
to programmatically manage your projects in the Google Cloud Platform.
With this API, you can do the following:

- Get a list of all projects associated with an account
- Create new projects
- Update existing projects
- Delete projects
- Undelete, or recover, projects that you don't want to delete

- `Client Library Documentation`_
- `Product Documentation`_


.. |alpha| image:: https://img.shields.io/badge/support-alpha-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#alpha-support
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-resource-manager.svg
   :target: https://pypi.org/project/google-cloud-resource-manager/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-resource-manager.svg
   :target: https://pypi.org/project/google-cloud-resource-manager/
.. _Google Cloud Resource Manager: https://cloud.google.com/resource-manager/
.. _Client Library Documentation: https://googleapis.dev/python/cloudresourcemanager/latest
.. _Product Documentation: https://cloud.google.com/resource-manager/docs/

.. note::

    Don't forget to look at the `Authentication`_ section below.
    It's slightly different from the rest of this library.

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Google Cloud Resource Manager API.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Google Cloud Resource Manager API.:  https://cloud.google.com/resource-manager

Installation
~~~~~~~~~~~~

Install this library in a `virtualenv`_ using pip. `virtualenv`_ is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With `virtualenv`_, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

.. _`virtualenv`: https://virtualenv.pypa.io/en/latest/


Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^
Python >= 3.5

Deprecated Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7. Python 2.7 support will be removed on January 1, 2020.


Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-resource-manager


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-resource-manager


Authentication
~~~~~~~~~~~~~~

Unlike the other APIs, the Resource Manager API is focused on managing your
various projects inside Google Cloud Platform. What this means (currently, as
of August 2015) is that you can't use a Service Account to work with some
parts of this API (for example, creating projects).

The reason is actually pretty simple: if your API call is trying to do
something like create a project, what project's Service Account can you use?
Currently none.

This means that for this API you should always use the credentials
provided by the `Google Cloud SDK`_, which you can get by running
``gcloud auth login``.

.. _Google Cloud SDK: http://cloud.google.com/sdk

Once you run that command, ``google-cloud-python`` will automatically pick up
the credentials, and you can use the "automatic discovery" feature of the
library.

Start by authenticating:

.. code-block:: bash

    $ gcloud auth login

And then simply create a client:

.. code-block:: python

   from google.cloud import resource_manager
   client = resource_manager.Client()

Using the API
-------------

Here's a quick example of the full life-cycle:

.. code-block:: python

   from google.cloud import resource_manager

   client = resource_manager.Client()

   # List all projects you have access to
   for project in client.list_projects():
       print(project)

   # Create a new project
   new_project = client.new_project(
    'your-project-id-here', name='My new project')
   new_project.create()

   # Update an existing project
   project = client.fetch_project('my-existing-project')
   project.name = 'Modified name'
   project.update()

   # Delete a project
   project = client.new_project('my-existing-project')
   project.delete()

   # Undelete a project
   project = client.new_project('my-existing-project')
   project.undelete()
