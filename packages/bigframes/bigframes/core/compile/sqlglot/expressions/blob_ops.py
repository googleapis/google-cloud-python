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

import bigframes_vendored.sqlglot.expressions as sge

from bigframes import operations as ops
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr
import bigframes.core.compile.sqlglot.scalar_compiler as scalar_compiler

register_unary_op = scalar_compiler.scalar_op_compiler.register_unary_op
register_binary_op = scalar_compiler.scalar_op_compiler.register_binary_op


@register_unary_op(ops.obj_fetch_metadata_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("OBJ.FETCH_METADATA", expr.expr)


@register_unary_op(ops.ObjGetAccessUrl)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("OBJ.GET_ACCESS_URL", expr.expr)


@register_binary_op(ops.obj_make_ref_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    return sge.func("OBJ.MAKE_REF", left.expr, right.expr)
