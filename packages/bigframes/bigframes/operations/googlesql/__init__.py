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

import bigframes.operations as ops
from bigframes import dtypes


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
