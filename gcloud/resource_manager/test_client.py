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


class Test__ProjectIterator(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.resource_manager.client import _ProjectIterator
        return _ProjectIterator

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_constructor(self):
        client = object()
        iterator = self._makeOne(client)
        self.assertEqual(iterator.path, '/projects')
        self.assertEqual(iterator.page_number, 0)
        self.assertEqual(iterator.next_page_token, None)
        self.assertTrue(iterator.client is client)
        self.assertEqual(iterator.extra_params, {})

    def test_get_items_from_response_empty(self):
        client = object()
        iterator = self._makeOne(client)
        self.assertEqual(list(iterator.get_items_from_response({})), [])

    def test_get_items_from_response_non_empty(self):
        from gcloud.resource_manager.project import Project

        PROJECT_ID = 'project-id'
        PROJECT_NAME = 'My Project Name'
        PROJECT_NUMBER = 12345678
        PROJECT_LABELS = {'env': 'prod'}
        PROJECT_LIFECYCLE_STATE = 'ACTIVE'
        API_RESOURCE = {
            'projectId': PROJECT_ID,
            'name': PROJECT_NAME,
            'projectNumber': PROJECT_NUMBER,
            'labels': PROJECT_LABELS,
            'lifecycleState': PROJECT_LIFECYCLE_STATE,
        }
        RESPONSE = {'projects': [API_RESOURCE]}

        client = object()
        iterator = self._makeOne(client)
        projects = list(iterator.get_items_from_response(RESPONSE))

        project, = projects
        self.assertTrue(isinstance(project, Project))
        self.assertEqual(project.project_id, PROJECT_ID)
        self.assertEqual(project._client, client)
        self.assertEqual(project.name, PROJECT_NAME)
        self.assertEqual(project.number, PROJECT_NUMBER)
        self.assertEqual(project.labels, PROJECT_LABELS)
        self.assertEqual(project.status, PROJECT_LIFECYCLE_STATE)


class TestClient(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.resource_manager.client import Client
        return Client

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_constructor(self):
        from gcloud.resource_manager.connection import Connection

        http = object()
        credentials = _Credentials()
        client = self._makeOne(credentials=credentials, http=http)
        self.assertTrue(isinstance(client.connection, Connection))
        self.assertEqual(client.connection._credentials, credentials)
        self.assertEqual(client.connection._http, http)

    def test_new_project_factory(self):
        from gcloud.resource_manager.project import Project

        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)
        project_id = 'project_id'
        name = object()
        labels = object()
        project = client.new_project(project_id, name=name, labels=labels)

        self.assertTrue(isinstance(project, Project))
        self.assertEqual(project._client, client)
        self.assertEqual(project.project_id, project_id)
        self.assertEqual(project.name, name)
        self.assertEqual(project.labels, labels)

    def test_fetch_project(self):
        from gcloud.resource_manager.project import Project

        project_id = 'project-id'
        project_number = 123
        project_name = 'Project Name'
        labels = {'env': 'prod'}
        project_resource = {
            'projectId': project_id,
            'projectNumber': project_number,
            'name': project_name,
            'labels': labels,
            'lifecycleState': 'ACTIVE',
        }

        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)
        # Patch the connection with one we can easily control.
        client.connection = _Connection(project_resource)

        project = client.fetch_project(project_id)
        self.assertTrue(isinstance(project, Project))
        self.assertEqual(project._client, client)
        self.assertEqual(project.project_id, project_id)
        self.assertEqual(project.name, project_name)
        self.assertEqual(project.labels, labels)

    def test_list_projects_return_type(self):
        from gcloud.resource_manager.client import _ProjectIterator

        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)
        # Patch the connection with one we can easily control.
        client.connection = _Connection({})

        results = client.list_projects()
        self.assertIsInstance(results, _ProjectIterator)

    def test_list_projects_no_paging(self):
        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)

        PROJECT_ID = 'project-id'
        PROJECT_NUMBER = 1
        STATUS = 'ACTIVE'
        PROJECTS_RESOURCE = {
            'projects': [
                {
                    'projectId': PROJECT_ID,
                    'projectNumber': PROJECT_NUMBER,
                    'lifecycleState': STATUS,
                },
            ],
        }
        # Patch the connection with one we can easily control.
        client.connection = _Connection(PROJECTS_RESOURCE)
        # Make sure there will be no paging.
        self.assertFalse('nextPageToken' in PROJECTS_RESOURCE)

        results = list(client.list_projects())

        project, = results
        self.assertEqual(project.project_id, PROJECT_ID)
        self.assertEqual(project.number, PROJECT_NUMBER)
        self.assertEqual(project.status, STATUS)

    def test_list_projects_with_paging(self):
        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)

        PROJECT_ID1 = 'project-id'
        PROJECT_NUMBER1 = 1
        STATUS = 'ACTIVE'
        TOKEN = 'next-page-token'
        FIRST_PROJECTS_RESOURCE = {
            'projects': [
                {
                    'projectId': PROJECT_ID1,
                    'projectNumber': PROJECT_NUMBER1,
                    'lifecycleState': STATUS,
                },
            ],
            'nextPageToken': TOKEN,
        }
        PROJECT_ID2 = 'project-id-2'
        PROJECT_NUMBER2 = 42
        SECOND_PROJECTS_RESOURCE = {
            'projects': [
                {
                    'projectId': PROJECT_ID2,
                    'projectNumber': PROJECT_NUMBER2,
                    'lifecycleState': STATUS,
                },
            ],
        }
        # Patch the connection with one we can easily control.
        client.connection = _Connection(FIRST_PROJECTS_RESOURCE,
                                        SECOND_PROJECTS_RESOURCE)

        # Page size = 1 with two response means we'll have two requests.
        results = list(client.list_projects(page_size=1))

        # Check that the results are as expected.
        project1, project2 = results
        self.assertEqual(project1.project_id, PROJECT_ID1)
        self.assertEqual(project1.number, PROJECT_NUMBER1)
        self.assertEqual(project1.status, STATUS)
        self.assertEqual(project2.project_id, PROJECT_ID2)
        self.assertEqual(project2.number, PROJECT_NUMBER2)
        self.assertEqual(project2.status, STATUS)

        # Check that two requests were required since page_size=1.
        request1, request2 = client.connection._requested
        self.assertEqual(request1, {
            'path': '/projects',
            'method': 'GET',
            'query_params': {
                'pageSize': 1,
            },
        })
        self.assertEqual(request2, {
            'path': '/projects',
            'method': 'GET',
            'query_params': {
                'pageSize': 1,
                'pageToken': TOKEN,
            },
        })

    def test_list_projects_with_filter(self):
        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)

        PROJECT_ID = 'project-id'
        PROJECT_NUMBER = 1
        STATUS = 'ACTIVE'
        PROJECTS_RESOURCE = {
            'projects': [
                {
                    'projectId': PROJECT_ID,
                    'projectNumber': PROJECT_NUMBER,
                    'lifecycleState': STATUS,
                },
            ],
        }
        # Patch the connection with one we can easily control.
        client.connection = _Connection(PROJECTS_RESOURCE)

        FILTER_PARAMS = {'id': 'project-id'}
        results = list(client.list_projects(filter_params=FILTER_PARAMS))

        project, = results
        self.assertEqual(project.project_id, PROJECT_ID)
        self.assertEqual(project.number, PROJECT_NUMBER)
        self.assertEqual(project.status, STATUS)

        # Check that the filter made it in the request.
        request, = client.connection._requested
        self.assertEqual(request, {
            'path': '/projects',
            'method': 'GET',
            'query_params': {
                'filter': FILTER_PARAMS,
            },
        })


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
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response
