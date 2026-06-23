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

import math

import pytest

import bigframes.core.expression as ex
import bigframes.operations as ops
from bigframes.core.bytecode import py_to_expression


def test_py_to_expression_simple_arithmetic():
    func = lambda x: x + 1
    expr = py_to_expression(func)
    assert expr is not None

    expected = ops.add_op.as_expr(ex.free_var("x"), ex.const(1))
    assert expr == expected


def test_py_to_expression_math_function():
    func = lambda x: math.sin(x)
    expr = py_to_expression(func)
    assert expr is not None

    expected = ops.numeric_ops.sin_op.as_expr(ex.free_var("x"))
    assert expr == expected


def test_py_to_expression_negation():
    func = lambda x: -x
    expr = py_to_expression(func)
    assert expr is not None

    expected = ops.numeric_ops.neg_op.as_expr(ex.free_var("x"))
    assert expr == expected


def test_py_to_expression_comparison():
    func = lambda x, y: x == y
    expr = py_to_expression(func)
    assert expr is not None

    expected = ops.comparison_ops.eq_op.as_expr(ex.free_var("x"), ex.free_var("y"))
    assert expr == expected


def test_py_to_expression_unsupported():
    # Control flow or unsupported structures should return None
    def func_with_loop(x):
        res = 0
        for val in range(int(x)):
            res += val
        return res

    with pytest.raises(ValueError):
        py_to_expression(func_with_loop)


global_none_val = None


def test_py_to_expression_global_none():
    # Test resolving a global variable explicitly set to None
    func = lambda x: x == global_none_val
    expr = py_to_expression(func)
    assert expr is not None

    expected = ops.comparison_ops.eq_op.as_expr(ex.free_var("x"), ex.const(None))
    assert expr == expected
