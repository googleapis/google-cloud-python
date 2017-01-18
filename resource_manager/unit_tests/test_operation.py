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

from google.cloud.resource_manager.operation import _Status


class TestOperation(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.resource_manager.operation import Operation
        return Operation

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor_defaults(self):
        client = object()
        OPERATION_NAME = 'operations/pc.1234567980'
        operation = self._make_one(name=OPERATION_NAME, client=client)
        self.assertEqual(operation.name, OPERATION_NAME)
        self.assertEqual(operation._client, client)
        self.assertIsNone(operation.metadata)
        self.assertFalse(operation.done)
        self.assertIsNone(operation.error)
        self.assertIsNone(operation.response)

    def test_constructor_explicit(self):
        client = object()
        OPERATION_NAME = 'operations/pc.1234567980'
        OPERATION_METADATA = {
            '@type': ('type.googleapis.com/'
                      'google.cloudresourcemanager.v1.ProjectCreationStatus')
        }
        operation = self._make_one(name=OPERATION_NAME, client=client,
                                   metadata=OPERATION_METADATA)
        self.assertEqual(operation.name, OPERATION_NAME)
        self.assertEqual(operation._client, client)
        self.assertFalse(operation.done)
        self.assertEqual(operation.metadata, OPERATION_METADATA)
        self.assertIsNone(operation.error)
        self.assertIsNone(operation.response)

    def test_from_api_repr(self):
        client = object()
        OPERATION_NAME = 'operations/pc.1234567980'
        OPERATION_METADATA = {
            '@type': ('type.googleapis.com/'
                      'google.cloudresourcemanager.v1.ProjectCreationStatus')
        }
        OPERATION_STATUS = {
            'code': 100,
            'message': 'Status Message',
            'details': [
                {
                    '@type': 'message details',
                    'field1': 12345
                }
            ]
        }
        resource = {
            'name': OPERATION_NAME,
            'metadata': OPERATION_METADATA,
            'error': OPERATION_STATUS
        }
        operation = self._get_target_class().from_api_repr(resource, client)
        self.assertEqual(operation._client, client)
        self.assertEqual(operation.name, OPERATION_NAME)
        self.assertEqual(operation.metadata, OPERATION_METADATA)
        self.assertFalse(operation.done)
        self.assertEqual(operation.error,
                         _Status.from_api_repr(OPERATION_STATUS))

    def test_full_name(self):
        OPERATION_NAME = 'operations/xy.1234567890'
        operation = self._make_one(OPERATION_NAME, None)
        self.assertEqual('%s' % OPERATION_NAME, operation.full_name)

    def test_full_name_missing_id(self):
        operation = self._make_one(None, None)
        with self.assertRaises(ValueError):
            self.assertIsNone(operation.full_name)

    def test_path(self):
        OPERATION_NAME = 'operations/xy.1234567890'
        operation = self._make_one(OPERATION_NAME, None)
        self.assertEqual('/%s' % OPERATION_NAME, operation.path)

    def test_get(self):
        OPERATION_NAME = 'operations/ab.0987654321'
        OPERATION_RESOURCE = {
            'name': OPERATION_NAME,
            'metadata': {
                '@type': 'ProjectCreateStatus'
            },
            'done': True,
            'response': {
                'key': 'value'
            },
        }
        connection = _Connection(OPERATION_RESOURCE)
        client = _Client(connection=connection)
        operation = self._make_one(OPERATION_NAME, client)
        self.assertFalse(operation.done)
        self.assertIsNone(operation.metadata)
        self.assertIsNone(operation.error)
        self.assertIsNone(operation.response)
        operation.get(client)
        self.assertEqual(operation.name, OPERATION_RESOURCE['name'])
        self.assertTrue(operation.done)
        self.assertEqual(operation.metadata, OPERATION_RESOURCE['metadata'])
        self.assertEqual(operation.response, OPERATION_RESOURCE['response'])

        request, = connection._requested
        # NOTE: data is not in the request since a GET request.
        expected_request = {
            'method': 'GET',
            'path': operation.path,
        }
        self.assertEqual(request, expected_request)

    def test_get_with_missing_client(self):
        OPERATION_NAME = 'operations/qr.2244668800'
        operation = self._make_one(OPERATION_NAME, None)
        with self.assertRaises(AttributeError):
            operation.get()

    def test_get_not_found(self):
        OPERATION_NAME = 'operations/qr.2244668800'
        connection = _Connection()
        client = _Client(connection=connection)
        operation = self._make_one(OPERATION_NAME, client)
        from google.cloud.exceptions import NotFound
        with self.assertRaises(NotFound):
            operation.get()


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        from google.cloud.exceptions import NotFound
        self._requested.append(kw)

        try:
            response, self._responses = self._responses[0], self._responses[1:]
        except:
            raise NotFound('miss')
        else:
            return response


class _Client(object):

    def __init__(self, connection=None):
        self._connection = connection
