Authentication
--------------

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
    you should download a service account JSON keyfile
    and point to it using an environment variable:

    .. code-block:: bash

        $ export GOOGLE_APPLICATION_CREDENTIALS="/path/to/keyfile.json"

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
