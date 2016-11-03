Using the API
=============


Authentication and Configuration
--------------------------------

- For an overview of authentication in ``google-cloud-python``,
  see :doc:`google-cloud-auth`.

- In addition to any authentication configuration, you should also set the
  :envvar:`GOOGLE_CLOUD_PROJECT` environment variable for the project you'd like
  to interact with. If you are Google App Engine or Google Compute Engine
  this will be detected automatically.

- The library now enables the ``gRPC`` transport for the logging API by
  default, assuming that the required dependencies are installed and
  importable.  To *disable* this transport, set the
  :envvar:`GOOGLE_CLOUD_DISABLE_GRPC` environment variable to a
  non-empty string, e.g.:  ``$ export GOOGLE_CLOUD_DISABLE_GRPC=true``.

- After configuring your environment, create a
  :class:`Client <google.cloud.logging.client.Client>`

  .. literalinclude:: logging_snippets.py
     :start-after: [START client_create_default]
     :end-before: [END client_create_default]

  or pass in ``credentials`` and ``project`` explicitly

  .. literalinclude:: logging_snippets.py
     :start-after: [START client_create_explicit]
     :end-before: [END client_create_explicit]


Writing log entries
-------------------

To write log entries, first create a
:class:`~google.cloud.logging.logger.Logger`, passing the "log name" with
which to associate the entries:

.. literalinclude:: logging_snippets.py
    :start-after: [START logger_create]
    :end-before: [END logger_create]

Write a simple text entry to the logger.

.. literalinclude:: logging_snippets.py
    :start-after: [START logger_log_text]
    :end-before: [END logger_log_text]

Write a dictionary entry to the logger.

.. literalinclude:: logging_snippets.py
    :start-after: [START logger_log_struct]
    :end-before: [END logger_log_struct]


Retrieving log entries
----------------------

Fetch entries for the default project.

.. literalinclude:: logging_snippets.py
    :start-after: [START client_list_entries_default]
    :end-before: [END client_list_entries_default]

Fetch entries across multiple projects.

.. literalinclude:: logging_snippets.py
    :start-after: [START client_list_entries_multi_project]
    :end-before: [END client_list_entries_multi_project]

Filter entries retrieved using the `Advanced Logs Filters`_ syntax

.. _Advanced Logs Filters: https://cloud.google.com/logging/docs/view/advanced_filters

Fetch entries for the default project.

.. literalinclude:: logging_snippets.py
    :start-after: [START client_list_entries_filter]
    :end-before: [END client_list_entries_filter]

Sort entries in descending timestamp order.

.. literalinclude:: logging_snippets.py
    :start-after: [START client_list_entries_order_by]
    :end-before: [END client_list_entries_order_by]

Retrieve entries in batches of 10, iterating until done.

.. literalinclude:: logging_snippets.py
    :start-after: [START client_list_entries_paged]
    :end-before: [END client_list_entries_paged]

Retrieve entries for a single logger, sorting in descending timestamp order:

.. literalinclude:: logging_snippets.py
    :start-after: [START logger_list_entries]
    :end-before: [END logger_list_entries]


Delete all entries for a logger
-------------------------------

.. literalinclude:: logging_snippets.py
    :start-after: [START logger_delete]
    :end-before: [END logger_delete]


Manage log metrics
------------------

Metrics are counters of entries which match a given filter.  They can be
used within Stackdriver Monitoring to create charts and alerts.

List all metrics for a project:

.. literalinclude:: logging_snippets.py
    :start-after: [START client_list_metrics]
    :end-before: [END client_list_metrics]

Create a metric:

.. literalinclude:: logging_snippets.py
    :start-after: [START metric_create]
    :end-before: [END metric_create]

Refresh local information about a metric:

.. literalinclude:: logging_snippets.py
    :start-after: [START metric_reload]
    :end-before: [END metric_reload]

Update a metric:

.. literalinclude:: logging_snippets.py
    :start-after: [START metric_update]
    :end-before: [END metric_update]

Delete a metric:

.. literalinclude:: logging_snippets.py
    :start-after: [START metric_delete]
    :end-before: [END metric_delete]

Export log entries using sinks
------------------------------

Sinks allow exporting entries which match a given filter to Cloud Storage
buckets, BigQuery datasets, or Cloud Pub/Sub topics.

Export to Cloud Storage
~~~~~~~~~~~~~~~~~~~~~~~

Make sure that the storage bucket you want to export logs too has
``cloud-logs@google.com`` as the owner. See
`Setting permissions for Cloud Storage`_.

.. _Setting permissions for Cloud Storage: https://cloud.google.com/logging/docs/export/configure_export#setting_product_name_short_permissions_for_writing_exported_logs

Add ``cloud-logs@google.com`` as the owner of the bucket:

.. literalinclude:: logging_snippets.py
    :start-after: [START sink_bucket_permissions]
    :end-before: [END sink_bucket_permissions]

Create a Cloud Storage sink:

.. literalinclude:: logging_snippets.py
    :start-after: [START sink_storage_create]
    :end-before: [END sink_storage_create]


Export to BigQuery
~~~~~~~~~~~~~~~~~~

To export logs to BigQuery you must log into the Cloud Platform Console
and add ``cloud-logs@google.com`` to a dataset.

See: `Setting permissions for BigQuery`_

.. _Setting permissions for BigQuery: https://cloud.google.com/logging/docs/export/configure_export#manual-access-bq

.. literalinclude:: logging_snippets.py
    :start-after: [START sink_dataset_permissions]
    :end-before: [END sink_dataset_permissions]

Create a BigQuery sink:

.. literalinclude:: logging_snippets.py
    :start-after: [START sink_bigquery_create]
    :end-before: [END sink_bigquery_create]


Export to Pub/Sub
~~~~~~~~~~~~~~~~~

To export logs to BigQuery you must log into the Cloud Platform Console
and add ``cloud-logs@google.com`` to a topic.

See: `Setting permissions for Pub/Sub`_

.. _Setting permissions for Pub/Sub: https://cloud.google.com/logging/docs/export/configure_export#manual-access-pubsub

.. literalinclude:: logging_snippets.py
    :start-after: [START sink_topic_permissions]
    :end-before: [END sink_topic_permissions]

Create a Cloud Pub/Sub sink:

.. literalinclude:: logging_snippets.py
    :start-after: [START sink_pubsub_create]
    :end-before: [END sink_pubsub_create]

Manage Sinks
~~~~~~~~~~~~

List all sinks for a project:

.. literalinclude:: logging_snippets.py
    :start-after: [START client_list_sinks]
    :end-before: [END client_list_sinks]

Refresh local information about a sink:

.. literalinclude:: logging_snippets.py
    :start-after: [START sink_reload]
    :end-before: [END sink_reload]

Update a sink:

.. literalinclude:: logging_snippets.py
    :start-after: [START sink_update]
    :end-before: [END sink_update]

Delete a sink:

.. literalinclude:: logging_snippets.py
    :start-after: [START sink_delete]
    :end-before: [END sink_delete]
