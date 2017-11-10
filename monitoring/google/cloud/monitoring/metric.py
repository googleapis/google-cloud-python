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

"""Metric Descriptors for the `Google Stackdriver Monitoring API (V3)`_.

.. _Google Stackdriver Monitoring API (V3):
    https://cloud.google.com/monitoring/api/ref_v3/rest/v3/\
    projects.metricDescriptors
"""

import collections

from google.cloud.monitoring.label import LabelDescriptor


class MetricKind(object):
    """Choices for the `kind of measurement`_.

    .. _kind of measurement:
        https://cloud.google.com/monitoring/api/ref_v3/rest/v3/\
        projects.metricDescriptors#MetricKind
    """

    METRIC_KIND_UNSPECIFIED = 'METRIC_KIND_UNSPECIFIED'
    """.. note:: An unspecified kind is not allowed in metric descriptors."""

    GAUGE = 'GAUGE'
    DELTA = 'DELTA'
    CUMULATIVE = 'CUMULATIVE'


class ValueType(object):
    """Choices for the `metric value type`_.

    .. _metric value type:
        https://cloud.google.com/monitoring/api/ref_v3/rest/v3/\
        projects.metricDescriptors#ValueType
    """

    VALUE_TYPE_UNSPECIFIED = 'VALUE_TYPE_UNSPECIFIED'
    """.. note:: An unspecified type is not allowed in metric descriptors."""

    BOOL = 'BOOL'
    INT64 = 'INT64'
    DOUBLE = 'DOUBLE'
    STRING = 'STRING'
    DISTRIBUTION = 'DISTRIBUTION'


class MetricDescriptor(object):
    """Specification of a metric type and its schema.

    The preferred way to construct a metric descriptor object is using the
    :meth:`~google.cloud.monitoring.client.Client.metric_descriptor` factory
    method of the :class:`~google.cloud.monitoring.client.Client` class.

    :type client: :class:`google.cloud.monitoring.client.Client`
    :param client: A client for operating on the metric descriptor.

    :type type_: str
    :param type_:
        The metric type including a DNS name prefix. For example:
        ``"compute.googleapis.com/instance/cpu/utilization"``

    :type metric_kind: str
    :param metric_kind:
        The kind of measurement. It must be one of
        :data:`MetricKind.GAUGE`, :data:`MetricKind.DELTA`,
        or :data:`MetricKind.CUMULATIVE`. See :class:`MetricKind`.

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

    :type name: str
    :param name:
        (Optional) The "resource name" of the metric descriptor. For example:
        ``"projects/<project_id>/metricDescriptors/<type>"``. As
        retrieved from the service, this will always be specified.
        You can and should omit it when constructing an instance for
        the purpose of creating a new metric descriptor.
    """

    def __init__(self, client, type_,
                 metric_kind=MetricKind.METRIC_KIND_UNSPECIFIED,
                 value_type=ValueType.VALUE_TYPE_UNSPECIFIED,
                 labels=(),
                 unit='', description='', display_name='',
                 name=None):
        self.client = client
        self.name = name
        self.type = type_
        self.labels = labels
        self.metric_kind = metric_kind
        self.value_type = value_type
        self.unit = unit
        self.description = description
        self.display_name = display_name

    def create(self):
        """Create a new metric descriptor based on this object.

        Example::

            >>> descriptor = client.metric_descriptor(
            ...     'custom.googleapis.com/my_metric',
            ...     metric_kind=MetricKind.GAUGE,
            ...     value_type=ValueType.DOUBLE,
            ...     description='This is a simple example of a custom metric.')
            >>> descriptor.create()

        The metric kind must not be :data:`MetricKind.METRIC_KIND_UNSPECIFIED`,
        and the value type must not be
        :data:`ValueType.VALUE_TYPE_UNSPECIFIED`.

        The ``name`` attribute is ignored in preparing the creation request.
        All attributes are overwritten by the values received in the response
        (normally affecting only ``name``).
        """
        path = '/projects/{project}/metricDescriptors/'.format(
            project=self.client.project)
        response = self.client._connection.api_request(
            method='POST', path=path, data=self._to_dict())
        self._init_from_dict(response)

    def delete(self):
        """Delete the metric descriptor identified by this object.

        Example::

            >>> descriptor = client.metric_descriptor(
            ...     'custom.googleapis.com/my_metric')
            >>> descriptor.delete()

        Only the ``client`` and ``type`` attributes are used.
        """
        path = '/projects/{project}/metricDescriptors/{type}'.format(
            project=self.client.project,
            type=self.type)
        self.client._connection.api_request(method='DELETE', path=path)

    @classmethod
    def _fetch(cls, client, metric_type):
        """Look up a metric descriptor by type.

        :type client: :class:`google.cloud.monitoring.client.Client`
        :param client: The client to use.

        :type metric_type: str
        :param metric_type: The metric type name.

        :rtype: :class:`MetricDescriptor`
        :returns: The metric descriptor instance.

        :raises: :class:`google.cloud.exceptions.NotFound` if the metric
                 descriptor is not found.
        """
        path = '/projects/{project}/metricDescriptors/{type}'.format(
            project=client.project,
            type=metric_type)
        info = client._connection.api_request(method='GET', path=path)
        return cls._from_dict(client, info)

    @classmethod
    def _list(cls, client, filter_string=None, type_prefix=None):
        """List all metric descriptors for the project.

        :type client: :class:`google.cloud.monitoring.client.Client`
        :param client: The client to use.

        :type filter_string: str
        :param filter_string:
            (Optional) Filter expression describing the metric descriptors to
            be returned. See the `filter documentation`_.

        :type type_prefix: str
        :param type_prefix:
            (Optional) Prefix constraining the selected metric types. This adds
            ``metric.type = starts_with("<prefix>")`` to the filter.

        :rtype: list of :class:`MetricDescriptor`
        :returns: A list of metric descriptor instances.

        .. _filter documentation:
            https://cloud.google.com/monitoring/api/v3/filters
        """
        path = '/projects/{project}/metricDescriptors/'.format(
            project=client.project)

        filters = []
        if filter_string is not None:
            filters.append(filter_string)

        if type_prefix is not None:
            filters.append('metric.type = starts_with("{prefix}")'.format(
                prefix=type_prefix))

        descriptors = []
        page_token = None
        while True:
            params = {}

            if filters:
                params['filter'] = ' AND '.join(filters)

            if page_token is not None:
                params['pageToken'] = page_token

            response = client._connection.api_request(
                method='GET', path=path, query_params=params)
            for info in response.get('metricDescriptors', ()):
                descriptors.append(cls._from_dict(client, info))

            page_token = response.get('nextPageToken')
            if not page_token:
                break

        return descriptors

    @classmethod
    def _from_dict(cls, client, info):
        """Construct a metric descriptor from the parsed JSON representation.

        :type client: :class:`google.cloud.monitoring.client.Client`
        :param client: A client to be included in the returned object.

        :type info: dict
        :param info:
            A ``dict`` parsed from the JSON wire-format representation.

        :rtype: :class:`MetricDescriptor`
        :returns: A metric descriptor.
        """
        descriptor = cls(client, None)
        descriptor._init_from_dict(info)
        return descriptor

    def _init_from_dict(self, info):
        """Initialize attributes from the parsed JSON representation.

        :type info: dict
        :param info:
            A ``dict`` parsed from the JSON wire-format representation.
        """
        self.name = info['name']
        self.type = info['type']
        self.labels = tuple(LabelDescriptor._from_dict(label)
                            for label in info.get('labels', []))
        self.metric_kind = info['metricKind']
        self.value_type = info['valueType']
        self.unit = info.get('unit', '')
        self.description = info.get('description', '')
        self.display_name = info.get('displayName', '')

    def _to_dict(self):
        """Build a dictionary ready to be serialized to the JSON wire format.

        :rtype: dict
        :returns: A dictionary.
        """
        info = {
            'type': self.type,
            'metricKind': self.metric_kind,
            'valueType': self.value_type,
        }

        if self.labels:
            info['labels'] = [label._to_dict() for label in self.labels]
        if self.unit:
            info['unit'] = self.unit
        if self.description:
            info['description'] = self.description
        if self.display_name:
            info['displayName'] = self.display_name

        return info

    def __repr__(self):
        return (
            '<MetricDescriptor:\n'
            ' name={name!r},\n'
            ' type={type!r},\n'
            ' metric_kind={metric_kind!r}, value_type={value_type!r},\n'
            ' labels={labels!r},\n'
            ' display_name={display_name!r}, unit={unit!r},\n'
            ' description={description!r}>'
        ).format(**self.__dict__)


class Metric(collections.namedtuple('Metric', 'type labels')):
    """A specific metric identified by specifying values for all labels.

    The preferred way to construct a metric object is using the
    :meth:`~google.cloud.monitoring.client.Client.metric` factory method
    of the :class:`~google.cloud.monitoring.client.Client` class.

    :type type: str
    :param type: The metric type name.

    :type labels: dict
    :param labels: A mapping from label names to values for all labels
                   enumerated in the associated :class:`MetricDescriptor`.
    """
    __slots__ = ()

    @classmethod
    def _from_dict(cls, info):
        """Construct a metric object from the parsed JSON representation.

        :type info: dict
        :param info:
            A ``dict`` parsed from the JSON wire-format representation.

        :rtype: :class:`Metric`
        :returns: A metric object.
        """
        return cls(
            type=info['type'],
            labels=info.get('labels', {}),
        )

    def _to_dict(self):
        """Build a dictionary ready to be serialized to the JSON format.

        :rtype: dict
        :returns: A dict representation of the object that can be written to
                  the API.
        """
        return {
            'type': self.type,
            'labels': self.labels,
        }
