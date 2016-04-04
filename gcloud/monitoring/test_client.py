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


class TestClient(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.monitoring.client import Client
        return Client

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_fetch_metric_descriptor(self):
        PROJECT = 'my-project'
        TYPE = 'custom.googleapis.com/my-metric'
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

        self.assertEqual(descriptor.name, NAME)
        self.assertEqual(descriptor.type, TYPE)
        self.assertEqual(descriptor.description, DESCRIPTION)

        request, = connection._requested
        expected_request = {'method': 'GET', 'path': '/' + NAME}
        self.assertEqual(request, expected_request)

    def test_list_metric_descriptors(self):
        PROJECT = 'my-project'
        PATH = 'projects/{project}/metricDescriptors/'.format(project=PROJECT)

        TYPE1 = 'custom.googleapis.com/my-metric-1'
        DESCRIPTION1 = 'This is my first metric.'
        NAME1 = PATH + TYPE1
        METRIC_DESCRIPTOR1 = {
            'name': NAME1,
            'type': TYPE1,
            'metricKind': 'GAUGE',
            'valueType': 'DOUBLE',
            'description': DESCRIPTION1,
        }

        TYPE2 = 'custom.googleapis.com/my-metric-2'
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

    def test_fetch_resource_descriptor(self):
        PROJECT = 'my-project'
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
        PROJECT = 'my-project'
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
        except IndexError:  # pragma: NO COVER
            raise NotFound('miss')
