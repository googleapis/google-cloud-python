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

import unittest2

PROJECT = 'my-project'

METRIC_TYPE = 'compute.googleapis.com/instance/uptime'
METRIC_LABELS = {'instance_name': 'instance-1'}
METRIC_LABELS2 = {'instance_name': 'instance-2'}

RESOURCE_TYPE = 'gce_instance'
RESOURCE_LABELS = {
    'project_id': 'my-project',
    'zone': 'us-east1-a',
    'instance_id': '1234567890123456789',
}
RESOURCE_LABELS2 = {
    'project_id': 'my-project',
    'zone': 'us-east1-b',
    'instance_id': '9876543210987654321',
}

METRIC_KIND = 'DELTA'
VALUE_TYPE = 'DOUBLE'

TS0 = '2016-04-06T22:05:00.042Z'
TS1 = '2016-04-06T22:05:01.042Z'
TS2 = '2016-04-06T22:05:02.042Z'


class TestAligner(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.monitoring.query import Aligner
        return Aligner

    def test_one(self):
        self.assertTrue(hasattr(self._getTargetClass(), 'ALIGN_RATE'))

    def test_names(self):
        for name in self._getTargetClass().__dict__:
            if not name.startswith('_'):
                self.assertEqual(getattr(self._getTargetClass(), name), name)


class TestReducer(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.monitoring.query import Reducer
        return Reducer

    def test_one(self):
        self.assertTrue(hasattr(self._getTargetClass(),
                                'REDUCE_PERCENTILE_99'))

    def test_names(self):
        for name in self._getTargetClass().__dict__:
            if not name.startswith('_'):
                self.assertEqual(getattr(self._getTargetClass(), name), name)


class TestQuery(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.monitoring.query import Query
        return Query

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor_minimal(self):
        client = _Client(project=PROJECT, connection=_Connection())
        query = self._makeOne(client)

        self.assertEqual(query._client, client)
        self.assertEqual(query._filter.metric_type,
                         self._getTargetClass().DEFAULT_METRIC_TYPE)

        self.assertIsNone(query._start_time)
        self.assertIsNone(query._end_time)

        self.assertIsNone(query._per_series_aligner)
        self.assertIsNone(query._alignment_period_seconds)
        self.assertIsNone(query._cross_series_reducer)
        self.assertEqual(query._group_by_fields, ())

    def test_constructor_maximal(self):
        import datetime

        T1 = datetime.datetime(2016, 4, 7, 2, 30, 30)
        DAYS, HOURS, MINUTES = 1, 2, 3
        T0 = T1 - datetime.timedelta(days=DAYS, hours=HOURS, minutes=MINUTES)

        client = _Client(project=PROJECT, connection=_Connection())
        query = self._makeOne(client, METRIC_TYPE,
                              end_time=T1,
                              days=DAYS, hours=HOURS, minutes=MINUTES)

        self.assertEqual(query._client, client)
        self.assertEqual(query._filter.metric_type, METRIC_TYPE)

        self.assertEqual(query._start_time, T0)
        self.assertEqual(query._end_time, T1)

        self.assertIsNone(query._per_series_aligner)
        self.assertIsNone(query._alignment_period_seconds)
        self.assertIsNone(query._cross_series_reducer)
        self.assertEqual(query._group_by_fields, ())

    def test_constructor_default_end_time(self):
        import datetime
        from gcloud._testing import _Monkey
        from gcloud.monitoring import query as MUT

        MINUTES = 5
        NOW, T0, T1 = [
            datetime.datetime(2016, 4, 7, 2, 30, 30),
            datetime.datetime(2016, 4, 7, 2, 25, 0),
            datetime.datetime(2016, 4, 7, 2, 30, 0),
        ]

        client = _Client(project=PROJECT, connection=_Connection())
        with _Monkey(MUT, _UTCNOW=lambda: NOW):
            query = self._makeOne(client, METRIC_TYPE, minutes=MINUTES)

        self.assertEqual(query._start_time, T0)
        self.assertEqual(query._end_time, T1)

    def test_constructor_nonzero_duration_illegal(self):
        import datetime
        T1 = datetime.datetime(2016, 4, 7, 2, 30, 30)
        client = _Client(project=PROJECT, connection=_Connection())
        with self.assertRaises(ValueError):
            self._makeOne(client, METRIC_TYPE, end_time=T1)

    def test_execution_without_interval_illegal(self):
        client = _Client(project=PROJECT, connection=_Connection())
        query = self._makeOne(client, METRIC_TYPE)
        with self.assertRaises(ValueError):
            list(query)

    def test_metric_type(self):
        client = _Client(project=PROJECT, connection=_Connection())
        query = self._makeOne(client, METRIC_TYPE)
        self.assertEqual(query.metric_type, METRIC_TYPE)

    def test_filter(self):
        client = _Client(project=PROJECT, connection=_Connection())
        query = self._makeOne(client, METRIC_TYPE)
        expected = 'metric.type = "{type}"'.format(type=METRIC_TYPE)
        self.assertEqual(query.filter, expected)

    def test_filter_by_group(self):
        GROUP = '1234567'
        client = _Client(project=PROJECT, connection=_Connection())
        query = self._makeOne(client, METRIC_TYPE)
        query = query.select_group(GROUP)
        expected = (
            'metric.type = "{type}"'
            ' AND group.id = "{group}"'
        ).format(type=METRIC_TYPE, group=GROUP)
        self.assertEqual(query.filter, expected)

    def test_filter_by_projects(self):
        PROJECT1, PROJECT2 = 'project-1', 'project-2'
        client = _Client(project=PROJECT, connection=_Connection())
        query = self._makeOne(client, METRIC_TYPE)
        query = query.select_projects(PROJECT1, PROJECT2)
        expected = (
            'metric.type = "{type}"'
            ' AND project = "{project1}" OR project = "{project2}"'
        ).format(type=METRIC_TYPE, project1=PROJECT1, project2=PROJECT2)
        self.assertEqual(query.filter, expected)

    def test_filter_by_resources(self):
        ZONE_PREFIX = 'europe-'
        client = _Client(project=PROJECT, connection=_Connection())
        query = self._makeOne(client, METRIC_TYPE)
        query = query.select_resources(zone_prefix=ZONE_PREFIX)
        expected = (
            'metric.type = "{type}"'
            ' AND resource.label.zone = starts_with("{prefix}")'
        ).format(type=METRIC_TYPE, prefix=ZONE_PREFIX)
        self.assertEqual(query.filter, expected)

    def test_filter_by_metrics(self):
        INSTANCE = 'my-instance'
        client = _Client(project=PROJECT, connection=_Connection())
        query = self._makeOne(client, METRIC_TYPE)
        query = query.select_metrics(instance_name=INSTANCE)
        expected = (
            'metric.type = "{type}"'
            ' AND metric.label.instance_name = "{instance}"'
        ).format(type=METRIC_TYPE, instance=INSTANCE)
        self.assertEqual(query.filter, expected)

    def test_request_parameters_minimal(self):
        import datetime

        T1 = datetime.datetime(2016, 4, 7, 2, 30, 0)

        client = _Client(project=PROJECT, connection=_Connection())
        query = self._makeOne(client, METRIC_TYPE)
        query = query.select_interval(end_time=T1)
        actual = list(query._build_query_params())
        expected = [
            ('filter', 'metric.type = "{type}"'.format(type=METRIC_TYPE)),
            ('interval.endTime', T1.isoformat() + 'Z'),
        ]
        self.assertEqual(actual, expected)

    def test_request_parameters_maximal(self):
        import datetime

        T0 = datetime.datetime(2016, 4, 7, 2, 0, 0)
        T1 = datetime.datetime(2016, 4, 7, 2, 30, 0)

        ALIGNER = 'ALIGN_DELTA'
        MINUTES, SECONDS, PERIOD = 1, 30, '90s'

        REDUCER = 'REDUCE_MEAN'
        FIELD1, FIELD2 = 'resource.zone', 'metric.instance_name'

        PAGE_SIZE = 100
        PAGE_TOKEN = 'second-page-please'

        client = _Client(project=PROJECT, connection=_Connection())
        query = self._makeOne(client, METRIC_TYPE)
        query = query.select_interval(start_time=T0, end_time=T1)
        query = query.align(ALIGNER, minutes=MINUTES, seconds=SECONDS)
        query = query.reduce(REDUCER, FIELD1, FIELD2)
        actual = list(query._build_query_params(headers_only=True,
                                                page_size=PAGE_SIZE,
                                                page_token=PAGE_TOKEN))
        expected = [
            ('filter', 'metric.type = "{type}"'.format(type=METRIC_TYPE)),
            ('interval.endTime', T1.isoformat() + 'Z'),
            ('interval.startTime', T0.isoformat() + 'Z'),
            ('aggregation.perSeriesAligner', ALIGNER),
            ('aggregation.alignmentPeriod', PERIOD),
            ('aggregation.crossSeriesReducer', REDUCER),
            ('aggregation.groupByFields', FIELD1),
            ('aggregation.groupByFields', FIELD2),
            ('view', 'HEADERS'),
            ('pageSize', PAGE_SIZE),
            ('pageToken', PAGE_TOKEN),
        ]
        self.assertEqual(actual, expected)

    def test_iteration(self):
        import datetime

        T0 = datetime.datetime(2016, 4, 6, 22, 5, 0)
        T1 = datetime.datetime(2016, 4, 6, 22, 10, 0)

        INTERVAL1 = {'startTime': TS0, 'endTime': TS1}
        INTERVAL2 = {'startTime': TS1, 'endTime': TS2}

        VALUE1 = 60  # seconds
        VALUE2 = 60.001  # seconds

        SERIES1 = {
            'metric': {'type': METRIC_TYPE, 'labels': METRIC_LABELS},
            'resource': {'type': RESOURCE_TYPE, 'labels': RESOURCE_LABELS},
            'metricKind': METRIC_KIND,
            'valueType': VALUE_TYPE,
            'points': [
                {'interval': INTERVAL2, 'value': {'doubleValue': VALUE1}},
                {'interval': INTERVAL1, 'value': {'doubleValue': VALUE1}},
            ],
        }
        SERIES2 = {
            'metric': {'type': METRIC_TYPE, 'labels': METRIC_LABELS2},
            'resource': {'type': RESOURCE_TYPE, 'labels': RESOURCE_LABELS2},
            'metricKind': METRIC_KIND,
            'valueType': VALUE_TYPE,
            'points': [
                {'interval': INTERVAL2, 'value': {'doubleValue': VALUE2}},
                {'interval': INTERVAL1, 'value': {'doubleValue': VALUE2}},
            ],
        }

        RESPONSE = {'timeSeries': [SERIES1, SERIES2]}

        connection = _Connection(RESPONSE)
        client = _Client(project=PROJECT, connection=connection)
        query = self._makeOne(client, METRIC_TYPE)
        query = query.select_interval(start_time=T0, end_time=T1)
        response = list(query)

        self.assertEqual(len(response), 2)
        series1, series2 = response

        self.assertEqual(series1.metric.labels, METRIC_LABELS)
        self.assertEqual(series2.metric.labels, METRIC_LABELS2)
        self.assertEqual(series1.resource.labels, RESOURCE_LABELS)
        self.assertEqual(series2.resource.labels, RESOURCE_LABELS2)

        self.assertEqual([p.value for p in series1.points], [VALUE1, VALUE1])
        self.assertEqual([p.value for p in series2.points], [VALUE2, VALUE2])
        self.assertEqual([p.end_time for p in series1.points], [TS1, TS2])
        self.assertEqual([p.end_time for p in series2.points], [TS1, TS2])

        expected_request = {
            'method': 'GET',
            'path': '/projects/{project}/timeSeries/'.format(project=PROJECT),
            'query_params': [
                ('filter', 'metric.type = "{type}"'.format(type=METRIC_TYPE)),
                ('interval.endTime', T1.isoformat() + 'Z'),
                ('interval.startTime', T0.isoformat() + 'Z'),
            ],
        }

        request, = connection._requested
        self.assertEqual(request, expected_request)

    def test_iteration_paged(self):
        import copy
        import datetime
        from gcloud.exceptions import NotFound

        T0 = datetime.datetime(2016, 4, 6, 22, 5, 0)
        T1 = datetime.datetime(2016, 4, 6, 22, 10, 0)

        INTERVAL1 = {'startTime': TS0, 'endTime': TS1}
        INTERVAL2 = {'startTime': TS1, 'endTime': TS2}

        VALUE1 = 60  # seconds
        VALUE2 = 60.001  # seconds

        SERIES1 = {
            'metric': {'type': METRIC_TYPE, 'labels': METRIC_LABELS},
            'resource': {'type': RESOURCE_TYPE, 'labels': RESOURCE_LABELS},
            'metricKind': METRIC_KIND,
            'valueType': VALUE_TYPE,
            'points': [
                {'interval': INTERVAL2, 'value': {'doubleValue': VALUE1}},
                {'interval': INTERVAL1, 'value': {'doubleValue': VALUE1}},
            ],
        }
        SERIES2_PART1 = {
            'metric': {'type': METRIC_TYPE, 'labels': METRIC_LABELS2},
            'resource': {'type': RESOURCE_TYPE, 'labels': RESOURCE_LABELS2},
            'metricKind': METRIC_KIND,
            'valueType': VALUE_TYPE,
            'points': [
                {'interval': INTERVAL2, 'value': {'doubleValue': VALUE2}},
            ],
        }
        SERIES2_PART2 = {
            'metric': {'type': METRIC_TYPE, 'labels': METRIC_LABELS2},
            'resource': {'type': RESOURCE_TYPE, 'labels': RESOURCE_LABELS2},
            'metricKind': METRIC_KIND,
            'valueType': VALUE_TYPE,
            'points': [
                {'interval': INTERVAL1, 'value': {'doubleValue': VALUE2}},
            ],
        }

        TOKEN = 'second-page-please'
        RESPONSE1 = {'timeSeries': [SERIES1, SERIES2_PART1],
                     'nextPageToken': TOKEN}
        RESPONSE2 = {'timeSeries': [SERIES2_PART2]}

        connection = _Connection(RESPONSE1, RESPONSE2)
        client = _Client(project=PROJECT, connection=connection)
        query = self._makeOne(client, METRIC_TYPE)
        query = query.select_interval(start_time=T0, end_time=T1)
        response = list(query)

        self.assertEqual(len(response), 2)
        series1, series2 = response

        self.assertEqual(series1.metric.labels, METRIC_LABELS)
        self.assertEqual(series2.metric.labels, METRIC_LABELS2)
        self.assertEqual(series1.resource.labels, RESOURCE_LABELS)
        self.assertEqual(series2.resource.labels, RESOURCE_LABELS2)

        self.assertEqual([p.value for p in series1.points], [VALUE1, VALUE1])
        self.assertEqual([p.value for p in series2.points], [VALUE2, VALUE2])
        self.assertEqual([p.end_time for p in series1.points], [TS1, TS2])
        self.assertEqual([p.end_time for p in series2.points], [TS1, TS2])

        expected_request1 = {
            'method': 'GET',
            'path': '/projects/{project}/timeSeries/'.format(project=PROJECT),
            'query_params': [
                ('filter', 'metric.type = "{type}"'.format(type=METRIC_TYPE)),
                ('interval.endTime', T1.isoformat() + 'Z'),
                ('interval.startTime', T0.isoformat() + 'Z'),
            ],
        }

        expected_request2 = copy.deepcopy(expected_request1)
        expected_request2['query_params'].append(('pageToken', TOKEN))

        request1, request2 = connection._requested
        self.assertEqual(request1, expected_request1)
        self.assertEqual(request2, expected_request2)

        with self.assertRaises(NotFound):
            list(query)

    def test_iteration_empty(self):
        import datetime

        T0 = datetime.datetime(2016, 4, 6, 22, 5, 0)
        T1 = datetime.datetime(2016, 4, 6, 22, 10, 0)

        connection = _Connection({})
        client = _Client(project=PROJECT, connection=connection)
        query = self._makeOne(client, METRIC_TYPE)
        query = query.select_interval(start_time=T0, end_time=T1)
        response = list(query)

        self.assertEqual(len(response), 0)

        expected_request = {
            'method': 'GET',
            'path': '/projects/{project}/timeSeries/'.format(project=PROJECT),
            'query_params': [
                ('filter', 'metric.type = "{type}"'.format(type=METRIC_TYPE)),
                ('interval.endTime', T1.isoformat() + 'Z'),
                ('interval.startTime', T0.isoformat() + 'Z'),
            ],
        }
        request, = connection._requested
        self.assertEqual(request, expected_request)

    def test_iteration_headers_only(self):
        import datetime

        T0 = datetime.datetime(2016, 4, 6, 22, 5, 0)
        T1 = datetime.datetime(2016, 4, 6, 22, 10, 0)

        SERIES1 = {
            'metric': {'type': METRIC_TYPE, 'labels': METRIC_LABELS},
            'resource': {'type': RESOURCE_TYPE, 'labels': RESOURCE_LABELS},
            'metricKind': METRIC_KIND,
            'valueType': VALUE_TYPE,
        }
        SERIES2 = {
            'metric': {'type': METRIC_TYPE, 'labels': METRIC_LABELS2},
            'resource': {'type': RESOURCE_TYPE, 'labels': RESOURCE_LABELS2},
            'metricKind': METRIC_KIND,
            'valueType': VALUE_TYPE,
        }

        RESPONSE = {'timeSeries': [SERIES1, SERIES2]}

        connection = _Connection(RESPONSE)
        client = _Client(project=PROJECT, connection=connection)
        query = self._makeOne(client, METRIC_TYPE)
        query = query.select_interval(start_time=T0, end_time=T1)
        response = list(query.iter(headers_only=True))

        self.assertEqual(len(response), 2)
        series1, series2 = response

        self.assertEqual(series1.metric.labels, METRIC_LABELS)
        self.assertEqual(series2.metric.labels, METRIC_LABELS2)
        self.assertEqual(series1.resource.labels, RESOURCE_LABELS)
        self.assertEqual(series2.resource.labels, RESOURCE_LABELS2)

        self.assertEqual(series1.points, [])
        self.assertEqual(series2.points, [])

        expected_request = {
            'method': 'GET',
            'path': '/projects/{project}/timeSeries/'.format(project=PROJECT),
            'query_params': [
                ('filter', 'metric.type = "{type}"'.format(type=METRIC_TYPE)),
                ('interval.endTime', T1.isoformat() + 'Z'),
                ('interval.startTime', T0.isoformat() + 'Z'),
                ('view', 'HEADERS'),
            ],
        }

        request, = connection._requested
        self.assertEqual(request, expected_request)


class Test_Filter(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.monitoring.query import _Filter
        return _Filter

    def _makeOne(self, metric_type):
        return self._getTargetClass()(metric_type)

    def test_minimal(self):
        obj = self._makeOne(METRIC_TYPE)
        expected = 'metric.type = "{type}"'.format(type=METRIC_TYPE)
        self.assertEqual(str(obj), expected)

    def test_maximal(self):
        obj = self._makeOne(METRIC_TYPE)
        obj.group_id = '1234567'
        obj.projects = 'project-1', 'project-2'
        obj.select_resources(resource_type='some-resource',
                             resource_label='foo')
        obj.select_metrics(metric_label_prefix='bar-')

        expected = (
            'metric.type = "{type}"'
            ' AND group.id = "1234567"'
            ' AND project = "project-1" OR project = "project-2"'
            ' AND resource.label.resource_label = "foo"'
            ' AND resource.type = "some-resource"'
            ' AND metric.label.metric_label = starts_with("bar-")'
        ).format(type=METRIC_TYPE)

        self.assertEqual(str(obj), expected)


class Test__build_label_filter(unittest2.TestCase):

    def _callFUT(self, *args, **kwargs):
        from gcloud.monitoring.query import _build_label_filter
        return _build_label_filter(*args, **kwargs)

    def test_no_labels(self):
        self.assertEqual(self._callFUT('resource'), '')

    def test_label_is_none(self):
        self.assertEqual(self._callFUT('resource', foo=None), '')

    def test_metric_labels(self):
        actual = self._callFUT(
            'metric',
            alpha_prefix='a-',
            beta_gamma_suffix='-b',
            delta_epsilon='xyz',
        )
        expected = (
            'metric.label.alpha = starts_with("a-")'
            ' AND metric.label.beta_gamma = ends_with("-b")'
            ' AND metric.label.delta_epsilon = "xyz"'
        )
        self.assertEqual(actual, expected)

    def test_resource_labels(self):
        actual = self._callFUT(
            'resource',
            alpha_prefix='a-',
            beta_gamma_suffix='-b',
            delta_epsilon='xyz',
        )
        expected = (
            'resource.label.alpha = starts_with("a-")'
            ' AND resource.label.beta_gamma = ends_with("-b")'
            ' AND resource.label.delta_epsilon = "xyz"'
        )
        self.assertEqual(actual, expected)

    def test_raw_label_filters(self):
        actual = self._callFUT(
            'resource',
            'resource.label.alpha = starts_with("a-")',
            'resource.label.beta_gamma = ends_with("-b")',
            'resource.label.delta_epsilon = "xyz"',
        )
        expected = (
            'resource.label.alpha = starts_with("a-")'
            ' AND resource.label.beta_gamma = ends_with("-b")'
            ' AND resource.label.delta_epsilon = "xyz"'
        )
        self.assertEqual(actual, expected)

    def test_resource_type(self):
        actual = self._callFUT('resource', resource_type='foo')
        expected = 'resource.type = "foo"'
        self.assertEqual(actual, expected)

    def test_resource_type_prefix(self):
        actual = self._callFUT('resource', resource_type_prefix='foo-')
        expected = 'resource.type = starts_with("foo-")'
        self.assertEqual(actual, expected)

    def test_resource_type_suffix(self):
        actual = self._callFUT('resource', resource_type_suffix='-foo')
        expected = 'resource.type = ends_with("-foo")'
        self.assertEqual(actual, expected)


class Test__format_timestamp(unittest2.TestCase):

    def _callFUT(self, timestamp):
        from gcloud.monitoring.query import _format_timestamp
        return _format_timestamp(timestamp)

    def test_naive(self):
        from datetime import datetime
        TIMESTAMP = datetime(2016, 4, 5, 13, 30, 0)
        timestamp = self._callFUT(TIMESTAMP)
        self.assertEqual(timestamp, '2016-04-05T13:30:00Z')

    def test_with_timezone(self):
        from datetime import datetime
        from gcloud._helpers import UTC
        TIMESTAMP = datetime(2016, 4, 5, 13, 30, 0, tzinfo=UTC)
        timestamp = self._callFUT(TIMESTAMP)
        self.assertEqual(timestamp, '2016-04-05T13:30:00Z')


class _Connection(object):

    def __init__(self, *responses):
        self._responses = list(responses)
        self._requested = []

    def api_request(self, **kwargs):
        from gcloud.exceptions import NotFound
        self._requested.append(kwargs)
        try:
            return self._responses.pop(0)
        except IndexError:
            raise NotFound('miss')


class _Client(object):

    def __init__(self, project, connection):
        self.project = project
        self.connection = connection
