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

import dataclasses
import functools
import itertools
import operator
from typing import cast, Literal, Optional, Sequence, Tuple, TYPE_CHECKING

import pandas as pd

import bigframes.core
from bigframes.core import identifiers, nodes, ordering, window_spec
from bigframes.core.compile.polars import lowering
import bigframes.core.expression as ex
import bigframes.core.guid as guid
import bigframes.core.rewrite
import bigframes.core.rewrite.schema_binding
import bigframes.dtypes
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops
import bigframes.operations.bool_ops as bool_ops
import bigframes.operations.comparison_ops as comp_ops
import bigframes.operations.generic_ops as gen_ops
import bigframes.operations.numeric_ops as num_ops

polars_installed = True
if TYPE_CHECKING:
    import polars as pl
else:
    try:
        import polars as pl
    except Exception:
        polars_installed = False

if polars_installed:
    _DTYPE_MAPPING = {
        # Direct mappings
        bigframes.dtypes.INT_DTYPE: pl.Int64(),
        bigframes.dtypes.FLOAT_DTYPE: pl.Float64(),
        bigframes.dtypes.BOOL_DTYPE: pl.Boolean(),
        bigframes.dtypes.STRING_DTYPE: pl.String(),
        bigframes.dtypes.NUMERIC_DTYPE: pl.Decimal(38, 9),
        bigframes.dtypes.BIGNUMERIC_DTYPE: pl.Decimal(76, 38),
        bigframes.dtypes.BYTES_DTYPE: pl.Binary(),
        bigframes.dtypes.DATE_DTYPE: pl.Date(),
        bigframes.dtypes.DATETIME_DTYPE: pl.Datetime(time_zone=None),
        bigframes.dtypes.TIMESTAMP_DTYPE: pl.Datetime(time_zone="UTC"),
        bigframes.dtypes.TIME_DTYPE: pl.Time(),
        bigframes.dtypes.TIMEDELTA_DTYPE: pl.Duration(),
        # Indirect mappings
        bigframes.dtypes.GEO_DTYPE: pl.String(),
        bigframes.dtypes.JSON_DTYPE: pl.String(),
    }

    def _bigframes_dtype_to_polars_dtype(
        dtype: bigframes.dtypes.ExpressionType,
    ) -> pl.DataType:
        if dtype is None:
            return pl.Null()
        if bigframes.dtypes.is_struct_like(dtype):
            return pl.Struct(
                [
                    pl.Field(name, _bigframes_dtype_to_polars_dtype(type))
                    for name, type in bigframes.dtypes.get_struct_fields(dtype).items()
                ]
            )
        if bigframes.dtypes.is_array_like(dtype):
            return pl.Array(
                inner=_bigframes_dtype_to_polars_dtype(
                    bigframes.dtypes.get_array_inner_type(dtype)
                )
            )
        else:
            return _DTYPE_MAPPING[dtype]

    @dataclasses.dataclass(frozen=True)
    class PolarsExpressionCompiler:
        """
        Simple compiler for converting bigframes expressions to polars expressions.

        Should be extended to dispatch based on bigframes schema types.
        """

        @functools.singledispatchmethod
        def compile_expression(self, expression: ex.Expression) -> pl.Expr:
            raise NotImplementedError(f"Cannot compile expression: {expression}")

        @compile_expression.register
        def _(
            self,
            expression: ex.ScalarConstantExpression,
        ) -> pl.Expr:
            value = expression.value
            if not isinstance(value, float) and pd.isna(value):  # type: ignore
                value = None
            if expression.dtype is None:
                return pl.lit(None)
            return pl.lit(value, _bigframes_dtype_to_polars_dtype(expression.dtype))

        @compile_expression.register
        def _(
            self,
            expression: ex.DerefOp,
        ) -> pl.Expr:
            return pl.col(expression.id.sql)

        @compile_expression.register
        def _(
            self,
            expression: ex.ResolvedDerefOp,
        ) -> pl.Expr:
            return pl.col(expression.id.sql)

        @compile_expression.register
        def _(
            self,
            expression: ex.OpExpression,
        ) -> pl.Expr:
            # TODO: Complete the implementation
            op = expression.op
            args = tuple(map(self.compile_expression, expression.inputs))
            return self.compile_op(op, *args)

        @functools.singledispatchmethod
        def compile_op(self, op: ops.ScalarOp, *args: pl.Expr) -> pl.Expr:
            raise NotImplementedError(f"Polars compiler hasn't implemented {op}")

        @compile_op.register(gen_ops.InvertOp)
        def _(self, op: ops.ScalarOp, input: pl.Expr) -> pl.Expr:
            return ~input

        @compile_op.register(num_ops.AbsOp)
        def _(self, op: ops.ScalarOp, input: pl.Expr) -> pl.Expr:
            return input.abs()

        @compile_op.register(num_ops.PosOp)
        def _(self, op: ops.ScalarOp, input: pl.Expr) -> pl.Expr:
            return input.__pos__()

        @compile_op.register(num_ops.NegOp)
        def _(self, op: ops.ScalarOp, input: pl.Expr) -> pl.Expr:
            return input.__neg__()

        @compile_op.register(bool_ops.AndOp)
        def _(self, op: ops.ScalarOp, l_input: pl.Expr, r_input: pl.Expr) -> pl.Expr:
            return l_input & r_input

        @compile_op.register(bool_ops.OrOp)
        def _(self, op: ops.ScalarOp, l_input: pl.Expr, r_input: pl.Expr) -> pl.Expr:
            return l_input | r_input

        @compile_op.register(num_ops.AddOp)
        def _(self, op: ops.ScalarOp, l_input: pl.Expr, r_input: pl.Expr) -> pl.Expr:
            return l_input + r_input

        @compile_op.register(num_ops.SubOp)
        def _(self, op: ops.ScalarOp, l_input: pl.Expr, r_input: pl.Expr) -> pl.Expr:
            return l_input - r_input

        @compile_op.register(num_ops.MulOp)
        def _(self, op: ops.ScalarOp, l_input: pl.Expr, r_input: pl.Expr) -> pl.Expr:
            return l_input * r_input

        @compile_op.register(num_ops.DivOp)
        def _(self, op: ops.ScalarOp, l_input: pl.Expr, r_input: pl.Expr) -> pl.Expr:
            return l_input / r_input

        @compile_op.register(num_ops.FloorDivOp)
        def _(self, op: ops.ScalarOp, l_input: pl.Expr, r_input: pl.Expr) -> pl.Expr:
            return l_input // r_input

        @compile_op.register(num_ops.FloorDivOp)
        def _(self, op: ops.ScalarOp, l_input: pl.Expr, r_input: pl.Expr) -> pl.Expr:
            return l_input // r_input

        @compile_op.register(num_ops.ModOp)
        def _(self, op: ops.ScalarOp, l_input: pl.Expr, r_input: pl.Expr) -> pl.Expr:
            return l_input % r_input

        @compile_op.register(num_ops.PowOp)
        @compile_op.register(num_ops.UnsafePowOp)
        def _(self, op: ops.ScalarOp, l_input: pl.Expr, r_input: pl.Expr) -> pl.Expr:
            return l_input**r_input

        @compile_op.register(comp_ops.EqOp)
        def _(self, op: ops.ScalarOp, l_input: pl.Expr, r_input: pl.Expr) -> pl.Expr:
            return l_input.eq(r_input)

        @compile_op.register(comp_ops.EqNullsMatchOp)
        def _(self, op: ops.ScalarOp, l_input: pl.Expr, r_input: pl.Expr) -> pl.Expr:
            return l_input.eq_missing(r_input)

        @compile_op.register(comp_ops.NeOp)
        def _(self, op: ops.ScalarOp, l_input: pl.Expr, r_input: pl.Expr) -> pl.Expr:
            return l_input.ne(r_input)

        @compile_op.register(comp_ops.GtOp)
        def _(self, op: ops.ScalarOp, l_input: pl.Expr, r_input: pl.Expr) -> pl.Expr:
            return l_input > r_input

        @compile_op.register(comp_ops.GeOp)
        def _(self, op: ops.ScalarOp, l_input: pl.Expr, r_input: pl.Expr) -> pl.Expr:
            return l_input >= r_input

        @compile_op.register(comp_ops.LtOp)
        def _(self, op: ops.ScalarOp, l_input: pl.Expr, r_input: pl.Expr) -> pl.Expr:
            return l_input < r_input

        @compile_op.register(comp_ops.LeOp)
        def _(self, op: ops.ScalarOp, l_input: pl.Expr, r_input: pl.Expr) -> pl.Expr:
            return l_input <= r_input

        @compile_op.register(gen_ops.IsInOp)
        def _(self, op: ops.ScalarOp, input: pl.Expr) -> pl.Expr:
            # TODO: Filter out types that can't be coerced to right type
            assert isinstance(op, gen_ops.IsInOp)
            if op.match_nulls or not any(map(pd.isna, op.values)):
                # newer polars version have nulls_equal arg
                return input.is_in(op.values)
            else:
                return input.is_in(op.values) or input.is_null()

        @compile_op.register(gen_ops.IsNullOp)
        def _(self, op: ops.ScalarOp, input: pl.Expr) -> pl.Expr:
            return input.is_null()

        @compile_op.register(gen_ops.NotNullOp)
        def _(self, op: ops.ScalarOp, input: pl.Expr) -> pl.Expr:
            return input.is_not_null()

        @compile_op.register(gen_ops.FillNaOp)
        @compile_op.register(gen_ops.CoalesceOp)
        def _(self, op: ops.ScalarOp, l_input: pl.Expr, r_input: pl.Expr) -> pl.Expr:
            return pl.coalesce(l_input, r_input)

        @compile_op.register(gen_ops.CaseWhenOp)
        def _(self, op: ops.ScalarOp, *inputs: pl.Expr) -> pl.Expr:
            expr = pl.when(inputs[0]).then(inputs[1])
            for pred, result in zip(inputs[2::2], inputs[3::2]):
                expr = expr.when(pred).then(result)  # type: ignore
            return expr

        @compile_op.register(gen_ops.WhereOp)
        def _(
            self,
            op: ops.ScalarOp,
            original: pl.Expr,
            condition: pl.Expr,
            otherwise: pl.Expr,
        ) -> pl.Expr:
            return pl.when(condition).then(original).otherwise(otherwise)

        @compile_op.register(gen_ops.AsTypeOp)
        def _(self, op: ops.ScalarOp, input: pl.Expr) -> pl.Expr:
            assert isinstance(op, gen_ops.AsTypeOp)
            # TODO: Polars casting works differently, need to lower instead to specific conversion ops.
            # eg. We want "True" instead of "true" for bool to strin
            return input.cast(_DTYPE_MAPPING[op.to_type], strict=not op.safe)

    @dataclasses.dataclass(frozen=True)
    class PolarsAggregateCompiler:
        scalar_compiler = PolarsExpressionCompiler()

        def get_args(
            self,
            agg: ex.Aggregation,
        ) -> Sequence[pl.Expr]:
            """Prepares arguments for aggregation by compiling them."""
            if isinstance(agg, ex.NullaryAggregation):
                return []
            elif isinstance(agg, ex.UnaryAggregation):
                arg = self.scalar_compiler.compile_expression(agg.arg)
                return [arg]
            elif isinstance(agg, ex.BinaryAggregation):
                larg = self.scalar_compiler.compile_expression(agg.left)
                rarg = self.scalar_compiler.compile_expression(agg.right)
                return [larg, rarg]

            raise NotImplementedError(
                f"Aggregation {agg} not yet supported in polars engine."
            )

        def compile_agg_expr(self, expr: ex.Aggregation):
            if isinstance(expr, ex.NullaryAggregation):
                inputs: Tuple = ()
            elif isinstance(expr, ex.UnaryAggregation):
                assert isinstance(expr.arg, ex.DerefOp)
                inputs = (expr.arg.id.sql,)
            elif isinstance(expr, ex.BinaryAggregation):
                assert isinstance(expr.left, ex.DerefOp)
                assert isinstance(expr.right, ex.DerefOp)
                inputs = (
                    expr.left.id.sql,
                    expr.right.id.sql,
                )
            else:
                raise ValueError(f"Unexpected aggregation: {expr.op}")

            return self.compile_agg_op(expr.op, inputs)

        def compile_agg_op(
            self, op: agg_ops.WindowOp, inputs: Sequence[str] = []
        ) -> pl.Expr:
            if isinstance(op, agg_ops.ProductOp):
                # TODO: Fix datatype inconsistency with float/int
                return pl.col(*inputs).product()
            if isinstance(op, agg_ops.SumOp):
                return pl.sum(*inputs)
            if isinstance(op, (agg_ops.SizeOp, agg_ops.SizeUnaryOp)):
                return pl.len()
            if isinstance(op, agg_ops.MeanOp):
                return pl.mean(*inputs)
            if isinstance(op, agg_ops.MedianOp):
                return pl.median(*inputs)
            if isinstance(op, agg_ops.AllOp):
                return pl.all(*inputs)
            if isinstance(op, agg_ops.AnyOp):
                return pl.any(*inputs)  # type: ignore
            if isinstance(op, agg_ops.NuniqueOp):
                return pl.col(*inputs).drop_nulls().n_unique()
            if isinstance(op, agg_ops.MinOp):
                return pl.min(*inputs)
            if isinstance(op, agg_ops.MaxOp):
                return pl.max(*inputs)
            if isinstance(op, agg_ops.CountOp):
                return pl.count(*inputs)
            if isinstance(op, agg_ops.CorrOp):
                return pl.corr(
                    pl.col(inputs[0]).fill_nan(None), pl.col(inputs[1]).fill_nan(None)
                )
            if isinstance(op, agg_ops.CovOp):
                return pl.cov(
                    pl.col(inputs[0]).fill_nan(None), pl.col(inputs[1]).fill_nan(None)
                )
            if isinstance(op, agg_ops.StdOp):
                return pl.std(inputs[0])
            if isinstance(op, agg_ops.VarOp):
                return pl.var(inputs[0])
            if isinstance(op, agg_ops.PopVarOp):
                return pl.var(inputs[0], ddof=0)
            if isinstance(op, agg_ops.FirstNonNullOp):
                return pl.col(*inputs).drop_nulls().first()
            if isinstance(op, agg_ops.LastNonNullOp):
                return pl.col(*inputs).drop_nulls().last()
            if isinstance(op, agg_ops.FirstOp):
                return pl.col(*inputs).first()
            if isinstance(op, agg_ops.LastOp):
                return pl.col(*inputs).last()
            if isinstance(op, agg_ops.ShiftOp):
                return pl.col(*inputs).shift(op.periods)
            if isinstance(op, agg_ops.DiffOp):
                return pl.col(*inputs) - pl.col(*inputs).shift(op.periods)
            if isinstance(op, agg_ops.AnyValueOp):
                return pl.max(
                    *inputs
                )  # probably something faster? maybe just get first item?
            raise NotImplementedError(
                f"Aggregate op {op} not yet supported in polars engine."
            )


@dataclasses.dataclass(frozen=True)
class PolarsCompiler:
    """
    Compiles ArrayValue to polars LazyFrame and executes.

    This feature is in development and is incomplete.
    While most node types are supported, this has the following limitations:
    1. GBQ data sources not supported.
    2. Joins do not order rows correctly
    3. Incomplete scalar op support
    4. Incomplete aggregate op support
    5. Incomplete analytic op support
    6. Some complex windowing types not supported (eg. groupby + rolling)
    7. UDFs are not supported.
    8. Returned types may not be entirely consistent with BigQuery backend
    9. Some operations are not entirely lazy - sampling and somse windowing.
    """

    expr_compiler = PolarsExpressionCompiler()
    agg_compiler = PolarsAggregateCompiler()

    def compile(self, plan: nodes.BigFrameNode) -> pl.LazyFrame:
        if not polars_installed:
            raise ValueError(
                "Polars is not installed, cannot compile to polars engine."
            )

        # TODO: Create standard way to configure BFET -> BFET rewrites
        # Polars has incomplete slice support in lazy mode
        node = plan
        node = bigframes.core.rewrite.column_pruning(node)
        node = nodes.bottom_up(node, bigframes.core.rewrite.rewrite_slice)
        node = bigframes.core.rewrite.pull_out_window_order(node)
        node = bigframes.core.rewrite.schema_binding.bind_schema_to_tree(node)
        node = lowering.lower_ops_to_polars(node)
        return self.compile_node(node)

    @functools.singledispatchmethod
    def compile_node(self, node: nodes.BigFrameNode) -> pl.LazyFrame:
        """Defines transformation but isn't cached, always use compile_node instead"""
        raise ValueError(f"Can't compile unrecognized node: {node}")

    @compile_node.register
    def compile_readlocal(self, node: nodes.ReadLocalNode):
        cols_to_read = {
            scan_item.source_id: scan_item.id.sql for scan_item in node.scan_list.items
        }
        lazy_frame = cast(
            pl.DataFrame, pl.from_arrow(node.local_data_source.data)
        ).lazy()
        lazy_frame = lazy_frame.select(cols_to_read.keys()).rename(cols_to_read)
        if node.offsets_col:
            lazy_frame = lazy_frame.with_columns(
                [pl.int_range(pl.len(), dtype=pl.Int64).alias(node.offsets_col.sql)]
            )
        return lazy_frame

    @compile_node.register
    def compile_filter(self, node: nodes.FilterNode):
        return self.compile_node(node.child).filter(
            self.expr_compiler.compile_expression(node.predicate)
        )

    @compile_node.register
    def compile_orderby(self, node: nodes.OrderByNode):
        frame = self.compile_node(node.child)
        if len(node.by) == 0:
            # pragma: no cover
            return frame
        return self._sort(frame, node.by)

    def _sort(
        self, frame: pl.LazyFrame, by: Sequence[ordering.OrderingExpression]
    ) -> pl.LazyFrame:
        sorted = frame.sort(
            [self.expr_compiler.compile_expression(by.scalar_expression) for by in by],
            descending=[not by.direction.is_ascending for by in by],
            nulls_last=[by.na_last for by in by],
            maintain_order=True,
        )
        return sorted

    @compile_node.register
    def compile_reversed(self, node: nodes.ReversedNode):
        return self.compile_node(node.child).reverse()

    @compile_node.register
    def compile_selection(self, node: nodes.SelectionNode):
        return self.compile_node(node.child).select(
            **{new.sql: orig.id.sql for orig, new in node.input_output_pairs}
        )

    @compile_node.register
    def compile_projection(self, node: nodes.ProjectionNode):
        new_cols = []
        for proj_expr, name in node.assignments:
            bound_expr = ex.bind_schema_fields(proj_expr, node.child.field_by_id)
            new_col = self.expr_compiler.compile_expression(bound_expr).alias(name.sql)
            if bound_expr.output_type is None:
                new_col = new_col.cast(
                    _bigframes_dtype_to_polars_dtype(bigframes.dtypes.DEFAULT_DTYPE)
                )
            new_cols.append(new_col)
        return self.compile_node(node.child).with_columns(new_cols)

    @compile_node.register
    def compile_offsets(self, node: nodes.PromoteOffsetsNode):
        return self.compile_node(node.child).with_columns(
            [pl.int_range(pl.len(), dtype=pl.Int64).alias(node.col_id.sql)]
        )

    @compile_node.register
    def compile_join(self, node: nodes.JoinNode):
        left = self.compile_node(node.left_child)
        right = self.compile_node(node.right_child)
        left_on = [l_name.id.sql for l_name, _ in node.conditions]
        right_on = [r_name.id.sql for _, r_name in node.conditions]
        if node.type == "right":
            return self._ordered_join(
                right, left, "left", right_on, left_on, node.joins_nulls
            ).select([id.sql for id in node.ids])
        return self._ordered_join(
            left, right, node.type, left_on, right_on, node.joins_nulls
        )

    def _ordered_join(
        self,
        left_frame: pl.LazyFrame,
        right_frame: pl.LazyFrame,
        how: Literal["inner", "outer", "left", "cross"],
        left_on: Sequence[str],
        right_on: Sequence[str],
        join_nulls: bool,
    ):
        if how == "right":
            # seems to cause seg faults as of v1.30 for no apparent reason
            raise ValueError("right join not supported")
        left = left_frame.with_columns(
            [
                pl.int_range(pl.len()).alias("_bf_join_l"),
            ]
        )
        right = right_frame.with_columns(
            [
                pl.int_range(pl.len()).alias("_bf_join_r"),
            ]
        )
        if how != "cross":
            joined = left.join(
                right,
                how=how,
                left_on=left_on,
                right_on=right_on,
                # Note: join_nulls renamed to nulls_equal for polars 1.24
                join_nulls=join_nulls,  # type: ignore
                coalesce=False,
            )
        else:
            joined = left.join(right, how=how, coalesce=False)

        join_order = (
            ["_bf_join_l", "_bf_join_r"]
            if how != "right"
            else ["_bf_join_r", "_bf_join_l"]
        )
        return joined.sort(join_order, nulls_last=True).drop(
            ["_bf_join_l", "_bf_join_r"]
        )

    @compile_node.register
    def compile_concat(self, node: nodes.ConcatNode):
        child_frames = [self.compile_node(child) for child in node.child_nodes]
        child_frames = [
            frame.rename(
                {col: id.sql for col, id in zip(frame.columns, node.output_ids)}
            )
            for frame in child_frames
        ]
        df = pl.concat(child_frames)
        return df

    @compile_node.register
    def compile_agg(self, node: nodes.AggregateNode):
        df = self.compile_node(node.child)
        if node.dropna and len(node.by_column_ids) > 0:
            df = df.filter(
                [pl.col(ref.id.sql).is_not_null() for ref in node.by_column_ids]
            )
        if node.order_by:
            df = self._sort(df, node.order_by)
        return self._aggregate(df, node.aggregations, node.by_column_ids)

    def _aggregate(
        self,
        df: pl.LazyFrame,
        aggregations: Sequence[Tuple[ex.Aggregation, identifiers.ColumnId]],
        grouping_keys: Tuple[ex.DerefOp, ...],
    ) -> pl.LazyFrame:
        # Need to materialize columns to broadcast constants
        agg_inputs = [
            list(
                map(
                    lambda x: x.alias(guid.generate_guid()),
                    self.agg_compiler.get_args(agg),
                )
            )
            for agg, _ in aggregations
        ]

        df_agg_inputs = df.with_columns(itertools.chain(*agg_inputs))

        agg_exprs = [
            self.agg_compiler.compile_agg_op(
                agg.op, list(map(lambda x: x.meta.output_name(), inputs))
            ).alias(id.sql)
            for (agg, id), inputs in zip(aggregations, agg_inputs)
        ]

        if len(grouping_keys) > 0:
            group_exprs = [pl.col(ref.id.sql) for ref in grouping_keys]
            grouped_df = df_agg_inputs.group_by(group_exprs)
            return grouped_df.agg(agg_exprs).sort(group_exprs, nulls_last=True)
        else:
            return df_agg_inputs.select(agg_exprs)

    @compile_node.register
    def compile_explode(self, node: nodes.ExplodeNode):
        assert node.offsets_col is None
        df = self.compile_node(node.child)
        cols = [pl.col(col.id.sql) for col in node.column_ids]
        return df.explode(cols)

    @compile_node.register
    def compile_sample(self, node: nodes.RandomSampleNode):
        df = self.compile_node(node.child)
        # Sample is not available on lazyframe
        return df.collect().sample(fraction=node.fraction).lazy()

    @compile_node.register
    def compile_window(self, node: nodes.WindowOpNode):
        df = self.compile_node(node.child)

        window = node.window_spec
        # Should have been handled by reweriter
        assert len(window.ordering) == 0
        if window.min_periods > 0:
            raise NotImplementedError("min_period not yet supported for polars engine")

        if (window.bounds is None) or (window.is_unbounded):
            # polars will automatically broadcast the aggregate to the matching input rows
            agg_pl = self.agg_compiler.compile_agg_expr(node.expression)
            if window.grouping_keys:
                agg_pl = agg_pl.over(id.id.sql for id in window.grouping_keys)
            result = df.with_columns(agg_pl.alias(node.output_name.sql))
        else:  # row-bounded window
            window_result = self._calc_row_analytic_func(
                df, node.expression, node.window_spec, node.output_name.sql
            )
            result = pl.concat([df, window_result], how="horizontal")

        # Probably easier just to pull this out as a rewriter
        if (
            node.expression.op.skips_nulls
            and not node.never_skip_nulls
            and node.expression.column_references
        ):
            nullity_expr = functools.reduce(
                operator.or_,
                (
                    pl.col(column.sql).is_null()
                    for column in node.expression.column_references
                ),
            )
            result = result.with_columns(
                pl.when(nullity_expr)
                .then(None)
                .otherwise(pl.col(node.output_name.sql))
                .alias(node.output_name.sql)
            )
        return result

    def _calc_row_analytic_func(
        self,
        frame: pl.LazyFrame,
        agg_expr: ex.Aggregation,
        window: window_spec.WindowSpec,
        name: str,
    ) -> pl.LazyFrame:
        if not isinstance(window.bounds, window_spec.RowsWindowBounds):
            raise NotImplementedError("Only row bounds supported by polars engine")
        groupby = None
        if len(window.grouping_keys) > 0:
            groupby = [
                self.expr_compiler.compile_expression(ref)
                for ref in window.grouping_keys
            ]

        # Polars API semi-bounded, and any grouped rolling window challenging
        # https://github.com/pola-rs/polars/issues/4799
        # https://github.com/pola-rs/polars/issues/8976
        pl_agg_expr = self.agg_compiler.compile_agg_expr(agg_expr).alias(name)
        index_col_name = "_bf_pl_engine_offsets"
        indexed_df = frame.with_row_index(index_col_name)
        # https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.rolling.html
        period_n, offset_n = _get_period_and_offset(window.bounds)
        return (
            indexed_df.rolling(
                index_column=index_col_name,
                period=f"{period_n}i",
                offset=f"{offset_n}i" if (offset_n is not None) else None,
                group_by=groupby,
            )
            .agg(pl_agg_expr)
            .select(name)
        )


def _get_period_and_offset(
    bounds: window_spec.RowsWindowBounds,
) -> tuple[int, Optional[int]]:
    # fixed size window
    if (bounds.start is not None) and (bounds.end is not None):
        return ((bounds.end - bounds.start + 1), bounds.start - 1)

    LARGE_N = 1000000000
    if bounds.start is not None:
        return (LARGE_N, bounds.start - 1)
    if bounds.end is not None:
        return (LARGE_N, None)
    raise ValueError("Not a bounded window")
