.. toctree::
  :maxdepth: 0
  :hidden:
  :caption: gcloud

  gcloud-api
  gcloud-config
  gcloud-auth

.. toctree::
  :maxdepth: 0
  :hidden:
  :caption: Datastore

  Client <datastore-client>
  datastore-entities
  datastore-keys
  datastore-queries
  datastore-transactions
  datastore-batches
  datastore-helpers

.. toctree::
  :maxdepth: 0
  :hidden:
  :caption: Storage

  Client <storage-client>
  storage-blobs
  storage-buckets
  storage-acl
  storage-batch

.. toctree::
  :maxdepth: 0
  :hidden:
  :caption: Pub/Sub

  pubsub-usage
  Client <pubsub-client>
  pubsub-topic
  pubsub-subscription
  pubsub-message
  pubsub-iam

.. toctree::
  :maxdepth: 0
  :hidden:
  :caption: BigQuery

  bigquery-usage
  Client <bigquery-client>
  bigquery-dataset
  bigquery-job
  bigquery-table
  bigquery-query
  bigquery-schema

.. toctree::
  :maxdepth: 0
  :hidden:
  :caption: Cloud Bigtable

  bigtable-usage
  bigtable-client-intro
  bigtable-instance-api
  bigtable-table-api
  bigtable-data-api
  Client <bigtable-client>
  bigtable-instance
  bigtable-cluster
  bigtable-table
  bigtable-column-family
  bigtable-row
  bigtable-row-filters
  bigtable-row-data

.. toctree::
  :maxdepth: 0
  :hidden:
  :caption: Resource Manager

  Overview <resource-manager-api>
  resource-manager-client
  resource-manager-project

.. toctree::
  :maxdepth: 0
  :hidden:
  :caption: DNS

  dns-usage
  Client <dns-client>
  dns-zone
  dns-resource-record-set
  dns-changes

.. toctree::
  :maxdepth: 0
  :hidden:
  :caption: Stackdriver Logging

  logging-usage
  Client <logging-client>
  logging-logger
  logging-entries
  logging-metric
  logging-sink
  logging-handlers
  logging-transports-sync
  logging-transports-thread
  logging-transports-base

.. toctree::
  :maxdepth: 0
  :hidden:
  :caption: Stackdriver Error Reporting

  error-reporting-usage
  Client <error-reporting-client>

.. toctree::
  :maxdepth: 0
  :hidden:
  :caption: Stackdriver Monitoring

  monitoring-usage
  Client <monitoring-client>
  monitoring-metric
  monitoring-resource
  monitoring-group
  monitoring-query
  monitoring-timeseries
  monitoring-label

.. toctree::
  :maxdepth: 0
  :hidden:
  :caption: Translate

  translate-usage
  Client <translate-client>

.. toctree::
  :maxdepth: 0
  :hidden:
  :caption: External Links

  GitHub <https://github.com/GoogleCloudPlatform/gcloud-python/>
  Issues <https://github.com/GoogleCloudPlatform/gcloud-python/issues>
  Stack Overflow <http://stackoverflow.com/questions/tagged/gcloud-python>
  PyPI <https://pypi.python.org/pypi/gcloud>

Getting started
---------------

The ``gcloud`` library is ``pip`` install-able:

.. code-block:: console

    $ pip install gcloud

If you want to install ``gcloud-python`` from source,
you can clone the repository from GitHub:

.. code-block:: console

    $ git clone git://github.com/GoogleCloudPlatform/gcloud-python.git
    $ cd gcloud-python
    $ python setup.py install

----

Cloud Datastore
~~~~~~~~~~~~~~~

`Google Cloud Datastore`_ is a fully managed, schemaless database for storing non-relational data.

.. _Google Cloud Datastore: https://developers.google.com/datastore/

.. code-block:: python

  from gcloud import datastore

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

  from gcloud import storage

  client = storage.Client()
  bucket = client.get_bucket('<your-bucket-name>')
  blob = bucket.blob('my-test-file.txt')
  blob.upload_from_string('this is test content!')
