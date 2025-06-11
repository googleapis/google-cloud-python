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

import dataclasses

from bigframes import dtypes
from bigframes.operations import base_ops
import bigframes.operations.type as op_typing

GeoAreaOp = base_ops.create_unary_op(
    name="geo_area",
    type_signature=op_typing.FixedOutputType(
        dtypes.is_geo_like, dtypes.FLOAT_DTYPE, description="geo-like"
    ),
)
geo_area_op = GeoAreaOp()

GeoStAstextOp = base_ops.create_unary_op(
    name="geo_st_astext",
    type_signature=op_typing.FixedOutputType(
        dtypes.is_geo_like, dtypes.STRING_DTYPE, description="geo-like"
    ),
)
geo_st_astext_op = GeoStAstextOp()

GeoStBoundaryOp = base_ops.create_unary_op(
    name="geo_st_boundary",
    type_signature=op_typing.FixedOutputType(
        dtypes.is_geo_like, dtypes.GEO_DTYPE, description="geo-like"
    ),
)
geo_st_boundary_op = GeoStBoundaryOp()

GeoStDifferenceOp = base_ops.create_binary_op(
    name="geo_st_difference", type_signature=op_typing.BinaryGeo()
)
geo_st_difference_op = GeoStDifferenceOp()

GeoStGeogfromtextOp = base_ops.create_unary_op(
    name="geo_st_geogfromtext",
    type_signature=op_typing.FixedOutputType(
        dtypes.is_string_like, dtypes.GEO_DTYPE, description="string-like"
    ),
)
geo_st_geogfromtext_op = GeoStGeogfromtextOp()

GeoStGeogpointOp = base_ops.create_binary_op(
    name="geo_st_geogpoint", type_signature=op_typing.BinaryNumericGeo()
)
geo_st_geogpoint_op = GeoStGeogpointOp()

GeoStIsclosedOp = base_ops.create_unary_op(
    name="geo_st_isclosed",
    type_signature=op_typing.FixedOutputType(
        dtypes.is_geo_like, dtypes.BOOL_DTYPE, description="geo-like"
    ),
)
geo_st_isclosed_op = GeoStIsclosedOp()

GeoXOp = base_ops.create_unary_op(
    name="geo_x",
    type_signature=op_typing.FixedOutputType(
        dtypes.is_geo_like, dtypes.FLOAT_DTYPE, description="geo-like"
    ),
)
geo_x_op = GeoXOp()

GeoYOp = base_ops.create_unary_op(
    name="geo_y",
    type_signature=op_typing.FixedOutputType(
        dtypes.is_geo_like, dtypes.FLOAT_DTYPE, description="geo-like"
    ),
)
geo_y_op = GeoYOp()

GeoStIntersectionOp = base_ops.create_binary_op(
    name="geo_st_intersection", type_signature=op_typing.BinaryGeo()
)
geo_st_intersection_op = GeoStIntersectionOp()


@dataclasses.dataclass(frozen=True)
class GeoStDistanceOp(base_ops.BinaryOp):
    name = "st_distance"
    use_spheroid: bool

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return dtypes.FLOAT_DTYPE


@dataclasses.dataclass(frozen=True)
class GeoStLengthOp(base_ops.UnaryOp):
    name = "geo_st_length"
    use_spheroid: bool = False

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        return dtypes.FLOAT_DTYPE
