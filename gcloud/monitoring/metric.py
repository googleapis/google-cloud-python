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

"""Metric Descriptors for the Google Monitoring API."""

# Features intentionally omitted from this first version of the client library:
#   - Creating and deleting metric descriptors.

import collections

from gcloud.monitoring.label import LabelDescriptor


class MetricDescriptor(collections.namedtuple(
        'MetricDescriptor', ('name type labels metric_kind value_type unit'
                             ' description display_name'))):
    """Specification of a metric type and its schema.

    Metric descriptor instances are immutable.

    :type name: string
    :param name: The "resource name" of the metric descriptor. For example:
                 ``"projects/<project_id>/metricDescriptors/<type>"``

    :type type: string
    :param type: The metric type including a DNS name prefix. For example:
                 ``"compute.googleapis.com/instance/cpu/utilization"``

    :type labels: list of :class:`~gcloud.monitoring.label.LabelDescriptor`
    :param labels: A sequence of label descriptors specifying the labels used
                   to identify a specific instance of this metric.

    :type metric_kind: string
    :param metric_kind: The kind of measurement. It must be one of ``"GAUGE"``,
                        ``"DELTA"``, or ``"CUMULATIVE"``.

    :type value_type: string
    :param value_type: The value type of the metric. It must be one of
                       ``"BOOL"``, ``"INT64"``, ``"DOUBLE"``, ``"STRING"``,
                       ``"DISTRIBUTION"``, or ``"MONEY"``.

    :type unit: string
    :param unit: The unit in which the metric value is reported.

    :type description: string
    :param description: A detailed description of the metric.

    :type display_name: string
    :param display_name: A concise name for the metric.
    """
    __slots__ = ()

    @classmethod
    def _fetch(cls, client, metric_type):
        """Look up a metric descriptor by type.

        :type client: :class:`gcloud.monitoring.client.Client`
        :param client: The client to use.

        :type metric_type: string
        :param metric_type: The metric type name.

        :rtype: :class:`MetricDescriptor`
        :returns: The metric descriptor instance.

        :raises: :class:`gcloud.exceptions.NotFound`
        """
        path = '/projects/{project}/metricDescriptors/{type}'.format(
            project=client.project,
            type=metric_type)
        info = client.connection.api_request('GET', path)
        return cls._from_dict(info)

    @classmethod
    def _list(cls, client, filter=None):
        """List all metric descriptors for the project.

        :type client: :class:`gcloud.monitoring.client.Client`
        :param client: The client to use.

        :type filter: string or None
        :param filter: An optional filter string describing the metric
                       descriptors to be returned.

        :rtype: list of :class:`MetricDescriptor`
        :returns: A list of metric descriptor instances.
        """
        # Allow "filter" as a parameter name: pylint: disable=redefined-builtin

        path = '/projects/{}/metricDescriptors/'.format(client.project)

        def _descriptors():
            page_token = None
            while True:
                params = {}

                if filter is not None:
                    params['filter'] = filter

                if page_token is not None:
                    params['pageToken'] = page_token

                response = client.connection.api_request('GET', path,
                                                         query_params=params)
                for info in response.get('metricDescriptors', []):
                    yield cls._from_dict(info)

                page_token = response.get('nextPageToken')
                if not page_token:
                    break

        return list(_descriptors())

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
            type=info.get('type', ''),
            name=info.get('name', ''),
            description=info.get('description', ''),
            display_name=info.get('displayName', ''),
            labels=tuple(LabelDescriptor._from_dict(label)
                         for label in info.get('labels', [])),
            metric_kind=info['metricKind'],
            value_type=info['valueType'],
            unit=info.get('unit', ''),
        )


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
            type=info.get('type', ''),
            labels=info.get('labels', {}),
        )
