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

"""AST linter to prohibit unescaped `.value` interpolation in SQLAlchemy compilers.

Checks methods on SQLAlchemy ``*Compiler`` subclasses and ``@compiles``-decorated
functions to catch direct or aliased interpolation of raw ``BindParameter`` values
(``.value`` / ``.effective_value``) into SQL strings without compiling through
``process(...)`` or escaping via an identifier/literal escaper.
"""

from __future__ import annotations

import ast
import io
import sys
import tokenize
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

UNSAFE_VALUE_ATTRS = frozenset({"value", "effective_value"})
IGNORE_MARKER = "compiler-safety: ignore"

PREPARER_SANITIZER_METHODS = frozenset(
    {
        "quote",
        "quote_identifier",
        "quote_column",
        "quote_schema",
        "format_table",
        "format_column",
        "format_label",
        "format_schema",
        "format_constraint",
        "format_sequence",
    }
)

ESCAPING_SANITIZER_NAMES = frozenset(
    {
        "render_literal_value",
        "escape_literal_column",
        "process_string_literal",
        "process_timestamp_literal",
        "process_literal_as_class_tagged_str",
        "_process_option_value",
        "alter_table",
        "alter_column",
        "format_column_name",
        "format_type",
    }
)

SAFE_METADATA_BUILTINS = frozenset(
    {"isinstance", "issubclass", "hasattr", "type", "len", "id", "callable"}
)

NUMERIC_BUILTINS = frozenset({"len", "int", "float", "abs", "round", "sum"})

LOG_METHODS = frozenset(
    {"debug", "info", "warning", "warn", "error", "exception", "critical", "log"}
)

CONTAINER_MUTATOR_METHODS = frozenset(
    {"append", "extend", "insert", "add", "update", "setdefault"}
)

FORMAT_METHODS = frozenset({"format", "format_map", "substitute", "safe_substitute"})

SQL_RETURNING_METHODS = frozenset({"get_column_specification", "post_create_table"})


@dataclass(frozen=True)
class LintError:
    """A single compiler safety lint violation."""

    filename: str
    lineno: int
    col_offset: int
    function: str
    message: str

    def format(self) -> str:
        return (
            f"{self.filename}:{self.lineno}:{self.col_offset}: "
            f"In '{self.function}': {self.message}"
        )


def _find_ignored_lines(source: str) -> set[int]:
    """Return 1-based line numbers containing an inline ignore comment."""
    ignored: set[int] = set()
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        for tok_type, tok_str, (lineno, _), _, _ in tokens:
            if tok_type == tokenize.COMMENT and IGNORE_MARKER in tok_str:
                ignored.add(lineno)
    except tokenize.TokenError:
        pass
    return ignored


def _base_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return ""


def _is_compiler_class(node: ast.ClassDef) -> bool:
    compiler_suffixes = ("Compiler", "CompilerMixin")
    return node.name.endswith(compiler_suffixes) or any(
        _base_name(base).endswith(compiler_suffixes) for base in node.bases
    )


def _is_compiles_decorated(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if _base_name(target) == "compiles":
            return True
    return False


def _is_sql_returning_function(name: str, is_compiles: bool) -> bool:
    return (
        is_compiles
        or name.startswith("visit_")
        or name.endswith("_clause")
        or name in SQL_RETURNING_METHODS
    )


def _is_unsafe_value_attr(node: ast.AST) -> bool:
    return isinstance(node, ast.Attribute) and node.attr in UNSAFE_VALUE_ATTRS


def _is_getattr_value_call(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "getattr"
        and len(node.args) >= 2
        and isinstance(node.args[1], ast.Constant)
        and node.args[1].value in UNSAFE_VALUE_ATTRS
    )


def _is_preparer_receiver(node: ast.AST) -> bool:
    return "preparer" in _base_name(node).lower()


def _is_escaping_sanitizer_call(node: ast.Call) -> bool:
    """Return True for calls that escape/quote their argument into safe SQL."""
    func = node.func
    if isinstance(func, ast.Name):
        return func.id in ESCAPING_SANITIZER_NAMES
    if isinstance(func, ast.Attribute):
        if func.attr in ESCAPING_SANITIZER_NAMES:
            return True
        if func.attr in PREPARER_SANITIZER_METHODS and _is_preparer_receiver(
            func.value
        ):
            return True
    return False


def _is_dispatch_sanitizer_call(node: ast.Call) -> bool:
    """Return True for SQLAlchemy compiler dispatch calls returning compiled SQL."""
    func = node.func
    return isinstance(func, ast.Attribute) and (
        func.attr == "process" or func.attr.startswith("visit_")
    )


def _is_sanitizer_call(node: ast.Call) -> bool:
    return _is_escaping_sanitizer_call(node) or _is_dispatch_sanitizer_call(node)


def _is_safe_metadata_call(node: ast.Call) -> bool:
    return isinstance(node.func, ast.Name) and node.func.id in SAFE_METADATA_BUILTINS


def _is_non_sql_call(node: ast.Call) -> bool:
    """Return True for diagnostic/logging/assertion calls that do not emit SQL."""
    func = node.func
    if isinstance(func, ast.Name):
        return func.id in {"assert_", "warn"}
    if isinstance(func, ast.Attribute):
        if func.attr == "warn":
            return True
        if func.attr in LOG_METHODS and "log" in _base_name(func.value).lower():
            return True
    return False


def _is_format_call(node: ast.Call) -> bool:
    return isinstance(node.func, ast.Attribute) and node.func.attr in FORMAT_METHODS


def _is_str_join_call(node: ast.Call) -> bool:
    return (
        isinstance(node.func, ast.Attribute)
        and node.func.attr == "join"
        and len(node.args) == 1
        and not node.keywords
    )


def _is_obviously_numeric(node: ast.AST) -> bool:
    if isinstance(node, ast.Constant):
        return not isinstance(node.value, (str, bytes))
    if isinstance(node, ast.UnaryOp) and isinstance(
        node.op, (ast.UAdd, ast.USub, ast.Invert)
    ):
        return True
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        return node.func.id in NUMERIC_BUILTINS
    return False


def _is_string_mod(node: ast.BinOp) -> bool:
    return isinstance(node.op, ast.Mod) and not _is_obviously_numeric(node.left)


def _flatten_add(node: ast.AST) -> list[ast.AST]:
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _flatten_add(node.left) + _flatten_add(node.right)
    return [node]


def _is_string_add(operands: Sequence[ast.AST]) -> bool:
    return all(
        not _is_obviously_numeric(op)
        and not isinstance(op, (ast.List, ast.Tuple, ast.ListComp))
        for op in operands
    )


def _is_string_sink(node: ast.AST) -> bool:
    if isinstance(node, ast.JoinedStr):
        return True
    if isinstance(node, ast.BinOp):
        return _is_string_mod(node) or (
            isinstance(node.op, ast.Add) and _is_string_add(_flatten_add(node))
        )
    if isinstance(node, ast.Call):
        return _is_format_call(node) or _is_str_join_call(node)
    return False


def _arg_names(args: ast.arguments) -> set[str]:
    names = {a.arg for a in (*args.posonlyargs, *args.args, *args.kwonlyargs)}
    if args.vararg is not None:
        names.add(args.vararg.arg)
    if args.kwarg is not None:
        names.add(args.kwarg.arg)
    return names


def _target_names(target: ast.AST) -> list[str]:
    if isinstance(target, ast.Name):
        return [target.id]
    if isinstance(target, (ast.Tuple, ast.List)):
        return [name for elt in target.elts for name in _target_names(elt)]
    if isinstance(target, ast.Starred):
        return _target_names(target.value)
    return []


def _pattern_bound_names(pattern: ast.pattern) -> list[str]:
    names: list[str] = []
    if isinstance(pattern, ast.MatchAs):
        if pattern.name is not None:
            names.append(pattern.name)
        if pattern.pattern is not None:
            names.extend(_pattern_bound_names(pattern.pattern))
    elif isinstance(pattern, ast.MatchStar) and pattern.name is not None:
        names.append(pattern.name)
    elif isinstance(pattern, ast.MatchMapping):
        if pattern.rest is not None:
            names.append(pattern.rest)
        for p in pattern.patterns:
            names.extend(_pattern_bound_names(p))
    elif isinstance(pattern, ast.MatchClass):
        for p in (*pattern.patterns, *pattern.kwd_patterns):
            names.extend(_pattern_bound_names(p))
    elif isinstance(pattern, (ast.MatchSequence, ast.MatchOr)):
        for p in pattern.patterns:
            names.extend(_pattern_bound_names(p))
    return names


def _is_irrefutable_pattern(pattern: ast.pattern) -> bool:
    if isinstance(pattern, ast.MatchAs):
        return pattern.pattern is None or _is_irrefutable_pattern(pattern.pattern)
    if isinstance(pattern, ast.MatchOr):
        return any(_is_irrefutable_pattern(p) for p in pattern.patterns)
    return False


class _FunctionChecker:
    """Flow-sensitive checker for a single compiler method or `@compiles` function."""

    def __init__(
        self,
        parent: CompilerSafetyVisitor,
        func_name: str,
        compiler_ref: str,
        is_sql_returning: bool,
    ):
        self.parent = parent
        self.func_name = func_name
        self.compiler_ref = compiler_ref
        self.is_sql_returning = is_sql_returning
        self._loop_break_taints: list[set[str]] = []

    def _is_ignored(self, node: ast.AST) -> bool:
        start = getattr(node, "lineno", None)
        if start is None:
            return False
        end = getattr(node, "end_lineno", start) or start
        return any(line in self.parent.ignored_lines for line in range(start, end + 1))

    def _report(self, node: ast.AST, kind: str = "interpolation") -> None:
        if self._is_ignored(node):
            return
        msg = (
            f"Unsafe {kind} of `.value` detected. "
            f"Compile via `{self.compiler_ref}.process(...)` or escape with "
            f"`{self.compiler_ref}.preparer.quote_identifier(...)`."
        )
        self.parent.add_error(
            LintError(
                filename=self.parent.filename,
                lineno=getattr(node, "lineno", 0),
                col_offset=getattr(node, "col_offset", 0),
                function=self.func_name,
                message=msg,
            )
        )

    def _update_target_taint(
        self, target: ast.AST, is_tainted: bool, tainted: set[str]
    ) -> None:
        if isinstance(target, ast.Subscript):
            if is_tainted and isinstance(target.value, ast.Name):
                tainted.add(target.value.id)
            return
        for name in _target_names(target):
            if is_tainted:
                tainted.add(name)
            else:
                tainted.discard(name)

    def _call_args_have_taint(self, call: ast.Call, tainted: set[str]) -> bool:
        return any(self._expr_has_taint(arg, tainted) for arg in call.args) or any(
            self._expr_has_taint(kw.value, tainted) for kw in call.keywords
        )

    def _expr_has_taint(self, expr: ast.AST, tainted: set[str]) -> bool:
        """Return True if `expr` evaluates to an unsanitized `.value`-derived value.

        Stops at string-formatting sinks (which report their own errors directly)
        and at recognized sanitizer/metadata calls.
        """
        if _is_unsafe_value_attr(expr):
            return True
        if isinstance(expr, ast.Name):
            return expr.id in tainted
        if isinstance(expr, ast.Call):
            if _is_getattr_value_call(expr):
                return True
            if (
                _is_sanitizer_call(expr)
                or _is_safe_metadata_call(expr)
                or _is_format_call(expr)
                or _is_str_join_call(expr)
            ):
                return False
            return self._expr_has_taint(
                expr.func, tainted
            ) or self._call_args_have_taint(expr, tainted)
        if isinstance(expr, ast.JoinedStr):
            return False
        if isinstance(expr, ast.BinOp):
            if _is_string_sink(expr):
                return False
            return self._expr_has_taint(expr.left, tainted) or self._expr_has_taint(
                expr.right, tainted
            )
        if isinstance(
            expr, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
        ):
            comp_tainted = set(tainted)
            for gen in expr.generators:
                gen_tainted = self._expr_has_taint(gen.iter, comp_tainted)
                self._update_target_taint(gen.target, gen_tainted, comp_tainted)
            if isinstance(expr, ast.DictComp):
                return self._expr_has_taint(
                    expr.key, comp_tainted
                ) or self._expr_has_taint(expr.value, comp_tainted)
            return self._expr_has_taint(expr.elt, comp_tainted)
        if isinstance(expr, ast.Compare):
            return False
        if isinstance(expr, ast.UnaryOp) and isinstance(expr.op, ast.Not):
            return False
        if isinstance(expr, ast.IfExp):
            return self._expr_has_taint(expr.body, tainted) or self._expr_has_taint(
                expr.orelse, tainted
            )
        if isinstance(expr, ast.Subscript):
            return self._expr_has_taint(expr.value, tainted)
        if isinstance(expr, ast.Lambda):
            return self._expr_has_taint(expr.body, tainted - _arg_names(expr.args))
        return any(
            self._expr_has_taint(child, tainted) for child in ast.iter_child_nodes(expr)
        )

    def _check_expr(self, expr: ast.AST, tainted: set[str]) -> None:
        if isinstance(expr, ast.JoinedStr):
            for part in expr.values:
                if isinstance(part, ast.FormattedValue):
                    if self._expr_has_taint(part.value, tainted):
                        self._report(expr)
                    self._check_expr(part.value, tainted)
                    if part.format_spec is not None:
                        self._check_expr(part.format_spec, tainted)
            return

        if isinstance(expr, ast.BinOp):
            if _is_string_mod(expr):
                self._check_expr(expr.left, tainted)
                if self._expr_has_taint(expr.right, tainted):
                    self._report(expr)
                self._check_expr(expr.right, tainted)
                return
            if isinstance(expr.op, ast.Add):
                operands = _flatten_add(expr)
                if _is_string_add(operands) and any(
                    self._expr_has_taint(op, tainted) for op in operands
                ):
                    self._report(expr)
                for op in operands:
                    self._check_expr(op, tainted)
                return
            self._check_expr(expr.left, tainted)
            self._check_expr(expr.right, tainted)
            return

        if isinstance(expr, ast.Call):
            if _is_non_sql_call(expr) or _is_escaping_sanitizer_call(expr):
                return
            if _is_format_call(expr):
                assert isinstance(expr.func, ast.Attribute)
                self._check_expr(expr.func.value, tainted)
                if self._call_args_have_taint(expr, tainted):
                    self._report(expr)
            elif _is_str_join_call(expr):
                assert isinstance(expr.func, ast.Attribute)
                self._check_expr(expr.func.value, tainted)
                if self._expr_has_taint(expr.args[0], tainted):
                    self._report(expr)
            else:
                self._check_expr(expr.func, tainted)
            for arg in expr.args:
                self._check_expr(arg, tainted)
            for kw in expr.keywords:
                self._check_expr(kw.value, tainted)
            if (
                isinstance(expr.func, ast.Attribute)
                and expr.func.attr in CONTAINER_MUTATOR_METHODS
                and isinstance(expr.func.value, ast.Name)
                and self._call_args_have_taint(expr, tainted)
            ):
                tainted.add(expr.func.value.id)
            return

        if isinstance(
            expr, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
        ):
            comp_tainted = set(tainted)
            for gen in expr.generators:
                self._check_expr(gen.iter, comp_tainted)
                gen_tainted = self._expr_has_taint(gen.iter, comp_tainted)
                self._update_target_taint(gen.target, gen_tainted, comp_tainted)
                for if_expr in gen.ifs:
                    self._check_expr(if_expr, comp_tainted)
            if isinstance(expr, ast.DictComp):
                self._check_expr(expr.key, comp_tainted)
                self._check_expr(expr.value, comp_tainted)
            else:
                self._check_expr(expr.elt, comp_tainted)
            return

        if isinstance(expr, ast.NamedExpr):
            self._check_expr(expr.value, tainted)
            self._update_target_taint(
                expr.target, self._expr_has_taint(expr.value, tainted), tainted
            )
            return

        if isinstance(expr, ast.Lambda):
            self._check_expr(expr.body, tainted - _arg_names(expr.args))
            return

        for child in ast.iter_child_nodes(expr):
            self._check_expr(child, tainted)

    def _assign_target(
        self, target: ast.AST, value: ast.AST, tainted: set[str]
    ) -> None:
        if (
            isinstance(target, (ast.Tuple, ast.List))
            and isinstance(value, (ast.Tuple, ast.List))
            and len(target.elts) == len(value.elts)
            and not any(isinstance(e, ast.Starred) for e in target.elts)
        ):
            for t_elt, v_elt in zip(target.elts, value.elts):
                self._assign_target(t_elt, v_elt, tainted)
            return
        self._update_target_taint(target, self._expr_has_taint(value, tainted), tainted)

    def _finish_loop(
        self,
        pre_tainted: set[str],
        body_tainted: set[str],
        body_term: bool,
        break_tainted: set[str],
        orelse: Sequence[ast.stmt],
    ) -> tuple[set[str], bool]:
        normal_after = set(pre_tainted) | (set() if body_term else body_tainted)
        if orelse:
            else_tainted, else_term = self._check_block(orelse, set(normal_after))
            return (
                (else_tainted | break_tainted) if not else_term else break_tainted
            ), False
        return normal_after | break_tainted, False

    def _check_stmt(self, stmt: ast.stmt, tainted: set[str]) -> tuple[set[str], bool]:
        if isinstance(stmt, ast.Assign):
            if all(_is_unsafe_value_attr(t) for t in stmt.targets):
                return tainted, False
            self._check_expr(stmt.value, tainted)
            for target in stmt.targets:
                self._assign_target(target, stmt.value, tainted)
            return tainted, False

        if isinstance(stmt, ast.AnnAssign):
            if stmt.value is None or _is_unsafe_value_attr(stmt.target):
                return tainted, False
            self._check_expr(stmt.value, tainted)
            self._assign_target(stmt.target, stmt.value, tainted)
            return tainted, False

        if isinstance(stmt, ast.AugAssign):
            if _is_unsafe_value_attr(stmt.target):
                return tainted, False
            self._check_expr(stmt.value, tainted)
            target_tainted = self._expr_has_taint(stmt.target, tainted)
            value_tainted = self._expr_has_taint(stmt.value, tainted)
            if isinstance(stmt.op, ast.Add) and _is_string_add(
                [stmt.target, stmt.value]
            ):
                if target_tainted or value_tainted:
                    self._report(stmt)
                    if isinstance(stmt.target, ast.Name):
                        tainted.discard(stmt.target.id)
            elif value_tainted and isinstance(stmt.target, ast.Name):
                tainted.add(stmt.target.id)
            return tainted, False

        if isinstance(stmt, ast.Delete):
            for target in stmt.targets:
                if isinstance(target, ast.Name):
                    tainted.discard(target.id)
            return tainted, False

        if isinstance(stmt, ast.Expr):
            self._check_expr(stmt.value, tainted)
            return tainted, False

        if isinstance(stmt, ast.Return):
            if stmt.value is not None:
                self._check_expr(stmt.value, tainted)
                if (
                    self.is_sql_returning
                    and not _is_string_sink(stmt.value)
                    and self._expr_has_taint(stmt.value, tainted)
                ):
                    self._report(stmt, kind="return")
            return tainted, True

        if isinstance(stmt, (ast.Raise, ast.Continue)):
            return tainted, True

        if isinstance(stmt, ast.Break):
            if self._loop_break_taints:
                self._loop_break_taints[-1] |= tainted
            return tainted, True

        if isinstance(stmt, ast.Assert):
            self._check_expr(stmt.test, tainted)
            return tainted, False

        if isinstance(stmt, ast.If):
            self._check_expr(stmt.test, tainted)
            body_tainted, body_term = self._check_block(stmt.body, set(tainted))
            else_tainted, else_term = self._check_block(stmt.orelse, set(tainted))
            if body_term and else_term:
                return body_tainted | else_tainted, True
            if body_term:
                return else_tainted, False
            if else_term:
                return body_tainted, False
            return body_tainted | else_tainted, False

        if isinstance(stmt, (ast.For, ast.AsyncFor)):
            self._check_expr(stmt.iter, tainted)
            iter_tainted = self._expr_has_taint(stmt.iter, tainted)
            loop_tainted = set(tainted)
            self._update_target_taint(stmt.target, iter_tainted, loop_tainted)
            self._loop_break_taints.append(set())
            body_tainted, body_term = self._check_block(stmt.body, set(loop_tainted))
            if not body_term and not body_tainted.issubset(loop_tainted):
                merged = loop_tainted | body_tainted
                self._update_target_taint(stmt.target, iter_tainted, merged)
                body_tainted, _ = self._check_block(stmt.body, merged)
            break_tainted = self._loop_break_taints.pop()
            return self._finish_loop(
                tainted, body_tainted, body_term, break_tainted, stmt.orelse
            )

        if isinstance(stmt, ast.While):
            self._check_expr(stmt.test, tainted)
            self._loop_break_taints.append(set())
            body_tainted, body_term = self._check_block(stmt.body, set(tainted))
            if not body_term and not body_tainted.issubset(tainted):
                merged = set(tainted) | body_tainted
                self._check_expr(stmt.test, merged)
                body_tainted, _ = self._check_block(stmt.body, merged)
            break_tainted = self._loop_break_taints.pop()
            return self._finish_loop(
                tainted, body_tainted, body_term, break_tainted, stmt.orelse
            )

        if isinstance(stmt, (ast.With, ast.AsyncWith)):
            for item in stmt.items:
                self._check_expr(item.context_expr, tainted)
                if item.optional_vars is not None:
                    self._update_target_taint(
                        item.optional_vars,
                        self._expr_has_taint(item.context_expr, tainted),
                        tainted,
                    )
            return self._check_block(stmt.body, tainted)

        if isinstance(stmt, (ast.Try, ast.TryStar)):
            handler_in = set(tainted)
            body_tainted = set(tainted)
            body_term = False
            for body_stmt in stmt.body:
                body_tainted, body_term = self._check_stmt(body_stmt, body_tainted)
                handler_in |= body_tainted
                if body_term:
                    break
            final_in = set(handler_in)
            live_states: list[set[str]] = []
            if not body_term:
                if stmt.orelse:
                    else_tainted, else_term = self._check_block(
                        stmt.orelse, set(body_tainted)
                    )
                    final_in |= else_tainted
                    if not else_term:
                        live_states.append(else_tainted)
                else:
                    live_states.append(body_tainted)
            for handler in stmt.handlers:
                h_tainted = set(handler_in)
                if handler.name:
                    h_tainted.discard(handler.name)
                h_out, h_term = self._check_block(handler.body, h_tainted)
                final_in |= h_out
                if not h_term:
                    live_states.append(h_out)
            if not live_states:
                if stmt.finalbody:
                    self._check_block(stmt.finalbody, final_in)
                return final_in, True
            merged = set().union(*live_states)
            if stmt.finalbody:
                return self._check_block(stmt.finalbody, merged)
            return merged, False

        if isinstance(stmt, ast.Match):
            self._check_expr(stmt.subject, tainted)
            subj_tainted = self._expr_has_taint(stmt.subject, tainted)
            live_states = []
            has_wildcard = False
            for case in stmt.cases:
                c_tainted = set(tainted)
                for name in _pattern_bound_names(case.pattern):
                    if subj_tainted:
                        c_tainted.add(name)
                    else:
                        c_tainted.discard(name)
                if case.guard is not None:
                    self._check_expr(case.guard, c_tainted)
                c_out, c_term = self._check_block(case.body, c_tainted)
                if not c_term:
                    live_states.append(c_out)
                if case.guard is None and _is_irrefutable_pattern(case.pattern):
                    has_wildcard = True
            if not has_wildcard:
                live_states.append(set(tainted))
            if not live_states:
                return set(), True
            return set().union(*live_states), False

        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
            is_compiles = _is_compiles_decorated(stmt)
            nested = _FunctionChecker(
                parent=self.parent,
                func_name=stmt.name,
                compiler_ref="compiler" if is_compiles else self.compiler_ref,
                is_sql_returning=is_compiles,
            )
            nested.check_function(stmt, initial_tainted=tainted - _arg_names(stmt.args))
            return tainted, False

        if isinstance(stmt, ast.ClassDef):
            self.parent.visit_ClassDef(stmt)
            return tainted, False

        return tainted, False

    def _check_block(
        self, stmts: Sequence[ast.stmt], tainted: set[str]
    ) -> tuple[set[str], bool]:
        for stmt in stmts:
            tainted, terminated = self._check_stmt(stmt, tainted)
            if terminated:
                return tainted, True
        return tainted, False

    def check_function(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        initial_tainted: set[str] | None = None,
    ) -> None:
        tainted = set(initial_tainted) if initial_tainted else set()
        self._check_block(node.body, tainted)


class CompilerSafetyVisitor(ast.NodeVisitor):
    """Module-level AST visitor dispatching compiler classes and `@compiles` hooks."""

    def __init__(self, filename: str, ignored_lines: set[int] | None = None):
        self.filename = filename
        self.ignored_lines = ignored_lines or set()
        self.in_compiler_class = False
        self._errors: list[LintError] = []
        self._seen_errors: set[LintError] = set()

    @property
    def errors(self) -> list[LintError]:
        return list(self._errors)

    def add_error(self, error: LintError) -> None:
        if error not in self._seen_errors:
            self._seen_errors.add(error)
            self._errors.append(error)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        prev = self.in_compiler_class
        self.in_compiler_class = _is_compiler_class(node)
        self.generic_visit(node)
        self.in_compiler_class = prev

    def _visit_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        is_compiles = _is_compiles_decorated(node)
        if self.in_compiler_class or is_compiles:
            checker = _FunctionChecker(
                parent=self,
                func_name=node.name,
                compiler_ref="self" if self.in_compiler_class else "compiler",
                is_sql_returning=_is_sql_returning_function(node.name, is_compiles),
            )
            checker.check_function(node)
        else:
            self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_function(node)


def check_source(source: str, filename: str = "<string>") -> list[LintError]:
    """Check Python source code for unsafe `.value` interpolation in compilers."""
    tree = ast.parse(source, filename=filename)
    ignored_lines = _find_ignored_lines(source)
    visitor = CompilerSafetyVisitor(filename, ignored_lines=ignored_lines)
    visitor.visit(tree)
    return visitor.errors


def _iter_python_files(paths: Iterable[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"Path does not exist: {path}")
        if path.is_dir():
            files.extend(
                sorted(p for p in path.rglob("*.py") if "__pycache__" not in p.parts)
            )
        elif path.suffix == ".py":
            files.append(path)
    return files


def check_paths(paths: Sequence[Path]) -> list[LintError]:
    """Check one or more Python files or directories."""
    errors: list[LintError] = []
    for path in _iter_python_files(paths):
        source = path.read_text(encoding="utf-8")
        errors.extend(check_source(source, filename=str(path)))
    return errors


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print(
            "Usage: check_compiler_safety.py <path> [<path> ...]",
            file=sys.stderr,
        )
        return 2

    try:
        errors = check_paths([Path(arg) for arg in args])
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    for err in errors:
        print(err.format(), file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
