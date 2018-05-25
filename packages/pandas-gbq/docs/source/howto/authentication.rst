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

To use service account credentials, set the ``private_key`` parameter to one
of:

* A file path to the JSON file.
* A string containing the JSON file contents.

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
