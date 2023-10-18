# Original: https://github.com/googleapis/python-bigquery/blob/main/google/cloud/bigquery/_pandas_helpers.py
# Copyright 2019 Google LLC
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

"""Shared helper functions for connecting BigQuery and pandas."""

import warnings

import google.cloud.bigquery.schema as schema
import pyarrow


def pyarrow_datetime():
    return pyarrow.timestamp("us", tz=None)


def pyarrow_numeric():
    return pyarrow.decimal128(38, 9)


def pyarrow_bignumeric():
    # 77th digit is partial.
    # https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#decimal_types
    return pyarrow.decimal256(76, 38)


def pyarrow_time():
    return pyarrow.time64("us")


def pyarrow_timestamp():
    return pyarrow.timestamp("us", tz="UTC")


# This dictionary is duplicated in bigquery_storage/test/unite/test_reader.py
# When modifying it be sure to update it there as well.
BQ_TO_ARROW_SCALARS = {
    "BOOL": pyarrow.bool_,
    "BOOLEAN": pyarrow.bool_,
    "BYTES": pyarrow.binary,
    "DATE": pyarrow.date32,
    "DATETIME": pyarrow_datetime,
    "FLOAT": pyarrow.float64,
    "FLOAT64": pyarrow.float64,
    "GEOGRAPHY": pyarrow.string,
    "INT64": pyarrow.int64,
    "INTEGER": pyarrow.int64,
    "NUMERIC": pyarrow_numeric,
    "STRING": pyarrow.string,
    "TIME": pyarrow_time,
    "TIMESTAMP": pyarrow_timestamp,
    "BIGNUMERIC": pyarrow_bignumeric,
}
ARROW_SCALAR_IDS_TO_BQ = {
    # https://arrow.apache.org/docs/python/api/datatypes.html#type-classes
    pyarrow.bool_().id: "BOOL",
    pyarrow.int8().id: "INT64",
    pyarrow.int16().id: "INT64",
    pyarrow.int32().id: "INT64",
    pyarrow.int64().id: "INT64",
    pyarrow.uint8().id: "INT64",
    pyarrow.uint16().id: "INT64",
    pyarrow.uint32().id: "INT64",
    pyarrow.uint64().id: "INT64",
    pyarrow.float16().id: "FLOAT64",
    pyarrow.float32().id: "FLOAT64",
    pyarrow.float64().id: "FLOAT64",
    pyarrow.time32("ms").id: "TIME",
    pyarrow.time64("ns").id: "TIME",
    pyarrow.timestamp("ns").id: "TIMESTAMP",
    pyarrow.date32().id: "DATE",
    pyarrow.date64().id: "DATETIME",  # because millisecond resolution
    pyarrow.binary().id: "BYTES",
    pyarrow.string().id: "STRING",  # also alias for pyarrow.utf8()
    # The exact scale and precision don't matter. Only the type ID matters,
    # and it's the same for all decimal128/decimal256 instances.
    pyarrow.decimal128(38, scale=9).id: "NUMERIC",
    pyarrow.decimal256(76, scale=38).id: "BIGNUMERIC",
}


BQ_FIELD_TYPE_TO_ARROW_FIELD_METADATA = {
    "GEOGRAPHY": {
        b"ARROW:extension:name": b"google:sqlType:geography",
        b"ARROW:extension:metadata": b'{"encoding": "WKT"}',
    },
    "DATETIME": {b"ARROW:extension:name": b"google:sqlType:datetime"},
}


def bq_to_arrow_struct_data_type(field):
    arrow_fields = []
    for subfield in field.fields:
        arrow_subfield = bq_to_arrow_field(subfield)
        if arrow_subfield:
            arrow_fields.append(arrow_subfield)
        else:
            # Could not determine a subfield type. Fallback to type
            # inference.
            return None
    return pyarrow.struct(arrow_fields)


def bq_to_arrow_data_type(field):
    """Return the Arrow data type, corresponding to a given BigQuery column.

    Returns:
        None: if default Arrow type inspection should be used.
    """
    if field.mode is not None and field.mode.upper() == "REPEATED":
        inner_type = bq_to_arrow_data_type(
            schema.SchemaField(field.name, field.field_type, fields=field.fields)
        )
        if inner_type:
            return pyarrow.list_(inner_type)
        return None

    field_type_upper = field.field_type.upper() if field.field_type else ""
    if field_type_upper in schema._STRUCT_TYPES:
        return bq_to_arrow_struct_data_type(field)

    data_type_constructor = BQ_TO_ARROW_SCALARS.get(field_type_upper)
    if data_type_constructor is None:
        return None
    return data_type_constructor()


def bq_to_arrow_field(bq_field, array_type=None):
    """Return the Arrow field, corresponding to a given BigQuery column.

    Returns:
        None: if the Arrow type cannot be determined.
    """
    arrow_type = bq_to_arrow_data_type(bq_field)
    if arrow_type is not None:
        if array_type is not None:
            arrow_type = array_type  # For GEOGRAPHY, at least initially
        is_nullable = bq_field.mode.upper() == "NULLABLE"
        metadata = BQ_FIELD_TYPE_TO_ARROW_FIELD_METADATA.get(
            bq_field.field_type.upper() if bq_field.field_type else ""
        )
        return pyarrow.field(
            bq_field.name, arrow_type, nullable=is_nullable, metadata=metadata
        )

    warnings.warn("Unable to determine type for field '{}'.".format(bq_field.name))
    return None
