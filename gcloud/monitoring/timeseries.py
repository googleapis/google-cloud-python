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

"""Time series for the `Google Stackdriver Monitoring API (V3)`_.

Features intentionally omitted from this first version of the client library:
  * Writing time series.
  * Natural representation of distribution values.

.. _Google Stackdriver Monitoring API (V3):
    https://cloud.google.com/monitoring/api/ref_v3/rest/v3/TimeSeries
"""

import collections

from gcloud.monitoring.metric import Metric
from gcloud.monitoring.resource import Resource


class TimeSeries(collections.namedtuple(
        'TimeSeries', 'metric resource metric_kind value_type points')):
    """A single time series of metric values.

    :type metric: :class:`~gcloud.monitoring.metric.Metric`
    :param metric: A metric object.

    :type resource: :class:`~gcloud.monitoring.resource.Resource`
    :param resource: A resource object.

    :type metric_kind: string
    :param metric_kind:
        The kind of measurement: :data:`MetricKind.GAUGE`,
        :data:`MetricKind.DELTA`, or :data:`MetricKind.CUMULATIVE`.
        See :class:`~gcloud.monitoring.metric.MetricKind`.

    :type value_type: string
    :param value_type:
        The value type of the metric: :data:`ValueType.BOOL`,
        :data:`ValueType.INT64`, :data:`ValueType.DOUBLE`,
        :data:`ValueType.STRING`, or :data:`ValueType.DISTRIBUTION`.
        See :class:`~gcloud.monitoring.metric.ValueType`.

    :type points: list of :class:`Point`
    :param points: A list of point objects.
    """

    _labels = None

    @property
    def labels(self):
        """A single dictionary with values for all the labels.

        This combines ``resource.labels`` and ``metric.labels`` and also
        adds ``"resource_type"``.
        """
        if self._labels is None:
            labels = {'resource_type': self.resource.type}
            labels.update(self.resource.labels)
            labels.update(self.metric.labels)
            self._labels = labels

        return self._labels

    def header(self, points=None):
        """Copy everything but the point data.

        :type points: list of :class:`Point`, or None
        :param points: An optional point list.

        :rtype: :class:`TimeSeries`
        :returns: The new time series object.
        """
        points = list(points) if points else []
        return self._replace(points=points)

    @classmethod
    def _from_dict(cls, info):
        """Construct a time series from the parsed JSON representation.

        :type info: dict
        :param info:
            A ``dict`` parsed from the JSON wire-format representation.

        :rtype: :class:`TimeSeries`
        :returns: A time series object.
        """
        metric = Metric._from_dict(info['metric'])
        resource = Resource._from_dict(info['resource'])
        metric_kind = info['metricKind']
        value_type = info['valueType']
        points = [Point._from_dict(p) for p in info.get('points', ())]
        return cls(metric, resource, metric_kind, value_type, points)

    def __repr__(self):
        """Return a representation string with the points elided."""
        return (
            '<TimeSeries with {num} points:\n'
            ' metric={metric!r},\n'
            ' resource={resource!r},\n'
            ' metric_kind={kind!r}, value_type={type!r}>'
        ).format(
            num=len(self.points),
            metric=self.metric,
            resource=self.resource,
            kind=self.metric_kind,
            type=self.value_type,
        )


class Point(collections.namedtuple('Point', 'end_time start_time value')):
    """A single point in a time series.

    :type end_time: string
    :param end_time: The end time in RFC3339 UTC "Zulu" format.

    :type start_time: string or None
    :param start_time: An optional start time in RFC3339 UTC "Zulu" format.

    :type value: object
    :param value: The metric value. This can be a scalar or a distribution.
    """
    __slots__ = ()

    @classmethod
    def _from_dict(cls, info):
        """Construct a Point from the parsed JSON representation.

        :type info: dict
        :param info:
            A ``dict`` parsed from the JSON wire-format representation.

        :rtype: :class:`Point`
        :returns: A point object.
        """
        end_time = info['interval']['endTime']
        start_time = info['interval'].get('startTime')
        (value_type, value), = info['value'].items()
        if value_type == 'int64Value':
            value = int(value)  # Convert from string.

        return cls(end_time, start_time, value)
