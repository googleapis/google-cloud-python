DB API Connection
=================

.. _spanner-client:


Creating a Connection
---------------------

To use the API, the :class:`~google.cloud.spanner_django.connection.Connection`
class defines a high-level interface which handles connection to a Spanner
databse:

.. code:: python

    from google.cloud.spanner import connection
    conn = connection.Connection()

Configuration
-------------

- For an overview of authentication in ``google.cloud-python``,
  see `Authentication
  <https://googleapis.dev/python/google-api-core/latest/auth.html>`_.

- In addition to any authentication configuration, you can also set the
  :envvar:`GCLOUD_PROJECT` environment variable for the Google Cloud Console
  project you'd like to interact with. If your code is running in Google App
  Engine or Google Compute Engine the project will be detected automatically.
  (Setting this environment variable is not required, you may instead pass the
  ``project`` explicitly when constructing a
  :class:`~google.cloud.spanner_django.connection.Connection`).
