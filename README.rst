Google Cloud Python Client
==========================

    Python idiomatic client for `Google Cloud Platform`_ services.

.. _Google Cloud Platform: https://cloud.google.com/

|pypi| |build| |appveyor| |coverage| |versions|

-  `Homepage`_
-  `API Documentation`_

.. _Homepage: https://googlecloudplatform.github.io/google-cloud-python/
.. _API Documentation: http://googlecloudplatform.github.io/google-cloud-python/

This client supports the following Google Cloud Platform services:

-  `Google Cloud Datastore`_
-  `Google Cloud Storage`_
-  `Google Cloud Pub/Sub`_
-  `Google BigQuery`_
-  `Google Cloud Resource Manager`_
-  `Google Stackdriver Logging`_
-  `Google Stackdriver Monitoring`_

.. _Google Cloud Datastore: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/datastore
.. _Google Cloud Storage: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/storage
.. _Google Cloud Pub/Sub: https://github.com/GoogleCloudPlatform/google-cloud-python#google-cloud-pubsub
.. _Google BigQuery: https://github.com/GoogleCloudPlatform/google-cloud-python#google-bigquery
.. _Google Cloud Resource Manager: https://github.com/GoogleCloudPlatform/google-cloud-python#google-cloud-resource-manager
.. _Google Stackdriver Logging: https://github.com/GoogleCloudPlatform/google-cloud-python#google-stackdriver-logging
.. _Google Stackdriver Monitoring: https://github.com/GoogleCloudPlatform/google-cloud-python#google-stackdriver-monitoring

If you need support for other Google APIs, check out the
`Google APIs Python Client library`_.

.. _Google APIs Python Client library: https://github.com/google/google-api-python-client

Quick Start
-----------

::

    $ pip install --upgrade google-cloud

Example Applications
--------------------

-  `getting-started-python`_ - A sample and `tutorial`_ that demonstrates how to build a complete web application using Cloud Datastore, Cloud Storage, and Cloud Pub/Sub and deploy it to Google App Engine or Google Compute Engine.
-  `google-cloud-python-expenses-demo`_ - A sample expenses demo using Cloud Datastore and Cloud Storage

.. _getting-started-python: https://github.com/GoogleCloudPlatform/getting-started-python
.. _tutorial: https://cloud.google.com/python
.. _google-cloud-python-expenses-demo: https://github.com/GoogleCloudPlatform/google-cloud-python-expenses-demo

Authentication
--------------

With ``google-cloud-python`` we try to make authentication as painless as possible.
Check out the `Authentication section`_ in our documentation to learn more.
You may also find the `authentication document`_ shared by all the
``google-cloud-*`` libraries to be helpful.

.. _Authentication section: http://google-cloud-python.readthedocs.io/en/latest/google-cloud-auth.html
.. _authentication document: https://github.com/GoogleCloudPlatform/gcloud-common/tree/master/authentication

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

See the ``google-cloud-python`` API `Pub/Sub documentation`_ to learn how to connect
to Cloud Pub/Sub using this Client Library.

.. _Pub/Sub documentation: https://googlecloudplatform.github.io/google-cloud-python/stable/pubsub-usage.html

To get started with this API, you'll need to create

.. code:: python

    from google.cloud import pubsub

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

Load data from CSV
~~~~~~~~~~~~~~~~~~

.. code:: python

    import csv

    from google.cloud import bigquery
    from google.cloud.bigquery import SchemaField

    client = bigquery.Client()

    dataset = client.dataset('dataset_name')
    dataset.create()  # API request

    SCHEMA = [
        SchemaField('full_name', 'STRING', mode='required'),
        SchemaField('age', 'INTEGER', mode='required'),
    ]
    table = dataset.table('table_name', SCHEMA)
    table.create()

    with open('csv_file', 'rb') as readable:
        table.upload_from_file(
            readable, source_format='CSV', skip_leading_rows=1)

Perform a synchronous query
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    # Perform a synchronous query.
    QUERY = (
        'SELECT name FROM [bigquery-public-data:usa_names.usa_1910_2013] '
        'WHERE state = "TX"')
    query = client.run_sync_query('%s LIMIT 100' % QUERY)
    query.timeout_ms = TIMEOUT_MS
    query.run()

    for row in query.rows:
        print row


See the ``google-cloud-python`` API `BigQuery documentation`_ to learn how to connect
to BigQuery using this Client Library.

.. _BigQuery documentation: https://googlecloudplatform.github.io/google-cloud-python/stable/bigquery-usage.html

Google Cloud Resource Manager
-----------------------------

The Cloud `Resource Manager`_ API (`Resource Manager API docs`_) provides
methods that you can use to programmatically manage your projects in the
Google Cloud Platform.

.. _Resource Manager: https://cloud.google.com/resource-manager/
.. _Resource Manager API docs: https://cloud.google.com/resource-manager/reference/rest/

See the ``google-cloud-python`` API `Resource Manager documentation`_ to learn how to
manage projects using this Client Library.

.. _Resource Manager documentation: https://googlecloudplatform.github.io/google-cloud-python/stable/resource-manager-api.html

Google Stackdriver Logging
--------------------------

`Stackdriver Logging`_ API (`Logging API docs`_) allows you to store, search,
analyze, monitor, and alert on log data and events from Google Cloud Platform.

.. _Stackdriver Logging: https://cloud.google.com/logging/
.. _Logging API docs: https://cloud.google.com/logging/docs/

.. code:: python

    from google.cloud import logging
    client = logging.Client()
    logger = client.logger('log_name')
    logger.log_text("A simple entry")  # API call

Example of fetching entries:

.. code:: python

    entries, token = logger.list_entries()
    for entry in entries:
        print entry.payload

See the ``google-cloud-python`` API `logging documentation`_ to learn how to connect
to Stackdriver Logging using this Client Library.

.. _logging documentation: https://googlecloudplatform.github.io/google-cloud-python/stable/logging-usage.html

Google Stackdriver Monitoring
-----------------------------

`Stackdriver Monitoring`_ (`Monitoring API docs`_) collects metrics,
events, and metadata from Google Cloud Platform, Amazon Web Services (AWS),
hosted uptime probes, application instrumentation, and a variety of common
application components including Cassandra, Nginx, Apache Web Server,
Elasticsearch and many others. Stackdriver ingests that data and generates
insights via dashboards, charts, and alerts.

This package currently supports all Monitoring API operations other than
writing custom metrics.

.. _Stackdriver Monitoring: https://cloud.google.com/monitoring/
.. _Monitoring API docs: https://cloud.google.com/monitoring/api/ref_v3/rest/

List available metric types:

.. code:: python

    from google.cloud import monitoring
    client = monitoring.Client()
    for descriptor in client.list_metric_descriptors():
        print(descriptor.type)

Display CPU utilization across your GCE instances during the last five minutes:

.. code:: python

    metric = 'compute.googleapis.com/instance/cpu/utilization'
    query = client.query(metric, minutes=5)
    print(query.as_dataframe())

See the ``google-cloud-python`` API `monitoring documentation`_ to learn how to connect
to Stackdriver Monitoring using this Client Library.

.. _monitoring documentation: https://googlecloudplatform.github.io/google-cloud-python/stable/monitoring-usage.html

Contributing
------------

Contributions to this library are always welcome and highly encouraged.

See `CONTRIBUTING`_ for more information on how to get started.

.. _CONTRIBUTING: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/CONTRIBUTING.rst

License
-------

Apache 2.0 - See `LICENSE`_ for more information.

.. _LICENSE: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/LICENSE

.. |build| image:: https://travis-ci.org/GoogleCloudPlatform/google-cloud-python.svg?branch=master
   :target: https://travis-ci.org/GoogleCloudPlatform/google-cloud-python
.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/googlecloudplatform/google-cloud-python?branch=master&svg=true
   :target: https://ci.appveyor.com/project/GoogleCloudPlatform/google-cloud-python
.. |coverage| image:: https://coveralls.io/repos/GoogleCloudPlatform/google-cloud-python/badge.png?branch=master
   :target: https://coveralls.io/r/GoogleCloudPlatform/google-cloud-python?branch=master
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud.svg
   :target: https://pypi.python.org/pypi/google-cloud
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud.svg
   :target: https://pypi.python.org/pypi/google-cloud
