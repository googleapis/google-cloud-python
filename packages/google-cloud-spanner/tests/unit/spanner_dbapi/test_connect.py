# Copyright 2020 Google LLC
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

"""connect() module function unit tests."""

import unittest
from unittest import mock

import google.auth.credentials


INSTANCE = "test-instance"
DATABASE = "test-database"
PROJECT = "test-project"
USER_AGENT = "user-agent"


def _make_credentials():
    class _CredentialsWithScopes(
        google.auth.credentials.Credentials, google.auth.credentials.Scoped
    ):
        pass

    return mock.Mock(spec=_CredentialsWithScopes)


@mock.patch("google.cloud.spanner_v1.Client")
class Test_connect(unittest.TestCase):
    def test_w_implicit(self, mock_client):
        from google.cloud.spanner_dbapi import connect
        from google.cloud.spanner_dbapi import Connection

        client = mock_client.return_value
        instance = client.instance.return_value
        database = instance.database.return_value

        connection = connect(INSTANCE, DATABASE)

        self.assertIsInstance(connection, Connection)

        self.assertIs(connection.instance, instance)
        client.instance.assert_called_once_with(INSTANCE)

        self.assertIs(connection.database, database)
        instance.database.assert_called_once_with(DATABASE, pool=None)
        # Datbase constructs its own pool
        self.assertIsNotNone(connection.database._pool)

    def test_w_explicit(self, mock_client):
        from google.cloud.spanner_v1.pool import AbstractSessionPool
        from google.cloud.spanner_dbapi import connect
        from google.cloud.spanner_dbapi import Connection
        from google.cloud.spanner_dbapi.version import PY_VERSION

        credentials = _make_credentials()
        pool = mock.create_autospec(AbstractSessionPool)
        client = mock_client.return_value
        instance = client.instance.return_value
        database = instance.database.return_value

        connection = connect(
            INSTANCE,
            DATABASE,
            PROJECT,
            credentials,
            pool=pool,
            user_agent=USER_AGENT,
        )

        self.assertIsInstance(connection, Connection)

        mock_client.assert_called_once_with(
            project=PROJECT, credentials=credentials, client_info=mock.ANY
        )
        client_info = mock_client.call_args_list[0][1]["client_info"]
        self.assertEqual(client_info.user_agent, USER_AGENT)
        self.assertEqual(client_info.python_version, PY_VERSION)

        self.assertIs(connection.instance, instance)
        client.instance.assert_called_once_with(INSTANCE)

        self.assertIs(connection.database, database)
        instance.database.assert_called_once_with(DATABASE, pool=pool)

    def test_w_credential_file_path(self, mock_client):
        from google.cloud.spanner_dbapi import connect
        from google.cloud.spanner_dbapi import Connection
        from google.cloud.spanner_dbapi.version import PY_VERSION

        credentials_path = "dummy/file/path.json"

        connection = connect(
            INSTANCE,
            DATABASE,
            PROJECT,
            credentials=credentials_path,
            user_agent=USER_AGENT,
        )

        self.assertIsInstance(connection, Connection)

        factory = mock_client.from_service_account_json
        factory.assert_called_once_with(
            credentials_path,
            project=PROJECT,
            client_info=mock.ANY,
        )
        client_info = factory.call_args_list[0][1]["client_info"]
        self.assertEqual(client_info.user_agent, USER_AGENT)
        self.assertEqual(client_info.python_version, PY_VERSION)
