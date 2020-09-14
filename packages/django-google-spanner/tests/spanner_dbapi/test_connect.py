# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

"""connect() module function unit tests."""

import unittest
from unittest import mock

import google.auth.credentials
from google.api_core.gapic_v1.client_info import ClientInfo
from google.cloud.spanner_dbapi import connect, Connection


def _make_credentials():
    class _CredentialsWithScopes(
        google.auth.credentials.Credentials, google.auth.credentials.Scoped
    ):
        pass

    return mock.Mock(spec=_CredentialsWithScopes)


class Test_connect(unittest.TestCase):
    def test_connect(self):
        PROJECT = "test-project"
        USER_AGENT = "user-agent"
        CREDENTIALS = _make_credentials()
        CLIENT_INFO = ClientInfo(user_agent=USER_AGENT)

        with mock.patch(
            "google.cloud.spanner_dbapi.spanner_v1.Client"
        ) as client_mock:
            with mock.patch(
                "google.cloud.spanner_dbapi.google_client_info",
                return_value=CLIENT_INFO,
            ) as client_info_mock:

                connection = connect(
                    "test-instance",
                    "test-database",
                    PROJECT,
                    CREDENTIALS,
                    USER_AGENT,
                )

                self.assertIsInstance(connection, Connection)
                client_info_mock.assert_called_once_with(USER_AGENT)

            client_mock.assert_called_once_with(
                project=PROJECT,
                credentials=CREDENTIALS,
                client_info=CLIENT_INFO,
            )

    def test_instance_not_found(self):
        with mock.patch(
            "google.cloud.spanner_v1.instance.Instance.exists",
            return_value=False,
        ) as exists_mock:

            with self.assertRaises(ValueError):
                connect("test-instance", "test-database")

            exists_mock.assert_called_once_with()

    def test_database_not_found(self):
        with mock.patch(
            "google.cloud.spanner_v1.instance.Instance.exists",
            return_value=True,
        ):
            with mock.patch(
                "google.cloud.spanner_v1.database.Database.exists",
                return_value=False,
            ) as exists_mock:

                with self.assertRaises(ValueError):
                    connect("test-instance", "test-database")

                exists_mock.assert_called_once_with()

    def test_connect_instance_id(self):
        INSTANCE = "test-instance"

        with mock.patch(
            "google.cloud.spanner_v1.client.Client.instance"
        ) as instance_mock:
            connection = connect(INSTANCE, "test-database")

            instance_mock.assert_called_once_with(INSTANCE)

        self.assertIsInstance(connection, Connection)

    def test_connect_database_id(self):
        DATABASE = "test-database"

        with mock.patch(
            "google.cloud.spanner_v1.instance.Instance.database"
        ) as database_mock:
            with mock.patch(
                "google.cloud.spanner_v1.instance.Instance.exists",
                return_value=True,
            ):
                connection = connect("test-instance", DATABASE)

                database_mock.assert_called_once_with(DATABASE, pool=mock.ANY)

        self.assertIsInstance(connection, Connection)
