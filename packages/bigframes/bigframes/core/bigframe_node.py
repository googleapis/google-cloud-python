# Copyright 2023 Google LLC
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

import abc
import collections
import dataclasses
import functools
import itertools
import typing
from typing import (
    Callable,
    Dict,
    Generator,
    Iterable,
    Mapping,
    Sequence,
    Set,
    Tuple,
    Union,
)

from bigframes.core import expression, field, identifiers
import bigframes.core.schema as schemata
import bigframes.dtypes

if typing.TYPE_CHECKING:
    import bigframes.session

COLUMN_SET = frozenset[identifiers.ColumnId]

T = typing.TypeVar("T")


@dataclasses.dataclass(eq=False, frozen=True)
class BigFrameNode:
    """
    Immutable node for representing 2D typed array as a tree of operators.

    All subclasses must be hashable so as to be usable as caching key.
    """

    @property
    def deterministic(self) -> bool:
        """Whether this node will evaluates deterministically."""
        return True

    @property
    def row_preserving(self) -> bool:
        """Whether this node preserves input rows."""
        return True

    @property
    def non_local(self) -> bool:
        """
        Whether this node combines information across multiple rows instead of processing rows independently.
        Used as an approximation for whether the expression may require shuffling to execute (and therefore be expensive).
        """
        return False

    @property
    def child_nodes(self) -> typing.Sequence[BigFrameNode]:
        """Direct children of this node"""
        return tuple([])

    @property
    @abc.abstractmethod
    def row_count(self) -> typing.Optional[int]:
        return None

    @abc.abstractmethod
    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> BigFrameNode:
        """Remap variable references"""
        ...

    @property
    @abc.abstractmethod
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        """The variables defined in this node (as opposed to by child nodes)."""
        ...

    @functools.cached_property
    def session(self):
        sessions = []
        for child in self.child_nodes:
            if child.session is not None:
                sessions.append(child.session)
        unique_sessions = len(set(sessions))
        if unique_sessions > 1:
            raise ValueError("Cannot use combine sources from multiple sessions.")
        elif unique_sessions == 1:
            return sessions[0]
        return None

    def _validate(self):
        """Validate the local data in the node."""
        return

    @functools.cache
    def validate_tree(self) -> bool:
        for child in self.child_nodes:
            child.validate_tree()
        self._validate()
        field_list = list(self.fields)
        if len(set(field_list)) != len(field_list):
            raise ValueError(f"Non unique field ids {list(self.fields)}")
        return True

    def _as_tuple(self) -> Tuple:
        """Get all fields as tuple."""
        return tuple(getattr(self, field.name) for field in dataclasses.fields(self))

    def __hash__(self) -> int:
        # Custom hash that uses cache to avoid costly recomputation
        return self._cached_hash

    def __eq__(self, other) -> bool:
        # Custom eq that tries to short-circuit full structural comparison
        if not isinstance(other, self.__class__):
            return False
        if self is other:
            return True
        if hash(self) != hash(other):
            return False
        return self._as_tuple() == other._as_tuple()

    # BigFrameNode trees can be very deep so its important avoid recalculating the hash from scratch
    # Each subclass of BigFrameNode should use this property to implement __hash__
    # The default dataclass-generated __hash__ method is not cached
    @functools.cached_property
    def _cached_hash(self):
        return hash(self._as_tuple())

    @property
    def roots(self) -> typing.Set[BigFrameNode]:
        roots = itertools.chain.from_iterable(
            map(lambda child: child.roots, self.child_nodes)
        )
        return set(roots)

    # TODO: Store some local data lazily for select, aggregate nodes.
    @property
    @abc.abstractmethod
    def fields(self) -> Sequence[field.Field]:
        ...

    @property
    def ids(self) -> Iterable[identifiers.ColumnId]:
        """All output ids from the node."""
        return (field.id for field in self.fields)

    @property
    @abc.abstractmethod
    def variables_introduced(self) -> int:
        """
        Defines number of values created by the current node. Helps represent the "width" of a query
        """
        ...

    @property
    def relation_ops_created(self) -> int:
        """
        Defines the number of relational ops generated by the current node. Used to estimate query planning complexity.
        """
        return 1

    @property
    def joins(self) -> bool:
        """
        Defines whether the node joins data.
        """
        return False

    @property
    @abc.abstractmethod
    def order_ambiguous(self) -> bool:
        """
        Whether row ordering is potentially ambiguous. For example, ReadTable (without a primary key) could be ordered in different ways.
        """
        ...

    @property
    @abc.abstractmethod
    def explicitly_ordered(self) -> bool:
        """
        Whether row ordering is potentially ambiguous. For example, ReadTable (without a primary key) could be ordered in different ways.
        """
        ...

    @functools.cached_property
    def height(self) -> int:
        if len(self.child_nodes) == 0:
            return 0
        return max(child.height for child in self.child_nodes) + 1

    @functools.cached_property
    def total_variables(self) -> int:
        return self.variables_introduced + sum(
            map(lambda x: x.total_variables, self.child_nodes)
        )

    @functools.cached_property
    def total_relational_ops(self) -> int:
        return self.relation_ops_created + sum(
            map(lambda x: x.total_relational_ops, self.child_nodes)
        )

    @functools.cached_property
    def total_joins(self) -> int:
        return int(self.joins) + sum(map(lambda x: x.total_joins, self.child_nodes))

    @functools.cached_property
    def schema(self) -> schemata.ArraySchema:
        # TODO: Make schema just a view on fields
        return schemata.ArraySchema(
            tuple(schemata.SchemaItem(i.id.name, i.dtype) for i in self.fields)
        )

    @property
    def planning_complexity(self) -> int:
        """
        Empirical heuristic measure of planning complexity.

        Used to determine when to decompose overly complex computations. May require tuning.
        """
        return self.total_variables * self.total_relational_ops * (1 + self.total_joins)

    @abc.abstractmethod
    def transform_children(
        self, t: Callable[[BigFrameNode], BigFrameNode]
    ) -> BigFrameNode:
        """Apply a function to each child node."""
        ...

    @abc.abstractmethod
    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> BigFrameNode:
        """Remap defined (in this node only) variables."""
        ...

    @property
    def defines_namespace(self) -> bool:
        """
        If true, this node establishes a new column id namespace.

        If false, this node consumes and produces ids in the namespace
        """
        return False

    @property
    def referenced_ids(self) -> COLUMN_SET:
        return frozenset()

    @functools.cached_property
    def defined_variables(self) -> set[str]:
        """Full set of variables defined in the namespace, even if not selected."""
        self_defined_variables = set(self.schema.names)
        if self.defines_namespace:
            return self_defined_variables
        return self_defined_variables.union(
            *(child.defined_variables for child in self.child_nodes)
        )

    def get_type(self, id: identifiers.ColumnId) -> bigframes.dtypes.Dtype:
        return self._dtype_lookup[id]

    # TODO: Deprecate in favor of field_by_id, and eventually, by rich references
    @functools.cached_property
    def _dtype_lookup(self) -> dict[identifiers.ColumnId, bigframes.dtypes.Dtype]:
        return {field.id: field.dtype for field in self.fields}

    @functools.cached_property
    def field_by_id(self) -> Mapping[identifiers.ColumnId, field.Field]:
        return {field.id: field for field in self.fields}

    @property
    def _node_expressions(
        self,
    ) -> Sequence[Union[expression.Expression, expression.Aggregation]]:
        """List of scalar expressions. Intended for checking engine compatibility with used ops."""
        return ()

    # Plan algorithms
    def unique_nodes(
        self: BigFrameNode,
    ) -> Generator[BigFrameNode, None, None]:
        """Walks the tree for unique nodes"""
        seen = set()
        stack: list[BigFrameNode] = [self]
        while stack:
            item = stack.pop()
            if item not in seen:
                yield item
                seen.add(item)
                stack.extend(item.child_nodes)

    def edges(
        self: BigFrameNode,
    ) -> Generator[Tuple[BigFrameNode, BigFrameNode], None, None]:
        for item in self.unique_nodes():
            for child in item.child_nodes:
                yield (item, child)

    def iter_nodes_topo(self: BigFrameNode) -> Generator[BigFrameNode, None, None]:
        """Returns nodes from bottom up."""
        queue = collections.deque(
            [node for node in self.unique_nodes() if not node.child_nodes]
        )

        child_to_parents: Dict[
            BigFrameNode, Set[BigFrameNode]
        ] = collections.defaultdict(set)
        for parent, child in self.edges():
            child_to_parents[child].add(parent)

        yielded = set()

        while queue:
            item = queue.popleft()
            yield item
            yielded.add(item)
            for parent in child_to_parents[item]:
                if set(parent.child_nodes).issubset(yielded):
                    queue.append(parent)

    def top_down(
        self: BigFrameNode,
        transform: Callable[[BigFrameNode], BigFrameNode],
    ) -> BigFrameNode:
        """
        Perform a top-down transformation of the BigFrameNode tree.
        """
        to_process = [self]
        results: Dict[BigFrameNode, BigFrameNode] = {}

        while to_process:
            item = to_process.pop()
            if item not in results.keys():
                item_result = transform(item)
                results[item] = item_result
                to_process.extend(item_result.child_nodes)

        to_process = [self]
        # for each processed item, replace its children
        for item in reversed(list(results.keys())):
            results[item] = results[item].transform_children(lambda x: results[x])

        return results[self]

    def bottom_up(
        self: BigFrameNode,
        transform: Callable[[BigFrameNode], BigFrameNode],
    ) -> BigFrameNode:
        """
        Perform a bottom-up transformation of the BigFrameNode tree.

        The `transform` function is applied to each node *after* its children
        have been transformed.  This allows for transformations that depend
        on the results of transforming subtrees.

        Returns the transformed root node.
        """
        results: dict[BigFrameNode, BigFrameNode] = {}
        for node in list(self.iter_nodes_topo()):
            # child nodes have already been transformed
            result = node.transform_children(lambda x: results[x])
            result = transform(result)
            results[node] = result

        return results[self]

    def reduce_up(self, reduction: Callable[[BigFrameNode, Tuple[T, ...]], T]) -> T:
        """Apply a bottom-up reduction to the tree."""
        results: dict[BigFrameNode, T] = {}
        for node in list(self.iter_nodes_topo()):
            # child nodes have already been transformed
            child_results = tuple(results[child] for child in node.child_nodes)
            result = reduction(node, child_results)
            results[node] = result

        return results[self]
