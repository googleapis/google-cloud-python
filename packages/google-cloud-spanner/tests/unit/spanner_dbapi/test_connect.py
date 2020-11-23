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


def _make_credentials():
    class _CredentialsWithScopes(
        google.auth.credentials.Credentials, google.auth.credentials.Scoped
    ):
        pass

    return mock.Mock(spec=_CredentialsWithScopes)


class Test_connect(unittest.TestCase):
    def test_connect(self):
        from google.cloud.spanner_dbapi import connect
        from google.cloud.spanner_dbapi import Connection

        PROJECT = "test-project"
        USER_AGENT = "user-agent"
        CREDENTIALS = _make_credentials()

        with mock.patch("google.cloud.spanner_v1.Client") as client_mock:
            connection = connect(
                "test-instance",
                "test-database",
                PROJECT,
                CREDENTIALS,
                user_agent=USER_AGENT,
            )

            self.assertIsInstance(connection, Connection)

            client_mock.assert_called_once_with(
                project=PROJECT, credentials=CREDENTIALS, client_info=mock.ANY
            )

    def test_instance_not_found(self):
        from google.cloud.spanner_dbapi import connect

        with mock.patch(
            "google.cloud.spanner_v1.instance.Instance.exists", return_value=False,
        ) as exists_mock:

            with self.assertRaises(ValueError):
                connect("test-instance", "test-database")

            exists_mock.assert_called_once_with()

    def test_database_not_found(self):
        from google.cloud.spanner_dbapi import connect

        with mock.patch(
            "google.cloud.spanner_v1.instance.Instance.exists", return_value=True,
        ):
            with mock.patch(
                "google.cloud.spanner_v1.database.Database.exists", return_value=False,
            ) as exists_mock:

                with self.assertRaises(ValueError):
                    connect("test-instance", "test-database")

                exists_mock.assert_called_once_with()

    def test_connect_instance_id(self):
        from google.cloud.spanner_dbapi import connect
        from google.cloud.spanner_dbapi import Connection

        INSTANCE = "test-instance"

        with mock.patch(
            "google.cloud.spanner_v1.client.Client.instance"
        ) as instance_mock:
            connection = connect(INSTANCE, "test-database")

            instance_mock.assert_called_once_with(INSTANCE)

        self.assertIsInstance(connection, Connection)

    def test_connect_database_id(self):
        from google.cloud.spanner_dbapi import connect
        from google.cloud.spanner_dbapi import Connection

        DATABASE = "test-database"

        with mock.patch(
            "google.cloud.spanner_v1.instance.Instance.database"
        ) as database_mock:
            with mock.patch(
                "google.cloud.spanner_v1.instance.Instance.exists", return_value=True,
            ):
                connection = connect("test-instance", DATABASE)

                database_mock.assert_called_once_with(DATABASE, pool=mock.ANY)

        self.assertIsInstance(connection, Connection)

    def test_default_sessions_pool(self):
        from google.cloud.spanner_dbapi import connect

        with mock.patch("google.cloud.spanner_v1.instance.Instance.database"):
            with mock.patch(
                "google.cloud.spanner_v1.instance.Instance.exists", return_value=True,
            ):
                connection = connect("test-instance", "test-database")

                self.assertIsNotNone(connection.database._pool)

    def test_sessions_pool(self):
        from google.cloud.spanner_dbapi import connect
        from google.cloud.spanner_v1.pool import FixedSizePool

        database_id = "test-database"
        pool = FixedSizePool()

        with mock.patch(
            "google.cloud.spanner_v1.instance.Instance.database"
        ) as database_mock:
            with mock.patch(
                "google.cloud.spanner_v1.instance.Instance.exists", return_value=True,
            ):
                connect("test-instance", database_id, pool=pool)
                database_mock.assert_called_once_with(database_id, pool=pool)
