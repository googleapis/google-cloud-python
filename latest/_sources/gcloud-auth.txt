Authentication
--------------

Quick overview
==============

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
