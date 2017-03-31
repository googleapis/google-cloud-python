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
     :dedent: 4

  or pass in ``credentials`` and ``project`` explicitly

  .. literalinclude:: logging_snippets.py
     :start-after: [START client_create_explicit]
     :end-before: [END client_create_explicit]
     :dedent: 4


Writing log entries
-------------------

To write log entries, first create a
:class:`~google.cloud.logging.logger.Logger`, passing the "log name" with
which to associate the entries:

.. literalinclude:: logging_snippets.py
    :start-after: [START logger_create]
    :end-before: [END logger_create]
    :dedent: 4

Write a simple text entry to the logger.

.. literalinclude:: logging_snippets.py
    :start-after: [START logger_log_text]
    :end-before: [END logger_log_text]
    :dedent: 4

Write a dictionary entry to the logger.

.. literalinclude:: logging_snippets.py
    :start-after: [START logger_log_struct]
    :end-before: [END logger_log_struct]
    :dedent: 4


Retrieving log entries
----------------------

Fetch entries for the default project.

.. literalinclude:: logging_snippets.py
    :start-after: [START client_list_entries_default]
    :end-before: [END client_list_entries_default]
    :dedent: 4

Fetch entries across multiple projects.

.. literalinclude:: logging_snippets.py
    :start-after: [START client_list_entries_multi_project]
    :end-before: [END client_list_entries_multi_project]
    :dedent: 4

Filter entries retrieved using the `Advanced Logs Filters`_ syntax

.. _Advanced Logs Filters: https://cloud.google.com/logging/docs/view/advanced_filters

Fetch entries for the default project.

.. literalinclude:: logging_snippets.py
    :start-after: [START client_list_entries_filter]
    :end-before: [END client_list_entries_filter]
    :dedent: 4

Sort entries in descending timestamp order.

.. literalinclude:: logging_snippets.py
    :start-after: [START client_list_entries_order_by]
    :end-before: [END client_list_entries_order_by]
    :dedent: 4

Retrieve entries in batches of 10, iterating until done.

.. literalinclude:: logging_snippets.py
    :start-after: [START client_list_entries_paged]
    :end-before: [END client_list_entries_paged]
    :dedent: 4

Retrieve entries for a single logger, sorting in descending timestamp order:

.. literalinclude:: logging_snippets.py
    :start-after: [START logger_list_entries]
    :end-before: [END logger_list_entries]
    :dedent: 4


Delete all entries for a logger
-------------------------------

.. literalinclude:: logging_snippets.py
    :start-after: [START logger_delete]
    :end-before: [END logger_delete]
    :dedent: 8


Manage log metrics
------------------

Metrics are counters of entries which match a given filter.  They can be
used within Stackdriver Monitoring to create charts and alerts.

List all metrics for a project:

.. literalinclude:: logging_snippets.py
    :start-after: [START client_list_metrics]
    :end-before: [END client_list_metrics]
    :dedent: 4

Create a metric:

.. literalinclude:: logging_snippets.py
    :start-after: [START metric_create]
    :end-before: [END metric_create]
    :dedent: 4

Refresh local information about a metric:

.. literalinclude:: logging_snippets.py
    :start-after: [START metric_reload]
    :end-before: [END metric_reload]
    :dedent: 4

Update a metric:

.. literalinclude:: logging_snippets.py
    :start-after: [START metric_update]
    :end-before: [END metric_update]
    :dedent: 4

Delete a metric:

.. literalinclude:: logging_snippets.py
    :start-after: [START metric_delete]
    :end-before: [END metric_delete]
    :dedent: 4

Export log entries using sinks
------------------------------

Sinks allow exporting entries which match a given filter to Cloud Storage
buckets, BigQuery datasets, or Cloud Pub/Sub topics.

Export to Cloud Storage
~~~~~~~~~~~~~~~~~~~~~~~

Make sure that the storage bucket you want to export logs too has
``cloud-logs@google.com`` as the owner. See
`Setting permissions for Cloud Storage`_.

.. _Setting permissions for Cloud Storage: https://cloud.google.com/logging/docs/export/configure_export_v2#errors_exporting_to_cloud_storage

Add ``cloud-logs@google.com`` as the owner of the bucket:

.. literalinclude:: logging_snippets.py
    :start-after: [START sink_bucket_permissions]
    :end-before: [END sink_bucket_permissions]
    :dedent: 4

Create a Cloud Storage sink:

.. literalinclude:: logging_snippets.py
    :start-after: [START sink_storage_create]
    :end-before: [END sink_storage_create]
    :dedent: 4


Export to BigQuery
~~~~~~~~~~~~~~~~~~

To export logs to BigQuery you must log into the Cloud Platform Console
and add ``cloud-logs@google.com`` to a dataset.

See: `Setting permissions for BigQuery`_

.. _Setting permissions for BigQuery: https://cloud.google.com/logging/docs/export/configure_export_v2#errors_exporting_to_bigquery

.. literalinclude:: logging_snippets.py
    :start-after: [START sink_dataset_permissions]
    :end-before: [END sink_dataset_permissions]
    :dedent: 4

Create a BigQuery sink:

.. literalinclude:: logging_snippets.py
    :start-after: [START sink_bigquery_create]
    :end-before: [END sink_bigquery_create]
    :dedent: 4


Export to Pub/Sub
~~~~~~~~~~~~~~~~~

To export logs to BigQuery you must log into the Cloud Platform Console
and add ``cloud-logs@google.com`` to a topic.

See: `Setting permissions for Pub/Sub`_

.. _Setting permissions for Pub/Sub: https://cloud.google.com/logging/docs/export/configure_export_v2#errors_exporting_logs_to_cloud_pubsub

.. literalinclude:: logging_snippets.py
    :start-after: [START sink_topic_permissions]
    :end-before: [END sink_topic_permissions]
    :dedent: 4

Create a Cloud Pub/Sub sink:

.. literalinclude:: logging_snippets.py
    :start-after: [START sink_pubsub_create]
    :end-before: [END sink_pubsub_create]
    :dedent: 4

Manage Sinks
~~~~~~~~~~~~

List all sinks for a project:

.. literalinclude:: logging_snippets.py
    :start-after: [START client_list_sinks]
    :end-before: [END client_list_sinks]
    :dedent: 4

Refresh local information about a sink:

.. literalinclude:: logging_snippets.py
    :start-after: [START sink_reload]
    :end-before: [END sink_reload]
    :dedent: 4

Update a sink:

.. literalinclude:: logging_snippets.py
    :start-after: [START sink_update]
    :end-before: [END sink_update]
    :dedent: 4

Delete a sink:

.. literalinclude:: logging_snippets.py
    :start-after: [START sink_delete]
    :end-before: [END sink_delete]
    :dedent: 4

Integration with Python logging module
--------------------------------------

It's possible to tie the Python :mod:`logging` module directly into Google
Stackdriver Logging. There are different handler options to accomplish this.
To automatically pick the default for your current environment, use
:meth:`~google.cloud.logging.client.Client.get_default_handler`.

.. literalinclude:: logging_snippets.py
    :start-after: [START create_default_handler]
    :end-before: [END create_default_handler]
    :dedent: 4

It is also possible to attach the handler to the root Python logger, so that
for example a plain ``logging.warn`` call would be sent to Stackdriver Logging,
as well as any other loggers created. A helper method
:meth:`~google.cloud.logging.client.Client.setup_logging` is provided
to configure this automatically.

.. literalinclude:: logging_snippets.py
    :start-after: [START setup_logging]
    :end-before: [END setup_logging]
    :dedent: 4

.. note::

    To reduce cost and quota usage, do not enable Stackdriver logging
    handlers while testing locally.

You can also exclude certain loggers:

.. literalinclude:: logging_snippets.py
    :start-after: [START setup_logging_excludes]
    :end-before: [END setup_logging_excludes]
    :dedent: 4

Cloud Logging Handler
=====================

If you prefer not to use
:meth:`~google.cloud.logging.client.Client.get_default_handler`, you can
directly create a
:class:`~google.cloud.logging.handlers.handlers.CloudLoggingHandler` instance
which will write directly to the API.

.. literalinclude:: logging_snippets.py
    :start-after: [START create_cloud_handler]
    :end-before: [END create_cloud_handler]
    :dedent: 4

.. note::

    This handler by default uses an asynchronous transport that sends log
    entries on a background thread. However, the API call will still be made
    in the same process. For other transport options, see the transports
    section.

All logs will go to a single custom log, which defaults to "python". The name
of the Python logger will be included in the structured log entry under the
"python_logger" field. You can change it by providing a name to the handler:

.. literalinclude:: logging_snippets.py
    :start-after: [START create_named_handler]
    :end-before: [END create_named_handler]
    :dedent: 4

fluentd logging handlers
========================

Besides :class:`~google.cloud.logging.handlers.handlers.CloudLoggingHandler`,
which writes directly to the API, two other handlers are provided.
:class:`~google.cloud.logging.handlers.app_engine.AppEngineHandler`, which is
recommended when running on the Google App Engine Flexible vanilla runtimes
(i.e. your app.yaml contains ``runtime: python``), and
:class:`~google.cloud.logging.handlers.container_engine.ContainerEngineHandler`
, which is recommended when running on `Google Container Engine`_ with the
Stackdriver Logging plugin enabled.

:meth:`~google.cloud.logging.client.Client.get_default_handler` and
:meth:`~google.cloud.logging.client.Client.setup_logging` will attempt to use
the environment to automatically detect whether the code is running in
these platforms and use the appropriate handler.

In both cases, the fluentd agent is configured to automatically parse log files
in an expected format and forward them to Stackdriver logging. The handlers
provided help set the correct metadata such as log level so that logs can be
filtered accordingly.

Cloud Logging Handler transports
=================================

The :class:`~google.cloud.logging.handlers.handlers.CloudLoggingHandler`
logging handler can use different transports. The default is
:class:`~google.cloud.logging.handlers.BackgroundThreadTransport`.

 1. :class:`~google.cloud.logging.handlers.BackgroundThreadTransport` this is
    the default. It writes entries on a background
    :class:`python.threading.Thread`.

 1. :class:`~google.cloud.logging.handlers.SyncTransport` this handler does a
    direct API call on each logging statement to write the entry.


.. _Google Container Engine: https://cloud.google.com/container-engine/
