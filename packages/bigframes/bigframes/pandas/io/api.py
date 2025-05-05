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

import inspect
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

import bigframes._config as config
import bigframes.core.blocks
import bigframes.core.global_session as global_session
import bigframes.core.indexes
import bigframes.core.reshape
import bigframes.core.tools
import bigframes.dataframe
import bigframes.enums
import bigframes.series
import bigframes.session
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


def _set_default_session_location_if_possible(query):
    # Set the location as per the query if this is the first query the user is
    # running and:
    # (1) Default session has not started yet, and
    # (2) Location is not set yet, and
    # (3) Use of regional endpoints is not set.
    # If query is a table name, then it would be the location of the table.
    # If query is a SQL with a table, then it would be table's location.
    # If query is a SQL with no table, then it would be the BQ default location.
    if (
        config.options.bigquery._session_started
        or config.options.bigquery.location
        or config.options.bigquery.use_regional_endpoints
    ):
        return

    clients_provider = bigframes.session.clients.ClientsProvider(
        project=config.options.bigquery.project,
        location=config.options.bigquery.location,
        use_regional_endpoints=config.options.bigquery.use_regional_endpoints,
        credentials=config.options.bigquery.credentials,
        application_name=config.options.bigquery.application_name,
        bq_kms_key_name=config.options.bigquery.kms_key_name,
        client_endpoints_override=config.options.bigquery.client_endpoints_override,
    )

    bqclient = clients_provider.bqclient

    if bigframes.session._io.bigquery.is_query(query):
        # Intentionally run outside of the session so that we can detect the
        # location before creating the session. Since it's a dry_run, labels
        # aren't necessary.
        job = bqclient.query(query, bigquery.QueryJobConfig(dry_run=True))
        config.options.bigquery.location = job.location
    else:
        table = bqclient.get_table(query)
        config.options.bigquery.location = table.location
