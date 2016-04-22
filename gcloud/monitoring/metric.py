# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Metric Descriptors for the `Google Monitoring API (V3)`_.

Features intentionally omitted from this first version of the client library:
  * Creating and deleting metric descriptors.

.. _Google Monitoring API (V3):
    https://cloud.google.com/monitoring/api/ref_v3/rest/v3/\
    projects.metricDescriptors
"""

import collections

from gcloud.monitoring.label import LabelDescriptor


class MetricKind(object):
    """Allowed values for the `kind of measurement`_.

    .. _kind of measurement:
        https://cloud.google.com/monitoring/api/ref_v3/rest/v3/\
        projects.metricDescriptors#MetricKind
    """

    GAUGE = 'GAUGE'
    DELTA = 'DELTA'
    CUMULATIVE = 'CUMULATIVE'


class ValueType(object):
    """Allowed values for the `metric value type`_.

    .. _metric value type:
        https://cloud.google.com/monitoring/api/ref_v3/rest/v3/\
        projects.metricDescriptors#ValueType
    """

    BOOL = 'BOOL'
    INT64 = 'INT64'
    DOUBLE = 'DOUBLE'
    STRING = 'STRING'
    DISTRIBUTION = 'DISTRIBUTION'
    MONEY = 'MONEY'


class MetricDescriptor(object):
    """Specification of a metric type and its schema.

    :type name: string
    :param name:
        The "resource name" of the metric descriptor. For example:
        ``"projects/<project_id>/metricDescriptors/<type>"``

    :type type_: string
    :param type_:
        The metric type including a DNS name prefix. For example:
        ``"compute.googleapis.com/instance/cpu/utilization"``

    :type labels: list of :class:`~gcloud.monitoring.label.LabelDescriptor`
    :param labels:
        A sequence of label descriptors specifying the labels used to
        identify a specific instance of this metric.

    :type metric_kind: string
    :param metric_kind:
        The kind of measurement. It must be one of :data:`MetricKind.GAUGE`,
        :data:`MetricKind.DELTA`, or :data:`MetricKind.CUMULATIVE`.
        See :class:`MetricKind`.

    :type value_type: string
    :param value_type:
        The value type of the metric. It must be one of :data:`ValueType.BOOL`,
        :data:`ValueType.INT64`, :data:`ValueType.DOUBLE`,
        :data:`ValueType.STRING`, :data:`ValueType.DISTRIBUTION`,
        or :data:`ValueType.MONEY`.
        See :class:`ValueType`.

    :type unit: string
    :param unit: The unit in which the metric value is reported.

    :type description: string
    :param description: A detailed description of the metric.

    :type display_name: string
    :param display_name: A concise name for the metric.
    """

    def __init__(self, name, type_, labels, metric_kind, value_type,
                 unit, description, display_name):
        self.name = name
        self.type = type_
        self.labels = labels
        self.metric_kind = metric_kind
        self.value_type = value_type
        self.unit = unit
        self.description = description
        self.display_name = display_name

    @classmethod
    def _fetch(cls, client, metric_type):
        """Look up a metric descriptor by type.

        :type client: :class:`gcloud.monitoring.client.Client`
        :param client: The client to use.

        :type metric_type: string
        :param metric_type: The metric type name.

        :rtype: :class:`MetricDescriptor`
        :returns: The metric descriptor instance.

        :raises: :class:`gcloud.exceptions.NotFound` if the metric descriptor
            is not found.
        """
        path = '/projects/{project}/metricDescriptors/{type}'.format(
            project=client.project,
            type=metric_type)
        info = client.connection.api_request(method='GET', path=path)
        return cls._from_dict(info)

    @classmethod
    def _list(cls, client, filter_string=None):
        """List all metric descriptors for the project.

        :type client: :class:`gcloud.monitoring.client.Client`
        :param client: The client to use.

        :type filter_string: string or None
        :param filter_string:
            An optional filter expression describing the metric descriptors
            to be returned. See the `filter documentation`_.

        :rtype: list of :class:`MetricDescriptor`
        :returns: A list of metric descriptor instances.

        .. _filter documentation:
            https://cloud.google.com/monitoring/api/v3/filters
        """
        path = '/projects/{project}/metricDescriptors/'.format(
            project=client.project)

        descriptors = []

        page_token = None
        while True:
            params = {}

            if filter_string is not None:
                params['filter'] = filter_string

            if page_token is not None:
                params['pageToken'] = page_token

            response = client.connection.api_request(
                method='GET', path=path, query_params=params)
            for info in response.get('metricDescriptors', ()):
                descriptors.append(cls._from_dict(info))

            page_token = response.get('nextPageToken')
            if not page_token:
                break

        return descriptors

    @classmethod
    def _from_dict(cls, info):
        """Construct a metric descriptor from the parsed JSON representation.

        :type info: dict
        :param info:
            A ``dict`` parsed from the JSON wire-format representation.

        :rtype: :class:`MetricDescriptor`
        :returns: A metric descriptor.
        """
        return cls(
            name=info['name'],
            type_=info['type'],
            labels=tuple(LabelDescriptor._from_dict(label)
                         for label in info.get('labels', ())),
            metric_kind=info['metricKind'],
            value_type=info['valueType'],
            unit=info.get('unit', ''),
            description=info.get('description', ''),
            display_name=info.get('displayName', ''),
        )

    def __repr__(self):
        return (
            'MetricDescriptor(\n'
            ' name={name!r},\n'
            ' type={type!r},\n'
            ' metric_kind={metric_kind!r}, value_type={value_type!r},\n'
            ' labels={labels!r},\n'
            ' display_name={display_name!r}, unit={unit!r},\n'
            ' description={description!r})'
        ).format(**self.__dict__)


class Metric(collections.namedtuple('Metric', 'type labels')):
    """A specific metric identified by specifying values for all labels.

    :type type: string
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
