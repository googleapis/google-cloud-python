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

"""Unit tests for scripts/check_compiler_safety.py."""

import importlib.util
import sys
import textwrap
from pathlib import Path

import pytest

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = PACKAGE_ROOT / "scripts" / "check_compiler_safety.py"


def _load_checker_module():
    spec = importlib.util.spec_from_file_location("check_compiler_safety", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = _load_checker_module()


def _check(code: str):
    return checker.check_source(textwrap.dedent(code), filename="test_file.py")


class TestUnsafeInterpolations:
    @pytest.mark.parametrize(
        "body",
        [
            'return f"{left}.{binary.right.value}"',
            'return f"{left}.{binary.right.effective_value}"',
            'return f"{left:{binary.right.value}}"',
            'return "%s.%s" % (left, binary.right.value)',
            'return "%s" % binary.right.value',
            'return "%(k)s" % {"k": binary.right.value}',
            'return "{}.{}".format(left, binary.right.value)',
            'return "{l}.{r}".format(l=left, r=binary.right.value)',
            'return "{r}".format_map({"r": binary.right.value})',
            'return Template("$a.$b").substitute(a=left, b=binary.right.value)',
            'return left + "." + binary.right.value',
            'return left + "." + str(binary.right.value)',
            'return left + "." + repr(binary.right.value)',
            'return ".".join([left, binary.right.value])',
            'return ".".join(k for k in binary.right.value)',
            'return ", ".join(f"`{k}`" for k in binary.right.value)',
            "return binary.right.value",
            "return str(binary.right.value)",
            'return self.process(sqlalchemy.text(f"SELECT {binary.right.value}"))',
            'return f"{left}.{urllib.parse.quote(binary.right.value)}"',
        ],
    )
    def test_direct_unsafe_patterns_caught(self, body):
        code = f"""
        class MyCompiler(SQLCompiler):
            def visit_json_getitem_op_binary(self, binary, operator_, **kw):
                left = self.process(binary.left, **kw)
                {body}
        """
        errors = _check(code)
        assert len(errors) == 1
        assert errors[0].function == "visit_json_getitem_op_binary"
        assert "self.process(...)" in errors[0].message

    @pytest.mark.parametrize(
        "body",
        [
            """
            field = binary.right.value
            return f"{left}.{field}"
            """,
            """
            field = getattr(binary.right, "value", None)
            return f"{left}.{field}"
            """,
            """
            field = getattr(binary.right, "effective_value", None)
            return f"{left}.{field}"
            """,
            """
            field: str = binary.right.value
            return f"{left}.{field}"
            """,
            """
            field = binary.right.value.replace("`", "")
            return f"{left}.`{field}`"
            """,
            """
            if (field := binary.right.value):
                return f"{left}.{field}"
            """,
            """
            _, field = left, binary.right.value
            return f"{left}.{field}"
            """,
            """
            field = binary.right.value[0]
            return f"{left}.{field}"
            """,
            """
            sql = left + "."
            sql += binary.right.value
            return sql
            """,
            """
            sql = binary.right.value
            sql += "_suffix"
            return sql
            """,
            """
            parts = [left]
            parts.append(binary.right.value)
            return ".".join(parts)
            """,
            """
            parts = [left]
            parts += [binary.right.value]
            return ".".join(parts)
            """,
            """
            params = {}
            params["v"] = binary.right.value
            return "%(v)s" % params
            """,
            """
            idx = binary.right.value + 1
            return f"{left}[{idx}]"
            """,
            """
            field = binary.right.value
            def _inner():
                return f"{left}.{field}"
            return _inner()
            """,
            """
            field = binary.right.value
            fn = lambda: f"{left}.{field}"
            return fn()
            """,
        ],
    )
    def test_aliased_and_tainted_patterns_caught(self, body):
        indented = textwrap.indent(textwrap.dedent(body).strip(), "        ")
        code = (
            "class MyCompiler(SQLCompiler):\n"
            "    def visit_op(self, binary, **kw):\n"
            "        left = self.process(binary.left, **kw)\n"
            f"{indented}\n"
        )
        errors = _check(code)
        assert len(errors) == 1

    def test_control_flow_taint_propagation(self):
        # Taint from one branch of if/else
        errors = _check(
            """
            class MyCompiler(SQLCompiler):
                def visit_op(self, binary, cond, **kw):
                    if cond:
                        val = binary.right.value
                    else:
                        val = "safe"
                    return f"SELECT {val}"
            """
        )
        assert len(errors) == 1

        # Sanitized in only one branch -> still tainted after if
        errors = _check(
            """
            class MyCompiler(SQLCompiler):
                def visit_op(self, binary, cond, **kw):
                    val = binary.right.value
                    if cond:
                        val = self.preparer.quote_identifier(val)
                    return f"SELECT {val}"
            """
        )
        assert len(errors) == 1

        # Loop over tainted iterable
        errors = _check(
            """
            class MyCompiler(SQLCompiler):
                def visit_op(self, binary, **kw):
                    out = []
                    for item in binary.right.value:
                        out.append(item)
                    return ", ".join(out)
            """
        )
        assert len(errors) == 1

        # Loop-carried taint across iterations
        errors = _check(
            """
            class MyCompiler(SQLCompiler):
                def visit_op(self, items, **kw):
                    val = "initial"
                    sql = ""
                    for item in items:
                        sql = f"SELECT {val}"
                        val = item.value
                    return sql
            """
        )
        assert len(errors) == 1

        # Break carrying taint out of loop
        errors = _check(
            """
            class MyCompiler(SQLCompiler):
                def visit_op(self, items, cond, **kw):
                    val = "safe"
                    for item in items:
                        if cond:
                            val = item.value
                            break
                    return f"SELECT {val}"
            """
        )
        assert len(errors) == 1

        # Try block taint visible in except and finally even when try returns
        errors = _check(
            """
            class MyCompiler(SQLCompiler):
                def visit_op(self, binary, **kw):
                    try:
                        val = binary.right.value
                        return self.preparer.quote_identifier(val)
                    except ValueError:
                        return f"SELECT {val}"
            """
        )
        assert len(errors) == 1

        # While loop taint
        errors = _check(
            """
            class MyCompiler(SQLCompiler):
                def visit_op(self, binary, cond, **kw):
                    val = "safe"
                    while cond:
                        sql = f"SELECT {val}"
                        val = binary.right.value
                    return sql
            """
        )
        assert len(errors) == 1

        # Match/case binding from tainted subject
        errors = _check(
            """
            class MyCompiler(SQLCompiler):
                def visit_op(self, binary, **kw):
                    match binary.right.value:
                        case str(s):
                            return f"SELECT {s}"
                        case _:
                            return "SELECT NULL"
            """
        )
        assert len(errors) == 1

        # With statement binding tainted expression
        errors = _check(
            """
            class MyCompiler(SQLCompiler):
                def visit_op(self, binary, **kw):
                    with ctx(binary.right.value) as v:
                        return f"SELECT {v}"
            """
        )
        assert len(errors) == 1

        # Try / else / finally taint propagation
        errors = _check(
            """
            class MyCompiler(SQLCompiler):
                def visit_try_else_finally(self, binary, **kw):
                    try:
                        val = binary.right.value
                    except KeyError:
                        val = "fallback"
                    else:
                        extra = val
                    finally:
                        sql = f"SELECT {val}"
                    return f"{sql}, {extra}"
            """
        )
        assert len(errors) == 2

        # Try where both try and except return, but finally still uses tainted var
        errors = _check(
            """
            class MyCompiler(SQLCompiler):
                def visit_try_all_return(self, binary, **kw):
                    try:
                        return self.process(binary.left)
                    except KeyError:
                        val = binary.right.value
                        return "NULL"
                    finally:
                        _ = f"SELECT {val}"
            """
        )
        assert len(errors) == 1

        # For / else taint propagation
        errors = _check(
            """
            class MyCompiler(SQLCompiler):
                def visit_for_else(self, items, **kw):
                    val = "safe"
                    for item in items:
                        val = item.value
                    else:
                        return f"SELECT {val}"
            """
        )
        assert len(errors) == 1

        # DictComp over tainted items
        errors = _check(
            """
            class MyCompiler(SQLCompiler):
                def visit_dictcomp(self, binary, **kw):
                    mapping = {k: v for k, v in binary.right.value.items()}
                    return "%(a)s" % mapping
            """
        )
        assert len(errors) == 1

        # Match with sequence, star, mapping, guard, and clean subject
        errors = _check(
            """
            class MyCompiler(SQLCompiler):
                def visit_match_patterns(self, binary, **kw):
                    match binary.right.value:
                        case [first, *rest] if first:
                            return f"SELECT {first}"
                        case {"k": v, **others}:
                            return f"SELECT {v}"
                        case "a" | "b":
                            return "SELECT 1"
                    return "SELECT 0"
            """
        )
        assert len(errors) == 2


class TestCompilerScopes:
    def test_compiles_decorator_bare_and_qualified(self):
        errors = _check(
            """
            @compiles(MyElement, "bigquery")
            def compile_my_element(element, compiler, **kw):
                return f"FUNC({element.arg.value})"

            @sqlalchemy.ext.compiler.compiles(OtherElement, "bigquery")
            def compile_other(element, compiler, **kw):
                return element.arg.value
            """
        )
        assert len(errors) == 2
        assert errors[0].function == "compile_my_element"
        assert "compiler.process(...)" in errors[0].message
        assert errors[1].function == "compile_other"
        assert "return" in errors[1].message

    def test_non_visit_compiler_methods_and_ddl_compiler(self):
        errors = _check(
            """
            class BigQueryDDLCompiler(DDLCompiler):
                def post_create_table(self, table):
                    return f"OPTIONS(x={table.opt.value})"

                def _helper(self, elem):
                    return f"{elem.value}"

            class CustomCompilerMixin:
                async def visit_async(self, elem, **kw):
                    return f"{elem.value}"
            """
        )
        assert len(errors) == 3
        assert {e.function for e in errors} == {
            "post_create_table",
            "_helper",
            "visit_async",
        }

    def test_module_qualified_compiler_base(self):
        errors = _check(
            """
            class PGCustom(compiler.SQLCompiler):
                def update_from_clause(self, stmt, **kw):
                    return f"FROM {stmt.table.value}"
            """
        )
        assert len(errors) == 1

    def test_non_compiler_classes_and_functions_ignored(self):
        errors = _check(
            """
            class RegularHelper(BaseThing):
                def visit_something(self, obj):
                    return f"{obj.value}"

            class CompilerSafetyVisitor(ast.NodeVisitor):
                def visit_Attribute(self, node):
                    return f"{node.value}"

            def regular_function(obj):
                return f"{obj.value}"

            class MyCompiler(SQLCompiler):
                class NestedData:
                    def format_info(self, obj):
                        return f"{obj.value}"
            """
        )
        assert errors == []


class TestSafePatternsNoFalsePositives:
    def test_sanitizers_and_quoting(self):
        errors = _check(
            """
            class BigQueryCompiler(SQLCompiler):
                def visit_json_getitem_op_binary(self, binary, operator_, **kw):
                    field_name = getattr(binary.right, "value", None)
                    if not isinstance(field_name, str):
                        raise CompileError(f"Invalid field: {field_name!r}")
                    left = self.process(binary.left, **kw)
                    return f"{left}.{self.preparer.quote_identifier(field_name)}"

                def visit_direct_quote(self, binary, **kw):
                    left = self.process(binary.left, **kw)
                    return f"{left}.{self.preparer.quote_identifier(binary.right.value)}"

                def visit_prefixed_quote(self, binary, **kw):
                    val = binary.right.value
                    return self.preparer.quote_identifier(f"prefix_{val}")

                def visit_preparer_alias(self, binary, **kw):
                    preparer = self.preparer
                    val = binary.right.value
                    return f"SELECT {preparer.quote(val)}"

                def visit_reassigned_clean(self, binary, **kw):
                    val = binary.right.value
                    val = self.preparer.quote_identifier(val)
                    return f"SELECT {val}"

                def visit_both_branches_sanitized(self, binary, cond, **kw):
                    val = binary.right.value
                    if cond:
                        val = self.preparer.quote_identifier(val)
                    else:
                        val = self.process(binary.right, **kw)
                    return f"SELECT {val}"

                def visit_literal_and_alembic(self, binary, **kw):
                    v = binary.right.value
                    a = self.sql_compiler.render_literal_value(v, String())
                    b = process_string_literal(v)
                    c = format_column_name(self, v)
                    return f"{a}, {b}, {c}"

                def visit_comprehension_sanitized(self, binary, **kw):
                    parts = [
                        self.preparer.quote_identifier(k)
                        for k in binary.right.value
                    ]
                    return ", ".join(parts)

                def visit_ternary_condition_tainted_branches_safe(self, binary, **kw):
                    val = binary.right.value
                    return f"{self.preparer.quote_identifier(val) if val else 'NULL'}"

                def visit_allowlist_subscript(self, binary, **kw):
                    val = binary.right.value
                    allowed = {"a": "ASC", "d": "DESC"}
                    return f"ORDER BY col {allowed[val]}"

                def visit_tuple_unpack_clean_slot(self, binary, **kw):
                    left_val, _raw = self.process(binary.left), binary.right.value
                    return f"SELECT {left_val}"

                def visit_shadowed_nested_param(self, binary, **kw):
                    val = binary.right.value
                    def _fmt(val):
                        return f"SELECT {val}"
                    return _fmt("safe")

                def visit_deleted_taint(self, binary, **kw):
                    val = binary.right.value
                    del val
                    val = "safe"
                    return f"SELECT {val}"
            """
        )
        assert errors == []

    def test_diagnostic_mutators_and_non_string_ops(self):
        errors = _check(
            """
            class BigQueryCompiler(SQLCompiler):
                def visit_bindparam(self, bindparam, **kw):
                    assert bindparam.value is not None, f"Bad value: {bindparam.value}"
                    assert_(bindparam.value != "", f"Empty: {bindparam.value}")
                    warnings.warn(f"Deprecated: {bindparam.value}")
                    sqlalchemy.util.warn(f"Warn: {bindparam.value}")
                    logger.warning(f"Log: {bindparam.value}")
                    if isinstance(bindparam.value, Decimal):
                        t = bindparam.value.as_tuple()
                        n = len(t.digits) + 1
                        rem = 10 % bindparam.value
                        _ = (n, rem)
                    bindparam.value = str(bindparam.value)
                    bindparam.value += "_x"
                    return self.process(bindparam, **kw)

                @staticmethod
                def _maybe_reescape(binary):
                    escape = binary.modifiers.pop("escape", None)
                    if escape and escape != "\\\\":
                        binary.right.value = escape.join(
                            v.replace(escape, "\\\\")
                            for v in binary.right.value.split(escape + escape)
                        )
                    return binary

                def _value_parameter(self, value):
                    return f"SELECT {value}"

                def visit_join_clause(self, table1, table2, cond, **kw):
                    return self.process(table1.join(table2, cond), **kw)
            """
        )
        assert errors == []

    def test_inline_ignore_comment(self):
        errors = _check(
            """
            class MyCompiler(SQLCompiler):
                def visit_ignored(self, binary, **kw):
                    left = self.process(binary.left, **kw)
                    part = f".{binary.right.value}"  # compiler-safety: ignore
                    return f"{left}{part}"

                def visit_multiline_ignored(self, binary, **kw):
                    return (
                        f"{self.process(binary.left)}."
                        f"{binary.right.value}"  # compiler-safety: ignore
                    )
            """
        )
        assert errors == []

        # Marker inside a string literal must NOT suppress the error.
        errors = _check(
            """
            class MyCompiler(SQLCompiler):
                def visit_fake_ignore(self, binary, **kw):
                    return f"{binary.right.value} -- compiler-safety: ignore"
            """
        )
        assert len(errors) == 1

    def test_no_duplicate_errors_on_chained_or_nested_sinks(self):
        errors = _check(
            """
            class MyCompiler(SQLCompiler):
                def visit_chained(self, binary, **kw):
                    left = self.process(binary.left, **kw)
                    return left + "." + binary.right.value + ")"

                def visit_nested(self, binary, **kw):
                    part = f".{binary.right.value}"
                    return f"SELECT {part}"
            """
        )
        assert len(errors) == 2


class TestCLIAndPackageIntegration:
    def test_current_package_passes(self):
        errors = checker.check_paths([PACKAGE_ROOT / "sqlalchemy_bigquery"])
        assert errors == []

    def test_cli_no_args_returns_2(self, capsys):
        assert checker.main([]) == 2
        assert "Usage:" in capsys.readouterr().err

    def test_cli_missing_path_returns_2(self, capsys, tmp_path):
        missing = tmp_path / "does_not_exist.py"
        assert checker.main([str(missing)]) == 2
        assert "does not exist" in capsys.readouterr().err

    def test_cli_directory_walk_and_exit_codes(self, capsys, tmp_path):
        clean_file = tmp_path / "clean.py"
        clean_file.write_text(
            "class C(SQLCompiler):\n"
            "    def visit_x(self, b):\n"
            "        return self.process(b.right)\n",
            encoding="utf-8",
        )
        (tmp_path / "notes.txt").write_text("not python", encoding="utf-8")
        pycache = tmp_path / "__pycache__"
        pycache.mkdir()
        (pycache / "ignored.py").write_text(
            "class C(SQLCompiler):\n"
            "    def visit_x(self, b):\n"
            "        return f'{b.right.value}'\n",
            encoding="utf-8",
        )
        assert checker.main([str(tmp_path)]) == 0
        assert capsys.readouterr().err == ""

        bad_file = tmp_path / "sub" / "bad.py"
        bad_file.parent.mkdir()
        bad_file.write_text(
            "class C(SQLCompiler):\n"
            "    def visit_x(self, b):\n"
            "        return f'{b.right.value}'\n",
            encoding="utf-8",
        )
        assert checker.main([str(clean_file)]) == 0
        assert checker.main([str(bad_file)]) == 1
        err_out = capsys.readouterr().err
        assert str(bad_file) in err_out
        assert "visit_x" in err_out

        assert checker.main([str(tmp_path)]) == 1
        err_out = capsys.readouterr().err
        assert str(bad_file) in err_out
        assert "visit_x" in err_out
