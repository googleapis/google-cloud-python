# Copyright 2023 Google LLC
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

import typing

import bigframes_vendored.ibis

import bigframes.core.compile.compiled as compiled
import bigframes.core.expression as ex
import bigframes.core.guid
import bigframes.core.ordering


def explode_unordered(
    input: compiled.UnorderedIR,
    columns: typing.Sequence[ex.DerefOp],
    offsets_id: typing.Optional[str],
) -> compiled.UnorderedIR:
    table = input._to_ibis_expr()
    column_ids = tuple(ref.id.sql for ref in columns)

    # The offset array ensures null represents empty arrays after unnesting.
    offset_array_id = bigframes.core.guid.generate_guid("offset_array_")
    offset_array = bigframes_vendored.ibis.range(
        0,
        bigframes_vendored.ibis.greatest(
            1,  # We always want at least 1 element to fill in NULLs for empty arrays.
            bigframes_vendored.ibis.least(
                *[table[column_id].length() for column_id in column_ids]
            ),
        ),
        1,
    ).name(offset_array_id)
    table_w_offset_array = table.select(
        offset_array,
        *input._column_names,
    )

    unnest_offset_id = offsets_id or bigframes.core.guid.generate_guid("unnest_offset_")
    unnest_offset = (
        table_w_offset_array[offset_array_id].unnest().name(unnest_offset_id)
    )
    table_w_offset = table_w_offset_array.select(
        unnest_offset,
        *input._column_names,
    )

    output_cols = tuple(input.column_ids) + ((offsets_id,) if offsets_id else ())
    unnested_columns = [
        table_w_offset[column_id][table_w_offset[unnest_offset_id]].name(column_id)
        if column_id in column_ids
        else table_w_offset[column_id]
        for column_id in output_cols
    ]
    table_w_unnest = table_w_offset.select(*unnested_columns)

    columns = [table_w_unnest[column_name] for column_name in output_cols]
    return compiled.UnorderedIR(
        table_w_unnest,
        columns=columns,  # type: ignore
    )
