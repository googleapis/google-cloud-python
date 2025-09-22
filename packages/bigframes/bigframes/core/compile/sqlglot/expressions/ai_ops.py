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

from bigframes import operations as ops
from bigframes.core.compile.sqlglot import scalar_compiler
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr

register_nary_op = scalar_compiler.scalar_op_compiler.register_nary_op


@register_nary_op(ops.AIGenerateBool, pass_op=True)
def _(*exprs: TypedExpr, op: ops.AIGenerateBool) -> sge.Expression:

    prompt: list[str | sge.Expression] = []
    column_ref_idx = 0

    for elem in op.prompt_context:
        if elem is None:
            prompt.append(exprs[column_ref_idx].expr)
        else:
            prompt.append(sge.Literal.string(elem))

    args = [sge.Kwarg(this="prompt", expression=sge.Tuple(expressions=prompt))]

    args.append(
        sge.Kwarg(this="connection_id", expression=sge.Literal.string(op.connection_id))
    )

    if op.endpoint is not None:
        args.append(
            sge.Kwarg(this="endpoint", expression=sge.Literal.string(op.endpoint))
        )

    args.append(
        sge.Kwarg(
            this="request_type", expression=sge.Literal.string(op.request_type.upper())
        )
    )

    if op.model_params is not None:
        args.append(
            sge.Kwarg(
                this="model_params",
                # sge.JSON requires a newer SQLGlot version than 23.6.3.
                # PARSE_JSON won't work as the function requires a JSON literal.
                expression=sge.JSON(this=sge.Literal.string(op.model_params)),
            )
        )

    return sge.func("AI.GENERATE_BOOL", *args)
