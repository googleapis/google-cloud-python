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
`See here for how this works in pandas <https://pandas.pydata.org/pandas-docs/stable/gotchas.html#nan-integer-na-values-and-na-type-promotions>`__

While this trade-off works well for most cases, it breaks down for storing
values greater than 2**53. Such values in BigQuery can represent identifiers
and unnoticed precision lost for identifier is what we want to avoid.

.. _authentication:

Authentication
''''''''''''''

Authentication to the Google ``BigQuery`` service via ``OAuth 2.0``
is possible with either user or service account credentials.

Authentication via user account credentials is as simple as following the prompts in a browser window
which will automatically open for you. You authenticate to the specified
``BigQuery`` account using the product name ``pandas GBQ``.
The remote authentication is supported via the ``auth_local_webserver`` in ``read_gbq``. By default,
account credentials are stored in an application-specific hidden user folder on the operating system. You
can override the default credentials location via the ``PANDAS_GBQ_CREDENTIALS_FILE`` environment variable.
Additional information on the authentication mechanism can be found
`here <https://developers.google.com/identity/protocols/OAuth2#clientside/>`__.

Authentication via service account credentials is possible through the `'private_key'` parameter. This method
is particularly useful when working on remote servers (eg. Jupyter Notebooks on remote host).
Additional information on service accounts can be found
`here <https://developers.google.com/identity/protocols/OAuth2#serviceaccount>`__.

Authentication via ``application default credentials`` is also possible, but only valid
if the parameter ``private_key`` is not provided. This method requires that the 
credentials can be fetched from the development environment. Otherwise, the OAuth2 
client-side authentication is used. Additional information can be found on
`application default credentials <https://developers.google.com/identity/protocols/application-default-credentials>`__.

.. note::

   The `'private_key'` parameter can be set to either the file path of the service account key
   in JSON format, or key contents of the service account key in JSON format.

.. note::

   A private key can be obtained from the Google developers console by clicking
   `here <https://console.developers.google.com/permissions/serviceaccounts>`__. Use JSON key type.
