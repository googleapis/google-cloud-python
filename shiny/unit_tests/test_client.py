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


class TestClient(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.shiny.client import Client
        return Client

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor(self):
        import mock
        from google.cloud.shiny.connection import Connection

        project = 'prujekt4'
        http = object()
        credentials = mock.Mock()
        scoped_credentials = object()
        credentials.create_scoped_required.return_value = True
        credentials.create_scoped.return_value = scoped_credentials
        client = self._make_one(
            project=project, credentials=credentials, http=http)

        # Verify the instance attributes.
        self.assertEqual(client.project, project)
        self.assertIsInstance(client.connection, Connection)
        self.assertEqual(client.connection._credentials, scoped_credentials)
        self.assertEqual(client.connection._http, http)
        credentials.create_scoped_required.assert_called_once_with()
        credentials.create_scoped.assert_called_once_with(Connection.SCOPE)

    def test_unicorn_factory(self):
        from google.cloud.shiny.unicorn import Unicorn

        project = 'pro-geckt'
        credentials = object()
        client = self._make_one(project=project, credentials=credentials)

        name = 'Plum Charming Cheeks'
        unicorn = client.unicorn(name)
        self.assertIsInstance(unicorn, Unicorn)
        self.assertEqual(unicorn.name, name)
        self.assertIs(unicorn.client, client)
