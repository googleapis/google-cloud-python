.. toctree::
  :maxdepth: 0
  :hidden:

=========
Big Query
=========

Using the API
=============

Authorization / Configuration
-----------------------------

- Use :class:`Client <gcloud.bigquery.client.Client>` objects to configure
  your applications.

- :class:`Client <gcloud.bigquery.client.Client>` objects hold both a ``project``
  and an authenticated connection to the PubSub service.

- The authentication credentials can be implicitly determined from the
  environment or directly via
  :meth:`from_service_account_json <gcloud.bigquery.client.Client.from_service_account_json>`
  and
  :meth:`from_service_account_p12 <gcloud.bigquery.client.Client.from_service_account_p12>`.

- After setting ``GOOGLE_APPLICATION_CREDENTIALS`` and ``GCLOUD_PROJECT``
  environment variables, create an instance of
  :class:`Client <gcloud.bigquery.client.Client>`.

  .. doctest::

     >>> from gcloud import bigquery
     >>> client = bigquery.Client()

- Override the credentials inferred from the environment by passing explicit
  ``credentials`` to one of the alternative classmethods, `from_service_account_json`:

  .. doctest::

     >>> from gcloud import bigquery
     >>> client = bigquery.Client.from_service_account_json('/path/to/creds.json')

  or `from_service_account_p12`:

  .. doctest::

     >>> from gcloud import bigquery
     >>> client = bigquery.Client.from_service_account_p12('/path/to/creds.p12', 'jrandom@example.com')

- Override the project inferred from the environment by passing an explicit
  ``project`` to the constructor, or to either of the alternative classmethods:

  .. doctest::

     >>> from gcloud import bigquery
     >>> client = bigquery.Client(project='PROJECT_ID')
