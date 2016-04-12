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

try:
    import pandas
except ImportError:
    HAVE_PANDAS = False
else:
    HAVE_PANDAS = True  # pragma: NO COVER

import unittest2


PROJECT = 'my-project'

INSTANCE_NAMES = ['instance-1', 'instance-2']
INSTANCE_ZONES = ['us-east1-a', 'us-east1-b']
INSTANCE_IDS = ['1234567890123456789', '9876543210987654321']

M = len(INSTANCE_NAMES)

METRIC_TYPE = 'compute.googleapis.com/instance/cpu/utilization'
METRIC_LABELS = list({'instance_name': INSTANCE_NAMES[i]}
                     for i in range(M))

RESOURCE_TYPE = 'gce_instance'
RESOURCE_LABELS = list({'project_id': PROJECT,
                        'zone': INSTANCE_ZONES[i],
                        'instance_id': INSTANCE_IDS[i]}
                       for i in range(M))

METRIC_KIND = 'GAUGE'
VALUE_TYPE = 'DOUBLE'
VALUES = list(0.1 * i for i in range(M))

TIMESTAMPS = [
    '2016-04-06T22:05:00.042Z',
    '2016-04-06T22:05:01.042Z',
    '2016-04-06T22:05:02.042Z',
]
N = len(TIMESTAMPS)


def parse_timestamps():  # pragma: NO COVER
    import datetime
    return [datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%fZ')
            for t in TIMESTAMPS]


def generate_query_results():  # pragma: NO COVER
    from gcloud.monitoring.metric import Metric
    from gcloud.monitoring.resource import Resource
    from gcloud.monitoring.timeseries import Point, TimeSeries

    def P(timestamp, value):
        return Point(
            start_time=timestamp,
            end_time=timestamp,
            value=value,
        )

    for i in range(M):
        yield TimeSeries(
            metric=Metric(type=METRIC_TYPE, labels=METRIC_LABELS[i]),
            resource=Resource(type=RESOURCE_TYPE, labels=RESOURCE_LABELS[i]),
            metric_kind=METRIC_KIND,
            value_type=VALUE_TYPE,
            points=[P(t, VALUES[i]) for t in TIMESTAMPS],
        )


@unittest2.skipUnless(HAVE_PANDAS, 'No pandas')
class Test__build_dataframe(unittest2.TestCase):  # pragma: NO COVER

    def _callFUT(self, *args, **kwargs):
        from gcloud.monitoring._dataframe import _build_dataframe
        return _build_dataframe(*args, **kwargs)

    def test_both_label_and_labels_illegal(self):
        with self.assertRaises(ValueError):
            self._callFUT([], label='instance_name', labels=['zone'])

    def test_empty_labels_illegal(self):
        with self.assertRaises(ValueError):
            self._callFUT([], labels=[])

    def test_simple_label(self):
        iterable = generate_query_results()
        dataframe = self._callFUT(iterable, label='instance_name')

        self.assertEqual(dataframe.shape, (N, M))
        self.assertEqual(dataframe.values.tolist(), [VALUES] * N)

        self.assertEqual(list(dataframe.columns), INSTANCE_NAMES)
        self.assertIsNone(dataframe.columns.name)

        self.assertEqual(list(dataframe.index), parse_timestamps())
        self.assertIsNone(dataframe.index.name)

    def test_multiple_labels(self):
        NAMES = ['resource_type', 'instance_id']

        iterable = generate_query_results()
        dataframe = self._callFUT(iterable, labels=NAMES)

        self.assertEqual(dataframe.shape, (N, M))
        self.assertEqual(dataframe.values.tolist(), [VALUES] * N)

        expected_headers = [(RESOURCE_TYPE, instance_id)
                            for instance_id in INSTANCE_IDS]
        self.assertEqual(list(dataframe.columns), expected_headers)
        self.assertEqual(dataframe.columns.names, NAMES)
        self.assertIsNone(dataframe.columns.name)

        self.assertEqual(list(dataframe.index), parse_timestamps())
        self.assertIsNone(dataframe.index.name)

    def test_multiple_labels_with_just_one(self):
        NAME = 'instance_id'
        NAMES = [NAME]

        iterable = generate_query_results()
        dataframe = self._callFUT(iterable, labels=NAMES)

        self.assertEqual(dataframe.shape, (N, M))
        self.assertEqual(dataframe.values.tolist(), [VALUES] * N)

        self.assertEqual(list(dataframe.columns), INSTANCE_IDS)
        self.assertEqual(dataframe.columns.names, NAMES)
        self.assertEqual(dataframe.columns.name, NAME)

        self.assertEqual(list(dataframe.index), parse_timestamps())
        self.assertIsNone(dataframe.index.name)

    def test_smart_labels(self):
        NAMES = ['resource_type', 'project_id',
                 'zone', 'instance_id',
                 'instance_name']

        iterable = generate_query_results()
        dataframe = self._callFUT(iterable)

        self.assertEqual(dataframe.shape, (N, M))
        self.assertEqual(dataframe.values.tolist(), [VALUES] * N)

        expected_headers = [
            (RESOURCE_TYPE, PROJECT, zone, instance_id, instance_name)
            for zone, instance_id, instance_name
            in zip(INSTANCE_ZONES, INSTANCE_IDS, INSTANCE_NAMES)]
        self.assertEqual(list(dataframe.columns), expected_headers)
        self.assertEqual(dataframe.columns.names, NAMES)
        self.assertIsNone(dataframe.columns.name)

        self.assertEqual(list(dataframe.index), parse_timestamps())
        self.assertIsNone(dataframe.index.name)

    def test_empty_table_simple_label(self):
        dataframe = self._callFUT([], label='instance_name')
        self.assertEqual(dataframe.shape, (0, 0))
        self.assertIsNone(dataframe.columns.name)
        self.assertIsNone(dataframe.index.name)
        self.assertIsInstance(dataframe.index, pandas.DatetimeIndex)

    def test_empty_table_multiple_labels(self):
        NAMES = ['resource_type', 'instance_id']
        dataframe = self._callFUT([], labels=NAMES)
        self.assertEqual(dataframe.shape, (0, 0))
        self.assertEqual(dataframe.columns.names, NAMES)
        self.assertIsNone(dataframe.columns.name)
        self.assertIsNone(dataframe.index.name)
        self.assertIsInstance(dataframe.index, pandas.DatetimeIndex)

    def test_empty_table_multiple_labels_with_just_one(self):
        NAME = 'instance_id'
        NAMES = [NAME]
        dataframe = self._callFUT([], labels=NAMES)
        self.assertEqual(dataframe.shape, (0, 0))
        self.assertEqual(dataframe.columns.names, NAMES)
        self.assertEqual(dataframe.columns.name, NAME)
        self.assertIsNone(dataframe.index.name)
        self.assertIsInstance(dataframe.index, pandas.DatetimeIndex)

    def test_empty_table_smart_labels(self):
        NAME = 'resource_type'
        NAMES = [NAME]
        dataframe = self._callFUT([])
        self.assertEqual(dataframe.shape, (0, 0))
        self.assertEqual(dataframe.columns.names, NAMES)
        self.assertEqual(dataframe.columns.name, NAME)
        self.assertIsNone(dataframe.index.name)
        self.assertIsInstance(dataframe.index, pandas.DatetimeIndex)


class Test__sorted_resource_labels(unittest2.TestCase):

    def _callFUT(self, labels):
        from gcloud.monitoring._dataframe import _sorted_resource_labels
        return _sorted_resource_labels(labels)

    def test_empty(self):
        self.assertEqual(self._callFUT([]), [])

    def test_sorted(self):
        from gcloud.monitoring._dataframe import TOP_RESOURCE_LABELS
        EXPECTED = TOP_RESOURCE_LABELS + ['other-1', 'other-2']
        self.assertEqual(self._callFUT(EXPECTED), EXPECTED)

    def test_reversed(self):
        from gcloud.monitoring._dataframe import TOP_RESOURCE_LABELS
        EXPECTED = TOP_RESOURCE_LABELS + ['other-1', 'other-2']
        INPUT = list(reversed(EXPECTED))
        self.assertEqual(self._callFUT(INPUT), EXPECTED)
