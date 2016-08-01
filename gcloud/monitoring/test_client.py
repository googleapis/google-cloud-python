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


class TestClient(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.monitoring.client import Client
        return Client

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_query(self):
        import datetime
        from gcloud._helpers import _datetime_to_rfc3339
        from gcloud.exceptions import NotFound

        START_TIME = datetime.datetime(2016, 4, 6, 22, 5, 0)
        END_TIME = datetime.datetime(2016, 4, 6, 22, 10, 0)
        MINUTES = 5

        METRIC_TYPE = 'compute.googleapis.com/instance/cpu/utilization'
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

        METRIC_KIND = 'GAUGE'
        VALUE_TYPE = 'DOUBLE'

        TS1 = '2016-04-06T22:05:00.042Z'
        TS2 = '2016-04-06T22:05:01.042Z'
        TS3 = '2016-04-06T22:05:02.042Z'

        VAL1 = 0.1
        VAL2 = 0.2

        def P(timestamp, value):
            return {
                'interval': {'startTime': timestamp, 'endTime': timestamp},
                'value': {'doubleValue': value},
            }

        SERIES1 = {
            'metric': {'type': METRIC_TYPE, 'labels': METRIC_LABELS},
            'resource': {'type': RESOURCE_TYPE, 'labels': RESOURCE_LABELS},
            'metricKind': METRIC_KIND,
            'valueType': VALUE_TYPE,
            'points': [P(TS3, VAL1), P(TS2, VAL1), P(TS1, VAL1)],
        }
        SERIES2 = {
            'metric': {'type': METRIC_TYPE, 'labels': METRIC_LABELS2},
            'resource': {'type': RESOURCE_TYPE, 'labels': RESOURCE_LABELS2},
            'metricKind': METRIC_KIND,
            'valueType': VALUE_TYPE,
            'points': [P(TS3, VAL2), P(TS2, VAL2), P(TS1, VAL2)],
        }

        RESPONSE = {'timeSeries': [SERIES1, SERIES2]}

        client = self._makeOne(project=PROJECT, credentials=_Credentials())
        connection = client.connection = _Connection(RESPONSE)

        # A simple query. In practice, it can be very convenient to let the
        # end time default to the start of the current minute.
        query = client.query(METRIC_TYPE, end_time=END_TIME, minutes=MINUTES)
        response = list(query)

        self.assertEqual(len(response), 2)
        series1, series2 = response

        self.assertEqual(series1.metric.type, METRIC_TYPE)
        self.assertEqual(series2.metric.type, METRIC_TYPE)
        self.assertEqual(series1.metric.labels, METRIC_LABELS)
        self.assertEqual(series2.metric.labels, METRIC_LABELS2)

        self.assertEqual(series1.resource.type, RESOURCE_TYPE)
        self.assertEqual(series2.resource.type, RESOURCE_TYPE)
        self.assertEqual(series1.resource.labels, RESOURCE_LABELS)
        self.assertEqual(series2.resource.labels, RESOURCE_LABELS2)

        self.assertEqual(series1.metric_kind, METRIC_KIND)
        self.assertEqual(series2.metric_kind, METRIC_KIND)
        self.assertEqual(series1.value_type, VALUE_TYPE)
        self.assertEqual(series2.value_type, VALUE_TYPE)

        self.assertEqual([p.value for p in series1.points], [VAL1, VAL1, VAL1])
        self.assertEqual([p.value for p in series2.points], [VAL2, VAL2, VAL2])
        self.assertEqual([p.end_time for p in series1.points], [TS1, TS2, TS3])
        self.assertEqual([p.end_time for p in series2.points], [TS1, TS2, TS3])

        expected_request = {
            'method': 'GET',
            'path': '/projects/{project}/timeSeries/'.format(project=PROJECT),
            'query_params': [
                ('filter', 'metric.type = "{type}"'.format(type=METRIC_TYPE)),
                ('interval.endTime', _datetime_to_rfc3339(END_TIME)),
                ('interval.startTime', _datetime_to_rfc3339(START_TIME)),
            ],
        }

        request, = connection._requested
        self.assertEqual(request, expected_request)

        with self.assertRaises(NotFound):
            list(query)

    def test_metric_descriptor_factory(self):
        TYPE = 'custom.googleapis.com/my_metric'
        METRIC_KIND = 'GAUGE'
        VALUE_TYPE = 'DOUBLE'
        DESCRIPTION = 'This is my metric.'

        client = self._makeOne(project=PROJECT, credentials=_Credentials())
        client.connection = _Connection()   # For safety's sake.
        descriptor = client.metric_descriptor(TYPE,
                                              metric_kind=METRIC_KIND,
                                              value_type=VALUE_TYPE,
                                              description=DESCRIPTION)

        self.assertIs(descriptor.client, client)

        self.assertIsNone(descriptor.name)
        self.assertEqual(descriptor.type, TYPE)
        self.assertEqual(descriptor.labels, ())

        self.assertEqual(descriptor.metric_kind, METRIC_KIND)
        self.assertEqual(descriptor.value_type, VALUE_TYPE)

        self.assertEqual(descriptor.unit, '')
        self.assertEqual(descriptor.description, DESCRIPTION)
        self.assertEqual(descriptor.display_name, '')

    def test_fetch_metric_descriptor(self):
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

        # This test is identical to TestMetricDescriptor.test_fetch()
        # except for the following three lines.
        client = self._makeOne(project=PROJECT, credentials=_Credentials())
        connection = client.connection = _Connection(METRIC_DESCRIPTOR)
        descriptor = client.fetch_metric_descriptor(TYPE)

        self.assertIs(descriptor.client, client)
        self.assertEqual(descriptor.name, NAME)
        self.assertEqual(descriptor.type, TYPE)
        self.assertEqual(descriptor.description, DESCRIPTION)

        request, = connection._requested
        expected_request = {'method': 'GET', 'path': '/' + NAME}
        self.assertEqual(request, expected_request)

    def test_list_metric_descriptors(self):
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

        # This test is identical to TestMetricDescriptor.test_list()
        # except for the following three lines.
        client = self._makeOne(project=PROJECT, credentials=_Credentials())
        connection = client.connection = _Connection(RESPONSE)
        descriptors = client.list_metric_descriptors()

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

    def test_fetch_resource_descriptor(self):
        TYPE = 'gce_instance'
        NAME = 'projects/{project}/monitoredResourceDescriptors/{type}'.format(
            project=PROJECT, type=TYPE)
        DISPLAY_NAME = 'GCE Instance'
        DESCRIPTION = 'A VM instance hosted in Google Compute Engine.'
        LABEL1 = {'key': 'project_id', 'valueType': 'STRING',
                  'description': 'The ID of the GCP project...'}
        LABEL2 = {'key': 'instance_id', 'valueType': 'STRING',
                  'description': 'The VM instance identifier...'}
        LABEL3 = {'key': 'zone', 'valueType': 'STRING',
                  'description': 'The GCE zone...'}

        RESOURCE_DESCRIPTOR = {
            'name': NAME,
            'type': TYPE,
            'displayName': DISPLAY_NAME,
            'description': DESCRIPTION,
            'labels': [LABEL1, LABEL2, LABEL3],
        }

        # This test is identical to TestResourceDescriptor.test_fetch()
        # except for the following three lines.
        client = self._makeOne(project=PROJECT, credentials=_Credentials())
        connection = client.connection = _Connection(RESOURCE_DESCRIPTOR)
        descriptor = client.fetch_resource_descriptor(TYPE)

        self.assertEqual(descriptor.name, NAME)
        self.assertEqual(descriptor.type, TYPE)
        self.assertEqual(descriptor.display_name, DISPLAY_NAME)
        self.assertEqual(descriptor.description, DESCRIPTION)

        self.assertEqual(len(descriptor.labels), 3)
        label1, label2, label3 = descriptor.labels
        self.assertEqual(label1.key, LABEL1['key'])
        self.assertEqual(label2.key, LABEL2['key'])
        self.assertEqual(label3.key, LABEL3['key'])

        request, = connection._requested
        expected_request = {'method': 'GET', 'path': '/' + NAME}
        self.assertEqual(request, expected_request)

    def test_list_resource_descriptors(self):
        PATH = 'projects/{project}/monitoredResourceDescriptors/'.format(
            project=PROJECT)

        TYPE1 = 'custom.googleapis.com/resource-1'
        DESCRIPTION1 = 'This is the first resource.'
        NAME1 = PATH + TYPE1
        RESOURCE_DESCRIPTOR1 = {
            'name': NAME1,
            'type': TYPE1,
            'description': DESCRIPTION1,
        }

        TYPE2 = 'custom.googleapis.com/resource-2'
        DESCRIPTION2 = 'This is the second resource.'
        NAME2 = PATH + TYPE2
        RESOURCE_DESCRIPTOR2 = {
            'name': NAME2,
            'type': TYPE2,
            'description': DESCRIPTION2,
        }

        RESPONSE = {
            'resourceDescriptors':
                [RESOURCE_DESCRIPTOR1, RESOURCE_DESCRIPTOR2],
        }

        # This test is identical to TestResourceDescriptor.test_list()
        # except for the following three lines.
        client = self._makeOne(project=PROJECT, credentials=_Credentials())
        connection = client.connection = _Connection(RESPONSE)
        descriptors = client.list_resource_descriptors()

        self.assertEqual(len(descriptors), 2)
        descriptor1, descriptor2 = descriptors

        self.assertEqual(descriptor1.name, NAME1)
        self.assertEqual(descriptor1.type, TYPE1)
        self.assertEqual(descriptor1.description, DESCRIPTION1)

        self.assertEqual(descriptor2.name, NAME2)
        self.assertEqual(descriptor2.type, TYPE2)
        self.assertEqual(descriptor2.description, DESCRIPTION2)

        request, = connection._requested
        expected_request = {'method': 'GET', 'path': '/' + PATH,
                            'query_params': {}}
        self.assertEqual(request, expected_request)


class _Credentials(object):

    _scopes = None

    @staticmethod
    def create_scoped_required():
        return True

    def create_scoped(self, scope):
        self._scopes = scope
        return self


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
