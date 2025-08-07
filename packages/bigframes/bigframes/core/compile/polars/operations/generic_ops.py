# Copyright 2025 Google LLC
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
BigFrames -> Polars compilation for the operations in bigframes.operations.generic_ops.

Please keep implementations in sequential order by op name.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import bigframes.core.compile.polars.compiler as polars_compiler
from bigframes.operations import generic_ops

if TYPE_CHECKING:
    import polars as pl


@polars_compiler.register_op(generic_ops.NotNullOp)
def notnull_op_impl(
    compiler: polars_compiler.PolarsExpressionCompiler,
    op: generic_ops.NotNullOp,  # type: ignore
    input: pl.Expr,
) -> pl.Expr:
    return input.is_not_null()


@polars_compiler.register_op(generic_ops.IsNullOp)
def isnull_op_impl(
    compiler: polars_compiler.PolarsExpressionCompiler,
    op: generic_ops.IsNullOp,  # type: ignore
    input: pl.Expr,
) -> pl.Expr:
    return input.is_null()
