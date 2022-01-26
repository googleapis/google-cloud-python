Direct Library Usage
====================

We recommend that you use the :mod:`google-cloud-logging` library
by integrating it with the :doc:`Python logging standard library</std-lib-integration>`;
However, you can also use the library to interact with the Google Cloud Logging API 
directly.

In addition to writing logs, you can use the library to manage 
:doc:`logs</entries>`, :doc:`sinks</sink>`, :doc:`metrics</metric>`, and other resources.

Setup
----------------------------

Create a Client
~~~~~~~~~~~~~~~~~

.. _Creating Client:

You must set up a :doc:`Client</client>` to use the library:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START usage_client_setup]
    :end-before: [END usage_client_setup]
    :dedent: 4

To use HTTP, :doc:`disable gRPC</grpc-vs-http>` when you set up the :doc:`Client</client>`: 

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START usage_http_client_setup]
    :end-before: [END usage_http_client_setup]
    :dedent: 4

Create a Logger
~~~~~~~~~~~~~~~~~

Loggers read, write, and delete logs from Google Cloud. 

You use your :doc:`Client</client>` to create a :doc:`Logger</logger>`.

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logger_create]
    :end-before: [END logger_create]
    :dedent: 4

To add custom labels, do so when you initialize a :doc:`Logger</logger>`.
When you add custom labels, these labels are added to each
:doc:`LogEntry</entries>` written by the :doc:`Logger</logger>`:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logger_custom_labels]
    :end-before: [END logger_custom_labels]
    :dedent: 4

By default, the library adds a `Monitored Resource field <https://cloud.google.com/logging/docs/api/v2/resource-list>`_
associated with the environment the code is run on. For example, code run on
App Engine will have a `gae_app <https://cloud.google.com/monitoring/api/resources#tag_gae_app>`_
resource, while code run locally will have a `global <https://cloud.google.com/monitoring/api/resources#tag_global>`_ resource field.

To manually set the resource field, do so when you initialize the :doc:`Logger</logger>`:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logger_custom_resource]
    :end-before: [END logger_custom_resource]
    :dedent: 4


Write Log Entries
-------------------

You write logs by using :meth:`Logger.log <google.cloud.logging_v2.logging.Logger.log>`:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logger_log_basic]
    :end-before: [END logger_log_basic]
    :dedent: 4

You can add `LogEntry fields <https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry>`_
by passing them as keyword arguments:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logger_log_fields]
    :end-before: [END logger_log_fields]
    :dedent: 4

:meth:`Logger.log <google.cloud.logging_v2.logger.Logger.log>` chooses the appropriate :doc:`LogEntry </entries>` type
based on input type. To specify type, you can use the following Logger methods:

- :meth:`Logger.log_text <google.cloud.logging_v2.logger.Logger.log_text>` creates a  :class:`~google.cloud.logging_v2.entries.TextEntry`
- :meth:`Logger.log_struct <google.cloud.logging_v2.logger.Logger.log_struct>` creates a :class:`~google.cloud.logging_v2.entries.StructEntry`
- :meth:`Logger.log_proto <google.cloud.logging_v2.logger.Logger.log_proto>` creates a :class:`~google.cloud.logging_v2.entries.ProtobufEntry`
- :meth:`Logger.log_empty <google.cloud.logging_v2.logger.Logger.log_empty>` creates an empty :class:`~google.cloud.logging_v2.entries.LogEntry`

Batch Write Logs
------------------

By default, each log write takes place in an individual network request, which may be inefficient at scale.

Using the :class:`~google.cloud.logging_v2.logger.Batch` class, logs are batched together, and only sent out 
when :func:`batch.commit <google.cloud.logging_v2.logger.Batch.commit>` is called.

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logger_log_batch]
    :end-before: [END logger_log_batch]
    :dedent: 4

To simplify things, you can also use :class:`~google.cloud.logging_v2.logger.Batch` as a context manager:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logger_log_batch_context]
    :end-before: [END logger_log_batch_context]
    :dedent: 4

In the previous example, the logs are automatically committed when the code exits the "with" block.

Retrieve Log Entries
---------------------

You retrieve log entries for the default project using 
:meth:`list_entries() <google.cloud.logging_v2.client.Client.list_entries>` 
on a :doc:`Client</client>` or :doc:`Logger</logger>` object:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START client_list_entries_default]
    :end-before: [END client_list_entries_default]
    :dedent: 4

Entries returned by
:meth:`Client.list_entries() <google.cloud.logging_v2.client.Client.list_entries>`
or
:meth:`Logger.list_entries() <google.cloud.logging_v2.logger.Logger.list_entries>`
are instances of one of the following classes:

- :class:`~google.cloud.logging_v2.entries.TextEntry`
- :class:`~google.cloud.logging_v2.entries.StructEntry`
- :class:`~google.cloud.logging_v2.entries.ProtobufEntry`

To filter entries retrieved using the `Advanced Logs Filters`_ syntax

.. _Advanced Logs Filters: https://cloud.google.com/logging/docs/view/advanced_filters

To fetch entries for the default project.

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START client_list_entries_filter]
    :end-before: [END client_list_entries_filter]
    :dedent: 4

To sort entries in descending timestamp order.

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START client_list_entries_order_by]
    :end-before: [END client_list_entries_order_by]
    :dedent: 4

To retrieve entries for a single logger, sorting in descending timestamp order:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logger_list_entries]
    :end-before: [END logger_list_entries]
    :dedent: 4

For example, to retrieve all `GKE Admin Activity audit logs`_
from the past 24 hours:

.. _GKE Admin Activity audit logs: https://cloud.google.com/kubernetes-engine/docs/how-to/audit-logging#audit_logs_in_your_project

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logging_list_gke_audit_logs]
    :end-before: [END logging_list_gke_audit_logs]
    :dedent: 4


Delete Log Entries
--------------------

To delete all logs associated with a logger, use the following call:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logger_delete]
    :end-before: [END logger_delete]
    :dedent: 8


Manage Log Metrics
--------------------

Logs-based metrics are counters of entries which match a given filter.
They can be used within Cloud Monitoring to create charts and alerts.

To list all logs-based metrics for a project:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START client_list_metrics]
    :end-before: [END client_list_metrics]
    :dedent: 4

To create a logs-based metric:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START metric_create]
    :end-before: [END metric_create]
    :dedent: 4

To refresh local information about a logs-based metric:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START metric_reload]
    :end-before: [END metric_reload]
    :dedent: 4

To update a logs-based metric:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START metric_update]
    :end-before: [END metric_update]
    :dedent: 4

To delete a logs-based metric:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START metric_delete]
    :end-before: [END metric_delete]
    :dedent: 4

Log Sinks
---------------

Sinks allow exporting of log entries which match a given filter to
Cloud Storage buckets, BigQuery datasets, or Cloud Pub/Sub topics.

Cloud Storage Sink
~~~~~~~~~~~~~~~~~~~~~~~

Ensure the storage bucket that you want to export logs to has
``cloud-logs@google.com`` as an owner. See
`Setting permissions for Cloud Storage`_.

.. _Setting permissions for Cloud Storage: https://cloud.google.com/logging/docs/export/configure_export_v2#errors_exporting_to_cloud_storage

Ensure that ``cloud-logs@google.com`` is an owner of the bucket:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START sink_bucket_permissions]
    :end-before: [END sink_bucket_permissions]
    :dedent: 4

To create a Cloud Storage sink:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START sink_storage_create]
    :end-before: [END sink_storage_create]
    :dedent: 4


BigQuery Sink
~~~~~~~~~~~~~~~~~~

To export logs to BigQuery, you must log into the Cloud Console
and add ``cloud-logs@google.com`` to a dataset.

See: `Setting permissions for BigQuery`_

.. _Setting permissions for BigQuery: https://cloud.google.com/logging/docs/export/configure_export_v2#errors_exporting_to_bigquery

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START sink_dataset_permissions]
    :end-before: [END sink_dataset_permissions]
    :dedent: 4

To create a BigQuery sink:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START sink_bigquery_create]
    :end-before: [END sink_bigquery_create]
    :dedent: 4


Pub/Sub Sink
~~~~~~~~~~~~~~~~~

To export logs to BigQuery you must log into the Cloud Console
and add ``cloud-logs@google.com`` to a topic.

See: `Setting permissions for Pub/Sub`_

.. _Setting permissions for Pub/Sub: https://cloud.google.com/logging/docs/export/configure_export_v2#errors_exporting_logs_to_cloud_pubsub

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START sink_topic_permissions]
    :end-before: [END sink_topic_permissions]
    :dedent: 4

To create a Cloud Pub/Sub sink:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START sink_pubsub_create]
    :end-before: [END sink_pubsub_create]
    :dedent: 4

Manage Sinks
~~~~~~~~~~~~~~

To list all sinks for a project:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START client_list_sinks]
    :end-before: [END client_list_sinks]
    :dedent: 4

To refresh local information about a sink:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START sink_reload]
    :end-before: [END sink_reload]
    :dedent: 4

To update a sink:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START sink_update]
    :end-before: [END sink_update]
    :dedent: 4

To delete a sink:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START sink_delete]
    :end-before: [END sink_delete]
    :dedent: 4
