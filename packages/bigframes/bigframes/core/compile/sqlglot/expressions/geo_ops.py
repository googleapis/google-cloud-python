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
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr
import bigframes.core.compile.sqlglot.scalar_compiler as scalar_compiler

register_unary_op = scalar_compiler.scalar_op_compiler.register_unary_op


@register_unary_op(ops.geo_area_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("ST_AREA", expr.expr)


@register_unary_op(ops.geo_st_astext_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("ST_ASTEXT", expr.expr)


@register_unary_op(ops.geo_st_boundary_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("ST_BOUNDARY", expr.expr)


@register_unary_op(ops.GeoStBufferOp, pass_op=True)
def _(expr: TypedExpr, op: ops.GeoStBufferOp) -> sge.Expression:
    return sge.func(
        "ST_BUFFER",
        expr.expr,
        sge.convert(op.buffer_radius),
        sge.convert(op.num_seg_quarter_circle),
        sge.convert(op.use_spheroid),
    )


@register_unary_op(ops.geo_st_centroid_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("ST_CENTROID", expr.expr)


@register_unary_op(ops.geo_st_convexhull_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("ST_CONVEXHULL", expr.expr)


@register_unary_op(ops.geo_st_geogfromtext_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("SAFE.ST_GEOGFROMTEXT", expr.expr)


@register_unary_op(ops.geo_st_isclosed_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("ST_ISCLOSED", expr.expr)


@register_unary_op(ops.GeoStLengthOp, pass_op=True)
def _(expr: TypedExpr, op: ops.GeoStLengthOp) -> sge.Expression:
    return sge.func("ST_LENGTH", expr.expr)


@register_unary_op(ops.GeoStRegionStatsOp, pass_op=True)
def _(
    geography: TypedExpr,
    op: ops.GeoStRegionStatsOp,
):
    args = [geography.expr, sge.convert(op.raster_id)]
    if op.band:
        args.append(sge.Kwarg(this="band", expression=sge.convert(op.band)))
    if op.include:
        args.append(sge.Kwarg(this="include", expression=sge.convert(op.include)))
    if op.options:
        args.append(
            sge.Kwarg(this="options", expression=sge.JSON(this=sge.convert(op.options)))
        )
    return sge.func("ST_REGIONSTATS", *args)


@register_unary_op(ops.GeoStSimplifyOp, pass_op=True)
def _(expr: TypedExpr, op: ops.GeoStSimplifyOp) -> sge.Expression:
    return sge.func(
        "ST_SIMPLIFY",
        expr.expr,
        sge.convert(op.tolerance_meters),
    )


@register_unary_op(ops.geo_x_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("SAFE.ST_X", expr.expr)


@register_unary_op(ops.geo_y_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("SAFE.ST_Y", expr.expr)
