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

import inspect
import logging
import typing
from typing import cast, Optional, TYPE_CHECKING
import warnings

import bigframes_vendored.ibis.expr.datatypes as ibis_dtypes
import bigframes_vendored.ibis.expr.operations.udf as ibis_udf

if TYPE_CHECKING:
    from bigframes.session import Session

import google.api_core.exceptions
from google.cloud import bigquery

import bigframes.core.compile.ibis_types
import bigframes.dtypes
import bigframes.exceptions as bfe
import bigframes.formatting_helpers as bf_formatting

from . import _function_session as bff_session
from . import _utils

logger = logging.getLogger(__name__)


class UnsupportedTypeError(ValueError):
    def __init__(self, type_, supported_types):
        self.type = type_
        self.supported_types = supported_types


class ReturnTypeMissingError(ValueError):
    pass


# TODO: Move this to compile folder
def ibis_signature_from_routine(routine: bigquery.Routine) -> _utils.IbisSignature:
    if routine.return_type:
        ibis_output_type = (
            bigframes.core.compile.ibis_types.ibis_type_from_bigquery_type(
                routine.return_type
            )
        )
    else:
        raise ReturnTypeMissingError

    ibis_output_type_override: Optional[ibis_dtypes.DataType] = None
    if python_output_type := _utils.get_python_output_type_from_bigframes_metadata(
        routine.description
    ):
        if not isinstance(ibis_output_type, ibis_dtypes.String):
            raise bf_formatting.create_exception_with_feedback_link(
                TypeError,
                "An explicit output_type should be provided only for a BigQuery function with STRING output.",
            )
        if typing.get_origin(python_output_type) is list:
            ibis_output_type_override = bigframes.core.compile.ibis_types.ibis_array_output_type_from_python_type(
                cast(type, python_output_type)
            )
        else:
            raise bf_formatting.create_exception_with_feedback_link(
                TypeError,
                "Currently only list of a type is supported as python output type.",
            )

    return _utils.IbisSignature(
        parameter_names=[arg.name for arg in routine.arguments],
        input_types=[
            bigframes.core.compile.ibis_types.ibis_type_from_bigquery_type(
                arg.data_type
            )
            if arg.data_type
            else None
            for arg in routine.arguments
        ],
        output_type=ibis_output_type,
        output_type_override=ibis_output_type_override,
    )


class DatasetMissingError(ValueError):
    pass


def get_routine_reference(
    routine_ref_str: str, bigquery_client: bigquery.Client, session: Optional[Session]
) -> bigquery.RoutineReference:
    try:
        # Handle cases "<project_id>.<dataset_name>.<routine_name>" and
        # "<dataset_name>.<routine_name>".
        return bigquery.RoutineReference.from_string(
            routine_ref_str,
            default_project=bigquery_client.project,
        )
    except ValueError:
        # Handle case of "<routine_name>".
        if not session:
            raise DatasetMissingError

        dataset_ref = bigquery.DatasetReference(
            bigquery_client.project, session._anonymous_dataset.dataset_id
        )
        return dataset_ref.routine(routine_ref_str)


def remote_function(*args, **kwargs):
    function_session = bff_session.FunctionSession()
    return function_session.remote_function(*args, **kwargs)


remote_function.__doc__ = bff_session.FunctionSession.remote_function.__doc__


def udf(*args, **kwargs):
    function_session = bff_session.FunctionSession()
    return function_session.udf(*args, **kwargs)


udf.__doc__ = bff_session.FunctionSession.udf.__doc__


# TODO(b/399894805): Support managed function.
def read_gbq_function(
    function_name: str,
    *,
    session: Session,
    is_row_processor: bool = False,
):
    """
    Read an existing BigQuery function and prepare it for use in future queries.
    """
    bigquery_client = session.bqclient
    ibis_client = session.ibis_client

    try:
        routine_ref = get_routine_reference(function_name, bigquery_client, session)
    except DatasetMissingError:
        raise bf_formatting.create_exception_with_feedback_link(
            ValueError,
            "Project and dataset must be provided, either directly or via session.",
        )

    # Find the routine and get its arguments.
    try:
        routine = bigquery_client.get_routine(routine_ref)
    except google.api_core.exceptions.NotFound:
        raise bf_formatting.create_exception_with_feedback_link(
            ValueError, f"Unknown function '{routine_ref}'."
        )

    if is_row_processor and len(routine.arguments) > 1:
        raise bf_formatting.create_exception_with_feedback_link(
            ValueError,
            "A multi-input function cannot be a row processor. A row processor function "
            "takes in a single input representing the row.",
        )

    try:
        ibis_signature = ibis_signature_from_routine(routine)
    except ReturnTypeMissingError:
        raise bf_formatting.create_exception_with_feedback_link(
            ValueError, "Function return type must be specified."
        )
    except bigframes.core.compile.ibis_types.UnsupportedTypeError as e:
        raise bf_formatting.create_exception_with_feedback_link(
            ValueError,
            f"Type {e.type} not supported, supported types are {e.supported_types}.",
        )

    # The name "args" conflicts with the Ibis operator, so we use
    # non-standard names for the arguments here.
    def func(*bigframes_args, **bigframes_kwargs):
        f"""Bigframes function {str(routine_ref)}."""
        nonlocal node  # type: ignore

        expr = node(*bigframes_args, **bigframes_kwargs)  # type: ignore
        return ibis_client.execute(expr)

    func.__signature__ = inspect.signature(func).replace(  # type: ignore
        parameters=[
            # TODO(shobs): Find a better way to support functions with param
            # named "name". This causes an issue in the ibis compilation.
            inspect.Parameter(
                f"bigframes_{name}",
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            )
            for name in ibis_signature.parameter_names
        ]
    )

    # TODO: Move ibis logic to compiler step

    func.__name__ = routine_ref.routine_id

    node = ibis_udf.scalar.builtin(
        func,
        name=routine_ref.routine_id,
        catalog=routine_ref.project,
        database=routine_ref.dataset_id,
        signature=(ibis_signature.input_types, ibis_signature.output_type),
    )  # type: ignore
    func.bigframes_bigquery_function = str(routine_ref)  # type: ignore

    # We will keep the "bigframes_remote_function" attr for remote function.
    if hasattr(routine, "remote_function_options") and routine.remote_function_options:
        func.bigframes_remote_function = func.bigframes_bigquery_function  # type: ignore

    # set input bigframes data types
    has_unknown_dtypes = False
    function_input_dtypes = []
    for ibis_type in ibis_signature.input_types:
        input_dtype = cast(bigframes.dtypes.Dtype, bigframes.dtypes.DEFAULT_DTYPE)
        if ibis_type is None:
            has_unknown_dtypes = True
        else:
            input_dtype = (
                bigframes.core.compile.ibis_types.ibis_dtype_to_bigframes_dtype(
                    ibis_type
                )
            )
        function_input_dtypes.append(input_dtype)
    if has_unknown_dtypes:
        msg = bfe.format_message(
            "The function has one or more missing input data types. BigQuery DataFrames "
            f"will assume default data type {bigframes.dtypes.DEFAULT_DTYPE} for them."
        )
        warnings.warn(msg, category=bfe.UnknownDataTypeWarning)
    func.input_dtypes = tuple(function_input_dtypes)  # type: ignore

    func.output_dtype = bigframes.core.compile.ibis_types.ibis_dtype_to_bigframes_dtype(  # type: ignore
        ibis_signature.output_type_override
        if ibis_signature.output_type_override
        else ibis_signature.output_type
    )

    func.bigframes_bigquery_function_output_dtype = bigframes.core.compile.ibis_types.ibis_dtype_to_bigframes_dtype(ibis_signature.output_type)  # type: ignore

    func.is_row_processor = is_row_processor  # type: ignore
    func.ibis_node = node  # type: ignore
    return func
