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

import typing

import bigframes_vendored.constants as constants
import bigframes_vendored.pandas.core.reshape.tile as vendored_pandas_tile
import pandas as pd

import bigframes.constants
import bigframes.core.expression as ex
import bigframes.core.ordering as order
import bigframes.core.utils as utils
import bigframes.core.window_spec as window_specs
import bigframes.dataframe
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops
import bigframes.series


def cut(
    x: bigframes.series.Series,
    bins: typing.Union[
        int,
        pd.IntervalIndex,
        typing.Iterable,
    ],
    *,
    right: typing.Optional[bool] = True,
    labels: typing.Union[typing.Iterable[str], bool, None] = None,
) -> bigframes.series.Series:
    if (
        labels is not None
        and labels is not False
        and not isinstance(labels, typing.Iterable)
    ):
        raise ValueError(
            "Bin labels must either be False, None or passed in as a list-like argument"
        )
    if (
        isinstance(labels, typing.Iterable)
        and len(list(labels)) > 0
        and not isinstance(list(labels)[0], str)
    ):
        raise NotImplementedError(
            "When using an iterable for labels, only iterables of strings are supported "
            f"but found {type(list(labels)[0])}. {constants.FEEDBACK_LINK}"
        )

    if x.size == 0:
        raise ValueError("Cannot cut empty array.")

    if isinstance(bins, int):
        if bins <= 0:
            raise ValueError("`bins` should be a positive integer.")
        if isinstance(labels, typing.Iterable):
            labels = tuple(labels)
            if len(labels) != bins:
                raise ValueError(
                    f"Bin labels({len(labels)}) must be same as the value of bins({bins})"
                )

        op = agg_ops.CutOp(bins, right=right, labels=labels)
        return x._apply_window_op(op, window_spec=window_specs.unbound())
    elif isinstance(bins, typing.Iterable):
        if isinstance(bins, pd.IntervalIndex):
            as_index: pd.IntervalIndex = bins
            bins = tuple((bin.left.item(), bin.right.item()) for bin in bins)
            # To maintain consistency with pandas' behavior
            right = True
            labels = None
        elif len(list(bins)) == 0:
            as_index = pd.IntervalIndex.from_tuples(list(bins))
            bins = tuple()
        elif isinstance(list(bins)[0], tuple):
            as_index = pd.IntervalIndex.from_tuples(list(bins))
            bins = tuple(bins)
            # To maintain consistency with pandas' behavior
            right = True
            labels = None
        elif pd.api.types.is_number(list(bins)[0]):
            bins_list = list(bins)
            as_index = pd.IntervalIndex.from_breaks(bins_list)
            single_type = all([isinstance(n, type(bins_list[0])) for n in bins_list])
            numeric_type = type(bins_list[0]) if single_type else float
            bins = tuple(
                [
                    (numeric_type(bins_list[i]), numeric_type(bins_list[i + 1]))
                    for i in range(len(bins_list) - 1)
                ]
            )
        else:
            raise ValueError("`bins` iterable should contain tuples or numerics.")

        if as_index.is_overlapping:
            raise ValueError("Overlapping IntervalIndex is not accepted.")  # TODO: test

        if isinstance(labels, typing.Iterable):
            labels = tuple(labels)
            if len(labels) != len(as_index):
                raise ValueError(
                    f"Bin labels({len(labels)}) must be same as the number of bin edges"
                    f"({len(as_index)})"
                )

        if len(as_index) == 0:
            dtype = agg_ops.CutOp(bins, right=right, labels=labels).output_type()
            return bigframes.series.Series(
                [pd.NA] * len(x),
                dtype=dtype,
                name=x.name,
                index=x.index,
                session=x._session,
            )
        else:
            op = agg_ops.CutOp(bins, right=right, labels=labels)
            return x._apply_window_op(op, window_spec=window_specs.unbound())
    else:
        raise ValueError("`bins` must be an integer or interable.")


cut.__doc__ = vendored_pandas_tile.cut.__doc__


def qcut(
    x: bigframes.series.Series,
    q: typing.Union[int, typing.Sequence[float]],
    *,
    labels: typing.Optional[bool] = None,
    duplicates: typing.Literal["drop", "error"] = "error",
) -> bigframes.series.Series:
    if isinstance(q, int) and q <= 0:
        raise ValueError("`q` should be a positive integer.")
    if utils.is_list_like(q):
        q = tuple(q)

    if labels is not False:
        raise NotImplementedError(
            f"Only labels=False is supported in BigQuery DataFrames so far. {constants.FEEDBACK_LINK}"
        )
    if duplicates != "drop":
        raise NotImplementedError(
            f"Only duplicates='drop' is supported in BigQuery DataFrames so far. {constants.FEEDBACK_LINK}"
        )
    block = x._block
    label = block.col_id_to_label[x._value_column]
    block, nullity_id = block.apply_unary_op(x._value_column, ops.notnull_op)
    block, result = block.apply_window_op(
        x._value_column,
        agg_ops.QcutOp(q),  # type: ignore
        window_spec=window_specs.unbound(
            grouping_keys=(nullity_id,),
            ordering=(order.ascending_over(x._value_column),),
        ),
    )
    block, result = block.project_expr(
        ops.where_op.as_expr(result, nullity_id, ex.const(None)), label=label
    )
    return bigframes.series.Series(block.select_column(result))


qcut.__doc__ = vendored_pandas_tile.qcut.__doc__
