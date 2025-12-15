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


import collections
import dataclasses
import functools
import itertools
from typing import (
    cast,
    Hashable,
    Iterable,
    Iterator,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
)

from bigframes.core import (
    agg_expressions,
    expression,
    graphs,
    identifiers,
    nodes,
    window_spec,
)

_MAX_INLINE_COMPLEXITY = 10


def apply_col_exprs_to_plan(
    plan: nodes.BigFrameNode, col_exprs: Sequence[nodes.ColumnDef]
) -> nodes.BigFrameNode:
    # TODO: Jointly fragmentize expressions to more efficiently reuse common sub-expressions
    target_ids = tuple(named_expr.id for named_expr in col_exprs)

    fragments = tuple(
        itertools.chain.from_iterable(
            fragmentize_expression(expr) for expr in col_exprs
        )
    )
    return push_into_tree(plan, fragments, target_ids)


def apply_agg_exprs_to_plan(
    plan: nodes.BigFrameNode,
    agg_defs: Sequence[nodes.ColumnDef],
    grouping_keys: Sequence[expression.DerefOp],
) -> nodes.BigFrameNode:
    factored_aggs = [factor_aggregation(agg_def) for agg_def in agg_defs]
    all_inputs = list(
        itertools.chain(*(factored_agg.agg_inputs for factored_agg in factored_aggs))
    )
    window_def = window_spec.WindowSpec(grouping_keys=tuple(grouping_keys))
    windowized_inputs = [
        nodes.ColumnDef(windowize(cdef.expression, window_def), cdef.id)
        for cdef in all_inputs
    ]
    plan = apply_col_exprs_to_plan(plan, windowized_inputs)
    all_aggs = list(
        itertools.chain(*(factored_agg.agg_exprs for factored_agg in factored_aggs))
    )
    plan = nodes.AggregateNode(
        plan,
        tuple((cdef.expression, cdef.id) for cdef in all_aggs),  # type: ignore
        by_column_ids=tuple(grouping_keys),
    )

    post_scalar_exprs = tuple(
        (factored_agg.root_scalar_expr for factored_agg in factored_aggs)
    )
    plan = nodes.ProjectionNode(
        plan, tuple((cdef.expression, cdef.id) for cdef in post_scalar_exprs)
    )
    final_ids = itertools.chain(
        (ref.id for ref in grouping_keys), (cdef.id for cdef in post_scalar_exprs)
    )
    plan = nodes.SelectionNode(
        plan, tuple(nodes.AliasedRef.identity(ident) for ident in final_ids)
    )

    return plan


@dataclasses.dataclass(frozen=True, eq=False)
class FactoredExpression:
    root_expr: expression.Expression
    sub_exprs: Tuple[nodes.ColumnDef, ...]


def fragmentize_expression(root: nodes.ColumnDef) -> Sequence[nodes.ColumnDef]:
    """
    The goal of this functions is to factor out an expression into multiple sub-expressions.
    """

    factored_expr = root.expression.reduce_up(gather_fragments)
    root_expr = nodes.ColumnDef(factored_expr.root_expr, root.id)
    return (root_expr, *factored_expr.sub_exprs)


@dataclasses.dataclass(frozen=True, eq=False)
class FactoredAggregation:
    """
    A three part recomposition of a general aggregating expression.

    1. agg_inputs: This is a set of (*col) -> col transformation that preprocess inputs for the aggregations ops
    2. agg_exprs: This is a set of pure aggregations (eg sum, mean, min, max) ops referencing the outputs of (1)
    3. root_scalar_expr: This is the final set, takes outputs of (2), applies scalar expression to produce final result.
    """

    # pure scalar expression
    root_scalar_expr: nodes.ColumnDef
    # pure agg expression, only refs cols and consts
    agg_exprs: Tuple[nodes.ColumnDef, ...]
    # can be analytic, scalar op, const, col refs
    agg_inputs: Tuple[nodes.ColumnDef, ...]


def windowize(
    root: expression.Expression, window: window_spec.WindowSpec
) -> expression.Expression:
    def windowize_local(expr: expression.Expression):
        if isinstance(expr, agg_expressions.Aggregation):
            if not expr.op.can_be_windowized:
                raise ValueError(f"Op: {expr.op} cannot be windowized.")
            return agg_expressions.WindowExpression(expr, window)
        if isinstance(expr, agg_expressions.WindowExpression):
            raise ValueError(f"Expression {expr} already windowed!")
        return expr

    return root.bottom_up(windowize_local)


def factor_aggregation(root: nodes.ColumnDef) -> FactoredAggregation:
    """
    Factor an aggregation def into three components.
    1. Input column expressions (includes analytic expressions)
    2. The set of underlying primitive aggregations
    3. A final post-aggregate scalar expression
    """
    final_aggs = list(dedupe(find_final_aggregations(root.expression)))
    agg_inputs = list(
        dedupe(itertools.chain.from_iterable(map(find_agg_inputs, final_aggs)))
    )

    agg_input_defs = tuple(
        nodes.ColumnDef(expr, identifiers.ColumnId.unique()) for expr in agg_inputs
    )
    agg_inputs_dict = {
        cdef.expression: expression.DerefOp(cdef.id) for cdef in agg_input_defs
    }

    agg_expr_to_ids = {expr: identifiers.ColumnId.unique() for expr in final_aggs}

    isolated_aggs = tuple(
        nodes.ColumnDef(sub_expressions(expr, agg_inputs_dict), agg_expr_to_ids[expr])
        for expr in final_aggs
    )
    agg_outputs_dict = {
        expr: expression.DerefOp(id) for expr, id in agg_expr_to_ids.items()
    }

    root_scalar_expr = nodes.ColumnDef(
        sub_expressions(root.expression, agg_outputs_dict), root.id  # type: ignore
    )

    return FactoredAggregation(
        root_scalar_expr=root_scalar_expr,
        agg_exprs=isolated_aggs,
        agg_inputs=agg_input_defs,
    )


def sub_expressions(
    root: expression.Expression,
    replacements: Mapping[expression.Expression, expression.Expression],
) -> expression.Expression:
    return root.top_down(lambda x: replacements.get(x, x))


def find_final_aggregations(
    root: expression.Expression,
) -> Iterator[agg_expressions.Aggregation]:
    if isinstance(root, agg_expressions.Aggregation):
        yield root
    elif isinstance(root, expression.OpExpression):
        for child in root.children:
            yield from find_final_aggregations(child)
    elif isinstance(root, expression.ScalarConstantExpression):
        return
    else:
        # eg, window expression, column references not allowed
        raise ValueError(f"Unexpected node: {root}")


def find_agg_inputs(
    root: agg_expressions.Aggregation,
) -> Iterator[expression.Expression]:
    for child in root.children:
        if not isinstance(
            child, (expression.DerefOp, expression.ScalarConstantExpression)
        ):
            yield child


def gather_fragments(
    root: expression.Expression, fragmentized_children: Sequence[FactoredExpression]
) -> FactoredExpression:
    replacements: list[expression.Expression] = []
    named_exprs = []  # root -> leaf dependency order
    for child_result in fragmentized_children:
        child_expr = child_result.root_expr
        is_leaf = isinstance(
            child_expr, (expression.DerefOp, expression.ScalarConstantExpression)
        )
        is_window_agg = isinstance(
            root, agg_expressions.WindowExpression
        ) and isinstance(child_expr, agg_expressions.Aggregation)
        do_inline = is_leaf | is_window_agg
        if not do_inline:
            id = identifiers.ColumnId.unique()
            replacements.append(expression.DerefOp(id))
            named_exprs.append(nodes.ColumnDef(child_result.root_expr, id))
            named_exprs.extend(child_result.sub_exprs)
        else:
            replacements.append(child_result.root_expr)
            named_exprs.extend(child_result.sub_exprs)
    new_root = replace_children(root, replacements)
    return FactoredExpression(new_root, tuple(named_exprs))


def replace_children(
    root: expression.Expression, new_children: Sequence[expression.Expression]
):
    mapping = {root.children[i]: new_children[i] for i in range(len(root.children))}
    return root.transform_children(lambda x: mapping.get(x, x))


def push_into_tree(
    root: nodes.BigFrameNode,
    exprs: Sequence[nodes.ColumnDef],
    target_ids: Sequence[identifiers.ColumnId],
) -> nodes.BigFrameNode:
    curr_root = root
    by_id = {expr.id: expr for expr in exprs}
    # id -> id
    graph = graphs.DiGraph(
        (expr.id for expr in exprs),
        (
            (expr.id, child_id)
            for expr in exprs
            for child_id in expr.expression.column_references
            if child_id in by_id.keys()
        ),
    )
    # TODO: Also prevent inlining expensive or non-deterministic
    # We avoid inlining multi-parent ids, as they would be inlined multiple places, potentially increasing work and/or compiled text size
    multi_parent_ids = set(id for id in graph.nodes if len(list(graph.parents(id))) > 2)
    scalar_ids = set(expr.id for expr in exprs if expr.expression.is_scalar_expr)

    analytic_defs = filter(
        lambda x: isinstance(x.expression, agg_expressions.WindowExpression), exprs
    )
    analytic_by_window = grouped(
        map(
            lambda x: (cast(agg_expressions.WindowExpression, x.expression).window, x),
            analytic_defs,
        )
    )

    def graph_extract_scalar_exprs() -> Sequence[nodes.ColumnDef]:
        results: dict[identifiers.ColumnId, expression.Expression] = dict()
        while (
            True
        ):  # Will converge as each loop either reduces graph size, or fails to find any candidate and breaks
            candidate_ids = list(
                id
                for id in graph.sinks
                if (id in scalar_ids)
                and not any(
                    (
                        child in multi_parent_ids
                        and id in results.keys()
                        and not is_simple(results[id])
                    )
                    for child in graph.children(id)
                )
            )
            if len(candidate_ids) == 0:
                break
            for id in candidate_ids:
                graph.remove_node(id)
                new_exprs = {
                    id: by_id[id].expression.bind_refs(
                        results, allow_partial_bindings=True
                    )
                }
                results.update(new_exprs)
        # TODO: We can prune expressions that won't be reused here,
        return tuple(nodes.ColumnDef(expr, id) for id, expr in results.items())

    def graph_extract_window_expr() -> Optional[
        Tuple[Sequence[nodes.ColumnDef], window_spec.WindowSpec]
    ]:
        for id in graph.sinks:
            next_def = by_id[id]
            if isinstance(next_def.expression, agg_expressions.WindowExpression):
                window = next_def.expression.window
                window_exprs = [
                    cdef
                    for cdef in analytic_by_window[window]
                    if cdef.id in graph.sinks
                ]
                agg_exprs = tuple(
                    nodes.ColumnDef(
                        cast(
                            agg_expressions.WindowExpression, cdef.expression
                        ).analytic_expr,
                        cdef.id,
                    )
                    for cdef in window_exprs
                )
                for cdef in window_exprs:
                    graph.remove_node(cdef.id)
                return (agg_exprs, window)

        return None

    while not graph.empty:
        pre_size = len(graph.nodes)
        scalar_exprs = graph_extract_scalar_exprs()
        if scalar_exprs:
            curr_root = nodes.ProjectionNode(
                curr_root, tuple((x.expression, x.id) for x in scalar_exprs)
            )
        while result := graph_extract_window_expr():
            defs, window = result
            assert len(defs) > 0
            curr_root = nodes.WindowOpNode(
                curr_root,
                tuple(defs),
                window,
            )
        if len(graph.nodes) >= pre_size:
            raise ValueError("graph didn't shrink")
    # TODO: Try to get the ordering right earlier, so can avoid this extra node.
    post_ids = (*root.ids, *target_ids)
    if tuple(curr_root.ids) != post_ids:
        curr_root = nodes.SelectionNode(
            curr_root, tuple(nodes.AliasedRef.identity(id) for id in post_ids)
        )
    return curr_root


@functools.cache
def is_simple(expr: expression.Expression) -> bool:
    count = 0
    for part in expr.walk():
        count += 1
        if count > _MAX_INLINE_COMPLEXITY:
            return False
    return True


K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


def grouped(values: Iterable[tuple[K, V]]) -> dict[K, list[V]]:
    result = collections.defaultdict(list)
    for k, v in values:
        result[k].append(v)
    return result


def dedupe(values: Iterable[K]) -> Iterator[K]:
    seen = set()
    for k in values:
        if k not in seen:
            seen.add(k)
            yield k
