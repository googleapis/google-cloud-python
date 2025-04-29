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
from typing import cast, Optional, Sequence, Tuple, TYPE_CHECKING

import bigframes.core
from bigframes.core import window_spec
import bigframes.core.expression as ex
import bigframes.core.guid as guid
import bigframes.core.nodes as nodes
import bigframes.core.rewrite
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops

polars_installed = True
if TYPE_CHECKING:
    import polars as pl
else:
    try:
        import polars as pl
    except Exception:
        polars_installed = False

if polars_installed:

    @dataclasses.dataclass(frozen=True)
    class PolarsExpressionCompiler:
        """
        Simple compiler for converting bigframes expressions to polars expressions.

        Should be extended to dispatch based on bigframes schema types.
        """

        @functools.singledispatchmethod
        def compile_expression(self, expression: ex.Expression):
            raise NotImplementedError(f"Cannot compile expression: {expression}")

        @compile_expression.register
        def _(
            self,
            expression: ex.ScalarConstantExpression,
        ):
            return pl.lit(expression.value)

        @compile_expression.register
        def _(
            self,
            expression: ex.DerefOp,
        ):
            return pl.col(expression.id.sql)

        @compile_expression.register
        def _(
            self,
            expression: ex.OpExpression,
        ):
            # TODO: Complete the implementation, convert to hash dispatch
            op = expression.op
            args = tuple(map(self.compile_expression, expression.inputs))
            if isinstance(op, ops.invert_op.__class__):
                return args[0].neg()
            if isinstance(op, ops.and_op.__class__):
                return args[0] & args[1]
            if isinstance(op, ops.or_op.__class__):
                return args[0] | args[1]
            if isinstance(op, ops.add_op.__class__):
                return args[0] + args[1]
            if isinstance(op, ops.sub_op.__class__):
                return args[0] - args[1]
            if isinstance(op, ops.ge_op.__class__):
                return args[0] >= args[1]
            if isinstance(op, ops.gt_op.__class__):
                return args[0] > args[1]
            if isinstance(op, ops.le_op.__class__):
                return args[0] <= args[1]
            if isinstance(op, ops.lt_op.__class__):
                return args[0] < args[1]
            if isinstance(op, ops.eq_op.__class__):
                return args[0] == args[1]
            if isinstance(op, ops.mod_op.__class__):
                return args[0] % args[1]
            if isinstance(op, ops.coalesce_op.__class__):
                return pl.coalesce(*args)
            if isinstance(op, ops.CaseWhenOp):
                expr = pl.when(args[0]).then(args[1])
                for pred, result in zip(args[2::2], args[3::2]):
                    return expr.when(pred).then(result)
                return expr
            raise NotImplementedError(f"Polars compiler hasn't implemented {op}")

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

        def compile_agg_op(self, op: agg_ops.WindowOp, inputs: Sequence[str] = []):
            if isinstance(op, agg_ops.ProductOp):
                # TODO: Need schema to cast back to original type if posisble (eg float back to int)
                return pl.col(*inputs).log().sum().exp()
            if isinstance(op, agg_ops.SumOp):
                return pl.sum(*inputs)
            if isinstance(op, agg_ops.MinOp):
                return pl.min(*inputs)
            if isinstance(op, agg_ops.MaxOp):
                return pl.max(*inputs)
            if isinstance(op, agg_ops.CountOp):
                return pl.count(*inputs)
            if isinstance(op, agg_ops.CorrOp):
                return pl.corr(*inputs)
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

    def compile(self, array_value: bigframes.core.ArrayValue) -> pl.LazyFrame:
        if not polars_installed:
            raise ValueError(
                "Polars is not installed, cannot compile to polars engine."
            )

        # TODO: Create standard way to configure BFET -> BFET rewrites
        # Polars has incomplete slice support in lazy mode
        node = nodes.bottom_up(array_value.node, bigframes.core.rewrite.rewrite_slice)
        return self.compile_node(node)

    @functools.singledispatchmethod
    def compile_node(self, node: nodes.BigFrameNode):
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
        return lazy_frame.select(cols_to_read.keys()).rename(cols_to_read)

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

        frame = frame.sort(
            [
                self.expr_compiler.compile_expression(by.scalar_expression)
                for by in node.by
            ],
            descending=[not by.direction.is_ascending for by in node.by],
            nulls_last=[by.na_last for by in node.by],
            maintain_order=True,
        )
        return frame

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
        new_cols = [
            self.expr_compiler.compile_expression(ex).alias(name.sql)
            for ex, name in node.assignments
        ]
        return self.compile_node(node.child).with_columns(new_cols)

    @compile_node.register
    def compile_offsets(self, node: nodes.PromoteOffsetsNode):
        return self.compile_node(node.child).with_columns(
            [pl.int_range(pl.len(), dtype=pl.Int64).alias(node.col_id.sql)]
        )

    @compile_node.register
    def compile_join(self, node: nodes.JoinNode):
        # Always totally order this, as adding offsets is relatively cheap for in-memory columnar data
        left = self.compile_node(node.left_child).with_columns(
            [
                pl.int_range(pl.len()).alias("_bf_join_l"),
            ]
        )
        right = self.compile_node(node.right_child).with_columns(
            [
                pl.int_range(pl.len()).alias("_bf_join_r"),
            ]
        )
        if node.type != "cross":
            left_on = [l_name.id.sql for l_name, _ in node.conditions]
            right_on = [r_name.id.sql for _, r_name in node.conditions]
            joined = left.join(
                right, how=node.type, left_on=left_on, right_on=right_on, coalesce=False
            )
        else:
            joined = left.join(right, how=node.type)
        return joined.sort(["_bf_join_l", "_bf_join_r"]).drop(
            ["_bf_join_l", "_bf_join_r"]
        )

    @compile_node.register
    def compile_concat(self, node: nodes.ConcatNode):
        return pl.concat(self.compile_node(child) for child in node.child_nodes)

    @compile_node.register
    def compile_agg(self, node: nodes.AggregateNode):
        df = self.compile_node(node.child)

        # Need to materialize columns to broadcast constants
        agg_inputs = [
            list(
                map(
                    lambda x: x.alias(guid.generate_guid()),
                    self.agg_compiler.get_args(agg),
                )
            )
            for agg, _ in node.aggregations
        ]

        df_agg_inputs = df.with_columns(itertools.chain(*agg_inputs))

        agg_exprs = [
            self.agg_compiler.compile_agg_op(
                agg.op, list(map(lambda x: x.meta.output_name(), inputs))
            ).alias(id.sql)
            for (agg, id), inputs in zip(node.aggregations, agg_inputs)
        ]

        if len(node.by_column_ids) > 0:
            group_exprs = [pl.col(ref.id.sql) for ref in node.by_column_ids]
            grouped_df = df_agg_inputs.group_by(group_exprs)
            return grouped_df.agg(agg_exprs).sort(group_exprs)
        else:
            return df_agg_inputs.select(agg_exprs)

    @compile_node.register
    def compile_explode(self, node: nodes.ExplodeNode):
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
        agg_expr = self.agg_compiler.compile_agg_expr(node.expression).alias(
            node.output_name.sql
        )
        # Three window types: completely unbound, grouped and row bounded

        window = node.window_spec

        if window.min_periods > 0:
            raise NotImplementedError("min_period not yet supported for polars engine")

        if window.bounds is None:
            # polars will automatically broadcast the aggregate to the matching input rows
            if len(window.grouping_keys) == 0:  # unbound window
                pass
            else:  # partition-only window
                agg_expr = agg_expr.over(
                    partition_by=[ref.id.sql for ref in window.grouping_keys]
                )
            return df.with_columns([agg_expr])

        else:  # row-bounded window
            assert isinstance(window.bounds, window_spec.RowsWindowBounds)
            # Polars API semi-bounded, and any grouped rolling window challenging
            # https://github.com/pola-rs/polars/issues/4799
            # https://github.com/pola-rs/polars/issues/8976
            index_col_name = "_bf_pl_engine_offsets"
            indexed_df = df.with_row_index(index_col_name)
            if len(window.grouping_keys) == 0:  # rolling-only window
                # https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.rolling.html
                offset_n = window.bounds.start
                period_n = _get_period(window.bounds) or df.collect().height
                results = indexed_df.rolling(
                    index_column=index_col_name,
                    period=f"{period_n}i",
                    offset=f"{offset_n}i" if offset_n else None,
                ).agg(agg_expr)
            else:  # groupby-rolling window
                raise NotImplementedError(
                    "Groupby rolling windows not yet implemented in polars engine"
                )
            # polars is columnar, so this is efficient
            # TODO: why can't just add columns?
            return pl.concat([df, results], how="horizontal")


def _get_period(bounds: window_spec.RowsWindowBounds) -> Optional[int]:
    """Returns None if the boundary is infinite."""
    if bounds.start is None or bounds.end is None:
        return None

    # collecting height is a massive kludge
    return bounds.end - bounds.start + 1
