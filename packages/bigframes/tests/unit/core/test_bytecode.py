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

import math
import pytest

from bigframes.core.bytecode import dis_to_expr
import bigframes.core.expression as ex
import bigframes.operations as ops


def test_dis_to_expr_simple_arithmetic():
    func = lambda row: row.x + 1
    expr = dis_to_expr(func, unpack_mode=False)
    assert expr is not None
    
    expected = ops.add_op.as_expr(ex.free_var("x"), ex.const(1))
    assert expr == expected


def test_dis_to_expr_unpack_mode():
    func = lambda col1, col2: col1 * col2
    expr = dis_to_expr(func, unpack_mode=True)
    assert expr is not None
    
    expected = ops.mul_op.as_expr(ex.free_var("col1"), ex.free_var("col2"))
    assert expr == expected


def test_dis_to_expr_math_function():
    func = lambda row: math.sin(row.x)
    expr = dis_to_expr(func, unpack_mode=False)
    assert expr is not None
    
    expected = ops.numeric_ops.sin_op.as_expr(ex.free_var("x"))
    assert expr == expected


def test_dis_to_expr_negation():
    func = lambda row: -row.x
    expr = dis_to_expr(func, unpack_mode=False)
    assert expr is not None
    
    expected = ops.numeric_ops.neg_op.as_expr(ex.free_var("x"))
    assert expr == expected


def test_dis_to_expr_comparison():
    func = lambda row: row.x == row.y
    expr = dis_to_expr(func, unpack_mode=False)
    assert expr is not None
    
    expected = ops.comparison_ops.eq_op.as_expr(ex.free_var("x"), ex.free_var("y"))
    assert expr == expected


def test_dis_to_expr_unsupported():
    # Control flow or unsupported structures should return None
    def func_with_loop(row):
        res = 0
        for val in range(int(row.x)):
            res += val
        return res

    expr = dis_to_expr(func_with_loop, unpack_mode=False)
    assert expr is None
