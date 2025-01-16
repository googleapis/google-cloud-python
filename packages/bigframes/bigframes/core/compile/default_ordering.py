# Copyright 2024 Google LLC
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

"""
Private helpers for loading a BigQuery table as a BigQuery DataFrames DataFrame.
"""

from __future__ import annotations

from typing import cast, Sequence

import bigframes_vendored.ibis
import bigframes_vendored.ibis.expr.datatypes as ibis_dtypes
import bigframes_vendored.ibis.expr.operations as ibis_ops
import bigframes_vendored.ibis.expr.types as ibis_types

import bigframes.core.guid as guid


def _convert_to_nonnull_string(column: ibis_types.Value) -> ibis_types.StringValue:
    col_type = column.type()
    if (
        col_type.is_numeric()
        or col_type.is_boolean()
        or col_type.is_binary()
        or col_type.is_temporal()
    ):
        result = column.cast(ibis_dtypes.String(nullable=True))
    elif col_type.is_geospatial():
        result = cast(ibis_types.GeoSpatialColumn, column).as_text()
    elif col_type.is_string():
        result = column
    else:
        # TO_JSON_STRING works with all data types, but isn't the most efficient
        # Needed for JSON, STRUCT and ARRAY datatypes
        result = ibis_ops.ToJsonString(column).to_expr()  # type: ignore
    # Escape backslashes and use backslash as delineator
    escaped = cast(
        ibis_types.StringColumn,
        result.fill_null(ibis_types.literal(""))
        if hasattr(result, "fill_null")
        else result.fillna(""),
    ).replace(
        "\\",  # type: ignore
        "\\\\",  # type: ignore
    )
    return cast(ibis_types.StringColumn, bigframes_vendored.ibis.literal("\\")).concat(
        escaped
    )


def gen_row_key(
    columns: Sequence[ibis_types.Value],
) -> bigframes_vendored.ibis.Value:
    ordering_hash_part = guid.generate_guid("bigframes_ordering_")
    ordering_hash_part2 = guid.generate_guid("bigframes_ordering_")
    ordering_rand_part = guid.generate_guid("bigframes_ordering_")

    # All inputs into hash must be non-null or resulting hash will be null
    str_values = list(map(_convert_to_nonnull_string, columns))
    full_row_str = (
        str_values[0].concat(*str_values[1:]) if len(str_values) > 1 else str_values[0]
    )
    full_row_hash = (
        full_row_str.hash()
        .name(ordering_hash_part)
        .cast(ibis_dtypes.String(nullable=True))
    )
    # By modifying value slightly, we get another hash uncorrelated with the first
    full_row_hash_p2 = (
        (full_row_str + "_")
        .hash()
        .name(ordering_hash_part2)
        .cast(ibis_dtypes.String(nullable=True))
    )
    # Used to disambiguate between identical rows (which will have identical hash)
    random_value = (
        bigframes_vendored.ibis.random()
        .name(ordering_rand_part)
        .cast(ibis_dtypes.String(nullable=True))
    )

    return full_row_hash.concat(full_row_hash_p2, random_value)
