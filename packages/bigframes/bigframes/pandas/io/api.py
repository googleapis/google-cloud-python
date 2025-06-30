# Copyright 2024 Google LLC
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

import functools
import inspect
import threading
import typing
from typing import (
    Any,
    Callable,
    Dict,
    IO,
    Iterable,
    Literal,
    MutableSequence,
    Optional,
    overload,
    Sequence,
    Tuple,
    Union,
)

import bigframes_vendored.constants as constants
import bigframes_vendored.pandas.io.gbq as vendored_pandas_gbq
from google.cloud import bigquery
import numpy
import pandas
from pandas._typing import (
    CompressionOptions,
    FilePath,
    ReadPickleBuffer,
    StorageOptions,
)
import pyarrow as pa

import bigframes._config as config
import bigframes.core.global_session as global_session
import bigframes.core.indexes
import bigframes.dataframe
import bigframes.enums
import bigframes.series
import bigframes.session
from bigframes.session import dry_runs
import bigframes.session._io.bigquery
import bigframes.session.clients

# Note: the following methods are duplicated from Session. This duplication
# enables the following:
#
# 1. Static type checking knows the argument and return types, which is
#    difficult to do with decorators. Aside: When we require Python 3.10, we
#    can use Concatenate for generic typing in decorators. See:
#    https://stackoverflow.com/a/68290080/101923
# 2. docstrings get processed by static processing tools, such as VS Code's
#    autocomplete.
# 3. Positional arguments function as expected. If we were to pull in the
#    methods directly from Session, a Session object would need to be the first
#    argument, even if we allow a default value.
# 4. Allows to set BigQuery options for the BigFrames session based on the
#    method and its arguments.


def read_arrow(pa_table: pa.Table) -> bigframes.dataframe.DataFrame:
    """Load a PyArrow Table to a BigQuery DataFrames DataFrame.

    Args:
        pa_table (pyarrow.Table):
            PyArrow table to load data from.

    Returns:
        bigframes.dataframe.DataFrame:
            A new DataFrame representing the data from the PyArrow table.
    """
    session = global_session.get_global_session()
    return session.read_arrow(pa_table=pa_table)


def read_csv(
    filepath_or_buffer: str | IO["bytes"],
    *,
    sep: Optional[str] = ",",
    header: Optional[int] = 0,
    names: Optional[
        Union[MutableSequence[Any], numpy.ndarray[Any, Any], Tuple[Any, ...], range]
    ] = None,
    index_col: Optional[
        Union[
            int,
            str,
            Sequence[Union[str, int]],
            bigframes.enums.DefaultIndexKind,
            Literal[False],
        ]
    ] = None,
    usecols: Optional[
        Union[
            MutableSequence[str],
            Tuple[str, ...],
            Sequence[int],
            pandas.Series,
            pandas.Index,
            numpy.ndarray[Any, Any],
            Callable[[Any], bool],
        ]
    ] = None,
    dtype: Optional[Dict] = None,
    engine: Optional[
        Literal["c", "python", "pyarrow", "python-fwf", "bigquery"]
    ] = None,
    encoding: Optional[str] = None,
    write_engine: constants.WriteEngineType = "default",
    **kwargs,
) -> bigframes.dataframe.DataFrame:
    return global_session.with_default_session(
        bigframes.session.Session.read_csv,
        filepath_or_buffer=filepath_or_buffer,
        sep=sep,
        header=header,
        names=names,
        index_col=index_col,
        usecols=usecols,
        dtype=dtype,
        engine=engine,
        encoding=encoding,
        write_engine=write_engine,
        **kwargs,
    )


read_csv.__doc__ = inspect.getdoc(bigframes.session.Session.read_csv)


def read_json(
    path_or_buf: str | IO["bytes"],
    *,
    orient: Literal[
        "split", "records", "index", "columns", "values", "table"
    ] = "columns",
    dtype: Optional[Dict] = None,
    encoding: Optional[str] = None,
    lines: bool = False,
    engine: Literal["ujson", "pyarrow", "bigquery"] = "ujson",
    write_engine: constants.WriteEngineType = "default",
    **kwargs,
) -> bigframes.dataframe.DataFrame:
    return global_session.with_default_session(
        bigframes.session.Session.read_json,
        path_or_buf=path_or_buf,
        orient=orient,
        dtype=dtype,
        encoding=encoding,
        lines=lines,
        engine=engine,
        write_engine=write_engine,
        **kwargs,
    )


read_json.__doc__ = inspect.getdoc(bigframes.session.Session.read_json)


@overload
def read_gbq(  # type: ignore[overload-overlap]
    query_or_table: str,
    *,
    index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = ...,
    columns: Iterable[str] = ...,
    configuration: Optional[Dict] = ...,
    max_results: Optional[int] = ...,
    filters: vendored_pandas_gbq.FiltersType = ...,
    use_cache: Optional[bool] = ...,
    col_order: Iterable[str] = ...,
    dry_run: Literal[False] = ...,
) -> bigframes.dataframe.DataFrame:
    ...


@overload
def read_gbq(
    query_or_table: str,
    *,
    index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = ...,
    columns: Iterable[str] = ...,
    configuration: Optional[Dict] = ...,
    max_results: Optional[int] = ...,
    filters: vendored_pandas_gbq.FiltersType = ...,
    use_cache: Optional[bool] = ...,
    col_order: Iterable[str] = ...,
    dry_run: Literal[True] = ...,
) -> pandas.Series:
    ...


def read_gbq(
    query_or_table: str,
    *,
    index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = (),
    columns: Iterable[str] = (),
    configuration: Optional[Dict] = None,
    max_results: Optional[int] = None,
    filters: vendored_pandas_gbq.FiltersType = (),
    use_cache: Optional[bool] = None,
    col_order: Iterable[str] = (),
    dry_run: bool = False,
) -> bigframes.dataframe.DataFrame | pandas.Series:
    _set_default_session_location_if_possible(query_or_table)
    return global_session.with_default_session(
        bigframes.session.Session.read_gbq,
        query_or_table,
        index_col=index_col,
        columns=columns,
        configuration=configuration,
        max_results=max_results,
        filters=filters,
        use_cache=use_cache,
        col_order=col_order,
        dry_run=dry_run,
    )


read_gbq.__doc__ = inspect.getdoc(bigframes.session.Session.read_gbq)


def _run_read_gbq_colab_sessionless_dry_run(
    query: str,
    *,
    pyformat_args: Dict[str, Any],
) -> pandas.Series:
    """Run a dry_run without a session."""

    query_formatted = bigframes.core.pyformat.pyformat(
        query,
        pyformat_args=pyformat_args,
        dry_run=True,
    )
    bqclient = _get_bqclient()
    job = _dry_run(query_formatted, bqclient)
    return dry_runs.get_query_stats_with_inferred_dtypes(job, (), ())


def _try_read_gbq_colab_sessionless_dry_run(
    query: str,
    *,
    pyformat_args: Dict[str, Any],
) -> Optional[pandas.Series]:
    """Run a dry_run without a session, only if the session hasn't yet started."""

    global _default_location_lock

    # Avoid creating a session just for dry run. We don't want to bind to a
    # location too early. This is especially important if the query only refers
    # to local data and not any BigQuery tables.
    with _default_location_lock:
        if not config.options.bigquery._session_started:
            return _run_read_gbq_colab_sessionless_dry_run(
                query, pyformat_args=pyformat_args
            )

    # Explicitly return None to indicate that we didn't run the dry run query.
    return None


@overload
def _read_gbq_colab(  # type: ignore[overload-overlap]
    query_or_table: str,
    *,
    pyformat_args: Optional[Dict[str, Any]] = ...,
    dry_run: Literal[False] = ...,
) -> bigframes.dataframe.DataFrame:
    ...


@overload
def _read_gbq_colab(
    query_or_table: str,
    *,
    pyformat_args: Optional[Dict[str, Any]] = ...,
    dry_run: Literal[True] = ...,
) -> pandas.Series:
    ...


def _read_gbq_colab(
    query_or_table: str,
    *,
    pyformat_args: Optional[Dict[str, Any]] = None,
    dry_run: bool = False,
) -> bigframes.dataframe.DataFrame | pandas.Series:
    """A Colab-specific version of read_gbq.

    Calls `_set_default_session_location_if_possible` and then delegates
    to `bigframes.session.Session._read_gbq_colab`.

    Args:
        query_or_table (str):
            SQL query or table ID (table ID not yet supported).
        pyformat_args (Optional[Dict[str, Any]]):
            Parameters to format into the query string.
        dry_run (bool):
            If True, estimates the query results size without returning data.
            The return will be a pandas Series with query metadata.

    Returns:
        Union[bigframes.dataframe.DataFrame, pandas.Series]:
            A BigQuery DataFrame if `dry_run` is False, otherwise a pandas Series.
    """
    if pyformat_args is None:
        pyformat_args = {}

    # Only try to set the global location if it's not a dry run. We don't want
    # to bind to a location too early. This is especially important if the query
    # only refers to local data and not any BigQuery tables.
    if dry_run:
        result = _try_read_gbq_colab_sessionless_dry_run(
            query_or_table, pyformat_args=pyformat_args
        )

        if result is not None:
            return result

        # If we made it this far, we must have a session that has already
        # started. That means we can safely call the "real" _read_gbq_colab,
        # which generates slightly nicer SQL.
    else:
        # Delay formatting the query with the special "session-less" logic. This
        # avoids doing unnecessary work if the session already has a location or has
        # already started.
        create_query = functools.partial(
            bigframes.core.pyformat.pyformat,
            query_or_table,
            pyformat_args=pyformat_args,
            dry_run=True,
        )
        _set_default_session_location_if_possible_deferred_query(create_query)

    return global_session.with_default_session(
        bigframes.session.Session._read_gbq_colab,
        query_or_table,
        pyformat_args=pyformat_args,
        dry_run=dry_run,
    )


def read_gbq_model(model_name: str):
    return global_session.with_default_session(
        bigframes.session.Session.read_gbq_model,
        model_name,
    )


read_gbq_model.__doc__ = inspect.getdoc(bigframes.session.Session.read_gbq_model)


def read_gbq_object_table(
    object_table: str, *, name: Optional[str] = None
) -> bigframes.dataframe.DataFrame:
    return global_session.with_default_session(
        bigframes.session.Session.read_gbq_object_table,
        object_table,
        name=name,
    )


read_gbq_object_table.__doc__ = inspect.getdoc(
    bigframes.session.Session.read_gbq_object_table
)


@overload
def read_gbq_query(  # type: ignore[overload-overlap]
    query: str,
    *,
    index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = ...,
    columns: Iterable[str] = ...,
    configuration: Optional[Dict] = ...,
    max_results: Optional[int] = ...,
    use_cache: Optional[bool] = ...,
    col_order: Iterable[str] = ...,
    filters: vendored_pandas_gbq.FiltersType = ...,
    dry_run: Literal[False] = ...,
) -> bigframes.dataframe.DataFrame:
    ...


@overload
def read_gbq_query(
    query: str,
    *,
    index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = ...,
    columns: Iterable[str] = ...,
    configuration: Optional[Dict] = ...,
    max_results: Optional[int] = ...,
    use_cache: Optional[bool] = ...,
    col_order: Iterable[str] = ...,
    filters: vendored_pandas_gbq.FiltersType = ...,
    dry_run: Literal[True] = ...,
) -> pandas.Series:
    ...


def read_gbq_query(
    query: str,
    *,
    index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = (),
    columns: Iterable[str] = (),
    configuration: Optional[Dict] = None,
    max_results: Optional[int] = None,
    use_cache: Optional[bool] = None,
    col_order: Iterable[str] = (),
    filters: vendored_pandas_gbq.FiltersType = (),
    dry_run: bool = False,
) -> bigframes.dataframe.DataFrame | pandas.Series:
    _set_default_session_location_if_possible(query)
    return global_session.with_default_session(
        bigframes.session.Session.read_gbq_query,
        query,
        index_col=index_col,
        columns=columns,
        configuration=configuration,
        max_results=max_results,
        use_cache=use_cache,
        col_order=col_order,
        filters=filters,
        dry_run=dry_run,
    )


read_gbq_query.__doc__ = inspect.getdoc(bigframes.session.Session.read_gbq_query)


@overload
def read_gbq_table(  # type: ignore[overload-overlap]
    query: str,
    *,
    index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = ...,
    columns: Iterable[str] = ...,
    max_results: Optional[int] = ...,
    filters: vendored_pandas_gbq.FiltersType = ...,
    use_cache: bool = ...,
    col_order: Iterable[str] = ...,
    dry_run: Literal[False] = ...,
) -> bigframes.dataframe.DataFrame:
    ...


@overload
def read_gbq_table(
    query: str,
    *,
    index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = ...,
    columns: Iterable[str] = ...,
    max_results: Optional[int] = ...,
    filters: vendored_pandas_gbq.FiltersType = ...,
    use_cache: bool = ...,
    col_order: Iterable[str] = ...,
    dry_run: Literal[True] = ...,
) -> pandas.Series:
    ...


def read_gbq_table(
    query: str,
    *,
    index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = (),
    columns: Iterable[str] = (),
    max_results: Optional[int] = None,
    filters: vendored_pandas_gbq.FiltersType = (),
    use_cache: bool = True,
    col_order: Iterable[str] = (),
    dry_run: bool = False,
) -> bigframes.dataframe.DataFrame | pandas.Series:
    _set_default_session_location_if_possible(query)
    return global_session.with_default_session(
        bigframes.session.Session.read_gbq_table,
        query,
        index_col=index_col,
        columns=columns,
        max_results=max_results,
        filters=filters,
        use_cache=use_cache,
        col_order=col_order,
        dry_run=dry_run,
    )


read_gbq_table.__doc__ = inspect.getdoc(bigframes.session.Session.read_gbq_table)


@typing.overload
def read_pandas(
    pandas_dataframe: pandas.DataFrame,
    *,
    write_engine: constants.WriteEngineType = "default",
) -> bigframes.dataframe.DataFrame:
    ...


@typing.overload
def read_pandas(
    pandas_dataframe: pandas.Series,
    *,
    write_engine: constants.WriteEngineType = "default",
) -> bigframes.series.Series:
    ...


@typing.overload
def read_pandas(
    pandas_dataframe: pandas.Index,
    *,
    write_engine: constants.WriteEngineType = "default",
) -> bigframes.core.indexes.Index:
    ...


def read_pandas(
    pandas_dataframe: Union[pandas.DataFrame, pandas.Series, pandas.Index],
    *,
    write_engine: constants.WriteEngineType = "default",
):
    return global_session.with_default_session(
        bigframes.session.Session.read_pandas,
        pandas_dataframe,
        write_engine=write_engine,
    )


read_pandas.__doc__ = inspect.getdoc(bigframes.session.Session.read_pandas)


def read_pickle(
    filepath_or_buffer: FilePath | ReadPickleBuffer,
    compression: CompressionOptions = "infer",
    storage_options: StorageOptions = None,
    *,
    write_engine: constants.WriteEngineType = "default",
):
    return global_session.with_default_session(
        bigframes.session.Session.read_pickle,
        filepath_or_buffer=filepath_or_buffer,
        compression=compression,
        storage_options=storage_options,
        write_engine=write_engine,
    )


read_pickle.__doc__ = inspect.getdoc(bigframes.session.Session.read_pickle)


def read_parquet(
    path: str | IO["bytes"],
    *,
    engine: str = "auto",
    write_engine: constants.WriteEngineType = "default",
) -> bigframes.dataframe.DataFrame:
    return global_session.with_default_session(
        bigframes.session.Session.read_parquet,
        path,
        engine=engine,
        write_engine=write_engine,
    )


read_parquet.__doc__ = inspect.getdoc(bigframes.session.Session.read_parquet)


def read_gbq_function(
    function_name: str,
    is_row_processor: bool = False,
):
    return global_session.with_default_session(
        bigframes.session.Session.read_gbq_function,
        function_name=function_name,
        is_row_processor=is_row_processor,
    )


read_gbq_function.__doc__ = inspect.getdoc(bigframes.session.Session.read_gbq_function)


def from_glob_path(
    path: str, *, connection: Optional[str] = None, name: Optional[str] = None
) -> bigframes.dataframe.DataFrame:
    return global_session.with_default_session(
        bigframes.session.Session.from_glob_path,
        path=path,
        connection=connection,
        name=name,
    )


from_glob_path.__doc__ = inspect.getdoc(bigframes.session.Session.from_glob_path)

_default_location_lock = threading.Lock()


def _get_bqclient() -> bigquery.Client:
    clients_provider = bigframes.session.clients.ClientsProvider(
        project=config.options.bigquery.project,
        location=config.options.bigquery.location,
        use_regional_endpoints=config.options.bigquery.use_regional_endpoints,
        credentials=config.options.bigquery.credentials,
        application_name=config.options.bigquery.application_name,
        bq_kms_key_name=config.options.bigquery.kms_key_name,
        client_endpoints_override=config.options.bigquery.client_endpoints_override,
        requests_transport_adapters=config.options.bigquery.requests_transport_adapters,
    )
    return clients_provider.bqclient


def _dry_run(query, bqclient) -> bigquery.QueryJob:
    job = bqclient.query(query, bigquery.QueryJobConfig(dry_run=True))
    return job


def _set_default_session_location_if_possible(query):
    _set_default_session_location_if_possible_deferred_query(lambda: query)


def _set_default_session_location_if_possible_deferred_query(create_query):
    # Set the location as per the query if this is the first query the user is
    # running and:
    # (1) Default session has not started yet, and
    # (2) Location is not set yet, and
    # (3) Use of regional endpoints is not set.
    # If query is a table name, then it would be the location of the table.
    # If query is a SQL with a table, then it would be table's location.
    # If query is a SQL with no table, then it would be the BQ default location.
    global _default_location_lock

    with _default_location_lock:
        if (
            config.options.bigquery._session_started
            or config.options.bigquery.location
            or config.options.bigquery.use_regional_endpoints
        ):
            return

        query = create_query()
        bqclient = _get_bqclient()

        if bigframes.session._io.bigquery.is_query(query):
            # Intentionally run outside of the session so that we can detect the
            # location before creating the session. Since it's a dry_run, labels
            # aren't necessary.
            job = _dry_run(query, bqclient)
            config.options.bigquery.location = job.location
        else:
            table = bqclient.get_table(query)
            config.options.bigquery.location = table.location
