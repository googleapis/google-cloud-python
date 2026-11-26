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

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
import sqlalchemy as sa
import sqlparse
from google.cloud.spanner_dbapi import parse_utils
from sqlalchemy.schema import CreateTable
from sqlalchemy.sql import quoted_name
from sqlalchemy.sql.compiler import OPERATORS
from sqlalchemy.sql.operators import json_getitem_op
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

    def test_json_getitem_sql_injection_prevented(self):
        """Test that malicious JSON keys cannot inject SQL."""
        dialect = SpannerDialect()
        records = sa.Table("records", sa.MetaData(), sa.Column("data", sa.JSON))
        malicious_key = (
            'display") FROM records WHERE FALSE UNION ALL '
            "SELECT (SELECT secret FROM secrets) -- injected"
        )

        stmt = sa.select(records.c.data[malicious_key].as_string())

        # 1. Default parameterized compilation
        compiled = stmt.compile(dialect=dialect)
        eq_(
            compiled.string,
            "SELECT JSON_VALUE(records.data, :data_1) AS anon_1 \nFROM records",
        )
        assert "UNION ALL" not in compiled.string
        assert "secrets" not in compiled.string
        raw_params = compiled.construct_params()
        eq_(len(raw_params), 1)
        param_name, raw_val = next(iter(raw_params.items()))
        processed_val = compiled._bind_processors[param_name](raw_val)
        eq_(
            processed_val,
            '$."display\\") FROM records WHERE FALSE UNION ALL '
            'SELECT (SELECT secret FROM secrets) -- injected"',
        )

        # 2. Literal binds compilation (e.g., Computed columns or literal_binds=True)
        compiled_literal = stmt.compile(
            dialect=dialect, compile_kwargs={"literal_binds": True}
        )
        eq_(
            compiled_literal.string,
            'SELECT JSON_VALUE(records.data, "$.\\"display\\\\\\") '
            "FROM records WHERE FALSE UNION ALL "
            'SELECT (SELECT secret FROM secrets) -- injected\\"") AS anon_1 \n'
            "FROM records",
        )

        # 3. Verify OPERATORS is not polluted and direct binary dispatch works
        assert json_getitem_op not in OPERATORS
        binary_expr = records.c.data[malicious_key]
        direct_compiler = dialect.statement_compiler(dialect, sa.select(records.c.data))
        direct_sql = direct_compiler.process(binary_expr)
        eq_(direct_sql, "JSON_VALUE(records.data, :data_1)")

    def test_json_getitem_adversarial_keys_and_types(self):
        """Test JSON indexing with 0, empty string, backslashes, and quotes."""
        dialect = SpannerDialect(paramstyle="format")
        records = sa.Table("records", sa.MetaData(), sa.Column("data", sa.JSON))

        cases = [
            ("display", '$."display"', '"$.\\"display\\""'),
            (0, "$[0]", '"$[0]"'),
            (3, "$[3]", '"$[3]"'),
            (True, '$."True"', '"$.\\"True\\""'),
            (False, '$."False"', '"$.\\"False\\""'),
            ("", '$.""', '"$.\\"\\""'),
            ('a"b', '$."a\\"b"', '"$.\\"a\\\\\\"b\\""'),
            ("a'b", '$."a\'b"', '"$.\\"a\\\'b\\""'),
            ("a\\b", '$."a\\b"', '"$.\\"a\\\\b\\""'),
            ("a\\", '$."a\\\\"', '"$.\\"a\\\\\\\\\\""'),
            ("foo\\\n", '$."foo\\\n"', '"$.\\"foo\\\\\\n\\""'),
            ('a\\"b', '$."a\\\\\\"b"', '"$.\\"a\\\\\\\\\\\\\\"b\\""'),
            ('"""', '$."\\"\\"\\""', '"$.\\"\\\\\\"\\\\\\"\\\\\\"\\""'),
            (
                "a\nb\tc\rd\0e\x7f",
                '$."a\nb\tc\rd\0e\x7f"',
                '"$.\\"a\\nb\\tc\\rd\\u0000e\\u007f\\""',
            ),
            ("%s", '$."%s"', '"$.\\"%%s\\""'),
        ]

        for key, expected_bind, expected_literal in cases:
            stmt = sa.select(records.c.data[key].as_string())
            compiled = stmt.compile(dialect=dialect)
            eq_(
                compiled.string,
                "SELECT JSON_VALUE(records.data, %s) AS anon_1 \nFROM records",
            )
            param_name, raw_val = next(iter(compiled.construct_params().items()))
            processed = compiled._bind_processors[param_name](raw_val)
            eq_(processed, expected_bind)

            compiled_lit = stmt.compile(
                dialect=dialect, compile_kwargs={"literal_binds": True}
            )
            eq_(
                compiled_lit.string,
                f"SELECT JSON_VALUE(records.data, {expected_literal}) AS anon_1 \n"
                "FROM records",
            )

        # Also test non-ClauseElement fallback in visit_json_getitem_op_binary
        compiler = dialect.statement_compiler(dialect, sa.select(records.c.data))
        for right_obj in (
            SimpleNamespace(value='display") --'),
            MagicMock(value='display") --'),
        ):
            fake_binary = SimpleNamespace(
                left=records.c.data,
                right=right_obj,
                operator=json_getitem_op,
            )
            eq_(
                compiler.visit_json_getitem_op_binary(fake_binary, json_getitem_op),
                'JSON_VALUE(records.data, "$.\\"display\\\\\\") --\\"")',
            )

    def test_json_path_getitem_compilation_and_escaping(self):
        """Test JSON path tuple indexing in parameterized and literal modes."""
        dialect = SpannerDialect(paramstyle="format")
        records = sa.Table("records", sa.MetaData(), sa.Column("data", sa.JSON))
        path = ("users", 0, True, 'first"name', "back\\")

        stmt = sa.select(records.c.data[path].as_string())
        compiled = stmt.compile(dialect=dialect)
        eq_(
            compiled.string,
            "SELECT JSON_VALUE(records.data, %s) AS anon_1 \nFROM records",
        )
        param_name, raw_val = next(iter(compiled.construct_params().items()))
        processed = compiled._bind_processors[param_name](raw_val)
        eq_(processed, '$."users"[0]."True"."first\\"name"."back\\\\"')

        compiled_lit = stmt.compile(
            dialect=dialect, compile_kwargs={"literal_binds": True}
        )
        eq_(
            compiled_lit.string,
            "SELECT JSON_VALUE(records.data, "
            '"$.\\"users\\"[0].\\"True\\".\\"first\\\\\\"name\\".\\"back\\\\\\\\\\"") '
            "AS anon_1 \nFROM records",
        )

    def test_json_getitem_statement_cache_and_bindparam_reuse(self):
        """Test statement caching and explicit bindparam reuse without mutation."""
        dialect = SpannerDialect()
        records = sa.Table(
            "records",
            sa.MetaData(),
            sa.Column("data", sa.JSON),
            sa.Column("name", sa.String),
        )
        cache = {}

        stmt1 = sa.select(records.c.data["key1"].as_string())
        stmt2 = sa.select(records.c.data["key2"].as_string())

        c1, params1, *_ = stmt1._compile_w_cache(
            dialect, compiled_cache=cache, column_keys=[]
        )
        c2, params2, *_ = stmt2._compile_w_cache(
            dialect, compiled_cache=cache, column_keys=[]
        )
        eq_(len(cache), 1)

        constructed1 = c1.construct_params(extracted_parameters=params1)
        constructed2 = c2.construct_params(extracted_parameters=params2)
        bname1, val1 = next(iter(constructed1.items()))
        bname2, val2 = next(iter(constructed2.items()))

        eq_(c1._bind_processors[bname1](val1), '$."key1"')
        eq_(c2._bind_processors[bname2](val2), '$."key2"')

        # Explicit valued bindparam reused across JSON and non-JSON expressions
        bp = sa.bindparam("k", "shared_key")
        bp_cache = {}
        stmt_bp1 = sa.select(records.c.data[bp].as_string())
        stmt_bp2 = sa.select(records.c.data[bp].as_string())
        c_bp1, p_bp1, *_ = stmt_bp1._compile_w_cache(
            dialect, compiled_cache=bp_cache, column_keys=[]
        )
        c_bp2, p_bp2, *_ = stmt_bp2._compile_w_cache(
            dialect, compiled_cache=bp_cache, column_keys=[]
        )
        eq_(len(bp_cache), 1)
        eq_(
            c_bp2._bind_processors["k"](
                c_bp2.construct_params(extracted_parameters=p_bp2)["k"]
            ),
            '$."shared_key"',
        )

        # Ensure bp.type was not mutated in-place for non-JSON comparisons
        stmt_name = sa.select(records.c.name).where(records.c.name == bp)
        c_name = stmt_name.compile(dialect=dialect)
        name_val = c_name.construct_params()["k"]
        if "k" in c_name._bind_processors:
            name_val = c_name._bind_processors["k"](name_val)
        eq_(name_val, "shared_key")

        # Explicit bindparam with tuple path (compile-time, cache hit, and runtime)
        path_cache = {}
        stmt_path = sa.select(
            records.c.data[sa.bindparam("p", value=("a", 0, "b"))].as_string()
        )
        stmt_untyped = sa.select(records.c.data[sa.bindparam("p")].as_string())
        c_path, p_path, *_ = stmt_path._compile_w_cache(
            dialect, compiled_cache=path_cache, column_keys=[]
        )
        c_untyped, _, *_ = stmt_untyped._compile_w_cache(
            dialect, compiled_cache=path_cache, column_keys=[]
        )
        eq_(len(path_cache), 1)
        eq_(
            c_path._bind_processors["p"](
                c_path.construct_params(extracted_parameters=p_path)["p"]
            ),
            '$."a"[0]."b"',
        )
        eq_(c_untyped._bind_processors["p"]("my_key"), '$."my_key"')
        eq_(c_untyped._bind_processors["p"](0), "$[0]")
        eq_(c_untyped._bind_processors["p"](("x", 1, "y")), '$."x"[1]."y"')

    def test_render_literal_value_triple_quote_and_trailing_escape(self):
        """Test render_literal_value escapes strings breaking raw triple quotes."""
        dialect = SpannerDialect(paramstyle="format")
        compiler = dialect.statement_compiler(dialect, sa.select(sa.literal("x")))

        eq_(
            compiler.render_literal_value('a"""b', sa.String()),
            '"a\\"\\"\\"b"',
        )
        eq_(
            compiler.render_literal_value('ends_with_quote"', sa.String()),
            '"ends_with_quote\\""',
        )
        eq_(
            compiler.render_literal_value("ends_with_backslash\\", sa.String()),
            '"ends_with_backslash\\\\"',
        )
        eq_(
            compiler.render_literal_value("has\rcarriage_return", sa.String()),
            '"has\\rcarriage_return"',
        )
        eq_(
            compiler.render_literal_value("has\x00null", sa.String()),
            '"has\\u0000null"',
        )
        eq_(
            compiler.render_literal_value('100% "quoted" mid', sa.String()),
            'r"""100%% "quoted" mid"""',
        )

    def test_unqualified_delete_compiles_with_dummy_where(self):
        """Test that unqualified DELETE statements automatically append WHERE 1=1."""
        dialect = SpannerDialect()
        test_table = sa.table("my_table", sa.column("id"))
        statement = sa.delete(test_table)
        compiled = str(statement.compile(dialect=dialect))
        eq_(compiled, "DELETE FROM my_table WHERE 1=1")

    def test_qualified_delete_compiles_without_dummy_where(self):
        """Test that qualified DELETE statements do not append extra WHERE 1=1."""
        dialect = SpannerDialect()
        test_table = sa.table("my_table", sa.column("id"))
        statement = sa.delete(test_table).where(test_table.c.id == 1)
        compiled = str(statement.compile(dialect=dialect))
        eq_(compiled, "DELETE FROM my_table WHERE my_table.id = :id_1")

    def test_unqualified_update_compiles_with_dummy_where(self):
        """Test that unqualified UPDATE statements automatically append WHERE 1=1."""
        dialect = SpannerDialect()
        test_table = sa.table("my_table", sa.column("id"))
        statement = sa.update(test_table).values(id=2)
        compiled = str(statement.compile(dialect=dialect))
        eq_(compiled, "UPDATE my_table SET id=:id WHERE 1=1")

    def test_qualified_update_compiles_without_dummy_where(self):
        """Test that qualified UPDATE statements do not append extra WHERE 1=1."""
        dialect = SpannerDialect()
        test_table = sa.table("my_table", sa.column("id"))
        statement = sa.update(test_table).where(test_table.c.id == 1).values(id=2)
        compiled = str(statement.compile(dialect=dialect))
        eq_(compiled, "UPDATE my_table SET id=:id WHERE my_table.id = :id_1")

    def test_unqualified_delete_with_returning_compiles_with_dummy_where(
        self,
    ):
        """Test unqualified DELETE with RETURNING has WHERE 1=1 before THEN RETURN."""
        dialect = SpannerDialect()
        test_table = sa.table("my_table", sa.column("id"))
        statement = sa.delete(test_table).returning(test_table.c.id)
        compiled = str(statement.compile(dialect=dialect))
        eq_(compiled, "DELETE FROM my_table WHERE 1=1 THEN RETURN id")

    def test_unqualified_update_with_returning_compiles_with_dummy_where(
        self,
    ):
        """Test unqualified UPDATE with RETURNING has WHERE 1=1 before THEN RETURN."""
        dialect = SpannerDialect()
        test_table = sa.table("my_table", sa.column("id"))
        statement = sa.update(test_table).values(id=2).returning(test_table.c.id)
        compiled = str(statement.compile(dialect=dialect))
        eq_(compiled, "UPDATE my_table SET id=:id WHERE 1=1 THEN RETURN id")

    def test_delete_with_comparison_operators_does_not_raise_type_error(self):
        """Test that DELETE with >, IN, LIKE operators compiles without TypeError."""
        dialect = SpannerDialect()
        test_table = sa.table("my_table", sa.column("id"), sa.column("val"))

        stmt_gt = sa.delete(test_table).where(test_table.c.id > 1)
        eq_(
            str(stmt_gt.compile(dialect=dialect)),
            "DELETE FROM my_table WHERE my_table.id > :id_1",
        )

        stmt_in = sa.delete(test_table).where(test_table.c.id.in_([1, 2]))
        eq_(
            str(stmt_in.compile(dialect=dialect)),
            "DELETE FROM my_table WHERE my_table.id IN (__[POSTCOMPILE_id_1])",
        )

    def test_update_with_comparison_operators_does_not_raise_type_error(self):
        """Test that UPDATE with >, IN, LIKE operators compiles without TypeError."""
        dialect = SpannerDialect()
        test_table = sa.table("my_table", sa.column("id"), sa.column("val"))

        stmt_gt = sa.update(test_table).where(test_table.c.id > 1).values(val="x")
        eq_(
            str(stmt_gt.compile(dialect=dialect)),
            "UPDATE my_table SET val=:val WHERE my_table.id > :id_1",
        )

    def test_manual_raw_sql_compiles_without_dummy_where(self):
        """Test that manually written raw SQL text constructs compile as written.

        SpannerSQLCompiler injects WHERE 1=1 only for SQLAlchemy Core/ORM ASTs
        (e.g. delete(table) or update(table)). Manually written raw SQL text
        constructs (e.g. text("DELETE FROM my_table")) are compiled without
        modification.
        """
        dialect = SpannerDialect()

        # 1. Raw SQL text without WHERE clause is compiled as written
        raw_delete = sa.text("DELETE FROM my_table")
        eq_(str(raw_delete.compile(dialect=dialect)), "DELETE FROM my_table")

        raw_update = sa.text("UPDATE my_table SET id = 1")
        eq_(str(raw_update.compile(dialect=dialect)), "UPDATE my_table SET id = 1")

        # 2. Raw SQL text with explicit WHERE 1=1 or WHERE TRUE is compiled as written
        raw_delete_with_where = sa.text("DELETE FROM my_table WHERE 1=1")
        eq_(
            str(raw_delete_with_where.compile(dialect=dialect)),
            "DELETE FROM my_table WHERE 1=1",
        )

        raw_update_with_where = sa.text("UPDATE my_table SET id = 1 WHERE TRUE")
        eq_(
            str(raw_update_with_where.compile(dialect=dialect)),
            "UPDATE my_table SET id = 1 WHERE TRUE",
        )

        # 3. Contrast with ORM/Core ASTs which automatically generate WHERE 1=1
        test_table = sa.table("my_table", sa.column("id"))
        ast_delete = sa.delete(test_table)
        eq_(str(ast_delete.compile(dialect=dialect)), "DELETE FROM my_table WHERE 1=1")

        ast_update = sa.update(test_table).values(id=1)
        eq_(
            str(ast_update.compile(dialect=dialect)),
            "UPDATE my_table SET id=:id WHERE 1=1",
        )

    def test_empty_where_appends_dummy_where(self):
        """Test that calling .where() without criteria appends WHERE 1=1."""
        dialect = SpannerDialect()
        test_table = sa.table("my_table", sa.column("id"))

        delete_stmt = sa.delete(test_table).where()
        eq_(str(delete_stmt.compile(dialect=dialect)), "DELETE FROM my_table WHERE 1=1")

        update_stmt = sa.update(test_table).values(id=1).where()
        eq_(
            str(update_stmt.compile(dialect=dialect)),
            "UPDATE my_table SET id=:id WHERE 1=1",
        )

    def test_explicit_literal_where_does_not_duplicate(self):
        """Test that explicit WHERE 1=1 does not produce WHERE 1=1 AND 1=1."""
        dialect = SpannerDialect()
        test_table = sa.table("my_table", sa.column("id"))

        delete_stmt = sa.delete(test_table).where(sa.literal_column("1=1"))
        eq_(str(delete_stmt.compile(dialect=dialect)), "DELETE FROM my_table WHERE 1=1")

        update_stmt = sa.update(test_table).values(id=1).where(sa.literal_column("1=1"))
        eq_(
            str(update_stmt.compile(dialect=dialect)),
            "UPDATE my_table SET id=:id WHERE 1=1",
        )

    def test_json_binary_dispatch_and_operators_table_integrity(self):
        """Test that JSON binary dispatch uses visitor methods and OPERATORS is pure."""
        dialect = SpannerDialect()
        records = sa.Table(
            "records",
            sa.MetaData(),
            sa.Column("id", sa.Integer),
            sa.Column("data", sa.JSON),
        )

        # 1. Global OPERATORS table is not mutated and only contains str values
        assert json_getitem_op not in OPERATORS
        assert all(isinstance(value, str) for value in OPERATORS.values())

        # 2. JSON indexing dispatches cleanly via visit_binary ->
        # visit_json_getitem_op_binary
        compiler = dialect.statement_compiler(dialect, sa.select(records))
        json_binary = records.c.data["key"]
        eq_(compiler.visit_binary(json_binary), "JSON_VALUE(records.data, :data_1)")

        # 3. Standard binary operators that rely on base
        # _generate_generic_binary still work
        compiler = dialect.statement_compiler(dialect, sa.select(records))
        generic_binary = records.c.id + 10
        eq_(compiler.visit_binary(generic_binary), "records.id + :id_1")

        compiler = dialect.statement_compiler(dialect, sa.select(records))
        comparison_binary = records.c.id == 5
        eq_(compiler.visit_binary(comparison_binary), "records.id = :id_1")

        # 4. Comparison operators with JSON subscript (exercises both
        # base _generate_generic_binary and visit_json_getitem_op_binary)
        stmt_where = sa.select(records).where(records.c.data["type"] == "Stadium")
        eq_(
            str(stmt_where.compile(dialect=dialect)),
            "SELECT records.id, records.data \n"
            "FROM records \n"
            "WHERE JSON_VALUE(records.data, :data_1) = :param_1",
        )

        stmt_is_null = sa.select(records).where(records.c.data["type"].is_(None))
        eq_(
            str(stmt_is_null.compile(dialect=dialect)),
            "SELECT records.id, records.data \n"
            "FROM records \n"
            "WHERE JSON_VALUE(records.data, :data_1) IS NULL",
        )

    def test_post_create_table_quotes_primary_key_columns(self):
        """Test that PRIMARY KEY columns are quoted when required."""
        dialect = SpannerDialect()
        metadata = sa.MetaData()

        # Composite PK with reserved keyword, mixed-case, explicit quote=True,
        # and normal lowercase.
        composite_table = sa.Table(
            "orders",
            metadata,
            sa.Column("order", sa.Integer, primary_key=True),
            sa.Column("UserId", sa.String(32), primary_key=True),
            sa.Column(quoted_name("lower", quote=True), sa.Integer, primary_key=True),
            sa.Column("id", sa.Integer, primary_key=True),
        )
        eq_(
            str(CreateTable(composite_table).compile(dialect=dialect)),
            "\nCREATE TABLE orders (\n"
            "\t`order` INT64 NOT NULL, \n"
            "\t`UserId` STRING(32) NOT NULL, \n"
            "\t`lower` INT64 NOT NULL, \n"
            "\tid INT64 NOT NULL\n"
            ") PRIMARY KEY (`order`, `UserId`, `lower`, id)\n\n",
        )

        # Explicit quote=False via quoted_name is respected.
        unquoted_table = sa.Table(
            "explicit_unquoted",
            metadata,
            sa.Column(quoted_name("MyCol", quote=False), sa.Integer, primary_key=True),
        )
        eq_(
            str(CreateTable(unquoted_table).compile(dialect=dialect)),
            "\nCREATE TABLE explicit_unquoted (\n"
            "\tMyCol INT64 NOT NULL GENERATED BY DEFAULT AS IDENTITY "
            "(BIT_REVERSED_POSITIVE)\n"
            ") PRIMARY KEY (MyCol)\n\n",
        )

        # A column marked is_literal=True must still be quoted in PRIMARY KEY.
        literal_column = sa.Column("bad; DROP TABLE x", sa.Integer, primary_key=True)
        literal_column.is_literal = True
        literal_table = sa.Table("literal_pk", metadata, literal_column)
        compiler = dialect.ddl_compiler(dialect, CreateTable(literal_table))
        eq_(
            compiler.post_create_table(literal_table),
            " PRIMARY KEY (`bad; DROP TABLE x`)",
        )

        # Table without primary key emits empty PRIMARY KEY ().
        keyless_table = sa.Table("keyless", metadata, sa.Column("value", sa.Integer))
        eq_(
            str(CreateTable(keyless_table).compile(dialect=dialect)),
            "\nCREATE TABLE keyless (\n\tvalue INT64\n) PRIMARY KEY ()\n\n",
        )

    def test_post_create_table_prevents_primary_key_ddl_injection(self):
        """Test that malicious PK column names cannot break out into stacked DDL."""
        dialect = SpannerDialect()
        malicious_column = "id); DROP TABLE users; --"
        single_pk_table = sa.Table(
            "items",
            sa.MetaData(),
            sa.Column(malicious_column, sa.Integer, primary_key=True),
        )
        compiled_single = str(CreateTable(single_pk_table).compile(dialect=dialect))
        eq_(
            compiled_single,
            "\nCREATE TABLE items (\n"
            f"\t`{malicious_column}` INT64 NOT NULL "
            "GENERATED BY DEFAULT AS IDENTITY (BIT_REVERSED_POSITIVE)\n"
            f") PRIMARY KEY (`{malicious_column}`)\n\n",
        )

        composite_pk_table = sa.Table(
            "composite_items",
            sa.MetaData(),
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column(malicious_column, sa.String(32), primary_key=True),
        )
        compiled_composite = str(
            CreateTable(composite_pk_table).compile(dialect=dialect)
        )
        eq_(
            compiled_composite,
            "\nCREATE TABLE composite_items (\n"
            "\tid INT64 NOT NULL, \n"
            f"\t`{malicious_column}` STRING(32) NOT NULL\n"
            f") PRIMARY KEY (id, `{malicious_column}`)\n\n",
        )

        for compiled_ddl in (compiled_single, compiled_composite):
            statements = [
                statement
                for statement in sqlparse.split(compiled_ddl)
                if statement.strip()
            ]
            eq_(len(statements), 1)
            eq_(
                parse_utils.classify_statement(statements[0]).statement_type,
                parse_utils.StatementType.DDL,
            )

    def test_post_create_table_quotes_interleave_in_and_prevents_ddl_injection(self):
        """Test that spanner_interleave_in is quoted and safe against DDL injection."""
        dialect = SpannerDialect()
        shared_metadata = sa.MetaData()
        plain_parent = sa.Table(
            "Parent", shared_metadata, sa.Column("id", sa.Integer, primary_key=True)
        )
        schema_parent = sa.Table(
            "Parent",
            shared_metadata,
            sa.Column("id", sa.Integer, primary_key=True),
            schema="MySchema",
        )
        unquoted_schema_parent = sa.Table(
            quoted_name("Parent", quote=False),
            sa.MetaData(),
            sa.Column("id", sa.Integer, primary_key=True),
            schema=quoted_name("MySchema", quote=False),
        )
        malicious_table_parent = sa.Table(
            "Parent; DROP TABLE x",
            shared_metadata,
            sa.Column("id", sa.Integer, primary_key=True),
            schema="Schema; DROP TABLE y",
        )

        cases = [
            ("order", False, False, "\nINTERLEAVE IN PARENT `order`"),
            (
                "ParentTable",
                True,
                False,
                "\nINTERLEAVE IN PARENT `ParentTable` ON DELETE CASCADE",
            ),
            ("team", False, True, "\nINTERLEAVE IN PARENT team"),
            ("", True, True, None),
            (None, True, False, None),
            (
                quoted_name("order", quote=False),
                False,
                False,
                "\nINTERLEAVE IN PARENT order",
            ),
            (
                quoted_name("lower", quote=True),
                False,
                False,
                "\nINTERLEAVE IN PARENT `lower`",
            ),
            (
                plain_parent,
                True,
                False,
                "\nINTERLEAVE IN PARENT `Parent` ON DELETE CASCADE",
            ),
            (
                schema_parent,
                False,
                False,
                "\nINTERLEAVE IN PARENT `MySchema`.`Parent`",
            ),
            (
                unquoted_schema_parent,
                False,
                False,
                "\nINTERLEAVE IN PARENT MySchema.Parent",
            ),
            (
                malicious_table_parent,
                False,
                False,
                "\nINTERLEAVE IN PARENT `Schema; DROP TABLE y`.`Parent; DROP TABLE x`",
            ),
            (
                "team; DROP TABLE users; --",
                False,
                False,
                "\nINTERLEAVE IN PARENT `team; DROP TABLE users; --`",
            ),
        ]

        for index, (parent, cascade, use_reserved_pk, expected_clause) in enumerate(
            cases
        ):
            table_kwargs = {"spanner_interleave_in": parent}
            if cascade:
                table_kwargs["spanner_interleave_on_delete_cascade"] = True

            if use_reserved_pk:
                columns = [
                    sa.Column("order", sa.Integer, primary_key=True),
                    sa.Column("UserId", sa.String(16), primary_key=True),
                ]
                expected_columns = (
                    "\t`order` INT64 NOT NULL, \n\t`UserId` STRING(16) NOT NULL"
                )
                expected_pk = "`order`, `UserId`"
            else:
                columns = [sa.Column("id", sa.Integer, primary_key=True)]
                expected_columns = (
                    "\tid INT64 NOT NULL "
                    "GENERATED BY DEFAULT AS IDENTITY (BIT_REVERSED_POSITIVE)"
                )
                expected_pk = "id"

            child_table = sa.Table(
                f"child_{index}", sa.MetaData(), *columns, **table_kwargs
            )
            compiled_ddl = str(CreateTable(child_table).compile(dialect=dialect))
            expected_suffix = (
                f",{expected_clause}" if expected_clause is not None else ""
            )
            eq_(
                compiled_ddl,
                f"\nCREATE TABLE child_{index} (\n"
                f"{expected_columns}\n"
                f") PRIMARY KEY ({expected_pk}){expected_suffix}\n\n",
            )
            statements = [
                statement
                for statement in sqlparse.split(compiled_ddl)
                if statement.strip()
            ]
            eq_(len(statements), 1)
            eq_(
                parse_utils.classify_statement(statements[0]).statement_type,
                parse_utils.StatementType.DDL,
            )

        for invalid_parent in (123, False, b"team"):
            invalid_table = sa.Table(
                "invalid_interleave",
                sa.MetaData(),
                sa.Column("id", sa.Integer, primary_key=True),
                spanner_interleave_in=invalid_parent,
            )
            with pytest.raises(
                TypeError, match="spanner_interleave_in must be a string or Table"
            ):
                CreateTable(invalid_table).compile(dialect=dialect)

    @pytest.mark.skip(
        reason=(
            "Requires SpannerIdentifierPreparer escaping from "
            "https://github.com/googleapis/google-cloud-python/pull/19210"
        )
    )
    def test_post_create_table_prevents_backtick_backslash_and_newline_ddl_injection(
        self,
    ):
        """Test PK and spanner_interleave_in escaping for backticks, \\, and \\n."""
        dialect = SpannerDialect()

        pk_cases = [
            ("id`); DROP TABLE users; --", r"id\u0060); DROP TABLE users; --"),
            ("id\\", r"id\\"),
            ("id\n; DROP TABLE users; --", r"id\n; DROP TABLE users; --"),
        ]
        for index, (raw_column, expected_escaped) in enumerate(pk_cases):
            table = sa.Table(
                f"pk_escape_{index}",
                sa.MetaData(),
                sa.Column(raw_column, sa.Integer, primary_key=True),
            )
            compiled_ddl = str(CreateTable(table).compile(dialect=dialect))
            eq_(
                compiled_ddl,
                f"\nCREATE TABLE pk_escape_{index} (\n"
                f"\t`{expected_escaped}` INT64 NOT NULL "
                "GENERATED BY DEFAULT AS IDENTITY (BIT_REVERSED_POSITIVE)\n"
                f") PRIMARY KEY (`{expected_escaped}`)\n\n",
            )
            statements = [
                statement
                for statement in sqlparse.split(compiled_ddl)
                if statement.strip()
            ]
            eq_(len(statements), 1)
            eq_(
                parse_utils.classify_statement(statements[0]).statement_type,
                parse_utils.StatementType.DDL,
            )

        interleave_cases = [
            ("team`); DROP TABLE users; --", r"team\u0060); DROP TABLE users; --"),
            ("team\\", r"team\\"),
            ("team\n; DROP TABLE users; --", r"team\n; DROP TABLE users; --"),
        ]
        for index, (raw_parent, expected_escaped) in enumerate(interleave_cases):
            table = sa.Table(
                f"interleave_escape_{index}",
                sa.MetaData(),
                sa.Column("id", sa.Integer, primary_key=True),
                spanner_interleave_in=raw_parent,
            )
            compiled_ddl = str(CreateTable(table).compile(dialect=dialect))
            eq_(
                compiled_ddl,
                f"\nCREATE TABLE interleave_escape_{index} (\n"
                "\tid INT64 NOT NULL "
                "GENERATED BY DEFAULT AS IDENTITY (BIT_REVERSED_POSITIVE)\n"
                f") PRIMARY KEY (id),\n"
                f"INTERLEAVE IN PARENT `{expected_escaped}`\n\n",
            )
            statements = [
                statement
                for statement in sqlparse.split(compiled_ddl)
                if statement.strip()
            ]
            eq_(len(statements), 1)
            eq_(
                parse_utils.classify_statement(statements[0]).statement_type,
                parse_utils.StatementType.DDL,
            )
