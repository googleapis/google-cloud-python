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

import typing
from typing import Tuple

import ibis
import pandas as pd

import bigframes.constants as constants
import bigframes.core as core
import bigframes.core.guid as guid
import bigframes.core.indexes as indexes
import bigframes.core.scalar
import bigframes.dataframe
import bigframes.series

if typing.TYPE_CHECKING:
    LocSingleKey = bigframes.series.Series | indexes.Index | slice


class LocSeriesIndexer:
    def __init__(self, series: bigframes.series.Series):
        self._series = series

    def __getitem__(self, key) -> bigframes.series.Series:
        """
        Only indexing by a boolean bigframes.series.Series or list of index entries is currently supported
        """
        return typing.cast(
            bigframes.series.Series, _loc_getitem_series_or_dataframe(self._series, key)
        )

    def __setitem__(self, key, value) -> None:
        # TODO(swast): support MultiIndex
        if isinstance(key, slice):
            # TODO(swast): Implement loc with slices.
            raise NotImplementedError(
                f"loc does not yet support slices. {constants.FEEDBACK_LINK}"
            )
        elif isinstance(key, list):
            # TODO(tbergeron): Implement loc for index label list.
            raise NotImplementedError(
                f"loc does not yet support index label lists. {constants.FEEDBACK_LINK}"
            )

        # Assume the key is for the index label.
        block = self._series._block
        value_column = self._series._value
        index_column = block.expr.get_column(block.index_columns[0])
        new_value = (
            ibis.case()
            .when(
                index_column == ibis.literal(key, index_column.type()),
                ibis.literal(value, value_column.type()),
            )
            .else_(value_column)
            .end()
            .name(value_column.get_name())
        )
        all_columns = []
        for column in block.expr.columns:
            if column.get_name() != value_column.get_name():
                all_columns.append(column)
            else:
                all_columns.append(new_value)
        new_expr = block.expr.projection(all_columns)

        # TODO(tbergeron): Use block operators rather than directly building desired ibis expressions.
        self._series._set_block(
            core.blocks.Block(
                new_expr,
                self._series._block.index_columns,
                self._series._block.column_labels,
                self._series._block.index.names,
            )
        )


class IlocSeriesIndexer:
    def __init__(self, series: bigframes.series.Series):
        self._series = series

    def __getitem__(
        self, key
    ) -> bigframes.core.scalar.Scalar | bigframes.series.Series:
        """
        Index series using integer offsets. Currently supports index by key type:

        slice: ex. series.iloc[2:5] returns values at index 2, 3, and 4 as a series
        individual offset: ex. series.iloc[0] returns value at index 0 as a scalar
        list: ex. series.iloc[1, 1, 2, 0] returns a series with the index 1 item repeated
        twice, followed by the index 2 and then and 0 items in that order.

        Other key types are not yet supported.
        """
        return _iloc_getitem_series_or_dataframe(self._series, key)


class LocDataFrameIndexer:
    def __init__(self, dataframe: bigframes.dataframe.DataFrame):
        self._dataframe = dataframe

    @typing.overload
    def __getitem__(self, key: LocSingleKey) -> bigframes.dataframe.DataFrame:
        ...

    # Technically this is wrong since we can have duplicate column labels, but
    # this is expected to be rare.
    @typing.overload
    def __getitem__(self, key: Tuple[LocSingleKey, str]) -> bigframes.series.Series:
        ...

    def __getitem__(self, key):
        # TODO(swast): If the DataFrame has a MultiIndex, we'll need to
        # disambiguate this from a single row selection.
        if isinstance(key, tuple) and len(key) == 2:
            df = typing.cast(
                bigframes.dataframe.DataFrame,
                _loc_getitem_series_or_dataframe(self._dataframe, key[0]),
            )
            return df[key[1]]

        return typing.cast(
            bigframes.dataframe.DataFrame,
            _loc_getitem_series_or_dataframe(self._dataframe, key),
        )

    def __setitem__(
        self,
        key: Tuple[slice, str],
        value: bigframes.dataframe.SingleItemValue,
    ):
        if (
            not isinstance(key, tuple)
            or len(key) != 2
            or not isinstance(key[0], slice)
            or (key[0].start is not None and key[0].start != 0)
            or (key[0].step is not None and key[0].step != 1)
            or key[0].stop is not None
        ):
            raise NotImplementedError(
                "Only setting a column by DataFrame.loc[:, 'column'] is supported."
                f"{constants.FEEDBACK_LINK}"
            )

        # TODO(swast): Support setting multiple columns with key[1] as a list
        # of labels and value as a DataFrame.
        df = self._dataframe.assign(**{key[1]: value})
        self._dataframe._set_block(df._get_block())


class ILocDataFrameIndexer:
    def __init__(self, dataframe: bigframes.dataframe.DataFrame):
        self._dataframe = dataframe

    def __getitem__(self, key) -> bigframes.dataframe.DataFrame | pd.Series:
        """
        Index dataframe using integer offsets. Currently supports index by key type:

        slice: i.e. df.iloc[2:5] returns rows at index 2, 3, and 4 as a dataframe
        individual offset: i.e. df.iloc[0] returns row at index 0 as a pandas Series

        Other key types are not yet supported.
        """
        return _iloc_getitem_series_or_dataframe(self._dataframe, key)


@typing.overload
def _loc_getitem_series_or_dataframe(
    series_or_dataframe: bigframes.series.Series, key
) -> bigframes.series.Series:
    ...


@typing.overload
def _loc_getitem_series_or_dataframe(
    series_or_dataframe: bigframes.dataframe.DataFrame, key
) -> bigframes.dataframe.DataFrame:
    ...


def _loc_getitem_series_or_dataframe(
    series_or_dataframe: bigframes.dataframe.DataFrame | bigframes.series.Series,
    key: LocSingleKey,
) -> bigframes.dataframe.DataFrame | bigframes.series.Series:
    if isinstance(key, bigframes.series.Series) and key.dtype == "boolean":
        return series_or_dataframe[key]
    elif isinstance(key, bigframes.series.Series):
        # TODO(henryjsolberg): support MultiIndex
        temp_name = guid.generate_guid(prefix="temp_series_name_")
        key = key.rename(temp_name)
        keys_df = key.to_frame()
        keys_df = keys_df.set_index(temp_name, drop=True)
        return _perform_loc_list_join(series_or_dataframe, keys_df)
    elif isinstance(key, bigframes.core.indexes.Index):
        # TODO(henryjsolberg): support MultiIndex
        block = key._data._get_block()
        block = block.select_columns(())
        keys_df = bigframes.dataframe.DataFrame(block)
        return _perform_loc_list_join(series_or_dataframe, keys_df)
    elif pd.api.types.is_list_like(key):
        # TODO(henryjsolberg): support MultiIndex
        if len(key) == 0:  # type: ignore
            return typing.cast(
                typing.Union[bigframes.dataframe.DataFrame, bigframes.series.Series],
                series_or_dataframe.iloc[0:0],
            )

        # We can't upload a DataFrame with None as the column name, so set it
        # an arbitrary string.
        index_name = series_or_dataframe.index.name
        index_name_is_none = index_name is None
        if index_name_is_none:
            index_name = "unnamed_col"

        keys_df = bigframes.dataframe.DataFrame(
            {index_name: key}, session=series_or_dataframe._get_block().expr._session
        )
        keys_df = keys_df.set_index(index_name, drop=True)

        if index_name_is_none:
            keys_df.index.name = None
        return _perform_loc_list_join(series_or_dataframe, keys_df)
    elif isinstance(key, slice):
        if (key.start is None) and (key.stop is None) and (key.step is None):
            return series_or_dataframe.copy()
        raise NotImplementedError(
            f"loc does not yet support indexing with a slice. {constants.FEEDBACK_LINK}"
        )
    elif callable(key):
        raise NotImplementedError(
            f"loc does not yet support indexing with a callable. {constants.FEEDBACK_LINK}"
        )
    elif pd.api.types.is_scalar(key):
        index_name = "unnamed_col"
        keys_df = bigframes.dataframe.DataFrame(
            {index_name: [key]}, session=series_or_dataframe._get_block().expr._session
        )
        keys_df = keys_df.set_index(index_name, drop=True)
        keys_df.index.name = None
        return _perform_loc_list_join(series_or_dataframe, keys_df)
    else:
        raise TypeError(
            "Invalid argument type. loc currently only supports indexing with a "
            "boolean bigframes Series, a list of index entries or a single index entry. "
            f"{constants.FEEDBACK_LINK}"
        )


@typing.overload
def _perform_loc_list_join(
    series_or_dataframe: bigframes.series.Series,
    keys_df: bigframes.dataframe.DataFrame,
) -> bigframes.series.Series:
    ...


@typing.overload
def _perform_loc_list_join(
    series_or_dataframe: bigframes.dataframe.DataFrame,
    keys_df: bigframes.dataframe.DataFrame,
) -> bigframes.dataframe.DataFrame:
    ...


def _perform_loc_list_join(
    series_or_dataframe: bigframes.dataframe.DataFrame | bigframes.series.Series,
    keys_df: bigframes.dataframe.DataFrame,
) -> bigframes.series.Series | bigframes.dataframe.DataFrame:
    # right join based on the old index so that the matching rows from the user's
    # original dataframe will be duplicated and reordered appropriately
    original_index_names = series_or_dataframe.index.names
    if isinstance(series_or_dataframe, bigframes.series.Series):
        original_name = series_or_dataframe.name
        name = series_or_dataframe.name if series_or_dataframe.name is not None else "0"
        result = typing.cast(
            bigframes.series.Series,
            series_or_dataframe.to_frame()._perform_join_by_index(keys_df, how="right")[
                name
            ],
        )
        result = result.rename(original_name)
    else:
        result = series_or_dataframe._perform_join_by_index(keys_df, how="right")  # type: ignore
    result = result.rename_axis(original_index_names)
    return result


@typing.overload
def _iloc_getitem_series_or_dataframe(
    series_or_dataframe: bigframes.series.Series, key
) -> bigframes.series.Series | bigframes.core.scalar.Scalar:
    ...


@typing.overload
def _iloc_getitem_series_or_dataframe(
    series_or_dataframe: bigframes.dataframe.DataFrame, key
) -> bigframes.dataframe.DataFrame | pd.Series:
    ...


def _iloc_getitem_series_or_dataframe(
    series_or_dataframe: bigframes.dataframe.DataFrame | bigframes.series.Series, key
) -> bigframes.dataframe.DataFrame | bigframes.series.Series | bigframes.core.scalar.Scalar | pd.Series:
    if isinstance(key, int):
        internal_slice_result = series_or_dataframe._slice(key, key + 1, 1)
        result_pd_df = internal_slice_result.to_pandas()
        if result_pd_df.empty:
            raise IndexError("single positional indexer is out-of-bounds")
        return result_pd_df.iloc[0]
    elif isinstance(key, slice):
        return series_or_dataframe._slice(key.start, key.stop, key.step)
    elif pd.api.types.is_list_like(key):
        # TODO(henryjsolberg): support MultiIndex

        if len(key) == 0:
            return typing.cast(
                typing.Union[bigframes.dataframe.DataFrame, bigframes.series.Series],
                series_or_dataframe.iloc[0:0],
            )
        df = series_or_dataframe
        if isinstance(series_or_dataframe, bigframes.series.Series):
            original_series_name = series_or_dataframe.name
            series_name = (
                original_series_name if original_series_name is not None else "0"
            )
            df = series_or_dataframe.to_frame()
        original_index_name = df.index.name
        temporary_index_name = guid.generate_guid(prefix="temp_iloc_index_")
        df = df.rename_axis(temporary_index_name)

        # set to offset index and use regular loc, then restore index
        df = df.reset_index(drop=False)
        result = df.loc[key]
        result = result.set_index(temporary_index_name)
        result = result.rename_axis(original_index_name)

        if isinstance(series_or_dataframe, bigframes.series.Series):
            result = result[series_name]
            result = typing.cast(bigframes.series.Series, result)
            result = result.rename(original_series_name)

        return result

    elif isinstance(key, tuple):
        raise NotImplementedError(
            f"iloc does not yet support indexing with a (row, column) tuple. {constants.FEEDBACK_LINK}"
        )
    elif callable(key):
        raise NotImplementedError(
            f"iloc does not yet support indexing with a callable. {constants.FEEDBACK_LINK}"
        )
    else:
        raise TypeError(f"Invalid argument type. {constants.FEEDBACK_LINK}")
