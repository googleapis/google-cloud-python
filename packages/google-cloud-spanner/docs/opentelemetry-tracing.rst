Tracing with OpenTelemetry
==========================

This library uses `OpenTelemetry <https://opentelemetry.io/>`_ to automatically generate traces providing insight on calls to Cloud Spanner. 
For information on the benefits and utility of tracing, see the `Cloud Trace docs <https://cloud.google.com/trace/docs/overview>`_.

To take advantage of these traces, we first need to install OpenTelemetry:

.. code-block:: sh

    pip install opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation

    # [Optional] Installs the cloud monitoring exporter, however you can use any exporter of your choice
    pip install opentelemetry-exporter-google-cloud

We also need to tell OpenTelemetry which exporter to use. To export Spanner traces to `Cloud Tracing <https://cloud.google.com/trace>`_, add the following lines to your application:

.. code:: python

    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.trace.sampling import ProbabilitySampler
    from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
    # BatchExportSpanProcessor exports spans to Cloud Trace 
    # in a seperate thread to not block on the main thread
    from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

    # Create and export one trace every 1000 requests
    sampler = ProbabilitySampler(1/1000)
    # Use the default tracer provider
    trace.set_tracer_provider(TracerProvider(sampler=sampler))
    trace.get_tracer_provider().add_span_processor(
        # Initialize the cloud tracing exporter
        BatchExportSpanProcessor(CloudTraceSpanExporter())
    )

Generated spanner traces should now be available on `Cloud Trace <https://console.cloud.google.com/traces>`_.

Tracing is most effective when many libraries are instrumented to provide insight over the entire lifespan of a request.
For a list of libraries that can be instrumented, see the `OpenTelemetry Integrations` section of the `OpenTelemetry Python docs <https://opentelemetry-python.readthedocs.io/en/stable/>`_
