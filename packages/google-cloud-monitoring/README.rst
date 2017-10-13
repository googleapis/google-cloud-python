Python Client for Stackdriver Monitoring
========================================

    Python idiomatic client for `Stackdriver Monitoring`_

.. _Stackdriver Monitoring: https://cloud.google.com/monitoring/

|pypi| |versions|

-  `Documentation`_

.. _Documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/monitoring/usage.html

Quick Start
-----------

.. code-block:: console

    $ pip install --upgrade google-cloud-monitoring

Fore more information on setting up your Python development environment, such as installing ``pip`` and on your system, please refer to `Python Development Environment Setup Guide`_ for Google Cloud Platform.

.. _Python Development Environment Setup Guide: https://cloud.google.com/python/setup

Authentication
--------------

With ``google-cloud-python`` we try to make authentication as painless as
possible. Check out the `Authentication section`_ in our documentation to
learn more. You may also find the `authentication document`_ shared by all
the ``google-cloud-*`` libraries to be helpful.

.. _Authentication section: https://google-cloud-python.readthedocs.io/en/latest/core/auth.html
.. _authentication document: https://github.com/GoogleCloudPlatform/google-cloud-common/tree/master/authentication

Using the API
-------------

`Stackdriver Monitoring`_ (`Monitoring API docs`_) collects metrics,
events, and metadata from Google Cloud Platform, Amazon Web Services (AWS),
hosted uptime probes, application instrumentation, and a variety of common
application components including Cassandra, Nginx, Apache Web Server,
Elasticsearch and many others. Stackdriver ingests that data and generates
insights via dashboards, charts, and alerts.

This package currently supports all Monitoring API operations other than
writing custom metrics.

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

See the ``google-cloud-python`` API `monitoring documentation`_ to learn how
to connect to Stackdriver Monitoring using this Client Library.

.. _monitoring documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/monitoring/usage.html

.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-monitoring.svg
   :target: https://pypi.org/project/google-cloud-monitoring/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-monitoring.svg
   :target: https://pypi.org/project/google-cloud-monitoring/
