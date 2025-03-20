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
import datetime
import functools
import re
import typing
from typing import Hashable, Iterable, List
import warnings

import bigframes_vendored.constants as constants
import bigframes_vendored.pandas.io.common as vendored_pandas_io_common
import numpy as np
import pandas as pd
import pandas.api.types as pdtypes
import pyarrow as pa
import typing_extensions

import bigframes.dtypes as dtypes
import bigframes.exceptions as bfe

UNNAMED_COLUMN_ID = "bigframes_unnamed_column"
UNNAMED_INDEX_ID = "bigframes_unnamed_index"


def is_gcs_path(value) -> typing_extensions.TypeGuard[str]:
    return isinstance(value, str) and value.startswith("gs://")


def get_axis_number(axis: typing.Union[str, int]) -> typing.Literal[0, 1]:
    if axis in {0, "index", "rows"}:
        return 0
    elif axis in {1, "columns"}:
        return 1
    raise ValueError(f"Not a valid axis: {axis}")


def is_list_like(obj: typing.Any) -> typing_extensions.TypeGuard[typing.Sequence]:
    return pd.api.types.is_list_like(obj)


def is_dict_like(obj: typing.Any) -> typing_extensions.TypeGuard[typing.Mapping]:
    return pd.api.types.is_dict_like(obj)


def combine_indices(index1: pd.Index, index2: pd.Index) -> pd.MultiIndex:
    """Combines indices into multi-index while preserving dtypes, names merging by rows 1:1"""
    multi_index = pd.MultiIndex.from_frame(
        pd.concat([index1.to_frame(index=False), index2.to_frame(index=False)], axis=1)
    )
    # to_frame will produce numbered default names, we don't want these
    multi_index.names = [*index1.names, *index2.names]
    return multi_index


def cross_indices(index1: pd.Index, index2: pd.Index) -> pd.MultiIndex:
    """Combines indices into multi-index while preserving dtypes, names using cross product"""
    multi_index = pd.MultiIndex.from_frame(
        pd.merge(
            left=index1.to_frame(index=False),
            right=index2.to_frame(index=False),
            how="cross",
        )
    )
    # to_frame will produce numbered default names, we don't want these
    multi_index.names = [*index1.names, *index2.names]
    return multi_index


def index_as_tuples(index: pd.Index) -> typing.Sequence[typing.Tuple]:
    if isinstance(index, pd.MultiIndex):
        return [label for label in index]
    else:
        return [(label,) for label in index]


def split_index(
    index: pd.Index, levels: int = 1
) -> typing.Tuple[typing.Optional[pd.Index], pd.Index]:
    nlevels = index.nlevels
    remaining = nlevels - levels
    if remaining > 0:
        return index.droplevel(list(range(remaining, nlevels))), index.droplevel(
            list(range(0, remaining))
        )
    else:
        return (None, index)


def get_standardized_ids(
    col_labels: Iterable[Hashable],
    idx_labels: Iterable[Hashable] = (),
    strict: bool = False,
) -> tuple[list[str], list[str]]:
    """Get stardardized column ids as column_ids_list, index_ids_list.
    The standardized_column_id must be valid BQ SQL schema column names, can only be string type and unique.

    Args:
        col_labels: column labels

        idx_labels: index labels, optional. If empty, will only return column ids.

    Return:
        Tuple of (standardized_column_ids, standardized_index_ids)
    """
    col_ids = [
        UNNAMED_COLUMN_ID
        if col_label is None
        else label_to_identifier(col_label, strict=strict)
        for col_label in col_labels
    ]
    idx_ids = [
        UNNAMED_INDEX_ID
        if idx_label is None
        else label_to_identifier(idx_label, strict=strict)
        for idx_label in idx_labels
    ]

    ids = disambiguate_ids(idx_ids + col_ids)

    idx_ids, col_ids = ids[: len(idx_ids)], ids[len(idx_ids) :]

    return col_ids, idx_ids


def label_to_identifier(label: typing.Hashable, strict: bool = False) -> str:
    """
    Convert pandas label to make legal bigquery identifier. May create collisions (should deduplicate after).
    Strict mode might not be necessary, but ibis seems to escape non-alphanumeric characters inconsistently.
    """
    # Column values will be loaded as null if the column name has spaces.
    # https://github.com/googleapis/python-bigquery/issues/1566
    identifier = str(label)
    if strict:
        identifier = str(label).replace(" ", "_")
        identifier = re.sub(r"[^a-zA-Z0-9_]", "", identifier)
        if not identifier:
            identifier = "id"
    return identifier


def disambiguate_ids(ids: typing.Sequence[str]) -> typing.List[str]:
    """Disambiguate list of ids by adding suffixes where needed. If inputs are legal sql ids, outputs should be as well."""
    return typing.cast(
        List[str],
        vendored_pandas_io_common.dedup_names(ids, is_potential_multiindex=False),
    )


def merge_column_labels(
    left_labels: pd.Index,
    right_labels: pd.Index,
    coalesce_labels: typing.Sequence,
    suffixes: tuple[str, str] = ("_x", "_y"),
) -> pd.Index:
    result_labels = []

    for col_label in left_labels:
        if col_label in right_labels:
            if col_label in coalesce_labels:
                # Merging on the same column only returns 1 key column from coalesce both.
                # Take the left key column.
                result_labels.append(col_label)
            else:
                result_labels.append(str(col_label) + suffixes[0])
        else:
            result_labels.append(col_label)

    for col_label in right_labels:
        if col_label in left_labels:
            if col_label in coalesce_labels:
                # Merging on the same column only returns 1 key column from coalesce both.
                # Pass the right key column.
                pass
            else:
                result_labels.append(str(col_label) + suffixes[1])
        else:
            result_labels.append(col_label)

    return pd.Index(result_labels)


def preview(*, name: str):
    """Decorate to warn of a preview API."""

    def decorator(func):
        msg = f"{name} is in preview. Its behavior may change in future versions."

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(bfe.format_message(msg), category=bfe.PreviewWarning)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def timedelta_to_micros(
    timedelta: typing.Union[pd.Timedelta, datetime.timedelta, np.timedelta64]
) -> int:
    if isinstance(timedelta, pd.Timedelta):
        # pd.Timedelta.value returns total nanoseconds.
        return timedelta.value // 1000

    if isinstance(timedelta, np.timedelta64):
        return timedelta.astype("timedelta64[us]").astype(np.int64)

    if isinstance(timedelta, datetime.timedelta):
        return (
            (timedelta.days * 3600 * 24) + timedelta.seconds
        ) * 1_000_000 + timedelta.microseconds

    raise TypeError(f"Unrecognized input type: {type(timedelta)}")


def replace_timedeltas_with_micros(dataframe: pd.DataFrame) -> List[str]:
    """
    Replaces in-place timedeltas to integer values in microseconds. Nanosecond part is ignored.

    Returns:
        The names of updated columns
    """
    updated_columns = []

    for col in dataframe.columns:
        if pdtypes.is_timedelta64_dtype(dataframe[col].dtype):
            dataframe[col] = dataframe[col].apply(timedelta_to_micros)
            updated_columns.append(col)

    if pdtypes.is_timedelta64_dtype(dataframe.index.dtype):
        dataframe.index = dataframe.index.map(timedelta_to_micros)
        updated_columns.append(dataframe.index.name)

    return updated_columns


def _search_for_nested_json_type(arrow_type: pa.DataType) -> bool:
    """
    Searches recursively for JSON array type within a PyArrow DataType.
    """
    if arrow_type == dtypes.JSON_ARROW_TYPE:
        return True
    if pa.types.is_list(arrow_type):
        return _search_for_nested_json_type(arrow_type.value_type)
    if pa.types.is_struct(arrow_type):
        for i in range(arrow_type.num_fields):
            if _search_for_nested_json_type(arrow_type.field(i).type):
                return True
        return False
    return False


def replace_json_with_string(dataframe: pd.DataFrame) -> List[str]:
    """
    Due to a BigQuery IO limitation with loading JSON from Parquet files (b/374784249),
    we're using a workaround: storing JSON as strings and then parsing them into JSON
    objects.
    TODO(b/395912450): Remove workaround solution once b/374784249 got resolved.
    """
    updated_columns = []

    for col in dataframe.columns:
        column_type = dataframe[col].dtype
        if column_type == dtypes.JSON_DTYPE:
            dataframe[col] = dataframe[col].astype(dtypes.STRING_DTYPE)
            updated_columns.append(col)
        elif isinstance(column_type, pd.ArrowDtype) and _search_for_nested_json_type(
            column_type.pyarrow_dtype
        ):
            raise NotImplementedError(
                f"Nested JSON types, found in column `{col}`: `{column_type}`', "
                f"are currently unsupported for upload. {constants.FEEDBACK_LINK}"
            )

    if dataframe.index.dtype == dtypes.JSON_DTYPE:
        dataframe.index = dataframe.index.astype(dtypes.STRING_DTYPE)
        updated_columns.append(dataframe.index.name)
    elif isinstance(
        dataframe.index.dtype, pd.ArrowDtype
    ) and _search_for_nested_json_type(dataframe.index.dtype.pyarrow_dtype):
        raise NotImplementedError(
            f"Nested JSON types, found in the index: `{dataframe.index.dtype}`', "
            f"are currently unsupported for upload. {constants.FEEDBACK_LINK}"
        )

    return updated_columns
