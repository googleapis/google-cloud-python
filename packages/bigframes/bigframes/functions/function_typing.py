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

from typing import Any, get_args, get_origin, Type

from google.cloud import bigquery

import bigframes.dtypes

# Input and output types supported by BigQuery DataFrames remote functions.
# TODO(shobs): Extend the support to all types supported by BQ remote functions
# https://cloud.google.com/bigquery/docs/remote-functions#limitations
RF_SUPPORTED_IO_PYTHON_TYPES = {
    bool: bigquery.StandardSqlDataType(type_kind=bigquery.StandardSqlTypeNames.BOOL),
    bytes: bigquery.StandardSqlDataType(type_kind=bigquery.StandardSqlTypeNames.BYTES),
    float: bigquery.StandardSqlDataType(
        type_kind=bigquery.StandardSqlTypeNames.FLOAT64
    ),
    int: bigquery.StandardSqlDataType(type_kind=bigquery.StandardSqlTypeNames.INT64),
    str: bigquery.StandardSqlDataType(type_kind=bigquery.StandardSqlTypeNames.STRING),
}

# Support array output types in BigQuery DataFrames remote functions even though
# it is not currently (2024-10-06) supported in BigQuery remote functions.
# https://cloud.google.com/bigquery/docs/remote-functions#limitations
# TODO(b/284515241): remove this special handling when BigQuery remote functions
# support array.
RF_SUPPORTED_ARRAY_OUTPUT_PYTHON_TYPES = {bool, float, int, str}

DEFAULT_RF_TYPE = RF_SUPPORTED_IO_PYTHON_TYPES[float]

RF_SUPPORTED_IO_BIGQUERY_TYPEKINDS = {
    "BOOLEAN",
    "BOOL",
    "BYTES",
    "FLOAT",
    "FLOAT64",
    "INT64",
    "INTEGER",
    "STRING",
    "ARRAY",
}


TIMEDELTA_DESCRIPTION_TAG = "#microseconds"


class UnsupportedTypeError(ValueError):
    def __init__(self, type_, supported_types):
        self.type = type_
        self.supported_types = supported_types
        super().__init__(
            f"'{type_}' is not one of the supported types {supported_types}"
        )


def sdk_type_from_python_type(
    t: type, allow_lists: bool = False
) -> bigquery.StandardSqlDataType:
    if (get_origin(t) is list) and allow_lists:
        return sdk_array_output_type_from_python_type(t)
    if t not in RF_SUPPORTED_IO_PYTHON_TYPES:
        raise UnsupportedTypeError(t, RF_SUPPORTED_IO_PYTHON_TYPES)
    return RF_SUPPORTED_IO_PYTHON_TYPES[t]


def sdk_array_output_type_from_python_type(t: type) -> bigquery.StandardSqlDataType:
    array_of = get_args(t)[0]
    if array_of not in RF_SUPPORTED_ARRAY_OUTPUT_PYTHON_TYPES:
        raise UnsupportedTypeError(array_of, RF_SUPPORTED_ARRAY_OUTPUT_PYTHON_TYPES)
    inner_type = RF_SUPPORTED_IO_PYTHON_TYPES[array_of]
    return bigquery.StandardSqlDataType(
        type_kind=bigquery.StandardSqlTypeNames.ARRAY, array_element_type=inner_type
    )


def sdk_type_to_bf_type(
    sdk_type: bigquery.StandardSqlDataType,
) -> bigframes.dtypes.Dtype:
    if sdk_type.array_element_type is not None:
        return bigframes.dtypes.list_type(
            sdk_type_to_bf_type(sdk_type.array_element_type)
        )
    if sdk_type.struct_type is not None:
        raise ValueError("Cannot handle struct types in remote function")
    assert sdk_type.type_kind is not None
    return bigframes.dtypes._TK_TO_BIGFRAMES[sdk_type.type_kind.name]


def sdk_type_to_py_type(
    sdk_type: bigquery.StandardSqlDataType,
) -> Type[Any]:
    if sdk_type.array_element_type is not None:
        return list[sdk_type_to_py_type(sdk_type.array_element_type)]  # type: ignore
    if sdk_type.struct_type is not None:
        raise ValueError("Cannot handle struct types in remote function")
    for key, value in RF_SUPPORTED_IO_PYTHON_TYPES.items():
        if value == sdk_type:
            return key
    raise ValueError(f"Cannot handle {sdk_type} in remote function")


def sdk_type_to_sql_string(
    sdk_type: bigquery.StandardSqlDataType,
) -> str:
    if sdk_type.array_element_type is not None:
        return f"ARRAY<{sdk_type_to_sql_string(sdk_type.array_element_type)}>"
    if sdk_type.struct_type is not None:
        raise ValueError("Cannot handle struct types in remote function")
    assert sdk_type.type_kind is not None
    return sdk_type.type_kind.name
