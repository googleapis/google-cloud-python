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

import unittest

from sqlalchemy import Column, Computed, Integer, MetaData, String, Table, select
from sqlalchemy.schema import CreateTable

from google.cloud.sqlalchemy_spanner import (
    TOKENLIST,
    AddTokenlistColumn,
    CreatePropertyGraph,
    CreateSearchIndex,
    DropColumn,
    DropPropertyGraph,
    DropSearchIndex,
    SpannerDialect,
    score,
    score_ngrams,
    search,
    search_substring,
    tokenize_array,
    tokenize_bool,
    tokenize_fulltext,
    tokenize_ngrams,
    tokenize_number,
    tokenize_substring,
)
from google.cloud.sqlalchemy_spanner.sqlalchemy_spanner import _type_map, _type_map_inv


class DDLTypesAndFunctionsTest(unittest.TestCase):
    def setUp(self):
        self.dialect = SpannerDialect()

    def test_tokenlist_compilation(self):
        tokenlist_type = TOKENLIST()
        compiled = tokenlist_type.compile(dialect=self.dialect)
        self.assertEqual(compiled, "TOKENLIST")

    def test_type_map_registration(self):
        self.assertIn("TOKENLIST", _type_map)
        self.assertEqual(_type_map["TOKENLIST"], TOKENLIST)
        self.assertEqual(_type_map_inv[TOKENLIST], "TOKENLIST")

    def test_computed_column_stored(self):
        metadata = MetaData()
        table = Table(
            "users",
            metadata,
            Column("id", String(20), primary_key=True),
            Column("first_name", String(50)),
            Column("last_name", String(50)),
            Column(
                "full_name",
                String(100),
                Computed("first_name || last_name", persisted=True),
            ),
        )
        ddl = str(CreateTable(table).compile(dialect=self.dialect))
        self.assertIn("full_name STRING(100) AS (first_name || last_name) STORED", ddl)

    def test_computed_column_hidden(self):
        metadata = MetaData()
        table = Table(
            "articles",
            metadata,
            Column("id", String(36), primary_key=True),
            Column("title", String(200)),
            Column(
                "title_tokens",
                TOKENLIST,
                Computed(tokenize_fulltext("title")),
                spanner_hidden=True,
            ),
        )
        ddl = str(CreateTable(table).compile(dialect=self.dialect))
        self.assertIn(
            "title_tokens TOKENLIST AS (TOKENIZE_FULLTEXT('title')) HIDDEN", ddl
        )

    def test_fts_functions_compilation(self):
        metadata = MetaData()
        table = Table(
            "docs",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("tokens", TOKENLIST),
        )
        stmt = (
            select(table.c.id)
            .where(search(table.c.tokens, "cloud spanner"))
            .order_by(score(table.c.tokens, "cloud spanner").desc())
        )
        compiled = str(
            stmt.compile(dialect=self.dialect, compile_kwargs={"literal_binds": True})
        )
        self.assertIn("SEARCH(docs.tokens, 'cloud spanner')", compiled)
        self.assertIn("SCORE(docs.tokens, 'cloud spanner')", compiled)

    def test_search_substring_and_score_ngrams(self):
        metadata = MetaData()
        table = Table(
            "docs",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("tokens", TOKENLIST),
        )
        stmt = (
            select(table.c.id)
            .where(search_substring(table.c.tokens, "span"))
            .order_by(score_ngrams(table.c.tokens, "span").desc())
        )
        compiled = str(
            stmt.compile(dialect=self.dialect, compile_kwargs={"literal_binds": True})
        )
        self.assertIn("SEARCH_SUBSTRING(docs.tokens, 'span')", compiled)
        self.assertIn("SCORE_NGRAMS(docs.tokens, 'span')", compiled)

    def test_tokenizer_functions(self):
        def _compile(func):
            return str(
                func.compile(
                    dialect=self.dialect, compile_kwargs={"literal_binds": True}
                )
            )

        self.assertEqual(
            _compile(tokenize_fulltext("text")), "TOKENIZE_FULLTEXT('text')"
        )
        self.assertEqual(
            _compile(tokenize_substring("text")), "TOKENIZE_SUBSTRING('text')"
        )
        self.assertEqual(_compile(tokenize_ngrams("text")), "TOKENIZE_NGRAMS('text')")
        self.assertEqual(_compile(tokenize_bool(True)), "TOKENIZE_BOOL(true)")
        self.assertEqual(_compile(tokenize_number(42)), "TOKENIZE_NUMBER(42)")
        self.assertEqual(
            _compile(tokenize_array(["a", "b"])), "TOKENIZE_ARRAY(['a', 'b'])"
        )

    def test_create_and_drop_search_index_ddl(self):
        create_op = CreateSearchIndex(
            "idx_search", "articles", ["title_tokens"], storing=["title"]
        )
        compiled = str(create_op.compile(dialect=self.dialect))
        self.assertEqual(
            compiled,
            "CREATE SEARCH INDEX idx_search ON articles (title_tokens) STORING (title)",
        )

        drop_op = create_op.reverse()
        self.assertIsInstance(drop_op, DropSearchIndex)
        compiled_drop = str(drop_op.compile(dialect=self.dialect))
        self.assertEqual(compiled_drop, "DROP SEARCH INDEX IF EXISTS idx_search")

    def test_add_and_drop_tokenlist_column_ddl(self):
        add_op = AddTokenlistColumn(
            "articles", "title_tokens", "TOKENIZE_FULLTEXT(title)", hidden=True
        )
        compiled = str(add_op.compile(dialect=self.dialect))
        expected_add = (
            "ALTER TABLE articles ADD COLUMN title_tokens TOKENLIST "
            "AS (TOKENIZE_FULLTEXT(title)) HIDDEN"
        )
        self.assertEqual(compiled, expected_add)

        drop_op = add_op.reverse()
        self.assertIsInstance(drop_op, DropColumn)
        compiled_drop = str(drop_op.compile(dialect=self.dialect))
        self.assertEqual(compiled_drop, "ALTER TABLE articles DROP COLUMN title_tokens")

    def test_create_and_drop_property_graph_ddl(self):
        create_op = CreatePropertyGraph("my_graph", "NODE TABLES (Users)")
        compiled = str(create_op.compile(dialect=self.dialect))
        self.assertEqual(compiled, "CREATE PROPERTY GRAPH my_graph NODE TABLES (Users)")

        drop_op = create_op.reverse()
        self.assertIsInstance(drop_op, DropPropertyGraph)
        compiled_drop = str(drop_op.compile(dialect=self.dialect))
        self.assertEqual(compiled_drop, "DROP PROPERTY GRAPH IF EXISTS my_graph")
