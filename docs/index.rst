.. toctree::
  :maxdepth: 2
  :hidden:

  releases
  core/index
  asset/index
  automl/index
  bigquery/usage
  bigquery_datatransfer/index
  bigtable/usage
  container/index
  dataproc/index
  datastore/usage
  dlp/index
  dns/usage
  firestore/index
  iot/index
  kms/index
  language/usage
  pubsub/index
  oslogin/index
  resource-manager/api
  runtimeconfig/usage
  spanner/usage
  speech/index
  error-reporting/usage
  monitoring/index
  logging/usage
  redis/index
  storage/client
  tasks/index
  texttospeech/index
  translate/usage
  vision/index
  videointelligence/index
  websecurityscanner/index

Google Cloud Client Library for Python
======================================

Getting started
---------------

For more information on setting up your Python development environment,
such as installing ``pip`` and ``virtualenv`` on your system, please refer
to `Python Development Environment Setup Guide`_ for Google Cloud Platform.

.. _Python Development Environment Setup Guide: https://cloud.google.com/python/setup

Cloud Datastore
~~~~~~~~~~~~~~~

`Google Cloud Datastore`_ is a fully managed, schemaless database for storing
non-relational data.

.. _Google Cloud Datastore: https://cloud.google.com/datastore/

Install the ``google-cloud-datastore`` library using ``pip``:

.. code-block:: console

    $ pip install google-cloud-datastore

Example
^^^^^^^

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

Install the ``google-cloud-storage`` library using ``pip``:

.. code-block:: console

    $ pip install google-cloud-storage

Example
^^^^^^^

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
