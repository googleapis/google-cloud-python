Authentication
==============

pandas-gbq `authenticates with the Google BigQuery service
<https://cloud.google.com/bigquery/docs/authentication/>`_ via OAuth 2.0.

.. _authentication:


Authenticating with a Service Account
--------------------------------------

Using service account credentials is particularly useful when working on
remote servers without access to user input.

Create a service account key via the `service account key creation page
<https://console.cloud.google.com/apis/credentials/serviceaccountkey>`_ in
the Google Cloud Platform Console. Select the JSON key type and download the
key file.

To use service account credentials, set the ``credentials`` parameter to the result of a call to:

* :func:`google.oauth2.service_account.Credentials.from_service_account_file`,
    which accepts a file path to the JSON file.

    .. code:: python

        from google.oauth2 import service_account
        import pandas_gbq

        credentials = service_account.Credentials.from_service_account_file(
            'path/to/key.json',
        )
        df = pandas_gbq.read_gbq(sql, project_id="YOUR-PROJECT-ID", credentials=credentials)

* :func:`google.oauth2.service_account.Credentials.from_service_account_info`,
    which accepts a dictionary corresponding to the JSON file contents.

    .. code:: python

        from google.oauth2 import service_account
        import pandas_gbq

        credentials = service_account.Credentials.from_service_account_info(
            {
                "type": "service_account",
                "project_id": "YOUR-PROJECT-ID",
                "private_key_id": "6747200734a1f2b9d8d62fc0b9414c5f2461db0e",
                "private_key": "-----BEGIN PRIVATE KEY-----\nM...I==\n-----END PRIVATE KEY-----\n",
                "client_email": "service-account@YOUR-PROJECT-ID.iam.gserviceaccount.com",
                "client_id": "12345678900001",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://accounts.google.com/o/oauth2/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/...iam.gserviceaccount.com"
            },
        )
        df = pandas_gbq.read_gbq(sql, project_id="YOUR-PROJECT-ID", credentials=credentials)

Use the :func:`~google.oauth2.service_account.Credentials.with_scopes` method
to use authorize with specific OAuth2 scopes, which may be required in
queries to federated data sources such as Google Sheets.

.. code:: python

   credentials = ...
   credentials = credentials.with_scopes(
       [
           'https://www.googleapis.com/auth/drive',
           'https://www.googleapis.com/auth/cloud-platform',
       ],
   )
   df = pandas_gbq.read_gbq(..., credentials=credentials)

See the `Getting started with authentication on Google Cloud Platform
<https://cloud.google.com/docs/authentication/getting-started>`_ guide for
more information on service accounts.

.. _authentication-user:

Authenticating with a User Account
----------------------------------

Use the `pydata-google-auth <https://pydata-google-auth.readthedocs.io/>`__
library to authenticate with a user account (i.e. a G Suite or Gmail
account). The :func:`pydata_google_auth.get_user_credentials` function loads
credentials from a cache on disk or initiates an OAuth 2.0 flow if cached
credentials are not found.

.. code:: python

   import pandas_gbq
   import pydata_google_auth

   SCOPES = [
       'https://www.googleapis.com/auth/cloud-platform',
       'https://www.googleapis.com/auth/drive',
   ]

   credentials = pydata_google_auth.get_user_credentials(
       SCOPES,
       # Set auth_local_webserver to True to have a slightly more convienient
       # authorization flow. Note, this doesn't work if you're running from a
       # notebook on a remote sever, such as over SSH or with Google Colab.
       auth_local_webserver=True,


   df = pandas_gbq.read_gbq(
       "SELECT my_col FROM `my_dataset.my_table`",
       project_id='YOUR-PROJECT-ID',
       credentials=credentials,
   )

.. warning::

   Do not store credentials on disk when using shared computing resources
   such as a GCE VM or Colab notebook. Use the
   :data:`pydata_google_auth.cache.NOOP` cache to avoid writing credentials
   to disk.

   .. code:: python

      import pydata_google_auth.cache

      credentials = pydata_google_auth.get_user_credentials(
          SCOPES,
          # Use the NOOP cache to avoid writing credentials to disk.
          cache=pydata_google_auth.cache.NOOP,
      )

Additional information on the user credentials authentication mechanism
can be found in the `Google Cloud authentication guide
<https://cloud.google.com/docs/authentication/end-user>`__.


Default Authentication Methods
------------------------------

If the ``credentials`` parameter (or the deprecated ``private_key``
parameter) is ``None``, pandas-gbq tries the following authentication
methods:

1. In-memory, cached credentials at ``pandas_gbq.context.credentials``. See
   :attr:`pandas_gbq.Context.credentials` for details.

   .. code:: python

       import pandas_gbq

       credentials = ...  # From google-auth or pydata-google-auth library.

       # Update the in-memory credentials cache (added in pandas-gbq 0.7.0).
       pandas_gbq.context.credentials = credentials
       pandas_gbq.context.project = "your-project-id"

       # The credentials and project_id arguments can be omitted.
       df = pandas_gbq.read_gbq("SELECT my_col FROM `my_dataset.my_table`")

2. Application Default Credentials via the :func:`google.auth.default`
   function.

   .. note::

       If pandas-gbq can obtain default credentials but those credentials
       cannot be used to query BigQuery, pandas-gbq will also try obtaining
       user account credentials.

       A common problem with default credentials when running on Google
       Compute Engine is that the VM does not have sufficient scopes to query
       BigQuery.

3. User account credentials.

   pandas-gbq loads cached credentials from a hidden user folder on the
   operating system.

   Windows
       ``%APPDATA%\pandas_gbq\bigquery_credentials.dat``

   Linux/Mac/Unix
       ``~/.config/pandas_gbq/bigquery_credentials.dat``

   If pandas-gbq does not find cached credentials, it opens a browser window
   asking for you to authenticate to your BigQuery account using the product
   name ``pandas GBQ``.
