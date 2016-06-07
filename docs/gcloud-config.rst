Configuration
*************

Overview
========

- Use service client objects to configure
  your applications.

  For example:

  .. code-block:: python

      >>> from gcloud import bigquery
      >>> client = bigquery.Client()

  You can override the detection of your default project by setting the
  ``project`` parameter when creating client objects.

.. code-block:: python

      >>> from gcloud import bigquery
      >>> client = bigquery.Client(project='my-project')

- Client objects hold both a ``project``
  and an authenticated connection to a service.

  .. code-block:: python

     >>> client.project
     u'my-project'

- The authentication credentials can be implicitly determined from the
  environment or directly. See :doc:`./gcloud-auth`.

- Logging in via ``gcloud auth login`` will automatically configure a JSON
  key file with your default project ID and credentials.
  Setting the ``GOOGLE_APPLICATION_CREDENTIALS`` and ``GCLOUD_PROJECT``
  environment variables will override the automatically configured credentials.

- You can change your default project ID to ``my-new-default-project`` with
  ``gcloud`` command line tool.

  .. code-block:: bash

     $ gcloud config set project my-new-default-project
