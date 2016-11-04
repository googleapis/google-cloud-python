Python Client for Google Cloud Datastore
========================================

    Python idiomatic client for `Google Cloud Datastore`_

.. _Google Cloud Datastore: https://cloud.google.com/datastore/docs

|pypi| |versions|

-  `Documentation`_

.. _Documentation: https://googlecloudplatform.github.io/google-cloud-python/stable/datastore-client.html

Quick Start
-----------

.. code-block:: console

    $ pip install --upgrade google-cloud-datastore

Authentication
--------------

With ``google-cloud-python`` we try to make authentication as painless as
possible. Check out the `Authentication section`_ in our documentation to
learn more. You may also find the `authentication document`_ shared by all
the ``google-cloud-*`` libraries to be helpful.

.. _Authentication section: http://google-cloud-python.readthedocs.io/en/latest/google-cloud-auth.html
.. _authentication document: https://github.com/GoogleCloudPlatform/gcloud-common/tree/master/authentication

Using the API
-------------

Google `Cloud Datastore`_ (`Datastore API docs`_) is a fully managed,
schemaless database for storing non-relational data. Cloud Datastore
automatically scales with your users and supports ACID transactions, high
availability of reads and writes, strong consistency for reads and ancestor
queries, and eventual consistency for all other queries.

.. _Cloud Datastore: https://cloud.google.com/datastore/docs
.. _Datastore API docs: https://cloud.google.com/datastore/docs/

See the ``google-cloud-python`` API `datastore documentation`_ to learn how to
interact with the Cloud Datastore using this Client Library.

.. _datastore documentation: https://googlecloudplatform.github.io/google-cloud-python/stable/datastore-client.html

See the `official Google Cloud Datastore documentation`_ for more details on
how to activate Cloud Datastore for your project.

.. _official Google Cloud Datastore documentation: https://cloud.google.com/datastore/docs/activate

.. code:: python

    from google.cloud import datastore
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
        print(result)

.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-datastore.svg
   :target: https://pypi.python.org/pypi/google-cloud-datastore
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-datastore.svg
   :target: https://pypi.python.org/pypi/google-cloud-datastore
