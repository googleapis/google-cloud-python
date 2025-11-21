import collections
import dataclasses
import functools
from typing import cast, Generic, Hashable, Iterable, Optional, Sequence, Tuple, TypeVar

from bigframes.core import agg_expressions, expression, identifiers, nodes, window_spec

_MAX_INLINE_COMPLEXITY = 10


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


T = TypeVar("T", bound=Hashable)


class DiGraph(Generic[T]):
    def __init__(self, edges: Iterable[Tuple[T, T]]):
        self._parents = collections.defaultdict(set)
        self._children = collections.defaultdict(set)  # specifically, unpushed ones
        # use dict for stable ordering, which grants determinism
        self._sinks: dict[T, None] = dict()
        for src, dst in edges:
            self._children[src].add(dst)
            self._parents[dst].add(src)
            # sinks have no children
            if not self._children[dst]:
                self._sinks[dst] = None
            if src in self._sinks:
                del self._sinks[src]

    @property
    def nodes(self):
        # should be the same set of ids as self._parents
        return self._children.keys()

    @property
    def sinks(self) -> Iterable[T]:
        return self._sinks.keys()

    @property
    def empty(self):
        return len(self.nodes) == 0

    def parents(self, node: T) -> set[T]:
        return self._parents[node]

    def children(self, node: T) -> set[T]:
        return self._children[node]

    def remove_node(self, node: T) -> None:
        for child in self._children[node]:
            self._parents[child].remove(node)
        for parent in self._parents[node]:
            self._children[parent].remove(node)
            if len(self._children[parent]) == 0:
                self._sinks[parent] = None
        del self._children[node]
        del self._parents[node]
        if node in self._sinks:
            del self._sinks[node]


def push_into_tree(
    root: nodes.BigFrameNode,
    exprs: Sequence[nodes.ColumnDef],
    target_ids: Sequence[identifiers.ColumnId],
) -> nodes.BigFrameNode:
    curr_root = root
    by_id = {expr.id: expr for expr in exprs}
    # id -> id
    graph = DiGraph(
        (expr.id, child_id)
        for expr in exprs
        for child_id in expr.expression.column_references
        if child_id in by_id.keys()
    )
    # TODO: Also prevent inlining expensive or non-deterministic
    # We avoid inlining multi-parent ids, as they would be inlined multiple places, potentially increasing work and/or compiled text size
    multi_parent_ids = set(id for id in graph.nodes if len(graph.parents(id)) > 2)
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
