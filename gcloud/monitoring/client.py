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

.. _Google Monitoring API (V3): https://cloud.google.com/monitoring/api/
"""

from gcloud.client import JSONClient
from gcloud.monitoring.connection import Connection
from gcloud.monitoring.metric import MetricDescriptor
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
        """Construct a query object for listing time series.

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

    def list_metric_descriptors(self, filter_string=None):
        """List all metric descriptors for the project.

        Example::

            >>> for descriptor in client.list_metric_descriptors():
            ...     print(descriptor.type)

        :type filter_string: string or None
        :param filter_string:
            An optional filter expression describing the metric descriptors
            to be returned. See the `filter documentation`_.

        :rtype: list of :class:`~gcloud.monitoring.metric.MetricDescriptor`
        :returns: A list of metric descriptor instances.

        .. _filter documentation:
            https://cloud.google.com/monitoring/api/v3/filters
        """
        return MetricDescriptor._list(self, filter_string)

    def fetch_resource_descriptor(self, resource_type):
        """Look up a resource descriptor by type.

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
        """List all resource descriptors for the project.

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
