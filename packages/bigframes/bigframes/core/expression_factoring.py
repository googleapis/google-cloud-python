import collections
import dataclasses
import functools
import itertools
from typing import Generic, Hashable, Iterable, Optional, Sequence, Tuple, TypeVar

from bigframes.core import agg_expressions, expression, identifiers, nodes

_MAX_INLINE_COMPLEXITY = 10


@dataclasses.dataclass(frozen=True, eq=False)
class NamedExpression:
    expr: expression.Expression
    name: identifiers.ColumnId


@dataclasses.dataclass(frozen=True, eq=False)
class FactoredExpression:
    root_expr: expression.Expression
    sub_exprs: Tuple[NamedExpression, ...]


def fragmentize_expression(root: NamedExpression) -> Sequence[NamedExpression]:
    """
    The goal of this functions is to factor out an expression into multiple sub-expressions.
    """

    factored_expr = root.expr.reduce_up(gather_fragments)
    root_expr = NamedExpression(factored_expr.root_expr, root.name)
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
            named_exprs.append(NamedExpression(child_result.root_expr, id))
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
    exprs: Sequence[NamedExpression],
    target_ids: Sequence[identifiers.ColumnId],
) -> nodes.BigFrameNode:
    curr_root = root
    by_id = {expr.name: expr for expr in exprs}
    # id -> id
    graph = DiGraph(
        (expr.name, child_id)
        for expr in exprs
        for child_id in expr.expr.column_references
        if child_id in by_id.keys()
    )
    # TODO: Also prevent inlining expensive or non-deterministic
    # We avoid inlining multi-parent ids, as they would be inlined multiple places, potentially increasing work and/or compiled text size
    multi_parent_ids = set(id for id in graph.nodes if len(graph.parents(id)) > 2)
    scalar_ids = set(expr.name for expr in exprs if expr.expr.is_scalar_expr)

    def graph_extract_scalar_exprs() -> Sequence[NamedExpression]:
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
                    id: by_id[id].expr.bind_refs(results, allow_partial_bindings=True)
                }
                results.update(new_exprs)
        # TODO: We can prune expressions that won't be reused here,
        return tuple(NamedExpression(expr, id) for id, expr in results.items())

    def graph_extract_window_expr() -> Optional[
        Tuple[identifiers.ColumnId, agg_expressions.WindowExpression]
    ]:
        candidate = list(
            itertools.islice((id for id in graph.sinks if id not in scalar_ids), 1)
        )
        if not candidate:
            return None
        else:
            id = next(iter(candidate))
            graph.remove_node(id)
            result_expr = by_id[id].expr
            assert isinstance(result_expr, agg_expressions.WindowExpression)
            return (id, result_expr)

    while not graph.empty:
        pre_size = len(graph.nodes)
        scalar_exprs = graph_extract_scalar_exprs()
        if scalar_exprs:
            curr_root = nodes.ProjectionNode(
                curr_root, tuple((x.expr, x.name) for x in scalar_exprs)
            )
        while result := graph_extract_window_expr():
            id, window_expr = result
            curr_root = nodes.WindowOpNode(
                curr_root, window_expr.analytic_expr, window_expr.window, output_name=id
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
