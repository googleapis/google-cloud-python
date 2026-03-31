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

import dataclasses
import functools
from typing import Callable, Mapping, Optional, Sequence, Tuple

from bigframes.core import bq_data, identifiers, nodes
import bigframes.core.expression as ex
from bigframes.core.ordering import OrderingExpression
import bigframes.dtypes

# SQL Nodes are generally terminal, so don't support rich transformation methods
# like remap_vars, remap_refs, etc.
# Still, fields should be defined on them, as typing info is still used for
# dispatching some operators in the emitter, and for validation.


# TODO: Join node, union node
@dataclasses.dataclass(frozen=True)
class SqlDataSource(nodes.LeafNode):
    source: bq_data.BigqueryDataSource

    @functools.cached_property
    def fields(self) -> Sequence[nodes.Field]:
        return tuple(
            nodes.Field(
                identifiers.ColumnId(source_id),
                self.source.schema.get_type(source_id),
                self.source.table.schema_by_id[source_id].is_nullable,
            )
            for source_id in self.source.schema.names
        )

    @property
    def variables_introduced(self) -> int:
        # This operation only renames variables, doesn't actually create new ones
        return 0

    @property
    def defines_namespace(self) -> bool:
        return True

    @property
    def explicitly_ordered(self) -> bool:
        return False

    @property
    def order_ambiguous(self) -> bool:
        return True

    @property
    def row_count(self) -> Optional[int]:
        return self.source.n_rows

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return tuple(self.ids)

    @property
    def consumed_ids(self):
        return ()

    @property
    def _node_expressions(self):
        return ()

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> SqlSelectNode:
        raise NotImplementedError()

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> SqlSelectNode:
        raise NotImplementedError()  # type: ignore


@dataclasses.dataclass(frozen=True)
class SqlWithCtesNode(nodes.BigFrameNode):
    # def, name pairs
    child: nodes.BigFrameNode
    cte_names: tuple[str, ...]
    cte_defs: tuple[nodes.BigFrameNode, ...]

    @property
    def child_nodes(self) -> Sequence[nodes.BigFrameNode]:
        return (self.child, *self.cte_defs)

    @property
    def fields(self) -> Sequence[nodes.Field]:
        return self.child.fields

    @property
    def variables_introduced(self) -> int:
        # This operation only renames variables, doesn't actually create new ones
        return 0

    @property
    def defines_namespace(self) -> bool:
        return True

    @property
    def explicitly_ordered(self) -> bool:
        return False

    @property
    def order_ambiguous(self) -> bool:
        return True

    @property
    def row_count(self) -> Optional[int]:
        return self.child.row_count

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return tuple(self.ids)

    @property
    def consumed_ids(self):
        return ()

    @property
    def _node_expressions(self):
        return ()

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> SqlWithCtesNode:
        raise NotImplementedError()

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> SqlWithCtesNode:
        raise NotImplementedError()  # type: ignore

    def transform_children(
        self, transform: Callable[[nodes.BigFrameNode], nodes.BigFrameNode]
    ) -> SqlWithCtesNode:
        return SqlWithCtesNode(
            transform(self.child),
            self.cte_names,
            tuple(transform(cte) for cte in self.cte_defs),
        )


@dataclasses.dataclass(frozen=True)
class SqlCteRefNode(nodes.LeafNode):
    cte_name: str
    cte_schema: tuple[nodes.Field, ...]

    @property
    def fields(self) -> Sequence[nodes.Field]:
        return self.cte_schema

    @property
    def variables_introduced(self) -> int:
        # This operation only renames variables, doesn't actually create new ones
        return 0

    @property
    def defines_namespace(self) -> bool:
        return True

    @property
    def explicitly_ordered(self) -> bool:
        return False

    @property
    def order_ambiguous(self) -> bool:
        return True

    @property
    def row_count(self) -> Optional[int]:
        raise NotImplementedError()

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return tuple(self.ids)

    @property
    def consumed_ids(self):
        return ()

    @property
    def _node_expressions(self):
        return ()

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> SqlCteRefNode:
        raise NotImplementedError()

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> SqlCteRefNode:
        raise NotImplementedError()  # type: ignore


@dataclasses.dataclass(frozen=True)
class SqlSelectNode(nodes.UnaryNode):
    selections: tuple[nodes.ColumnDef, ...] = ()
    predicates: tuple[ex.Expression, ...] = ()
    sorting: tuple[OrderingExpression, ...] = ()
    limit: Optional[int] = None

    @functools.cached_property
    def fields(self) -> Sequence[nodes.Field]:
        fields = []
        for cdef in self.selections:
            bound_expr = ex.bind_schema_fields(cdef.expression, self.child.field_by_id)
            field = nodes.Field(
                cdef.id,
                bigframes.dtypes.dtype_for_etype(bound_expr.output_type),
                nullable=bound_expr.nullable,
            )

            # Special case until we get better nullability inference in expression objects themselves
            if bound_expr.is_identity and not any(
                self.child.field_by_id[id].nullable
                for id in cdef.expression.column_references
            ):
                field = field.with_nonnull()
            fields.append(field)

        return tuple(fields)

    @property
    def variables_introduced(self) -> int:
        # This operation only renames variables, doesn't actually create new ones
        return 0

    @property
    def defines_namespace(self) -> bool:
        return True

    @property
    def row_count(self) -> Optional[int]:
        if self.child.row_count is not None:
            if self.limit is not None:
                return min([self.limit, self.child.row_count])
            return self.child.row_count

        return None

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return tuple(cdef.id for cdef in self.selections)

    @property
    def consumed_ids(self):
        raise NotImplementedError()

    @property
    def _node_expressions(self):
        raise NotImplementedError()

    @property
    def is_star_selection(self) -> bool:
        return tuple(self.ids) == tuple(self.child.ids)

    @functools.cache
    def get_id_mapping(self) -> dict[identifiers.ColumnId, ex.Expression]:
        return {cdef.id: cdef.expression for cdef in self.selections}

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> SqlSelectNode:
        raise NotImplementedError()

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> SqlSelectNode:
        raise NotImplementedError()  # type: ignore
