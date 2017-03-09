# Copyright 2016 Google Inc.
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

import unittest

METRIC_TYPE = 'compute.googleapis.com/instance/uptime'
METRIC_LABELS = {'instance_name': 'instance-1'}

RESOURCE_TYPE = 'gce_instance'
RESOURCE_LABELS = {
    'project_id': 'my-project',
    'zone': 'us-east1-a',
    'instance_id': '1234567890123456789',
}

METRIC_KIND = 'DELTA'
VALUE_TYPE = 'DOUBLE'

TS0 = '2016-04-06T22:05:00.042Z'
TS1 = '2016-04-06T22:05:01.042Z'
TS2 = '2016-04-06T22:05:02.042Z'


class TestTimeSeries(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.monitoring.timeseries import TimeSeries

        return TimeSeries

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor(self):
        from google.cloud.monitoring.metric import Metric
        from google.cloud.monitoring.resource import Resource
        from google.cloud.monitoring.timeseries import Point

        VALUE = 60  # seconds

        METRIC = Metric(type=METRIC_TYPE, labels=METRIC_LABELS)
        RESOURCE = Resource(type=RESOURCE_TYPE, labels=RESOURCE_LABELS)
        POINTS = [
            Point(start_time=TS0, end_time=TS1, value=VALUE),
            Point(start_time=TS1, end_time=TS2, value=VALUE),
        ]

        series = self._make_one(metric=METRIC,
                                resource=RESOURCE,
                                metric_kind=METRIC_KIND,
                                value_type=VALUE_TYPE,
                                points=POINTS)

        self.assertEqual(series.metric, METRIC)
        self.assertEqual(series.resource, RESOURCE)
        self.assertEqual(series.metric_kind, METRIC_KIND)
        self.assertEqual(series.value_type, VALUE_TYPE)
        self.assertEqual(series.points, POINTS)

    def test_from_dict(self):
        VALUE = 60  # seconds

        info = {
            'metric': {'type': METRIC_TYPE, 'labels': METRIC_LABELS},
            'resource': {'type': RESOURCE_TYPE, 'labels': RESOURCE_LABELS},
            'metricKind': METRIC_KIND,
            'valueType': VALUE_TYPE,
            'points': [
                {
                    'interval': {'startTime': TS0, 'endTime': TS1},
                    'value': {'doubleValue': VALUE},
                },
                {
                    'interval': {'startTime': TS1, 'endTime': TS2},
                    'value': {'doubleValue': VALUE},
                },
            ],
        }

        series = self._get_target_class()._from_dict(info)

        self.assertEqual(series.metric.type, METRIC_TYPE)
        self.assertEqual(series.metric.labels, METRIC_LABELS)
        self.assertEqual(series.resource.type, RESOURCE_TYPE)
        self.assertEqual(series.resource.labels, RESOURCE_LABELS)

        self.assertEqual(series.metric_kind, METRIC_KIND)
        self.assertEqual(series.value_type, VALUE_TYPE)

        self.assertEqual(len(series.points), 2)
        point1, point2 = series.points

        self.assertEqual(point1.start_time, TS0)
        self.assertEqual(point1.end_time, TS1)
        self.assertEqual(point1.value, VALUE)

        self.assertEqual(point2.start_time, TS1)
        self.assertEqual(point2.end_time, TS2)
        self.assertEqual(point2.value, VALUE)

    def test_from_dict_no_points(self):
        info = {
            'metric': {'type': METRIC_TYPE, 'labels': METRIC_LABELS},
            'resource': {'type': RESOURCE_TYPE, 'labels': RESOURCE_LABELS},
            'metricKind': METRIC_KIND,
            'valueType': VALUE_TYPE,
        }

        series = self._get_target_class()._from_dict(info)

        self.assertEqual(series.metric.type, METRIC_TYPE)
        self.assertEqual(series.metric.labels, METRIC_LABELS)
        self.assertEqual(series.resource.type, RESOURCE_TYPE)
        self.assertEqual(series.resource.labels, RESOURCE_LABELS)

        self.assertEqual(series.metric_kind, METRIC_KIND)
        self.assertEqual(series.value_type, VALUE_TYPE)

        self.assertEqual(series.points, [])

    def test_labels(self):
        info = {
            'metric': {'type': METRIC_TYPE, 'labels': METRIC_LABELS},
            'resource': {'type': RESOURCE_TYPE, 'labels': RESOURCE_LABELS},
            'metricKind': METRIC_KIND,
            'valueType': VALUE_TYPE,
        }

        series = self._get_target_class()._from_dict(info)

        labels = {'resource_type': RESOURCE_TYPE}
        labels.update(RESOURCE_LABELS)
        labels.update(METRIC_LABELS)

        self.assertIsNone(series._labels)
        self.assertEqual(series.labels, labels)
        self.assertIsNotNone(series._labels)
        self.assertEqual(series.labels, labels)

    def test_to_dict(self):
        import datetime
        from google.cloud._helpers import _datetime_to_rfc3339

        from google.cloud.monitoring.metric import Metric
        from google.cloud.monitoring.resource import Resource
        from google.cloud.monitoring.timeseries import Point

        VALUE = 42
        end_time = datetime.datetime.now()
        end_time_str = _datetime_to_rfc3339(end_time, ignore_zone=False)

        METRIC = Metric(type=METRIC_TYPE, labels=METRIC_LABELS)
        RESOURCE = Resource(type=RESOURCE_TYPE, labels=RESOURCE_LABELS)
        POINT = Point(start_time=None, end_time=end_time_str, value=VALUE)

        info = {
            'metric': {'type': METRIC_TYPE, 'labels': METRIC_LABELS},
            'resource': {'type': RESOURCE_TYPE, 'labels': RESOURCE_LABELS},
            'points': [{
                'interval': {
                    'endTime': end_time_str},
                'value': {'int64Value': str(VALUE)},
            }]
        }

        series = self._make_one(metric=METRIC, resource=RESOURCE,
                                metric_kind=None, value_type=None,
                                points=[POINT])
        series_dict = series._to_dict()
        self.assertEqual(info, series_dict)


class TestPoint(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.monitoring.timeseries import Point

        return Point

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor(self):
        VALUE = 3.14
        point = self._make_one(start_time=TS0, end_time=TS1, value=VALUE)
        self.assertEqual(point.start_time, TS0)
        self.assertEqual(point.end_time, TS1)
        self.assertEqual(point.value, VALUE)

    def test_from_dict(self):
        VALUE = 3.14
        info = {
            'interval': {'startTime': TS0, 'endTime': TS1},
            'value': {'doubleValue': VALUE},
        }
        point = self._get_target_class()._from_dict(info)
        self.assertEqual(point.start_time, TS0)
        self.assertEqual(point.end_time, TS1)
        self.assertEqual(point.value, VALUE)

    def test_from_dict_defaults(self):
        VALUE = 3.14
        info = {
            'interval': {'endTime': TS1},
            'value': {'doubleValue': VALUE},
        }
        point = self._get_target_class()._from_dict(info)
        self.assertIsNone(point.start_time)
        self.assertEqual(point.end_time, TS1)
        self.assertEqual(point.value, VALUE)

    def test_from_dict_int64(self):
        VALUE = 2 ** 63 - 1
        info = {
            'interval': {'endTime': TS1},
            'value': {'int64Value': str(VALUE)},
        }
        point = self._get_target_class()._from_dict(info)
        self.assertIsNone(point.start_time)
        self.assertEqual(point.end_time, TS1)
        self.assertEqual(point.value, VALUE)

    def test_to_dict_int64(self):
        import datetime
        from google.cloud._helpers import _datetime_to_rfc3339

        VALUE = 42
        end_time = datetime.datetime.now()
        end_time_str = _datetime_to_rfc3339(end_time, ignore_zone=False)
        point = self._make_one(end_time=end_time_str, start_time=None,
                               value=VALUE)
        info = {
            'interval': {'endTime': end_time_str},
            'value': {'int64Value': str(VALUE)},
        }

        point_dict = point._to_dict()
        self.assertEqual(info, point_dict)

    def test_to_dict_float_with_start_time(self):
        import datetime
        from google.cloud._helpers import _datetime_to_rfc3339

        VALUE = 1.6180339
        start_time = datetime.datetime.now()
        start_time_str = _datetime_to_rfc3339(start_time, ignore_zone=False)
        end_time = datetime.datetime.now()
        end_time_str = _datetime_to_rfc3339(end_time, ignore_zone=False)

        point = self._make_one(end_time=end_time_str,
                               start_time=start_time_str, value=VALUE)
        info = {
            'interval': {
                'startTime': start_time_str,
                'endTime': end_time_str},
            'value': {'doubleValue': VALUE},
        }

        point_dict = point._to_dict()
        self.assertEqual(info, point_dict)
