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
from typing import cast, Optional, TYPE_CHECKING
import warnings

import ibis

if TYPE_CHECKING:
    from bigframes.session import Session

import bigframes_vendored.constants as constants
import google.api_core.exceptions
import google.api_core.retry
from google.cloud import bigquery
import google.iam.v1

import bigframes.core.compile.ibis_types
import bigframes.dtypes
import bigframes.functions.remote_function_template

from . import _remote_function_session as rf_session
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
    if not routine.return_type:
        raise ReturnTypeMissingError

    return _utils.IbisSignature(
        parameter_names=[arg.name for arg in routine.arguments],
        input_types=[
            bigframes.core.compile.ibis_types.ibis_type_from_type_kind(
                arg.data_type.type_kind
            )
            if arg.data_type
            else None
            for arg in routine.arguments
        ],
        output_type=bigframes.core.compile.ibis_types.ibis_type_from_type_kind(
            routine.return_type.type_kind
        ),
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
    remote_function_session = rf_session.RemoteFunctionSession()
    return remote_function_session.remote_function(*args, **kwargs)


remote_function.__doc__ = rf_session.RemoteFunctionSession.remote_function.__doc__


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
        raise ValueError(
            "Project and dataset must be provided, either directly or via session. "
            f"{constants.FEEDBACK_LINK}"
        )

    # Find the routine and get its arguments.
    try:
        routine = bigquery_client.get_routine(routine_ref)
    except google.api_core.exceptions.NotFound:
        raise ValueError(f"Unknown function '{routine_ref}'. {constants.FEEDBACK_LINK}")

    try:
        ibis_signature = ibis_signature_from_routine(routine)
    except ReturnTypeMissingError:
        raise ValueError(
            f"Function return type must be specified. {constants.FEEDBACK_LINK}"
        )
    except bigframes.core.compile.ibis_types.UnsupportedTypeError as e:
        raise ValueError(
            f"Type {e.type} not supported, supported types are {e.supported_types}. "
            f"{constants.FEEDBACK_LINK}"
        )

    # The name "args" conflicts with the Ibis operator, so we use
    # non-standard names for the arguments here.
    def func(*bigframes_args, **bigframes_kwargs):
        f"""Remote function {str(routine_ref)}."""
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

    node = ibis.udf.scalar.builtin(
        func,
        name=routine_ref.routine_id,
        catalog=routine_ref.project,
        database=routine_ref.dataset_id,
        signature=(ibis_signature.input_types, ibis_signature.output_type),
    )
    func.bigframes_remote_function = str(routine_ref)  # type: ignore

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
        warnings.warn(
            "The function has one or more missing input data types."
            f" BigQuery DataFrames will assume default data type {bigframes.dtypes.DEFAULT_DTYPE} for them.",
            category=bigframes.exceptions.UnknownDataTypeWarning,
        )
    func.input_dtypes = tuple(function_input_dtypes)  # type: ignore

    func.output_dtype = bigframes.core.compile.ibis_types.ibis_dtype_to_bigframes_dtype(  # type: ignore
        ibis_signature.output_type
    )
    func.is_row_processor = is_row_processor  # type: ignore
    func.ibis_node = node  # type: ignore
    return func
