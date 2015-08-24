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
