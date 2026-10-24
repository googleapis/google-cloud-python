# Copyright 2026 Google LLC
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

from unittest.mock import MagicMock

from sqlalchemy.testing import eq_
from sqlalchemy.testing.plugin.plugin_base import fixtures

from google.cloud.sqlalchemy_spanner.sqlalchemy_spanner import SpannerDialect


class TestSpannerDialect(fixtures.TestBase):
    def test_get_multi_indexes_excludes_search_indexes_sql(self):
        """Test that get_multi_indexes SQL query excludes SEARCH indexes."""
        dialect = SpannerDialect()
        connection = MagicMock()
        mock_snapshot = MagicMock()
        mock_snapshot.execute_sql.return_value = []
        connection.connection.database.snapshot.return_value.__enter__.return_value = (
            mock_snapshot
        )

        dialect.get_multi_indexes(connection)

        # Retrieve the SQL executed by snapshot
        executed_sql = mock_snapshot.execute_sql.call_args[0][0]
        assert "i.index_type != 'SEARCH'" in executed_sql

    def test_get_multi_indexes_handles_none_column_ordering(self):
        """Test get_multi_indexes with None column ordering."""
        dialect = SpannerDialect()
        connection = MagicMock()
        mock_snapshot = MagicMock()
        # Mock row: schema, table, index_name, columns,
        # is_unique, column_orderings, storing_columns
        mock_row = [
            "public",
            "my_table",
            "idx_search",
            ["col1"],
            False,
            [None],  # column_ordering is None
            [],
        ]
        mock_snapshot.execute_sql.return_value = [mock_row]
        connection.connection.database.snapshot.return_value.__enter__.return_value = (
            mock_snapshot
        )

        res = dialect.get_multi_indexes(connection)
        assert ("public", "my_table") in res
        index_info = res[("public", "my_table")][0]
        eq_(index_info["column_sorting"], {})

    def test_get_multi_indexes_handles_null_column_orderings_array(self):
        """Test get_multi_indexes when column_orderings array is None."""
        dialect = SpannerDialect()
        connection = MagicMock()
        mock_snapshot = MagicMock()
        mock_row = [
            "public",
            "my_table",
            "idx_test",
            ["col1"],
            False,
            None,  # row[5] is None
            [],
        ]
        mock_snapshot.execute_sql.return_value = [mock_row]
        connection.connection.database.snapshot.return_value.__enter__.return_value = (
            mock_snapshot
        )

        res = dialect.get_multi_indexes(connection)
        assert ("public", "my_table") in res
        index_info = res[("public", "my_table")][0]
        eq_(index_info["column_sorting"], {})

    def test_get_multi_unique_constraints_groups_columns(self):
        """Test get_multi_unique_constraints groups the columns of each constraint."""
        dialect = SpannerDialect()
        connection = MagicMock()
        mock_snapshot = MagicMock()
        # Mock rows: schema, table, constraint_name, column_name, ordered by
        # constraint and column position. The emulator repeats the rows of the
        # backing unique constraint of a foreign key for each referencing key.
        mock_snapshot.execute_sql.return_value = [
            ["", "parent", "IDX_parent_a_b_U", "a"],
            ["", "parent", "IDX_parent_a_b_U", "a"],
            ["", "parent", "IDX_parent_a_b_U", "b"],
            ["", "parent", "IDX_parent_a_b_U", "b"],
            ["", "parent", "IDX_parent_c_U", "c"],
            ["my_schema", "other", "IDX_other_x_U", "x"],
        ]
        connection.connection.database.snapshot.return_value.__enter__.return_value = (
            mock_snapshot
        )

        res = dialect.get_multi_unique_constraints(connection)

        eq_(
            res,
            {
                (None, "parent"): [
                    {"name": "IDX_parent_a_b_U", "column_names": ["a", "b"]},
                    {"name": "IDX_parent_c_U", "column_names": ["c"]},
                ],
                ("my_schema", "other"): [
                    {"name": "IDX_other_x_U", "column_names": ["x"]}
                ],
            },
        )

    def test_get_multi_unique_constraints_sql(self):
        """Test get_multi_unique_constraints reads all tables in one query."""
        dialect = SpannerDialect()
        connection = MagicMock()
        mock_snapshot = MagicMock()
        mock_snapshot.execute_sql.return_value = []
        connection.connection.database.snapshot.return_value.__enter__.return_value = (
            mock_snapshot
        )

        dialect.get_multi_unique_constraints(
            connection, filter_names=["parent", "other"]
        )

        mock_snapshot.execute_sql.assert_called_once()
        executed_sql = mock_snapshot.execute_sql.call_args[0][0]
        assert "INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS kcu" in executed_sql
        assert "kcu.ORDINAL_POSITION" in executed_sql
        assert "tc.table_name = 'parent' OR tc.table_name = 'other'" in executed_sql
        assert 'tc.CONSTRAINT_TYPE = "UNIQUE"' in executed_sql
        assert "tc.CONSTRAINT_NAME IS NOT NULL" in executed_sql

    def test_get_unique_constraints(self):
        """Test get_unique_constraints returns the constraints of one table."""
        dialect = SpannerDialect()
        connection = MagicMock()
        mock_snapshot = MagicMock()
        mock_snapshot.execute_sql.return_value = [
            ["", "parent", "IDX_parent_a_b_U", "a"],
            ["", "parent", "IDX_parent_a_b_U", "b"],
        ]
        connection.connection.database.snapshot.return_value.__enter__.return_value = (
            mock_snapshot
        )

        eq_(
            dialect.get_unique_constraints(connection, "parent"),
            [{"name": "IDX_parent_a_b_U", "column_names": ["a", "b"]}],
        )
        executed_sql = mock_snapshot.execute_sql.call_args[0][0]
        assert "tc.table_name = 'parent'" in executed_sql

        mock_snapshot.execute_sql.return_value = []
        eq_(dialect.get_unique_constraints(connection, "no_constraints"), [])

    def test_max_size_exported(self):
        """Test MAX_SIZE export and int_from_size helper behavior."""
        from google.cloud.sqlalchemy_spanner import MAX_SIZE
        from google.cloud.sqlalchemy_spanner.sqlalchemy_spanner import (
            _max_size,
            int_from_size,
        )

        eq_(MAX_SIZE, 2621440)
        eq_(_max_size, MAX_SIZE)
        eq_(SpannerDialect.max_size, MAX_SIZE)
        eq_(int_from_size("MAX"), 2621440)
        eq_(int_from_size("100"), 100)
