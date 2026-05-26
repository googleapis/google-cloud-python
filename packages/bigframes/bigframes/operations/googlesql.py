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


from __future__ import annotations

import dataclasses
import typing
from enum import Enum, auto
from typing import Callable, Iterable

import pandas as pd

import bigframes.operations as ops
import bigframes.operations.type as op_typing
from bigframes import dtypes
from bigframes.operations.base_ops import _convert_expr_input

if typing.TYPE_CHECKING:
    # Avoids circular dependency
    import bigframes.core.expression

@dataclasses.dataclass(frozen=True)
class ArgSpec:
    arg_name: str | None = None
    optional: bool = False
    is_vararg: bool = False
    const_only: bool = False


@dataclasses.dataclass(frozen=True)
class OpSignature:
    # Detailed specs for each parameter. This is particularly relevant for ren
    arg_specs: typing.Sequence[ArgSpec]
    resolve_return_type: typing.Any
    has_varargs: bool = False


# Eventually we should migrate every op over to this that can be directly emitted 1:1 as a sql op
# This will allow us to fully lower to pure SQL dialect expressions and emitting sql text is trivial.
@dataclasses.dataclass(frozen=True)
class GoogleSqlScalarOp(ops.NaryOp):
    name: typing.ClassVar[str] = "googlesql_scalar"

    # syntax
    sql_name: str
    args: tuple[ArgSpec, ...]
    # typing
    signature: typing.Callable[..., dtypes.ExpressionType]

    # semantics
    is_deterministic: bool = True

    @property
    def deterministic(self) -> bool:
        return self.is_deterministic

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return self.signature(*input_types)
    def as_expr(self, *args: str | ex.Expression, **kwargs: Any) -> ex.Expression:
        import bigframes.core.expression as ex

        def wrap_input(expr, index: int):
            if isinstance(expr, ex.Expression):
                return expr

            is_const_only = False
            if index < len(self.args):
                is_const_only = self.args[index].const_only

            if isinstance(expr, str) and not is_const_only:
                return ex.deref(expr)
            else:
                return ex.const(expr)

        name_to_index = {arg_spec.arg_name: i for i, arg_spec in enumerate(self.args) if arg_spec.arg_name is not None}

        # Keep this in sync with output_type and compilers
        inputs: list[ex.Expression] = []

        for i, expr in enumerate(args):
            inputs.append(wrap_input(expr, i))

        for name, expr in kwargs.items():
            if name not in name_to_index:
                raise ValueError(f"Argument '{name}' is not valid for this operation.")
            index = name_to_index[name]
            if index >= len(inputs):
                inputs.extend([ex.OmittedArg()] * (index - len(inputs) + 1))
            inputs[index] = wrap_input(expr, index)

        return ex.OpExpression(
            self,
            tuple(inputs),
        )



RAND = GoogleSqlScalarOp(
    "RAND", args=(), is_deterministic=False, signature=lambda: dtypes.FLOAT_DTYPE
)


def _check_geo_input(
    t: dtypes.ExpressionType, out: dtypes.ExpressionType
) -> dtypes.ExpressionType:
    if t is not None and not dtypes.is_geo_like(t):
        raise TypeError(f"Type {t} is not supported. Type must be geo-like")
    return out


def _check_simplify_inputs(
    geo: dtypes.ExpressionType, tol: dtypes.ExpressionType
) -> dtypes.ExpressionType:
    if geo is not None and not dtypes.is_geo_like(geo):
        raise TypeError(f"Type {geo} is not supported. Type must be geo-like")
    if tol is not None and not dtypes.is_numeric(tol):
        raise TypeError(f"Type {tol} is not supported. Type must be numeric")
    return dtypes.GEO_DTYPE


ST_AREA = GoogleSqlScalarOp(
    "ST_AREA",
    args=(ArgSpec(),),
    is_deterministic=True,
    signature=lambda geo: _check_geo_input(geo, dtypes.FLOAT_DTYPE),
)

ST_CENTROID = GoogleSqlScalarOp(
    "ST_CENTROID",
    args=(ArgSpec(),),
    is_deterministic=True,
    signature=lambda geo: _check_geo_input(geo, dtypes.GEO_DTYPE),
)

ST_SIMPLIFY = GoogleSqlScalarOp(
    "ST_SIMPLIFY",
    args=(ArgSpec(), ArgSpec()),
    is_deterministic=True,
    signature=_check_simplify_inputs,
)

def _ai_classify_output_type(*input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
    output_mode = input_types[5] if len(input_types) > 5 else None
    if output_mode is not None:
        return dtypes.list_type(dtypes.STRING_DTYPE)
    return dtypes.STRING_DTYPE

AI_CLASSIFY = GoogleSqlScalarOp(
    sql_name="AI.CLASSIFY",
    args=(
        ArgSpec(arg_name="input"),
        ArgSpec(arg_name="categories"),
        ArgSpec(arg_name="examples", optional=True, const_only=True),
        ArgSpec(arg_name="connection_id", optional=True, const_only=True),
        ArgSpec(arg_name="endpoint", optional=True, const_only=True),
        ArgSpec(arg_name="output_mode", optional=True, const_only=True),
        ArgSpec(arg_name="optimization_mode", optional=True, const_only=True),
        ArgSpec(arg_name="max_error_ratio", optional=True, const_only=True),
    ),
    signature=_ai_classify_output_type,
)


@dataclasses.dataclass(frozen=True)
class AIGenerateOp(GoogleSqlScalarOp):
    sql_name: str = "AI.GENERATE"
    args: tuple[ArgSpec, ...] = (
        ArgSpec(arg_name="prompt"),
        ArgSpec(arg_name="connection_id", optional=True, const_only=True),
        ArgSpec(arg_name="endpoint", optional=True, const_only=True),
        ArgSpec(arg_name="request_type", optional=True, const_only=True),
        ArgSpec(arg_name="model_params", optional=True, const_only=True),
        ArgSpec(arg_name="output_schema", optional=True, const_only=True),
    )
    signature: typing.Callable[..., dtypes.ExpressionType] = lambda: dtypes.STRING_DTYPE
    output_schema: str | None = None

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        import pyarrow as pa
        if self.output_schema is None:
            output_fields = (pa.field("result", pa.string()),)
        else:
            from bigframes.operations import output_schemas
            output_fields = output_schemas.parse_sql_fields(self.output_schema)

        return pd.ArrowDtype(
            pa.struct(
                (
                    *output_fields,
                    pa.field("full_response", dtypes.JSON_ARROW_TYPE),
                    pa.field("status", pa.string()),
                )
            )
        )


def _ai_generate_bool_output_type(*input_types):
    import pyarrow as pa
    return pd.ArrowDtype(
        pa.struct(
            (
                pa.field("result", pa.bool_()),
                pa.field("full_response", dtypes.JSON_ARROW_TYPE),
                pa.field("status", pa.string()),
            )
        )
    )

AI_GENERATE_BOOL = GoogleSqlScalarOp(
    sql_name="AI.GENERATE_BOOL",
    args=(
        ArgSpec(arg_name="prompt"),
        ArgSpec(arg_name="connection_id", optional=True, const_only=True),
        ArgSpec(arg_name="endpoint", optional=True, const_only=True),
        ArgSpec(arg_name="request_type", optional=True, const_only=True),
        ArgSpec(arg_name="model_params", optional=True, const_only=True),
    ),
    signature=_ai_generate_bool_output_type,
)


def _ai_generate_int_output_type(*input_types):
    import pyarrow as pa
    return pd.ArrowDtype(
        pa.struct(
            (
                pa.field("result", pa.int64()),
                pa.field("full_response", dtypes.JSON_ARROW_TYPE),
                pa.field("status", pa.string()),
            )
        )
    )

AI_GENERATE_INT = GoogleSqlScalarOp(
    sql_name="AI.GENERATE_INT",
    args=(
        ArgSpec(arg_name="prompt"),
        ArgSpec(arg_name="connection_id", optional=True, const_only=True),
        ArgSpec(arg_name="endpoint", optional=True, const_only=True),
        ArgSpec(arg_name="request_type", optional=True, const_only=True),
        ArgSpec(arg_name="model_params", optional=True, const_only=True),
    ),
    signature=_ai_generate_int_output_type,
)


def _ai_generate_double_output_type(*input_types):
    import pyarrow as pa
    return pd.ArrowDtype(
        pa.struct(
            (
                pa.field("result", pa.float64()),
                pa.field("full_response", dtypes.JSON_ARROW_TYPE),
                pa.field("status", pa.string()),
            )
        )
    )

AI_GENERATE_DOUBLE = GoogleSqlScalarOp(
    sql_name="AI.GENERATE_DOUBLE",
    args=(
        ArgSpec(arg_name="prompt"),
        ArgSpec(arg_name="connection_id", optional=True, const_only=True),
        ArgSpec(arg_name="endpoint", optional=True, const_only=True),
        ArgSpec(arg_name="request_type", optional=True, const_only=True),
        ArgSpec(arg_name="model_params", optional=True, const_only=True),
    ),
    signature=_ai_generate_double_output_type,
)


def _ai_embed_output_type(*input_types):
    import pyarrow as pa
    return pd.ArrowDtype(
        pa.struct(
            (
                pa.field("result", pa.list_(pa.float64())),
                pa.field("status", pa.string()),
            )
        )
    )

AI_EMBED = GoogleSqlScalarOp(
    sql_name="AI.EMBED",
    args=(
        ArgSpec(arg_name="content"),
        ArgSpec(arg_name="endpoint", optional=True, const_only=True),
        ArgSpec(arg_name="model", optional=True, const_only=True),
        ArgSpec(arg_name="task_type", optional=True, const_only=True),
        ArgSpec(arg_name="title", optional=True, const_only=True),
        ArgSpec(arg_name="model_params", optional=True, const_only=True),
        ArgSpec(arg_name="connection_id", optional=True, const_only=True),
    ),
    signature=_ai_embed_output_type,
)


AI_IF = GoogleSqlScalarOp(
    sql_name="AI.IF",
    args=(
        ArgSpec(arg_name="prompt"),
        ArgSpec(arg_name="connection_id", optional=True, const_only=True),
        ArgSpec(arg_name="endpoint", optional=True, const_only=True),
        ArgSpec(arg_name="optimization_mode", optional=True, const_only=True),
        ArgSpec(arg_name="max_error_ratio", optional=True, const_only=True),
    ),
    signature=lambda *args: dtypes.BOOL_DTYPE,
)


AI_SCORE = GoogleSqlScalarOp(
    sql_name="AI.SCORE",
    args=(
        ArgSpec(arg_name="prompt"),
        ArgSpec(arg_name="connection_id", optional=True, const_only=True),
        ArgSpec(arg_name="endpoint", optional=True, const_only=True),
        ArgSpec(arg_name="max_error_ratio", optional=True, const_only=True),
    ),
    signature=lambda *args: dtypes.FLOAT_DTYPE,
)


AI_SIMILARITY = GoogleSqlScalarOp(
    sql_name="AI.SIMILARITY",
    args=(
        ArgSpec(arg_name="content1"),
        ArgSpec(arg_name="content2"),
        ArgSpec(arg_name="endpoint", optional=True, const_only=True),
        ArgSpec(arg_name="model", optional=True, const_only=True),
        ArgSpec(arg_name="model_params", optional=True, const_only=True),
        ArgSpec(arg_name="connection_id", optional=True, const_only=True),
    ),
    signature=lambda *args: dtypes.FLOAT_DTYPE,
)



def apply_op(
    op: ops.NaryOp,
    args: typing.Sequence[typing.Any] = (),
    kwargs: typing.Dict[str, typing.Any] = {},
) -> typing.Any:
    """Applies an operation to a mix of Series-like, literal, and other values, with necessary alignment."""
    import bigframes.core.align as align
    return align.apply_op(op, args=args, kwargs=kwargs)