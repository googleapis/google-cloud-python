# Copyright 2026 Google LLC
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
from typing import Any, Dict, Sequence, Tuple, Union

import bigframes.core.expression as ex
import bigframes.core.identifiers as ids
from bigframes.core.blocks import Block


def align_n(
    objects: Sequence[Any],
    how: typing.Literal["inner", "left", "outer", "right", "cross"] = "outer",
) -> Tuple[Sequence[Any], Block]:
    """Aligns a list of mixed Series-like, Index-like, and scalar values.

    Returns the list of mapped Expression objects corresponding to the aligned columns/constants,
    along with the joined Block representing the aligned data.
    """
    import bigframes.core.indexes as bf_indexes
    import bigframes.series as bf_series

    # Find the first Series or Index object to serve as reference
    ref_obj = None
    for obj in objects:
        if isinstance(obj, (bf_series.Series, bf_indexes.Index)):
            ref_obj = obj
            break

    if ref_obj is None:
        raise ValueError("At least one input must be a BigFrames Series or Index object.")

    block = ref_obj._block
    series_to_expr = {id(ref_obj): ex.deref(ref_obj._value_column)}

    # Collect all other unique Series and Index objects
    all_block_likes = []
    for obj in objects:
        if isinstance(obj, (bf_series.Series, bf_indexes.Index)) and id(obj) not in series_to_expr:
            all_block_likes.append(obj)
            series_to_expr[id(obj)] = None

    # Join Series/Index objects one by one
    for s in all_block_likes:
        (
            block,
            (
                get_column_left,
                get_column_right,
            ),
        ) = block.join(s._block, how=how)

        # Remap existing expressions
        rebindings = {
            ids.ColumnId(old): ids.ColumnId(new)
            for old, new in get_column_left.items()
        }
        for oid, expr in series_to_expr.items():
            if expr is not None:
                series_to_expr[oid] = expr.remap_column_refs(rebindings)

        # Assign expression for newly joined Series/Index
        new_col_id = get_column_right[s._value_column]
        series_to_expr[id(s)] = ex.deref(new_col_id)

    # Build the final list of aligned expressions/scalars
    final_exprs = []
    for obj in objects:
        if isinstance(obj, (bf_series.Series, bf_indexes.Index)):
            final_exprs.append(series_to_expr[id(obj)])
        else:
            final_exprs.append(obj)

    return final_exprs, block


def apply_op(
    op: Any,  # Any ops.NaryOp type to prevent circular import
    args: Sequence[Any] = (),
    kwargs: Dict[str, Any] = {},
) -> Any:
    """Applies an operation to a mix of Series, Index, literal, and other values, with necessary alignment."""
    import bigframes.core.convert as bf_convert
    import bigframes.core.indexes as bf_indexes
    import bigframes.series as bf_series

    # Find a reference block-like object in the inputs
    ref_obj = None
    for arg in args:
        if isinstance(arg, (bf_series.Series, bf_indexes.Index)):
            ref_obj = arg
            break
    if ref_obj is None:
        for val in kwargs.values():
            if isinstance(val, (bf_series.Series, bf_indexes.Index)):
                ref_obj = val
                break

    if ref_obj is None:
        raise ValueError("At least one input must be a BigFrames Series or Index.")

    session = ref_obj._block.session
    ref_index = ref_obj.index

    # Convert inputs that are list-like or pandas Series/Index to BigFrames Series
    def convert_input(val):
        if isinstance(val, (bf_series.Series, bf_indexes.Index)):
            return val
        elif bf_convert.can_convert_to_series(val):
            return bf_convert.to_bf_series(val, ref_index, session)
        else:
            return val

    converted_args = [convert_input(arg) for arg in args]
    converted_kwargs = {k: convert_input(v) for k, v in kwargs.items()}

    # Collect all inputs for alignment
    alignment_inputs = []
    for arg in converted_args:
        alignment_inputs.append(arg)
    for val in converted_kwargs.values():
        alignment_inputs.append(val)

    # Perform core alignment
    aligned_inputs, block = align_n(alignment_inputs, how="outer")

    # Map the aligned expressions back to args and kwargs, wrapping any remaining raw scalars as ex.const
    final_args = []
    cursor = 0
    for arg in converted_args:
        expr = aligned_inputs[cursor]
        if not isinstance(expr, ex.Expression):
            expr = ex.const(expr)
        final_args.append(expr)
        cursor += 1

    final_kwargs = {}
    for k, v in converted_kwargs.items():
        expr = aligned_inputs[cursor]
        if not isinstance(expr, ex.Expression):
            expr = ex.const(expr)
        final_kwargs[k] = expr
        cursor += 1

    # Apply the operation and construct the result
    expr = op.as_expr(*final_args, **final_kwargs)
    block, result_id = block.project_expr(expr)

    # Depending on the type of the reference object, return Series or Index
    if isinstance(ref_obj, bf_series.Series):
        return bf_series.Series(block.select_column(result_id))
    else:
        return bf_indexes.Index(block.select_column(result_id))
