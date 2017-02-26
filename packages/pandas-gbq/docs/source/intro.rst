Introduction
============

Supported Data Types
++++++++++++++++++++

Pandas supports all these `BigQuery data types <https://cloud.google.com/bigquery/data-types>`__:
``STRING``, ``INTEGER`` (64bit), ``FLOAT`` (64 bit), ``BOOLEAN`` and
``TIMESTAMP`` (microsecond precision). Data types ``BYTES`` and ``RECORD``
are not supported.

Integer and boolean ``NA`` handling
+++++++++++++++++++++++++++++++++++

Since all columns in BigQuery queries are nullable, and NumPy lacks of ``NA``
support for integer and boolean types, this module will store ``INTEGER`` or
``BOOLEAN`` columns with at least one ``NULL`` value as ``dtype=object``.
Otherwise those columns will be stored as ``dtype=int64`` or ``dtype=bool``
respectively.

This is opposite to default pandas behaviour which will promote integer
type to float in order to store NAs.
`See here for how this works in pandas <http://pandas.pydata.org/pandas-docs/stable/gotchas.html#nan-integer-na-values-and-na-type-promotions>`__

While this trade-off works well for most cases, it breaks down for storing
values greater than 2**53. Such values in BigQuery can represent identifiers
and unnoticed precision lost for identifier is what we want to avoid.

.. _authentication:

Authentication
''''''''''''''

Authentication to the Google ``BigQuery`` service is via ``OAuth 2.0``.
Is possible to authenticate with either user account credentials or service account credentials.

Authenticating with user account credentials is as simple as following the prompts in a browser window
which will be automatically opened for you. You will be authenticated to the specified
``BigQuery`` account using the product name ``pandas GBQ``. It is only possible on local host.
The remote authentication using user account credentials is not currently supported in pandas.
Additional information on the authentication mechanism can be found
`here <https://developers.google.com/identity/protocols/OAuth2#clientside/>`__.

Authentication with service account credentials is possible via the `'private_key'` parameter. This method
is particularly useful when working on remote servers (eg. jupyter iPython notebook on remote host).
Additional information on service accounts can be found
`here <https://developers.google.com/identity/protocols/OAuth2#serviceaccount>`__.

Authentication via ``application default credentials`` is also possible. This is only valid
if the parameter ``private_key`` is not provided. This method also requires that
the credentials can be fetched from the environment the code is running in.
Otherwise, the OAuth2 client-side authentication is used.
Additional information on
`application default credentials <https://developers.google.com/identity/protocols/application-default-credentials>`__.

.. note::

   The `'private_key'` parameter can be set to either the file path of the service account key
   in JSON format, or key contents of the service account key in JSON format.

.. note::

   A private key can be obtained from the Google developers console by clicking
   `here <https://console.developers.google.com/permissions/serviceaccounts>`__. Use JSON key type.
