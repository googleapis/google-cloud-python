# Copyright 2015 Google Inc.
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


class TestProject(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.resource_manager.project import Project

        return Project

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor_defaults(self):
        client = object()
        PROJECT_ID = 'project-id'
        project = self._make_one(PROJECT_ID, client)
        self.assertEqual(project.project_id, PROJECT_ID)
        self.assertEqual(project._client, client)
        self.assertIsNone(project.name)
        self.assertIsNone(project.number)
        self.assertEqual(project.labels, {})
        self.assertIsNone(project.status)
        self.assertIsNone(project.parent)

    def test_constructor_explicit(self):
        client = object()
        PROJECT_ID = 'project-id'
        DISPLAY_NAME = 'name'
        LABELS = {'foo': 'bar'}
        project = self._make_one(PROJECT_ID, client,
                                 name=DISPLAY_NAME, labels=LABELS)
        self.assertEqual(project.project_id, PROJECT_ID)
        self.assertEqual(project._client, client)
        self.assertEqual(project.name, DISPLAY_NAME)
        self.assertIsNone(project.number)
        self.assertEqual(project.labels, LABELS)
        self.assertIsNone(project.status)
        self.assertIsNone(project.parent)

    def test_from_api_repr(self):
        client = object()
        PROJECT_ID = 'project-id'
        PROJECT_NAME = 'My Project Name'
        PROJECT_NUMBER = 12345678
        PROJECT_LABELS = {'env': 'prod'}
        PROJECT_LIFECYCLE_STATE = 'ACTIVE'
        PARENT = {'type': 'organization', 'id': '433637338579'}

        resource = {'projectId': PROJECT_ID,
                    'name': PROJECT_NAME,
                    'projectNumber': PROJECT_NUMBER,
                    'labels': PROJECT_LABELS,
                    'lifecycleState': PROJECT_LIFECYCLE_STATE,
                    'parent': PARENT}
        project = self._get_target_class().from_api_repr(resource, client)
        self.assertEqual(project.project_id, PROJECT_ID)
        self.assertEqual(project._client, client)
        self.assertEqual(project.name, PROJECT_NAME)
        self.assertEqual(project.number, PROJECT_NUMBER)
        self.assertEqual(project.labels, PROJECT_LABELS)
        self.assertEqual(project.status, PROJECT_LIFECYCLE_STATE)
        self.assertEqual(project.parent, PARENT)

    def test_full_name(self):
        PROJECT_ID = 'project-id'
        project = self._make_one(PROJECT_ID, None)
        self.assertEqual('projects/%s' % PROJECT_ID, project.full_name)

    def test_full_name_missing_id(self):
        project = self._make_one(None, None)
        with self.assertRaises(ValueError):
            self.assertIsNone(project.full_name)

    def test_path(self):
        PROJECT_ID = 'project-id'
        project = self._make_one(PROJECT_ID, None)
        self.assertEqual('/projects/%s' % PROJECT_ID, project.path)

    def test_create(self):
        PROJECT_ID = 'project-id'
        PROJECT_NUMBER = 123
        PROJECT_RESOURCE = {
            'projectId': PROJECT_ID,
            'projectNumber': PROJECT_NUMBER,
            'name': 'Project Name',
            'labels': {},
            'lifecycleState': 'ACTIVE',
            'parent': {
                'type': 'organization',
                'id': '433637338589',
            },
        }
        connection = _Connection(PROJECT_RESOURCE)
        client = _Client(connection=connection)
        project = self._make_one(PROJECT_ID, client)
        self.assertIsNone(project.number)
        project.create()
        self.assertEqual(project.number, PROJECT_NUMBER)
        request, = connection._requested

        expected_request = {
            'method': 'POST',
            'data': {
                'projectId': PROJECT_ID,
                'labels': {},
                'name': None,
            },
            'path': '/projects',
        }
        self.assertEqual(request, expected_request)

    def test_reload(self):
        PROJECT_ID = 'project-id'
        PROJECT_NUMBER = 123
        PROJECT_RESOURCE = {
            'projectId': PROJECT_ID,
            'projectNumber': PROJECT_NUMBER,
            'name': 'Project Name',
            'labels': {'env': 'prod'},
            'lifecycleState': 'ACTIVE',
            'parent': {
                'type': 'organization',
                'id': '433637338579',
            },
        }
        connection = _Connection(PROJECT_RESOURCE)
        client = _Client(connection=connection)
        project = self._make_one(PROJECT_ID, client)
        self.assertIsNone(project.number)
        self.assertIsNone(project.name)
        self.assertEqual(project.labels, {})
        self.assertIsNone(project.status)
        project.reload()
        self.assertEqual(project.name, PROJECT_RESOURCE['name'])
        self.assertEqual(project.number, PROJECT_NUMBER)
        self.assertEqual(project.labels, PROJECT_RESOURCE['labels'])
        self.assertEqual(project.status, PROJECT_RESOURCE['lifecycleState'])

        request, = connection._requested
        # NOTE: data is not in the request since a GET request.
        expected_request = {
            'method': 'GET',
            'path': project.path,
        }
        self.assertEqual(request, expected_request)

    def test_exists(self):
        PROJECT_ID = 'project-id'
        connection = _Connection({'projectId': PROJECT_ID})
        client = _Client(connection=connection)
        project = self._make_one(PROJECT_ID, client)
        self.assertTrue(project.exists())

    def test_exists_with_explicitly_passed_client(self):
        PROJECT_ID = 'project-id'
        connection = _Connection({'projectId': PROJECT_ID})
        client = _Client(connection=connection)
        project = self._make_one(PROJECT_ID, None)
        self.assertTrue(project.exists(client=client))

    def test_exists_with_missing_client(self):
        PROJECT_ID = 'project-id'
        project = self._make_one(PROJECT_ID, None)
        with self.assertRaises(AttributeError):
            project.exists()

    def test_exists_not_found(self):
        PROJECT_ID = 'project-id'
        connection = _Connection()
        client = _Client(connection=connection)
        project = self._make_one(PROJECT_ID, client)
        self.assertFalse(project.exists())

    def test_update(self):
        PROJECT_ID = 'project-id'
        PROJECT_NUMBER = 123
        PROJECT_NAME = 'Project Name'
        LABELS = {'env': 'prod'}
        PROJECT_RESOURCE = {
            'projectId': PROJECT_ID,
            'projectNumber': PROJECT_NUMBER,
            'name': PROJECT_NAME,
            'labels': LABELS,
            'lifecycleState': 'ACTIVE',
        }
        connection = _Connection(PROJECT_RESOURCE)
        client = _Client(connection=connection)
        project = self._make_one(PROJECT_ID, client)
        project.name = PROJECT_NAME
        project.labels = LABELS
        project.update()

        request, = connection._requested
        expected_request = {
            'method': 'PUT',
            'data': {
                'name': PROJECT_NAME,
                'labels': LABELS,
                'parent': None,
            },
            'path': project.path,
        }
        self.assertEqual(request, expected_request)

    def test_delete_without_reload_data(self):
        PROJECT_ID = 'project-id'
        PROJECT_NUMBER = 123
        PROJECT_RESOURCE = {
            'projectId': PROJECT_ID,
            'projectNumber': PROJECT_NUMBER,
            'name': 'Project Name',
            'labels': {'env': 'prod'},
            'lifecycleState': 'ACTIVE',
            'parent': {
                'type': 'organization',
                'id': '433637338579',
            },
        }
        connection = _Connection(PROJECT_RESOURCE)
        client = _Client(connection=connection)
        project = self._make_one(PROJECT_ID, client)
        project.delete(reload_data=False)

        request, = connection._requested
        # NOTE: data is not in the request since a DELETE request.
        expected_request = {
            'method': 'DELETE',
            'path': project.path,
        }
        self.assertEqual(request, expected_request)

    def test_delete_with_reload_data(self):
        PROJECT_ID = 'project-id'
        PROJECT_NUMBER = 123
        PROJECT_RESOURCE = {
            'projectId': PROJECT_ID,
            'projectNumber': PROJECT_NUMBER,
            'name': 'Project Name',
            'labels': {'env': 'prod'},
            'lifecycleState': 'ACTIVE',
            'parent': {
                'type': 'organization',
                'id': '433637338579',
            },
        }
        DELETING_PROJECT = PROJECT_RESOURCE.copy()
        DELETING_PROJECT['lifecycleState'] = NEW_STATE = 'DELETE_REQUESTED'

        connection = _Connection(PROJECT_RESOURCE, DELETING_PROJECT)
        client = _Client(connection=connection)
        project = self._make_one(PROJECT_ID, client)
        project.delete(reload_data=True)
        self.assertEqual(project.status, NEW_STATE)

        delete_request, get_request = connection._requested
        # NOTE: data is not in the request since a DELETE request.
        expected_delete_request = {
            'method': 'DELETE',
            'path': project.path,
        }
        self.assertEqual(delete_request, expected_delete_request)

        # NOTE: data is not in the request since a GET request.
        expected_get_request = {
            'method': 'GET',
            'path': project.path,
        }
        self.assertEqual(get_request, expected_get_request)

    def test_undelete_without_reload_data(self):
        PROJECT_ID = 'project-id'
        PROJECT_NUMBER = 123
        PROJECT_RESOURCE = {
            'projectId': PROJECT_ID,
            'projectNumber': PROJECT_NUMBER,
            'name': 'Project Name',
            'labels': {'env': 'prod'},
            'lifecycleState': 'DELETE_REQUESTED',
            'parent': {
                'type': 'organization',
                'id': '433637338579',
            },
        }
        connection = _Connection(PROJECT_RESOURCE)
        client = _Client(connection=connection)
        project = self._make_one(PROJECT_ID, client)
        project.undelete(reload_data=False)

        request, = connection._requested
        # NOTE: data is not in the request, undelete doesn't need it.
        expected_request = {
            'method': 'POST',
            'path': project.path + ':undelete',
        }
        self.assertEqual(request, expected_request)

    def test_undelete_with_reload_data(self):
        PROJECT_ID = 'project-id'
        PROJECT_NUMBER = 123
        PROJECT_RESOURCE = {
            'projectId': PROJECT_ID,
            'projectNumber': PROJECT_NUMBER,
            'name': 'Project Name',
            'labels': {'env': 'prod'},
            'lifecycleState': 'DELETE_REQUESTED',
            'parent': {
                'type': 'organization',
                'id': '433637338579',
            },
        }
        UNDELETED_PROJECT = PROJECT_RESOURCE.copy()
        UNDELETED_PROJECT['lifecycleState'] = NEW_STATE = 'ACTIVE'

        connection = _Connection(PROJECT_RESOURCE, UNDELETED_PROJECT)
        client = _Client(connection=connection)
        project = self._make_one(PROJECT_ID, client)
        project.undelete(reload_data=True)
        self.assertEqual(project.status, NEW_STATE)

        undelete_request, get_request = connection._requested
        # NOTE: data is not in the request, undelete doesn't need it.
        expected_undelete_request = {
            'method': 'POST',
            'path': project.path + ':undelete',
        }
        self.assertEqual(undelete_request, expected_undelete_request)

        # NOTE: data is not in the request since a GET request.
        expected_get_request = {
            'method': 'GET',
            'path': project.path,
        }
        self.assertEqual(get_request, expected_get_request)


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        from google.cloud.exceptions import NotFound

        self._requested.append(kw)

        try:
            response, self._responses = self._responses[0], self._responses[1:]
        except IndexError:
            raise NotFound('miss')
        else:
            return response


class _Client(object):

    def __init__(self, connection=None):
        self._connection = connection
