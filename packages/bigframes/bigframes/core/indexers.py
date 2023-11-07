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
from typing import List, Tuple, Union

import ibis
import pandas as pd

import bigframes.constants as constants
import bigframes.core.blocks
import bigframes.core.guid as guid
import bigframes.core.indexes as indexes
import bigframes.core.scalar
import bigframes.dataframe
import bigframes.operations as ops
import bigframes.series

if typing.TYPE_CHECKING:
    LocSingleKey = Union[
        bigframes.series.Series, indexes.Index, slice, bigframes.core.scalar.Scalar
    ]


class LocSeriesIndexer:
    def __init__(self, series: bigframes.series.Series):
        self._series = series

    def __getitem__(
        self, key
    ) -> Union[bigframes.core.scalar.Scalar, bigframes.series.Series]:
        return _loc_getitem_series_or_dataframe(self._series, key)

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
        value_column = self._series._value_column
        index_column = block.index_columns[0]

        # if index == key return value else value_colum
        block, insert_cond = block.apply_unary_op(
            index_column, ops.partial_right(ops.eq_op, key)
        )
        block, result_id = block.apply_binary_op(
            insert_cond,
            self._series._value_column,
            ops.partial_arg1(ops.where_op, value),
        )
        block = block.copy_values(result_id, value_column).drop_columns(
            [insert_cond, result_id]
        )

        self._series._set_block(block)


class IlocSeriesIndexer:
    def __init__(self, series: bigframes.series.Series):
        self._series = series

    def __getitem__(
        self, key
    ) -> Union[bigframes.core.scalar.Scalar, bigframes.series.Series]:
        """
        Index series using integer offsets. Currently supports index by key type:

        slice: ex. series.iloc[2:5] returns values at index 2, 3, and 4 as a series
        individual offset: ex. series.iloc[0] returns value at index 0 as a scalar
        list: ex. series.iloc[1, 1, 2, 0] returns a series with the index 1 item repeated
        twice, followed by the index 2 and then and 0 items in that order.

        Other key types are not yet supported.
        """
        return _iloc_getitem_series_or_dataframe(self._series, key)


class IatSeriesIndexer:
    def __init__(self, series: bigframes.series.Series):
        self._series = series

    def __getitem__(self, key: int) -> bigframes.core.scalar.Scalar:
        if not isinstance(key, int):
            raise ValueError("Series iAt based indexing can only have integer indexers")
        return self._series.iloc[key]


class AtSeriesIndexer:
    def __init__(self, series: bigframes.series.Series):
        self._series = series

    def __getitem__(
        self, key: LocSingleKey
    ) -> Union[bigframes.core.scalar.Scalar, bigframes.series.Series]:
        return self._series.loc[key]

    def __setitem__(
        self,
        key: LocSingleKey,
        value: bigframes.core.scalar.Scalar,
    ):
        if not pd.api.types.is_scalar(value):
            raise NotImplementedError(
                "series.at.__setitem__ only supports scalar right-hand values. "
                f"{constants.FEEDBACK_LINK}"
            )
        self._series.loc[key] = value


class LocDataFrameIndexer:
    def __init__(self, dataframe: bigframes.dataframe.DataFrame):
        self._dataframe = dataframe

    @typing.overload
    def __getitem__(
        self, key: LocSingleKey
    ) -> Union[bigframes.dataframe.DataFrame, pd.Series]:
        ...

    # Technically this is wrong since we can have duplicate column labels, but
    # this is expected to be rare.
    @typing.overload
    def __getitem__(
        self, key: Tuple[LocSingleKey, str]
    ) -> Union[bigframes.series.Series, bigframes.core.scalar.Scalar]:
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
            isinstance(key, tuple)
            and len(key) == 2
            and isinstance(key[0], slice)
            and (key[0].start is None or key[0].start == 0)
            and (key[0].step is None or key[0].step == 1)
            and key[0].stop is None
        ):
            # TODO(swast): Support setting multiple columns with key[1] as a list
            # of labels and value as a DataFrame.
            df = self._dataframe.assign(**{key[1]: value})
            self._dataframe._set_block(df._get_block())
        elif (
            isinstance(key, tuple)
            and len(key) == 2
            and isinstance(key[0], bigframes.series.Series)
            and key[0].dtype == "boolean"
        ) and pd.api.types.is_scalar(value):
            new_column = key[0].map({True: value, False: None})
            try:
                original_column = self._dataframe[key[1]]
            except KeyError:
                self._dataframe[key[1]] = new_column
                return
            try:
                self._dataframe[key[1]] = new_column.fillna(original_column)
            except ibis.common.exceptions.IbisTypeError:
                raise TypeError(
                    f"Cannot assign scalar of type {type(value)} to column of type {original_column.dtype}, or index type of series argument does not match dataframe."
                )
        else:
            raise NotImplementedError(
                "Only DataFrame.loc[:, 'column'] and DataFrame.loc[bool series, 'column'] = Scalar are supported."
                f"{constants.FEEDBACK_LINK}"
            )


class ILocDataFrameIndexer:
    def __init__(self, dataframe: bigframes.dataframe.DataFrame):
        self._dataframe = dataframe

    def __getitem__(self, key) -> Union[bigframes.dataframe.DataFrame, pd.Series]:
        """
        Index dataframe using integer offsets. Currently supports index by key type:

        slice: i.e. df.iloc[2:5] returns rows at index 2, 3, and 4 as a dataframe
        individual offset: i.e. df.iloc[0] returns row at index 0 as a pandas Series

        Other key types are not yet supported.
        """
        return _iloc_getitem_series_or_dataframe(self._dataframe, key)


class IatDataFrameIndexer:
    def __init__(self, dataframe: bigframes.dataframe.DataFrame):
        self._dataframe = dataframe

    def __getitem__(self, key: tuple) -> bigframes.core.scalar.Scalar:
        error_message = "DataFrame.iat should be indexed by a tuple of exactly 2 ints"
        # we raise TypeError or ValueError under the same conditions that pandas does
        if isinstance(key, int):
            raise TypeError(error_message)
        if not isinstance(key, tuple):
            raise ValueError(error_message)
        key_values_are_ints = [isinstance(key_value, int) for key_value in key]
        if not all(key_values_are_ints):
            raise ValueError(error_message)
        if len(key) != 2:
            raise TypeError(error_message)
        block: bigframes.core.blocks.Block = self._dataframe._block  # type: ignore
        column_block = block.select_columns([block.value_columns[key[1]]])
        column = bigframes.series.Series(column_block)
        return column.iloc[key[0]]


class AtDataFrameIndexer:
    def __init__(self, dataframe: bigframes.dataframe.DataFrame):
        self._dataframe = dataframe

    def __getitem__(
        self, key: tuple
    ) -> Union[bigframes.core.scalar.Scalar, bigframes.series.Series]:
        if not isinstance(key, tuple):
            raise TypeError(
                "DataFrame.at should be indexed by a (row label, column name) tuple."
            )
        return self._dataframe.loc[key]


@typing.overload
def _loc_getitem_series_or_dataframe(
    series_or_dataframe: bigframes.series.Series, key
) -> Union[bigframes.core.scalar.Scalar, bigframes.series.Series]:
    ...


@typing.overload
def _loc_getitem_series_or_dataframe(
    series_or_dataframe: bigframes.dataframe.DataFrame, key
) -> Union[bigframes.dataframe.DataFrame, pd.Series]:
    ...


def _loc_getitem_series_or_dataframe(
    series_or_dataframe: Union[bigframes.dataframe.DataFrame, bigframes.series.Series],
    key: LocSingleKey,
) -> Union[
    bigframes.dataframe.DataFrame,
    bigframes.series.Series,
    pd.Series,
    bigframes.core.scalar.Scalar,
]:
    if isinstance(key, bigframes.series.Series) and key.dtype == "boolean":
        return series_or_dataframe[key]
    elif isinstance(key, bigframes.series.Series):
        temp_name = guid.generate_guid(prefix="temp_series_name_")
        if len(series_or_dataframe.index.names) > 1:
            temp_name = series_or_dataframe.index.names[0]
        key = key.rename(temp_name)
        keys_df = key.to_frame()
        keys_df = keys_df.set_index(temp_name, drop=True)
        return _perform_loc_list_join(series_or_dataframe, keys_df)
    elif isinstance(key, bigframes.core.indexes.Index):
        block = key._data._get_block()
        block = block.select_columns(())
        keys_df = bigframes.dataframe.DataFrame(block)
        return _perform_loc_list_join(series_or_dataframe, keys_df)
    elif pd.api.types.is_list_like(key):
        key = typing.cast(List, key)
        if len(key) == 0:
            return typing.cast(
                Union[bigframes.dataframe.DataFrame, bigframes.series.Series],
                series_or_dataframe.iloc[0:0],
            )
        if pd.api.types.is_list_like(key[0]):
            original_index_names = series_or_dataframe.index.names
            num_index_cols = len(original_index_names)

            entry_col_count_correct = [len(entry) == num_index_cols for entry in key]
            if not all(entry_col_count_correct):
                # pandas usually throws TypeError in these cases- tuple causes IndexError, but that
                # seems like unintended behavior
                raise TypeError(
                    "All entries must be of equal length when indexing by list of listlikes"
                )
            temporary_index_names = [
                guid.generate_guid(prefix="temp_loc_index_")
                for _ in range(len(original_index_names))
            ]
            index_cols_dict = {}
            for i in range(num_index_cols):
                index_name = temporary_index_names[i]
                values = [entry[i] for entry in key]
                index_cols_dict[index_name] = values
            keys_df = bigframes.dataframe.DataFrame(
                index_cols_dict, session=series_or_dataframe._get_block().expr.session
            )
            keys_df = keys_df.set_index(temporary_index_names, drop=True)
            keys_df = keys_df.rename_axis(original_index_names)
        else:
            # We can't upload a DataFrame with None as the column name, so set it
            # an arbitrary string.
            index_name = series_or_dataframe.index.name
            index_name_is_none = index_name is None
            if index_name_is_none:
                index_name = "unnamed_col"
            keys_df = bigframes.dataframe.DataFrame(
                {index_name: key},
                session=series_or_dataframe._get_block().expr.session,
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
            {index_name: [key]}, session=series_or_dataframe._get_block().expr.session
        )
        keys_df = keys_df.set_index(index_name, drop=True)
        keys_df.index.name = None
        result = _perform_loc_list_join(series_or_dataframe, keys_df)
        pandas_result = result.to_pandas()
        # although loc[scalar_key] returns multiple results when scalar_key
        # is not unique, we download the results here and return the computed
        # individual result (as a scalar or pandas series) when the key is unique,
        # since we expect unique index keys to be more common. loc[[scalar_key]]
        # can be used to retrieve one-item DataFrames or Series.
        if len(pandas_result) == 1:
            return pandas_result.iloc[0]
        # when the key is not unique, we return a bigframes data type
        # as usual for methods that return dataframes/series
        return result
    else:
        raise TypeError(
            "Invalid argument type. Expected bigframes.Series, bigframes.Index, "
            "list, : (empty slice), or scalar. "
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
    series_or_dataframe: Union[bigframes.dataframe.DataFrame, bigframes.series.Series],
    keys_df: bigframes.dataframe.DataFrame,
) -> Union[bigframes.series.Series, bigframes.dataframe.DataFrame]:
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
) -> Union[bigframes.series.Series, bigframes.core.scalar.Scalar]:
    ...


@typing.overload
def _iloc_getitem_series_or_dataframe(
    series_or_dataframe: bigframes.dataframe.DataFrame, key
) -> Union[bigframes.dataframe.DataFrame, pd.Series]:
    ...


def _iloc_getitem_series_or_dataframe(
    series_or_dataframe: Union[bigframes.dataframe.DataFrame, bigframes.series.Series],
    key,
) -> Union[
    bigframes.dataframe.DataFrame,
    bigframes.series.Series,
    bigframes.core.scalar.Scalar,
    pd.Series,
]:
    if isinstance(key, int):
        internal_slice_result = series_or_dataframe._slice(key, key + 1, 1)
        result_pd_df = internal_slice_result.to_pandas()
        if result_pd_df.empty:
            raise IndexError("single positional indexer is out-of-bounds")
        return result_pd_df.iloc[0]
    elif isinstance(key, slice):
        return series_or_dataframe._slice(key.start, key.stop, key.step)
    elif isinstance(key, tuple) and len(key) == 0:
        return series_or_dataframe
    elif isinstance(key, tuple) and len(key) == 1:
        return _iloc_getitem_series_or_dataframe(series_or_dataframe, key[0])
    elif (
        isinstance(key, tuple)
        and isinstance(series_or_dataframe, bigframes.dataframe.DataFrame)
        and len(key) == 2
    ):
        return series_or_dataframe.iat[key]
    elif isinstance(key, tuple):
        raise pd.errors.IndexingError("Too many indexers")
    elif pd.api.types.is_list_like(key):
        if len(key) == 0:
            return typing.cast(
                Union[bigframes.dataframe.DataFrame, bigframes.series.Series],
                series_or_dataframe.iloc[0:0],
            )
        df = series_or_dataframe
        if isinstance(series_or_dataframe, bigframes.series.Series):
            original_series_name = series_or_dataframe.name
            series_name = (
                original_series_name if original_series_name is not None else "0"
            )
            df = series_or_dataframe.to_frame()
        original_index_names = df.index.names
        temporary_index_names = [
            guid.generate_guid(prefix="temp_iloc_index_")
            for _ in range(len(df.index.names))
        ]
        df = df.rename_axis(temporary_index_names)

        # set to offset index and use regular loc, then restore index
        df = df.reset_index(drop=False)
        result = df.loc[key]
        result = result.set_index(temporary_index_names)
        result = result.rename_axis(original_index_names)

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
