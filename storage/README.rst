Python Client for Google Cloud Storage
======================================

|GA| |pypi| |versions| 

`Google Cloud Storage`_ allows you to store data on
Google infrastructure with very high reliability, performance and
availability, and can be used to distribute large data objects to users
via direct download.

- `Client Library Documentation`_
- `Storage API docs`_

.. |GA| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-storage.svg
   :target: https://pypi.org/project/google-cloud-storage
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-storage.svg
   :target: https://pypi.org/project/google-cloud-storage
.. _Google Cloud Storage: https://cloud.google.com/storage/docs
.. _Client Library Documentation: https://googleapis.dev/python/storage/latest
.. _Storage API docs: https://cloud.google.com/storage/docs/json_api/v1

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Google Cloud Storage API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Google Cloud Storage API.:  https://cloud.google.com/storage
.. _Setup Authentication.: https://googleapis.dev/python/google-api-core/latest/auth.html

Installation
~~~~~~~~~~~~

Install this library in a `virtualenv`_ using pip. `virtualenv`_ is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With `virtualenv`_, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

.. _`virtualenv`: https://virtualenv.pypa.io/en/latest/


Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^
Python >= 3.5

Deprecated Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7. Python 2.7 support will be removed on January 1, 2020.


Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-storage


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-storage


Example Usage
~~~~~~~~~~~~~

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
