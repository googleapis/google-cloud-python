# Copyright 2024 Google LLC All rights reserved.
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

"""Unit tests for SpannerExecutionContext and reset_connection."""

import unittest
from unittest import mock

from google.cloud import spanner_dbapi
from google.cloud.sqlalchemy_spanner.sqlalchemy_spanner import (
    SpannerExecutionContext,
    reset_connection,
)


class ResetConnectionTest(unittest.TestCase):
    def test_reset_connection_clears_timeout(self):
        dbapi_conn = mock.MagicMock(spec=spanner_dbapi.Connection)
        dbapi_conn.inside_transaction = False

        reset_connection(dbapi_conn, connection_record=None)

        self.assertIsNone(dbapi_conn.staleness)
        self.assertFalse(dbapi_conn.read_only)
        self.assertIsNone(dbapi_conn.timeout)

    def test_reset_connection_with_wrapper(self):
        inner_conn = mock.MagicMock(spec=spanner_dbapi.Connection)
        inner_conn.inside_transaction = False
        wrapper = mock.MagicMock()
        wrapper.connection = inner_conn

        reset_connection(wrapper, connection_record=None)

        self.assertIsNone(inner_conn.staleness)
        self.assertFalse(inner_conn.read_only)
        self.assertIsNone(inner_conn.timeout)


class SpannerExecutionContextPreExecTest(unittest.TestCase):
    def _make_context(self, execution_options):
        ctx = SpannerExecutionContext.__new__(SpannerExecutionContext)
        ctx.execution_options = execution_options

        dbapi_conn = mock.MagicMock()
        dbapi_conn.connection = mock.MagicMock()
        ctx._dbapi_connection = dbapi_conn
        ctx.cursor = mock.MagicMock()

        return ctx

    @mock.patch(
        "google.cloud.sqlalchemy_spanner.sqlalchemy_spanner.DefaultExecutionContext.pre_exec"
    )
    def test_pre_exec_sets_timeout(self, mock_super_pre_exec):
        ctx = self._make_context({"timeout": 60})
        ctx.pre_exec()

        self.assertEqual(ctx._dbapi_connection.connection.timeout, 60)

    @mock.patch(
        "google.cloud.sqlalchemy_spanner.sqlalchemy_spanner.DefaultExecutionContext.pre_exec"
    )
    def test_pre_exec_no_timeout_leaves_connection_unchanged(self, mock_super_pre_exec):
        ctx = self._make_context({})

        conn = ctx._dbapi_connection.connection
        conn._mock_children.clear()

        ctx.pre_exec()

        set_attrs = {
            name
            for name, _ in conn._mock_children.items()
            if not name.startswith("_")
        }
        self.assertNotIn("timeout", set_attrs)

    @mock.patch(
        "google.cloud.sqlalchemy_spanner.sqlalchemy_spanner.DefaultExecutionContext.pre_exec"
    )
    def test_pre_exec_timeout_with_other_options(self, mock_super_pre_exec):
        ctx = self._make_context(
            {"timeout": 30, "read_only": True, "request_priority": 2}
        )
        ctx.pre_exec()

        self.assertEqual(ctx._dbapi_connection.connection.timeout, 30)
        self.assertTrue(ctx._dbapi_connection.connection.read_only)
        self.assertEqual(ctx._dbapi_connection.connection.request_priority, 2)
