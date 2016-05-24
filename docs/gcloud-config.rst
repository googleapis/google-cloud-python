Configuration
*************

Overview
========

- Use service :class:`Client <gcloud.client.Client>` objects to configure
  your applications.

  For example:

  .. code-block:: python

     >>> from gcloud import bigquery
     >>> client = bigquery.Client()

- :class:`Client <gcloud.client.Client>` objects hold both a ``project``
  and an authenticated connection to a service.

- The authentication credentials can be implicitly determined from the
  environment or directly via
  :meth:`from_service_account_json <gcloud.client.Client.from_service_account_json>`
  and
  :meth:`from_service_account_p12 <gcloud.client.Client.from_service_account_p12>`.

- Logging in with the `Google Cloud SDK`_ will automatically configure a JSON
  key file with your default project ID and credentials.
  Setting the ``GOOGLE_APPLICATION_CREDENTIALS`` and ``GCLOUD_PROJECT``
  environment variables will override the automatically configured credentials.

- You can change your default project ID to ``my-new-default-project`` with
  ``gcloud`` command line tool.

  .. code-block:: bash

     $ gcloud config set project my-new-default-project

.. _Google Cloud SDK: http://cloud.google.com/sdk

- You can override the credentials inferred from the environment by passing
  explicit ``credentials`` to one of the alternative ``classmethod`` factories,
  :meth:`gcloud.client.Client.from_service_account_json`:

  .. code-block:: python

     >>> from gcloud import bigquery
     >>> client = bigquery.Client.from_service_account_json('/path/to/creds.json')

  or :meth:`gcloud.client.Client.from_service_account_p12`:

  .. code-block:: python

     >>> from gcloud import bigquery
     >>> client = bigquery.Client.from_service_account_p12(
     ...     '/path/to/creds.p12', 'jrandom@example.com')
