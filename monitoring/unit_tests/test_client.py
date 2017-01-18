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

import mock


PROJECT = 'my-project'


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


class TestClient(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.monitoring.client import Client

        return Client

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_query(self):
        import datetime
        from google.cloud._helpers import _datetime_to_rfc3339
        from google.cloud.exceptions import NotFound

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

        client = self._make_one(
            project=PROJECT, credentials=_make_credentials())
        connection = client._connection = _Connection(RESPONSE)

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

        client = self._make_one(
            project=PROJECT, credentials=_make_credentials())
        client._connection = _Connection()   # For safety's sake.
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

    def test_metric_factory(self):
        TYPE = 'custom.googleapis.com/my_metric'
        LABELS = {
            'instance_name': 'my-instance'
        }

        client = self._make_one(
            project=PROJECT, credentials=_make_credentials())
        client._connection = _Connection()   # For safety's sake.
        metric = client.metric(TYPE, LABELS)
        self.assertEqual(metric.type, TYPE)
        self.assertEqual(metric.labels, LABELS)

    def test_resource_factory(self):
        TYPE = 'https://cloud.google.com/monitoring/api/resources'
        LABELS = {
            'instance_id': 'my-instance-id',
            'zone': 'us-central1-f'
        }

        client = self._make_one(
            project=PROJECT, credentials=_make_credentials())
        client._connection = _Connection()   # For safety's sake.
        resource = client.resource(TYPE, LABELS)
        self.assertEqual(resource.type, TYPE)
        self.assertEqual(resource.labels, LABELS)

    def test_timeseries_factory_gauge(self):
        import datetime
        from google.cloud._helpers import _datetime_to_rfc3339

        METRIC_TYPE = 'custom.googleapis.com/my_metric'
        METRIC_LABELS = {
            'status': 'successful'
        }

        RESOURCE_TYPE = 'gce_instance'
        RESOURCE_LABELS = {
            'instance_id': '1234567890123456789',
            'zone': 'us-central1-f'
        }

        VALUE = 42
        TIME1 = datetime.datetime.utcnow()
        TIME1_STR = _datetime_to_rfc3339(TIME1, ignore_zone=False)

        client = self._make_one(
            project=PROJECT, credentials=_make_credentials())
        client._connection = _Connection()   # For safety's sake.
        metric = client.metric(METRIC_TYPE, METRIC_LABELS)
        resource = client.resource(RESOURCE_TYPE, RESOURCE_LABELS)

        # Construct a time series assuming a gauge metric.
        timeseries = client.time_series(metric, resource, VALUE,
                                        end_time=TIME1)
        self.assertEqual(timeseries.metric, metric)
        self.assertEqual(timeseries.resource, resource)
        self.assertEqual(len(timeseries.points), 1)
        self.assertEqual(timeseries.points[0].value, VALUE)
        self.assertIsNone(timeseries.points[0].start_time)
        self.assertEqual(timeseries.points[0].end_time, TIME1_STR)

        TIME2 = datetime.datetime.utcnow()
        TIME2_STR = _datetime_to_rfc3339(TIME2, ignore_zone=False)
        # Construct a time series assuming a gauge metric using the current
        # time
        with mock.patch('google.cloud.monitoring.client._UTCNOW',
                        new=lambda: TIME2):
            timeseries_no_end = client.time_series(metric, resource, VALUE)

        self.assertEqual(timeseries_no_end.points[0].end_time, TIME2_STR)
        self.assertIsNone(timeseries_no_end.points[0].start_time)

    def test_timeseries_factory_cumulative(self):
        import datetime
        from google.cloud._helpers import _datetime_to_rfc3339

        MY_CUMULATIVE_METRIC = 'custom.googleapis.com/my_cumulative_metric'
        METRIC_LABELS = {
            'status': 'successful'
        }

        RESOURCE_TYPE = 'gce_instance'
        RESOURCE_LABELS = {
            'instance_id': '1234567890123456789',
            'zone': 'us-central1-f'
        }

        client = self._make_one(
            project=PROJECT, credentials=_make_credentials())
        client._connection = _Connection()   # For safety's sake.
        resource = client.resource(RESOURCE_TYPE, RESOURCE_LABELS)

        VALUE = 42
        VALUE2 = 43
        RESET_TIME = datetime.datetime.utcnow()
        TIME1 = datetime.datetime.utcnow()
        TIME2 = datetime.datetime.utcnow()

        # Construct a couple of time series assuming a cumulative metric.
        cumulative_metric = client.metric(MY_CUMULATIVE_METRIC, METRIC_LABELS)
        cumulative_timeseries = client.time_series(cumulative_metric,
                                                   resource,
                                                   VALUE,
                                                   start_time=RESET_TIME,
                                                   end_time=TIME1)

        cumulative_timeseries2 = client.time_series(cumulative_metric,
                                                    resource,
                                                    VALUE2,
                                                    start_time=RESET_TIME,
                                                    end_time=TIME2)

        RESET_TIME_STR = _datetime_to_rfc3339(RESET_TIME, ignore_zone=False)
        TIME1_STR = _datetime_to_rfc3339(TIME1, ignore_zone=False)
        TIME2_STR = _datetime_to_rfc3339(TIME2, ignore_zone=False)

        self.assertEqual(cumulative_timeseries.points[0].start_time,
                         RESET_TIME_STR)
        self.assertEqual(cumulative_timeseries.points[0].end_time, TIME1_STR)
        self.assertEqual(cumulative_timeseries.points[0].value, VALUE)
        self.assertEqual(cumulative_timeseries2.points[0].start_time,
                         RESET_TIME_STR)
        self.assertEqual(cumulative_timeseries2.points[0].end_time,
                         TIME2_STR)
        self.assertEqual(cumulative_timeseries2.points[0].value, VALUE2)

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
        client = self._make_one(
            project=PROJECT, credentials=_make_credentials())
        connection = client._connection = _Connection(METRIC_DESCRIPTOR)
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
        client = self._make_one(
            project=PROJECT, credentials=_make_credentials())
        connection = client._connection = _Connection(RESPONSE)
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
        client = self._make_one(
            project=PROJECT, credentials=_make_credentials())
        connection = client._connection = _Connection(RESOURCE_DESCRIPTOR)
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
        client = self._make_one(
            project=PROJECT, credentials=_make_credentials())
        connection = client._connection = _Connection(RESPONSE)
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

    def test_group(self):
        GROUP_ID = 'GROUP_ID'
        DISPLAY_NAME = 'My Group'
        PARENT_ID = 'PARENT_ID'
        FILTER = 'resource.type = "gce_instance"'
        IS_CLUSTER = False

        client = self._make_one(
            project=PROJECT, credentials=_make_credentials())
        group = client.group(GROUP_ID, display_name=DISPLAY_NAME,
                             parent_id=PARENT_ID, filter_string=FILTER,
                             is_cluster=IS_CLUSTER)

        self.assertEqual(group.id, GROUP_ID)
        self.assertEqual(group.display_name, DISPLAY_NAME)
        self.assertEqual(group.parent_id, PARENT_ID)
        self.assertEqual(group.filter, FILTER)
        self.assertEqual(group.is_cluster, IS_CLUSTER)

    def test_group_defaults(self):
        client = self._make_one(
            project=PROJECT, credentials=_make_credentials())
        group = client.group()

        self.assertIsNone(group.id)
        self.assertIsNone(group.display_name)
        self.assertIsNone(group.parent_id)
        self.assertIsNone(group.filter)
        self.assertFalse(group.is_cluster)

    def test_fetch_group(self):
        PATH = 'projects/{project}/groups/'.format(project=PROJECT)
        GROUP_ID = 'GROUP_ID'
        GROUP_NAME = PATH + GROUP_ID
        DISPLAY_NAME = 'My Group'
        PARENT_ID = 'PARENT_ID'
        PARENT_NAME = PATH + PARENT_ID
        FILTER = 'resource.type = "gce_instance"'
        IS_CLUSTER = False

        GROUP = {
            'name': GROUP_NAME,
            'displayName': DISPLAY_NAME,
            'parentName': PARENT_NAME,
            'filter': FILTER,
            'isCluster': IS_CLUSTER
        }

        client = self._make_one(
            project=PROJECT, credentials=_make_credentials())
        connection = client._connection = _Connection(GROUP)
        group = client.fetch_group(GROUP_ID)

        self.assertEqual(group.id, GROUP_ID)
        self.assertEqual(group.display_name, DISPLAY_NAME)
        self.assertEqual(group.parent_id, PARENT_ID)
        self.assertEqual(group.filter, FILTER)
        self.assertEqual(group.is_cluster, IS_CLUSTER)

        request, = connection._requested
        expected_request = {'method': 'GET', 'path': '/' + GROUP_NAME}
        self.assertEqual(request, expected_request)

    def test_list_groups(self):
        PATH = 'projects/{project}/groups/'.format(project=PROJECT)
        GROUP_NAME = PATH + 'GROUP_ID'
        DISPLAY_NAME = 'My Group'
        PARENT_NAME = PATH + 'PARENT_ID'
        FILTER = 'resource.type = "gce_instance"'
        IS_CLUSTER = False

        GROUP = {
            'name': GROUP_NAME,
            'displayName': DISPLAY_NAME,
            'parentName': PARENT_NAME,
            'filter': FILTER,
            'isCluster': IS_CLUSTER,
        }

        RESPONSE = {
            'group': [GROUP],
        }
        client = self._make_one(
            project=PROJECT, credentials=_make_credentials())
        connection = client._connection = _Connection(RESPONSE)
        groups = client.list_groups()

        self.assertEqual(len(groups), 1)

        group = groups[0]
        self.assertEqual(group.name, GROUP_NAME)
        self.assertEqual(group.display_name, DISPLAY_NAME)
        self.assertEqual(group.parent_name, PARENT_NAME)
        self.assertEqual(group.filter, FILTER)
        self.assertEqual(group.is_cluster, IS_CLUSTER)

        request, = connection._requested
        expected_request = {'method': 'GET', 'path': '/' + PATH,
                            'query_params': {}}
        self.assertEqual(request, expected_request)

    def test_write_time_series(self):
        PATH = '/projects/{project}/timeSeries/'.format(project=PROJECT)
        client = self._make_one(
            project=PROJECT, credentials=_make_credentials())

        RESOURCE_TYPE = 'gce_instance'
        RESOURCE_LABELS = {
            'instance_id': '1234567890123456789',
            'zone': 'us-central1-f'
        }

        METRIC_TYPE = 'custom.googleapis.com/my_metric'
        METRIC_LABELS = {
            'status': 'successful'
        }
        METRIC_TYPE2 = 'custom.googleapis.com/count_404s'
        METRIC_LABELS2 = {
            'request_ip': '127.0.0.1'
        }

        connection = client._connection = _Connection({})

        METRIC = client.metric(METRIC_TYPE, METRIC_LABELS)
        METRIC2 = client.metric(METRIC_TYPE2, METRIC_LABELS2)
        RESOURCE = client.resource(RESOURCE_TYPE, RESOURCE_LABELS)

        TIMESERIES1 = client.time_series(METRIC, RESOURCE, 3)
        TIMESERIES2 = client.time_series(METRIC2, RESOURCE, 3.14)

        expected_data = {
            'timeSeries': [
                TIMESERIES1._to_dict(),
                TIMESERIES2._to_dict()
            ]
        }
        expected_request = {'method': 'POST', 'path': PATH,
                            'data': expected_data}

        client.write_time_series([TIMESERIES1, TIMESERIES2])
        request, = connection._requested
        self.assertEqual(request, expected_request)

    def test_write_point(self):
        import datetime

        PATH = '/projects/{project}/timeSeries/'.format(project=PROJECT)
        client = self._make_one(
            project=PROJECT, credentials=_make_credentials())

        RESOURCE_TYPE = 'gce_instance'
        RESOURCE_LABELS = {
            'instance_id': '1234567890123456789',
            'zone': 'us-central1-f'
        }

        METRIC_TYPE = 'custom.googleapis.com/my_metric'
        METRIC_LABELS = {
            'status': 'successful'
        }

        connection = client._connection = _Connection({})

        METRIC = client.metric(METRIC_TYPE, METRIC_LABELS)
        RESOURCE = client.resource(RESOURCE_TYPE, RESOURCE_LABELS)
        VALUE = 3.14
        TIMESTAMP = datetime.datetime.now()
        TIMESERIES = client.time_series(METRIC, RESOURCE, VALUE, TIMESTAMP)

        expected_request = {'method': 'POST', 'path': PATH,
                            'data': {'timeSeries': [TIMESERIES._to_dict()]}}

        client.write_point(METRIC, RESOURCE, VALUE, TIMESTAMP)
        request, = connection._requested
        self.assertEqual(request, expected_request)


class _Connection(object):

    def __init__(self, *responses):
        self._responses = list(responses)
        self._requested = []

    def api_request(self, **kwargs):
        from google.cloud.exceptions import NotFound

        self._requested.append(kwargs)
        try:
            return self._responses.pop(0)
        except IndexError:
            raise NotFound('miss')
