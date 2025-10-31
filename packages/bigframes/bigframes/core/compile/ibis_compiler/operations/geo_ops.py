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

from typing import cast

from bigframes_vendored.ibis.expr import types as ibis_types
import bigframes_vendored.ibis.expr.datatypes as ibis_dtypes
import bigframes_vendored.ibis.expr.operations.udf as ibis_udf

from bigframes.core.compile.ibis_compiler import scalar_op_compiler
from bigframes.operations import geo_ops as ops

register_unary_op = scalar_op_compiler.scalar_op_compiler.register_unary_op
register_binary_op = scalar_op_compiler.scalar_op_compiler.register_binary_op


# Geo Ops
@register_unary_op(ops.geo_area_op)
def geo_area_op_impl(x: ibis_types.Value):
    return cast(ibis_types.GeoSpatialValue, x).area()


@register_unary_op(ops.geo_st_astext_op)
def geo_st_astext_op_impl(x: ibis_types.Value):
    return cast(ibis_types.GeoSpatialValue, x).as_text()


@register_unary_op(ops.geo_st_boundary_op, pass_op=False)
def geo_st_boundary_op_impl(x: ibis_types.Value):
    return st_boundary(x)


@register_unary_op(ops.GeoStBufferOp, pass_op=True)
def geo_st_buffer_op_impl(x: ibis_types.Value, op: ops.GeoStBufferOp):
    return st_buffer(
        x,
        op.buffer_radius,
        op.num_seg_quarter_circle,
        op.use_spheroid,
    )


@register_unary_op(ops.geo_st_centroid_op, pass_op=False)
def geo_st_centroid_op_impl(x: ibis_types.Value):
    return cast(ibis_types.GeoSpatialValue, x).centroid()


@register_unary_op(ops.geo_st_convexhull_op, pass_op=False)
def geo_st_convexhull_op_impl(x: ibis_types.Value):
    return st_convexhull(x)


@register_binary_op(ops.geo_st_difference_op, pass_op=False)
def geo_st_difference_op_impl(x: ibis_types.Value, y: ibis_types.Value):
    return cast(ibis_types.GeoSpatialValue, x).difference(
        cast(ibis_types.GeoSpatialValue, y)
    )


@register_binary_op(ops.GeoStDistanceOp, pass_op=True)
def geo_st_distance_op_impl(
    x: ibis_types.Value, y: ibis_types.Value, op: ops.GeoStDistanceOp
):
    return st_distance(x, y, op.use_spheroid)


@register_unary_op(ops.geo_st_geogfromtext_op)
def geo_st_geogfromtext_op_impl(x: ibis_types.Value):
    # Ibis doesn't seem to provide a dedicated method to cast from string to geography,
    # so we use a BigQuery scalar function, st_geogfromtext(), directly.
    return st_geogfromtext(x)


@register_binary_op(ops.geo_st_geogpoint_op, pass_op=False)
def geo_st_geogpoint_op_impl(x: ibis_types.Value, y: ibis_types.Value):
    return cast(ibis_types.NumericValue, x).point(cast(ibis_types.NumericValue, y))


@register_binary_op(ops.geo_st_intersection_op, pass_op=False)
def geo_st_intersection_op_impl(x: ibis_types.Value, y: ibis_types.Value):
    return cast(ibis_types.GeoSpatialValue, x).intersection(
        cast(ibis_types.GeoSpatialValue, y)
    )


@register_unary_op(ops.geo_st_isclosed_op, pass_op=False)
def geo_st_isclosed_op_impl(x: ibis_types.Value):
    return st_isclosed(x)


@register_unary_op(ops.GeoStSimplifyOp, pass_op=True)
def st_simplify_op_impl(x: ibis_types.Value, op: ops.GeoStSimplifyOp):
    x = cast(ibis_types.GeoSpatialValue, x)
    return st_simplify(x, op.tolerance_meters)


@register_unary_op(ops.geo_x_op)
def geo_x_op_impl(x: ibis_types.Value):
    return cast(ibis_types.GeoSpatialValue, x).x()


@register_unary_op(ops.GeoStLengthOp, pass_op=True)
def geo_length_op_impl(x: ibis_types.Value, op: ops.GeoStLengthOp):
    # Call the st_length UDF defined in this file (or imported)
    return st_length(x, op.use_spheroid)


@register_unary_op(ops.geo_y_op)
def geo_y_op_impl(x: ibis_types.Value):
    return cast(ibis_types.GeoSpatialValue, x).y()


@ibis_udf.scalar.builtin
def st_convexhull(x: ibis_dtypes.geography) -> ibis_dtypes.geography:  # type: ignore
    """ST_CONVEXHULL"""
    ...


@ibis_udf.scalar.builtin
def st_geogfromtext(a: str) -> ibis_dtypes.geography:  # type: ignore
    """Convert string to geography."""


@ibis_udf.scalar.builtin
def st_boundary(a: ibis_dtypes.geography) -> ibis_dtypes.geography:  # type: ignore
    """Find the boundary of a geography."""


@ibis_udf.scalar.builtin
def st_buffer(
    geography: ibis_dtypes.geography,  # type: ignore
    buffer_radius: ibis_dtypes.Float64,
    num_seg_quarter_circle: ibis_dtypes.Float64,
    use_spheroid: ibis_dtypes.Boolean,
) -> ibis_dtypes.geography:  # type: ignore
    ...


@ibis_udf.scalar.builtin
def st_distance(a: ibis_dtypes.geography, b: ibis_dtypes.geography, use_spheroid: bool) -> ibis_dtypes.float:  # type: ignore
    """Convert string to geography."""


@ibis_udf.scalar.builtin
def st_length(geog: ibis_dtypes.geography, use_spheroid: bool) -> ibis_dtypes.float:  # type: ignore
    """ST_LENGTH BQ builtin. This body is never executed."""
    pass


@ibis_udf.scalar.builtin
def st_isclosed(a: ibis_dtypes.geography) -> ibis_dtypes.boolean:  # type: ignore
    """Checks if a geography is closed."""


@ibis_udf.scalar.builtin
def st_simplify(
    geography: ibis_dtypes.geography,  # type: ignore
    tolerance_meters: ibis_dtypes.float,  # type: ignore
) -> ibis_dtypes.geography:  # type: ignore
    ...
