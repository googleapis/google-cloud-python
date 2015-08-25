# Copyright 2015 Google Inc. All rights reserved.
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

import unittest2


class TestProject(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.resource_manager.project import Project
        return Project

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_constructor_defaults(self):
        client = object()
        PROJECT_ID = 'project-id'
        project = self._makeOne(PROJECT_ID, client)
        self.assertEqual(project.project_id, PROJECT_ID)
        self.assertEqual(project._client, client)
        self.assertEqual(project.name, None)
        self.assertEqual(project.number, None)
        self.assertEqual(project.labels, {})
        self.assertEqual(project.status, None)

    def test_constructor_explicit(self):
        client = object()
        PROJECT_ID = 'project-id'
        DISPLAY_NAME = 'name'
        LABELS = {'foo': 'bar'}
        project = self._makeOne(PROJECT_ID, client,
                                name=DISPLAY_NAME, labels=LABELS)
        self.assertEqual(project.project_id, PROJECT_ID)
        self.assertEqual(project._client, client)
        self.assertEqual(project.name, DISPLAY_NAME)
        self.assertEqual(project.number, None)
        self.assertEqual(project.labels, LABELS)
        self.assertEqual(project.status, None)

    def test_from_api_repr(self):
        client = object()
        PROJECT_ID = 'project-id'
        PROJECT_NAME = 'My Project Name'
        PROJECT_NUMBER = 12345678
        PROJECT_LABELS = {'env': 'prod'}
        PROJECT_LIFECYCLE_STATE = 'ACTIVE'
        resource = {'projectId': PROJECT_ID,
                    'name': PROJECT_NAME,
                    'projectNumber': PROJECT_NUMBER,
                    'labels': PROJECT_LABELS,
                    'lifecycleState': PROJECT_LIFECYCLE_STATE}
        project = self._getTargetClass().from_api_repr(resource, client)
        self.assertEqual(project.project_id, PROJECT_ID)
        self.assertEqual(project._client, client)
        self.assertEqual(project.name, PROJECT_NAME)
        self.assertEqual(project.number, PROJECT_NUMBER)
        self.assertEqual(project.labels, PROJECT_LABELS)
        self.assertEqual(project.status, PROJECT_LIFECYCLE_STATE)

    def test_full_name(self):
        PROJECT_ID = 'project-id'
        project = self._makeOne(PROJECT_ID, None)
        self.assertEqual('projects/%s' % PROJECT_ID, project.full_name)

    def test_full_name_missing_id(self):
        project = self._makeOne(None, None)
        with self.assertRaises(ValueError):
            self.assertIsNone(project.full_name)

    def test_path(self):
        PROJECT_ID = 'project-id'
        project = self._makeOne(PROJECT_ID, None)
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
        }
        connection = _Connection(PROJECT_RESOURCE)
        client = _Client(connection=connection)
        project = self._makeOne(PROJECT_ID, client)
        self.assertEqual(project.number, None)
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
        }
        connection = _Connection(PROJECT_RESOURCE)
        client = _Client(connection=connection)
        project = self._makeOne(PROJECT_ID, client)
        self.assertEqual(project.number, None)
        self.assertEqual(project.name, None)
        self.assertEqual(project.labels, {})
        self.assertEqual(project.status, None)
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
        project = self._makeOne(PROJECT_ID, client)
        self.assertTrue(project.exists())

    def test_exists_with_explicitly_passed_client(self):
        PROJECT_ID = 'project-id'
        connection = _Connection({'projectId': PROJECT_ID})
        client = _Client(connection=connection)
        project = self._makeOne(PROJECT_ID, None)
        self.assertTrue(project.exists(client=client))

    def test_exists_with_missing_client(self):
        PROJECT_ID = 'project-id'
        project = self._makeOne(PROJECT_ID, None)
        with self.assertRaises(AttributeError):
            project.exists()

    def test_exists_not_found(self):
        PROJECT_ID = 'project-id'
        connection = _Connection()
        client = _Client(connection=connection)
        project = self._makeOne(PROJECT_ID, client)
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
        project = self._makeOne(PROJECT_ID, client)
        project.name = PROJECT_NAME
        project.labels = LABELS
        project.update()

        request, = connection._requested
        expected_request = {
            'method': 'PUT',
            'data': {
                'name': PROJECT_NAME,
                'labels': LABELS,
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
        }
        connection = _Connection(PROJECT_RESOURCE)
        client = _Client(connection=connection)
        project = self._makeOne(PROJECT_ID, client)
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
        }
        DELETING_PROJECT = PROJECT_RESOURCE.copy()
        DELETING_PROJECT['lifecycleState'] = NEW_STATE = 'DELETE_REQUESTED'

        connection = _Connection(PROJECT_RESOURCE, DELETING_PROJECT)
        client = _Client(connection=connection)
        project = self._makeOne(PROJECT_ID, client)
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
        }
        connection = _Connection(PROJECT_RESOURCE)
        client = _Client(connection=connection)
        project = self._makeOne(PROJECT_ID, client)
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
        }
        UNDELETED_PROJECT = PROJECT_RESOURCE.copy()
        UNDELETED_PROJECT['lifecycleState'] = NEW_STATE = 'ACTIVE'

        connection = _Connection(PROJECT_RESOURCE, UNDELETED_PROJECT)
        client = _Client(connection=connection)
        project = self._makeOne(PROJECT_ID, client)
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
        from gcloud.exceptions import NotFound
        self._requested.append(kw)

        try:
            response, self._responses = self._responses[0], self._responses[1:]
        except:
            raise NotFound('miss')
        else:
            return response


class _Client(object):

    def __init__(self, connection=None):
        self.connection = connection
