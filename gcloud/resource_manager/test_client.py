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

    def test_project_factory(self):
        from gcloud.resource_manager.project import Project

        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)
        project_id = 'project_id'
        name = object()
        labels = object()
        project = client.project(project_id, name=name, labels=labels)

        self.assertTrue(isinstance(project, Project))
        self.assertEqual(project._client, client)
        self.assertEqual(project.project_id, project_id)
        self.assertEqual(project.name, name)
        self.assertEqual(project.labels, labels)


class _Credentials(object):

    _scopes = None

    @staticmethod
    def create_scoped_required():
        return True

    def create_scoped(self, scope):
        self._scopes = scope
        return self
