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
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#general-availability
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
.. _Setup Authentication.: https://cloud.google.com/storage/docs/reference/libraries#setting_up_authentication

Installation
~~~~~~~~~~~~

`Set up a Python development environment`_ and install this library in a `venv`.
`venv`_ is a tool to create isolated Python environments. The basic problem it
addresses is one of dependencies and versions, and indirectly permissions.

Make sure you're using Python 3.3 or later, which includes `venv`_ by default.
With `venv`, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

.. _Set up a Python development environment: https://cloud.google.com/python/docs/setup
.. _`venv`: https://docs.python.org/3/library/venv.html


Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^
Python >= 3.6

Deprecated Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7: Python 2.7 support will be removed sometime after January 1, 2020.

Unsupported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 3.5: the last released version which supported Python 3.5 was
``google-cloud-storage 1.32.0``, released 2020-10-16.

Python == 2.7: the last released version which supported Python 2.7 was
``google-cloud-storage 1.44.0``, released 2022-01-05.

Mac/Linux
^^^^^^^^^

.. code-block:: console

    python -m venv env
    source env/bin/activate
    pip install google-cloud-storage


Windows
^^^^^^^

.. code-block:: console

    py -m venv env
    .\env\Scripts\activate
    pip install google-cloud-storage


Example Usage
~~~~~~~~~~~~~

.. code:: python

    # Imports the Google Cloud client library
    from google.cloud import storage

    # Instantiates a client
    client = storage.Client()

    # Creates a new bucket and uploads an object
    new_bucket = client.create_bucket('new-bucket-id')
    new_blob = new_bucket.blob('remote/path/storage.txt')
    new_blob.upload_from_filename(filename='/local/path.txt')

    # Retrieve an existing bucket
    # https://console.cloud.google.com/storage/browser/[bucket-id]/
    bucket = client.get_bucket('bucket-id')
    # Then do other things...
    blob = bucket.get_blob('remote/path/to/file.txt')
    print(blob.download_as_bytes())
    blob.upload_from_string('New contents!')


What's Next
~~~~~~~~~~~

Now that you've set up your Python client for Cloud Storage,
you can get started running `Storage samples.`_

.. _Storage samples.: https://github.com/googleapis/python-storage/tree/main/samples
