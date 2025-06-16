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
import typing

import pandas as pd
import pyarrow as pa

from bigframes import dtypes
from bigframes.operations import base_ops


@dataclasses.dataclass(frozen=True)
class JSONExtract(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "json_extract"
    json_path: str

    def output_type(self, *input_types):
        input_type = input_types[0]
        if not dtypes.is_json_like(input_type):
            raise TypeError(
                "Input type must be a valid JSON object or JSON-formatted string type."
                + f" Received type: {input_type}"
            )
        return input_type


@dataclasses.dataclass(frozen=True)
class JSONQueryArray(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "json_query_array"
    json_path: str

    def output_type(self, *input_types):
        input_type = input_types[0]
        if not dtypes.is_json_like(input_type):
            raise TypeError(
                "Input type must be a valid JSON object or JSON-formatted string type."
                + f" Received type: {input_type}"
            )
        return pd.ArrowDtype(
            pa.list_(dtypes.bigframes_dtype_to_arrow_dtype(input_type))
        )


@dataclasses.dataclass(frozen=True)
class JSONExtractArray(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "json_extract_array"
    json_path: str

    def output_type(self, *input_types):
        input_type = input_types[0]
        if not dtypes.is_json_like(input_type):
            raise TypeError(
                "Input type must be a valid JSON object or JSON-formatted string type."
                + f" Received type: {input_type}"
            )
        return pd.ArrowDtype(
            pa.list_(dtypes.bigframes_dtype_to_arrow_dtype(input_type))
        )


@dataclasses.dataclass(frozen=True)
class JSONExtractStringArray(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "json_extract_string_array"
    json_path: str

    def output_type(self, *input_types):
        input_type = input_types[0]
        if not dtypes.is_json_like(input_type):
            raise TypeError(
                "Input type must be a valid JSON object or JSON-formatted string type."
                + f" Received type: {input_type}"
            )
        return pd.ArrowDtype(
            pa.list_(dtypes.bigframes_dtype_to_arrow_dtype(dtypes.STRING_DTYPE))
        )


@dataclasses.dataclass(frozen=True)
class ParseJSON(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "parse_json"

    def output_type(self, *input_types):
        input_type = input_types[0]
        if input_type != dtypes.STRING_DTYPE:
            raise TypeError(
                "Input type must be a valid JSON-formatted string type."
                + f" Received type: {input_type}"
            )
        return dtypes.JSON_DTYPE


@dataclasses.dataclass(frozen=True)
class ToJSONString(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "to_json_string"

    def output_type(self, *input_types):
        input_type = input_types[0]
        if not dtypes.is_json_like(input_type):
            raise TypeError(
                "Input type must be a valid JSON object or JSON-formatted string type."
                + f" Received type: {input_type}"
            )
        return dtypes.STRING_DTYPE


@dataclasses.dataclass(frozen=True)
class JSONSet(base_ops.BinaryOp):
    name: typing.ClassVar[str] = "json_set"
    json_path: str

    def output_type(self, *input_types):
        left_type = input_types[0]
        right_type = input_types[1]
        if not dtypes.is_json_like(left_type):
            raise TypeError(
                "Input type must be a valid JSON object or JSON-formatted string type."
                + f" Received type: {left_type}"
            )
        if not dtypes.is_json_encoding_type(right_type):
            raise TypeError(
                "The value to be assigned must be a type that can be encoded as JSON."
                + f"Received type: {right_type}"
            )

        return dtypes.JSON_DTYPE


@dataclasses.dataclass(frozen=True)
class JSONValue(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "json_value"
    json_path: str

    def output_type(self, *input_types):
        input_type = input_types[0]
        if not dtypes.is_json_like(input_type):
            raise TypeError(
                "Input type must be a valid JSON object or JSON-formatted string type."
                + f" Received type: {input_type}"
            )
        return dtypes.STRING_DTYPE


@dataclasses.dataclass(frozen=True)
class JSONValueArray(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "json_value_array"
    json_path: str

    def output_type(self, *input_types):
        input_type = input_types[0]
        if not dtypes.is_json_like(input_type):
            raise TypeError(
                "Input type must be a valid JSON object or JSON-formatted string type."
                + f" Received type: {input_type}"
            )
        return pd.ArrowDtype(
            pa.list_(dtypes.bigframes_dtype_to_arrow_dtype(dtypes.STRING_DTYPE))
        )


@dataclasses.dataclass(frozen=True)
class JSONQuery(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "json_query"
    json_path: str

    def output_type(self, *input_types):
        input_type = input_types[0]
        if not dtypes.is_json_like(input_type):
            raise TypeError(
                "Input type must be a valid JSON object or JSON-formatted string type."
                + f" Received type: {input_type}"
            )
        return input_type
