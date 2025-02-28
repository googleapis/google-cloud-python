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

from bigframes import dtypes
from bigframes.operations import base_ops
import bigframes.operations.type as op_typing

geo_area_op = base_ops.create_unary_op(
    name="geo_area",
    type_signature=op_typing.FixedOutputType(
        dtypes.is_geo_like, dtypes.FLOAT_DTYPE, description="geo-like"
    ),
)

geo_st_astext_op = base_ops.create_unary_op(
    name="geo_st_astext",
    type_signature=op_typing.FixedOutputType(
        dtypes.is_geo_like, dtypes.STRING_DTYPE, description="geo-like"
    ),
)

geo_st_boundary_op = base_ops.create_unary_op(
    name="geo_st_boundary",
    type_signature=op_typing.FixedOutputType(
        dtypes.is_geo_like, dtypes.GEO_DTYPE, description="geo-like"
    ),
)

geo_st_geogfromtext_op = base_ops.create_unary_op(
    name="geo_st_geogfromtext",
    type_signature=op_typing.FixedOutputType(
        dtypes.is_string_like, dtypes.GEO_DTYPE, description="string-like"
    ),
)


geo_st_geogpoint_op = base_ops.create_binary_op(
    name="geo_st_geogpoint", type_signature=op_typing.BinaryNumericGeo()
)

geo_x_op = base_ops.create_unary_op(
    name="geo_x",
    type_signature=op_typing.FixedOutputType(
        dtypes.is_geo_like, dtypes.FLOAT_DTYPE, description="geo-like"
    ),
)

geo_y_op = base_ops.create_unary_op(
    name="geo_y",
    type_signature=op_typing.FixedOutputType(
        dtypes.is_geo_like, dtypes.FLOAT_DTYPE, description="geo-like"
    ),
)
