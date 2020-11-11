# Copyright 2020 Google LLC All rights reserved.
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

"""Cloud Spanner DB-API Connection class unit tests."""

import mock
import unittest


class TestHelpers(unittest.TestCase):
    def test__execute_insert_heterogenous(self):
        from google.cloud.spanner_dbapi import _helpers

        sql = "sql"
        params = (sql, None)
        with mock.patch(
            "google.cloud.spanner_dbapi._helpers.sql_pyformat_args_to_spanner",
            return_value=params,
        ) as mock_pyformat:
            with mock.patch(
                "google.cloud.spanner_dbapi._helpers.get_param_types", return_value=None
            ) as mock_param_types:
                transaction = mock.MagicMock()
                transaction.execute_update = mock_execute = mock.MagicMock()
                _helpers._execute_insert_heterogenous(transaction, [params])

                mock_pyformat.assert_called_once_with(params[0], params[1])
                mock_param_types.assert_called_once_with(None)
                mock_execute.assert_called_once_with(sql, params=None, param_types=None)

    def test__execute_insert_homogenous(self):
        from google.cloud.spanner_dbapi import _helpers

        transaction = mock.MagicMock()
        transaction.insert = mock.MagicMock()
        parts = mock.MagicMock()
        parts.get = mock.MagicMock(return_value=0)

        _helpers._execute_insert_homogenous(transaction, parts)
        transaction.insert.assert_called_once_with(0, 0, 0)

    def test_handle_insert(self):
        from google.cloud.spanner_dbapi import _helpers

        connection = mock.MagicMock()
        connection.database.run_in_transaction = mock_run_in = mock.MagicMock()
        sql = "sql"
        parts = mock.MagicMock()
        with mock.patch(
            "google.cloud.spanner_dbapi._helpers.parse_insert", return_value=parts
        ):
            parts.get = mock.MagicMock(return_value=True)
            mock_run_in.return_value = 0
            result = _helpers.handle_insert(connection, sql, None)
            self.assertEqual(result, 0)

            parts.get = mock.MagicMock(return_value=False)
            mock_run_in.return_value = 1
            result = _helpers.handle_insert(connection, sql, None)
            self.assertEqual(result, 1)


class TestColumnInfo(unittest.TestCase):
    def test_ctor(self):
        from google.cloud.spanner_dbapi.cursor import ColumnInfo

        name = "col-name"
        type_code = 8
        display_size = 5
        internal_size = 10
        precision = 3
        scale = None
        null_ok = False

        cols = ColumnInfo(
            name, type_code, display_size, internal_size, precision, scale, null_ok
        )

        self.assertEqual(cols.name, name)
        self.assertEqual(cols.type_code, type_code)
        self.assertEqual(cols.display_size, display_size)
        self.assertEqual(cols.internal_size, internal_size)
        self.assertEqual(cols.precision, precision)
        self.assertEqual(cols.scale, scale)
        self.assertEqual(cols.null_ok, null_ok)
        self.assertEqual(
            cols.fields,
            (name, type_code, display_size, internal_size, precision, scale, null_ok),
        )

    def test___get_item__(self):
        from google.cloud.spanner_dbapi.cursor import ColumnInfo

        fields = ("col-name", 8, 5, 10, 3, None, False)
        cols = ColumnInfo(*fields)

        for i in range(0, 7):
            self.assertEqual(cols[i], fields[i])

    def test___str__(self):
        from google.cloud.spanner_dbapi.cursor import ColumnInfo

        cols = ColumnInfo("col-name", 8, None, 10, 3, None, False)

        self.assertEqual(
            str(cols),
            "ColumnInfo(name='col-name', type_code=8, internal_size=10, precision='3')",
        )
