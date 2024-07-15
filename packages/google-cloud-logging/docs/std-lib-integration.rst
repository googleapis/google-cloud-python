Integration with `logging` Standard Library
===========================================

We recommend that you use :mod:`google-cloud-logging` to integrate with
the Python :mod:`logging` standard library. This way, you can write logs using Python
standards, and still have your logs appear in Google Cloud Logging.

Automatic Configuration
-----------------------

To integrate :mod:`google-cloud-logging` with the standard :mod:`logging` module,
call :meth:`~google.cloud.logging_v2.client.Client.setup_logging` on a :class:`~google.cloud.logging_v2.client.Client` instance.

.. literalinclude:: ../samples/snippets/handler.py
    :start-after: [START logging_handler_setup]
    :end-before: [END logging_handler_setup]
    :dedent: 4

This :meth:`~google.cloud.logging_v2.client.Client.setup_logging` function chooses the best configurations for the environment your
code is running on. For more information, see the `Google Cloud Logging documentation <https://cloud.google.com/logging/docs/setup/python>`_.

Manual Handler Configuration
-----------------------------

.. _Manual Handler:

Automatic Configuration automatically determines the appropriate handler for the environment.
To specify the handler yourself, construct an instance manually and pass it in
as an argument to :meth:`~google.cloud.logging_v2.handlers.setup_logging`:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START create_cloud_handler]
    :end-before: [END create_cloud_handler]
    :dedent: 4

There are two supported handler classes to choose from:

- :class:`~google.cloud.logging_v2.handlers.handlers.CloudLoggingHandler`: 
    - Sends logs directly to Cloud Logging over the network (:doc:`gRPC or HTTP</grpc-vs-http>`)
    - Logs are transmitted according to a :ref:`Transport <Transports>` class
    - This is the default handler on most environments, including local development
- :class:`~google.cloud.logging_v2.handlers.structured_log.StructuredLogHandler`: 
    - Outputs logs as `structured JSON <https://cloud.google.com/logging/docs/structured-logging#special-payload-fields>`_ 
      to standard out, to be read and parsed by a GCP logging agent
    - This is the default handler on Kubernetes Engine, Cloud Functions and Cloud Run

Handler classes can also be specified via `dictConfig <https://docs.python.org/3/library/logging.config.html#logging-config-dictschema>`_:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logging_dict_config]
    :end-before: [END logging_dict_config]
    :dedent: 4

Note that since :class:`~google.cloud.logging_v2.handlers.handlers.CloudLoggingHandler` requires an already initialized :class:`~google.cloud.logging_v2.client.Client`,
you must initialize a client and include it in the dictConfig entry for a `CloudLoggingHandler`.

Standard Library
---------------------------

After you setup the Google Cloud Logging library with the Python :mod:`logging` standard library,
you can send logs with the standard logging library as you normally would:

.. literalinclude:: ../samples/snippets/handler.py
    :start-after: [START logging_handler_usage]
    :end-before: [END logging_handler_usage]
    :dedent: 4

For more information on using the Python :mod:`logging` standard library, see the `logging documentation <https://docs.python.org/3/howto/logging.html#a-simple-example>`_

Logging JSON Payloads
----------------------

.. _JSON:

Although the Python :mod:`logging` standard library `expects all logs to be strings <https://docs.python.org/3/library/logging.html#logging.Logger.debug>`_,
Google Cloud Logging allows `JSON payload data <https://cloud.google.com/logging/docs/structured-logging>`_.

To write JSON logs using the standard library integration, do one of the following:

1. Use the `json_fields` `extra` argument:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logging_extra_json_fields]
    :end-before: [END logging_extra_json_fields]
    :dedent: 4

2. Log a JSON-parsable string:

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logging_json_dumps]
    :end-before: [END logging_json_dumps]
    :dedent: 4


Automatic Metadata Detection
----------------------------

.. _Autodetection:

The Google Cloud Logging library attempts to detect and attach additional
`LogEntry fields <https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry>`_ .
The following fields are currently supported:

- labels
- trace
- span_id
- trace_sampled
- http_request
- source_location
- resource
- :ref:`json_fields<JSON>`

.. note::
    | More information about `trace`, `span_id`, and `trace_sampled` can be found :doc:`here </auto-trace-span-extraction>`.
    | `http_request` requires a :doc:`supported Python web framework </web-framework-integration>`.


Manual Metadata Using the `extra` Argument
--------------------------------------------

.. _Manual-Metadata:

The Python :mod:`logging` standard library accepts `an "extra" argument <https://docs.python.org/3/library/logging.html#logging.Logger.debug>`_ when
writing logs. You can use this argument to populate LogRecord objects with user-defined
key-value pairs. Google Cloud Logging uses the `extra` field as a way to pass in additional
metadata to populate `LogEntry fields`_.

.. literalinclude:: ../samples/snippets/usage_guide.py
    :start-after: [START logging_extras]
    :end-before: [END logging_extras]
    :dedent: 4

All of the `LogEntry fields`_
that can be :ref:`autodetected<Autodetection>` can also be set manually through the `extra` argument. Fields sent explicitly through the `extra`
argument override any :ref:`automatically detected<Autodetection>` fields.

CloudLoggingHandler Transports
------------------------------

.. _Transports:

:doc:`Transport</transport>` classes define how the :class:`~google.cloud.logging_v2.handlers.handlers.CloudLoggingHandler`
transports logs over the network to Google Cloud. There are two Transport implementations
(defined as subclasses of :class:`transports.base.Transport <google.cloud.logging_v2.handlers.transports.base.Transport>`):

- :class:`~google.cloud.logging_v2.handlers.transports.background_thread.BackgroundThreadTransport`:
    - sends logs in batches, using a background thread
    - the default Transport class
- :class:`~google.cloud.logging_v2.handlers.transports.sync.SyncTransport`:
    - sends each log synchronously in a single API call

You can set a Transport class by passing it as an argument when 
:ref:`initializing CloudLoggingHandler manually.<manual handler>`

You can use both transport options over :doc:`gRPC or HTTP</grpc-vs-http>`.

.. note::
    :class:`~google.cloud.logging_v2.handlers.structured_log.StructuredLogHandler`
    prints logs as formatted JSON to standard output, and does not use a Transport class.

.. _LogEntry fields: https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry