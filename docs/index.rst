.. toctree::
  :maxdepth: 2
  :hidden:

  core/index
  bigquery/usage
  bigtable/usage
  datastore/usage
  dns/usage
  firestore/index
  language/usage
  pubsub/index
  resource-manager/api
  runtimeconfig/usage
  spanner/usage
  speech/index
  error-reporting/usage
  monitoring/usage
  logging/usage
  storage/client
  translate/usage
  vision/index
  videointelligence/index

Google Cloud Client Library for Python
======================================

Getting started
---------------

The ``google-cloud`` library is ``pip`` install-able:

.. code-block:: console

    $ pip install google-cloud

Fore more information on setting up your Python development environment, such as installing ``pip`` on your system, please refer to `Python Development Environment Setup Guide`_ for Google Cloud Platform.

.. _Python Development Environment Setup Guide: https://cloud.google.com/python/setup

Cloud Datastore
~~~~~~~~~~~~~~~

`Google Cloud Datastore`_ is a fully managed, schemaless database for storing non-relational data.

.. _Google Cloud Datastore: https://cloud.google.com/datastore/

.. code-block:: python

  from google.cloud import datastore

  client = datastore.Client()
  key = client.key('Person')

  entity = datastore.Entity(key=key)
  entity['name'] = 'Your name'
  entity['age'] = 25
  client.put(entity)

Cloud Storage
~~~~~~~~~~~~~

`Google Cloud Storage`_ allows you to store data on Google infrastructure.

.. _Google Cloud Storage: https://cloud.google.com/storage/

.. code-block:: python

  from google.cloud import storage

  client = storage.Client()
  bucket = client.get_bucket('<your-bucket-name>')
  blob = bucket.blob('my-test-file.txt')
  blob.upload_from_string('this is test content!')

Resources
~~~~~~~~~

* `GitHub <https://github.com/GoogleCloudPlatform/google-cloud-python/>`__
* `Issues <https://github.com/GoogleCloudPlatform/google-cloud-python/issues>`__
* `Stack Overflow <http://stackoverflow.com/questions/tagged/google-cloud-python>`__
* `PyPI <https://pypi.org/project/google-cloud/>`__
