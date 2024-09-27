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
from datetime import datetime
import inspect
import sys
import typing
from typing import Any, Iterable, List, Literal, Optional, Sequence, Tuple, Union

import bigframes_vendored.constants as constants
import bigframes_vendored.pandas.core.reshape.concat as vendored_pandas_concat
import bigframes_vendored.pandas.core.reshape.encoding as vendored_pandas_encoding
import bigframes_vendored.pandas.core.reshape.merge as vendored_pandas_merge
import bigframes_vendored.pandas.core.reshape.tile as vendored_pandas_tile
import bigframes_vendored.pandas.core.tools.datetimes as vendored_pandas_datetimes
import pandas

import bigframes._config as config
import bigframes.core.blocks
import bigframes.core.expression as ex
import bigframes.core.global_session as global_session
import bigframes.core.indexes
import bigframes.core.joins
import bigframes.core.reshape
import bigframes.core.tools
import bigframes.dataframe
import bigframes.enums
import bigframes.functions._utils as functions_utils
import bigframes.operations as ops
from bigframes.pandas.io.api import (
    read_csv,
    read_gbq,
    read_gbq_function,
    read_gbq_model,
    read_gbq_query,
    read_gbq_table,
    read_json,
    read_pandas,
    read_parquet,
    read_pickle,
)
import bigframes.series
import bigframes.session
import bigframes.session._io.bigquery
import bigframes.session.clients
import bigframes.version

try:
    import resource
except ImportError:
    # resource is only available on Unix-like systems.
    # https://docs.python.org/3/library/resource.html
    resource = None  # type: ignore


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
    labels: Union[Iterable[str], bool, None] = None,
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
        new_block, new_id = block.project_expr(
            ops.eq_op.as_expr(column_id, ex.const(value))
        )
        intermediate_col_ids.append(new_id)
        block, _ = new_block.project_expr(
            ops.fillna_op.as_expr(new_id, ex.const(False)),
            label=new_column_label,
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


def remote_function(
    input_types: Union[None, type, Sequence[type]] = None,
    output_type: Optional[type] = None,
    dataset: Optional[str] = None,
    bigquery_connection: Optional[str] = None,
    reuse: bool = True,
    name: Optional[str] = None,
    packages: Optional[Sequence[str]] = None,
    cloud_function_service_account: Optional[str] = None,
    cloud_function_kms_key_name: Optional[str] = None,
    cloud_function_docker_repository: Optional[str] = None,
    max_batching_rows: Optional[int] = 1000,
    cloud_function_timeout: Optional[int] = 600,
    cloud_function_max_instances: Optional[int] = None,
    cloud_function_vpc_connector: Optional[str] = None,
    cloud_function_memory_mib: Optional[int] = 1024,
    cloud_function_ingress_settings: Literal[
        "all", "internal-only", "internal-and-gclb"
    ] = "all",
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
        cloud_function_service_account=cloud_function_service_account,
        cloud_function_kms_key_name=cloud_function_kms_key_name,
        cloud_function_docker_repository=cloud_function_docker_repository,
        max_batching_rows=max_batching_rows,
        cloud_function_timeout=cloud_function_timeout,
        cloud_function_max_instances=cloud_function_max_instances,
        cloud_function_vpc_connector=cloud_function_vpc_connector,
        cloud_function_memory_mib=cloud_function_memory_mib,
        cloud_function_ingress_settings=cloud_function_ingress_settings,
    )


remote_function.__doc__ = inspect.getdoc(bigframes.session.Session.remote_function)


@typing.overload
def to_datetime(
    arg: Union[
        vendored_pandas_datetimes.local_iterables,
        bigframes.series.Series,
        bigframes.dataframe.DataFrame,
    ],
    *,
    utc: bool = False,
    format: Optional[str] = None,
    unit: Optional[str] = None,
) -> bigframes.series.Series:
    ...


@typing.overload
def to_datetime(
    arg: Union[int, float, str, datetime],
    *,
    utc: bool = False,
    format: Optional[str] = None,
    unit: Optional[str] = None,
) -> Union[pandas.Timestamp, datetime]:
    ...


def to_datetime(
    arg: Union[
        Union[int, float, str, datetime],
        vendored_pandas_datetimes.local_iterables,
        bigframes.series.Series,
        bigframes.dataframe.DataFrame,
    ],
    *,
    utc: bool = False,
    format: Optional[str] = None,
    unit: Optional[str] = None,
) -> Union[pandas.Timestamp, datetime, bigframes.series.Series]:
    return bigframes.core.tools.to_datetime(
        arg,
        utc=utc,
        format=format,
        unit=unit,
    )


to_datetime.__doc__ = vendored_pandas_datetimes.to_datetime.__doc__


def get_default_session_id() -> str:
    """Gets the session id that is used whenever a custom session
    has not been provided.

    It is the session id of the default global session. It is prefixed to
    the table id of all temporary tables created in the global session.

    Returns:
        str, the default global session id, ex. 'sessiona1b2c'
    """
    return get_global_session().session_id


def clean_up_by_session_id(
    session_id: str,
    location: Optional[str] = None,
    project: Optional[str] = None,
) -> None:
    """Searches through BigQuery tables and routines and deletes the ones
    created during the session with the given session id. The match is
    determined by having the session id present in the resource name or
    metadata. The cloud functions serving the cleaned up routines are also
    cleaned up.

    This could be useful if the session object has been lost.
    Calling `session.close()` or `bigframes.pandas.close_session()`
    is preferred in most cases.

    Args:
        session_id (str):
            The session id to clean up. Can be found using
            session.session_id or get_default_session_id().

        location (str, default None):
            The location of the session to clean up. If given, used
            together with project kwarg to determine the dataset
            to search through for tables to clean up.

        project (str, default None):
            The project id associated with the session to clean up.
            If given, used together with location kwarg to determine
            the dataset to search through for tables to clean up.

    Returns:
        None
    """
    session = get_global_session()

    if (location is None) != (project is None):
        raise ValueError(
            "Only one of project or location was given. Must specify both or neither."
        )
    elif location is None and project is None:
        dataset = session._anonymous_dataset
    else:
        dataset = bigframes.session._io.bigquery.create_bq_dataset_reference(
            session.bqclient,
            location=location,
            project=project,
            api_name="clean_up_by_session_id",
        )

    bigframes.session._io.bigquery.delete_tables_matching_session_id(
        session.bqclient, dataset, session_id
    )

    functions_utils._clean_up_by_session_id(
        session.bqclient, session.cloudfunctionsclient, dataset, session_id
    )


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
MultiIndex = bigframes.core.indexes.MultiIndex
Series = bigframes.series.Series
__version__ = bigframes.version.__version__

# Other public pandas attributes
NamedAgg = namedtuple("NamedAgg", ["column", "aggfunc"])

options = config.options
"""Global :class:`~bigframes._config.Options` to configure BigQuery DataFrames."""

option_context = config.option_context
"""Global :class:`~bigframes._config.option_context` to configure BigQuery DataFrames."""


# Session management APIs
def get_global_session():
    return global_session.get_global_session()


get_global_session.__doc__ = global_session.get_global_session.__doc__


def close_session():
    return global_session.close_session()


close_session.__doc__ = global_session.close_session.__doc__


def reset_session():
    return global_session.close_session()


reset_session.__doc__ = global_session.close_session.__doc__


# SQL Compilation uses recursive algorithms on deep trees
# 10M tree depth should be sufficient to generate any sql that is under bigquery limit
# Note: This limit does not have the desired effect on Python 3.12 in
# which the applicable limit is now hard coded. See:
# https://github.com/python/cpython/issues/112282
sys.setrecursionlimit(max(10000000, sys.getrecursionlimit()))

if resource is not None:
    soft_limit, hard_limit = resource.getrlimit(resource.RLIMIT_STACK)
    if soft_limit < hard_limit or hard_limit == resource.RLIM_INFINITY:
        try:
            resource.setrlimit(resource.RLIMIT_STACK, (hard_limit, hard_limit))
        except Exception:
            pass

# Use __all__ to let type checkers know what is part of the public API.
__all__ = [
    # Functions
    "concat",
    "merge",
    "read_csv",
    "read_gbq",
    "read_gbq_function",
    "read_gbq_model",
    "read_gbq_query",
    "read_gbq_table",
    "read_json",
    "read_pandas",
    "read_parquet",
    "read_pickle",
    "remote_function",
    "to_datetime",
    # pandas dtype attributes
    "NA",
    "BooleanDtype",
    "Float64Dtype",
    "Int64Dtype",
    "StringDtype",
    "ArrowDtype",
    # Class aliases
    "DataFrame",
    "Index",
    "MultiIndex",
    "Series",
    "__version__",
    # Other public pandas attributes
    "NamedAgg",
    "options",
    "option_context",
    # Session management APIs
    "get_global_session",
    "close_session",
    "reset_session",
]
