# Copyright 2025 Google LLC
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

import unittest.mock as mock

import bigframes_vendored.sqlglot.expressions as sge
import pytest

import bigframes.core.compile.sqlglot.expression_compiler as expression_compiler
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr
import bigframes.operations as ops


def test_register_unary_op():
    compiler = expression_compiler.ExpressionCompiler()

    class MockUnaryOp(ops.UnaryOp):
        name = "mock_unary_op"

    mock_op = MockUnaryOp()
    mock_impl = mock.Mock()

    @compiler.register_unary_op(mock_op)
    def _(expr: TypedExpr) -> sge.Expression:
        mock_impl(expr)
        return sge.Identifier(this="output")

    arg = TypedExpr(sge.Identifier(this="input"), "string")
    result = compiler.compile_row_op(mock_op, [arg])
    assert result == sge.Identifier(this="output")
    mock_impl.assert_called_once_with(arg)


def test_register_unary_op_pass_op():
    compiler = expression_compiler.ExpressionCompiler()

    class MockUnaryOp(ops.UnaryOp):
        name = "mock_unary_op_pass_op"

    mock_op = MockUnaryOp()
    mock_impl = mock.Mock()

    @compiler.register_unary_op(mock_op, pass_op=True)
    def _(expr: TypedExpr, op: ops.UnaryOp) -> sge.Expression:
        mock_impl(expr, op)
        return sge.Identifier(this="output")

    arg = TypedExpr(sge.Identifier(this="input"), "string")
    result = compiler.compile_row_op(mock_op, [arg])
    assert result == sge.Identifier(this="output")
    mock_impl.assert_called_once_with(arg, mock_op)


def test_register_binary_op():
    compiler = expression_compiler.ExpressionCompiler()

    class MockBinaryOp(ops.BinaryOp):
        name = "mock_binary_op"

    mock_op = MockBinaryOp()
    mock_impl = mock.Mock()

    @compiler.register_binary_op(mock_op)
    def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
        mock_impl(left, right)
        return sge.Identifier(this="output")

    arg1 = TypedExpr(sge.Identifier(this="input1"), "string")
    arg2 = TypedExpr(sge.Identifier(this="input2"), "string")
    result = compiler.compile_row_op(mock_op, [arg1, arg2])
    assert result == sge.Identifier(this="output")
    mock_impl.assert_called_once_with(arg1, arg2)


def test_register_binary_op_pass_on():
    compiler = expression_compiler.ExpressionCompiler()

    class MockBinaryOp(ops.BinaryOp):
        name = "mock_binary_op_pass_op"

    mock_op = MockBinaryOp()
    mock_impl = mock.Mock()

    @compiler.register_binary_op(mock_op, pass_op=True)
    def _(left: TypedExpr, right: TypedExpr, op: ops.BinaryOp) -> sge.Expression:
        mock_impl(left, right, op)
        return sge.Identifier(this="output")

    arg1 = TypedExpr(sge.Identifier(this="input1"), "string")
    arg2 = TypedExpr(sge.Identifier(this="input2"), "string")
    result = compiler.compile_row_op(mock_op, [arg1, arg2])
    assert result == sge.Identifier(this="output")
    mock_impl.assert_called_once_with(arg1, arg2, mock_op)


def test_register_ternary_op():
    compiler = expression_compiler.ExpressionCompiler()

    class MockTernaryOp(ops.TernaryOp):
        name = "mock_ternary_op"

    mock_op = MockTernaryOp()
    mock_impl = mock.Mock()

    @compiler.register_ternary_op(mock_op)
    def _(arg1: TypedExpr, arg2: TypedExpr, arg3: TypedExpr) -> sge.Expression:
        mock_impl(arg1, arg2, arg3)
        return sge.Identifier(this="output")

    arg1 = TypedExpr(sge.Identifier(this="input1"), "string")
    arg2 = TypedExpr(sge.Identifier(this="input2"), "string")
    arg3 = TypedExpr(sge.Identifier(this="input3"), "string")
    result = compiler.compile_row_op(mock_op, [arg1, arg2, arg3])
    assert result == sge.Identifier(this="output")
    mock_impl.assert_called_once_with(arg1, arg2, arg3)


def test_register_nary_op():
    compiler = expression_compiler.ExpressionCompiler()

    class MockNaryOp(ops.NaryOp):
        name = "mock_nary_op"

    mock_op = MockNaryOp()
    mock_impl = mock.Mock()

    @compiler.register_nary_op(mock_op)
    def _(*args: TypedExpr) -> sge.Expression:
        mock_impl(*args)
        return sge.Identifier(this="output")

    arg1 = TypedExpr(sge.Identifier(this="input1"), "string")
    arg2 = TypedExpr(sge.Identifier(this="input2"), "string")
    result = compiler.compile_row_op(mock_op, [arg1, arg2])
    assert result == sge.Identifier(this="output")
    mock_impl.assert_called_once_with(arg1, arg2)


def test_register_nary_op_pass_on():
    compiler = expression_compiler.ExpressionCompiler()

    class MockNaryOp(ops.NaryOp):
        name = "mock_nary_op_pass_op"

    mock_op = MockNaryOp()
    mock_impl = mock.Mock()

    @compiler.register_nary_op(mock_op, pass_op=True)
    def _(*args: TypedExpr, op: ops.NaryOp) -> sge.Expression:
        mock_impl(*args, op=op)
        return sge.Identifier(this="output")

    arg1 = TypedExpr(sge.Identifier(this="input1"), "string")
    arg2 = TypedExpr(sge.Identifier(this="input2"), "string")
    arg3 = TypedExpr(sge.Identifier(this="input3"), "string")
    arg4 = TypedExpr(sge.Identifier(this="input4"), "string")
    result = compiler.compile_row_op(mock_op, [arg1, arg2, arg3, arg4])
    assert result == sge.Identifier(this="output")
    mock_impl.assert_called_once_with(arg1, arg2, arg3, arg4, op=mock_op)


def test_binary_op_parentheses():
    compiler = expression_compiler.ExpressionCompiler()

    class MockAddOp(ops.BinaryOp):
        name = "mock_add_op"

    class MockMulOp(ops.BinaryOp):
        name = "mock_mul_op"

    add_op = MockAddOp()
    mul_op = MockMulOp()

    @compiler.register_binary_op(add_op)
    def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
        return sge.Add(this=left.expr, expression=right.expr)

    @compiler.register_binary_op(mul_op)
    def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
        return sge.Mul(this=left.expr, expression=right.expr)

    a = TypedExpr(sge.Identifier(this="a"), "int")
    b = TypedExpr(sge.Identifier(this="b"), "int")
    c = TypedExpr(sge.Identifier(this="c"), "int")

    # (a + b) * c
    add_expr = compiler.compile_row_op(add_op, [a, b])
    add_typed_expr = TypedExpr(add_expr, "int")
    result1 = compiler.compile_row_op(mul_op, [add_typed_expr, c])
    assert result1.sql() == "(a + b) * c"

    # a * (b + c)
    add_expr_2 = compiler.compile_row_op(add_op, [b, c])
    add_typed_expr_2 = TypedExpr(add_expr_2, "int")
    result2 = compiler.compile_row_op(mul_op, [a, add_typed_expr_2])
    assert result2.sql() == "a * (b + c)"


def test_register_duplicate_op_raises():
    compiler = expression_compiler.ExpressionCompiler()

    class MockUnaryOp(ops.UnaryOp):
        name = "mock_unary_op_duplicate"

    mock_op = MockUnaryOp()

    @compiler.register_unary_op(mock_op)
    def _(expr: TypedExpr) -> sge.Expression:
        return sge.Identifier(this="output")

    with pytest.raises(ValueError):

        @compiler.register_unary_op(mock_op)
        def _(expr: TypedExpr) -> sge.Expression:
            return sge.Identifier(this="output2")
