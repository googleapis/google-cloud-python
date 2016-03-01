Using the API
=============


Authentication and Configuration
--------------------------------

- For an overview of authentication in ``gcloud-python``,
  see :doc:`gcloud-auth`.

- In addition to any authentication configuration, you should also set the
  :envvar:`GCLOUD_PROJECT` environment variable for the project you'd like
  to interact with. If you are Google App Engine or Google Compute Engine
  this will be detected automatically.

- After configuring your environment, create a
  :class:`Client <gcloud.logging.client.Client>`

  .. doctest::

     >>> from gcloud import logging
     >>> client = logging.Client()

  or pass in ``credentials`` and ``project`` explicitly

  .. doctest::

     >>> from gcloud import logging
     >>> client = logging.Client(project='my-project', credentials=creds)


Writing log entries
-------------------

Write a simple text entry to a logger.

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> logger = client.logger('log_name')
   >>> logger.log_text("A simple entry")  # API call

Write a dictionary entry to a logger.

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> logger = client.logger('log_name')
   >>> logger.log_struct(
   ...     message="My second entry",
   ...     weather="partly cloudy")  # API call


Retrieving log entries
----------------------

Fetch entries for the default project.

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> entries, token = client.list_entries()  # API call
   >>> for entry in entries:
   ...    timestamp = entry.timestamp.isoformat()
   ...    print('%sZ: %s | %s' %
   ...          (timestamp, entry.text_payload, entry.struct_payload))
   2016-02-17T20:35:49.031864072Z: A simple entry | None
   2016-02-17T20:38:15.944418531Z: None | {'message': 'My second entry', 'weather': 'partly cloudy'}

Fetch entries across multiple projects.

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> entries, token = client.list_entries(
   ...     project_ids=['one-project', 'another-project'])  # API call

Filter entries retrieved using the `Advanced Logs Filters`_ syntax

.. _Advanced Logs Filters: https://cloud.google.com/logging/docs/view/advanced_filters

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> FILTER = "log:log_name AND textPayload:simple"
   >>> entries, token = client.list_entries(filter=FILTER)  # API call

Sort entries in descending timestamp order.

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> entries, token = client.list_entries(order_by=logging.DESCENDING)  # API call

Retrieve entities in batches of 10, iterating until done.

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> retrieved = []
   >>> token = None
   >>> while True:
   ...     entries, token = client.list_entries(page_size=10)  # API call
   ...     retrieved.extend(entries)
   ...     if token is None:
   ...         break


Delete all entries for a logger
-------------------------------

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> logger = client.logger('log_name')
   >>> logger.delete()  # API call


Manage log metrics
------------------

Metrics are counters of entries which match a given filter.  They can be
used within Cloud Monitoring to create charts and alerts.

Create a metric:

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> metric = client.metric(
   ...     "robots", "Robots all up in your server",
   ...     filter='log:apache-access AND textPayload:robot')
   >>> metric.exists()  # API call
   False
   >>> metric.create()  # API call
   >>> metric.exists()  # API call
   True

List all metrics for a project:

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> metrics, token = client.list_metrics()
   >>> len(metrics)
   1
   >>> metric = metrics[0]
   >>> metric.name
   "robots"

Refresh local information about a metric:

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> metric = client.metric("robots")
   >>> metric.reload()  # API call
   >>> metric.description
   "Robots all up in your server"
   >>> metric.filter
   "log:apache-access AND textPayload:robot"

Update a metric:

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> metric = client.metric("robots")
   >>> metric.exists()  # API call
   True
   >>> metric.reload()  # API call
   >>> metric.description = "Danger, Will Robinson!"
   >>> metric.update()  # API call

Delete a metric:

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> metric = client.metric("robots")
   >>> metric.exists()  # API call
   True
   >>> metric.delete()  # API call
   >>> metric.exists()  # API call
   False


Export log entries using sinks
------------------------------

Sinks allow exporting entries which match a given filter to Cloud Storage
buckets, BigQuery datasets, or Cloud Pub/Sub topics.

Create a Cloud Storage sink:

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> sink = client.sink(
   ...     "robots-storage",
   ...     filter='log:apache-access AND textPayload:robot')
   >>> sink.storage_bucket = "my-bucket-name"
   >>> sink.exists()  # API call
   False
   >>> sink.create()  # API call
   >>> sink.exists()  # API call
   True

Create a BigQuery sink:

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> sink = client.sink(
   ...     "robots-bq",
   ...     filter='log:apache-access AND textPayload:robot')
   >>> sink.bigquery_dataset = "projects/my-project/datasets/my-dataset"
   >>> sink.exists()  # API call
   False
   >>> sink.create()  # API call
   >>> sink.exists()  # API call
   True

Create a Cloud Pub/Sub sink:

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> sink = client.sink(
   ...     "robots-pubsub",
   ...     filter='log:apache-access AND textPayload:robot')
   >>> sink.pubsub_topic = 'projects/my-project/topics/my-topic'
   >>> sink.exists()  # API call
   False
   >>> sink.create()  # API call
   >>> sink.exists()  # API call
   True

List all sinks for a project:

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> sinks, token = client.list_sinks()
   >>> for sink in sinks:
   ...     print('%s: %s' % (sink.name, sink.destination))
   robots-storage: storage.googleapis.com/my-bucket-name
   robots-bq: bigquery.googleapis.com/projects/my-project/datasets/my-dataset
   robots-pubsub: pubsub.googleapis.com/projects/my-project/topics/my-topic

Refresh local information about a sink:

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> sink = client.sink('robots-storage')
   >>> sink.filter is None
   True
   >>> sink.reload()  # API call
   >>> sink.filter
   'log:apache-access AND textPayload:robot'
   >>> sink.destination
   'storage.googleapis.com/my-bucket-name'

Update a sink:

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> sink = client.sink("robots")
   >>> sink.reload()  # API call
   >>> sink.filter = "log:apache-access"
   >>> sink.update()  # API call

Delete a sink:

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> sink = client.sink(
   ...     "robots",
   ...     filter='log:apache-access AND textPayload:robot')
   >>> sink.exists()  # API call
   True
   >>> sink.delete()  # API call
   >>> sink.exists()  # API call
   False
