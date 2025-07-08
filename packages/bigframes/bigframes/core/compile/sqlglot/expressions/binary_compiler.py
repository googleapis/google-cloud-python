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

from __future__ import annotations

import sqlglot.expressions as sge

from bigframes import dtypes
from bigframes import operations as ops
from bigframes.core.compile.sqlglot.expressions.op_registration import OpRegistration
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr

BINARY_OP_REGISTRATION = OpRegistration()


def compile(op: ops.BinaryOp, left: TypedExpr, right: TypedExpr) -> sge.Expression:
    return BINARY_OP_REGISTRATION[op](op, left, right)


# TODO: add parenthesize for operators
@BINARY_OP_REGISTRATION.register(ops.add_op)
def _(op, left: TypedExpr, right: TypedExpr) -> sge.Expression:
    if left.dtype == dtypes.STRING_DTYPE and right.dtype == dtypes.STRING_DTYPE:
        # String addition
        return sge.Concat(expressions=[left.expr, right.expr])

    # Numerical addition
    return sge.Add(this=left.expr, expression=right.expr)


@BINARY_OP_REGISTRATION.register(ops.ge_op)
def _(op, left: TypedExpr, right: TypedExpr) -> sge.Expression:
    return sge.GTE(this=left.expr, expression=right.expr)


@BINARY_OP_REGISTRATION.register(ops.JSONSet)
def _(op, left: TypedExpr, right: TypedExpr) -> sge.Expression:
    return sge.func("JSON_SET", left.expr, sge.convert(op.json_path), right.expr)
