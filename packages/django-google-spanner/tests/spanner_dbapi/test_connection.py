# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

"""Connection() class unit tests."""

import unittest
from unittest import mock

# import google.cloud.spanner_dbapi.exceptions as dbapi_exceptions

from google.cloud.spanner_dbapi import Connection, InterfaceError
from google.cloud.spanner_dbapi.connection import AUTOCOMMIT_MODE_WARNING
from google.cloud.spanner_v1.database import Database
from google.cloud.spanner_v1.instance import Instance


class TestConnection(unittest.TestCase):
    instance_name = "instance-name"
    database_name = "database-name"

    def _make_connection(self):
        # we don't need real Client object to test the constructor
        instance = Instance(self.instance_name, client=None)
        database = instance.database(self.database_name)
        return Connection(instance, database)

    def test_ctor(self):
        connection = self._make_connection()

        self.assertIsInstance(connection.instance, Instance)
        self.assertEqual(connection.instance.instance_id, self.instance_name)

        self.assertIsInstance(connection.database, Database)
        self.assertEqual(connection.database.database_id, self.database_name)

        self.assertFalse(connection.is_closed)

    def test_close(self):
        connection = self._make_connection()

        self.assertFalse(connection.is_closed)
        connection.close()
        self.assertTrue(connection.is_closed)

        with self.assertRaises(InterfaceError):
            connection.cursor()

    @mock.patch("warnings.warn")
    def test_transaction_autocommit_warnings(self, warn_mock):
        connection = self._make_connection()
        connection.autocommit = True

        connection.commit()
        warn_mock.assert_called_with(
            AUTOCOMMIT_MODE_WARNING, UserWarning, stacklevel=2
        )
        connection.rollback()
        warn_mock.assert_called_with(
            AUTOCOMMIT_MODE_WARNING, UserWarning, stacklevel=2
        )

    def test_database_property(self):
        connection = self._make_connection()
        self.assertIsInstance(connection.database, Database)
        self.assertEqual(connection.database, connection._database)

        with self.assertRaises(AttributeError):
            connection.database = None

    def test_instance_property(self):
        connection = self._make_connection()
        self.assertIsInstance(connection.instance, Instance)
        self.assertEqual(connection.instance, connection._instance)

        with self.assertRaises(AttributeError):
            connection.instance = None
