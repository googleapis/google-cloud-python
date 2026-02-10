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

from dataclasses import asdict

import bigframes_vendored.sqlglot.expressions as sge

from bigframes import operations as ops
from bigframes.core.compile.sqlglot import expression_compiler
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr

register_nary_op = expression_compiler.expression_compiler.register_nary_op


@register_nary_op(ops.AIGenerate, pass_op=True)
def _(*exprs: TypedExpr, op: ops.AIGenerate) -> sge.Expression:
    args = [_construct_prompt(exprs, op.prompt_context)] + _construct_named_args(op)

    return sge.func("AI.GENERATE", *args)


@register_nary_op(ops.AIGenerateBool, pass_op=True)
def _(*exprs: TypedExpr, op: ops.AIGenerateBool) -> sge.Expression:
    args = [_construct_prompt(exprs, op.prompt_context)] + _construct_named_args(op)

    return sge.func("AI.GENERATE_BOOL", *args)


@register_nary_op(ops.AIGenerateInt, pass_op=True)
def _(*exprs: TypedExpr, op: ops.AIGenerateInt) -> sge.Expression:
    args = [_construct_prompt(exprs, op.prompt_context)] + _construct_named_args(op)

    return sge.func("AI.GENERATE_INT", *args)


@register_nary_op(ops.AIGenerateDouble, pass_op=True)
def _(*exprs: TypedExpr, op: ops.AIGenerateDouble) -> sge.Expression:
    args = [_construct_prompt(exprs, op.prompt_context)] + _construct_named_args(op)

    return sge.func("AI.GENERATE_DOUBLE", *args)


@register_nary_op(ops.AIIf, pass_op=True)
def _(*exprs: TypedExpr, op: ops.AIIf) -> sge.Expression:
    args = [_construct_prompt(exprs, op.prompt_context)] + _construct_named_args(op)

    return sge.func("AI.IF", *args)


@register_nary_op(ops.AIClassify, pass_op=True)
def _(*exprs: TypedExpr, op: ops.AIClassify) -> sge.Expression:
    category_literals = [sge.Literal.string(cat) for cat in op.categories]
    categories_arg = sge.Kwarg(
        this="categories", expression=sge.array(*category_literals)
    )

    args = [
        _construct_prompt(exprs, op.prompt_context, param_name="input"),
        categories_arg,
    ] + _construct_named_args(op)

    return sge.func("AI.CLASSIFY", *args)


@register_nary_op(ops.AIScore, pass_op=True)
def _(*exprs: TypedExpr, op: ops.AIScore) -> sge.Expression:
    args = [_construct_prompt(exprs, op.prompt_context)] + _construct_named_args(op)

    return sge.func("AI.SCORE", *args)


def _construct_prompt(
    exprs: tuple[TypedExpr, ...],
    prompt_context: tuple[str | None, ...],
    param_name: str = "prompt",
) -> sge.Kwarg:
    prompt: list[str | sge.Expression] = []
    column_ref_idx = 0

    for elem in prompt_context:
        if elem is None:
            prompt.append(exprs[column_ref_idx].expr)
            column_ref_idx += 1
        else:
            prompt.append(sge.Literal.string(elem))

    return sge.Kwarg(this=param_name, expression=sge.Tuple(expressions=prompt))


def _construct_named_args(op: ops.NaryOp) -> list[sge.Kwarg]:
    args = []

    op_args = asdict(op)

    connection_id = op_args.get("connection_id", None)
    if connection_id is not None:
        args.append(
            sge.Kwarg(
                this="connection_id", expression=sge.Literal.string(connection_id)
            )
        )

    endpoit = op_args.get("endpoint", None)
    if endpoit is not None:
        args.append(sge.Kwarg(this="endpoint", expression=sge.Literal.string(endpoit)))

    request_type = op_args.get("request_type", None)
    if request_type is not None:
        args.append(
            sge.Kwarg(
                this="request_type", expression=sge.Literal.string(request_type.upper())
            )
        )

    model_params = op_args.get("model_params", None)
    if model_params is not None:
        args.append(
            sge.Kwarg(
                this="model_params",
                # sge.JSON requires the SQLGlot version to be at least 25.18.0
                # PARSE_JSON won't work as the function requires a JSON literal.
                expression=sge.JSON(this=sge.Literal.string(model_params)),
            )
        )

    output_schema = op_args.get("output_schema", None)
    if output_schema is not None:
        args.append(
            sge.Kwarg(
                this="output_schema",
                expression=sge.Literal.string(output_schema),
            )
        )

    return args
