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

import ast
import re
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
import sqlalchemy as sa
from google.cloud.spanner_dbapi import parse_utils
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

    @pytest.mark.parametrize("paramstyle", ["format", "named"])
    @pytest.mark.parametrize(
        "value,expected",
        [
            (b"", 'b""'),
            (b"hello world", 'b"hello world"'),
            (rb"\' OR 1=1 --", 'b"\\x5c\\x27 OR 1=1 --"'),
            (
                b"a\"b'c\\d%s\x00\n\r\t\x7f\xff\xfe",
                'b"a\\x22b\\x27c\\x5cd\\x25s\\x00\\x0a\\x0d\\x09\\x7f\\xff\\xfe"',
            ),
            (bytearray(b"a\x00\xff"), 'b"a\\x00\\xff"'),
            (memoryview(b"a\x00\xff"), 'b"a\\x00\\xff"'),
            (memoryview(b"abcd").cast("I"), 'b"abcd"'),
            (memoryview(b"abcd").cast("B", (2, 2)), 'b"abcd"'),
            (None, "NULL"),
        ],
    )
    def test_render_literal_value_binary_escaping(self, paramstyle, value, expected):
        """Bytes literals use b"..." with special bytes hex-escaped."""
        dialect = SpannerDialect(paramstyle=paramstyle)
        compiler = dialect.statement_compiler(dialect, sa.select(sa.literal(b"x")))
        eq_(compiler.render_literal_value(value, sa.LargeBinary()), expected)

    def test_render_literal_value_all_256_bytes(self):
        """Every byte value 0x00..0xFF renders as valid b"..." output."""
        dialect = SpannerDialect(paramstyle="format")
        compiler = dialect.statement_compiler(dialect, sa.select(sa.literal(b"x")))
        all_bytes = bytes(range(256))
        rendered = compiler.render_literal_value(all_bytes, sa.LargeBinary())

        assert rendered.startswith('b"') and rendered.endswith('"')
        inner = rendered[2:-1]
        assert all(0x20 <= ord(ch) <= 0x7E for ch in inner)
        assert not any(ch in inner for ch in ('"', "'", "%"))
        # Every backslash must introduce an exact \xHH hex escape
        assert re.sub(r"\\x[0-9a-f]{2}", "", inner).find("\\") == -1
        eq_(ast.literal_eval(rendered), all_bytes)

    @pytest.mark.parametrize(
        "binary_type",
        [sa.LargeBinary(20), sa.BINARY(16), sa.VARBINARY(32), sa.BLOB(64)],
    )
    def test_render_literal_value_binary_types(self, binary_type):
        """LargeBinary, BINARY, VARBINARY, and BLOB keep length and escape."""
        dialect = SpannerDialect(paramstyle="format")
        compiler = dialect.statement_compiler(dialect, sa.select(sa.literal(b"x")))
        eq_(
            compiler.render_literal_value(rb"\' OR 1=1 --", binary_type),
            'b"\\x5c\\x27 OR 1=1 --"',
        )
        adapted = binary_type.dialect_impl(dialect)
        eq_(adapted.length, binary_type.length)
        processor = adapted.literal_processor(dialect)
        eq_(processor(None), "NULL")
        eq_(processor(rb"\' OR 1=1 --"), 'b"\\x5c\\x27 OR 1=1 --"')

    @pytest.mark.parametrize("bad_value", ["not bytes", 123, object()])
    def test_binary_literal_processor_rejects_non_bytes(self, bad_value):
        """Binary literal processor rejects non-bytes inputs with TypeError."""
        dialect = SpannerDialect(paramstyle="format")
        processor = sa.LargeBinary().dialect_impl(dialect).literal_processor(dialect)
        with pytest.raises(TypeError, match="Expected bytes-like object"):
            processor(bad_value)

    def test_binary_literal_unhappy_paths_and_mismatched_types(self):
        """Check NullType and str values passed alongside LargeBinary."""
        dialect = SpannerDialect(paramstyle="format")
        compiler = dialect.statement_compiler(dialect, sa.select(sa.literal(b"x")))

        # Untyped bytearray/memoryview default to NullType in SQLAlchemy
        with pytest.raises(
            NotImplementedError, match="Don't know how to literal-quote"
        ):
            compiler.render_literal_value(bytearray(b"a"), sa.types.NullType())

        # Any str passed directly with LargeBinary fails closed inside literal_processor
        for bad_str in ("plain", r"\' OR 1=1 --"):
            with pytest.raises(TypeError, match="Expected bytes-like object"):
                compiler.render_literal_value(bad_str, sa.LargeBinary())

    def test_binary_literal_binds_and_literal_execute(self):
        """Check literal_binds, literal_execute, IN, and mixed %s params."""
        dialect = SpannerDialect(paramstyle="format")
        items = sa.Table(
            "items",
            sa.MetaData(),
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("payload", sa.LargeBinary(20)),
            sa.Column("fixed", sa.BINARY(16)),
        )

        stmt = sa.select(items.c.id).where(
            items.c.payload == rb"\' OR 1=1 --",
            items.c.fixed == b"\xff\x00%s",
        )
        eq_(
            str(stmt.compile(dialect=dialect, compile_kwargs={"literal_binds": True})),
            "SELECT items.id \n"
            "FROM items \n"
            'WHERE items.payload = b"\\x5c\\x27 OR 1=1 --" '
            'AND items.fixed = b"\\xff\\x00\\x25s"',
        )

        # Mixed bound param + %s binary literal must not confuse spanner_dbapi pyformat
        mixed_stmt = sa.select(items.c.id).where(
            items.c.id == 1,
            items.c.payload == sa.literal(b"%s", literal_execute=True),
        )
        compiled_mixed = mixed_stmt.compile(dialect=dialect)
        expanded_mixed = compiled_mixed._process_parameters_for_postcompile(
            compiled_mixed.construct_params()
        )
        parsed_sql, parsed_params = parse_utils.sql_pyformat_args_to_spanner(
            expanded_mixed.statement, [compiled_mixed.construct_params()["id_1"]]
        )
        eq_(
            parsed_sql,
            "SELECT items.id \n"
            "FROM items \n"
            'WHERE items.id = @a0 AND items.payload = b"\\x25s"',
        )
        eq_(parsed_params, {"a0": 1})

        literal_exec_stmt = sa.select(
            sa.literal(rb"\' OR 1=1 --", literal_execute=True)
        )
        compiled_literal_exec = literal_exec_stmt.compile(dialect=dialect)
        expanded = compiled_literal_exec._process_parameters_for_postcompile(
            compiled_literal_exec.construct_params()
        )
        eq_(expanded.statement, 'SELECT b"\\x5c\\x27 OR 1=1 --" AS anon_1')

        expanding_stmt = sa.select(items.c.id).where(
            items.c.payload.in_(
                sa.bindparam(
                    "payloads",
                    [rb"\' OR 1=1 --", b"\xff\x00"],
                    expanding=True,
                    literal_execute=True,
                )
            )
        )
        compiled_expanding = expanding_stmt.compile(dialect=dialect)
        expanded_in = compiled_expanding._process_parameters_for_postcompile(
            compiled_expanding.construct_params()
        )
        eq_(
            expanded_in.statement,
            "SELECT items.id \n"
            "FROM items \n"
            'WHERE items.payload IN (b"\\x5c\\x27 OR 1=1 --", b"\\xff\\x00")',
        )

    def test_binary_literal_type_decorator_and_array(self):
        """TypeDecorator and ARRAY(LargeBinary) use Spanner bytes escaping."""

        class CustomBytesWrapper(sa.TypeDecorator):
            impl = sa.LargeBinary
            cache_ok = True

            def process_bind_param(self, value, dialect):
                return value.encode("utf-8") if isinstance(value, str) else value

        dialect = SpannerDialect(paramstyle="format")
        wrapped_literal_processor = CustomBytesWrapper()._cached_literal_processor(
            dialect
        )
        eq_(wrapped_literal_processor(r"\' OR 1=1 --"), 'b"\\x5c\\x27 OR 1=1 --"')

        array_literal_processor = sa.ARRAY(sa.LargeBinary).literal_processor(dialect)
        eq_(
            array_literal_processor([rb"\' OR 1=1 --", b"\xff"]),
            '[b"\\x5c\\x27 OR 1=1 --", b"\\xff"]',
        )
        eq_(array_literal_processor([b"a", None]), '[b"a", NULL]')
        with pytest.raises(TypeError, match="Expected bytes-like object"):
            array_literal_processor(["not_bytes"])

        items = sa.Table(
            "items",
            sa.MetaData(),
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("wrapped", CustomBytesWrapper()),
            sa.Column("tags", sa.ARRAY(sa.LargeBinary)),
        )
        wrapped_stmt = sa.select(items.c.id).where(items.c.wrapped == r"\' OR 1=1 --")
        eq_(
            str(
                wrapped_stmt.compile(
                    dialect=dialect, compile_kwargs={"literal_binds": True}
                )
            ),
            "SELECT items.id \n"
            "FROM items \n"
            'WHERE items.wrapped = b"\\x5c\\x27 OR 1=1 --"',
        )
        array_stmt = sa.select(items.c.id).where(items.c.tags == [rb"\' OR 1=1 --"])
        eq_(
            str(
                array_stmt.compile(
                    dialect=dialect, compile_kwargs={"literal_binds": True}
                )
            ),
            "SELECT items.id \n"
            "FROM items \n"
            'WHERE items.tags = [b"\\x5c\\x27 OR 1=1 --"]',
        )

    def test_binary_literal_with_variant(self):
        """Variant types targeting Spanner binary handle bytes and reject str."""
        dialect = SpannerDialect(paramstyle="format")
        binary_variant = sa.String().with_variant(sa.LargeBinary(), "spanner+spanner")
        stmt = sa.select(sa.literal(rb"\' OR 1=1 --", binary_variant))
        eq_(
            str(stmt.compile(dialect=dialect, compile_kwargs={"literal_binds": True})),
            'SELECT b"\\x5c\\x27 OR 1=1 --" AS anon_1',
        )

        str_stmt = sa.select(sa.literal(r"\' OR 1=1 --", binary_variant))
        with pytest.raises(TypeError, match="Expected bytes-like object"):
            str_stmt.compile(dialect=dialect, compile_kwargs={"literal_binds": True})

        class VariantWrapper(sa.TypeDecorator):
            impl = binary_variant
            cache_ok = True

            def process_bind_param(self, value, dialect):
                return value.encode("utf-8") if isinstance(value, str) else value

        wrapped_variant_stmt = sa.select(sa.literal(r"\' OR 1=1 --", VariantWrapper()))
        eq_(
            str(
                wrapped_variant_stmt.compile(
                    dialect=dialect, compile_kwargs={"literal_binds": True}
                )
            ),
            'SELECT b"\\x5c\\x27 OR 1=1 --" AS anon_1',
        )

    def test_render_literal_value_string_wrapper_and_uuid(self):
        """String TypeDecorators and non-native Uuid still escape string literals."""

        class CustomStringWrapper(sa.TypeDecorator):
            impl = sa.String
            cache_ok = True

            def process_bind_param(self, value, dialect):
                return value

        dialect = SpannerDialect(paramstyle="format")
        for string_like_type in (
            CustomStringWrapper(),
            sa.Uuid(as_uuid=False),
            sa.UUID(as_uuid=False),
        ):
            stmt = sa.select(sa.literal(r"\' OR 1=1 --", string_like_type))
            eq_(
                str(
                    stmt.compile(
                        dialect=dialect, compile_kwargs={"literal_binds": True}
                    )
                ),
                'SELECT r"""\\\' OR 1=1 --""" AS anon_1',
            )

    def test_binary_literal_in_computed_and_default_ddl(self):
        """CREATE TABLE preserves BYTES types and escapes DEFAULT/Computed."""
        dialect = SpannerDialect(paramstyle="format")
        items = sa.Table(
            "items",
            sa.MetaData(),
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("payload", sa.LargeBinary(20)),
            sa.Column("fixed", sa.BINARY(16)),
            sa.Column(
                "default_blob",
                sa.LargeBinary,
                server_default=sa.DefaultClause(sa.literal(rb"\' OR 1=1 --")),
            ),
            sa.Column(
                "fallback",
                sa.LargeBinary,
                sa.Computed(sa.func.coalesce(sa.column("payload"), rb"\' OR 1=1 --")),
            ),
        )
        ddl = str(sa.schema.CreateTable(items).compile(dialect=dialect))
        assert "payload BYTES(20)" in ddl
        assert "fixed BYTES(16)" in ddl
        assert 'default_blob BYTES(MAX) DEFAULT (b"\\x5c\\x27 OR 1=1 --")' in ddl
        assert 'AS (coalesce(payload, b"\\x5c\\x27 OR 1=1 --")) STORED' in ddl

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
