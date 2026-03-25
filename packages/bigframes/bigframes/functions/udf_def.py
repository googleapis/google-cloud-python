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

import dataclasses
import inspect
from typing import cast, Optional
import warnings

from google.cloud import bigquery

import bigframes.dtypes
import bigframes.exceptions as bfe
import bigframes.formatting_helpers as bf_formatting
from bigframes.functions import function_typing


class ReturnTypeMissingError(ValueError):
    pass


@dataclasses.dataclass(frozen=True)
class UdfField:
    name: str = dataclasses.field()
    dtype: bigquery.StandardSqlDataType = dataclasses.field(hash=False, compare=False)

    @classmethod
    def from_sdk(cls, arg: bigquery.RoutineArgument) -> UdfField:
        assert arg.name is not None
        assert arg.data_type is not None
        return cls(arg.name, arg.data_type)


@dataclasses.dataclass(frozen=True)
class UdfSignature:
    input_types: tuple[UdfField, ...] = dataclasses.field()
    output_bq_type: bigquery.StandardSqlDataType = dataclasses.field(
        hash=False, compare=False
    )

    @property
    def bf_input_types(self) -> tuple[bigframes.dtypes.Dtype, ...]:
        return tuple(
            function_typing.sdk_type_to_bf_type(arg.dtype) for arg in self.input_types
        )

    @property
    def bf_output_type(self) -> bigframes.dtypes.Dtype:
        return function_typing.sdk_type_to_bf_type(self.output_bq_type)

    @property
    def py_input_types(self) -> tuple[type, ...]:
        return tuple(
            function_typing.sdk_type_to_py_type(arg.dtype) for arg in self.input_types
        )

    @property
    def py_output_type(self) -> type:
        return function_typing.sdk_type_to_py_type(self.output_bq_type)

    @property
    def sql_input_types(self) -> tuple[str, ...]:
        return tuple(
            function_typing.sdk_type_to_sql_string(arg.dtype)
            for arg in self.input_types
        )

    @property
    def sql_output_type(self) -> str:
        return function_typing.sdk_type_to_sql_string(self.output_bq_type)

    @classmethod
    def from_routine(cls, routine: bigquery.Routine) -> UdfSignature:
        if routine.return_type is None:
            raise ReturnTypeMissingError
        bq_return_type = cast(bigquery.StandardSqlDataType, routine.return_type)

        if (
            bq_return_type.type_kind is None
            or bq_return_type.type_kind
            not in function_typing.RF_SUPPORTED_IO_BIGQUERY_TYPEKINDS
        ):
            raise ValueError(
                f"Remote function must have one of the following supported output types: {function_typing.RF_SUPPORTED_IO_BIGQUERY_TYPEKINDS}"
            )

        udf_fields = []
        for argument in routine.arguments:
            if argument.data_type is None:
                msg = bfe.format_message(
                    "The function has one or more missing input data types. BigQuery DataFrames "
                    f"will assume default data type {function_typing.DEFAULT_RF_TYPE} for them."
                )
                warnings.warn(msg, category=bfe.UnknownDataTypeWarning)
                assert argument.name is not None
                udf_fields.append(
                    UdfField(argument.name, function_typing.DEFAULT_RF_TYPE)
                )
            else:
                udf_fields.append(UdfField.from_sdk(argument))

        return cls(
            input_types=tuple(udf_fields),
            output_bq_type=bq_return_type,
        )

    @classmethod
    def from_py_signature(cls, signature: inspect.Signature):
        input_types: list[UdfField] = []
        for parameter in signature.parameters.values():
            if parameter.annotation is inspect.Signature.empty:
                raise bf_formatting.create_exception_with_feedback_link(
                    ValueError,
                    "'input_types' was not set and parameter "
                    f"'{parameter.name}' is missing a type annotation. "
                    "Types are required to use @remote_function.",
                )
            bq_type = function_typing.sdk_type_from_python_type(parameter.annotation)
            input_types.append(UdfField(parameter.name, bq_type))

        if signature.return_annotation is inspect.Signature.empty:
            raise bf_formatting.create_exception_with_feedback_link(
                ValueError,
                "'output_type' was not set and function is missing a "
                "return type annotation. Types are required to use "
                "@remote_function.",
            )
        output_bq_type = function_typing.sdk_type_from_python_type(
            signature.return_annotation,
            allow_lists=True,
        )
        return cls(tuple(input_types), output_bq_type)


@dataclasses.dataclass(frozen=True)
class BigqueryUdf:
    routine_ref: bigquery.RoutineReference = dataclasses.field()
    signature: UdfSignature
    # Used to provide alternative interpretations of output bq type, eg interpret int as timestamp
    output_type_override: Optional[bigframes.dtypes.Dtype] = dataclasses.field(
        default=None
    )

    @property
    def bigframes_output_type(self) -> bigframes.dtypes.Dtype:
        return self.output_type_override or function_typing.sdk_type_to_bf_type(
            self.signature.output_bq_type
        )

    @classmethod
    def from_routine(cls, routine: bigquery.Routine) -> BigqueryUdf:
        signature = UdfSignature.from_routine(routine)

        if (
            signature.output_bq_type.type_kind is None
            or signature.output_bq_type.type_kind
            not in function_typing.RF_SUPPORTED_IO_BIGQUERY_TYPEKINDS
        ):
            raise ValueError(
                f"Remote function must have one of the following supported output types: {function_typing.RF_SUPPORTED_IO_BIGQUERY_TYPEKINDS}"
            )
        return cls(routine.reference, signature=signature)
