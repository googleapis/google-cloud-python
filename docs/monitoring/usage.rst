Stackdriver Monitoring
======================

.. toctree::
  :maxdepth: 2
  :hidden:

  releases
  client
  group
  query
  types
  enums

Introduction
------------

With the Stackdriver Monitoring API, you can work with Stackdriver metric data
pertaining to monitored resources in Google Cloud Platform (GCP)
or elsewhere.

Essential concepts:

- Metric data is associated with a **monitored resource**. A monitored
  resource has a *resource type* and a set of *resource labels* —
  key-value pairs — that identify the particular resource.
- A **metric** further identifies the particular kind of data that
  is being collected. It has a *metric type* and a set of
  *metric labels* that, when combined with the resource labels, identify
  a particular time series.
- A **time series** is a collection of data points associated with
  points or intervals in time.

Please refer to the documentation for the `Stackdriver Monitoring API`_ for
more information.

At present, this client library supports the following features
of the API:

- Querying of time series.
- Querying of metric descriptors and monitored resource descriptors.
- Creation and deletion of metric descriptors for custom metrics.
- Writing of custom metric data.

.. _Stackdriver Monitoring API: https://cloud.google.com/monitoring/api/v3/


The Stackdriver Monitoring Client Object
----------------------------------------

The Stackdriver Monitoring client library generally makes its
functionality available as methods of the monitoring
:class:`~google.cloud.monitoring.client.Client` class.
A :class:`~google.cloud.monitoring.client.Client` instance holds
authentication credentials and the ID of the target project with
which the metric data of interest is associated. This project ID
will often refer to a `Stackdriver account`_ binding multiple
GCP projects and AWS accounts. It can also simply be the ID of
a monitored project.

Most often the authentication credentials will be determined
implicitly from your environment. See :doc:`/core/auth` for
more information.

It is thus typical to create a client object as follows:

.. code-block:: python

    >>> from google.cloud import monitoring
    >>> client = monitoring.Client(project='target-project')

If you are running in Google Compute Engine or Google App Engine,
the current project is the default target project. This default
can be further overridden with the :envvar:`GOOGLE_CLOUD_PROJECT`
environment variable. Using the default target project is
even easier:

.. code-block:: python

    >>> client = monitoring.Client()

If necessary, you can pass in ``credentials`` and ``project`` explicitly:

.. code-block:: python

    >>> client = monitoring.Client(project='target-project', credentials=...)

.. _Stackdriver account: https://cloud.google.com/monitoring/accounts/


Monitored Resource Descriptors
------------------------------

The available monitored resource types are defined by *monitored resource
descriptors*. You can fetch a list of these with the
:meth:`~google.cloud.monitoring.client.Client.list_resource_descriptors` method:

.. code-block:: python

    >>> for descriptor in client.list_resource_descriptors():
    ...     print(descriptor.type)

Each :class:`~google.cloud.monitoring.resource.ResourceDescriptor`
has a type, a display name, a description, and a list of
:class:`~google.cloud.monitoring.label.LabelDescriptor` instances.
See the documentation about `Monitored Resources`_
for more information.

.. _Monitored Resources:
    https://cloud.google.com/monitoring/api/v3/monitored-resources


Metric Descriptors
------------------

The available metric types are defined by *metric descriptors*.
They include `platform metrics`_, `agent metrics`_, and `custom metrics`_.
You can list all of these with the
:meth:`~google.cloud.monitoring.client.Client.list_metric_descriptors` method:

.. code-block:: python

    >>> for descriptor in client.list_metric_descriptors():
    ...     print(descriptor.type)

See :class:`~google.cloud.monitoring.metric.MetricDescriptor` and the
`Metric Descriptors`_ API documentation for more information.

You can create new metric descriptors to define custom metrics in
the ``custom.googleapis.com`` namespace. You do this by creating a
:class:`~google.cloud.monitoring.metric.MetricDescriptor` object using the
client's :meth:`~google.cloud.monitoring.client.Client.metric_descriptor`
factory and then calling the object's
:meth:`~google.cloud.monitoring.metric.MetricDescriptor.create` method:

.. code-block:: python

    >>> from google.cloud.monitoring import MetricKind, ValueType
    >>> descriptor = client.metric_descriptor(
    ...     'custom.googleapis.com/my_metric',
    ...     metric_kind=MetricKind.GAUGE,
    ...     value_type=ValueType.DOUBLE,
    ...     description='This is a simple example of a custom metric.')
    >>> descriptor.create()

You can delete such a metric descriptor as follows:

.. code-block:: python

    >>> descriptor = client.metric_descriptor(
    ...     'custom.googleapis.com/my_metric')
    >>> descriptor.delete()

To define a custom metric parameterized by one or more labels,
you must build the appropriate
:class:`~google.cloud.monitoring.label.LabelDescriptor` objects
and include them in the
:class:`~google.cloud.monitoring.metric.MetricDescriptor` object
before you call
:meth:`~google.cloud.monitoring.metric.MetricDescriptor.create`:

.. code-block:: python

    >>> from google.cloud.monitoring import LabelDescriptor, LabelValueType
    >>> label = LabelDescriptor('response_code', LabelValueType.INT64,
    ...                         description='HTTP status code')
    >>> descriptor = client.metric_descriptor(
    ...     'custom.googleapis.com/my_app/response_count',
    ...     metric_kind=MetricKind.CUMULATIVE,
    ...     value_type=ValueType.INT64,
    ...     labels=[label],
    ...     description='Cumulative count of HTTP responses.')
    >>> descriptor.create()

.. _platform metrics: https://cloud.google.com/monitoring/api/metrics
.. _agent metrics: https://cloud.google.com/monitoring/agent/
.. _custom metrics: https://cloud.google.com/monitoring/custom-metrics/
.. _Metric Descriptors:
    https://cloud.google.com/monitoring/api/ref_v3/rest/v3/\
    projects.metricDescriptors


Groups
------

A group is a dynamic collection of *monitored resources* whose membership is
defined by a `filter`_.  These groups are usually created via the
`Stackdriver dashboard`_. You can list all the groups in a project with the
:meth:`~google.cloud.monitoring.client.Client.list_groups` method:

.. code-block:: python

    >>> for group in client.list_groups():
    ...     print(group.id, group.display_name, group.parent_id)
    ('a001', 'Production', None)
    ('a002', 'Front-end', 'a001')
    ('1003', 'Back-end', 'a001')

See :class:`~google.cloud.monitoring.group.Group` and the API documentation for
`Groups`_ and `Group members`_ for more information.

You can get a specific group based on it's ID as follows:

.. code-block:: python

    >>> group = client.fetch_group('a001')

You can get the current members of this group using the
:meth:`~google.cloud.monitoring.group.Group.list_members` method:

.. code-block:: python

    >>> for member in group.list_members():
    ...     print(member)

Passing in ``end_time`` and ``start_time`` to the above method will return
historical members based on the current filter of the group. The group
membership changes over time, as *monitored resources* come and go, and as they
change properties.

You can create new groups to define new collections of *monitored resources*.
You do this by creating a :class:`~google.cloud.monitoring.group.Group` object using
the client's :meth:`~google.cloud.monitoring.client.Client.group` factory and then
calling the object's :meth:`~google.cloud.monitoring.group.Group.create` method:

.. code-block:: python

    >>> filter_string = 'resource.zone = "us-central1-a"'
    >>> group = client.group(
    ...     display_name='My group',
    ...     filter_string=filter_string,
    ...     parent_id='a001',
    ...     is_cluster=True)
    >>> group.create()
    >>> group.id
    '1234'

You can further manipulate an existing group by first initializing a Group
object with it's ID or name, and then calling various methods on it.

Delete a group:

.. code-block:: python

    >>> group = client.group('1234')
    >>> group.exists()
    True
    >>> group.delete()


Update a group:

.. code-block:: python

    >>> group = client.group('1234')
    >>> group.exists()
    True
    >>> group.reload()
    >>> group.display_name = 'New Display Name'
    >>> group.update()

.. _Stackdriver dashboard:
    https://support.stackdriver.com/customer/portal/articles/\
    1535145-creating-groups
.. _filter:
    https://cloud.google.com/monitoring/api/v3/filters#group-filter
.. _Groups:
    https://cloud.google.com/monitoring/api/ref_v3/rest/v3/\
    projects.groups
.. _Group members:
    https://cloud.google.com/monitoring/api/ref_v3/rest/v3/\
    projects.groups.members


Time Series Queries
-------------------

A time series includes a collection of data points and a set of
resource and metric label values.
See :class:`~google.cloud.monitoring.timeseries.TimeSeries` and the
`Time Series`_ API documentation for more information.

While you can obtain time series objects by iterating over a
:class:`~google.cloud.monitoring.query.Query` object, usually it is
more useful to retrieve time series data in the form of a
:class:`pandas.DataFrame`, where each column corresponds to a
single time series. For this, you must have :mod:`pandas` installed;
it is not a required dependency of ``google-cloud-python``.

You can display CPU utilization across your GCE instances over a five minute duration ending at
the start of the current minute as follows:

.. code-block:: python

    >>> METRIC = 'compute.googleapis.com/instance/cpu/utilization'
    >>> query = client.query(METRIC, minutes=5)
    >>> print(query.as_dataframe())

:class:`~google.cloud.monitoring.query.Query` objects provide a variety of
methods for refining the query. You can request temporal alignment
and cross-series reduction, and you can filter by label values.
See the client :meth:`~google.cloud.monitoring.client.Client.query` method
and the :class:`~google.cloud.monitoring.query.Query` class for more
information.

For example, you can display CPU utilization during the last hour
across GCE instances with names beginning with ``"mycluster-"``,
averaged over five-minute intervals and aggregated per zone, as
follows:

.. code-block:: python

    >>> from google.cloud.monitoring import Aligner, Reducer
    >>> METRIC = 'compute.googleapis.com/instance/cpu/utilization'
    >>> query = (client.query(METRIC, hours=1)
    ...          .select_metrics(instance_name_prefix='mycluster-')
    ...          .align(Aligner.ALIGN_MEAN, minutes=5)
    ...          .reduce(Reducer.REDUCE_MEAN, 'resource.zone'))
    >>> print(query.as_dataframe())

.. _Time Series:
    https://cloud.google.com/monitoring/api/ref_v3/rest/v3/TimeSeries


Writing Custom Metrics
---------------------------

The Stackdriver Monitoring API can be used to write data points to custom metrics. Please refer to
the documentation on `Custom Metrics`_ for more information.

To write a data point to a custom metric, you must provide an instance of
:class:`~google.cloud.monitoring.metric.Metric` specifying the metric type as well as the values for
the metric labels. You will need to have either created the metric descriptor earlier (see the
`Metric Descriptors`_ section) or rely on metric type auto-creation (see `Auto-creation of
custom metrics`_).

You will also need to provide a :class:`~google.cloud.monitoring.resource.Resource` instance
specifying a monitored resource type as well as values for all of the monitored resource labels,
except for ``project_id``, which is ignored when it's included in writes to the API. A good
choice is to use the underlying physical resource where your application code runs – e.g., a
monitored resource type of ``gce_instance`` or ``aws_ec2_instance``. In some limited
circumstances, such as when only a single process writes to the custom metric, you may choose to
use the ``global`` monitored resource type.

See `Monitored resource types`_ for more information about particular monitored resource types.

.. code-block:: python

  >>> from google.cloud import monitoring
  >>> # Create a Resource object for the desired monitored resource type.
  >>> resource = client.resource(
  ...     'gce_instance',
  ...     labels={
  ...         'instance_id': '1234567890123456789',
  ...         'zone': 'us-central1-f'
  ...     }
  ... )
  >>> # Create a Metric object, specifying the metric type as well as values for any metric labels.
  >>> metric = client.metric(
  ...     type_='custom.googleapis.com/my_metric',
  ...     labels={
  ...         'status': 'successful'
  ...     }
  ... )

With a ``Metric`` and ``Resource`` in hand, the :class:`~google.cloud.monitoring.client.Client`
can be used to write :class:`~google.cloud.monitoring.timeseries.Point` values.

When writing points, the Python type of the value must match the *value type* of the metric
descriptor associated with the metric. For example, a Python float will map to ``ValueType.DOUBLE``.

Stackdriver Monitoring supports several *metric kinds*: ``GAUGE``, ``CUMULATIVE``, and ``DELTA``.
However, ``DELTA`` is not supported for custom metrics.

``GAUGE`` metrics represent only a single point in time, so only the ``end_time`` should be
specified:

.. code-block:: python

    >>> client.write_point(metric=metric, resource=resource,
    ...                    value=3.14, end_time=end_time)  # API call

By default, ``end_time`` defaults to :meth:`~datetime.datetime.utcnow()`, so metrics can be written
to the current time as follows:

.. code-block:: python

   >>> client.write_point(metric, resource, 3.14)  # API call

``CUMULATIVE`` metrics enable the monitoring system to compute rates of increase on metrics that
sometimes reset, such as after a process restart. Without cumulative metrics, this
reset would otherwise show up as a huge negative spike. For cumulative metrics, the same start
time should be re-used repeatedly as more points are written to the time series.

In the examples below, the ``end_time`` again defaults to the current time:

.. code-block:: python

    >>> RESET = datetime.utcnow()
    >>> client.write_point(metric, resource, 3, start_time=RESET)  # API call
    >>> client.write_point(metric, resource, 6, start_time=RESET)  # API call

To write multiple ``TimeSeries`` in a single batch, you can use
:meth:`~google.cloud.monitoring.client.write_time_series`:

.. code-block:: python

    >>> ts1 = client.time_series(metric1, resource, 3.14, end_time=end_time)
    >>> ts2 = client.time_series(metric2, resource, 42, end_time=end_time)
    >>> client.write_time_series([ts1, ts2])  # API call

While multiple time series can be written in a single batch, each ``TimeSeries`` object sent to
the API must only include a single point.

All timezone-naive Python ``datetime`` objects are assumed to be UTC.

.. _TimeSeries: https://cloud.google.com/monitoring/api/ref_v3/rest/v3/TimeSeries
.. _Custom Metrics: https://cloud.google.com/monitoring/custom-metrics/
.. _Auto-creation of custom metrics:
    https://cloud.google.com/monitoring/custom-metrics/creating-metrics#auto-creation
.. _Metrics: https://cloud.google.com/monitoring/api/v3/metrics
.. _Monitored resource types:
    https://cloud.google.com/monitoring/api/resources
