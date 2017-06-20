.. toctree::
  :maxdepth: 2
  :hidden:

  core/index
  bigquery/usage
  bigtable/usage
  datastore/usage
  dns/usage
  language/usage
  pubsub/usage
  resource-manager/api
  runtimeconfig/usage
  spanner/usage
  speech/usage
  error-reporting/usage
  monitoring/usage
  logging/usage
  storage/client
  translate/usage
  vision/index

Google Cloud Client Library for Python
======================================

Getting started
---------------

The ``google-cloud`` library is ``pip`` install-able:

.. code-block:: console

    $ pip install google-cloud

Cloud Datastore
~~~~~~~~~~~~~~~

`Google Cloud Datastore`_ is a fully managed, schemaless database for storing non-relational data.

.. _Google Cloud Datastore: https://developers.google.com/datastore/

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

.. _Google Cloud Storage: https://developers.google.com/storage/

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
* `PyPI <https://pypi.python.org/pypi/google-cloud>`__
