Google Cloud Python Client
==========================

    Python idiomatic client for `Google Cloud Platform`_ services.

.. _Google Cloud Platform: https://cloud.google.com/

|pypi| |build| |coverage|

-  `Homepage`_
-  `API Documentation`_

.. _Homepage: https://googlecloudplatform.github.io/gcloud-python/
.. _API Documentation: http://googlecloudplatform.github.io/gcloud-python/latest/

This client supports the following Google Cloud Platform services:

-  `Google Cloud Datastore`_
-  `Google Cloud Storage`_

.. _Google Cloud Datastore: #google-cloud-datastore
.. _Google Cloud Storage: #google-cloud-storage

If you need support for other Google APIs, check out the
`Google APIs Python Client library`_.

.. _Google APIs Python Client library: https://github.com/google/google-api-python-client

Quickstart
----------

::

    $ pip install gcloud

Example Applications
--------------------

-  `gcloud-python-expenses-demo`_ - A sample expenses demo using Cloud Datastore and Cloud Storage

.. _gcloud-python-expenses-demo: https://github.com/GoogleCloudPlatform/gcloud-python-expenses-demo

Google Cloud Datastore
----------------------

Google `Cloud Datastore`_ (`Datastore API docs`_) is a fully managed, schemaless
database for storing non-relational data. Cloud Datastore automatically scales
with your users and supports ACID transactions, high availability of reads and
writes, strong consistency for reads and ancestor queries, and eventual
consistency for all other queries.

.. _Cloud Datastore: https://cloud.google.com/datastore/docs
.. _Datastore API docs: https://cloud.google.com/datastore/docs/apis/v1beta2/

See the ``gcloud-python`` API `datastore documentation`_ to learn how to
interact with the Cloud Datastore using this Client Library.

.. _datastore documentation: https://googlecloudplatform.github.io/gcloud-python/latest/datastore-api.html

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

.. _storage documentation: https://googlecloudplatform.github.io/gcloud-python/latest/storage-api.html

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

Contributing
------------

Contributions to this library are always welcome and highly encouraged.

See `CONTRIBUTING`_ for more information on how to get started.

.. _CONTRIBUTING: https://github.com/GoogleCloudPlatform/gcloud-python/blob/master/CONTRIBUTING.rst

Python Versions
-------------------------

We support `Python 2.6`_ and `Python 2.7`_ and plan to support `Python 3.3`_ and
`Python 3.4`_. For more information, see `Supported Python Versions`_ in
``CONTRIBUTING``.

.. _Python 2.6: https://docs.python.org/2.6/
.. _Python 2.7: https://docs.python.org/2.7/
.. _Python 3.3: https://docs.python.org/3.3/
.. _Python 3.4: https://docs.python.org/3.4/
.. _Supported Python Versions: https://github.com/GoogleCloudPlatform/gcloud-python/blob/master/CONTRIBUTING.rst#supported-python-versions

Versioning
----------

This library follows `Semantic Versioning`_.

.. _Semantic Versioning: http://semver.org/

It is currently in major version zero (``0.y.z``), which means that anything
may change at any time and the public API should not be considered
stable.

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
