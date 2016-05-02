# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Client for interacting with the `Google Monitoring API (V3)`_.

Example::

    >>> from gcloud import monitoring
    >>> client = monitoring.Client()
    >>> query = client.query(minutes=5)
    >>> print(query.as_dataframe())  # Requires pandas.

At present, the client supports querying of time series, metric descriptors,
and monitored resource descriptors.

.. _Google Monitoring API (V3): https://cloud.google.com/monitoring/api/v3/
"""

from gcloud.client import JSONClient
from gcloud.monitoring.connection import Connection
from gcloud.monitoring.metric import MetricDescriptor
from gcloud.monitoring.metric import MetricKind
from gcloud.monitoring.metric import ValueType
from gcloud.monitoring.query import Query
from gcloud.monitoring.resource import ResourceDescriptor


class Client(JSONClient):
    """Client to bundle configuration needed for API requests.

    :type project: string
    :param project: The target project. If not passed, falls back to the
                    default inferred from the environment.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials` or
                       :class:`NoneType`
    :param credentials: The OAuth2 Credentials to use for the connection
                        owned by this client. If not passed (and if no ``http``
                        object is passed), falls back to the default inferred
                        from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``
    :param http: An optional HTTP object to make requests. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.
    """

    _connection_class = Connection

    def query(self,
              metric_type=Query.DEFAULT_METRIC_TYPE,
              end_time=None,
              days=0, hours=0, minutes=0):
        """Construct a query object for retrieving metric data.

        Example::

            >>> query = client.query(minutes=5)
            >>> print(query.as_dataframe())  # Requires pandas.

        :type metric_type: string
        :param metric_type: The metric type name. The default value is
            :data:`Query.DEFAULT_METRIC_TYPE
            <gcloud.monitoring.query.Query.DEFAULT_METRIC_TYPE>`,
            but please note that this default value is provided only for
            demonstration purposes and is subject to change. See the
            `supported metrics`_.

        :type end_time: :class:`datetime.datetime` or None
        :param end_time: The end time (inclusive) of the time interval
            for which results should be returned, as a datetime object.
            The default is the start of the current minute.

            The start time (exclusive) is determined by combining the
            values of  ``days``, ``hours``, and ``minutes``, and
            subtracting the resulting duration from the end time.

            It is also allowed to omit the end time and duration here,
            in which case
            :meth:`~gcloud.monitoring.query.Query.select_interval`
            must be called before the query is executed.

        :type days: integer
        :param days: The number of days in the time interval.

        :type hours: integer
        :param hours: The number of hours in the time interval.

        :type minutes: integer
        :param minutes: The number of minutes in the time interval.

        :rtype: :class:`~gcloud.monitoring.query.Query`
        :returns: The query object.

        :raises: :exc:`ValueError` if ``end_time`` is specified but
            ``days``, ``hours``, and ``minutes`` are all zero.
            If you really want to specify a point in time, use
            :meth:`~gcloud.monitoring.query.Query.select_interval`.

        .. _supported metrics: https://cloud.google.com/monitoring/api/metrics
        """
        return Query(self, metric_type,
                     end_time=end_time,
                     days=days, hours=hours, minutes=minutes)

    def metric_descriptor(self, type_,
                          metric_kind=MetricKind.METRIC_KIND_UNSPECIFIED,
                          value_type=ValueType.VALUE_TYPE_UNSPECIFIED,
                          labels=(), unit='', description='', display_name=''):
        """Construct a metric descriptor object.

        Metric descriptors specify the schema for a particular metric type.

        This factory method is used most often in conjunction with the metric
        descriptor :meth:`~gcloud.monitoring.metric.MetricDescriptor.create`
        method to define custom metrics::

            >>> descriptor = client.metric_descriptor(
            ...     'custom.googleapis.com/my_metric',
            ...     metric_kind=MetricKind.GAUGE,
            ...     value_type=ValueType.DOUBLE,
            ...     description='This is a simple example of a custom metric.')
            >>> descriptor.create()

        Here is an example where the custom metric is parameterized by a
        metric label::

            >>> label = LabelDescriptor('response_code', LabelValueType.INT64,
            ...                         description='HTTP status code')
            >>> descriptor = client.metric_descriptor(
            ...     'custom.googleapis.com/my_app/response_count',
            ...     metric_kind=MetricKind.CUMULATIVE,
            ...     value_type=ValueType.INT64,
            ...     labels=[label],
            ...     description='Cumulative count of HTTP responses.')
            >>> descriptor.create()

        :type type_: string
        :param type_:
            The metric type including a DNS name prefix. For example:
            ``"custom.googleapis.com/my_metric"``

        :type metric_kind: string
        :param metric_kind:
            The kind of measurement. It must be one of
            :data:`MetricKind.GAUGE`, :data:`MetricKind.DELTA`,
            or :data:`MetricKind.CUMULATIVE`.
            See :class:`~gcloud.monitoring.metric.MetricKind`.

        :type value_type: string
        :param value_type:
            The value type of the metric. It must be one of
            :data:`ValueType.BOOL`, :data:`ValueType.INT64`,
            :data:`ValueType.DOUBLE`, :data:`ValueType.STRING`,
            or :data:`ValueType.DISTRIBUTION`.
            See :class:`ValueType`.

        :type labels: list of :class:`~gcloud.monitoring.label.LabelDescriptor`
        :param labels:
            A sequence of zero or more label descriptors specifying the labels
            used to identify a specific instance of this metric.

        :type unit: string
        :param unit: An optional unit in which the metric value is reported.

        :type description: string
        :param description: An optional detailed description of the metric.

        :type display_name: string
        :param display_name: An optional concise name for the metric.
        """
        return MetricDescriptor(
            self, type_,
            metric_kind=metric_kind,
            value_type=value_type,
            labels=labels,
            unit=unit,
            description=description,
            display_name=display_name,
        )

    def fetch_metric_descriptor(self, metric_type):
        """Look up a metric descriptor by type.

        Example::

            >>> METRIC = 'compute.googleapis.com/instance/cpu/utilization'
            >>> print(client.fetch_metric_descriptor(METRIC))

        :type metric_type: string
        :param metric_type: The metric type name.

        :rtype: :class:`~gcloud.monitoring.metric.MetricDescriptor`
        :returns: The metric descriptor instance.

        :raises: :class:`gcloud.exceptions.NotFound` if the metric descriptor
            is not found.
        """
        return MetricDescriptor._fetch(self, metric_type)

    def list_metric_descriptors(self, filter_string=None, type_prefix=None):
        """List all metric descriptors for the project.

        Examples::

            >>> for descriptor in client.list_metric_descriptors():
            ...     print(descriptor.type)

            >>> for descriptor in client.list_metric_descriptors(
            ...         type_prefix='custom.'):
            ...     print(descriptor.type)

        :type filter_string: string or None
        :param filter_string:
            An optional filter expression describing the metric descriptors
            to be returned. See the `filter documentation`_.

        :type type_prefix: string or None
        :param type_prefix: An optional prefix constraining the selected
            metric types. This adds ``metric.type = starts_with("<prefix>")``
            to the filter.

        :rtype: list of :class:`~gcloud.monitoring.metric.MetricDescriptor`
        :returns: A list of metric descriptor instances.

        .. _filter documentation:
            https://cloud.google.com/monitoring/api/v3/filters
        """
        return MetricDescriptor._list(self, filter_string,
                                      type_prefix=type_prefix)

    def fetch_resource_descriptor(self, resource_type):
        """Look up a monitored resource descriptor by type.

        Example::

            >>> print(client.fetch_resource_descriptor('gce_instance'))

        :type resource_type: string
        :param resource_type: The resource type name.

        :rtype: :class:`~gcloud.monitoring.resource.ResourceDescriptor`
        :returns: The resource descriptor instance.

        :raises: :class:`gcloud.exceptions.NotFound` if the resource descriptor
            is not found.
        """
        return ResourceDescriptor._fetch(self, resource_type)

    def list_resource_descriptors(self, filter_string=None):
        """List all monitored resource descriptors for the project.

        Example::

            >>> for descriptor in client.list_resource_descriptors():
            ...     print(descriptor.type)

        :type filter_string: string or None
        :param filter_string:
            An optional filter expression describing the resource descriptors
            to be returned. See the `filter documentation`_.

        :rtype: list of :class:`~gcloud.monitoring.resource.ResourceDescriptor`
        :returns: A list of resource descriptor instances.

        .. _filter documentation:
            https://cloud.google.com/monitoring/api/v3/filters
        """
        return ResourceDescriptor._list(self, filter_string)
