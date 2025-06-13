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

import logging
from typing import Callable, cast, get_origin, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from bigframes.session import Session
    import bigframes.series

import google.api_core.exceptions
from google.cloud import bigquery

import bigframes.formatting_helpers as bf_formatting
from bigframes.functions import _function_session as bff_session
from bigframes.functions import _utils, function_typing, udf_def

logger = logging.getLogger(__name__)


class UnsupportedTypeError(ValueError):
    def __init__(self, type_, supported_types):
        self.type = type_
        self.supported_types = supported_types


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


def _try_import_routine(
    routine: bigquery.Routine, session: bigframes.Session
) -> BigqueryCallableRoutine:
    udf_def = _routine_as_udf_def(routine)
    override_type = _get_output_type_override(routine)
    is_remote = (
        hasattr(routine, "remote_function_options") and routine.remote_function_options
    )
    if override_type is not None:
        return BigqueryCallableRoutine(
            udf_def,
            session,
            post_routine=_utils._build_unnest_post_routine(override_type),
        )
    return BigqueryCallableRoutine(udf_def, session, is_managed=not is_remote)


def _try_import_row_routine(
    routine: bigquery.Routine, session: bigframes.Session
) -> BigqueryCallableRowRoutine:
    udf_def = _routine_as_udf_def(routine)
    override_type = _get_output_type_override(routine)
    is_remote = (
        hasattr(routine, "remote_function_options") and routine.remote_function_options
    )
    if override_type is not None:
        return BigqueryCallableRowRoutine(
            udf_def,
            session,
            post_routine=_utils._build_unnest_post_routine(override_type),
        )
    return BigqueryCallableRowRoutine(udf_def, session, is_managed=not is_remote)


def _routine_as_udf_def(routine: bigquery.Routine) -> udf_def.BigqueryUdf:
    try:
        return udf_def.BigqueryUdf.from_routine(routine)
    except udf_def.ReturnTypeMissingError:
        raise bf_formatting.create_exception_with_feedback_link(
            ValueError, "Function return type must be specified."
        )
    except function_typing.UnsupportedTypeError as e:
        raise bf_formatting.create_exception_with_feedback_link(
            ValueError,
            f"Type {e.type} not supported, supported types are {e.supported_types}.",
        )


def _get_output_type_override(routine: bigquery.Routine) -> Optional[type[list]]:
    if routine.description is not None and isinstance(routine.description, str):
        if python_output_type := _utils.get_python_output_type_from_bigframes_metadata(
            routine.description
        ):
            bq_return_type = cast(bigquery.StandardSqlDataType, routine.return_type)

            if bq_return_type is None or bq_return_type.type_kind != "STRING":
                raise bf_formatting.create_exception_with_feedback_link(
                    TypeError,
                    "An explicit output_type should be provided only for a BigQuery function with STRING output.",
                )
            if get_origin(python_output_type) is list:
                return python_output_type
            else:
                raise bf_formatting.create_exception_with_feedback_link(
                    TypeError,
                    "Currently only list of "
                    "a type is supported as python output type.",
                )

    return None


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

    if is_row_processor:
        return _try_import_row_routine(routine, session)
    else:
        return _try_import_routine(routine, session)


class BigqueryCallableRoutine:
    """
    A reference to a routine in the context of a session.

    Can be used both directly as a callable, or as an input to dataframe ops that take a callable.
    """

    def __init__(
        self,
        udf_def: udf_def.BigqueryUdf,
        session: bigframes.Session,
        *,
        local_func: Optional[Callable] = None,
        cloud_function_ref: Optional[str] = None,
        post_routine: Optional[
            Callable[[bigframes.series.Series], bigframes.series.Series]
        ] = None,
        is_managed: bool = False,
    ):
        self._udf_def = udf_def
        self._session = session
        self._post_routine = post_routine
        self._local_fun = local_func
        self._cloud_function = cloud_function_ref
        self._is_managed = is_managed

    def __call__(self, *args, **kwargs):
        if self._local_fun:
            return self._local_fun(*args, **kwargs)
        # avoid circular imports
        import bigframes.core.sql as bf_sql
        import bigframes.session._io.bigquery as bf_io_bigquery

        args_string = ", ".join(map(bf_sql.simple_literal, args))
        sql = f"SELECT `{str(self._udf_def.routine_ref)}`({args_string})"
        iter, job = bf_io_bigquery.start_query_with_client(self._session.bqclient, sql=sql, query_with_job=True, job_config=bigquery.QueryJobConfig())  # type: ignore
        return list(iter.to_arrow().to_pydict().values())[0][0]

    @property
    def bigframes_bigquery_function(self) -> str:
        return str(self._udf_def.routine_ref)

    @property
    def bigframes_remote_function(self):
        return None if self._is_managed else str(self._udf_def.routine_ref)

    @property
    def is_row_processor(self) -> bool:
        return False

    @property
    def udf_def(self) -> udf_def.BigqueryUdf:
        return self._udf_def

    @property
    def bigframes_cloud_function(self) -> Optional[str]:
        return self._cloud_function

    @property
    def input_dtypes(self):
        return self.udf_def.signature.bf_input_types

    @property
    def output_dtype(self):
        return self.udf_def.signature.bf_output_type

    @property
    def bigframes_bigquery_function_output_dtype(self):
        return self.output_dtype

    def _post_process_series(
        self, series: bigframes.series.Series
    ) -> bigframes.series.Series:
        if self._post_routine is not None:
            return self._post_routine(series)
        return series


class BigqueryCallableRowRoutine:
    """
    A reference to a routine in the context of a session.

    Can be used both directly as a callable, or as an input to dataframe ops that take a callable.
    """

    def __init__(
        self,
        udf_def: udf_def.BigqueryUdf,
        session: bigframes.Session,
        *,
        local_func: Optional[Callable] = None,
        cloud_function_ref: Optional[str] = None,
        post_routine: Optional[
            Callable[[bigframes.series.Series], bigframes.series.Series]
        ] = None,
        is_managed: bool = False,
    ):
        self._udf_def = udf_def
        self._session = session
        self._post_routine = post_routine
        self._local_fun = local_func
        self._cloud_function = cloud_function_ref
        self._is_managed = is_managed

    def __call__(self, *args, **kwargs):
        if self._local_fun:
            return self._local_fun(*args, **kwargs)
        # avoid circular imports
        import bigframes.core.sql as bf_sql
        import bigframes.session._io.bigquery as bf_io_bigquery

        args_string = ", ".join(map(bf_sql.simple_literal, args))
        sql = f"SELECT `{str(self._udf_def.routine_ref)}`({args_string})"
        iter, job = bf_io_bigquery.start_query_with_client(self._session.bqclient, sql=sql, query_with_job=True, job_config=bigquery.QueryJobConfig())  # type: ignore
        return list(iter.to_arrow().to_pydict().values())[0][0]

    @property
    def bigframes_bigquery_function(self) -> str:
        return str(self._udf_def.routine_ref)

    @property
    def bigframes_remote_function(self):
        return None if self._is_managed else str(self._udf_def.routine_ref)

    @property
    def is_row_processor(self) -> bool:
        return True

    @property
    def udf_def(self) -> udf_def.BigqueryUdf:
        return self._udf_def

    @property
    def bigframes_cloud_function(self) -> Optional[str]:
        return self._cloud_function

    @property
    def input_dtypes(self):
        return self.udf_def.signature.bf_input_types

    @property
    def output_dtype(self):
        return self.udf_def.signature.bf_output_type

    @property
    def bigframes_bigquery_function_output_dtype(self):
        return self.output_dtype

    def _post_process_series(
        self, series: bigframes.series.Series
    ) -> bigframes.series.Series:
        if self._post_routine is not None:
            return self._post_routine(series)
        return series
