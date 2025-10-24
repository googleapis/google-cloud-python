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
BigFrames -> Polars compilation for the operations in bigframes.operations.numeric_ops.

Please keep implementations in sequential order by op name.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import bigframes.core.compile.polars.compiler as polars_compiler
from bigframes.operations import numeric_ops

if TYPE_CHECKING:
    import polars as pl


@polars_compiler.register_op(numeric_ops.CosOp)
def cos_op_impl(
    compiler: polars_compiler.PolarsExpressionCompiler,
    op: numeric_ops.CosOp,  # type: ignore
    input: pl.Expr,
) -> pl.Expr:
    return input.cos()


@polars_compiler.register_op(numeric_ops.LnOp)
def ln_op_impl(
    compiler: polars_compiler.PolarsExpressionCompiler,
    op: numeric_ops.LnOp,  # type: ignore
    input: pl.Expr,
) -> pl.Expr:
    import polars as pl

    return pl.when(input <= 0).then(float("nan")).otherwise(input.log())


@polars_compiler.register_op(numeric_ops.Log10Op)
def log10_op_impl(
    compiler: polars_compiler.PolarsExpressionCompiler,
    op: numeric_ops.Log10Op,  # type: ignore
    input: pl.Expr,
) -> pl.Expr:
    import polars as pl

    return pl.when(input <= 0).then(float("nan")).otherwise(input.log(base=10))


@polars_compiler.register_op(numeric_ops.Log1pOp)
def log1p_op_impl(
    compiler: polars_compiler.PolarsExpressionCompiler,
    op: numeric_ops.Log1pOp,  # type: ignore
    input: pl.Expr,
) -> pl.Expr:
    import polars as pl

    return pl.when(input <= -1).then(float("nan")).otherwise((input + 1).log())


@polars_compiler.register_op(numeric_ops.SinOp)
def sin_op_impl(
    compiler: polars_compiler.PolarsExpressionCompiler,
    op: numeric_ops.SinOp,  # type: ignore
    input: pl.Expr,
) -> pl.Expr:
    return input.sin()


@polars_compiler.register_op(numeric_ops.SqrtOp)
def sqrt_op_impl(
    compiler: polars_compiler.PolarsExpressionCompiler,
    op: numeric_ops.SqrtOp,  # type: ignore
    input: pl.Expr,
) -> pl.Expr:
    import polars as pl

    return pl.when(input < 0).then(float("nan")).otherwise(input.sqrt())


@polars_compiler.register_op(numeric_ops.IsNanOp)
def is_nan_op_impl(
    compiler: polars_compiler.PolarsExpressionCompiler,
    op: numeric_ops.IsNanOp,  # type: ignore
    input: pl.Expr,
) -> pl.Expr:
    return input.is_nan()


@polars_compiler.register_op(numeric_ops.IsFiniteOp)
def is_finite_op_impl(
    compiler: polars_compiler.PolarsExpressionCompiler,
    op: numeric_ops.IsFiniteOp,  # type: ignore
    input: pl.Expr,
) -> pl.Expr:
    return input.is_finite()
