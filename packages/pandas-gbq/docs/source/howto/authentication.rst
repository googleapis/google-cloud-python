Authentication
==============

pandas-gbq `authenticates with the Google BigQuery service
<https://cloud.google.com/bigquery/docs/authentication/>`_ via OAuth 2.0.

.. _authentication:


Authentication with a Service Account
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

        credentials = google.oauth2.service_account.Credentials.from_service_account_file(
            'path/to/key.json',
        )
        df = pandas_gbq.read_gbq(sql, project_id="YOUR-PROJECT-ID", credentials=credentials)

* :func:`google.oauth2.service_account.Credentials.from_service_account_info`,
    which accepts a dictionary corresponding to the JSON file contents.

    .. code:: python

        credentials = google.oauth2.service_account.Credentials.from_service_account_info(
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

See the `Getting started with authentication on Google Cloud Platform
<https://cloud.google.com/docs/authentication/getting-started>`_ guide for
more information on service accounts.

Default Authentication Methods
------------------------------

If the ``private_key`` parameter is ``None``, pandas-gbq tries the following
authentication methods:

1. Application Default Credentials via the :func:`google.auth.default`
   function.

   .. note::

       If pandas-gbq can obtain default credentials but those credentials
       cannot be used to query BigQuery, pandas-gbq will also try obtaining
       user account credentials.

       A common problem with default credentials when running on Google
       Compute Engine is that the VM does not have sufficient scopes to query
       BigQuery.

2. User account credentials.

   pandas-gbq loads cached credentials from a hidden user folder on the
   operating system. Override the location of the cached user credentials
   by setting the ``PANDAS_GBQ_CREDENTIALS_FILE`` environment variable.

   If pandas-gbq does not find cached credentials, it opens a browser window
   asking for you to authenticate to your BigQuery account using the product
   name ``pandas GBQ``.

   Additional information on the user credentails authentication mechanism
   can be found `here
   <https://developers.google.com/identity/protocols/OAuth2#clientside/>`__.
