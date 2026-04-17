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
import functools
import inspect
import io
import os
import textwrap
import warnings
from typing import Any, Optional, Sequence, Type, cast, get_args, get_origin

import cloudpickle
import google_crc32c
import pandas as pd
from google.cloud import bigquery

import bigframes.dtypes
import bigframes.exceptions as bfe
import bigframes.formatting_helpers as bf_formatting
from bigframes.functions import function_typing

# Protocol version 4 is available in python version 3.4 and above
# https://docs.python.org/3/library/pickle.html#data-stream-format
_pickle_protocol_version = 4


class ReturnTypeMissingError(ValueError):
    pass


@dataclasses.dataclass(frozen=True)
class UdfArg:
    name: str = dataclasses.field()
    dtype: DirectScalarType | RowSeriesInputFieldV1

    def __post_init__(self):
        assert isinstance(self.name, str)
        assert isinstance(self.dtype, (DirectScalarType, RowSeriesInputFieldV1))

    @classmethod
    def from_py_param(cls, param: inspect.Parameter) -> UdfArg:
        if param.annotation == pd.Series:
            return cls(param.name, RowSeriesInputFieldV1())
        return cls(param.name, DirectScalarType(param.annotation))

    @classmethod
    def from_sdk(cls, arg: bigquery.RoutineArgument) -> UdfArg:
        assert arg.name is not None

        if arg.data_type is None:
            msg = bfe.format_message(
                "The function has one or more missing input data types. BigQuery DataFrames "
                f"will assume default data type {function_typing.DEFAULT_RF_TYPE} for them."
            )
            warnings.warn(msg, category=bfe.UnknownDataTypeWarning)
            sdk_type = function_typing.DEFAULT_RF_TYPE
        else:
            sdk_type = arg.data_type
        return cls(arg.name, DirectScalarType.from_sdk_type(sdk_type))

    @property
    def py_type(self) -> type:
        return self.dtype.py_type

    @property
    def bf_type(self) -> bigframes.dtypes.Dtype:
        return self.dtype.bf_type

    @property
    def sql_type(self) -> str:
        return self.dtype.sql_type

    def stable_hash(self) -> bytes:
        hash_val = google_crc32c.Checksum()
        hash_val.update(self.name.encode())
        hash_val.update(self.dtype.stable_hash())
        return hash_val.digest()


@dataclasses.dataclass(frozen=True)
class DirectScalarType:
    """
    Represents a scalar value that is passed directly to the remote function.

    For these values, BigQuery handles the serialization and deserialization without any additional processing.
    """

    _py_type: type

    @property
    def py_type(self) -> type:
        return self._py_type

    @property
    def bf_type(self) -> bigframes.dtypes.Dtype:
        return function_typing.sdk_type_to_bf_type(
            function_typing.sdk_type_from_python_type(self._py_type)
        )

    @property
    def sql_type(self) -> str:
        sdk_type = function_typing.sdk_type_from_python_type(self._py_type)
        return function_typing.sdk_type_to_sql_string(sdk_type)

    def stable_hash(self) -> bytes:
        hash_val = google_crc32c.Checksum()
        hash_val.update(self._py_type.__name__.encode())
        return hash_val.digest()

    @classmethod
    def from_sdk_type(cls, sdk_type: bigquery.StandardSqlDataType) -> DirectScalarType:
        return cls(function_typing.sdk_type_to_py_type(sdk_type))

    @property
    def emulating_type(self) -> DirectScalarType:
        return self


@dataclasses.dataclass(frozen=True)
class VirtualListTypeV1:
    """
    Represents a list of scalar values that is emulated as a JSON array string in the remote function.

    Only works as output paramter right now where array -> string in function runtime, and then string -> array in SQL post-processing (defined in out_expr()).
    """

    _PROTOCOL_ID = "virtual_list_v1"

    inner_dtype: DirectScalarType

    @property
    def py_type(self) -> Type[list[Any]]:
        return list[self.inner_dtype.py_type]  # type: ignore

    @property
    def bf_type(self) -> bigframes.dtypes.Dtype:
        return bigframes.dtypes.list_type(self.inner_dtype.bf_type)

    @property
    def emulating_type(self) -> DirectScalarType:
        # Regardless of list inner type, string is used to emulate the list in the remote function.
        return DirectScalarType(str)

    def out_expr(
        self, expr: bigframes.core.expression.Expression
    ) -> bigframes.core.expression.Expression:
        # essentially we are undoing json.dumps in sql
        import bigframes.operations as ops

        as_str_list = ops.JSONValueArray(json_path="$").as_expr(expr)
        if self.inner_dtype.py_type is str:
            return as_str_list
        elif self.inner_dtype.py_type is bool:
            # hack so we don't need to make ArrayMap support general expressions yet
            # with b/495513753 we can map the equality operator instead
            return ops.ArrayMapOp(ops.IsInOp(values=("true",))).as_expr(as_str_list)
        else:
            return ops.ArrayMapOp(ops.AsTypeOp(self.inner_dtype.bf_type)).as_expr(
                as_str_list
            )

    @property
    def sql_type(self) -> str:
        return f"ARRAY<{self.inner_dtype.sql_type}>"

    def stable_hash(self) -> bytes:
        hash_val = google_crc32c.Checksum()
        hash_val.update(self._PROTOCOL_ID.encode())
        hash_val.update(self.inner_dtype.stable_hash())
        return hash_val.digest()


@dataclasses.dataclass(frozen=True)
class RowSeriesInputFieldV1:
    """
    Used to handle functions that logically take a series as an input, but handled via a string protocol in the remote function.

    For these, the serialization is dependent on index metadata, which must be provided by the caller.
    """

    _PROTOCOL_ID = "row_series_input_v1"

    @property
    def py_type(self) -> type:
        return pd.Series

    @property
    def bf_type(self) -> bigframes.dtypes.Dtype:
        # Code paths shouldn't hit this.
        raise ValueError("Series does not have a corresponding BigFrames type.")

    @property
    def sql_type(self) -> str:
        return "STRING"

    @property
    def emulating_type(self) -> DirectScalarType:
        # Regardless of list inner type, string is used to emulate the list in the remote function.
        return DirectScalarType(str)

    def stable_hash(self) -> bytes:
        hash_val = google_crc32c.Checksum()
        hash_val.update(self._PROTOCOL_ID.encode())
        return hash_val.digest()


@dataclasses.dataclass(frozen=True)
class UdfSignature:
    """
    Represents the mapping of input types from bigframes to sql to python and back.
    """

    inputs: tuple[UdfArg, ...] = dataclasses.field()
    output: DirectScalarType | VirtualListTypeV1

    def __post_init__(self):
        # Validate inputs and outputs are of the correct types.
        assert all(isinstance(arg, UdfArg) for arg in self.inputs)
        assert isinstance(self.output, (DirectScalarType, VirtualListTypeV1))

    def to_sql_input_signature(self) -> str:
        return ",".join(
            f"{field.name} {field.sql_type}"
            for field in self.with_devirtualize().inputs
        )

    @property
    def protocol_metadata(self) -> str | None:
        import bigframes.functions._utils

        if isinstance(self.output, VirtualListTypeV1):
            return bigframes.functions._utils.get_bigframes_metadata(
                python_output_type=self.output.py_type
            )
        return None

    @property
    def is_virtual(self) -> bool:
        dtypes = (self.output,) + tuple(arg.dtype for arg in self.inputs)
        return not all(isinstance(dtype, DirectScalarType) for dtype in dtypes)

    @property
    def is_row_processor(self) -> bool:
        return any(isinstance(arg.dtype, RowSeriesInputFieldV1) for arg in self.inputs)

    def with_devirtualize(self) -> UdfSignature:
        return UdfSignature(
            inputs=tuple(
                UdfArg(arg.name, arg.dtype.emulating_type) for arg in self.inputs
            ),
            output=self.output.emulating_type,
        )

    # TODO(493293086): Deprecate is_row_processor.
    @classmethod
    def from_routine(
        cls, routine: bigquery.Routine, is_row_processor: bool = False
    ) -> UdfSignature:
        import bigframes.functions._utils

        ## Handle return type
        if routine.return_type is None:
            raise ReturnTypeMissingError(
                f"Routine {routine} has no return type. Routine properties: {routine._properties}"
            )

        bq_return_type = cast(bigquery.StandardSqlDataType, routine.return_type)

        return_type: DirectScalarType | VirtualListTypeV1 = (
            DirectScalarType.from_sdk_type(bq_return_type)
        )
        if (
            python_output_type
            := bigframes.functions._utils.get_python_output_type_from_bigframes_metadata(
                routine.description
            )
        ):
            if bq_return_type.type_kind != "STRING":
                raise bf_formatting.create_exception_with_feedback_link(
                    TypeError,
                    "An explicit output_type should be provided only for a BigQuery function with STRING output.",
                )

            if get_origin(python_output_type) is list:
                inner_type = get_args(python_output_type)[0]
                return_type = VirtualListTypeV1(DirectScalarType(inner_type))
            else:
                raise bf_formatting.create_exception_with_feedback_link(
                    TypeError,
                    "Currently only list of a type is supported as python output type.",
                )

        ## Handle input types
        udf_fields = []

        for i, argument in enumerate(routine.arguments):
            if is_row_processor and i == 0:
                if argument.data_type.type_kind == "STRING":
                    udf_fields.append(UdfArg(argument.name, RowSeriesInputFieldV1()))
                else:
                    raise ValueError(
                        "Row processor functions must have STRING input type as first argument."
                    )
            udf_fields.append(UdfArg.from_sdk(argument))

        return cls(
            inputs=tuple(udf_fields),
            output=return_type,
        )

    @classmethod
    def from_py_signature(cls, signature: inspect.Signature):
        import bigframes.series

        input_types: list[UdfArg] = []
        for parameter in signature.parameters.values():
            if parameter.annotation is inspect.Signature.empty:
                raise bf_formatting.create_exception_with_feedback_link(
                    ValueError,
                    "'input_types' was not set and parameter "
                    f"'{parameter.name}' is missing a type annotation. "
                    "Types are required to use udfs.",
                )
            if parameter.annotation is bigframes.series.Series:
                raise TypeError(
                    "Argument type hint must be Pandas Series, not BigFrames Series."
                )

            input_types.append(UdfArg.from_py_param(parameter))

        if signature.return_annotation is inspect.Signature.empty:
            raise bf_formatting.create_exception_with_feedback_link(
                ValueError,
                "'output_type' was not set and function is missing a "
                "return type annotation. Types are required to use "
                "udfs.",
            )

        output_type = DirectScalarType(signature.return_annotation)
        return cls(tuple(input_types), output_type)

    def to_remote_function_compatible(self) -> UdfSignature:
        # need to virtualize list outputs
        if isinstance(self.output, DirectScalarType):
            if get_origin(self.output.py_type) is list:
                inner_py_type = get_args(self.output.py_type)[0]
                return UdfSignature(
                    inputs=self.inputs,
                    output=VirtualListTypeV1(DirectScalarType(inner_py_type)),
                )
        return self

    def stable_hash(self) -> bytes:
        hash_val = google_crc32c.Checksum()
        for input_type in self.inputs:
            hash_val.update(input_type.stable_hash())
        hash_val.update(self.output.stable_hash())
        return hash_val.digest()


@dataclasses.dataclass(frozen=True)
class BigqueryUdf:
    """
    Represents the information needed to call a BigQuery remote function - not a full spec.
    """

    routine_ref: bigquery.RoutineReference = dataclasses.field()
    signature: UdfSignature

    def with_devirtualize(self) -> BigqueryUdf:
        if not self.signature.is_virtual:
            return self
        return BigqueryUdf(
            routine_ref=self.routine_ref,
            signature=self.signature.with_devirtualize(),
        )

    @classmethod
    def from_routine(
        cls, routine: bigquery.Routine, is_row_processor: bool = False
    ) -> BigqueryUdf:
        signature = UdfSignature.from_routine(
            routine, is_row_processor=is_row_processor
        )
        return cls(routine.reference, signature=signature)


@dataclasses.dataclass(frozen=True)
class CodeDef:
    # Produced by cloudpickle, not compatible across python versions
    pickled_code: bytes
    # This is just the function itself, and does not include referenced objects/functions/modules
    function_source: Optional[str]
    entry_point: Optional[str]
    package_requirements: tuple[str, ...]

    @classmethod
    def from_func(cls, func, package_requirements: Sequence[str] | None = None):
        bytes_io = io.BytesIO()
        cloudpickle.dump(func, bytes_io, protocol=_pickle_protocol_version)
        source = None
        entry_point = None
        try:
            # dedent is hacky, but works for some nested functions
            source = textwrap.dedent(inspect.getsource(func))
            entry_point = func.__name__
        except OSError:
            pass
        return cls(
            pickled_code=bytes_io.getvalue(),
            function_source=source,
            entry_point=entry_point,
            package_requirements=tuple(package_requirements or []),
        )

    @functools.cache
    def stable_hash(self) -> bytes:
        # There is a known cell-id sensitivity of the cloudpickle serialization in
        # notebooks https://github.com/cloudpipe/cloudpickle/issues/538. Because of
        # this, if a cell contains a udf decorated with @remote_function, a unique
        # cloudpickle code is generated every time the cell is run, creating new
        # cloud artifacts every time. This is slow and wasteful.
        # A workaround of the same can be achieved by replacing the filename in the
        # code object to a static value
        # https://github.com/cloudpipe/cloudpickle/issues/120#issuecomment-338510661.
        #
        # To respect the user code/environment let's make this modification on a
        # copy of the udf, not on the original udf itself.
        def_copy = cloudpickle.loads(self.pickled_code)
        def_copy.__code__ = def_copy.__code__.replace(
            co_filename="bigframes_place_holder_filename"
        )

        normalized_pickled_code = cloudpickle.dumps(
            def_copy, protocol=_pickle_protocol_version
        )

        hash_val = google_crc32c.Checksum()
        hash_val.update(normalized_pickled_code)

        if self.package_requirements:
            for p in sorted(self.package_requirements):
                hash_val.update(p.encode())

        return hash_val.digest()

    def to_callable(self):
        """
        Reconstructs the python callable from the pickled code.

        Assumption: package_requirements match local environment
        """
        return cloudpickle.loads(self.pickled_code)


@dataclasses.dataclass(frozen=True)
class ManagedFunctionConfig:
    code: CodeDef
    signature: UdfSignature
    max_batching_rows: Optional[int]
    container_cpu: Optional[float]
    container_memory: Optional[str]
    bq_connection_id: Optional[str]
    # capture_refernces=True -> deploy as cloudpickle
    # capture_references=False -> deploy as source
    capture_references: bool = False

    def stable_hash(self) -> bytes:
        hash_val = google_crc32c.Checksum()
        hash_val.update(self.code.stable_hash())
        hash_val.update(self.signature.stable_hash())
        hash_val.update(str(self.max_batching_rows).encode())
        hash_val.update(str(self.container_cpu).encode())
        hash_val.update(str(self.container_memory).encode())
        hash_val.update(str(self.bq_connection_id).encode())
        hash_val.update(str(self.capture_references).encode())
        return hash_val.digest()


@dataclasses.dataclass(frozen=True)
class CloudRunFunctionConfig:
    code: CodeDef
    signature: UdfSignature
    timeout_seconds: int | None
    max_instance_count: int | None
    vpc_connector: str | None
    vpc_connector_egress_settings: str
    memory_mib: int | None
    cpus: float | None
    ingress_settings: str
    workers: int | None
    threads: int | None
    concurrency: int | None

    def stable_hash(self) -> bytes:
        hash_val = google_crc32c.Checksum()
        hash_val.update(self.code.stable_hash())
        hash_val.update(self.signature.stable_hash())
        hash_val.update(str(self.timeout_seconds).encode())
        hash_val.update(str(self.max_instance_count).encode())
        hash_val.update(str(self.vpc_connector).encode())
        hash_val.update(str(self.vpc_connector_egress_settings).encode())
        hash_val.update(str(self.memory_mib).encode())
        hash_val.update(str(self.cpus).encode())
        hash_val.update(str(self.ingress_settings).encode())
        hash_val.update(str(self.workers).encode())
        hash_val.update(str(self.threads).encode())
        hash_val.update(str(self.concurrency).encode())
        return hash_val.digest()


@dataclasses.dataclass(frozen=True)
class RemoteFunctionConfig:
    """
    Represents the information needed to create a BigQuery remote function.
    """

    endpoint: str
    signature: UdfSignature
    connection_id: str
    max_batching_rows: int
    bq_metadata: str | None = None

    @classmethod
    def from_bq_routine(cls, routine: bigquery.Routine) -> RemoteFunctionConfig:
        return cls(
            endpoint=routine.remote_function_options.endpoint,
            connection_id=os.path.basename(routine.remote_function_options.connection),
            signature=UdfSignature.from_routine(routine),
            max_batching_rows=routine.remote_function_options.max_batching_rows,
            bq_metadata=routine.description,
        )

    def stable_hash(self) -> bytes:
        hash_val = google_crc32c.Checksum()
        hash_val.update(self.endpoint.encode())
        hash_val.update(self.signature.stable_hash())
        hash_val.update(self.connection_id.encode())
        hash_val.update(str(self.max_batching_rows).encode())
        hash_val.update(str(self.bq_metadata).encode())
        return hash_val.digest()
