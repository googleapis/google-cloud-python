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
import sqlparse
from google.cloud.spanner_dbapi import parse_utils
from google.cloud.spanner_v1 import param_types
from sqlalchemy.engine.reflection import ObjectKind
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.schema import CreateTable
from sqlalchemy.sql.compiler import OPERATORS
from sqlalchemy.sql.elements import quoted_name
from sqlalchemy.sql.operators import json_getitem_op
from sqlalchemy.testing import eq_
from sqlalchemy.testing.plugin.plugin_base import fixtures

from google.cloud import spanner_dbapi
from google.cloud.sqlalchemy_spanner.sqlalchemy_spanner import (
    SpannerDialect,
    _escape_json_path_key,
)


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

    def test_escape_json_path_key_edge_cases(self):
        """Test _escape_json_path_key across quote and backslash boundaries."""
        cases = [
            ("", ""),
            ("simple", "simple"),
            ("\\", "\\\\"),
            ("\\\\", "\\\\\\\\"),
            ('"', '\\"'),
            ('\\"', '\\\\\\"'),
            ('\\\\"', '\\\\\\\\\\"'),
            ('a\\b"c\\', 'a\\b\\"c\\\\'),
            ('"\\"', '\\"\\\\\\"'),
            ('a\\"b\\"c\\d\\', 'a\\\\\\"b\\\\\\"c\\d\\\\'),
            ("\\\\\\a", "\\\\\\a"),
            ('\\\\\\"\\\\\\a\\\\', '\\\\\\\\\\\\\\"\\\\\\a\\\\\\\\'),
            (123, "123"),
        ]
        for raw_key, expected in cases:
            eq_(_escape_json_path_key(raw_key), expected)

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
            compiler.render_literal_value("has\x7fdel", sa.String()),
            '"has\\u007fdel"',
        )
        eq_(
            compiler.render_literal_value("has\nnewline\tand\ttab", sa.String()),
            'r"""has\nnewline\tand\ttab"""',
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
            # Non-byte-format and multi-dimensional memoryviews must flatten to bytes
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
        semicolon_payload = b'"; DROP TABLE users; --'
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
            sa.Column(
                "semicolon_blob",
                sa.LargeBinary,
                server_default=sa.DefaultClause(sa.literal(semicolon_payload)),
            ),
        )
        ddl = str(sa.schema.CreateTable(items).compile(dialect=dialect))
        assert "payload BYTES(20)" in ddl
        assert "fixed BYTES(16)" in ddl
        assert 'default_blob BYTES(MAX) DEFAULT (b"\\x5c\\x27 OR 1=1 --")' in ddl
        assert 'AS (coalesce(payload, b"\\x5c\\x27 OR 1=1 --")) STORED' in ddl
        assert (
            'semicolon_blob BYTES(MAX) DEFAULT (b"\\x22; DROP TABLE users; --")' in ddl
        )
        # Escaping '"' as \x22 keeps sqlparse from splitting DDL on ';'
        eq_(sqlparse.split(ddl), [ddl.strip()])

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

    def test_identifier_preparer_escapes_backticks_backslashes_and_controls(self):
        """Test GoogleSQL identifier escaping and quoting rules."""
        dialect = SpannerDialect()
        preparer = dialect.identifier_preparer

        eq_(preparer.escape_quote, "\\")

        # Valid unquoted GoogleSQL identifiers remain unquoted
        for identifier in ("users", "_", "_private_1", "col_a1"):
            eq_(preparer.quote(identifier), identifier)

        # Default Spanner collation sentinel remains unquoted only in format_collation,
        # while identifiers literally named '"unicode"' are properly backtick-quoted.
        eq_(preparer.format_collation('"unicode"'), '"unicode"')
        eq_(preparer.format_collation('"UNICODE"'), '"UNICODE"')
        eq_(preparer.format_collation("my_collation"), "my_collation")
        eq_(preparer.format_collation("MyCollation"), "`MyCollation`")
        eq_(
            preparer.format_collation("col`; DROP TABLE x"),
            "`col\\u0060; DROP TABLE x`",
        )
        eq_(
            preparer.format_collation(
                "my_collation", collation_schema="sch`; DROP TABLE x"
            ),
            "`sch\\u0060; DROP TABLE x`.my_collation",
        )
        eq_(
            preparer.format_collation('"unicode"', collation_schema="sch"),
            'sch."unicode"',
        )
        eq_(
            str(
                sa.collate(sa.literal_column("c"), '"unicode"').compile(dialect=dialect)
            ),
            'c COLLATE "unicode"',
        )
        eq_(
            str(
                sa.collate(sa.literal_column("c"), "my_collation").compile(
                    dialect=dialect
                )
            ),
            "c COLLATE my_collation",
        )
        eq_(preparer.quote('"unicode"'), '`"unicode"`')
        eq_(preparer.quote('"UNICODE"'), '`"UNICODE"`')

        # Reserved words (both ANSI and Spanner-specific) must be quoted
        for keyword in ("select", "SELECT", "from", "struct", "unnest"):
            eq_(preparer.quote(keyword), f"`{keyword}`")

        # Comprehensive permutations: whitespace, non-ASCII/UTF-8, symbols, '$',
        # leading digits, newlines, quotes, backslashes, backticks, empty string.
        cases = [
            (" ", "` `"),
            ("~", "`~`"),
            ("\x80", "`\x80`"),
            ("Café", "`Café`"),
            ("café", "`café`"),
            ("🎵", "`🎵`"),
            ("Café`\\🎵", "`Café\\u0060\\\\🎵`"),
            ("semi;colon", "`semi;colon`"),
            ("`", "`\\u0060`"),
            ("\\", "`\\\\`"),
            ("\\\\", "`\\\\\\\\`"),
            ("\\`", "`\\\\\\u0060`"),
            ("\\\\`", "`\\\\\\\\\\u0060`"),
            ("\\\\\\`", "`\\\\\\\\\\\\\\u0060`"),
            ("\\\\`\\\\`", "`\\\\\\\\\\u0060\\\\\\\\\\u0060`"),
            ("foo\n", "`foo\\n`"),
            ("\nfoo", "`\\nfoo`"),
            ("foo\nbar", "`foo\\nbar`"),
            ("select\n", "`select\\n`"),
            ("Line1\nLine2\r\nLine3", "`Line1\\nLine2\\r\\nLine3`"),
            ("Col\a\b\f\t\vName", "`Col\\u0007\\u0008\\u000c\\t\\u000bName`"),
            ("Null\0Char", "`Null\\u0000Char`"),
            ("Del\x7fChar", "`Del\\u007fChar`"),
            ("$foo", "`$foo`"),
            ("foo$", "`foo$`"),
            ("foo$bar", "`foo$bar`"),
            ("1column", "`1column`"),
            ("MixedCase", "`MixedCase`"),
            ('a"b', '`a"b`'),
            ("a'b", "`a'b`"),
            ("TrailingBackslash\\", "`TrailingBackslash\\\\`"),
            ("foo\\` SELECT 1 --", "`foo\\\\\\u0060 SELECT 1 --`"),
            ("a\\u0060b", "`a\\\\u0060b`"),
            ("col`; DROP TABLE users; --", "`col\\u0060; DROP TABLE users; --`"),
            ("", "``"),
            (sa.sql.quoted_name("users", quote=True), "`users`"),
            (
                sa.sql.quoted_name("forced`\\name\n", quote=True),
                "`forced\\u0060\\\\name\\n`",
            ),
            (
                sa.sql.elements._truncated_label("long`\\label\n"),
                "`long\\u0060\\\\label\\n`",
            ),
        ]
        for raw_identifier, expected_quoted in cases:
            eq_(preparer.quote(raw_identifier), expected_quoted)
            # Repeat call exercises self._strings cache consistently
            eq_(preparer.quote(raw_identifier), expected_quoted)
            if not isinstance(raw_identifier, sa.sql.quoted_name):
                eq_(preparer.unformat_identifiers(expected_quoted), [raw_identifier])

        # Explicit quote=False opt-out on quoted_name is respected by SQLAlchemy
        unquoted_name = sa.sql.quoted_name("unquoted_raw", quote=False)
        eq_(preparer.quote(unquoted_name), "unquoted_raw")

        # Function names use _requires_quotes_illegal_chars
        for function_name, expected_function_sql in (
            ("MyCustomFn", "MyCustomFn()"),
            ("fn\n", "`fn\\n`()"),
            ("fn$name", "`fn$name`()"),
            ("1fn", "`1fn`()"),
            ("café", "`café`()"),
            ("fn`inject", "`fn\\u0060inject`()"),
            ('"unicode"', '`"unicode"`()'),
        ):
            eq_(
                str(getattr(sa.func, function_name)().compile(dialect=dialect)),
                expected_function_sql,
            )
        eq_(
            str(sa.func.my_pkg.my_fn().compile(dialect=dialect)),
            "my_pkg.my_fn()",
        )

    def test_identifier_preparer_all_ascii_control_characters(self):
        """Test every ASCII control character (0x00..0x1F and 0x7F) is escaped."""
        dialect = SpannerDialect()
        preparer = dialect.identifier_preparer

        named_escapes = {0x0A: "\\n", 0x0D: "\\r", 0x09: "\\t"}
        for codepoint in (*range(0x00, 0x20), 0x7F):
            identifier = f"col{chr(codepoint)}name"
            escaped = preparer._escape_identifier(identifier)
            # No raw ASCII control character may remain in the escaped identifier
            assert all(0x20 <= ord(character) != 0x7F for character in escaped)
            expected_escape = named_escapes.get(codepoint, f"\\u{codepoint:04x}")
            eq_(escaped, f"col{expected_escape}name")
            eq_(preparer.quote(identifier), f"`{escaped}`")
            eq_(preparer._unescape_identifier(escaped), identifier)

    def test_identifier_preparer_double_percents_depends_on_paramstyle(self):
        """Test percent doubling matches dialect paramstyle."""
        format_dialect = SpannerDialect(dbapi=spanner_dbapi)
        named_dialect = SpannerDialect(paramstyle="named")

        eq_(format_dialect.identifier_preparer.quote("rate_%s"), "`rate_%%s`")
        eq_(
            format_dialect.identifier_preparer.quote(
                sa.sql.quoted_name("a%s", quote=True)
            ),
            "`a%%s`",
        )
        eq_(named_dialect.identifier_preparer.quote("rate_%s"), "`rate_%s`")

    def test_identifier_injection_prevented_in_dql_dml_and_ddl(self):
        """Test malicious identifiers cannot inject SQL, DDL, or confuse sqlparse."""
        dialect = SpannerDialect(dbapi=spanner_dbapi)
        malicious_schema = "sch`; DROP TABLE users; --"
        malicious_table = "t`; DROP TABLE users; --"
        malicious_column = "c\\`; DROP TABLE users; /*"
        malicious_comment_column = "c2` /* comment */ --"
        malicious_index = "idx`; DROP TABLE users; DROP TABLE x"
        malicious_foreign_key = "fk`; DROP TABLE users; --"
        malicious_parent = "parent`; DROP TABLE users; --"
        malicious_sequence = "seq`; DROP TABLE users; --"

        metadata = sa.MetaData(schema=malicious_schema)
        parent = sa.Table(
            malicious_parent,
            metadata,
            sa.Column("id", sa.Integer, primary_key=True),
        )
        table = sa.Table(
            malicious_table,
            metadata,
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column(malicious_column, sa.String(64)),
            sa.Column(malicious_comment_column, sa.String(64)),
            sa.ForeignKeyConstraint(["id"], [parent.c.id], name=malicious_foreign_key),
            sa.Index(
                malicious_index,
                "id",
                spanner_storing=[malicious_column],
                spanner_interleave_in=malicious_parent,
            ),
        )
        sequence = sa.Sequence(malicious_sequence, schema=malicious_schema)

        # DQL (including schema-aliased tables, labels, and aliases) & DML
        label_name = "lbl`/* comment */ --"
        alias_name = "al`; DROP TABLE users"
        aliased_table = table.alias(alias_name)
        select_statement = sa.select(
            aliased_table.c[malicious_column].label(label_name)
        )
        select_sql = str(select_statement.compile(dialect=dialect))
        assert (
            "`sch\\u0060; DROP TABLE users; --`.`t\\u0060; DROP TABLE users; --`"
            in select_sql
        )
        assert "AS `al\\u0060; DROP TABLE users`" in select_sql
        assert "AS `lbl\\u0060/* comment */ --`" in select_sql
        classified_select = spanner_dbapi.parse_utils.classify_statement(select_sql)
        eq_(
            classified_select.statement_type,
            spanner_dbapi.parsed_statement.StatementType.QUERY,
        )
        assert "`lbl\\u0060/* comment */ --`" in classified_select.statement.sql

        insert_sql = str(
            table.insert()
            .values({"id": 1, malicious_column: "v"})
            .returning(table.c[malicious_column])
            .compile(dialect=dialect)
        )
        assert "`t\\u0060; DROP TABLE users; --`" in insert_sql
        assert "THEN RETURN `c\\\\\\u0060; DROP TABLE users; /*`" in insert_sql
        eq_(
            spanner_dbapi.parse_utils.classify_statement(insert_sql).statement_type,
            spanner_dbapi.parsed_statement.StatementType.INSERT,
        )

        update_sql = str(
            table.update().values({malicious_column: "v"}).compile(dialect=dialect)
        )
        assert "WHERE 1=1" in update_sql
        eq_(
            spanner_dbapi.parse_utils.classify_statement(update_sql).statement_type,
            spanner_dbapi.parsed_statement.StatementType.UPDATE,
        )

        delete_sql = str(
            sa.delete(table)
            .returning(table.c[malicious_column])
            .compile(dialect=dialect)
        )
        assert (
            "DELETE FROM `sch\\u0060; DROP TABLE users; --`."
            "`t\\u0060; DROP TABLE users; --`" in delete_sql
        )
        assert (
            "THEN RETURN `t\\u0060;_DROP_TABLE_users;_--_1`."
            "`c\\\\\\u0060; DROP TABLE users; /*`" in delete_sql
        )

        # DDL with semicolons/comments inside escaped identifiers stays unsplit
        create_table_sql = str(sa.schema.CreateTable(table).compile(dialect=dialect))
        assert "`fk\\u0060; DROP TABLE users; --`" in create_table_sql
        eq_(sqlparse.split(create_table_sql), [create_table_sql.strip()])

        create_index_sql = str(
            sa.schema.CreateIndex(next(iter(table.indexes))).compile(dialect=dialect)
        )
        eq_(
            create_index_sql,
            "CREATE INDEX `sch\\u0060; DROP TABLE users; --`."
            "`idx\\u0060; DROP TABLE users; DROP TABLE x` "
            "ON `sch\\u0060; DROP TABLE users; --`.`t\\u0060; DROP TABLE users; --` "
            "(id) STORING (`c\\\\\\u0060; DROP TABLE users; /*`), "
            "INTERLEAVE IN `parent\\u0060; DROP TABLE users; --`",
        )
        eq_(sqlparse.split(create_index_sql), [create_index_sql])

        drop_table_sql = str(sa.schema.DropTable(table).compile(dialect=dialect))
        eq_(
            sqlparse.split(drop_table_sql),
            [
                "DROP INDEX `idx\\u0060; DROP TABLE users; DROP TABLE x`;",
                "ALTER TABLE `sch\\u0060; DROP TABLE users; --`."
                "`t\\u0060; DROP TABLE users; --` "
                "DROP CONSTRAINT `fk\\u0060; DROP TABLE users; --`;",
                "DROP TABLE `sch\\u0060; DROP TABLE users; --`."
                "`t\\u0060; DROP TABLE users; --`",
            ],
        )

        for sequence_sql in (
            str(sa.schema.CreateSequence(sequence).compile(dialect=dialect)),
            str(sa.schema.DropSequence(sequence).compile(dialect=dialect)),
            str(sa.select(sequence.next_value()).compile(dialect=dialect)),
        ):
            assert (
                "`sch\\u0060; DROP TABLE users; --`."
                "`seq\\u0060; DROP TABLE users; --`" in sequence_sql
            )
            eq_(sqlparse.split(sequence_sql), [sequence_sql])

    def test_identifier_preparer_unescape_and_unformat_identifiers(self):
        """Test single-pass unescaping, multipart unformatting, and unhappy paths."""
        dialect = SpannerDialect(dbapi=spanner_dbapi)
        preparer = dialect.identifier_preparer

        # Single-pass unescaping covers all GoogleSQL escape sequences and does not
        # corrupt escaped backslashes followed by escape letters (e.g. \\n).
        eq_(preparer._unescape_identifier("a\\\\nb"), "a\\nb")
        eq_(
            preparer._unescape_identifier("a\\a\\b\\f\\n\\r\\t\\vb"), "a\a\b\f\n\r\t\vb"
        )
        eq_(preparer._unescape_identifier("\\?\\\"\\'\\`\\\\"), "?\"'`\\")
        eq_(preparer._unescape_identifier("a\\u0060b\\`c"), "a`b`c")
        eq_(preparer._unescape_identifier("\\000\\101\\377"), "\x00A\xff")
        eq_(preparer._unescape_identifier("\\x41\\X42\\U0001f600"), "AB\U0001f600")
        eq_(
            preparer._unescape_identifier("\\ud7ff\\ue000\\U0010ffff"),
            "\ud7ff\ue000\U0010ffff",
        )
        eq_(preparer._unescape_identifier("a%%b"), "a%%b")
        eq_(preparer._unescape_identifier("plain_identifier"), "plain_identifier")

        # Empty, unquoted, mixed, and multipart unformat_identifiers cases
        eq_(preparer.unformat_identifiers(""), [])
        eq_(preparer.unformat_identifiers("``"), [""])
        eq_(preparer.unformat_identifiers("``.``"), ["", ""])
        eq_(
            preparer.unformat_identifiers("schema.table.column"),
            ["schema", "table", "column"],
        )
        eq_(
            preparer.unformat_identifiers("schema.`tab.le`.col"),
            ["schema", "tab.le", "col"],
        )
        eq_(
            preparer.unformat_identifiers("`a\\u0060b`.col.`c\\\\d`"),
            ["a`b", "col", "c\\d"],
        )
        parts = ["sch`ma\\", "tab.le\\", "col\n`name"]
        formatted = ".".join(preparer.quote(part) for part in parts)
        eq_(preparer.unformat_identifiers(formatted), parts)

        # quote_schema escapes malicious schema names as single identifiers
        eq_(
            preparer.quote_schema("sch`; DROP TABLE x"),
            "`sch\\u0060; DROP TABLE x`",
        )

        # External GoogleSQL backslash-escaped identifiers unformat cleanly too
        eq_(
            preparer.unformat_identifiers("`a\\\\`.`\\``.`.`"),
            ["a\\", "`", "."],
        )

        # Invalid/truncated escape sequences fail explicitly
        with pytest.raises(ValueError, match="Unterminated escape sequence"):
            preparer._unescape_identifier("abc\\")
        for invalid_escape in ("\\z", "\\800"):
            with pytest.raises(ValueError, match="Invalid escape sequence"):
                preparer._unescape_identifier(invalid_escape)
        for invalid_octal in ("\\0", "\\77", "\\01a", "\\400", "\\777"):
            with pytest.raises(ValueError, match="Invalid octal escape sequence"):
                preparer._unescape_identifier(invalid_octal)
        for invalid_hex, escape_letter in (
            ("\\x4", "x"),
            ("\\x4z", "x"),
            ("\\X4", "X"),
            ("\\X4z", "X"),
        ):
            with pytest.raises(
                ValueError, match=f"Invalid \\\\{escape_letter} escape sequence"
            ):
                preparer._unescape_identifier(invalid_hex)
        for invalid_short_unicode, escape_letter in (
            ("\\u12", "u"),
            ("\\u12zz", "u"),
            ("\\U1234", "U"),
            ("\\U1234567z", "U"),
        ):
            with pytest.raises(
                ValueError, match=f"Invalid \\\\{escape_letter} escape sequence"
            ):
                preparer._unescape_identifier(invalid_short_unicode)
        for invalid_unicode in ("\\ud800", "\\udfff", "\\U0000d800", "\\U00110000"):
            with pytest.raises(ValueError, match="Invalid Unicode codepoint"):
                preparer._unescape_identifier(invalid_unicode)

        # Malformed qualified identifier strings fail explicitly
        malformed_cases = [
            ("`abc\\", "Unterminated escape sequence"),
            ("`unclosed", "Unterminated quoted identifier"),
            ("`bad\\`", "Unterminated quoted identifier"),
            ("`a`.`b` EXTRA", "Unexpected character after quoted identifier"),
            ("`a.b`c.d", "Unexpected character after quoted identifier"),
            ("a.", "Trailing dot in qualified identifier"),
            ("`a`.", "Trailing dot in qualified identifier"),
            (".", "Invalid unquoted identifier segment"),
            ("a..b", "Invalid unquoted identifier segment"),
            (".a", "Invalid unquoted identifier segment"),
            ("1bad.col", "Invalid unquoted identifier segment"),
            (" a ", "Invalid unquoted identifier segment"),
            ("a`b", "Invalid unquoted identifier segment"),
            ("café", "Invalid unquoted identifier segment"),
            ("`a`.`b", "Unterminated quoted identifier"),
        ]
        for malformed, expected_message in malformed_cases:
            with pytest.raises(ValueError, match=expected_message):
                preparer.unformat_identifiers(malformed)

        # Non-string inputs fail with TypeError across preparer entrypoints
        for invalid_value in (None, 123, b"bytes"):
            for preparer_method in (
                preparer.quote,
                preparer.quote_identifier,
                preparer.format_collation,
                preparer._escape_identifier,
                preparer._unescape_identifier,
                preparer.unformat_identifiers,
                preparer._requires_quotes,
                preparer._requires_quotes_illegal_chars,
            ):
                with pytest.raises(TypeError, match="Identifier must be a string"):
                    preparer_method(invalid_value)

    def _create_mock_connection(self, rows=None):
        connection = MagicMock()
        mock_snapshot = MagicMock()
        mock_snapshot.execute_sql.return_value = rows if rows is not None else []
        connection.connection.database.snapshot.return_value.__enter__.return_value = (
            mock_snapshot
        )
        return connection, mock_snapshot

    @pytest.mark.parametrize(
        ("method_name", "name_param", "rows", "expected_result"),
        [
            ("get_view_names", None, [], []),
            ("get_sequence_names", None, [], []),
            ("get_table_names", None, [], []),
            ("get_view_definition", "view_name", [("SELECT 1",)], "SELECT 1"),
            ("get_unique_constraints", "table_name", [], []),
            ("has_table", "table_name", [], False),
            ("has_sequence", "sequence_name", [], False),
        ],
    )
    def test_reflection_binds_parameters(
        self, method_name, name_param, rows, expected_result
    ):
        """Reflection methods bind schema and object names as STRING parameters."""
        dialect = SpannerDialect()
        malicious_schema = "' OR '1'='1\" UNION ALL SELECT secret FROM users --"
        malicious_name = "tbl' OR '1'='1\" UNION ALL SELECT secret FROM users --"

        connection, mock_snapshot = self._create_mock_connection(rows=rows)
        args = (malicious_name,) if name_param else ()
        result = getattr(dialect, method_name)(
            connection, *args, schema=malicious_schema
        )
        eq_(result, expected_result)

        call_args = mock_snapshot.execute_sql.call_args
        executed_sql = call_args.args[0]
        assert malicious_schema not in executed_sql
        assert "@table_schema" in executed_sql

        expected_params = {"table_schema": malicious_schema}
        expected_types = {"table_schema": param_types.STRING}
        if name_param:
            assert malicious_name not in executed_sql
            assert f"@{name_param}" in executed_sql
            expected_params[name_param] = malicious_name
            expected_types[name_param] = param_types.STRING

        eq_(call_args.kwargs["params"], expected_params)
        eq_(call_args.kwargs["param_types"], expected_types)

        # Default schema=None must normalize to "" for Spanner INFORMATION_SCHEMA.
        default_connection, default_snapshot = self._create_mock_connection(rows=rows)
        getattr(dialect, method_name)(default_connection, *args)
        eq_(
            default_snapshot.execute_sql.call_args.kwargs["params"]["table_schema"],
            "",
        )

    def test_get_view_definition_missing_raises(self):
        """get_view_definition raises NoSuchTableError when the view is absent."""
        dialect = SpannerDialect()
        connection, _ = self._create_mock_connection(rows=[])
        with pytest.raises(NoSuchTableError, match=r"\.missing_view"):
            dialect.get_view_definition(connection, "missing_view")

    @pytest.mark.parametrize(
        "method_name",
        [
            "get_multi_columns",
            "get_multi_indexes",
            "get_multi_pk_constraint",
            "get_multi_foreign_keys",
        ],
    )
    def test_get_multi_binds_filter_names_with_unnest(self, method_name):
        """get_multi_* methods parameterize filter_names via IN UNNEST(@table_names)."""
        dialect = SpannerDialect()
        malicious_schema = "s' OR '1'='1"
        malicious_table = "t' OR '1'='1 --"
        connection, mock_snapshot = self._create_mock_connection()

        eq_(
            getattr(dialect, method_name)(
                connection,
                schema=malicious_schema,
                filter_names=[malicious_table, "other_table"],
            ),
            {},
        )
        call_args = mock_snapshot.execute_sql.call_args
        executed_sql = call_args.args[0]
        assert malicious_schema not in executed_sql
        assert malicious_table not in executed_sql
        assert "IN UNNEST(@table_names)" in executed_sql
        eq_(
            call_args.kwargs["params"],
            {
                "table_schema": malicious_schema,
                "table_names": [malicious_table, "other_table"],
            },
        )
        eq_(
            call_args.kwargs["param_types"],
            {
                "table_schema": param_types.STRING,
                "table_names": param_types.Array(param_types.STRING),
            },
        )

    @pytest.mark.parametrize(
        "method_name",
        [
            "get_multi_columns",
            "get_multi_indexes",
            "get_multi_pk_constraint",
            "get_multi_foreign_keys",
        ],
    )
    def test_get_multi_omits_unnest_when_filter_names_is_none(self, method_name):
        """filter_names=None reflects all tables without an UNNEST predicate."""
        dialect = SpannerDialect()
        connection, mock_snapshot = self._create_mock_connection()

        eq_(
            getattr(dialect, method_name)(connection, schema="s", filter_names=None), {}
        )
        call_args = mock_snapshot.execute_sql.call_args
        assert "UNNEST(@table_names)" not in call_args.args[0]
        eq_(call_args.kwargs["params"], {"table_schema": "s"})
        eq_(call_args.kwargs["param_types"], {"table_schema": param_types.STRING})

    @pytest.mark.parametrize(
        "method_name",
        [
            "get_multi_columns",
            "get_multi_indexes",
            "get_multi_pk_constraint",
            "get_multi_foreign_keys",
        ],
    )
    def test_get_multi_short_circuits_on_empty_filter_names(self, method_name):
        """Empty filter_names=[] returns {} without executing SQL after kind check."""
        dialect = SpannerDialect()
        connection, mock_snapshot = self._create_mock_connection()

        eq_(getattr(dialect, method_name)(connection, filter_names=[]), {})
        mock_snapshot.execute_sql.assert_not_called()

        with pytest.raises(
            NotImplementedError,
            match="Spanner does not support MATERIALIZED VIEWS",
        ):
            getattr(dialect, method_name)(
                connection, filter_names=[], kind=ObjectKind.MATERIALIZED_VIEW
            )

    @pytest.mark.parametrize(
        "method_name",
        [
            "get_multi_columns",
            "get_multi_indexes",
            "get_multi_pk_constraint",
            "get_multi_foreign_keys",
        ],
    )
    def test_get_multi_normalizes_set_and_quoted_name_inputs(self, method_name):
        """Non-list iterables and SQLAlchemy quoted_name normalize to list[str]."""
        dialect = SpannerDialect()
        connection, mock_snapshot = self._create_mock_connection()

        getattr(dialect, method_name)(
            connection,
            schema=quoted_name("my_schema", True),
            filter_names={quoted_name("users", True)},
        )
        params = mock_snapshot.execute_sql.call_args.kwargs["params"]
        eq_(params["table_schema"], "my_schema")
        assert type(params["table_schema"]) is str
        eq_(params["table_names"], ["users"])
        assert type(params["table_names"][0]) is str

    @pytest.mark.parametrize(
        "method_name",
        [
            "get_columns",
            "get_indexes",
            "get_pk_constraint",
            "get_foreign_keys",
        ],
    )
    def test_single_table_reflection_binds_parameters(self, method_name):
        """Single-table methods delegate to get_multi_* with bound parameters."""
        dialect = SpannerDialect()
        malicious_schema = "s' OR '1'='1"
        malicious_table = "t' OR '1'='1 --"
        connection, mock_snapshot = self._create_mock_connection()

        eq_(
            getattr(dialect, method_name)(
                connection, malicious_table, schema=malicious_schema
            ),
            [],
        )
        call_args = mock_snapshot.execute_sql.call_args
        assert malicious_schema not in call_args.args[0]
        assert malicious_table not in call_args.args[0]
        eq_(
            call_args.kwargs["params"],
            {"table_schema": malicious_schema, "table_names": [malicious_table]},
        )
