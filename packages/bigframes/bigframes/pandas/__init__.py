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

"""BigQuery DataFrames provides a DataFrame API backed by the BigQuery engine."""

from __future__ import annotations

from collections import namedtuple
import inspect
import typing
from typing import (
    Any,
    Callable,
    Dict,
    IO,
    Iterable,
    List,
    Literal,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Union,
)

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
import bigframes.core.global_session as global_session
import bigframes.core.indexes
import bigframes.core.reshape
import bigframes.dataframe
import bigframes.series
import bigframes.session
import third_party.bigframes_vendored.pandas.core.reshape.concat as vendored_pandas_concat
import third_party.bigframes_vendored.pandas.core.reshape.merge as vendored_pandas_merge
import third_party.bigframes_vendored.pandas.core.reshape.tile as vendored_pandas_tile


# Include method definition so that the method appears in our docs for
# bigframes.pandas general functions.
@typing.overload
def concat(
    objs: Iterable[bigframes.series.Series],
    *,
    axis: typing.Literal["index", 0] = ...,
    join=...,
    ignore_index=...,
) -> bigframes.series.Series:
    ...


@typing.overload
def concat(
    objs: Iterable[bigframes.dataframe.DataFrame],
    *,
    axis: typing.Literal["index", 0] = ...,
    join=...,
    ignore_index=...,
) -> bigframes.dataframe.DataFrame:
    ...


@typing.overload
def concat(
    objs: Iterable[Union[bigframes.dataframe.DataFrame, bigframes.series.Series]],
    *,
    axis: typing.Literal["columns", 1],
    join=...,
    ignore_index=...,
) -> bigframes.dataframe.DataFrame:
    ...


@typing.overload
def concat(
    objs: Iterable[Union[bigframes.dataframe.DataFrame, bigframes.series.Series]],
    *,
    axis=...,
    join=...,
    ignore_index=...,
) -> Union[bigframes.dataframe.DataFrame, bigframes.series.Series]:
    ...


def concat(
    objs: Iterable[Union[bigframes.dataframe.DataFrame, bigframes.series.Series]],
    *,
    axis: typing.Union[str, int] = 0,
    join: Literal["inner", "outer"] = "outer",
    ignore_index: bool = False,
) -> Union[bigframes.dataframe.DataFrame, bigframes.series.Series]:
    return bigframes.core.reshape.concat(
        objs=objs, axis=axis, join=join, ignore_index=ignore_index
    )


concat.__doc__ = vendored_pandas_concat.concat.__doc__


def cut(
    x: bigframes.series.Series,
    bins: int,
    *,
    labels: Optional[bool] = None,
) -> bigframes.series.Series:
    return bigframes.core.reshape.cut(
        x,
        bins,
        labels=labels,
    )


cut.__doc__ = vendored_pandas_tile.cut.__doc__


def merge(
    left: DataFrame,
    right: DataFrame,
    how: Literal[
        "inner",
        "left",
        "outer",
        "right",
    ] = "inner",
    on: Optional[str] = None,
    *,
    left_on: Optional[str] = None,
    right_on: Optional[str] = None,
    sort: bool = False,
    suffixes: tuple[str, str] = ("_x", "_y"),
) -> DataFrame:
    return bigframes.core.joins.merge(
        left,
        right,
        how=how,
        on=on,
        left_on=left_on,
        right_on=right_on,
        sort=sort,
        suffixes=suffixes,
    )


merge.__doc__ = vendored_pandas_merge.merge.__doc__


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
        options.bigquery._session_started
        or options.bigquery.location
        or options.bigquery.use_regional_endpoints
    ):
        return

    clients_provider = bigframes.session.ClientsProvider(
        project=options.bigquery.project,
        location=options.bigquery.location,
        use_regional_endpoints=options.bigquery.use_regional_endpoints,
        credentials=options.bigquery.credentials,
    )

    bqclient = clients_provider.bqclient

    if bigframes.session._is_query(query):
        job = bqclient.query(query, bigquery.QueryJobConfig(dry_run=True))
        options.bigquery.location = job.location
    else:
        table = bqclient.get_table(query)
        options.bigquery.location = table.location


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
        Union[int, str, Sequence[Union[str, int]], Literal[False]]
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
        **kwargs,
    )


read_json.__doc__ = inspect.getdoc(bigframes.session.Session.read_json)


def read_gbq(
    query: str,
    *,
    index_col: Iterable[str] | str = (),
    col_order: Iterable[str] = (),
    max_results: Optional[int] = None,
) -> bigframes.dataframe.DataFrame:
    _set_default_session_location_if_possible(query)
    return global_session.with_default_session(
        bigframes.session.Session.read_gbq,
        query,
        index_col=index_col,
        col_order=col_order,
        max_results=max_results,
    )


read_gbq.__doc__ = inspect.getdoc(bigframes.session.Session.read_gbq)


def read_gbq_model(model_name: str):
    return global_session.with_default_session(
        bigframes.session.Session.read_gbq_model,
        model_name,
    )


read_gbq_model.__doc__ = inspect.getdoc(bigframes.session.Session.read_gbq_model)


def read_gbq_query(
    query: str,
    *,
    index_col: Iterable[str] | str = (),
    col_order: Iterable[str] = (),
    max_results: Optional[int] = None,
) -> bigframes.dataframe.DataFrame:
    _set_default_session_location_if_possible(query)
    return global_session.with_default_session(
        bigframes.session.Session.read_gbq_query,
        query,
        index_col=index_col,
        col_order=col_order,
        max_results=max_results,
    )


read_gbq_query.__doc__ = inspect.getdoc(bigframes.session.Session.read_gbq_query)


def read_gbq_table(
    query: str,
    *,
    index_col: Iterable[str] | str = (),
    col_order: Iterable[str] = (),
    max_results: Optional[int] = None,
) -> bigframes.dataframe.DataFrame:
    _set_default_session_location_if_possible(query)
    return global_session.with_default_session(
        bigframes.session.Session.read_gbq_table,
        query,
        index_col=index_col,
        col_order=col_order,
        max_results=max_results,
    )


read_gbq_table.__doc__ = inspect.getdoc(bigframes.session.Session.read_gbq_table)


def read_pandas(pandas_dataframe: pandas.DataFrame) -> bigframes.dataframe.DataFrame:
    return global_session.with_default_session(
        bigframes.session.Session.read_pandas,
        pandas_dataframe,
    )


read_pandas.__doc__ = inspect.getdoc(bigframes.session.Session.read_pandas)


def read_pickle(
    filepath_or_buffer: FilePath | ReadPickleBuffer,
    compression: CompressionOptions = "infer",
    storage_options: StorageOptions = None,
):
    return global_session.with_default_session(
        bigframes.session.Session.read_pickle,
        filepath_or_buffer=filepath_or_buffer,
        compression=compression,
        storage_options=storage_options,
    )


read_pickle.__doc__ = inspect.getdoc(bigframes.session.Session.read_pickle)


def read_parquet(path: str | IO["bytes"]) -> bigframes.dataframe.DataFrame:
    return global_session.with_default_session(
        bigframes.session.Session.read_parquet,
        path,
    )


read_parquet.__doc__ = inspect.getdoc(bigframes.session.Session.read_parquet)


def remote_function(
    input_types: List[type],
    output_type: type,
    dataset: Optional[str] = None,
    bigquery_connection: Optional[str] = None,
    reuse: bool = True,
    name: Optional[str] = None,
):
    return global_session.with_default_session(
        bigframes.session.Session.remote_function,
        input_types=input_types,
        output_type=output_type,
        dataset=dataset,
        bigquery_connection=bigquery_connection,
        reuse=reuse,
        name=name,
    )


remote_function.__doc__ = inspect.getdoc(bigframes.session.Session.remote_function)


def read_gbq_function(function_name: str):
    return global_session.with_default_session(
        bigframes.session.Session.read_gbq_function,
        function_name=function_name,
    )


read_gbq_function.__doc__ = inspect.getdoc(bigframes.session.Session.read_gbq_function)

# pandas dtype attributes
NA = pandas.NA
BooleanDtype = pandas.BooleanDtype
Float64Dtype = pandas.Float64Dtype
Int64Dtype = pandas.Int64Dtype
StringDtype = pandas.StringDtype
ArrowDtype = pandas.ArrowDtype

# Class aliases
# TODO(swast): Make these real classes so we can refer to these in type
# checking and docstrings.
DataFrame = bigframes.dataframe.DataFrame
Index = bigframes.core.indexes.Index
Series = bigframes.series.Series

# Other public pandas attributes
NamedAgg = namedtuple("NamedAgg", ["column", "aggfunc"])

options = config.options
"""Global :class:`~bigframes._config.Options` to configure BigQuery DataFrames."""

# Session management APIs
get_global_session = global_session.get_global_session
reset_session = global_session.reset_session


# Use __all__ to let type checkers know what is part of the public API.
__all___ = [
    # Functions
    "concat",
    "merge",
    "read_csv",
    "read_gbq",
    "read_gbq_function",
    "read_gbq_model",
    "read_pandas",
    "read_pickle",
    "remote_function",
    # pandas dtype attributes
    "NA",
    "BooleanDtype",
    "Float64Dtype",
    "Int64Dtype",
    "StringDtype",
    "ArrowDtype"
    # Class aliases
    "DataFrame",
    "Index",
    "Series",
    # Other public pandas attributes
    "NamedAgg",
    "options",
    # Session management APIs
    "get_global_session",
    "reset_session",
]
