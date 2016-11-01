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
        from google.cloud.shiny.client import _JSONShinyAPI

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
        self.assertIsInstance(client.shiny_api, _JSONShinyAPI)

        # Check the mocks.
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


class Test_JSONShinyAPI(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.shiny.client import _JSONShinyAPI
        return _JSONShinyAPI

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor(self):
        import mock

        client = mock.Mock()
        connection = object()
        client.connection = connection

        shiny_api = self._make_one(client)
        self.assertIs(shiny_api._client, client)
        self.assertIs(shiny_api._connection, connection)

    def test_do_nothing(self):
        import mock

        client = mock.Mock()
        connection = mock.Mock()
        client.connection = connection

        shiny_api = self._make_one(client)
        name = 'Clover Sparkle Boy'

        # Make the request.
        self.assertIsNone(shiny_api.do_nothing(name))

        # Verify which request was made.
        expected_path = 'do-nothing/{}'.format(name)
        expected_data = {'transmogrify': 'doodad'}
        connection.api_request.assert_called_once_with(
            method='POST', path=expected_path, data=expected_data)
