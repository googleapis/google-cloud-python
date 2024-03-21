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
from typing import Mapping, Optional, Sequence, Tuple

import bigframes.core.expression as scalar_exprs
import bigframes.core.join_def as join_defs
import bigframes.core.nodes as nodes
import bigframes.core.ordering as order
import bigframes.operations as ops

Selection = Tuple[Tuple[scalar_exprs.Expression, str], ...]


@dataclasses.dataclass(frozen=True)
class SquashedSelect:
    """Squash together as many nodes as possible, separating out the projection, filter and reordering expressions."""

    root: nodes.BigFrameNode
    columns: Tuple[Tuple[scalar_exprs.Expression, str], ...]
    predicate: Optional[scalar_exprs.Expression]
    ordering: Tuple[order.OrderingExpression, ...]

    @classmethod
    def from_node(cls, node: nodes.BigFrameNode) -> SquashedSelect:
        if isinstance(node, nodes.ProjectionNode):
            return cls.from_node(node.child).project(node.assignments)
        elif isinstance(node, nodes.FilterNode):
            return cls.from_node(node.child).filter(node.predicate)
        elif isinstance(node, nodes.ReversedNode):
            return cls.from_node(node.child).reverse()
        elif isinstance(node, nodes.OrderByNode):
            return cls.from_node(node.child).order_with(node.by)
        else:
            selection = tuple(
                (scalar_exprs.UnboundVariableExpression(id), id)
                for id in get_node_column_ids(node)
            )
            return cls(node, selection, None, ())

    @property
    def column_lookup(self) -> Mapping[str, scalar_exprs.Expression]:
        return {col_id: expr for expr, col_id in self.columns}

    def project(
        self, projection: Tuple[Tuple[scalar_exprs.Expression, str], ...]
    ) -> SquashedSelect:
        new_columns = tuple(
            (expr.bind_all_variables(self.column_lookup), id) for expr, id in projection
        )
        return SquashedSelect(self.root, new_columns, self.predicate, self.ordering)

    def filter(self, predicate: scalar_exprs.Expression) -> SquashedSelect:
        if self.predicate is None:
            new_predicate = predicate.bind_all_variables(self.column_lookup)
        else:
            new_predicate = ops.and_op.as_expr(
                self.predicate, predicate.bind_all_variables(self.column_lookup)
            )
        return SquashedSelect(self.root, self.columns, new_predicate, self.ordering)

    def reverse(self) -> SquashedSelect:
        new_ordering = tuple(expr.with_reverse() for expr in self.ordering)
        return SquashedSelect(self.root, self.columns, self.predicate, new_ordering)

    def order_with(self, by: Tuple[order.OrderingExpression, ...]):
        adjusted_orderings = [
            order_part.bind_variables(self.column_lookup) for order_part in by
        ]
        new_ordering = (*adjusted_orderings, *self.ordering)
        return SquashedSelect(self.root, self.columns, self.predicate, new_ordering)

    def maybe_join(
        self, right: SquashedSelect, join_def: join_defs.JoinDefinition
    ) -> Optional[SquashedSelect]:
        if join_def.type == "cross":
            # Cannot convert cross join to projection
            return None

        r_exprs_by_id = {id: expr for expr, id in right.columns}
        l_exprs_by_id = {id: expr for expr, id in self.columns}
        l_join_exprs = [l_exprs_by_id[cond.left_id] for cond in join_def.conditions]
        r_join_exprs = [r_exprs_by_id[cond.right_id] for cond in join_def.conditions]

        if (self.root != right.root) or any(
            l_expr != r_expr for l_expr, r_expr in zip(l_join_exprs, r_join_exprs)
        ):
            return None

        join_type = join_def.type

        # Mask columns and remap names to expected schema
        lselection = self.columns
        rselection = right.columns
        if join_type == "inner":
            new_predicate = and_predicates(self.predicate, right.predicate)
        elif join_type == "outer":
            new_predicate = or_predicates(self.predicate, right.predicate)
        elif join_type == "left":
            new_predicate = self.predicate
        elif join_type == "right":
            new_predicate = right.predicate

        l_relative, r_relative = relative_predicates(self.predicate, right.predicate)
        lmask = l_relative if join_type in {"right", "outer"} else None
        rmask = r_relative if join_type in {"left", "outer"} else None
        if lmask is not None:
            lselection = tuple((apply_mask(expr, lmask), id) for expr, id in lselection)
        if rmask is not None:
            rselection = tuple((apply_mask(expr, rmask), id) for expr, id in rselection)
        new_columns = remap_names(join_def, lselection, rselection)

        # Reconstruct ordering
        if join_type == "right":
            new_ordering = right.ordering
        elif join_type == "outer":
            if lmask is not None:
                prefix = order.OrderingExpression(lmask, order.OrderingDirection.DESC)
                left_ordering = tuple(
                    order.OrderingExpression(
                        apply_mask(ref.scalar_expression, lmask),
                        ref.direction,
                        ref.na_last,
                    )
                    for ref in self.ordering
                )
                right_ordering = (
                    tuple(
                        order.OrderingExpression(
                            apply_mask(ref.scalar_expression, rmask),
                            ref.direction,
                            ref.na_last,
                        )
                        for ref in right.ordering
                    )
                    if rmask
                    else right.ordering
                )
                new_ordering = (prefix, *left_ordering, *right_ordering)
            else:
                new_ordering = self.ordering
        elif join_type in {"inner", "left"}:
            new_ordering = self.ordering
        else:
            raise ValueError(f"Unexpected join type {join_type}")
        return SquashedSelect(self.root, new_columns, new_predicate, new_ordering)

    def expand(self) -> nodes.BigFrameNode:
        # Safest to apply predicates first, as it may filter out inputs that cannot be handled by other expressions
        root = self.root
        if self.predicate:
            root = nodes.FilterNode(child=root, predicate=self.predicate)
        if self.ordering:
            root = nodes.OrderByNode(child=root, by=self.ordering)
        return nodes.ProjectionNode(child=root, assignments=self.columns)


def maybe_rewrite_join(join_node: nodes.JoinNode) -> nodes.BigFrameNode:
    left_side = SquashedSelect.from_node(join_node.left_child)
    right_side = SquashedSelect.from_node(join_node.right_child)
    joined = left_side.maybe_join(right_side, join_node.join)
    if joined is not None:
        return joined.expand()
    else:
        return join_node


def remap_names(
    join: join_defs.JoinDefinition, lselection: Selection, rselection: Selection
) -> Selection:
    new_selection: Selection = tuple()
    l_exprs_by_id = {id: expr for expr, id in lselection}
    r_exprs_by_id = {id: expr for expr, id in rselection}
    for mapping in join.mappings:
        if mapping.source_table == join_defs.JoinSide.LEFT:
            expr = l_exprs_by_id[mapping.source_id]
        else:  # Right
            expr = r_exprs_by_id[mapping.source_id]
        id = mapping.destination_id
        new_selection = (*new_selection, (expr, id))
    return new_selection


def and_predicates(
    expr1: Optional[scalar_exprs.Expression], expr2: Optional[scalar_exprs.Expression]
) -> Optional[scalar_exprs.Expression]:
    if expr1 is None:
        return expr2
    if expr2 is None:
        return expr1
    left_predicates = decompose_conjunction(expr1)
    right_predicates = decompose_conjunction(expr2)
    # remove common predicates
    all_predicates = itertools.chain(
        left_predicates, [p for p in right_predicates if p not in left_predicates]
    )
    return merge_predicates(list(all_predicates))


def or_predicates(
    expr1: Optional[scalar_exprs.Expression], expr2: Optional[scalar_exprs.Expression]
) -> Optional[scalar_exprs.Expression]:
    if (expr1 is None) or (expr2 is None):
        return None
    # TODO(tbergeron): Factor out common predicates
    return ops.or_op.as_expr(expr1, expr2)


def relative_predicates(
    expr1: Optional[scalar_exprs.Expression], expr2: Optional[scalar_exprs.Expression]
) -> Tuple[Optional[scalar_exprs.Expression], Optional[scalar_exprs.Expression]]:
    left_predicates = decompose_conjunction(expr1) if expr1 else ()
    right_predicates = decompose_conjunction(expr2) if expr2 else ()
    left_relative = tuple(
        pred for pred in left_predicates if pred not in right_predicates
    )
    right_relative = tuple(
        pred for pred in right_predicates if pred not in left_predicates
    )
    return merge_predicates(left_relative), merge_predicates(right_relative)


def apply_mask(
    expr: scalar_exprs.Expression, mask: scalar_exprs.Expression
) -> scalar_exprs.Expression:
    return ops.where_op.as_expr(expr, mask, scalar_exprs.const(None))


def merge_predicates(
    predicates: Sequence[scalar_exprs.Expression],
) -> Optional[scalar_exprs.Expression]:
    if len(predicates) == 0:
        return None

    return functools.reduce(ops.and_op.as_expr, predicates)


def decompose_conjunction(
    expr: scalar_exprs.Expression,
) -> Tuple[scalar_exprs.Expression, ...]:
    if isinstance(expr, scalar_exprs.OpExpression) and isinstance(
        expr.op, type(ops.and_op)
    ):
        return tuple(
            itertools.chain.from_iterable(decompose_conjunction(i) for i in expr.inputs)
        )
    else:
        return (expr,)


def get_node_column_ids(node: nodes.BigFrameNode) -> Tuple[str, ...]:
    # TODO: Convert to use node.schema once that has been merged
    # Note: this actually compiles the node to get the schema
    import bigframes.core

    return tuple(bigframes.core.ArrayValue(node).column_ids)
