.. toctree::
  :maxdepth: 1
  :hidden:

GCloud Auth
-----------

For the majority of cases, authentication with the ``gcloud`` library
will **"just work"**. Credentials are loaded implicitly from the environment
where the code is running and **no code** is required to enable authentication
within your code.

The core :mod:`gcloud.credentials` module provides helper methods
for any account type needed.

A production application should **use a service account**, but you may
wish to use your own personal user account when first getting started with
the ``gcloud`` library.

=============
Basic Example
=============

With an environment set up to use `Google Default Credentials`_, your
API requests will be authenticated automatically:

.. code-block:: python

   from gcloud import datastore
   from gcloud import pubsub
   from gcloud import storage

   entities = datastore.get([
       datastore.Key('EntityKind', 1, dataset_id='foo')])

   bucket = storage.get_bucket('bucket-name')

   pubsub.Topic('topic_name', project_id='my.project').create()

=============
Advanced Uses
=============

A custom connection can be used as the default, but will need to be
explicitly set. The
:func:`set_default_connection() <gcloud.datastore.__init__.set_default_connection>`
function is provided in all sub-packages to set a connection. For
example, in the ``datastore`` sub-package:

.. code-block:: python

   credentials = get_custom_credentials()
   connection = datastore.Connection(credentials=credentials)
   datastore.set_default_connection(connection)

   # ... Create keys.
   entities = datastore.get([key1, key2])

If no default is set, all functions which make a connection to an API
accept an optional ``connection`` argument. For example, with ``datastore``,
the implicit behavior can be duplicated with:

.. code-block:: python

   from gcloud.credentials import get_credentials

   credentials = get_credentials().create_scoped(datastore.SCOPE)
   connection = datastore.Connection(credentials=credentials)

   # ... Create keys.
   entities = datastore.get([key1, key2], connection=connection)

If no connection is passed explicity and
:func:`set_default_connection() <gcloud.datastore.__init__.set_default_connection>`
is never called, the request will fail:

.. code-block:: python

   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "gcloud/datastore/api.py", line 200, in get
       connection = _require_connection(connection)
     File "gcloud/datastore/api.py", line 82, in _require_connection
       raise EnvironmentError('Connection could not be inferred.')
   EnvironmentError: Connection could not be inferred.

---------------------------------
Multiple Simultaneous Connections
---------------------------------

Some applications will need to read and write data into multiple projects.
This may require using more than one set of credentials (either via JSON key
files or other means).

As a result, a single connection will be insufficient to make all API requests.
To use two separate connections, proceed as above by using explicit connections
in each function that makes an API request:

.. code-block:: python

   credentials1 = my_custom_credentials_function('foo')
   credentials2 = my_custom_credentials_function('bar')

   connection1 = datastore.Connection(credentials=credentials1)
   connection2 = datastore.Connection(credentials=credentials2)

   key1 = datastore.Key('CompanyA', 1337, dataset_id='foo')
   entities1 = datastore.get([key1], connection=connection1)

   key2 = datastore.Key('CompanyB', 42, dataset_id='bar')
   datastore.delete([key2], connection=connection2)

If one is connection used more often than another, it can still be used as the
default:

.. code-block:: python

   datastore.set_default_connection(connection=connection1)

   entities1 = datastore.get([key1])

   datastore.delete([key2], connection=connection2)

=======================
Supported Account Types
=======================

With the helper functions provided, we support the following
OAuth 2.0 account types:

- Google `App Engine Service Accounts`_
- Google `Compute Engine Service Accounts`_
- `Service Accounts`_ with JSON `Service Account Key`_
- User Accounts (3-legged `OAuth`_ 2.0) with refresh token
- Service Accounts with PKCS12 / P12 `Service Account Key`_

==========================
Google Default Credentials
==========================

All but one `supported account type`_ listed above can be handled by using
Google `Application Default`_ credentials via
:func:`get_credentials() <gcloud.credentials.get_credentials>`. This function
can be used directly to obtain ``credentials`` to be passed
to a ``Connection`` or can be used implictly by calling
:func:`get_connection (datastore) <gcloud.datastore.__init__.get_connection>`
and :func:`get_connection (storage) <gcloud.storage.__init__.get_connection>`.

----------------------------------
Google App Engine Service Accounts
----------------------------------

:func:`get_credentials() <gcloud.credentials.get_credentials>`
implicitly handles **Google App Engine Service Accounts** with no user
intervention required.

To explicitly load these credentials:

.. code-block:: python

   from oauth2client.appengine import AppAssertionCredentials
   credentials = AppAssertionCredentials([])

--------------------------------------
Google Compute Engine Service Accounts
--------------------------------------

:func:`get_credentials() <gcloud.credentials.get_credentials>` implicitly
handles **Google Compute Engine Service Accounts** with no user intervention
required. However, when creating the `instance`_, the service account
must be enabled and the correct set of scopes must be selected for
the services you intend to use.

To explicitly load these credentials:

.. code-block:: python

   from oauth2client.gce import AppAssertionCredentials
   credentials = AppAssertionCredentials([])

.. _instance: https://cloud.google.com/compute/docs/instances

-------------------------------
Service Accounts with JSON keys
-------------------------------

As mentioned above, support for **Service Accounts with JSON keys** can be done
by setting the ``GOOGLE_APPLICATION_CREDENTIALS`` environment variable:

.. code-block:: bash

  $ export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key_file.json"

If you'd like to load these credentials explicitly rather than via the
environment, you can use
:func:`get_for_service_account_json() <gcloud.credentials.get_for_service_account_json>`:

.. code-block:: python

   from gcloud.credentials import get_for_service_account_json

   private_key_path = '/path/to/key_file.p12'

   credentials = get_for_service_account_json(private_key_path)

-------------------------------------------------
User Accounts (3-legged OAuth) with refresh token
-------------------------------------------------

As mentioned in the introduction, a production application should
**use a service account**. However, when just getting started with the library,
it can be useful to just use an authorized user account.

If you've installed the ``gcloud`` command line `tool`_, you can authorize
a user account by running

.. code-block:: bash

  $ gcloud auth login

(it's very likely you've already done so).

.. _tool: https://cloud.google.com/sdk/gcloud/

After doing so, you can re-use these credentials within ``gcloud``
just by using :func:`get_credentials() <gcloud.credentials.get_credentials>`:

.. code-block:: python

   from gcloud.credentials import get_credentials
   credentials = get_credentials()

.. note::

   The ``gcloud`` CLI tool will create an authorized user JSON credentials
   file on your system. On \*nix systems, this will typically reside in
   ``${HOME}/.config/gcloud/application_default_credentials.json``.

In addition to using the credentials from the ``gcloud`` CLI, you can use your
own credentials file. This file will contain a JSON object with four keys:

.. code-block:: json

  {
    "client_id": "123",
    "client_secret": "secret",
    "refresh_token": "FOO",
    "type": "authorized_user"
  }

This can be used just as a JSON key file can be used for a service account

.. code-block:: bash

  $ export GOOGLE_APPLICATION_CREDENTIALS="/path/to/authorized_user_credentials.json"

As with Service Accounts with JSON keys, you can explicitly load an authorized
user account key with
:func:`get_for_service_account_json() <gcloud.credentials.get_for_service_account_json>`.

=================================
PKCS12 / P12 Service Account Keys
=================================

PKCS12 / P12 Service Account keys are the only `supported account type`_ above
that is not covered by Google Default Credentials.

.. _supported account type: #supported-account-types

This is because **JSON Service Account Credentials** are the preferred format.

If for some reason you need (or want) to use a P12 key,
:func:`get_for_service_account_p12() <gcloud.credentials.get_for_service_account_p12>`
allows you to load service account credentials for such a key:

.. code-block:: python

   from gcloud.credentials import get_for_service_account_p12

   client_email = 'foo@developer.gserviceaccount.com'
   private_key_path = '/path/to/key_file.p12'

   credentials = get_for_service_account_p12(client_email, private_key_path)

Notice that unlike the JSON Service Account Key, the P12 key also
**requires the email address** for the service account. (This is because the
JSON key file contains the email address, while the P12 key file only contains
the private key bytes.)

==========================
Enabling a service account
==========================

.. include:: _components/enabling-a-service-account.rst

.. _Service Account Key: https://cloud.google.com/storage/docs/authentication#generating-a-private-key
.. _Application Default: https://developers.google.com/accounts/docs/application-default-credentials
.. _App Engine Service Accounts: https://cloud.google.com/appengine/docs/python/appidentity/
.. _Compute Engine Service Accounts: https://cloud.google.com/compute/docs/authentication#metadata
.. _OAuth: https://developers.google.com/accounts/docs/OAuth2WebServer
.. _Service Accounts: #enabling-a-service-account
