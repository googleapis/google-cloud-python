# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import sys
import unittest

from mock_import import mock_import
from unittest import mock


@mock_import()
@unittest.skipIf(sys.version_info < (3, 6), reason="Skipping Python 3.5")
class TestBase(unittest.TestCase):
    PROJECT = "project"
    INSTANCE_ID = "instance_id"
    DATABASE_ID = "database_id"
    USER_AGENT = "django_spanner/2.2.0a1"
    OPTIONS = {"option": "dummy"}

    settings_dict = {
        "PROJECT": PROJECT,
        "INSTANCE": INSTANCE_ID,
        "NAME": DATABASE_ID,
        "user_agent": USER_AGENT,
        "OPTIONS": OPTIONS,
    }

    def _get_target_class(self):
        from django_spanner.base import DatabaseWrapper

        return DatabaseWrapper

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_property_instance(self):
        settings_dict = {"INSTANCE": "instance"}
        db_wrapper = self._make_one(settings_dict=settings_dict)

        with mock.patch("django_spanner.base.spanner") as mock_spanner:
            mock_spanner.Client = mock_client = mock.MagicMock()
            mock_client().instance = mock_instance = mock.MagicMock()
            _ = db_wrapper.instance
            mock_instance.assert_called_once_with(settings_dict["INSTANCE"])

    def test_property__nodb_connection(self):
        db_wrapper = self._make_one(None)
        with self.assertRaises(NotImplementedError):
            db_wrapper._nodb_connection()

    def test_get_connection_params(self):
        db_wrapper = self._make_one(self.settings_dict)
        params = db_wrapper.get_connection_params()

        self.assertEqual(params["project"], self.PROJECT)
        self.assertEqual(params["instance_id"], self.INSTANCE_ID)
        self.assertEqual(params["database_id"], self.DATABASE_ID)
        self.assertEqual(params["user_agent"], self.USER_AGENT)
        self.assertEqual(params["option"], self.OPTIONS["option"])

    def test_get_new_connection(self):
        db_wrapper = self._make_one(self.settings_dict)
        db_wrapper.Database = mock_database = mock.MagicMock()
        mock_database.connect = mock_connect = mock.MagicMock()
        conn_params = {"test_param": "dummy"}
        db_wrapper.get_new_connection(conn_params)
        mock_connect.assert_called_once_with(**conn_params)

    def test_init_connection_state(self):
        db_wrapper = self._make_one(self.settings_dict)
        db_wrapper.connection = mock_connection = mock.MagicMock()
        mock_connection.close = mock_close = mock.MagicMock()
        db_wrapper.init_connection_state()
        mock_close.assert_called_once_with()

    def test_create_cursor(self):
        db_wrapper = self._make_one(self.settings_dict)
        db_wrapper.connection = mock_connection = mock.MagicMock()
        mock_connection.cursor = mock_cursor = mock.MagicMock()
        db_wrapper.create_cursor()
        mock_cursor.assert_called_once_with()

    def test__set_autocommit(self):
        db_wrapper = self._make_one(self.settings_dict)
        db_wrapper.connection = mock_connection = mock.MagicMock()
        mock_connection.autocommit = False
        db_wrapper._set_autocommit(True)
        self.assertEqual(mock_connection.autocommit, True)

    def test_is_usable(self):
        from google.cloud.spanner_dbapi.exceptions import Error

        db_wrapper = self._make_one(self.settings_dict)
        db_wrapper.connection = None
        self.assertFalse(db_wrapper.is_usable())

        db_wrapper.connection = mock_connection = mock.MagicMock()
        mock_connection.is_closed = True
        self.assertFalse(db_wrapper.is_usable())

        mock_connection.is_closed = False
        self.assertTrue(db_wrapper.is_usable())

        mock_connection.cursor = mock.MagicMock(side_effect=Error)
        self.assertFalse(db_wrapper.is_usable())
