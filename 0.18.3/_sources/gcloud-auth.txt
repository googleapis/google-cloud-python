Authentication
**************

.. _Overview:

Overview
========

*   **If you're running in Compute Engine or App Engine**,
    authentication should "just work".

*   **If you're developing locally**,
    the easiest way to authenticate is using the `Google Cloud SDK`_:

    .. code-block:: bash

        $ gcloud beta auth application-default login

    Note that this command generates credentials for client libraries. To authenticate the CLI itself, use:

    .. code-block:: bash

        $ gcloud auth login

    Previously, `gcloud auth login` was used for both use cases. If your gcloud installation does not support the new command, please update it:

    .. code-block:: bash

        $ gcloud components update

.. _Google Cloud SDK: http://cloud.google.com/sdk


*   **If you're running your application elsewhere**,
    you should download a `service account`_ JSON keyfile
    and point to it using an environment variable:

    .. code-block:: bash

        $ export GOOGLE_APPLICATION_CREDENTIALS="/path/to/keyfile.json"

.. _service account: https://cloud.google.com/storage/docs/authentication#generating-a-private-key

Client-Provided Authentication
==============================

Every package uses a :class:`Client <gcloud.client.Client>`
as a base for interacting with an API.
For example:

.. code-block:: python

    from gcloud import datastore
    client = datastore.Client()

Passing no arguments at all will "just work" if you've followed the
instructions in the :ref:`Overview`.
The credentials are inferred from your local environment by using
Google `Application Default Credentials`_.

.. _Application Default Credentials: https://developers.google.com/identity/protocols/application-default-credentials

.. _Precedence:

Credential Discovery Precedence
-------------------------------

When loading the `Application Default Credentials`_,
the library will check properties of your local environment
in the following order:

#. Application running in Google App Engine
#. JSON or PKCS12/P12 keyfile pointed to by
   ``GOOGLE_APPLICATION_CREDENTIALS`` environment variable
#. Credentials provided by the Google Cloud SDK (via ``gcloud auth login``)
#. Application running in Google Compute Engine

Explicit Credentials
====================

The Application Default Credentials discussed above can be useful
if your code needs to run in many different environments or
if you just don't want authentication to be a focus in your code.

However, you may want to be explicit because

* your code will only run in one place
* you may have code which needs to be run as a specific service account
  every time (rather than with the locally inferred credentials)
* you may want to use two separate accounts to simultaneously access data
  from different projects

In these situations, you can create an explicit
:class:`Credentials <oauth2client.client.Credentials>` object suited to your
environment.
After creation,
you can pass it directly to a :class:`Client <gcloud.client.Client>`:

.. code:: python

    client = Client(credentials=credentials)

Google App Engine Environment
-----------------------------

To create
:class:`credentials <oauth2client.contrib.appengine.AppAssertionCredentials>`
just for Google App Engine:

.. code:: python

    from oauth2client.contrib.appengine import AppAssertionCredentials
    credentials = AppAssertionCredentials([])

Google Compute Engine Environment
---------------------------------

To create
:class:`credentials <oauth2client.contrib.gce.AppAssertionCredentials>`
just for Google Compute Engine:

.. code:: python

    from oauth2client.contrib.gce import AppAssertionCredentials
    credentials = AppAssertionCredentials([])

Service Accounts
----------------

A `service account`_ can be used with both a JSON keyfile and
a PKCS12/P12 keyfile.

Directly creating ``credentials`` in `oauth2client`_ for a service
account is a rather complex process,
so as a convenience, the
:meth:`from_service_account_json() <gcloud.client.Client.from_service_account_json>`
and
:meth:`from_service_account_p12() <gcloud.client.Client.from_service_account_p12>`
factories are provided to create a :class:`Client <gcloud.client.Client>` with
service account credentials.

.. _oauth2client: http://oauth2client.readthedocs.org/en/latest/

For example, with a JSON keyfile:

.. code:: python

    client = Client.from_service_account_json('/path/to/keyfile.json')

.. tip::

    Unless you have a specific reason to use a PKCS12/P12 key for your
    service account,
    we recommend using a JSON key.

User Accounts (3-legged OAuth 2.0) with a refresh token
-------------------------------------------------------

The majority of cases are intended to authenticate machines or
workers rather than actual user accounts. However, it's also
possible to call Google Cloud APIs with a user account via
`OAuth 2.0`_.

.. _OAuth 2.0: https://developers.google.com/identity/protocols/OAuth2

.. tip::

    A production application should **use a service account**,
    but you may wish to use your own personal user account when first
    getting started with the ``gcloud-python`` library.

The simplest way to use credentials from a user account is via
Application Default Credentials using ``gcloud auth login``
(as mentioned above):

.. code:: python

    from oauth2client.client import GoogleCredentials
    credentials = GoogleCredentials.get_application_default()

This will still follow the :ref:`precedence <Precedence>`
described above,
so be sure none of the other possible environments conflict
with your user provided credentials.

Advanced users of `oauth2client`_ can also use custom flows to
create credentials using `client secrets`_ or using a
`webserver flow`_.
After creation, :class:`Credentials <oauth2client.client.Credentials>`
can be serialized with
:meth:`to_json() <oauth2client.client.Credentials.to_json>`
and stored in a file and then and deserialized with
:meth:`from_json() <oauth2client.client.Credentials.from_json>`.

.. _client secrets: https://developers.google.com/api-client-library/python/guide/aaa_oauth#flow_from_clientsecrets
.. _webserver flow: https://developers.google.com/api-client-library/python/guide/aaa_oauth#OAuth2WebServerFlow

Troubleshooting
===============

Setting up a Service Account
----------------------------

If your application is not running on Google Compute Engine,
you need a `Google Developers Service Account`_.

#. Visit the `Google Developers Console`_.

#. Create a new project or click on an existing project.

#. Navigate to **APIs & auth** > **APIs** and enable the APIs
   that your application requires.

   .. raw:: html

     <img src="https://raw.githubusercontent.com/GoogleCloudPlatform/gcloud-common/master/authentication/enable-apis.png"/>

  .. note::

      You may need to enable billing in order to use these services.

      * **BigQuery**

        * BigQuery API

      * **Datastore**

        * Google Cloud Datastore API

      * **Pub/Sub**

        * Google Cloud Pub/Sub

      * **Storage**

        * Google Cloud Storage
        * Google Cloud Storage JSON API

#. Navigate to **APIs & auth** > **Credentials**.

   You should see a screen like one of the following:

   .. raw:: html

     <img src="https://raw.githubusercontent.com/GoogleCloudPlatform/gcloud-common/master/authentication/create-new-service-account.png">

   .. raw:: html

     <img src="https://raw.githubusercontent.com/GoogleCloudPlatform/gcloud-common/master/authentication/create-new-service-account-existing-keys.png">

  Find the "Add credentials" drop down and select "Service account" to be
  guided through downloading a new JSON keyfile.

  If you want to re-use an existing service account,
  you can easily generate a new keyfile.
  Just select the account you wish to re-use,
  and click **Generate new JSON key**:

   .. raw:: html

     <img src="https://raw.githubusercontent.com/GoogleCloudPlatform/gcloud-common/master/authentication/reuse-service-account.png">

.. _Google Developers Console: https://console.developers.google.com/project
.. _Google Developers Service Account: https://developers.google.com/accounts/docs/OAuth2ServiceAccount

Using Google Compute Engine
---------------------------

If your code is running on Google Compute Engine,
using the inferred Google `Application Default Credentials`_
will be sufficient for retrieving credentials.

However, by default your credentials may not grant you
access to the services you intend to use.
Be sure when you `set up the GCE instance`_,
you add the correct scopes for the APIs you want to access:

* **All APIs**

    * ``https://www.googleapis.com/auth/cloud-platform``
    * ``https://www.googleapis.com/auth/cloud-platform.read-only``

* **BigQuery**

    * ``https://www.googleapis.com/auth/bigquery``
    * ``https://www.googleapis.com/auth/bigquery.insertdata``

* **Datastore**

    * ``https://www.googleapis.com/auth/datastore``
    * ``https://www.googleapis.com/auth/userinfo.email``

* **Pub/Sub**

    * ``https://www.googleapis.com/auth/pubsub``

* **Storage**

    * ``https://www.googleapis.com/auth/devstorage.full_control``
    * ``https://www.googleapis.com/auth/devstorage.read_only``
    * ``https://www.googleapis.com/auth/devstorage.read_write``

.. _set up the GCE instance: https://cloud.google.com/compute/docs/authentication#using

Advanced Customization
======================

Though the ``gcloud-python`` library defaults to using `oauth2client`_
to sign requests and ``httplib2`` for sending requests,
it is not a strict requirement.

The :class:`Client <gcloud.client.Client>` constructor accepts an optional
``http`` argument in place of a ``credentials`` object.
If passed, all HTTP requests made by the client will use your
custom HTTP object.

In order for this to be possible,
the ``http`` object must do two things:

* Handle authentication on its own
* Define a method ``request()`` that can subsitute for
  :meth:`httplib2.Http.request`.

The entire signature from ``httplib2`` need not be implemented,
we only use it as

.. code-block:: python

    http.request(uri, method=method_name, body=body, headers=headers)

For an example of such an implementation,
a ``gcloud-python`` user created a `custom HTTP class`_
using the `requests`_ library.

.. _custom HTTP class: https://github.com/GoogleCloudPlatform/gcloud-python/issues/908#issuecomment-110811556
.. _requests: http://www.python-requests.org/en/latest/

As for handling authentication on your own,
it may be easiest just to re-use bits from ``oauth2client``.
Unfortunately, these parts have a hard dependency on ``httplib2``.
We hope to enable using `custom HTTP libraries`_ with ``oauth2client`` at
some point.

.. _custom HTTP libraries: https://github.com/google/oauth2client/issues/128
