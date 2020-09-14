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
