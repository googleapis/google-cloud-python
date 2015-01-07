.. toctree::
  :maxdepth: 0
  :hidden:

  datastore-api
  datastore-entities
  datastore-keys
  datastore-transactions
  datastore-queries
  storage-api
  storage-buckets
  storage-keys
  storage-acl


Getting started
---------------

.. include:: _components/getting-started.rst

Cloud Datastore
~~~~~~~~~~~~~~~

`Google Cloud Datastore`_ is a fully managed, schemaless database for storing non-relational data.

.. _Google Cloud Datastore: https://developers.google.com/datastore/

.. code-block:: python

  from gcloud import datastore
  dataset = datastore.get_dataset('<dataset-id>')
  entity = dataset.entity('Person')
  entity['name'] = 'Your name'
  entity['age'] = 25
  entity.save()

Cloud Storage
~~~~~~~~~~~~~

`Google Cloud Storage`_ allows you to store data on Google infrastructure.

.. _Google Cloud Storage: https://developers.google.com/storage/

.. code-block:: python

  from gcloud import storage
  bucket = storage.get_bucket('<your-bucket-name>', '<your-project-id>')
  key = bucket.new_key('my-test-file.txt')
  key = key.upload_contents_from_string('this is test content!')
