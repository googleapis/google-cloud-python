# Copyright 2016 Google LLC
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

"""Client for interacting with the `Google Stackdriver Monitoring API (V3)`_.

Example::

    >>> from google.cloud import monitoring
    >>> client = monitoring.Client()
    >>> query = client.query(minutes=5)
    >>> print(query.as_dataframe())  # Requires pandas.

At present, the client supports querying of time series, metric descriptors,
and monitored resource descriptors.

.. _Google Stackdriver Monitoring API (V3):
    https://cloud.google.com/monitoring/api/v3/
"""

import datetime

from google.cloud._helpers import _datetime_to_rfc3339
from google.cloud.client import ClientWithProject

from google.cloud.monitoring._http import Connection
from google.cloud.monitoring.group import Group
from google.cloud.monitoring.metric import Metric
from google.cloud.monitoring.metric import MetricDescriptor
from google.cloud.monitoring.metric import MetricKind
from google.cloud.monitoring.metric import ValueType
from google.cloud.monitoring.query import Query
from google.cloud.monitoring.resource import Resource
from google.cloud.monitoring.resource import ResourceDescriptor
from google.cloud.monitoring.timeseries import Point
from google.cloud.monitoring.timeseries import TimeSeries


_UTCNOW = datetime.datetime.utcnow  # To be replaced by tests.


class Client(ClientWithProject):
    """Client to bundle configuration needed for API requests.

    :type project: str
    :param project: The target project. If not passed, falls back to the
                    default inferred from the environment.

    :type credentials: :class:`~google.auth.credentials.Credentials`
    :param credentials: (Optional) The OAuth2 Credentials to use for this
                        client. If not passed (and if no ``_http`` object is
                        passed), falls back to the default inferred from the
                        environment.

    :type _http: :class:`~requests.Session`
    :param _http: (Optional) HTTP object to make requests. Can be any object
                  that defines ``request()`` with the same interface as
                  :meth:`requests.Session.request`. If not passed, an
                  ``_http`` object is created that is bound to the
                  ``credentials`` for the current object.
                  This parameter should be considered private, and could
                  change in the future.
    """

    SCOPE = ('https://www.googleapis.com/auth/monitoring.read',
             'https://www.googleapis.com/auth/monitoring',
             'https://www.googleapis.com/auth/cloud-platform')
    """The scopes required for authenticating as a Monitoring consumer."""

    def __init__(self, project=None, credentials=None, _http=None):
        super(Client, self).__init__(
            project=project, credentials=credentials, _http=_http)
        self._connection = Connection(self)

    def query(self,
              metric_type=Query.DEFAULT_METRIC_TYPE,
              end_time=None,
              days=0, hours=0, minutes=0):
        """Construct a query object for retrieving metric data.

        Example::

            >>> query = client.query(minutes=5)
            >>> print(query.as_dataframe())  # Requires pandas.

        :type metric_type: str
        :param metric_type: The metric type name. The default value is
            :data:`Query.DEFAULT_METRIC_TYPE
            <google.cloud.monitoring.query.Query.DEFAULT_METRIC_TYPE>`,
            but please note that this default value is provided only for
            demonstration purposes and is subject to change. See the
            `supported metrics`_.

        :type end_time: :class:`datetime.datetime`
        :param end_time:
            (Optional) The end time (inclusive) of the time interval
            for which results should be returned, as a datetime object.
            The default is the start of the current minute.

            The start time (exclusive) is determined by combining the
            values of  ``days``, ``hours``, and ``minutes``, and
            subtracting the resulting duration from the end time.

            It is also allowed to omit the end time and duration here,
            in which case
            :meth:`~google.cloud.monitoring.query.Query.select_interval`
            must be called before the query is executed.

        :type days: int
        :param days: The number of days in the time interval.

        :type hours: int
        :param hours: The number of hours in the time interval.

        :type minutes: int
        :param minutes: The number of minutes in the time interval.

        :rtype: :class:`~google.cloud.monitoring.query.Query`
        :returns: The query object.

        :raises: :exc:`ValueError` if ``end_time`` is specified but
            ``days``, ``hours``, and ``minutes`` are all zero.
            If you really want to specify a point in time, use
            :meth:`~google.cloud.monitoring.query.Query.select_interval`.

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
        descriptor
        :meth:`~google.cloud.monitoring.metric.MetricDescriptor.create`
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

        :type type_: str
        :param type_:
            The metric type including a DNS name prefix. For example:
            ``"custom.googleapis.com/my_metric"``

        :type metric_kind: str
        :param metric_kind:
            The kind of measurement. It must be one of
            :data:`MetricKind.GAUGE`, :data:`MetricKind.DELTA`,
            or :data:`MetricKind.CUMULATIVE`.
            See :class:`~google.cloud.monitoring.metric.MetricKind`.

        :type value_type: str
        :param value_type:
            The value type of the metric. It must be one of
            :data:`ValueType.BOOL`, :data:`ValueType.INT64`,
            :data:`ValueType.DOUBLE`, :data:`ValueType.STRING`,
            or :data:`ValueType.DISTRIBUTION`.
            See :class:`ValueType`.

        :type labels:
            list of :class:`~google.cloud.monitoring.label.LabelDescriptor`
        :param labels:
            A sequence of zero or more label descriptors specifying the labels
            used to identify a specific instance of this metric.

        :type unit: str
        :param unit: An optional unit in which the metric value is reported.

        :type description: str
        :param description: An optional detailed description of the metric.

        :type display_name: str
        :param display_name: An optional concise name for the metric.

        :rtype: :class:`MetricDescriptor`
        :returns: The metric descriptor created with the passed-in arguments.
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

    @staticmethod
    def metric(type_, labels):
        """Factory for constructing metric objects.

        :class:`~google.cloud.monitoring.metric.Metric` objects are typically
        created to write custom metric values. The type should match the
        metric type specified in the
        :class:`~google.cloud.monitoring.metric.MetricDescriptor` used to
        create the custom metric::

             >>> metric = client.metric('custom.googleapis.com/my_metric',
             ...                        labels={
             ...                            'status': 'successful',
             ...                         })

        :type type_: str
        :param type_: The metric type name.

        :type labels: dict
        :param labels: A mapping from label names to values for all labels
                       enumerated in the associated
                       :class:`~.metric.MetricDescriptor`.

        :rtype: :class:`~google.cloud.monitoring.metric.Metric`
        :returns: The metric object.
        """
        return Metric(type=type_, labels=labels)

    @staticmethod
    def resource(type_, labels):
        """Factory for constructing monitored resource objects.

        A monitored resource object (
        :class:`~google.cloud.monitoring.resource.Resource`) is
        typically used to create a
        :class:`~google.cloud.monitoring.timeseries.TimeSeries` object.

        For a list of possible monitored resource types and their associated
        labels, see:

        https://cloud.google.com/monitoring/api/resources

        :type type_: str
        :param type_: The monitored resource type name.

        :type labels: dict
        :param labels: A mapping from label names to values for all labels
                       enumerated in the associated
                       :class:`~.resource.ResourceDescriptor`,
                       except that ``project_id`` can and should be omitted
                       when writing time series data.

        :rtype: :class:`~google.cloud.monitoring.resource.Resource`
        :returns: A monitored resource object.
        """
        return Resource(type_, labels)

    @staticmethod
    def time_series(metric, resource, value,
                    end_time=None, start_time=None):
        """Construct a time series object for a single data point.

        .. note::

           While :class:`~google.cloud.monitoring.timeseries.TimeSeries`
           objects returned by the API typically have multiple data points,
           :class:`~google.cloud.monitoring.timeseries.TimeSeries` objects
           sent to the API must have at most one point.

        For example::

            >>> timeseries = client.time_series(metric, resource, 1.23,
            ...                                 end_time=end)

        For more information, see:

        https://cloud.google.com/monitoring/api/ref_v3/rest/v3/TimeSeries

        :type metric: :class:`~google.cloud.monitoring.metric.Metric`
        :param metric: A :class:`~google.cloud.monitoring.metric.Metric`.

        :type resource: :class:`~google.cloud.monitoring.resource.Resource`
        :param resource: A :class:`~google.cloud.monitoring.resource.Resource`
                         object.

        :type value: bool, int, string, or float
        :param value:
            The value of the data point to create for the
            :class:`~google.cloud.monitoring.timeseries.TimeSeries`.

            .. note::

               The Python type of the value will determine the
               :class:`~ValueType` sent to the API, which must match the value
               type specified in the metric descriptor. For example, a Python
               float will be sent to the API as a :data:`ValueType.DOUBLE`.

        :type end_time: :class:`~datetime.datetime`
        :param end_time:
            The end time for the point to be included in the time series.
            Assumed to be UTC if no time zone information is present.
            Defaults to the current time, as obtained by calling
            :meth:`datetime.datetime.utcnow`.

        :type start_time: :class:`~datetime.datetime`
        :param start_time:
            The start time for the point to be included in the time series.
            Assumed to be UTC if no time zone information is present.
            Defaults to None. If the start time is unspecified,
            the API interprets the start time to be the same as the end time.

        :rtype: :class:`~google.cloud.monitoring.timeseries.TimeSeries`
        :returns: A time series object.
        """
        if end_time is None:
            end_time = _UTCNOW()

        end_time = _datetime_to_rfc3339(end_time, ignore_zone=False)
        if start_time:
            start_time = _datetime_to_rfc3339(start_time, ignore_zone=False)

        point = Point(value=value, start_time=start_time, end_time=end_time)
        return TimeSeries(metric=metric, resource=resource, metric_kind=None,
                          value_type=None, points=[point])

    def fetch_metric_descriptor(self, metric_type):
        """Look up a metric descriptor by type.

        Example::

            >>> METRIC = 'compute.googleapis.com/instance/cpu/utilization'
            >>> print(client.fetch_metric_descriptor(METRIC))

        :type metric_type: str
        :param metric_type: The metric type name.

        :rtype: :class:`~google.cloud.monitoring.metric.MetricDescriptor`
        :returns: The metric descriptor instance.

        :raises: :class:`google.cloud.exceptions.NotFound` if the metric
                 descriptor is not found.
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

        :type filter_string: str
        :param filter_string:
            (Optional) An optional filter expression describing the metric
            descriptors to be returned. See the `filter documentation`_.

        :type type_prefix: str
        :param type_prefix:
            (Optional) An optional prefix constraining the selected metric
            types. This adds ``metric.type = starts_with("<prefix>")`` to the
            filter.

        :rtype:
            list of :class:`~google.cloud.monitoring.metric.MetricDescriptor`
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

        :type resource_type: str
        :param resource_type: The resource type name.

        :rtype: :class:`~google.cloud.monitoring.resource.ResourceDescriptor`
        :returns: The resource descriptor instance.

        :raises: :class:`google.cloud.exceptions.NotFound` if the resource
                 descriptor is not found.
        """
        return ResourceDescriptor._fetch(self, resource_type)

    def list_resource_descriptors(self, filter_string=None):
        """List all monitored resource descriptors for the project.

        Example::

            >>> for descriptor in client.list_resource_descriptors():
            ...     print(descriptor.type)

        :type filter_string: str
        :param filter_string:
            (Optional) An optional filter expression describing the resource
            descriptors to be returned. See the `filter documentation`_.

        :rtype: list of
                :class:`~google.cloud.monitoring.resource.ResourceDescriptor`
        :returns: A list of resource descriptor instances.

        .. _filter documentation:
            https://cloud.google.com/monitoring/api/v3/filters
        """
        return ResourceDescriptor._list(self, filter_string)

    def group(self, group_id=None, display_name=None, parent_id=None,
              filter_string=None, is_cluster=False):
        """Factory constructor for group object.

        .. note::
          This will not make an HTTP request; it simply instantiates
          a group object owned by this client.

        :type group_id: str
        :param group_id: (Optional) The ID of the group.

        :type display_name: str
        :param display_name:
            (Optional) A user-assigned name for this group, used only for
            display purposes.

        :type parent_id: str
        :param parent_id:
            (Optional) The ID of the group's parent, if it has one.

        :type filter_string: str
        :param filter_string:
            (Optional) The filter string used to determine which monitored
            resources belong to this group.

        :type is_cluster: bool
        :param is_cluster:
            If true, the members of this group are considered to be a cluster.
            The system can perform additional analysis on groups that are
            clusters.

        :rtype: :class:`Group`
        :returns: The group created with the passed-in arguments.

        :raises:
            :exc:`ValueError` if both ``group_id`` and ``name`` are specified.
        """
        return Group(
            self,
            group_id=group_id,
            display_name=display_name,
            parent_id=parent_id,
            filter_string=filter_string,
            is_cluster=is_cluster,
        )

    def fetch_group(self, group_id):
        """Fetch a group from the API based on it's ID.

        Example::

            >>> try:
            >>>     group = client.fetch_group('1234')
            >>> except google.cloud.exceptions.NotFound:
            >>>     print('That group does not exist!')

        :type group_id: str
        :param group_id: The ID of the group.

        :rtype: :class:`~google.cloud.monitoring.group.Group`
        :returns: The group instance.

        :raises: :class:`google.cloud.exceptions.NotFound` if the group
                 is not found.
        """
        return Group._fetch(self, group_id)

    def list_groups(self):
        """List all groups for the project.

        Example::

            >>> for group in client.list_groups():
            ...     print((group.display_name, group.name))

        :rtype: list of :class:`~google.cloud.monitoring.group.Group`
        :returns: A list of group instances.
        """
        return Group._list(self)

    def write_time_series(self, timeseries_list):
        """Write a list of time series objects to the API.

        The recommended approach to creating time series objects is using
        the :meth:`~google.cloud.monitoring.client.Client.time_series` factory
        method.

        Example::

            >>> client.write_time_series([ts1, ts2])

        If you only need to write a single time series object, consider using
        the :meth:`~google.cloud.monitoring.client.Client.write_point` method
        instead.

        :type timeseries_list:
            list of :class:`~google.cloud.monitoring.timeseries.TimeSeries`
        :param timeseries_list:
            A list of time series object to be written
            to the API. Each time series must contain exactly one point.
        """
        path = '/projects/{project}/timeSeries/'.format(
            project=self.project)
        timeseries_dict = [timeseries._to_dict()
                           for timeseries in timeseries_list]
        self._connection.api_request(method='POST', path=path,
                                     data={'timeSeries': timeseries_dict})

    def write_point(self, metric, resource, value,
                    end_time=None,
                    start_time=None):
        """Write a single point for a metric to the API.

        This is a convenience method to write a single time series object to
        the API. To write multiple time series objects to the API as a batch
        operation, use the
        :meth:`~google.cloud.monitoring.client.Client.time_series`
        factory method to create time series objects and the
        :meth:`~google.cloud.monitoring.client.Client.write_time_series`
        method to write the objects.

        Example::

            >>> client.write_point(metric, resource, 3.14)

        :type metric: :class:`~google.cloud.monitoring.metric.Metric`
        :param metric: A :class:`~google.cloud.monitoring.metric.Metric`
                       object.

        :type resource: :class:`~google.cloud.monitoring.resource.Resource`
        :param resource: A :class:`~google.cloud.monitoring.resource.Resource`
                         object.

        :type value: bool, int, string, or float
        :param value:
            The value of the data point to create for the
            :class:`~google.cloud.monitoring.timeseries.TimeSeries`.

            .. note::

               The Python type of the value will determine the
               :class:`~ValueType` sent to the API, which must match the value
               type specified in the metric descriptor. For example, a Python
               float will be sent to the API as a :data:`ValueType.DOUBLE`.

        :type end_time: :class:`~datetime.datetime`
        :param end_time:
            The end time for the point to be included in the time series.
            Assumed to be UTC if no time zone information is present.
            Defaults to the current time, as obtained by calling
            :meth:`datetime.datetime.utcnow`.

        :type start_time: :class:`~datetime.datetime`
        :param start_time:
            The start time for the point to be included in the time series.
            Assumed to be UTC if no time zone information is present.
            Defaults to None. If the start time is unspecified,
            the API interprets the start time to be the same as the end time.
        """
        timeseries = self.time_series(
            metric, resource, value, end_time, start_time)
        self.write_time_series([timeseries])
