.. toctree::
  :maxdepth: 0
  :hidden:
  :caption: gcloud

  gcloud-api
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

.. toctree::
  :maxdepth: 0
  :hidden:
  :caption: Storage

  Client <storage-client>
  storage-blobs
  storage-buckets
  storage-acl

.. toctree::
  :maxdepth: 0
  :hidden:
  :caption: Pub/Sub

  pubsub-usage
  Client <pubsub-client>
  pubsub-topic
  pubsub-subscription
  pubsub-message

.. toctree::
  :maxdepth: 0
  :hidden:
  :caption: BigQuery

  bigquery-usage
  Client <bigquery-client>
  bigquery-dataset
  bigquery-job
  bigquery-table

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
  dns-resource_record_set
  dns-changes

.. toctree::
  :maxdepth: 0
  :hidden:
  :caption: Cloud Search

  search-usage
  Client <search-client>
  search-index
  search-document

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

If you have trouble installing
``pycrypto`` or ``pyopenssl``
(and you're on Ubuntu),
you can try install the precompiled packages:

.. code-block:: console

    $ sudo apt-get install python-crypto python-openssl

If you want to install everything with ``pip``,
try installing the ``dev`` packages beforehand:

.. code-block:: console

    $ sudo apt-get install python-dev libssl-dev

If you want to install `gcloud-python` from source,
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
