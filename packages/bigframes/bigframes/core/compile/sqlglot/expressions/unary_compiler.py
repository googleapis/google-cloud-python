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

import typing

import sqlglot.expressions as sge

from bigframes import operations as ops
from bigframes.core.compile.sqlglot.expressions.op_registration import OpRegistration
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr

UnaryOpCompiler = typing.Callable[[ops.UnaryOp, TypedExpr], sge.Expression]

UNARY_OP_REIGSTRATION = OpRegistration[UnaryOpCompiler]()


def compile(op: ops.UnaryOp, expr: TypedExpr) -> sge.Expression:
    return UNARY_OP_REIGSTRATION[op](op, expr)
