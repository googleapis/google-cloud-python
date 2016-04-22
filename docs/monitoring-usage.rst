Using the API
=============


Introduction
------------

With the Monitoring API, you can work with Stackdriver metric data
pertaining to monitored resources in Google Cloud Platform (GCP)
or elsewhere.

Essential concepts:

- Metric data is associated with a **monitored resource**. A monitored
  resource has a *resource type* and a set of *resource labels* —
  key-value pairs — that identify the particular resource.
- A **metric** further identifies the particular kind of data that
  is being collected. It has a *metric type* and a set of *metric
  labels* that, when combined with the resource labels, identify
  a particular time series.
- A **time series** is a collection of data points associated with
  points or intervals in time.

Please refer to the documentation for the `Monitoring API`_ for
more information.

At present, this client library supports querying of time series,
metric descriptors, and resource descriptors.

.. _Monitoring API: https://cloud.google.com/monitoring/api/


The Monitoring Client Object
----------------------------

The monitoring client library generally makes its
functionality available as methods of the monitoring
:class:`~gcloud.monitoring.client.Client` class.
A :class:`~gcloud.monitoring.client.Client` instance holds
authentication credentials and the ID of the target project with
which the metric data of interest is associated. This project ID
will often refer to a `Stackdriver account`_ binding multiple
GCP projects and AWS accounts. It can also simply be the ID of
a monitored project.

Most often the authentication credentials will be determined
implicitly from your environment. See :doc:`gcloud-auth` for
more information.

It is thus typical to create a client object as follows::

    >>> from gcloud import monitoring
    >>> client = monitoring.Client(project='target-project')

If you are running in Google Compute Engine or Google App Engine,
the current project is the default target project. This default
can be further overridden with the :envvar:`GCLOUD_PROJECT`
environment variable. Using the default target project is
even easier::

    >>> client = monitoring.Client()

If necessary, you can pass in ``credentials`` and ``project`` explicitly::

    >>> client = monitoring.Client(project='target-project', credentials=...)

.. _Stackdriver account: https://cloud.google.com/monitoring/accounts/


Monitored Resource Descriptors
------------------------------

The available monitored resource types are defined by *monitored resource
descriptors*. You can fetch a list of these with the
:meth:`~gcloud.monitoring.client.Client.list_resource_descriptors` method::

    >>> for descriptor in client.list_resource_descriptors():
    ...     print(descriptor.type)

Each :class:`~gcloud.monitoring.resource.ResourceDescriptor`
has a type, a display name, a description, and a list of
:class:`~gcloud.monitoring.label.LabelDescriptor` instances.
See the documentation about `Monitored Resources`_
for more information.

.. _Monitored Resources:
    https://cloud.google.com/monitoring/api/v3/monitored-resources


Metric Descriptors
------------------

The available metric types are defined by *metric descriptors*.
They include `platform metrics`_, `agent metrics`_, and `custom metrics`_.
You can list all of these with the
:meth:`~gcloud.monitoring.client.Client.list_metric_descriptors` method::

    >>> for descriptor in client.list_metric_descriptors():
    ...     print(descriptor.type)

See :class:`~gcloud.monitoring.metric.MetricDescriptor` and the
`Metric Descriptors`_ API documentation for more information.

.. _platform metrics: https://cloud.google.com/monitoring/api/metrics
.. _agent metrics: https://cloud.google.com/monitoring/agent/
.. _custom metrics: https://cloud.google.com/monitoring/custom-metrics/
.. _Metric Descriptors:
    https://cloud.google.com/monitoring/api/ref_v3/rest/v3/\
    projects.metricDescriptors


Time Series Queries
-------------------

A time series includes a collection of data points and a set of
resource and metric label values.
See :class:`~gcloud.monitoring.timeseries.TimeSeries` and the
`Time Series`_ API documentation for more information.

While you can obtain time series objects by iterating over a
:class:`~gcloud.monitoring.query.Query` object, usually it is
more useful to retrieve time series data in the form of a
:class:`pandas.DataFrame`, where each column corresponds to a
single time series. For this, you must have :mod:`pandas` installed;
it is not a required dependency of ``gcloud-python``.

You can display CPU utilization across your GCE instances during
the last five minutes as follows::

    >>> METRIC = 'compute.googleapis.com/instance/cpu/utilization'
    >>> query = client.query(METRIC, minutes=5)
    >>> print(query.as_dataframe())

:class:`~gcloud.monitoring.query.Query` objects provide a variety of
methods for refining the query. You can request temporal alignment
and cross-series reduction, and you can filter by label values.
See the client :meth:`~gcloud.monitoring.client.Client.query` method
and the :class:`~gcloud.monitoring.query.Query` class for more
information.

For example, you can display CPU utilization during the last hour
across GCE instances with names beginning with ``"mycluster-"``,
averaged over five-minute intervals and aggregated per zone, as
follows::

    >>> from gcloud.monitoring import Aligner, Reducer
    >>> METRIC = 'compute.googleapis.com/instance/cpu/utilization'
    >>> query = (client.query(METRIC, hours=1)
    ...          .select_metrics(instance_name_prefix='mycluster-')
    ...          .align(Aligner.ALIGN_MEAN, minutes=5)
    ...          .reduce(Reducer.REDUCE_MEAN, 'resource.zone'))
    >>> print(query.as_dataframe())

.. _Time Series:
    https://cloud.google.com/monitoring/api/ref_v3/rest/v3/TimeSeries
