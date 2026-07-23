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
from sqlalchemy import Column, Index, Table, MetaData, Uuid, types
from sqlalchemy.schema import CreateIndex
from sqlalchemy.testing import eq_
from sqlalchemy.testing.plugin.plugin_base import fixtures
from google.cloud.sqlalchemy_spanner.sqlalchemy_spanner import (
    _type_map,
    _type_map_inv,
    SpannerDialect,
    SpannerDDLCompiler,
)


class TestSpannerDialect(fixtures.TestBase):
    def test_tokenlist_in_type_map(self):
        """Test that TOKENLIST is registered in _type_map to prevent KeyError during reflection."""
        assert "TOKENLIST" in _type_map
        eq_(_type_map["TOKENLIST"], types.String)

    def test_uuid_in_type_map(self):
        """Test that native UUID is registered in _type_map."""
        assert "UUID" in _type_map
        eq_(_type_map["UUID"], types.UUID)

    def test_uuid_in_type_map_inv(self):
        """Test that types.UUID maps to 'UUID' in _type_map_inv."""
        assert types.UUID in _type_map_inv
        eq_(_type_map_inv[types.UUID], "UUID")

    def test_visit_uuid_compilation(self):
        """Test that SpannerTypeCompiler compiles types.UUID and Uuid to 'UUID'."""
        dialect = SpannerDialect()
        eq_(dialect.type_compiler.process(types.UUID()), "UUID")
        eq_(dialect.type_compiler.process(Uuid()), "UUID")

    def test_string36_backward_compatibility(self):
        """Test that existing String(36) compiles to STRING(36) without regression."""
        dialect = SpannerDialect()
        processed = dialect.type_compiler.process(types.String(36))
        eq_(processed, "STRING(36)")
        eq_(_type_map["STRING"], types.String)

    def test_get_multi_indexes_excludes_search_indexes_sql(self):
        """Test that get_multi_indexes SQL query excludes SEARCH indexes."""
        dialect = SpannerDialect()
        connection = MagicMock()
        mock_snapshot = MagicMock()
        mock_snapshot.execute_sql.return_value = []
        connection.connection.database.snapshot.return_value.__enter__.return_value = mock_snapshot

        dialect.get_multi_indexes(connection)

        # Retrieve the SQL executed by snapshot
        executed_sql = mock_snapshot.execute_sql.call_args[0][0]
        assert "i.index_type != 'SEARCH'" in executed_sql

    def test_get_multi_indexes_handles_none_column_ordering(self):
        """Test that get_multi_indexes does not crash when column_ordering has None elements."""
        dialect = SpannerDialect()
        connection = MagicMock()
        mock_snapshot = MagicMock()
        # Mock row: schema, table, index_name, columns, is_unique, column_orderings, storing_columns
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
        connection.connection.database.snapshot.return_value.__enter__.return_value = mock_snapshot

        res = dialect.get_multi_indexes(connection)
        assert ("public", "my_table") in res
        index_info = res[("public", "my_table")][0]
        eq_(index_info["column_sorting"]["col1"], None)

    def test_visit_create_index_storing_unbound_columns(self):
        """Test creating index with spanner_storing when storing columns are string names or unbound objects."""
        compiler = SpannerDDLCompiler(SpannerDialect(), None)
        metadata = MetaData()
        t = Table("t", metadata, Column("col1", types.String(100)))
        # In batch mode, storing columns may be string names not in t.c, or Column objects without t.c mapping
        idx = Index("ix_test", t.c.col1, spanner_storing=["storing_col1", Column("storing_col2", types.String(50))])

        create_index_op = CreateIndex(idx)
        ddl = compiler.visit_create_index(create_index_op)
        assert "STORING (storing_col1, storing_col2)" in ddl
