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

import typing
from typing import Any, List, Optional, Tuple, Union

import bigframes_vendored.constants as constants
import bigframes_vendored.pandas.core.reshape.encoding as vendored_pandas_encoding
import pandas

from bigframes import operations
from bigframes.core import blocks, expression
from bigframes.dataframe import DataFrame
from bigframes.series import Series


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
        blocks._BQ_MAX_COLUMNS - len(block.value_columns) - len(block.index_columns) - 1
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
    block: blocks.Block,
    level: pandas.Index,
    column_label: str,
    column_id: str,
    dummy_na: bool,
) -> Tuple[blocks.Block, List[str]]:
    intermediate_col_ids = []
    for value in level:
        new_column_label = f"{column_label}{value}"
        if column_label == "":
            new_column_label = value
        new_block, new_id = block.project_expr(
            operations.eq_op.as_expr(column_id, expression.const(value))
        )
        intermediate_col_ids.append(new_id)
        block, _ = new_block.project_expr(
            operations.fillna_op.as_expr(new_id, expression.const(False)),
            label=new_column_label,
        )
    if dummy_na:
        # dummy column name for na depends on the dtype
        na_string = str(pandas.Index([None], dtype=level.dtype)[0])
        new_column_label = f"{column_label}{na_string}"
        block, _ = block.apply_unary_op(
            column_id, operations.isnull_op, result_label=new_column_label
        )
    return block, intermediate_col_ids
