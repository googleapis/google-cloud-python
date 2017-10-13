Python Client for Google Cloud Storage
======================================

    Python idiomatic client for `Google Cloud Storage`_

.. _Google Cloud Storage: https://cloud.google.com/storage/docs

|pypi| |versions|

-  `Documentation`_

.. _Documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/storage/client.html

Quick Start
-----------

.. code-block:: console

    $ pip install --upgrade google-cloud-storage

Fore more information on setting up your Python development environment, such as installing ``pip`` and on your system, please refer to `Python Development Environment Setup Guide`_ for Google Cloud Platform.

.. _Python Development Environment Setup Guide: https://cloud.google.com/python/setup

Authentication
--------------

With ``google-cloud-python`` we try to make authentication as painless as
possible. Check out the `Authentication section`_ in our documentation to
learn more. You may also find the `authentication document`_ shared by all
the ``google-cloud-*`` libraries to be helpful.

.. _Authentication section: https://google-cloud-python.readthedocs.io/en/latest/core/auth.html
.. _authentication document: https://github.com/GoogleCloudPlatform/google-cloud-common/tree/master/authentication

Using the API
-------------

Google `Cloud Storage`_ (`Storage API docs`_) allows you to store data on
Google infrastructure with very high reliability, performance and
availability, and can be used to distribute large data objects to users
via direct download.

.. _Cloud Storage: https://cloud.google.com/storage/docs
.. _Storage API docs: https://cloud.google.com/storage/docs/json_api/v1

See the ``google-cloud-python`` API `storage documentation`_ to learn how to
connect to Cloud Storage using this Client Library.

.. _storage documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/storage/client.html

You need to create a Google Cloud Storage bucket to use this client library.
Follow along with the `official Google Cloud Storage documentation`_ to learn
how to create a bucket.

.. _official Google Cloud Storage documentation: https://cloud.google.com/storage/docs/cloud-console#_creatingbuckets

.. code:: python

    from google.cloud import storage
    client = storage.Client()
    # https://console.cloud.google.com/storage/browser/[bucket-id]/
    bucket = client.get_bucket('bucket-id-here')
    # Then do other things...
    blob = bucket.get_blob('remote/path/to/file.txt')
    print(blob.download_as_string())
    blob.upload_from_string('New contents!')
    blob2 = bucket.blob('remote/path/storage.txt')
    blob2.upload_from_filename(filename='/local/path.txt')

.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-storage.svg
   :target: https://pypi.org/project/google-cloud-storage
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-storage.svg
   :target: https://pypi.org/project/google-cloud-storage
