# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

"""Cursor() class unit tests."""

import unittest
from unittest import mock

from google.cloud.spanner_dbapi import connect, InterfaceError


class TestCursor(unittest.TestCase):
    def test_close(self):
        with mock.patch(
            "google.cloud.spanner_v1.instance.Instance.exists",
            return_value=True,
        ):
            with mock.patch(
                "google.cloud.spanner_v1.database.Database.exists",
                return_value=True,
            ):
                connection = connect("test-instance", "test-database")

        cursor = connection.cursor()
        self.assertFalse(cursor.is_closed)

        cursor.close()

        self.assertTrue(cursor.is_closed)
        with self.assertRaises(InterfaceError):
            cursor.execute("SELECT * FROM database")

    def test_connection_closed(self):
        with mock.patch(
            "google.cloud.spanner_v1.instance.Instance.exists",
            return_value=True,
        ):
            with mock.patch(
                "google.cloud.spanner_v1.database.Database.exists",
                return_value=True,
            ):
                connection = connect("test-instance", "test-database")

        cursor = connection.cursor()
        self.assertFalse(cursor.is_closed)

        connection.close()

        self.assertTrue(cursor.is_closed)
        with self.assertRaises(InterfaceError):
            cursor.execute("SELECT * FROM database")

    def test_executemany_on_closed_cursor(self):
        with mock.patch(
            "google.cloud.spanner_v1.instance.Instance.exists",
            return_value=True,
        ):
            with mock.patch(
                "google.cloud.spanner_v1.database.Database.exists",
                return_value=True,
            ):
                connection = connect("test-instance", "test-database")

        cursor = connection.cursor()
        cursor.close()

        with self.assertRaises(InterfaceError):
            cursor.executemany(
                """SELECT * FROM table1 WHERE "col1" = @a1""", ()
            )

    def test_executemany(self):
        operation = """SELECT * FROM table1 WHERE "col1" = @a1"""
        params_seq = ((1,), (2,))

        with mock.patch(
            "google.cloud.spanner_v1.instance.Instance.exists",
            return_value=True,
        ):
            with mock.patch(
                "google.cloud.spanner_v1.database.Database.exists",
                return_value=True,
            ):
                connection = connect("test-instance", "test-database")

        cursor = connection.cursor()
        with mock.patch(
            "google.cloud.spanner_dbapi.cursor.Cursor.execute"
        ) as execute_mock:
            cursor.executemany(operation, params_seq)

        execute_mock.assert_has_calls(
            (mock.call(operation, (1,)), mock.call(operation, (2,)))
        )
