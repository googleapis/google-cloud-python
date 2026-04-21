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
    args = [
        _construct_prompt(exprs, op.prompt_context, param_name="input"),
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

    for field, value in op_args.items():
        if value is None or field == "prompt_context":
            continue

        if field == "categories":
            category_literals = [sge.Literal.string(cat) for cat in value]
            categories_arg = sge.Kwarg(
                this="categories", expression=sge.array(*category_literals)
            )
            args.append(categories_arg)
        elif field == "model_params":
            # model_params is a JSON string, so we need to use the JSON function to pass it as a named argument.
            args.append(
                sge.Kwarg(
                    this="model_params",
                    # sge.JSON requires the SQLGlot version to be at least 25.18.0
                    # PARSE_JSON won't work as the function requires a JSON literal.
                    expression=sge.JSON(this=sge.Literal.string(value)),
                )
            )
        elif field == "request_type":
            args.append(
                sge.Kwarg(this=field, expression=sge.Literal.string(value.upper()))
            )
        else:
            args.append(
                sge.Kwarg(this=field, expression=sge.Literal.string(str(value)))
            )

    return args
