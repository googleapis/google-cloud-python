Google Cloud Python Client
==========================

    Python idiomatic client for `Google Cloud Platform`_ services.

.. _Google Cloud Platform: https://cloud.google.com/

|pypi| |build| |coverage| |versions|

-  `Homepage`_
-  `API Documentation`_

.. _Homepage: https://googlecloudplatform.github.io/gcloud-python/
.. _API Documentation: http://googlecloudplatform.github.io/gcloud-python/stable/

This client supports the following Google Cloud Platform services:

-  `Google Cloud Datastore`_
-  `Google Cloud Storage`_
-  `Google Cloud Pub/Sub`_
-  `Google BigQuery`_
-  `Google Cloud Resource Manager`_

.. _Google Cloud Datastore: https://github.com/GoogleCloudPlatform/gcloud-python#google-cloud-datastore
.. _Google Cloud Storage: https://github.com/GoogleCloudPlatform/gcloud-python#google-cloud-storage
.. _Google Cloud Pub/Sub: https://github.com/GoogleCloudPlatform/gcloud-python#google-cloud-pubsub
.. _Google BigQuery: https://github.com/GoogleCloudPlatform/gcloud-python#google-bigquery
.. _Google Cloud Resource Manager: https://github.com/GoogleCloudPlatform/gcloud-python#google-cloud-resource-manager

If you need support for other Google APIs, check out the
`Google APIs Python Client library`_.

.. _Google APIs Python Client library: https://github.com/google/google-api-python-client

Quick Start
-----------

::

    $ pip install --upgrade gcloud

Example Applications
--------------------

-  `getting-started-python`_ - A sample and `tutorial`_ that demonstrates how to build a complete web application using Cloud Datastore, Cloud Storage, and Cloud Pub/Sub and deploy it to Google App Engine or Google Compute Engine.
-  `gcloud-python-expenses-demo`_ - A sample expenses demo using Cloud Datastore and Cloud Storage

.. _getting-started-python: https://github.com/GoogleCloudPlatform/getting-started-python
.. _tutorial: https://cloud.google.com/python
.. _gcloud-python-expenses-demo: https://github.com/GoogleCloudPlatform/gcloud-python-expenses-demo

Authentication
--------------

With ``gcloud-python`` we try to make authentication as painless as possible.
Check out the `Authentication section`_ in our documentation to learn more.
You may also find the `authentication document`_ shared by all the ``gcloud-*``
libraries to be helpful.

.. _Authentication section: http://gcloud-python.readthedocs.org/en/latest/gcloud-auth.html
.. _authentication document: https://github.com/GoogleCloudPlatform/gcloud-common/tree/master/authentication

Google Cloud Datastore
----------------------

Google `Cloud Datastore`_ (`Datastore API docs`_) is a fully managed, schemaless
database for storing non-relational data. Cloud Datastore automatically scales
with your users and supports ACID transactions, high availability of reads and
writes, strong consistency for reads and ancestor queries, and eventual
consistency for all other queries.

.. _Cloud Datastore: https://cloud.google.com/datastore/docs
.. _Datastore API docs: https://cloud.google.com/datastore/docs/apis/v1beta3/

See the ``gcloud-python`` API `datastore documentation`_ to learn how to
interact with the Cloud Datastore using this Client Library.

.. _datastore documentation: https://googlecloudplatform.github.io/gcloud-python/stable/datastore-client.html

See the `official Google Cloud Datastore documentation`_ for more details on how
to activate Cloud Datastore for your project.

.. _official Google Cloud Datastore documentation: https://cloud.google.com/datastore/docs/activate

.. code:: python

    from gcloud import datastore
    # Create, populate and persist an entity
    entity = datastore.Entity(key=datastore.Key('EntityKind'))
    entity.update({
        'foo': u'bar',
        'baz': 1337,
        'qux': False,
    })
    # Then query for entities
    query = datastore.Query(kind='EntityKind')
    for result in query.fetch():
        print result

Google Cloud Storage
--------------------

Google `Cloud Storage`_ (`Storage API docs`_) allows you to store data on Google
infrastructure with very high reliability, performance and availability, and can
be used to distribute large data objects to users via direct download.

.. _Cloud Storage: https://cloud.google.com/storage/docs
.. _Storage API docs: https://cloud.google.com/storage/docs/json_api/v1

See the ``gcloud-python`` API `storage documentation`_ to learn how to connect
to Cloud Storage using this Client Library.

.. _storage documentation: https://googlecloudplatform.github.io/gcloud-python/stable/storage-client.html

You need to create a Google Cloud Storage bucket to use this client library.
Follow along with the `official Google Cloud Storage documentation`_ to learn
how to create a bucket.

.. _official Google Cloud Storage documentation: https://cloud.google.com/storage/docs/cloud-console#_creatingbuckets

.. code:: python

    from gcloud import storage
    client = storage.Client()
    bucket = client.get_bucket('bucket-id-here')
    # Then do other things...
    blob = bucket.get_blob('/remote/path/to/file.txt')
    print blob.download_as_string()
    blob.upload_from_string('New contents!')
    blob2 = bucket.blob('/remote/path/storage.txt')
    blob2.upload_from_filename(filename='/local/path.txt')

Google Cloud Pub/Sub
--------------------

Google `Cloud Pub/Sub`_ (`Pub/Sub API docs`_) is designed to provide reliable,
many-to-many, asynchronous messaging between applications. Publisher
applications can send messages to a ``topic`` and other applications can
subscribe to that topic to receive the messages. By decoupling senders and
receivers, Google Cloud Pub/Sub allows developers to communicate between
independently written applications.

.. _Cloud Pub/Sub: https://cloud.google.com/pubsub/docs
.. _Pub/Sub API docs: https://cloud.google.com/pubsub/reference/rest/

See the ``gcloud-python`` API `Pub/Sub documentation`_ to learn how to connect
to Cloud Pub/Sub using this Client Library.

.. _Pub/Sub documentation: https://googlecloudplatform.github.io/gcloud-python/stable/pubsub-usage.html

To get started with this API, you'll need to create

.. code:: python

    from gcloud import pubsub

    client = pubsub.Client()
    topic = client.topic('topic_name')
    topic.create()

    topic.publish('this is the message_payload',
                  attr1='value1', attr2='value2')

Google BigQuery
---------------

Querying massive datasets can be time consuming and expensive without the
right hardware and infrastructure. Google `BigQuery`_ (`BigQuery API docs`_)
solves this problem by enabling super-fast, SQL-like queries against
append-only tables, using the processing power of Google's infrastructure.

.. _BigQuery: https://cloud.google.com/bigquery/what-is-bigquery
.. _BigQuery API docs: https://cloud.google.com/bigquery/docs/reference/v2/

This package is still being implemented, but it is almost complete!

See the ``gcloud-python`` API `BigQuery documentation`_ to learn how to connect
to BigQuery using this Client Library.

.. _BigQuery documentation: https://googlecloudplatform.github.io/gcloud-python/stable/bigquery-usage.html

Google Cloud Resource Manager
-----------------------------

The Cloud `Resource Manager`_ API (`Resource Manager API docs`_) provides
methods that you can use to programmatically manage your projects in the
Google Cloud Platform.

.. _Resource Manager: https://cloud.google.com/resource-manager/
.. _Resource Manager API docs: https://cloud.google.com/resource-manager/reference/rest/

See the ``gcloud-python`` API `Resource Manager documentation`_ to learn how to
manage projects using this Client Library.

.. _Resource Manager documentation: https://googlecloudplatform.github.io/gcloud-python/stable/resource-manager-api.html

Contributing
------------

Contributions to this library are always welcome and highly encouraged.

See `CONTRIBUTING`_ for more information on how to get started.

.. _CONTRIBUTING: https://github.com/GoogleCloudPlatform/gcloud-python/blob/master/CONTRIBUTING.rst

License
-------

Apache 2.0 - See `LICENSE`_ for more information.

.. _LICENSE: https://github.com/GoogleCloudPlatform/gcloud-python/blob/master/LICENSE

.. |build| image:: https://travis-ci.org/GoogleCloudPlatform/gcloud-python.svg?branch=master
   :target: https://travis-ci.org/GoogleCloudPlatform/gcloud-python
.. |coverage| image:: https://coveralls.io/repos/GoogleCloudPlatform/gcloud-python/badge.png?branch=master
   :target: https://coveralls.io/r/GoogleCloudPlatform/gcloud-python?branch=master
.. |pypi| image:: https://img.shields.io/pypi/v/gcloud.svg
   :target: https://pypi.python.org/pypi/gcloud
.. |versions| image:: https://img.shields.io/pypi/pyversions/gcloud.svg
   :target: https://pypi.python.org/pypi/gcloud
