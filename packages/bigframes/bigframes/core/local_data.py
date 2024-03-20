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

"""Methods that deal with local pandas/pyarrow dataframes."""

from __future__ import annotations

import pyarrow as pa

import bigframes.core.schema as schemata
import bigframes.dtypes


def arrow_schema_to_bigframes(arrow_schema: pa.Schema) -> schemata.ArraySchema:
    """Infer the corresponding bigframes schema given a pyarrow schema."""
    schema_items = tuple(
        schemata.SchemaItem(
            field.name,
            bigframes_type_for_arrow_type(field.type),
        )
        for field in arrow_schema
    )
    return schemata.ArraySchema(schema_items)


def adapt_pa_table(arrow_table: pa.Table) -> pa.Table:
    """Adapt a pyarrow table to one that can be handled by bigframes. Converts tz to UTC and unit to us for temporal types."""
    new_schema = pa.schema(
        [
            pa.field(field.name, arrow_type_replacements(field.type))
            for field in arrow_table.schema
        ]
    )
    return arrow_table.cast(new_schema)


def bigframes_type_for_arrow_type(pa_type: pa.DataType) -> bigframes.dtypes.Dtype:
    return bigframes.dtypes.ibis_dtype_to_bigframes_dtype(
        bigframes.dtypes.arrow_dtype_to_ibis_dtype(arrow_type_replacements(pa_type))
    )


def arrow_type_replacements(type: pa.DataType) -> pa.DataType:
    if pa.types.is_timestamp(type):
        # This is potentially lossy, but BigFrames doesn't support ns
        new_tz = "UTC" if (type.tz is not None) else None
        return pa.timestamp(unit="us", tz=new_tz)
    if pa.types.is_time64(type):
        # This is potentially lossy, but BigFrames doesn't support ns
        return pa.time64("us")
    else:
        return type
