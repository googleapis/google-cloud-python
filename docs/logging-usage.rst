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

- The library now enables the ``gRPC`` transport for the logging API by
  default, assuming that the required dependencies are installed and
  importable.  To *disable* this transport, set the
  :envvar:`GCLOUD_DISABLE_GAX` environment variable to a non-empty string,
  e.g.:  ``$ export GCLOUD_DISABLE_GAX=1``.

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
   ...    print('%sZ: %s' %
   ...          (timestamp, entry.payload))
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

Retrieve entries in batches of 10, iterating until done.

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> retrieved = []
   >>> token = None
   >>> while True:
   ...     entries, token = client.list_entries(page_size=10, page_token=token)  # API call
   ...     retrieved.extend(entries)
   ...     if token is None:
   ...         break

Retrieve entries for a single logger, sorting in descending timestamp order:

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> logger = client.logger('log_name')
   >>> entries, token = logger.list_entries(order_by=logging.DESCENDING)  # API call

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
used within Stackdriver Monitoring to create charts and alerts.

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

Export to Cloud Storage
~~~~~~~~~~~~~~~~~~~~~~~

Make sure that the storage bucket you want to export logs too has
``cloud-logs@google.com`` as the owner. See `Set permission for writing exported logs`_.

Add ``cloud-logs@google.com`` as the owner of ``my-bucket-name``:

.. doctest::

    >>> from gcloud import storage
    >>> client = storage.Client()
    >>> bucket = client.get_bucket('my-bucket-name')
    >>> bucket.acl.reload()
    >>> logs_group = bucket.acl.group('cloud-logs@google.com')
    >>> logs_group.grant_owner()
    >>> bucket.acl.add_entity(logs_group)
    >>> bucket.acl.save()

.. _Set permission for writing exported logs: https://cloud.google.com/logging/docs/export/configure_export#setting_product_name_short_permissions_for_writing_exported_logs

Export to BigQuery
~~~~~~~~~~~~~~~~~~

To export logs to BigQuery you must log into the Cloud Platform Console
and add ``cloud-logs@google.com`` to a dataset.

See: `Setting permissions for BigQuery`_

.. doctest::

    >>> from gcloud import bigquery
    >>> from gcloud.bigquery.dataset import AccessGrant
    >>> bigquery_client = bigquery.Client()
    >>> dataset = bigquery_client.dataset('my-dataset-name')
    >>> dataset.create()
    >>> dataset.reload()
    >>> grants = dataset.access_grants
    >>> grants.append(AccessGrant(
    ...     'WRITER', 'groupByEmail', 'cloud-logs@google.com')))
    >>> dataset.access_grants = grants
    >>> dataset.update()

.. _Setting permissions for BigQuery: https://cloud.google.com/logging/docs/export/configure_export#manual-access-bq

Export to Pub/Sub
~~~~~~~~~~~~~~~~~

To export logs to BigQuery you must log into the Cloud Platform Console
and add ``cloud-logs@google.com`` to a topic.

See: `Setting permissions for Pub/Sub`_

.. doctest::

    >>> from gcloud import pubsub
    >>> client = pubsub.Client()
    >>> topic = client.topic('your-topic-name')
    >>> policy = top.get_iam_policy()
    >>> policy.owners.add(policy.group('cloud-logs@google.com'))
    >>> topic.set_iam_policy(policy)

.. _Setting permissions for Pub/Sub: https://cloud.google.com/logging/docs/export/configure_export#manual-access-pubsub

Create a Cloud Storage sink:

.. doctest::

   >>> from gcloud import logging
   >>> client = logging.Client()
   >>> sink = client.sink(
   ...     "robots-storage",
   ...     'log:apache-access AND textPayload:robot',
   ...     'storage.googleapis.com/my-bucket-name')
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
   ...     'log:apache-access AND textPayload:robot',
   ...     'bigquery.googleapis.com/projects/projects/my-project/datasets/my-dataset')
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
   ...      'log:apache-access AND textPayload:robot',
   ...      'pubsub.googleapis.com/projects/my-project/topics/my-topic')
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

Integration with Python logging module
---------------------------------------------


It's possible to tie the Python :mod:`logging` module directly into Google Cloud Logging. To use it,
create a :class:`CloudLoggingHandler <gcloud.logging.CloudLoggingHandler>` instance from your
Logging client.

.. doctest::

    >>> import logging
    >>> import gcloud.logging # Don't conflict with standard logging
    >>> from gcloud.logging.handlers import CloudLoggingHandler
    >>> client = gcloud.logging.Client()
    >>> handler = CloudLoggingHandler(client)
    >>> cloud_logger = logging.getLogger('cloudLogger')
    >>> cloud_logger.setLevel(logging.INFO) # defaults to WARN
    >>> cloud_logger.addHandler(handler)
    >>> cloud_logger.error('bad news') # API call

.. note::

    This handler currently only supports a synchronous API call, which means each logging statement
    that uses this handler will require an API call.

It is also possible to attach the handler to the root Python logger, so that for example a plain
`logging.warn` call would be sent to Cloud Logging, as well as any other loggers created. However,
you must avoid infinite recursion from the logging calls the client itself makes. A helper
method :meth:`setup_logging <gcloud.logging.handlers.setup_logging>` is provided to configure
this automatically:

.. doctest::

    >>> import logging
    >>> import gcloud.logging # Don't conflict with standard logging
    >>> from gcloud.logging.handlers import CloudLoggingHandler, setup_logging
    >>> client = gcloud.logging.Client()
    >>> handler = CloudLoggingHandler(client)
    >>> logging.getLogger().setLevel(logging.INFO) # defaults to WARN
    >>> setup_logging(handler)
    >>> logging.error('bad news') # API call
