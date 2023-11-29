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
import bigframes.constants as constants
import bigframes.core.blocks
import bigframes.core.global_session as global_session
import bigframes.core.indexes
import bigframes.core.reshape
import bigframes.dataframe
import bigframes.operations as ops
import bigframes.series
import bigframes.session
import bigframes.session.clients
import third_party.bigframes_vendored.pandas.core.reshape.concat as vendored_pandas_concat
import third_party.bigframes_vendored.pandas.core.reshape.encoding as vendored_pandas_encoding
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


def get_dummies(
    data: Union[DataFrame, Series],
    prefix: Union[List, dict, str, None] = None,
    prefix_sep: Union[List, dict, str, None] = "_",
    dummy_na: bool = False,
    columns: Optional[List] = None,
    drop_first: bool = False,
    dtype: Any = None,
) -> DataFrame:
    # simplify input parameters into per-input-label lists
    # also raise errors for invalid parameters
    column_labels, prefixes, prefix_seps = _standardize_get_dummies_params(
        data, prefix, prefix_sep, columns, dtype
    )

    # combine prefixes into per-column-id list
    full_columns_prefixes, columns_ids = _determine_get_dummies_columns_from_labels(
        data, column_labels, prefix is not None, prefixes, prefix_seps
    )

    # run queries to compute unique values
    block = data._block
    max_unique_value = (
        bigframes.core.blocks._BQ_MAX_COLUMNS
        - len(block.value_columns)
        - len(block.index_columns)
        - 1
    ) // len(column_labels)
    columns_values = [
        block._get_unique_values([col_id], max_unique_value) for col_id in columns_ids
    ]

    # for each dummified column, add the content of the output columns via block operations
    intermediate_col_ids = []
    for i in range(len(columns_values)):
        level = columns_values[i].get_level_values(0).sort_values().dropna()
        if drop_first:
            level = level[1:]
        column_label = full_columns_prefixes[i]
        column_id = columns_ids[i]
        block, new_intermediate_col_ids = _perform_get_dummies_block_operations(
            block, level, column_label, column_id, dummy_na
        )
        intermediate_col_ids.extend(new_intermediate_col_ids)

    # drop dummified columns (and the intermediate columns we added)
    block = block.drop_columns(columns_ids + intermediate_col_ids)
    return DataFrame(block)


get_dummies.__doc__ = vendored_pandas_encoding.get_dummies.__doc__


def _standardize_get_dummies_params(
    data: Union[DataFrame, Series],
    prefix: Union[List, dict, str, None],
    prefix_sep: Union[List, dict, str, None],
    columns: Optional[List],
    dtype: Any,
) -> Tuple[List, List[str], List[str]]:
    block = data._block

    if isinstance(data, Series):
        columns = [block.column_labels[0]]
    if columns is not None and not pandas.api.types.is_list_like(columns):
        raise TypeError("Input must be a list-like for parameter `columns`")
    if dtype is not None and dtype not in [
        pandas.BooleanDtype,
        bool,
        "Boolean",
        "boolean",
        "bool",
    ]:
        raise NotImplementedError(
            f"Only Boolean dtype is currently supported. {constants.FEEDBACK_LINK}"
        )

    if columns is None:
        default_dummy_types = [pandas.StringDtype, "string[pyarrow]"]
        columns = []
        columns_set = set()
        for col_id in block.value_columns:
            label = block.col_id_to_label[col_id]
            if (
                label not in columns_set
                and block.expr.get_column_type(col_id) in default_dummy_types
            ):
                columns.append(label)
                columns_set.add(label)

    column_labels: List = typing.cast(List, columns)

    def parse_prefix_kwarg(kwarg, kwarg_name) -> Optional[List[str]]:
        if kwarg is None:
            return None
        if isinstance(kwarg, str):
            return [kwarg] * len(column_labels)
        if isinstance(kwarg, dict):
            return [kwarg[column] for column in column_labels]
        kwarg = typing.cast(List, kwarg)
        if pandas.api.types.is_list_like(kwarg) and len(kwarg) != len(column_labels):
            raise ValueError(
                f"Length of '{kwarg_name}' ({len(kwarg)}) did not match "
                f"the length of the columns being encoded ({len(column_labels)})."
            )
        if pandas.api.types.is_list_like(kwarg):
            return list(map(str, kwarg))
        raise TypeError(f"{kwarg_name} kwarg must be a string, list, or dictionary")

    prefix_seps = parse_prefix_kwarg(prefix_sep or "_", "prefix_sep")
    prefix_seps = typing.cast(List, prefix_seps)
    prefixes = parse_prefix_kwarg(prefix, "prefix")
    if prefixes is None:
        prefixes = column_labels
    prefixes = typing.cast(List, prefixes)

    return column_labels, prefixes, prefix_seps


def _determine_get_dummies_columns_from_labels(
    data: Union[DataFrame, Series],
    column_labels: List,
    prefix_given: bool,
    prefixes: List[str],
    prefix_seps: List[str],
) -> Tuple[List[str], List[str]]:
    block = data._block

    columns_ids = []
    columns_prefixes = []
    for i in range(len(column_labels)):
        label = column_labels[i]
        empty_prefix = label is None or (isinstance(data, Series) and not prefix_given)
        full_prefix = "" if empty_prefix else prefixes[i] + prefix_seps[i]

        for col_id in block.label_to_col_id[label]:
            columns_ids.append(col_id)
            columns_prefixes.append(full_prefix)

    return columns_prefixes, columns_ids


def _perform_get_dummies_block_operations(
    block: bigframes.core.blocks.Block,
    level: pandas.Index,
    column_label: str,
    column_id: str,
    dummy_na: bool,
) -> Tuple[bigframes.core.blocks.Block, List[str]]:
    intermediate_col_ids = []
    for value in level:
        new_column_label = f"{column_label}{value}"
        if column_label == "":
            new_column_label = value
        new_block, new_id = block.apply_unary_op(
            column_id, ops.BinopPartialLeft(ops.eq_op, value)
        )
        intermediate_col_ids.append(new_id)
        block, _ = new_block.apply_unary_op(
            new_id,
            ops.BinopPartialRight(ops.fillna_op, False),
            result_label=new_column_label,
        )
    if dummy_na:
        # dummy column name for na depends on the dtype
        na_string = str(pandas.Index([None], dtype=level.dtype)[0])
        new_column_label = f"{column_label}{na_string}"
        block, _ = block.apply_unary_op(
            column_id, ops.isnull_op, result_label=new_column_label
        )
    return block, intermediate_col_ids


def qcut(
    x: bigframes.series.Series,
    q: int,
    *,
    labels: Optional[bool] = None,
    duplicates: typing.Literal["drop", "error"] = "error",
) -> bigframes.series.Series:
    return bigframes.core.reshape.qcut(x, q, labels=labels, duplicates=duplicates)


qcut.__doc__ = vendored_pandas_tile.qcut.__doc__


def merge(
    left: DataFrame,
    right: DataFrame,
    how: Literal[
        "inner",
        "left",
        "outer",
        "right",
        "cross",
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

    clients_provider = bigframes.session.clients.ClientsProvider(
        project=options.bigquery.project,
        location=options.bigquery.location,
        use_regional_endpoints=options.bigquery.use_regional_endpoints,
        credentials=options.bigquery.credentials,
        application_name=options.bigquery.application_name,
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
    query_or_table: str,
    *,
    index_col: Iterable[str] | str = (),
    col_order: Iterable[str] = (),
    max_results: Optional[int] = None,
    use_cache: bool = True,
) -> bigframes.dataframe.DataFrame:
    _set_default_session_location_if_possible(query_or_table)
    return global_session.with_default_session(
        bigframes.session.Session.read_gbq,
        query_or_table,
        index_col=index_col,
        col_order=col_order,
        max_results=max_results,
        use_cache=use_cache,
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
    use_cache: bool = True,
) -> bigframes.dataframe.DataFrame:
    _set_default_session_location_if_possible(query)
    return global_session.with_default_session(
        bigframes.session.Session.read_gbq_query,
        query,
        index_col=index_col,
        col_order=col_order,
        max_results=max_results,
        use_cache=use_cache,
    )


read_gbq_query.__doc__ = inspect.getdoc(bigframes.session.Session.read_gbq_query)


def read_gbq_table(
    query: str,
    *,
    index_col: Iterable[str] | str = (),
    col_order: Iterable[str] = (),
    max_results: Optional[int] = None,
    use_cache: bool = True,
) -> bigframes.dataframe.DataFrame:
    _set_default_session_location_if_possible(query)
    return global_session.with_default_session(
        bigframes.session.Session.read_gbq_table,
        query,
        index_col=index_col,
        col_order=col_order,
        max_results=max_results,
        use_cache=use_cache,
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
    packages: Optional[Sequence[str]] = None,
):
    return global_session.with_default_session(
        bigframes.session.Session.remote_function,
        input_types=input_types,
        output_type=output_type,
        dataset=dataset,
        bigquery_connection=bigquery_connection,
        reuse=reuse,
        name=name,
        packages=packages,
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

option_context = config.option_context
"""Global :class:`~bigframes._config.option_context` to configure BigQuery DataFrames."""

# Session management APIs
get_global_session = global_session.get_global_session
close_session = global_session.close_session
reset_session = global_session.close_session


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
    "option_context",
    # Session management APIs
    "get_global_session",
    "close_session",
    "reset_session",
]
