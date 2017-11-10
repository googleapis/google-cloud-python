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

"""Time series for the `Google Stackdriver Monitoring API (V3)`_.

Features intentionally omitted from this first version of the client library:
  * Writing time series.
  * Natural representation of distribution values.

.. _Google Stackdriver Monitoring API (V3):
    https://cloud.google.com/monitoring/api/ref_v3/rest/v3/TimeSeries
"""

import collections

from google.cloud.monitoring.metric import Metric
from google.cloud.monitoring.resource import Resource


class TimeSeries(collections.namedtuple(
        'TimeSeries', 'metric resource metric_kind value_type points')):
    """A single time series of metric values.

    The preferred way to construct a
    :class:`~google.cloud.monitoring.timeseries.TimeSeries` object is
    using the :meth:`~google.cloud.monitoring.client.Client.time_series`
    factory method of the :class:`~google.cloud.monitoring.client.Client`
    class.

    :type metric: :class:`~google.cloud.monitoring.metric.Metric`
    :param metric: A metric object.

    :type resource: :class:`~google.cloud.monitoring.resource.Resource`
    :param resource: A resource object.

    :type metric_kind: str
    :param metric_kind:
        The kind of measurement: :data:`MetricKind.GAUGE`,
        :data:`MetricKind.DELTA`, or :data:`MetricKind.CUMULATIVE`.
        See :class:`~google.cloud.monitoring.metric.MetricKind`.

    :type value_type: str
    :param value_type:
        The value type of the metric: :data:`ValueType.BOOL`,
        :data:`ValueType.INT64`, :data:`ValueType.DOUBLE`,
        :data:`ValueType.STRING`, or :data:`ValueType.DISTRIBUTION`.
        See :class:`~google.cloud.monitoring.metric.ValueType`.

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

    def _to_dict(self):
        """Build a dictionary ready to be serialized to the JSON wire format.

        Since this method is used when writing to the API, it excludes
        output-only fields.

        :rtype: dict
        :returns: The dictionary representation of the time series object.
        """
        info = {
            'metric': self.metric._to_dict(),
            'resource': self.resource._to_dict(),
            'points': [point._to_dict() for point in self.points],
        }

        return info

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


def _make_typed_value(value):
    """Create a dict representing a TypedValue API object.

    Typed values are objects with the value itself as the value, keyed by the
    type of the value. They are used when writing points to time series. This
    method returns the dict representation for the TypedValue.

    This method uses the Python type of the object to infer the correct
    type to send to the API. For example, a Python float will be sent to the
    API with "doubleValue" as its key.

    See https://cloud.google.com/monitoring/api/ref_v3/rest/v3/TypedValue

    :type value: bool, int, float, str, or dict
    :param value: value to infer the typed value of.

    :rtype: dict
    :returns: A dict
    """
    typed_value_map = {
        bool: 'boolValue',
        int: 'int64Value',
        float: 'doubleValue',
        str: 'stringValue',
        dict: 'distributionValue',
    }
    type_ = typed_value_map[type(value)]
    if type_ == 'int64Value':
        value = str(value)
    return {type_: value}


class Point(collections.namedtuple('Point', 'end_time start_time value')):
    """A single point in a time series.

    :type end_time: str
    :param end_time: The end time in RFC3339 UTC "Zulu" format.

    :type start_time: str
    :param start_time: (Optional) The start time in RFC3339 UTC "Zulu" format.

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

    def _to_dict(self):
        """Build a dictionary ready to be serialized to the JSON wire format.

        This method serializes a point in JSON format to be written
        to the API.

        :rtype: dict
        :returns: The dictionary representation of the point object.
        """
        info = {
            'interval': {
                'endTime': self.end_time,
            },
            'value': _make_typed_value(self.value),
        }

        if self.start_time is not None:
            info['interval']['startTime'] = self.start_time

        return info
