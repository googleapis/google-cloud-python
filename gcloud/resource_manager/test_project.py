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

from gcloud.resource_manager.client import Client


class TestProject(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.resource_manager.project import Project
        return Project

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_from_api_repr(self):
        """Projects should be created properly from an API representation."""
        client = _Client()
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
        self.assertEqual(project.name, PROJECT_NAME)
        self.assertEqual(project.number, PROJECT_NUMBER)
        self.assertEqual(project.labels, PROJECT_LABELS)
        self.assertEqual(project.status, PROJECT_LIFECYCLE_STATE)

    def test_constructor(self):
        """Constructing a project should set properties appropriately."""
        client = _Client()
        PROJECT_ID = 'project-id'
        project = self._makeOne(project_id=PROJECT_ID, client=client)
        self.assertEqual(project.project_id, PROJECT_ID)
        self.assertEqual(project.client, client)
        self.assertEqual(project.name, None)
        self.assertEqual(project.number, None)
        self.assertEqual(project.labels, {})
        self.assertEqual(project.status, None)

    def test_full_name(self):
        """Check that the full_name property works."""
        PROJECT_ID = 'project-id'
        project = self._makeOne(project_id=PROJECT_ID, client=_Client())
        self.assertEqual('projects/%s' % PROJECT_ID, project.full_name)

    def test_full_name_missing_id(self):
        """Getting the full_name property with no ID should raise an error."""
        project = self._makeOne(project_id=None, client=_Client())
        with self.assertRaises(ValueError):
            self.assertIsNone(project.full_name)

    def test_path(self):
        """Check that the path property works."""
        PROJECT_ID = 'project-id'
        project = self._makeOne(project_id=PROJECT_ID, client=_Client())
        self.assertEqual('/projects/%s' % PROJECT_ID, project.path)

    def test_create(self):
        """Creating an object should make a specific HTTP request."""
        PROJECT_RESOURCE = {
            'projectId': 'project-id',
            'projectNumber': 123,
            'name': 'Project Name',
            'labels': {},
            'lifecycleState': 'ACTIVE'}
        connection = _Connection(PROJECT_RESOURCE)
        client = _Client(connection=connection)
        project = client.project(PROJECT_RESOURCE['projectId'])
        self.assertEqual(project.number, None)
        project.create()
        self.assertEqual(project.number, PROJECT_RESOURCE['projectNumber'])
        request = connection._requested[0]
        self.assertEqual(request['method'], 'POST')
        self.assertEqual(request['data']['projectId'],
                         PROJECT_RESOURCE['projectId'])
        self.assertEqual(request['path'], '/projects')

    def test_reload(self):
        """Calling reload should pull in remote information via the API."""
        PROJECT = {
            'projectId': 'project-id',
            'projectNumber': 123,
            'name': 'Project Name',
            'labels': {'env': 'prod'},
            'lifecycleState': 'ACTIVE'}
        connection = _Connection(PROJECT)
        client = _Client(connection=connection)
        project = client.project(PROJECT['projectId'])
        self.assertEqual(project.number, None)
        self.assertEqual(project.name, None)
        self.assertEqual(project.labels, {})
        self.assertEqual(project.status, None)
        project.reload()
        self.assertEqual(project.name, PROJECT['name'])
        self.assertEqual(project.number, PROJECT['projectNumber'])
        self.assertEqual(project.labels, PROJECT['labels'])
        self.assertEqual(project.status, PROJECT['lifecycleState'])

        request = connection._requested[0]
        self.assertEqual(request['method'], 'GET')
        self.assertEqual(request['path'], project.path)
        self.assertTrue('data' not in request)

    def test_update(self):
        """Updating should save data remotely."""
        PROJECT = {
            'projectId': 'project-id',
            'projectNumber': 123,
            'name': 'Project Name',
            'labels': {'env': 'prod'},
            'lifecycleState': 'ACTIVE'}
        connection = _Connection(PROJECT)
        client = _Client(connection=connection)
        project = client.project(PROJECT['projectId'])
        project.name = PROJECT['name']
        project.labels = PROJECT['labels']
        project.update()
        request = connection._requested[0]
        self.assertEqual(request['method'], 'PUT')
        self.assertEqual(request['path'], project.path)
        data = request['data']
        self.assertEqual(data, {'name': PROJECT['name'],
                                'labels': PROJECT['labels']})

    def test_exists(self):
        """Mock out the response to see if the exists method works."""
        PROJECT_ID = 'project-id'
        connection = _Connection({'projectId': PROJECT_ID})
        client = _Client(connection=connection)
        project = self._makeOne(project_id=PROJECT_ID, client=client)
        self.assertTrue(project.exists())

    def test_exists_with_explicitly_passed_client(self):
        """exists(client=client) should use the client provided."""
        PROJECT_ID = 'project-id'
        connection = _Connection({'projectId': PROJECT_ID})
        client = _Client(connection=connection)
        project = self._makeOne(project_id=PROJECT_ID, client=None)
        self.assertTrue(project.exists(client=client))

    def test_exists_with_missing_client(self):
        """If we can't find a client, throw an Exception."""
        PROJECT_ID = 'project-id'
        project = self._makeOne(project_id=PROJECT_ID, client=None)
        with self.assertRaises(ValueError):
            project.exists(client=None)

    def test_exists_not_found(self):
        """Mock out the response to see if the exists method works."""
        PROJECT_ID = 'project-id'
        connection = _Connection()
        client = _Client(connection=connection)
        project = self._makeOne(project_id=PROJECT_ID, client=client)
        self.assertFalse(project.exists())

    def test_delete(self):
        """Deleting should send a DELETE request."""
        PROJECT = {
            'projectId': 'project-id',
            'projectNumber': 123,
            'name': 'Project Name',
            'labels': {'env': 'prod'},
            'lifecycleState': 'ACTIVE'}
        connection = _Connection(PROJECT)
        client = _Client(connection=connection)
        project = client.project(PROJECT['projectId'])
        project.delete(reload_data=False)
        request = connection._requested[0]
        self.assertEqual(request['method'], 'DELETE')
        self.assertEqual(request['path'], project.path)
        self.assertTrue('data' not in request)

    def test_delete_with_reload_data(self):
        PROJECT = {
            'projectId': 'project-id',
            'projectNumber': 123,
            'name': 'Project Name',
            'labels': {'env': 'prod'},
            'lifecycleState': 'ACTIVE'}
        DELETING_PROJECT = PROJECT.copy()
        DELETING_PROJECT['lifecycleState'] = 'DELETE_REQUESTED'

        connection = _Connection(PROJECT, DELETING_PROJECT)
        client = _Client(connection=connection)
        project = client.project(PROJECT['projectId'])
        project.delete(reload_data=True)

        delete_request = connection._requested[0]
        self.assertEqual(delete_request['method'], 'DELETE')
        self.assertEqual(delete_request['path'], project.path)
        self.assertTrue('data' not in delete_request)

        get_request = connection._requested[1]
        self.assertEqual(get_request['method'], 'GET')
        self.assertEqual(get_request['path'], project.path)
        self.assertEqual(project.status, 'DELETE_REQUESTED')

    def test_undelete(self):
        """Undeleting should send a POST request to :undelete."""
        PROJECT = {
            'projectId': 'project-id',
            'projectNumber': 123,
            'name': 'Project Name',
            'labels': {'env': 'prod'},
            'lifecycleState': 'DELETE_REQUESTED'}
        connection = _Connection(PROJECT)
        client = _Client(connection=connection)
        project = client.project(PROJECT['projectId'])
        project.undelete(reload_data=False)

        request = connection._requested[0]
        self.assertEqual(request['method'], 'POST')
        self.assertEqual(request['path'], project.path + ':undelete')
        self.assertTrue('data' not in request)

    def test_undelete_with_reload_data(self):
        PROJECT = {
            'projectId': 'project-id',
            'projectNumber': 123,
            'name': 'Project Name',
            'labels': {'env': 'prod'},
            'lifecycleState': 'DELETE_REQUESTED'}
        UNDELETED_PROJECT = PROJECT.copy()
        UNDELETED_PROJECT['lifecycleState'] = 'ACTIVE'

        connection = _Connection(PROJECT, UNDELETED_PROJECT)
        client = _Client(connection=connection)
        project = client.project(PROJECT['projectId'])
        project.undelete(reload_data=True)

        undelete_request = connection._requested[0]
        self.assertEqual(undelete_request['method'], 'POST')
        self.assertEqual(undelete_request['path'], project.path + ':undelete')
        self.assertTrue('data' not in undelete_request)

        get_request = connection._requested[1]
        self.assertEqual(get_request['method'], 'GET')
        self.assertEqual(get_request['path'], project.path)
        self.assertEqual(project.status, 'ACTIVE')


class _Connection(object):
    """A mock Connection object which accepts a list of responses to return.

    This also let's you check the requests passed through the connection.
    """

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


class _Client(Client):
    """A mock Client, which only let's you set a connection.

    The connection property just returns the connection without any lazy
    creation of the connection object.
    """

    def __init__(self, connection=None):
        self.connection = connection
