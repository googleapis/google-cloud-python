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


class TestMetricKind(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.monitoring.metric import MetricKind
        return MetricKind

    def test_one(self):
        self.assertTrue(hasattr(self._getTargetClass(), 'GAUGE'))

    def test_names(self):
        for name in self._getTargetClass().__dict__:
            if not name.startswith('_'):
                self.assertEqual(getattr(self._getTargetClass(), name), name)


class TestValueType(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.monitoring.metric import ValueType
        return ValueType

    def test_one(self):
        self.assertTrue(hasattr(self._getTargetClass(), 'DISTRIBUTION'))

    def test_names(self):
        for name in self._getTargetClass().__dict__:
            if not name.startswith('_'):
                self.assertEqual(getattr(self._getTargetClass(), name), name)


class TestMetricDescriptor(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.monitoring.metric import MetricDescriptor
        return MetricDescriptor

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        from gcloud.monitoring.label import LabelDescriptor

        TYPE = 'appengine.googleapis.com/http/server/response_count'
        NAME = 'projects/my-project/metricDescriptors/' + TYPE
        LABELS = [
            LabelDescriptor(key='loading', value_type='BOOL',
                            description='Loaded a new instance?'),
            LabelDescriptor(key='response_code', value_type='INT64',
                            description='HTTP status code for the request.'),
        ]

        METRIC_KIND = 'DELTA'
        VALUE_TYPE = 'INT64'

        UNIT = '{responses}/s'
        DESCRIPTION = 'Delta HTTP response count.'
        DISPLAY_NAME = 'Response count'

        client = object()
        descriptor = self._makeOne(
            client=client,
            name=NAME,
            type_=TYPE,
            labels=LABELS,
            metric_kind=METRIC_KIND,
            value_type=VALUE_TYPE,
            unit=UNIT,
            description=DESCRIPTION,
            display_name=DISPLAY_NAME,
        )

        self.assertIs(descriptor.client, client)

        self.assertEqual(descriptor.name, NAME)
        self.assertEqual(descriptor.type, TYPE)
        self.assertEqual(descriptor.labels, LABELS)

        self.assertEqual(descriptor.metric_kind, METRIC_KIND)
        self.assertEqual(descriptor.value_type, VALUE_TYPE)

        self.assertEqual(descriptor.unit, UNIT)
        self.assertEqual(descriptor.description, DESCRIPTION)
        self.assertEqual(descriptor.display_name, DISPLAY_NAME)

    def test_constructor_defaults(self):
        TYPE = 'appengine.googleapis.com/http/server/response_count'

        client = object()
        descriptor = self._makeOne(client=client, type_=TYPE)

        self.assertIs(descriptor.client, client)

        self.assertIsNone(descriptor.name)
        self.assertEqual(descriptor.type, TYPE)
        self.assertEqual(descriptor.labels, ())

        self.assertEqual(descriptor.metric_kind, 'METRIC_KIND_UNSPECIFIED')
        self.assertEqual(descriptor.value_type, 'VALUE_TYPE_UNSPECIFIED')

        self.assertEqual(descriptor.unit, '')
        self.assertEqual(descriptor.description, '')
        self.assertEqual(descriptor.display_name, '')

    def test_from_dict(self):
        TYPE = 'appengine.googleapis.com/http/server/response_count'
        NAME = 'projects/my-project/metricDescriptors/' + TYPE
        LABEL1 = {'key': 'loading', 'valueType': 'BOOL',
                  'description': 'Loaded a new instance?'}
        LABEL2 = {'key': 'response_code', 'valueType': 'INT64',
                  'description': 'HTTP status code for the request.'}

        METRIC_KIND = 'DELTA'
        VALUE_TYPE = 'INT64'

        UNIT = '{responses}/s'
        DESCRIPTION = 'Delta HTTP response count.'
        DISPLAY_NAME = 'Response count'

        info = {
            'name': NAME,
            'type': TYPE,
            'labels': [LABEL1, LABEL2],
            'metricKind': METRIC_KIND,
            'valueType': VALUE_TYPE,
            'unit': UNIT,
            'description': DESCRIPTION,
            'displayName': DISPLAY_NAME,
        }
        client = object()
        descriptor = self._getTargetClass()._from_dict(client, info)

        self.assertIs(descriptor.client, client)

        self.assertEqual(descriptor.name, NAME)
        self.assertEqual(descriptor.type, TYPE)

        self.assertEqual(len(descriptor.labels), 2)
        label1, label2 = descriptor.labels
        self.assertEqual(label1.key, LABEL1['key'])
        self.assertEqual(label2.key, LABEL2['key'])

        self.assertEqual(descriptor.metric_kind, METRIC_KIND)
        self.assertEqual(descriptor.value_type, VALUE_TYPE)

        self.assertEqual(descriptor.unit, UNIT)
        self.assertEqual(descriptor.description, DESCRIPTION)
        self.assertEqual(descriptor.display_name, DISPLAY_NAME)

    def test_from_dict_defaults(self):
        TYPE = 'appengine.googleapis.com/http/server/response_count'
        NAME = 'projects/my-project/metricDescriptors/' + TYPE
        METRIC_KIND = 'CUMULATIVE'
        VALUE_TYPE = 'DOUBLE'

        info = {
            'name': NAME,
            'type': TYPE,
            'metricKind': METRIC_KIND,
            'valueType': VALUE_TYPE,
        }
        client = object()
        descriptor = self._getTargetClass()._from_dict(client, info)

        self.assertIs(descriptor.client, client)

        self.assertEqual(descriptor.name, NAME)
        self.assertEqual(descriptor.type, TYPE)
        self.assertEqual(descriptor.labels, ())
        self.assertEqual(descriptor.metric_kind, METRIC_KIND)
        self.assertEqual(descriptor.value_type, VALUE_TYPE)
        self.assertEqual(descriptor.unit, '')
        self.assertEqual(descriptor.description, '')
        self.assertEqual(descriptor.display_name, '')

    def test_to_dict(self):
        TYPE = 'appengine.googleapis.com/http/server/response_count'
        NAME = 'projects/my-project/metricDescriptors/' + TYPE
        LABEL1 = {'key': 'loading', 'valueType': 'BOOL',
                  'description': 'Loaded a new instance?'}
        LABEL2 = {'key': 'response_code', 'valueType': 'INT64',
                  'description': 'HTTP status code for the request.'}

        METRIC_KIND = 'DELTA'
        VALUE_TYPE = 'INT64'

        UNIT = '{responses}/s'
        DESCRIPTION = 'Delta HTTP response count.'
        DISPLAY_NAME = 'Response count'

        info = {
            'name': NAME,
            'type': TYPE,
            'labels': [LABEL1, LABEL2],
            'metricKind': METRIC_KIND,
            'valueType': VALUE_TYPE,
            'unit': UNIT,
            'description': DESCRIPTION,
            'displayName': DISPLAY_NAME,
        }
        client = object()
        descriptor = self._getTargetClass()._from_dict(client, info)

        del info['name']
        self.assertEqual(descriptor._to_dict(), info)

    def test_to_dict_defaults(self):
        TYPE = 'appengine.googleapis.com/http/server/response_count'
        NAME = 'projects/my-project/metricDescriptors/' + TYPE
        METRIC_KIND = 'DELTA'
        VALUE_TYPE = 'INT64'

        info = {
            'name': NAME,
            'type': TYPE,
            'metricKind': METRIC_KIND,
            'valueType': VALUE_TYPE,
        }
        client = object()
        descriptor = self._getTargetClass()._from_dict(client, info)

        del info['name']
        self.assertEqual(descriptor._to_dict(), info)

    def test_create(self):
        PROJECT = 'my-project'
        TYPE = 'custom.googleapis.com/my_metric'
        PATH = 'projects/{project}/metricDescriptors/'.format(project=PROJECT)
        NAME = PATH + TYPE

        METRIC_KIND = 'GAUGE'
        VALUE_TYPE = 'DOUBLE'
        DESCRIPTION = 'This is my metric.'

        REQUEST = {
            'type': TYPE,
            'metricKind': METRIC_KIND,
            'valueType': VALUE_TYPE,
            'description': DESCRIPTION,
        }
        RESPONSE = dict(REQUEST, name=NAME)

        connection = _Connection(RESPONSE)
        client = _Client(project=PROJECT, connection=connection)
        descriptor = self._makeOne(
            client=client,
            type_=TYPE,
            metric_kind=METRIC_KIND,
            value_type=VALUE_TYPE,
            description=DESCRIPTION,
        )
        descriptor.create()

        self.assertEqual(descriptor.name, NAME)
        self.assertEqual(descriptor.type, TYPE)
        self.assertEqual(descriptor.labels, ())

        self.assertEqual(descriptor.metric_kind, METRIC_KIND)
        self.assertEqual(descriptor.value_type, VALUE_TYPE)

        self.assertEqual(descriptor.unit, '')
        self.assertEqual(descriptor.description, DESCRIPTION)
        self.assertEqual(descriptor.display_name, '')

        request, = connection._requested
        expected_request = {'method': 'POST', 'path': '/' + PATH,
                            'data': REQUEST}
        self.assertEqual(request, expected_request)

    def test_delete(self):
        PROJECT = 'my-project'
        TYPE = 'custom.googleapis.com/my_metric'
        NAME = 'projects/{project}/metricDescriptors/{type}'.format(
            project=PROJECT, type=TYPE)

        connection = _Connection({})
        client = _Client(project=PROJECT, connection=connection)
        descriptor = self._makeOne(
            client=client,
            type_=TYPE,
            metric_kind='NOTUSED',
            value_type='NOTUSED',
        )
        descriptor.delete()

        request, = connection._requested
        expected_request = {'method': 'DELETE', 'path': '/' + NAME}
        self.assertEqual(request, expected_request)

    def test_fetch(self):
        PROJECT = 'my-project'
        TYPE = 'custom.googleapis.com/my_metric'
        NAME = 'projects/{project}/metricDescriptors/{type}'.format(
            project=PROJECT, type=TYPE)
        DESCRIPTION = 'This is my metric.'

        METRIC_DESCRIPTOR = {
            'name': NAME,
            'type': TYPE,
            'metricKind': 'GAUGE',
            'valueType': 'DOUBLE',
            'description': DESCRIPTION,
        }

        connection = _Connection(METRIC_DESCRIPTOR)
        client = _Client(project=PROJECT, connection=connection)
        descriptor = self._getTargetClass()._fetch(client, TYPE)

        self.assertIs(descriptor.client, client)
        self.assertEqual(descriptor.name, NAME)
        self.assertEqual(descriptor.type, TYPE)
        self.assertEqual(descriptor.description, DESCRIPTION)

        request, = connection._requested
        expected_request = {'method': 'GET', 'path': '/' + NAME}
        self.assertEqual(request, expected_request)

    def test_list(self):
        PROJECT = 'my-project'
        PATH = 'projects/{project}/metricDescriptors/'.format(project=PROJECT)

        TYPE1 = 'custom.googleapis.com/my_metric_1'
        DESCRIPTION1 = 'This is my first metric.'
        NAME1 = PATH + TYPE1
        METRIC_DESCRIPTOR1 = {
            'name': NAME1,
            'type': TYPE1,
            'metricKind': 'GAUGE',
            'valueType': 'DOUBLE',
            'description': DESCRIPTION1,
        }

        TYPE2 = 'custom.googleapis.com/my_metric_2'
        DESCRIPTION2 = 'This is my second metric.'
        NAME2 = PATH + TYPE2
        METRIC_DESCRIPTOR2 = {
            'name': NAME2,
            'type': TYPE2,
            'metricKind': 'GAUGE',
            'valueType': 'DOUBLE',
            'description': DESCRIPTION2,
        }

        RESPONSE = {
            'metricDescriptors': [METRIC_DESCRIPTOR1, METRIC_DESCRIPTOR2],
        }

        connection = _Connection(RESPONSE)
        client = _Client(project=PROJECT, connection=connection)
        descriptors = self._getTargetClass()._list(client)

        self.assertEqual(len(descriptors), 2)
        descriptor1, descriptor2 = descriptors

        self.assertIs(descriptor1.client, client)
        self.assertEqual(descriptor1.name, NAME1)
        self.assertEqual(descriptor1.type, TYPE1)
        self.assertEqual(descriptor1.description, DESCRIPTION1)

        self.assertIs(descriptor2.client, client)
        self.assertEqual(descriptor2.name, NAME2)
        self.assertEqual(descriptor2.type, TYPE2)
        self.assertEqual(descriptor2.description, DESCRIPTION2)

        request, = connection._requested
        expected_request = {'method': 'GET', 'path': '/' + PATH,
                            'query_params': {}}
        self.assertEqual(request, expected_request)

    def test_list_paged(self):
        from gcloud.exceptions import NotFound

        PROJECT = 'my-project'
        PATH = 'projects/{project}/metricDescriptors/'.format(project=PROJECT)

        TYPE1 = 'custom.googleapis.com/my_metric_1'
        DESCRIPTION1 = 'This is my first metric.'
        NAME1 = PATH + TYPE1
        METRIC_DESCRIPTOR1 = {
            'name': NAME1,
            'type': TYPE1,
            'metricKind': 'GAUGE',
            'valueType': 'DOUBLE',
            'description': DESCRIPTION1,
        }

        TYPE2 = 'custom.googleapis.com/my_metric_2'
        DESCRIPTION2 = 'This is my second metric.'
        NAME2 = PATH + TYPE2
        METRIC_DESCRIPTOR2 = {
            'name': NAME2,
            'type': TYPE2,
            'metricKind': 'GAUGE',
            'valueType': 'DOUBLE',
            'description': DESCRIPTION2,
        }

        TOKEN = 'second-page-please'
        RESPONSE1 = {
            'metricDescriptors': [METRIC_DESCRIPTOR1],
            'nextPageToken': TOKEN,
        }
        RESPONSE2 = {
            'metricDescriptors': [METRIC_DESCRIPTOR2],
        }

        connection = _Connection(RESPONSE1, RESPONSE2)
        client = _Client(project=PROJECT, connection=connection)
        descriptors = self._getTargetClass()._list(client)

        self.assertEqual(len(descriptors), 2)
        descriptor1, descriptor2 = descriptors

        self.assertEqual(descriptor1.name, NAME1)
        self.assertEqual(descriptor1.type, TYPE1)
        self.assertEqual(descriptor1.description, DESCRIPTION1)

        self.assertEqual(descriptor2.name, NAME2)
        self.assertEqual(descriptor2.type, TYPE2)
        self.assertEqual(descriptor2.description, DESCRIPTION2)

        request1, request2 = connection._requested
        expected_request1 = {'method': 'GET', 'path': '/' + PATH,
                             'query_params': {}}
        expected_request2 = {'method': 'GET', 'path': '/' + PATH,
                             'query_params': {'pageToken': TOKEN}}
        self.assertEqual(request1, expected_request1)
        self.assertEqual(request2, expected_request2)

        with self.assertRaises(NotFound):
            self._getTargetClass()._list(client)

    def test_list_filtered(self):
        PROJECT = 'my-project'
        PATH = 'projects/{project}/metricDescriptors/'.format(project=PROJECT)

        # Request only custom metrics.
        FILTER = 'metric.type = starts_with("custom.googleapis.com/")'

        # But let's say there are no custom metrics.
        RESPONSE = {'metricDescriptors': []}

        connection = _Connection(RESPONSE)
        client = _Client(project=PROJECT, connection=connection)
        descriptors = self._getTargetClass()._list(client, FILTER)

        self.assertEqual(len(descriptors), 0)

        request, = connection._requested
        expected_request = {'method': 'GET', 'path': '/' + PATH,
                            'query_params': {'filter': FILTER}}
        self.assertEqual(request, expected_request)

    def test_list_filtered_by_type_prefix(self):
        PROJECT = 'my-project'
        PATH = 'projects/{project}/metricDescriptors/'.format(project=PROJECT)

        # Request only custom metrics.
        PREFIX = 'custom.googleapis.com/'
        FILTER = 'metric.type = starts_with("{prefix}")'.format(prefix=PREFIX)

        # But let's say there are no custom metrics.
        RESPONSE = {'metricDescriptors': []}

        connection = _Connection(RESPONSE)
        client = _Client(project=PROJECT, connection=connection)
        descriptors = self._getTargetClass()._list(client, type_prefix=PREFIX)

        self.assertEqual(len(descriptors), 0)

        request, = connection._requested
        expected_request = {'method': 'GET', 'path': '/' + PATH,
                            'query_params': {'filter': FILTER}}
        self.assertEqual(request, expected_request)


class TestMetric(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.monitoring.metric import Metric
        return Metric

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        TYPE = 'appengine.googleapis.com/http/server/response_count'
        LABELS = {
            'response_code': 200,
            'loading': False,
        }
        metric = self._makeOne(type=TYPE, labels=LABELS)
        self.assertEqual(metric.type, TYPE)
        self.assertEqual(metric.labels, LABELS)

    def test_from_dict(self):
        TYPE = 'appengine.googleapis.com/http/server/response_count'
        LABELS = {
            'response_code': 200,
            'loading': False,
        }
        info = {
            'type': TYPE,
            'labels': LABELS,
        }
        metric = self._getTargetClass()._from_dict(info)
        self.assertEqual(metric.type, TYPE)
        self.assertEqual(metric.labels, LABELS)

    def test_from_dict_defaults(self):
        TYPE = 'appengine.googleapis.com/http/server/response_count'
        info = {'type': TYPE}
        metric = self._getTargetClass()._from_dict(info)
        self.assertEqual(metric.type, TYPE)
        self.assertEqual(metric.labels, {})


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
