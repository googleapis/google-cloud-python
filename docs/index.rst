.. toctree::
  :maxdepth: 1
  :hidden:

  Core Libraries <core/index>
  Asset Management <asset/index>
  AutoML <automl/index>
  BigQuery <bigquery/index>
  BigQuery Data-Transfer <bigquery_datatransfer/index>
  Bigtable <bigtable/index>
  Container <container/index>
  Dataproc <dataproc/index>
  Datastore <datastore/index>
  Data Loss Prevention <dlp/index>
  DNS <dns/usage>
  Firestore <firestore/index>
  IoT <iot/index>
  Key Management <kms/index>
  Language <language/index>
  PubSub <pubsub/index>
  OSLogin <oslogin/index>
  Redis <redis/index>
  Resource Manager <resource-manager/index>
  Runtime Configuration <runtimeconfig/usage>
  Security Scanner <websecurityscanner/index>
  Spanner <spanner/index>
  Speech <speech/index>
  Storage <storage/index>
  Tasks <tasks/index>
  Text-to-Speech <texttospeech/index>
  Translate <translate/index>
  Vision <vision/index>
  Video Intelligence <videointelligence/index>
  Stackdriver Error Reporting <error-reporting/usage>
  Stackdriver Logging <logging/index>
  Stackdriver Monitoring <monitoring/index>
  Stackdriver Trace <trace/index>
  Release History <releases>

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
