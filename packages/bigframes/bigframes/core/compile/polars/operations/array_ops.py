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

"""
BigFrames -> Polars compilation for the operations in bigframes.operations.array_ops.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import bigframes.core.compile.polars.compiler as polars_compiler
import bigframes.dtypes as dtypes
from bigframes.operations import generic_ops

if TYPE_CHECKING:
    import polars as pl


@polars_compiler.register_op(generic_ops.GetItemOp)
def getitem_op_impl(
    compiler: polars_compiler.PolarsExpressionCompiler,
    op: generic_ops.GetItemOp,  # type: ignore
    input: pl.Expr,
) -> pl.Expr:
    input_type = compiler._expr_types.get(id(input))
    if input_type is not None and dtypes.is_struct_like(input_type):
        if isinstance(op.key, str):
            return input.struct.field(op.key)
        else:
            raise NotImplementedError(
                "Referencing a struct field by number not implemented in polars compiler."
            )
    elif input_type is not None and dtypes.is_string_like(input_type):
        return input.str.slice(op.key, 1)
    else:
        return input.list.get(op.key)


@polars_compiler.register_op(generic_ops.DynamicGetItemOp)
def dynamic_getitem_op_impl(
    compiler: polars_compiler.PolarsExpressionCompiler,
    op: generic_ops.DynamicGetItemOp,  # type: ignore
    left: pl.Expr,
    right: pl.Expr,
) -> pl.Expr:
    left_type = compiler._expr_types.get(id(left))
    if left_type is not None and dtypes.is_string_like(left_type):
        return left.str.slice(right, 1)
    else:
        return left.list.get(right)
