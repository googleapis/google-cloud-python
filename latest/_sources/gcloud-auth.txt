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

        $ gcloud auth login

.. _Google Cloud SDK: http://cloud.google.com/sdk


*   **If you're running your application elsewhere**,
    you should download a `service account`_ JSON keyfile
    and point to it using an environment variable:

    .. code-block:: bash

        $ export GOOGLE_APPLICATION_CREDENTIALS="/path/to/keyfile.json"

.. _service account: https://cloud.google.com/storage/docs/authentication#generating-a-private-key

Client-Provided Authentication
==============================

Every package uses a :class:`Client <gcloud.client.Client>` as a base
for interacting with an API. For example:

.. code-block:: python

    from gcloud import datastore
    client = datastore.Client()

Passing no arguments at all will "just work" if you've following the
instructions in the :ref:`Overview`. The credentials are inferred from your
local environment by using Google `Application Default Credentials`_.

.. _Application Default Credentials: https://developers.google.com/identity/protocols/application-default-credentials

Credential Discovery Precedence
-------------------------------

When loading the `Application Default Credentials`_, the library will check
properties of your local environment in the following order

#. Application running in Google App Engine
#. JSON or PKCS12/P12 keyfile pointed to by
   ``GOOGLE_APPLICATION_CREDENTIALS`` environment variable
#. Credentials provided by the Google Cloud SDK (via ``gcloud auth login``)
#. Application running in Google Compute Engine

Loading Credentials Explicitly
------------------------------

In addition, the
:meth:`from_service_account_json() <gcloud.client.Client.from_service_account_json>`
and
:meth:`from_service_account_p12() <gcloud.client.Client.from_service_account_p12>`
factories can be used if you know the specific type of credentials you'd
like to use.

.. code:: python

    client = Client.from_service_account_json('/path/to/keyfile.json')

.. tip::

    Unless you have an explicit reason to use a PKCS12 key for your
    service account, we recommend using a JSON key.

Finally, if you are **familiar** with the `oauth2client`_ library, you can
create a ``credentials`` object and pass it directly:

.. code:: python

    client = Client(credentials=credentials)

.. _oauth2client: http://oauth2client.readthedocs.org/en/latest/
