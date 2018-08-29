Resource Manager
----------------

.. toctree::
  :maxdepth: 2
  :hidden:

  client
  project

The Cloud Resource Manager API provides methods that you can use
to programmatically manage your projects in the Google Cloud Platform.
With this API, you can do the following:

- Get a list of all projects associated with an account
- Create new projects
- Update existing projects
- Delete projects
- Undelete, or recover, projects that you don't want to delete

.. note::

    Don't forget to look at the :ref:`Authentication` section below.
    It's slightly different from the rest of this library.

Installation
------------

Install the ``google-cloud-resource-manager`` library using ``pip``:

.. code-block:: console

    $ pip install google-cloud-resource-manager

Usage
-----

Here's a quick example of the full life-cycle:

.. code-block:: python

    >>> from google.cloud import resource_manager
    >>> client = resource_manager.Client()

    >>> # List all projects you have access to
    >>> for project in client.list_projects():
    ...     print(project)

    >>> # Create a new project
    >>> new_project = client.new_project('your-project-id-here',
    ...                                  name='My new project')
    >>> new_project.create()

    >>> # Update an existing project
    >>> project = client.fetch_project('my-existing-project')
    >>> print(project)
    <Project: Existing Project (my-existing-project)>
    >>> project.name = 'Modified name'
    >>> project.update()
    >>> print(project)
    <Project: Modified name (my-existing-project)>

    >>> # Delete a project
    >>> project = client.new_project('my-existing-project')
    >>> project.delete()

    >>> # Undelete a project
    >>> project = client.new_project('my-existing-project')
    >>> project.undelete()

.. _Authentication:

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

Once you run that command, ``google-cloud-python`` will automatically pick up the
credentials, and you can use the "automatic discovery" feature of the library.

Start by authenticating:

.. code-block:: bash

    $ gcloud auth login

And then simply create a client:

.. code-block:: python

    >>> from google.cloud import resource_manager
    >>> client = resource_manager.Client()

Changelog
~~~~~~~~~

For a list of all ``google-cloud-resource-manager`` releases:

.. toctree::
  :maxdepth: 2

  changelog
