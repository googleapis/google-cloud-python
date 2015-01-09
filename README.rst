Google Cloud Python Client
==========================

Python idiomatic client for Google Cloud Platform services.

|build| |coverage| |pypi|
-------------------------

-  `Homepage`_

.. _Homepage: https://googlecloudplatform.github.io/gcloud-python/

This client supports the following Google Cloud Platform services:

-  `Google Cloud Datastore`_
-  `Google Cloud Storage`_

.. _Google Cloud Datastore: https://cloud.google.com/products/cloud-datastore/
.. _Google Cloud Storage: https://cloud.google.com/products/cloud-storage/

If you need support for other Google APIs, check out the
`Google APIs Python Client library`_.

.. _Google APIs Python Client library: https://github.com/google/google-api-python-client

Versioning
----------

This library follows `Semantic Versioning`_.

.. _Semantic Versioning: http://semver.org/

It is currently in major version zero (``0.y.z``), which means that anything
may change at any time and the public API should not be considered
stable.

Quickstart
----------

::

    $ pip install gcloud

Google Cloud Datastore
----------------------

Google `Cloud Datastore`_ is a fully managed, schemaless database for
storing non-relational data. Cloud Datastore automatically scales with
your users and supports ACID transactions, high availability of reads and
writes, strong consistency for reads and ancestor queries, and eventual
consistency for all other queries.

.. _Cloud Datastore: https://developers.google.com/datastore/

See the `Google Cloud Datastore docs`_ for more details on how to activate
Cloud Datastore for your project.

.. _Google Cloud Datastore docs: https://developers.google.com/datastore/docs/activate

See the ``gcloud-python`` API `datastore documentation`_ to learn how to interact
with the Cloud Datastore using this Client Library.

.. _datastore documentation: https://googlecloudplatform.github.io/gcloud-python/datastore-api.html

.. code:: python

    from gcloud import datastore
    datastore.set_defaults()
    # Then do other things...
    query = datastore.Query(kind='EntityKind')
    entity = datastore.Entity(key=datastore.Key('EntityKind'))

Google Cloud Storage
--------------------

Google `Cloud Storage`_ allows you to store data on Google infrastructure with
very high reliability, performance and availability, and can be used to
distribute large data objects to users via direct download.

.. _Cloud Storage: https://developers.google.com/storage/

You need to create a Google Cloud Storage bucket to use this client
library. Follow the steps on the `Google Cloud Storage docs`_
to learn how to create a bucket.

.. _Google Cloud Storage docs: https://developers.google.com/storage/docs/cloud-console#_creatingbuckets

See the ``gcloud-python`` API `storage documentation`_ to learn how to connect
to Cloud Storage using this Client Library.

.. _storage documentation: https://googlecloudplatform.github.io/gcloud-python/storage-api.html

.. code:: python

    import gcloud.storage
    bucket = gcloud.storage.get_bucket('bucket-id-here', 'project-id')
    # Then do other things...
    key = bucket.get_key('/remote/path/to/file.txt')
    print key.get_contents_as_string()
    key.set_contents_from_string('New contents!')
    bucket.upload_file('/remote/path/storage.txt', '/local/path.txt')

Contributing
------------

Contributions to this library are always welcome and highly encouraged.

See `CONTRIBUTING`_ for more information on how to get started.

.. _CONTRIBUTING: https://github.com/GoogleCloudPlatform/gcloud-python/blob/master/CONTRIBUTING.rst

Supported Python Versions
-------------------------

We support:

-  `Python 2.6`_
-  `Python 2.7`_

We plan to support:

-  `Python 3.3`_
-  `Python 3.4`_

.. _Python 2.6: https://docs.python.org/2.6/
.. _Python 2.7: https://docs.python.org/2.7/
.. _Python 3.3: https://docs.python.org/3.3/
.. _Python 3.4: https://docs.python.org/3.4/

Supported versions can be found in our ``tox.ini`` `config`_.

.. _config: https://github.com/GoogleCloudPlatform/gcloud-python/blob/master/tox.ini

We explicitly decided not to support `Python 2.5`_ due to `decreased usage`_
and lack of continuous integration `support`_.

.. _Python 2.5: https://docs.python.org/2.5/
.. _decreased usage: https://caremad.io/2013/10/a-look-at-pypi-downloads/
.. _support: http://blog.travis-ci.com/2013-11-18-upcoming-build-environment-updates/

We also explicitly decided to support Python 3 beginning with version
3.3. Reasons for this include:

-  Encouraging use of newest versions of Python 3
-  Taking the lead of prominent open-source `projects`_
-  `Unicode literal support`_ which allows for a cleaner codebase that
   works in both Python 2 and Python 3

.. _projects: http://flask.pocoo.org/docs/0.10/python3/
.. _Unicode literal support: https://www.python.org/dev/peps/pep-0414/

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
