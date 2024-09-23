# Copyright (c) 2023 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from typing import Optional, cast

from google.cloud.bigquery import schema
import pyarrow
import pyarrow.types

_ARROW_SCALAR_IDS_TO_BQ = {
    # https://arrow.apache.org/docs/python/api/datatypes.html#type-classes
    pyarrow.bool_().id: "BOOLEAN",
    pyarrow.int8().id: "INTEGER",
    pyarrow.int16().id: "INTEGER",
    pyarrow.int32().id: "INTEGER",
    pyarrow.int64().id: "INTEGER",
    pyarrow.uint8().id: "INTEGER",
    pyarrow.uint16().id: "INTEGER",
    pyarrow.uint32().id: "INTEGER",
    pyarrow.uint64().id: "INTEGER",
    pyarrow.float16().id: "FLOAT",
    pyarrow.float32().id: "FLOAT",
    pyarrow.float64().id: "FLOAT",
    pyarrow.time32("ms").id: "TIME",
    pyarrow.time64("ns").id: "TIME",
    pyarrow.timestamp("ns").id: "TIMESTAMP",
    pyarrow.date32().id: "DATE",
    pyarrow.date64().id: "DATETIME",  # because millisecond resolution
    pyarrow.binary().id: "BYTES",
    pyarrow.string().id: "STRING",  # also alias for pyarrow.utf8()
    pyarrow.large_string().id: "STRING",
    # The exact decimal's scale and precision are not important, as only
    # the type ID matters, and it's the same for all decimal256 instances.
    pyarrow.decimal128(38, scale=9).id: "NUMERIC",
    pyarrow.decimal256(76, scale=38).id: "BIGNUMERIC",
}


def arrow_type_to_bigquery_field(name, type_) -> Optional[schema.SchemaField]:
    detected_type = _ARROW_SCALAR_IDS_TO_BQ.get(type_.id, None)
    if detected_type is not None:
        return schema.SchemaField(name, detected_type)

    if pyarrow.types.is_list(type_):
        return arrow_list_type_to_bigquery(name, type_)

    if pyarrow.types.is_struct(type_):
        inner_fields: list[pyarrow.Field] = []
        struct_type = cast(pyarrow.StructType, type_)
        for field_index in range(struct_type.num_fields):
            field = struct_type[field_index]
            inner_fields.append(arrow_type_to_bigquery_field(field.name, field.type))

        return schema.SchemaField(name, "RECORD", fields=inner_fields)

    return None


def arrow_list_type_to_bigquery(name, type_) -> Optional[schema.SchemaField]:
    inner_field = arrow_type_to_bigquery_field(name, type_.value_type)
    if inner_field is None:
        return None

    return schema.SchemaField(
        name, inner_field.field_type, mode="REPEATED", fields=inner_field.fields
    )
