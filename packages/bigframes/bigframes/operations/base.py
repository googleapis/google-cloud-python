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

import pandas as pd

import bigframes.constants as constants
import bigframes.core.blocks as blocks
import bigframes.core.scalar as scalars
import bigframes.dtypes
import bigframes.operations as ops
import bigframes.series as series
import bigframes.session
import third_party.bigframes_vendored.pandas.pandas._typing as vendored_pandas_typing

# BigQuery has 1 MB query size limit, 5000 items shouldn't take more than 10% of this depending on data type.
# TODO(tbergeron): Convert to bytes-based limit
MAX_INLINE_SERIES_SIZE = 5000


class SeriesMethods:
    def __init__(
        self,
        data=None,
        index: vendored_pandas_typing.Axes | None = None,
        dtype: typing.Optional[
            bigframes.dtypes.DtypeString | bigframes.dtypes.Dtype
        ] = None,
        name: str | None = None,
        copy: typing.Optional[bool] = None,
        *,
        session: typing.Optional[bigframes.session.Session] = None,
    ):
        block = None
        if copy is not None and not copy:
            raise ValueError(
                f"Series constructor only supports copy=True. {constants.FEEDBACK_LINK}"
            )
        if isinstance(data, blocks.Block):
            assert len(data.value_columns) == 1
            assert len(data.column_labels) == 1
            block = data

        elif isinstance(data, SeriesMethods):
            block = data._get_block()

        if block:
            if name:
                if not isinstance(name, typing.Hashable):
                    raise ValueError(
                        f"BigQuery DataFrames only supports hashable series names. {constants.FEEDBACK_LINK}"
                    )
                block = block.with_column_labels([name])
            if index:
                raise NotImplementedError(
                    f"Series 'index' constructor parameter not supported when passing BigQuery-backed objects. {constants.FEEDBACK_LINK}"
                )
            if dtype:
                block = block.multi_apply_unary_op(
                    block.value_columns, ops.AsTypeOp(dtype)
                )
            self._block = block

        else:
            import bigframes.pandas

            pd_series = pd.Series(
                data=data, index=index, dtype=dtype, name=name  # type:ignore
            )
            pd_dataframe = pd_series.to_frame()
            if pd_series.name is None:
                # to_frame will set default numeric column label if unnamed, but we do not support int column label, so must rename
                pd_dataframe = pd_dataframe.set_axis(["unnamed_col"], axis=1)
            if (
                pd_dataframe.size < MAX_INLINE_SERIES_SIZE
                # TODO(swast): Workaround data types limitation in inline data.
                and not any(
                    dt.pyarrow_dtype
                    for dt in pd_dataframe.dtypes
                    if isinstance(dt, pd.ArrowDtype)
                )
            ):
                self._block = blocks.block_from_local(pd_dataframe)
            elif session:
                self._block = session.read_pandas(pd_dataframe)._get_block()
            else:
                # Uses default global session
                self._block = bigframes.pandas.read_pandas(pd_dataframe)._get_block()
            if pd_series.name is None:
                self._block = self._block.with_column_labels([None])

    @property
    def _value_column(self) -> str:
        return self._block.value_columns[0]

    @property
    def _name(self) -> blocks.Label:
        return self._block.column_labels[0]

    @property
    def _dtype(self):
        return self._block.dtypes[0]

    def _set_block(self, block: blocks.Block):
        self._block = block

    def _get_block(self) -> blocks.Block:
        return self._block

    def _apply_unary_op(
        self,
        op: ops.UnaryOp,
    ) -> series.Series:
        """Applies a unary operator to the series."""
        block, result_id = self._block.apply_unary_op(
            self._value_column, op, result_label=self._name
        )
        return series.Series(block.select_column(result_id))

    def _apply_binary_op(
        self,
        other: typing.Any,
        op: ops.BinaryOp,
        alignment: typing.Literal["outer", "left"] = "outer",
    ) -> series.Series:
        """Applies a binary operator to the series and other."""
        if isinstance(other, pd.Series):
            # TODO: Convert to BigQuery DataFrames series
            raise NotImplementedError(
                f"Pandas series not supported as operand. {constants.FEEDBACK_LINK}"
            )
        if isinstance(other, series.Series):
            (left, right, block) = self._align(other, how=alignment)

            block, result_id = block.apply_binary_op(
                left, right, op, self._value_column
            )

            name = self._name
            if (
                isinstance(other, series.Series)
                and other.name != self._name
                and alignment == "outer"
            ):
                name = None

            return series.Series(
                block.select_column(result_id).assign_label(result_id, name)
            )
        else:
            partial_op = ops.BinopPartialRight(op, other)
            return self._apply_unary_op(partial_op)

    def _apply_corr_aggregation(self, other: series.Series) -> float:
        (left, right, block) = self._align(other, how="outer")

        return block.get_corr_stat(left, right)

    def _align(self, other: series.Series, how="outer") -> tuple[str, str, blocks.Block]:  # type: ignore
        """Aligns the series value with another scalar or series object. Returns new left column id, right column id and joined tabled expression."""
        values, block = self._align_n(
            [
                other,
            ],
            how,
        )
        return (values[0], values[1], block)

    def _align_n(
        self,
        others: typing.Sequence[typing.Union[series.Series, scalars.Scalar]],
        how="outer",
    ) -> tuple[typing.Sequence[str], blocks.Block]:
        value_ids = [self._value_column]
        block = self._block
        for other in others:
            if isinstance(other, series.Series):
                combined_index, (
                    get_column_left,
                    get_column_right,
                ) = block.index.join(other._block.index, how=how)
                value_ids = [
                    *[get_column_left[value] for value in value_ids],
                    get_column_right[other._value_column],
                ]
                block = combined_index._block
            else:
                # Will throw if can't interpret as scalar.
                dtype = typing.cast(bigframes.dtypes.Dtype, self._dtype)
                block, constant_col_id = block.create_constant(other, dtype=dtype)
                value_ids = [*value_ids, constant_col_id]
        return (value_ids, block)
