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


class TestResourceDescriptor(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.monitoring.resource import ResourceDescriptor
        return ResourceDescriptor

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        from gcloud.monitoring.label import LabelDescriptor

        TYPE = 'gce_instance'
        NAME = 'projects/my-project/monitoredResourceDescriptors/' + TYPE
        DISPLAY_NAME = 'GCE Instance'
        DESCRIPTION = 'A VM instance hosted in Google Compute Engine.'
        LABELS = [
            LabelDescriptor(key='project_id', value_type='STRING',
                            description='The ID of the GCP project...'),
            LabelDescriptor(key='instance_id', value_type='STRING',
                            description='The VM instance identifier...'),
            LabelDescriptor(key='zone', value_type='STRING',
                            description='The GCE zone...'),
        ]

        descriptor = self._makeOne(
            name=NAME,
            type_=TYPE,
            display_name=DISPLAY_NAME,
            description=DESCRIPTION,
            labels=LABELS,
        )

        self.assertEqual(descriptor.name, NAME)
        self.assertEqual(descriptor.type, TYPE)
        self.assertEqual(descriptor.display_name, DISPLAY_NAME)
        self.assertEqual(descriptor.description, DESCRIPTION)
        self.assertEqual(descriptor.labels, LABELS)

    def test_from_dict(self):
        TYPE = 'gce_instance'
        NAME = 'projects/my-project/monitoredResourceDescriptors/' + TYPE
        DISPLAY_NAME = 'GCE Instance'
        DESCRIPTION = 'A VM instance hosted in Google Compute Engine.'
        LABEL1 = {'key': 'project_id', 'valueType': 'STRING',
                  'description': 'The ID of the GCP project...'}
        LABEL2 = {'key': 'instance_id', 'valueType': 'STRING',
                  'description': 'The VM instance identifier...'}
        LABEL3 = {'key': 'zone', 'valueType': 'STRING',
                  'description': 'The GCE zone...'}

        info = {
            'name': NAME,
            'type': TYPE,
            'displayName': DISPLAY_NAME,
            'description': DESCRIPTION,
            'labels': [LABEL1, LABEL2, LABEL3],
        }
        descriptor = self._getTargetClass()._from_dict(info)

        self.assertEqual(descriptor.name, NAME)
        self.assertEqual(descriptor.type, TYPE)
        self.assertEqual(descriptor.display_name, DISPLAY_NAME)
        self.assertEqual(descriptor.description, DESCRIPTION)

        self.assertEqual(len(descriptor.labels), 3)
        label1, label2, label3 = descriptor.labels
        self.assertEqual(label1.key, LABEL1['key'])
        self.assertEqual(label2.key, LABEL2['key'])
        self.assertEqual(label3.key, LABEL3['key'])

    def test_from_dict_defaults(self):
        TYPE = 'gce_instance'
        NAME = 'projects/my-project/monitoredResourceDescriptors/' + TYPE

        info = {
            'name': NAME,
            'type': TYPE,
        }
        descriptor = self._getTargetClass()._from_dict(info)

        self.assertEqual(descriptor.name, NAME)
        self.assertEqual(descriptor.type, TYPE)
        self.assertEqual(descriptor.display_name, '')
        self.assertEqual(descriptor.description, '')
        self.assertEqual(descriptor.labels, ())

    def test_fetch(self):
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

        connection = _Connection(RESOURCE_DESCRIPTOR)
        client = _Client(project=PROJECT, connection=connection)
        descriptor = self._getTargetClass()._fetch(client, TYPE)

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

    def test_list(self):
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

        connection = _Connection(RESPONSE)
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

        request, = connection._requested
        expected_request = {'method': 'GET', 'path': '/' + PATH,
                            'query_params': {}}
        self.assertEqual(request, expected_request)

    def test_list_paged(self):
        from gcloud.exceptions import NotFound

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

        TOKEN = 'second-page-please'
        RESPONSE1 = {
            'resourceDescriptors': [RESOURCE_DESCRIPTOR1],
            'nextPageToken': TOKEN,
        }
        RESPONSE2 = {
            'resourceDescriptors': [RESOURCE_DESCRIPTOR2],
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
        PATH = 'projects/{project}/monitoredResourceDescriptors/'.format(
            project=PROJECT)

        # Request only resources with type names that start with "foobar_".
        FILTER = 'resource.type = starts_with("foobar_")'

        # But there are none.
        RESPONSE = {'resourceDescriptors': []}

        connection = _Connection(RESPONSE)
        client = _Client(project=PROJECT, connection=connection)
        descriptors = self._getTargetClass()._list(client, FILTER)

        self.assertEqual(len(descriptors), 0)

        request, = connection._requested
        expected_request = {'method': 'GET', 'path': '/' + PATH,
                            'query_params': {'filter': FILTER}}
        self.assertEqual(request, expected_request)


class TestResource(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.monitoring.resource import Resource
        return Resource

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        TYPE = 'gce_instance'
        LABELS = {
            'project_id': 'my-project',
            'instance_id': '1234567890123456789',
            'zone': 'us-central1-a',
        }
        resource = self._makeOne(type=TYPE, labels=LABELS)
        self.assertEqual(resource.type, TYPE)
        self.assertEqual(resource.labels, LABELS)

    def test_from_dict(self):
        TYPE = 'gce_instance'
        LABELS = {
            'project_id': 'my-project',
            'instance_id': '1234567890123456789',
            'zone': 'us-central1-a',
        }
        info = {
            'type': TYPE,
            'labels': LABELS,
        }
        resource = self._getTargetClass()._from_dict(info)
        self.assertEqual(resource.type, TYPE)
        self.assertEqual(resource.labels, LABELS)

    def test_from_dict_defaults(self):
        TYPE = 'gce_instance'
        info = {'type': TYPE}
        resource = self._getTargetClass()._from_dict(info)
        self.assertEqual(resource.type, TYPE)
        self.assertEqual(resource.labels, {})


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
