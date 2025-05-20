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
from typing import List, Sequence, Union

import bigframes_vendored.constants as constants
import bigframes_vendored.pandas.pandas._typing as vendored_pandas_typing
import pandas as pd

import bigframes.core.blocks as blocks
import bigframes.core.convert
import bigframes.core.expression as ex
import bigframes.core.identifiers as ids
import bigframes.core.indexes as indexes
import bigframes.core.scalar as scalars
import bigframes.core.utils as bf_utils
import bigframes.dtypes
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops
import bigframes.series as series
import bigframes.session


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
        import bigframes.pandas

        # Ignore object dtype if provided, as it provides no additional
        # information about what BigQuery type to use.
        if dtype is not None and bigframes.dtypes.is_object_like(dtype):
            dtype = None

        read_pandas_func = (
            session.read_pandas
            if (session is not None)
            else (lambda x: bigframes.pandas.read_pandas(x))
        )

        block: typing.Optional[blocks.Block] = None
        if (name is not None) and not isinstance(name, typing.Hashable):
            raise ValueError(
                f"BigQuery DataFrames only supports hashable series names. {constants.FEEDBACK_LINK}"
            )
        if copy is not None and not copy:
            raise ValueError(
                f"Series constructor only supports copy=True. {constants.FEEDBACK_LINK}"
            )

        if isinstance(data, blocks.Block):
            block = data
        elif isinstance(data, SeriesMethods):
            block = data._get_block()
        # special case where data is local scalar, but index is bigframes index (maybe very big)
        elif (
            not bf_utils.is_list_like(data) and not isinstance(data, indexes.Index)
        ) and isinstance(index, indexes.Index):
            block = index._block
            block, _ = block.create_constant(data)
            block = block.with_column_labels([None])
            # prevents no-op reindex later
            index = None
        elif isinstance(data, indexes.Index) or isinstance(index, indexes.Index):
            data = indexes.Index(data, dtype=dtype, name=name, session=session)
            # set to none as it has already been applied, avoid re-cast later
            if data.nlevels != 1:
                raise NotImplementedError("Cannot interpret multi-index as Series.")
            # Reset index to promote index columns to value columns, set default index
            data_block = data._block.reset_index(drop=False).with_column_labels(
                data.names
            )
            if index is not None:  # Align data and index by offset
                bf_index = indexes.Index(index, session=session)
                idx_block = bf_index._block.reset_index(
                    drop=False
                )  # reset to align by offsets, and then reset back
                idx_cols = idx_block.value_columns
                data_block, (l_mapping, _) = idx_block.join(data_block, how="left")
                data_block = data_block.set_index([l_mapping[col] for col in idx_cols])
                data_block = data_block.with_index_labels(bf_index.names)
                # prevents no-op reindex later
                index = None
            block = data_block

        if block:
            assert len(block.value_columns) == 1
            assert len(block.column_labels) == 1
            if index is not None:  # reindexing operation
                bf_index = indexes.Index(index)
                idx_block = bf_index._block
                idx_cols = idx_block.index_columns
                block, _ = idx_block.join(block, how="left")
                block = block.with_index_labels(bf_index.names)
            if name:
                block = block.with_column_labels([name])
            if dtype:
                bf_dtype = bigframes.dtypes.bigframes_type(dtype)
                block = block.multi_apply_unary_op(ops.AsTypeOp(to_type=bf_dtype))
        else:
            pd_series = pd.Series(
                data=data,
                index=index,  # type:ignore
                dtype=dtype,  # type:ignore
                name=name,
            )
            block = read_pandas_func(pd_series)._get_block()  # type:ignore

        assert block is not None
        self._block: blocks.Block = block

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
        reverse: bool = False,
    ) -> series.Series:
        """Applies a binary operator to the series and other."""
        if bigframes.core.convert.can_convert_to_series(other):
            self_index = indexes.Index(self._block)
            other_series = bigframes.core.convert.to_bf_series(
                other, self_index, self._block.session
            )
            (self_col, other_col, block) = self._align(other_series, how=alignment)

            name = self._name
            # Drop name if both objects have name attr, but they don't match
            if (
                hasattr(other, "name")
                and other_series.name != self._name
                and alignment == "outer"
            ):
                name = None
            expr = op.as_expr(
                other_col if reverse else self_col, self_col if reverse else other_col
            )
            block, result_id = block.project_expr(expr, name)
            return series.Series(block.select_column(result_id))

        else:  # Scalar binop
            name = self._name
            expr = op.as_expr(
                ex.const(other) if reverse else self._value_column,
                self._value_column if reverse else ex.const(other),
            )
            block, result_id = self._block.project_expr(expr, name)
            return series.Series(block.select_column(result_id))

    def _apply_nary_op(
        self,
        op: ops.NaryOp,
        others: Sequence[typing.Union[series.Series, scalars.Scalar]],
        ignore_self=False,
    ):
        """Applies an n-ary operator to the series and others."""
        values, block = self._align_n(
            others, ignore_self=ignore_self, cast_scalars=False
        )
        block, result_id = block.project_expr(op.as_expr(*values))
        return series.Series(block.select_column(result_id))

    def _apply_binary_aggregation(
        self, other: series.Series, stat: agg_ops.BinaryAggregateOp
    ) -> float:
        (left, right, block) = self._align(other, how="outer")
        assert isinstance(left, ex.DerefOp)
        assert isinstance(right, ex.DerefOp)
        return block.get_binary_stat(left.id.name, right.id.name, stat)

    AlignedExprT = Union[ex.ScalarConstantExpression, ex.DerefOp]

    @typing.overload
    def _align(
        self, other: series.Series, how="outer"
    ) -> tuple[ex.DerefOp, ex.DerefOp, blocks.Block,]:
        ...

    @typing.overload
    def _align(
        self, other: typing.Union[series.Series, scalars.Scalar], how="outer"
    ) -> tuple[ex.DerefOp, AlignedExprT, blocks.Block,]:
        ...

    def _align(
        self, other: typing.Union[series.Series, scalars.Scalar], how="outer"
    ) -> tuple[ex.DerefOp, AlignedExprT, blocks.Block,]:
        """Aligns the series value with another scalar or series object. Returns new left column id, right column id and joined tabled expression."""
        values, block = self._align_n(
            [
                other,
            ],
            how,
        )
        return (typing.cast(ex.DerefOp, values[0]), values[1], block)

    def _align3(self, other1: series.Series | scalars.Scalar, other2: series.Series | scalars.Scalar, how="left", cast_scalars: bool = True) -> tuple[ex.DerefOp, AlignedExprT, AlignedExprT, blocks.Block]:  # type: ignore
        """Aligns the series value with 2 other scalars or series objects. Returns new values and joined tabled expression."""
        values, index = self._align_n([other1, other2], how, cast_scalars=cast_scalars)
        return (
            typing.cast(ex.DerefOp, values[0]),
            values[1],
            values[2],
            index,
        )

    def _align_n(
        self,
        others: typing.Sequence[typing.Union[series.Series, scalars.Scalar]],
        how="outer",
        ignore_self=False,
        cast_scalars: bool = False,
    ) -> tuple[
        typing.Sequence[Union[ex.ScalarConstantExpression, ex.DerefOp]],
        blocks.Block,
    ]:
        if ignore_self:
            value_ids: List[Union[ex.ScalarConstantExpression, ex.DerefOp]] = []
        else:
            value_ids = [ex.deref(self._value_column)]

        block = self._block
        for other in others:
            if isinstance(other, series.Series):
                block, (
                    get_column_left,
                    get_column_right,
                ) = block.join(other._block, how=how)
                rebindings = {
                    ids.ColumnId(old): ids.ColumnId(new)
                    for old, new in get_column_left.items()
                }
                remapped_value_ids = (
                    value.remap_column_refs(rebindings) for value in value_ids
                )
                value_ids = [
                    *remapped_value_ids,  # type: ignore
                    ex.deref(get_column_right[other._value_column]),
                ]
            else:
                # Will throw if can't interpret as scalar.
                dtype = typing.cast(bigframes.dtypes.Dtype, self._dtype)
                value_ids = [
                    *value_ids,
                    ex.const(other, dtype=dtype if cast_scalars else None),
                ]
        return (value_ids, block)

    def _throw_if_null_index(self, opname: str):
        if len(self._block.index_columns) == 0:
            raise bigframes.exceptions.NullIndexError(
                f"Series cannot perform {opname} as it has no index. Set an index using set_index."
            )
