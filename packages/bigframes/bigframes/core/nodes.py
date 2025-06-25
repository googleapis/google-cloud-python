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
import dataclasses
import datetime
import functools
import itertools
import typing
from typing import (
    AbstractSet,
    Callable,
    cast,
    Iterable,
    Mapping,
    Optional,
    Sequence,
    Tuple,
)

import google.cloud.bigquery as bq

from bigframes.core import identifiers, local_data, sequences
from bigframes.core.bigframe_node import BigFrameNode, COLUMN_SET
import bigframes.core.expression as ex
from bigframes.core.field import Field
from bigframes.core.ordering import OrderingExpression, RowOrdering
import bigframes.core.slices as slices
import bigframes.core.window_spec as window
import bigframes.dtypes

if typing.TYPE_CHECKING:
    import bigframes.core.ordering as orderings
    import bigframes.session


# A fixed number of variable to assume for overhead on some operations
OVERHEAD_VARIABLES = 5


class AdditiveNode:
    """Definition of additive - if you drop added_fields, you end up with the descendent.

    .. code-block:: text

        AdditiveNode (fields: a, b, c; added_fields: c)
            |
            |  additive_base
            V
        BigFrameNode (fields: a, b)

    """

    @property
    @abc.abstractmethod
    def added_fields(self) -> Tuple[Field, ...]:
        ...

    @property
    @abc.abstractmethod
    def additive_base(self) -> BigFrameNode:
        ...

    @abc.abstractmethod
    def replace_additive_base(self, BigFrameNode) -> BigFrameNode:
        ...


@dataclasses.dataclass(frozen=True, eq=False)
class UnaryNode(BigFrameNode):
    child: BigFrameNode

    @property
    def child_nodes(self) -> typing.Sequence[BigFrameNode]:
        return (self.child,)

    @property
    def fields(self) -> Sequence[Field]:
        return self.child.fields

    @property
    def explicitly_ordered(self) -> bool:
        return self.child.explicitly_ordered

    def transform_children(
        self, t: Callable[[BigFrameNode], BigFrameNode]
    ) -> UnaryNode:
        transformed = dataclasses.replace(self, child=t(self.child))
        if self == transformed:
            # reusing existing object speeds up eq, and saves a small amount of memory
            return self
        return transformed

    def replace_child(self, new_child: BigFrameNode) -> UnaryNode:
        new_self = dataclasses.replace(self, child=new_child)  # type: ignore
        return new_self

    @property
    def order_ambiguous(self) -> bool:
        return self.child.order_ambiguous


@dataclasses.dataclass(frozen=True, eq=False)
class SliceNode(UnaryNode):
    """Logical slice node conditionally becomes limit or filter over row numbers."""

    start: Optional[int]
    stop: Optional[int]
    step: int = 1

    @property
    def row_preserving(self) -> bool:
        """Whether this node preserves input rows."""
        return False

    @property
    def non_local(self) -> bool:
        """
        Whether this node combines information across multiple rows instead of processing rows independently.
        Used as an approximation for whether the expression may require shuffling to execute (and therefore be expensive).
        """
        return True

    # these are overestimates, more accurate numbers available by converting to concrete limit or analytic+filter ops
    @property
    def variables_introduced(self) -> int:
        return 2

    @property
    def relation_ops_created(self) -> int:
        return 2

    @property
    def is_limit(self) -> bool:
        """Returns whether this is equivalent to a ORDER BY ... LIMIT N."""
        # TODO: Handle tail case.
        return (
            (not self.start)
            and (self.step == 1)
            and (self.stop is not None)
            and (self.stop > 0)
        )

    @property
    def is_noop(self) -> bool:
        """Returns whether this node doesn't actually change the results."""
        # TODO: Handle tail case.
        return (
            ((not self.start) or (self.start == 0))
            and (self.step == 1)
            and ((self.stop is None) or (self.stop == self.row_count))
        )

    @property
    def row_count(self) -> typing.Optional[int]:
        child_length = self.child.row_count
        if child_length is None:
            return None
        return slices.slice_output_rows(
            (self.start, self.stop, self.step), child_length
        )

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return ()

    @property
    def referenced_ids(self) -> COLUMN_SET:
        return frozenset()

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> SliceNode:
        return self

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> SliceNode:
        return self


@dataclasses.dataclass(frozen=True, eq=False)
class InNode(BigFrameNode, AdditiveNode):
    """
    Special Join Type that only returns rows from the left side, as well as adding a bool column indicating whether a match exists on the right side.

    Modelled separately from join node, as this operation preserves row identity.
    """

    left_child: BigFrameNode
    right_child: BigFrameNode
    left_col: ex.DerefOp
    right_col: ex.DerefOp
    indicator_col: identifiers.ColumnId

    def _validate(self):
        assert not (
            set(self.left_child.ids) & set(self.right_child.ids)
        ), "Join ids collide"

    @property
    def row_preserving(self) -> bool:
        return False

    @property
    def non_local(self) -> bool:
        return True

    @property
    def child_nodes(self) -> typing.Sequence[BigFrameNode]:
        return (self.left_child, self.right_child)

    @property
    def order_ambiguous(self) -> bool:
        return False

    @property
    def explicitly_ordered(self) -> bool:
        # Preserves left ordering always
        return True

    @property
    def added_fields(self) -> Tuple[Field, ...]:
        return (Field(self.indicator_col, bigframes.dtypes.BOOL_DTYPE, nullable=False),)

    @property
    def fields(self) -> Sequence[Field]:
        return sequences.ChainedSequence(
            self.left_child.fields,
            self.added_fields,
        )

    @functools.cached_property
    def variables_introduced(self) -> int:
        """Defines the number of variables generated by the current node. Used to estimate query planning complexity."""
        return 1

    @property
    def joins(self) -> bool:
        return True

    @property
    def row_count(self) -> Optional[int]:
        return self.left_child.row_count

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return (self.indicator_col,)

    @property
    def referenced_ids(self) -> COLUMN_SET:
        return frozenset({self.left_col.id, self.right_col.id})

    @property
    def additive_base(self) -> BigFrameNode:
        return self.left_child

    @property
    def joins_nulls(self) -> bool:
        left_nullable = self.left_child.field_by_id[self.left_col.id].nullable
        right_nullable = self.right_child.field_by_id[self.right_col.id].nullable
        return left_nullable or right_nullable

    @property
    def _node_expressions(self):
        return (self.left_col, self.right_col)

    def replace_additive_base(self, node: BigFrameNode):
        return dataclasses.replace(self, left_child=node)

    def transform_children(self, t: Callable[[BigFrameNode], BigFrameNode]) -> InNode:
        transformed = dataclasses.replace(
            self, left_child=t(self.left_child), right_child=t(self.right_child)
        )
        if self == transformed:
            # reusing existing object speeds up eq, and saves a small amount of memory
            return self
        return transformed

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> InNode:
        return dataclasses.replace(
            self, indicator_col=mappings.get(self.indicator_col, self.indicator_col)
        )

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> InNode:
        return dataclasses.replace(self, left_col=self.left_col.remap_column_refs(mappings, allow_partial_bindings=True), right_col=self.right_col.remap_column_refs(mappings, allow_partial_bindings=True))  # type: ignore


@dataclasses.dataclass(frozen=True, eq=False)
class JoinNode(BigFrameNode):
    left_child: BigFrameNode
    right_child: BigFrameNode
    conditions: typing.Tuple[typing.Tuple[ex.DerefOp, ex.DerefOp], ...]
    type: typing.Literal["inner", "outer", "left", "right", "cross"]
    propogate_order: bool

    def _validate(self):
        assert not (
            set(self.left_child.ids) & set(self.right_child.ids)
        ), "Join ids collide"

    @property
    def row_preserving(self) -> bool:
        return False

    @property
    def non_local(self) -> bool:
        return True

    @property
    def child_nodes(self) -> typing.Sequence[BigFrameNode]:
        return (self.left_child, self.right_child)

    @property
    def order_ambiguous(self) -> bool:
        return True

    @property
    def explicitly_ordered(self) -> bool:
        return self.propogate_order

    @functools.cached_property
    def fields(self) -> Sequence[Field]:
        left_fields: Iterable[Field] = self.left_child.fields
        if self.type in ("right", "outer"):
            left_fields = map(lambda x: x.with_nullable(), left_fields)
        right_fields: Iterable[Field] = self.right_child.fields
        if self.type in ("left", "outer"):
            right_fields = map(lambda x: x.with_nullable(), right_fields)
        return (*left_fields, *right_fields)

    @property
    def joins_nulls(self) -> bool:
        for left_ref, right_ref in self.conditions:
            if (
                self.left_child.field_by_id[left_ref.id].nullable
                and self.right_child.field_by_id[right_ref.id].nullable
            ):
                return True
        return False

    @functools.cached_property
    def variables_introduced(self) -> int:
        """Defines the number of variables generated by the current node. Used to estimate query planning complexity."""
        return OVERHEAD_VARIABLES

    @property
    def joins(self) -> bool:
        return True

    @property
    def row_count(self) -> Optional[int]:
        if self.type == "cross":
            if self.left_child.row_count is None or self.right_child.row_count is None:
                return None
            return self.left_child.row_count * self.right_child.row_count

        return None

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return ()

    @property
    def referenced_ids(self) -> COLUMN_SET:
        return frozenset(
            itertools.chain.from_iterable(
                (*l_cond.column_references, *r_cond.column_references)
                for l_cond, r_cond in self.conditions
            )
        )

    @property
    def consumed_ids(self) -> COLUMN_SET:
        return frozenset(*self.ids, *self.referenced_ids)

    @property
    def _node_expressions(self):
        return tuple(itertools.chain.from_iterable(self.conditions))

    def transform_children(self, t: Callable[[BigFrameNode], BigFrameNode]) -> JoinNode:
        transformed = dataclasses.replace(
            self, left_child=t(self.left_child), right_child=t(self.right_child)
        )
        if self == transformed:
            # reusing existing object speeds up eq, and saves a small amount of memory
            return self
        return transformed

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> JoinNode:
        return self

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> JoinNode:
        new_conds = tuple(
            (
                l_cond.remap_column_refs(mappings, allow_partial_bindings=True),
                r_cond.remap_column_refs(mappings, allow_partial_bindings=True),
            )
            for l_cond, r_cond in self.conditions
        )
        return dataclasses.replace(self, conditions=new_conds)  # type: ignore


@dataclasses.dataclass(frozen=True, eq=False)
class ConcatNode(BigFrameNode):
    # TODO: Explcitly map column ids from each child
    children: Tuple[BigFrameNode, ...]
    output_ids: Tuple[identifiers.ColumnId, ...]

    def _validate(self):
        if len(self.children) == 0:
            raise ValueError("Concat requires at least one input table. Zero provided.")
        child_schemas = [child.schema.dtypes for child in self.children]
        if not len(set(child_schemas)) == 1:
            raise ValueError("All inputs must have identical dtypes. {child_schemas}")

    @property
    def child_nodes(self) -> typing.Sequence[BigFrameNode]:
        return self.children

    @property
    def order_ambiguous(self) -> bool:
        return any(child.order_ambiguous for child in self.children)

    @property
    def explicitly_ordered(self) -> bool:
        # Consider concat as an ordered operations (even though input frames may not be ordered)
        return True

    @property
    def fields(self) -> Sequence[Field]:
        # TODO: Output names should probably be aligned beforehand or be part of concat definition
        # TODO: Handle nullability
        return tuple(
            Field(id, field.dtype)
            for id, field in zip(self.output_ids, self.children[0].fields)
        )

    @functools.cached_property
    def variables_introduced(self) -> int:
        """Defines the number of variables generated by the current node. Used to estimate query planning complexity."""
        return len(self.schema.items) + OVERHEAD_VARIABLES

    @property
    def row_count(self) -> Optional[int]:
        sub_counts = [node.row_count for node in self.child_nodes]
        total = 0
        for count in sub_counts:
            if count is None:
                return None
            total += count
        return total

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return self.output_ids

    def transform_children(
        self, t: Callable[[BigFrameNode], BigFrameNode]
    ) -> ConcatNode:
        transformed = dataclasses.replace(
            self, children=tuple(t(child) for child in self.children)
        )
        if self == transformed:
            # reusing existing object speeds up eq, and saves a small amount of memory
            return self
        return transformed

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> ConcatNode:
        new_ids = tuple(mappings.get(id, id) for id in self.output_ids)
        return dataclasses.replace(self, output_ids=new_ids)

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> ConcatNode:
        return self


@dataclasses.dataclass(frozen=True, eq=False)
class FromRangeNode(BigFrameNode):
    # TODO: Enforce single-row, single column constraint
    start: BigFrameNode
    end: BigFrameNode
    step: int
    output_id: identifiers.ColumnId = identifiers.ColumnId("labels")

    @property
    def roots(self) -> typing.Set[BigFrameNode]:
        return {self}

    @property
    def child_nodes(self) -> typing.Sequence[BigFrameNode]:
        return (self.start, self.end)

    @property
    def order_ambiguous(self) -> bool:
        return False

    @property
    def explicitly_ordered(self) -> bool:
        return True

    @functools.cached_property
    def fields(self) -> Sequence[Field]:
        return (
            Field(self.output_id, next(iter(self.start.fields)).dtype, nullable=False),
        )

    @functools.cached_property
    def variables_introduced(self) -> int:
        """Defines the number of variables generated by the current node. Used to estimate query planning complexity."""
        return len(self.schema.items) + OVERHEAD_VARIABLES

    @property
    def row_count(self) -> Optional[int]:
        return None

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return (self.output_id,)

    @property
    def defines_namespace(self) -> bool:
        return True

    def transform_children(
        self, t: Callable[[BigFrameNode], BigFrameNode]
    ) -> FromRangeNode:
        transformed = dataclasses.replace(self, start=t(self.start), end=t(self.end))
        if self == transformed:
            # reusing existing object speeds up eq, and saves a small amount of memory
            return self
        return transformed

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> FromRangeNode:
        return dataclasses.replace(
            self, output_id=mappings.get(self.output_id, self.output_id)
        )

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> FromRangeNode:
        return self


# Input Nodex
# TODO: Most leaf nodes produce fixed column names based on the datasource
# They should support renaming
@dataclasses.dataclass(frozen=True, eq=False)
class LeafNode(BigFrameNode):
    @property
    def roots(self) -> typing.Set[BigFrameNode]:
        return {self}

    @property
    def fast_offsets(self) -> bool:
        return False

    @property
    def fast_ordered_limit(self) -> bool:
        return False

    def transform_children(self, t: Callable[[BigFrameNode], BigFrameNode]) -> LeafNode:
        return self


class ScanItem(typing.NamedTuple):
    id: identifiers.ColumnId
    dtype: bigframes.dtypes.Dtype  # Might be multiple logical types for a given physical source type
    source_id: str  # Flexible enough for both local data and bq data

    def with_id(self, id: identifiers.ColumnId) -> ScanItem:
        return ScanItem(id, self.dtype, self.source_id)

    def with_source_id(self, source_id: str) -> ScanItem:
        return ScanItem(self.id, self.dtype, source_id)


@dataclasses.dataclass(frozen=True)
class ScanList:
    """
    Defines the set of columns to scan from a source, along with the variable to bind the columns to.
    """

    items: typing.Tuple[ScanItem, ...]

    @classmethod
    def from_items(cls, items: Iterable[ScanItem]) -> ScanList:
        return cls(tuple(items))

    def filter_cols(
        self,
        ids: AbstractSet[identifiers.ColumnId],
    ) -> ScanList:
        """Drop columns from the scan that except those in the 'ids' arg."""
        result = ScanList(tuple(item for item in self.items if item.id in ids))
        if len(result.items) == 0:
            # We need to select something, or sql syntax breaks
            result = ScanList(self.items[:1])
        return result

    def project(
        self,
        selections: Mapping[identifiers.ColumnId, identifiers.ColumnId],
    ) -> ScanList:
        """Project given ids from the scanlist, dropping previous bindings."""
        by_id = {item.id: item for item in self.items}
        result = ScanList(
            tuple(
                by_id[old_id].with_id(new_id) for old_id, new_id in selections.items()
            )
        )
        if len(result.items) == 0:
            # We need to select something, or sql syntax breaks
            result = ScanList((self.items[:1]))
        return result

    def remap_source_ids(
        self,
        mapping: Mapping[str, str],
    ) -> ScanList:
        items = tuple(
            item.with_source_id(mapping.get(item.source_id, item.source_id))
            for item in self.items
        )
        return ScanList(items)

    def append(
        self, source_id: str, dtype: bigframes.dtypes.Dtype, id: identifiers.ColumnId
    ) -> ScanList:
        return ScanList((*self.items, ScanItem(id, dtype, source_id)))


@dataclasses.dataclass(frozen=True, eq=False)
class ReadLocalNode(LeafNode):
    # TODO: Track nullability for local data
    local_data_source: local_data.ManagedArrowTable
    # Mapping of local ids to bfet id.
    scan_list: ScanList
    session: bigframes.session.Session
    # Offsets are generated only if this is non-null
    offsets_col: Optional[identifiers.ColumnId] = None

    @property
    def fields(self) -> Sequence[Field]:
        fields = tuple(
            Field(col_id, dtype) for col_id, dtype, _ in self.scan_list.items
        )
        if self.offsets_col is not None:
            return tuple(
                itertools.chain(
                    fields,
                    (
                        Field(
                            self.offsets_col, bigframes.dtypes.INT_DTYPE, nullable=False
                        ),
                    ),
                )
            )
        return fields

    @property
    def variables_introduced(self) -> int:
        """Defines the number of variables generated by the current node. Used to estimate query planning complexity."""
        return len(self.scan_list.items) + 1

    @property
    def fast_offsets(self) -> bool:
        return True

    @property
    def fast_ordered_limit(self) -> bool:
        return True

    @property
    def order_ambiguous(self) -> bool:
        return False

    @property
    def explicitly_ordered(self) -> bool:
        return True

    @property
    def row_count(self) -> typing.Optional[int]:
        return self.local_data_source.metadata.row_count

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return tuple(item.id for item in self.fields)

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> ReadLocalNode:
        new_scan_list = ScanList(
            tuple(
                ScanItem(mappings.get(item.id, item.id), item.dtype, item.source_id)
                for item in self.scan_list.items
            )
        )
        new_offsets_col = (
            mappings.get(self.offsets_col, self.offsets_col)
            if (self.offsets_col is not None)
            else None
        )
        return dataclasses.replace(
            self, scan_list=new_scan_list, offsets_col=new_offsets_col
        )

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> ReadLocalNode:
        return self


@dataclasses.dataclass(frozen=True)
class GbqTable:
    project_id: str = dataclasses.field()
    dataset_id: str = dataclasses.field()
    table_id: str = dataclasses.field()
    physical_schema: Tuple[bq.SchemaField, ...] = dataclasses.field()
    is_physically_stored: bool = dataclasses.field()
    cluster_cols: typing.Optional[Tuple[str, ...]]

    @staticmethod
    def from_table(table: bq.Table, columns: Sequence[str] = ()) -> GbqTable:
        # Subsetting fields with columns can reduce cost of row-hash default ordering
        if columns:
            schema = tuple(item for item in table.schema if item.name in columns)
        else:
            schema = tuple(table.schema)
        return GbqTable(
            project_id=table.project,
            dataset_id=table.dataset_id,
            table_id=table.table_id,
            physical_schema=schema,
            is_physically_stored=(table.table_type in ["TABLE", "MATERIALIZED_VIEW"]),
            cluster_cols=None
            if table.clustering_fields is None
            else tuple(table.clustering_fields),
        )

    def get_table_ref(self) -> bq.TableReference:
        return bq.TableReference(
            bq.DatasetReference(self.project_id, self.dataset_id), self.table_id
        )

    @property
    @functools.cache
    def schema_by_id(self):
        return {col.name: col for col in self.physical_schema}


@dataclasses.dataclass(frozen=True)
class BigqueryDataSource:
    """
    Google BigQuery Data source.

    This should not be modified once defined, as all attributes contribute to the default ordering.
    """

    table: GbqTable
    at_time: typing.Optional[datetime.datetime] = None
    # Added for backwards compatibility, not validated
    sql_predicate: typing.Optional[str] = None
    ordering: typing.Optional[orderings.RowOrdering] = None
    n_rows: Optional[int] = None


## Put ordering in here or just add order_by node above?
@dataclasses.dataclass(frozen=True, eq=False)
class ReadTableNode(LeafNode):
    source: BigqueryDataSource
    # Subset of physical schema column
    # Mapping of table schema ids to bfet id.
    scan_list: ScanList

    table_session: bigframes.session.Session = dataclasses.field()

    def _validate(self):
        # enforce invariants
        physical_names = set(map(lambda i: i.name, self.source.table.physical_schema))
        if not set(scan.source_id for scan in self.scan_list.items).issubset(
            physical_names
        ):
            raise ValueError(
                f"Requested schema {self.scan_list} cannot be derived from table schemal {self.source.table.physical_schema}"
            )

    @property
    def session(self):
        return self.table_session

    @property
    def fields(self) -> Sequence[Field]:
        return tuple(
            Field(col_id, dtype, self.source.table.schema_by_id[source_id].is_nullable)
            for col_id, dtype, source_id in self.scan_list.items
        )

    @property
    def relation_ops_created(self) -> int:
        # Assume worst case, where readgbq actually has baked in analytic operation to generate index
        return 3

    @property
    def fast_offsets(self) -> bool:
        # Fast head is only supported when row offsets are available or data is clustered over ordering key.
        return (self.source.ordering is not None) and self.source.ordering.is_sequential

    @property
    def fast_ordered_limit(self) -> bool:
        if self.source.ordering is None:
            return False
        order_cols = self.source.ordering.all_ordering_columns
        # monotonicity would probably be fine
        if not all(col.scalar_expression.is_identity for col in order_cols):
            return False
        order_col_ids = tuple(
            cast(ex.DerefOp, col.scalar_expression).id.name for col in order_cols
        )
        cluster_col_ids = self.source.table.cluster_cols
        if cluster_col_ids is None:
            return False

        return order_col_ids == cluster_col_ids[: len(order_col_ids)]

    @property
    def order_ambiguous(self) -> bool:
        return (
            self.source.ordering is None
        ) or not self.source.ordering.is_total_ordering

    @property
    def explicitly_ordered(self) -> bool:
        return self.source.ordering is not None

    @functools.cached_property
    def variables_introduced(self) -> int:
        return len(self.scan_list.items) + 1

    @property
    def row_count(self) -> typing.Optional[int]:
        if self.source.sql_predicate is None and self.source.table.is_physically_stored:
            return self.source.n_rows
        return None

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return tuple(item.id for item in self.scan_list.items)

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> ReadTableNode:
        new_scan_list = ScanList(
            tuple(
                ScanItem(mappings.get(item.id, item.id), item.dtype, item.source_id)
                for item in self.scan_list.items
            )
        )
        return dataclasses.replace(self, scan_list=new_scan_list)

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> ReadTableNode:
        return self

    def with_order_cols(self):
        # Maybe the ordering should be required to always be in the scan list, and then we won't need this?
        if self.source.ordering is None:
            return self, orderings.RowOrdering()

        order_cols = {col.sql for col in self.source.ordering.referenced_columns}
        scan_cols = {col.source_id for col in self.scan_list.items}
        new_scan_cols = [
            ScanItem(
                identifiers.ColumnId.unique(),
                dtype=bigframes.dtypes.convert_schema_field(field)[1],
                source_id=field.name,
            )
            for field in self.source.table.physical_schema
            if (field.name in order_cols) and (field.name not in scan_cols)
        ]
        new_scan_list = ScanList(items=(*self.scan_list.items, *new_scan_cols))
        new_order = self.source.ordering.remap_column_refs(
            {identifiers.ColumnId(item.source_id): item.id for item in new_scan_cols},
            allow_partial_bindings=True,
        )
        return dataclasses.replace(self, scan_list=new_scan_list), new_order


@dataclasses.dataclass(frozen=True, eq=False)
class CachedTableNode(ReadTableNode):
    # The original BFET subtree that was cached
    # note: this isn't a "child" node.
    original_node: BigFrameNode = dataclasses.field()


# Unary nodes
@dataclasses.dataclass(frozen=True, eq=False)
class PromoteOffsetsNode(UnaryNode, AdditiveNode):
    col_id: identifiers.ColumnId

    @property
    def non_local(self) -> bool:
        return True

    @property
    def fields(self) -> Sequence[Field]:
        return sequences.ChainedSequence(self.child.fields, self.added_fields)

    @property
    def relation_ops_created(self) -> int:
        return 2

    @functools.cached_property
    def variables_introduced(self) -> int:
        return 1

    @property
    def row_count(self) -> Optional[int]:
        return self.child.row_count

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return (self.col_id,)

    @property
    def referenced_ids(self) -> COLUMN_SET:
        return frozenset()

    @property
    def added_fields(self) -> Tuple[Field, ...]:
        return (Field(self.col_id, bigframes.dtypes.INT_DTYPE, nullable=False),)

    @property
    def additive_base(self) -> BigFrameNode:
        return self.child

    def replace_additive_base(self, node: BigFrameNode) -> PromoteOffsetsNode:
        return dataclasses.replace(self, child=node)

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> PromoteOffsetsNode:
        return dataclasses.replace(self, col_id=mappings.get(self.col_id, self.col_id))

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> PromoteOffsetsNode:
        return self


@dataclasses.dataclass(frozen=True, eq=False)
class FilterNode(UnaryNode):
    # TODO: Infer null constraints from predicate
    predicate: ex.Expression

    @property
    def row_preserving(self) -> bool:
        return False

    @property
    def variables_introduced(self) -> int:
        return 1

    @property
    def row_count(self) -> Optional[int]:
        return None

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return ()

    @property
    def consumed_ids(self) -> COLUMN_SET:
        return frozenset(self.ids) | self.referenced_ids

    @property
    def referenced_ids(self) -> COLUMN_SET:
        return frozenset(self.predicate.column_references)

    @property
    def _node_expressions(self):
        return (self.predicate,)

    def transform_exprs(
        self, fn: Callable[[ex.Expression], ex.Expression]
    ) -> FilterNode:
        return dataclasses.replace(
            self,
            predicate=fn(self.predicate),
        )

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> FilterNode:
        return self

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> FilterNode:
        return dataclasses.replace(
            self,
            predicate=self.predicate.remap_column_refs(
                mappings, allow_partial_bindings=True
            ),
        )


@dataclasses.dataclass(frozen=True, eq=False)
class OrderByNode(UnaryNode):
    by: Tuple[OrderingExpression, ...]
    # This is an optimization, if true, can discard previous orderings.
    # might be a total ordering even if false
    is_total_order: bool = False

    @property
    def variables_introduced(self) -> int:
        return 0

    @property
    def relation_ops_created(self) -> int:
        # Doesnt directly create any relational operations
        return 0

    @property
    def explicitly_ordered(self) -> bool:
        return True

    @property
    def row_count(self) -> Optional[int]:
        return self.child.row_count

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return ()

    @property
    def consumed_ids(self) -> COLUMN_SET:
        return frozenset(self.ids) | self.referenced_ids

    @property
    def referenced_ids(self) -> COLUMN_SET:
        return frozenset(
            itertools.chain.from_iterable(map(lambda x: x.referenced_columns, self.by))
        )

    @property
    def _node_expressions(self):
        return tuple(map(lambda x: x.scalar_expression, self.by))

    def transform_exprs(
        self, fn: Callable[[ex.Expression], ex.Expression]
    ) -> OrderByNode:
        new_by = cast(
            tuple[OrderingExpression, ...],
            tuple(
                dataclasses.replace(
                    by_expr, scalar_expression=fn(by_expr.scalar_expression)
                )
                for by_expr in self.by
            ),
        )
        return dataclasses.replace(self, by=new_by)

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> OrderByNode:
        return self

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> OrderByNode:
        all_refs = set(
            itertools.chain.from_iterable(map(lambda x: x.referenced_columns, self.by))
        )
        ref_mapping = {id: ex.DerefOp(mappings[id]) for id in all_refs}
        return self.transform_exprs(
            lambda ex: ex.bind_refs(ref_mapping, allow_partial_bindings=True)
        )


@dataclasses.dataclass(frozen=True, eq=False)
class ReversedNode(UnaryNode):
    # useless field to make sure has distinct hash
    reversed: bool = True

    @property
    def variables_introduced(self) -> int:
        return 0

    @property
    def relation_ops_created(self) -> int:
        # Doesnt directly create any relational operations
        return 0

    @property
    def row_count(self) -> Optional[int]:
        return self.child.row_count

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return ()

    @property
    def referenced_ids(self) -> COLUMN_SET:
        return frozenset()

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> ReversedNode:
        return self

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> ReversedNode:
        return self


class AliasedRef(typing.NamedTuple):
    ref: ex.DerefOp
    id: identifiers.ColumnId

    @classmethod
    def identity(cls, id: identifiers.ColumnId) -> AliasedRef:
        return cls(ex.DerefOp(id), id)

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> AliasedRef:
        return AliasedRef(self.ref, mappings.get(self.id, self.id))

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> AliasedRef:
        return AliasedRef(ex.DerefOp(mappings.get(self.ref.id, self.ref.id)), self.id)


@dataclasses.dataclass(frozen=True, eq=False)
class SelectionNode(UnaryNode):
    input_output_pairs: Tuple[AliasedRef, ...]

    def _validate(self):
        for ref, _ in self.input_output_pairs:
            if ref.id not in set(self.child.ids):
                raise ValueError(f"Reference to column not in child: {ref.id}")

    @functools.cached_property
    def fields(self) -> Sequence[Field]:
        input_fields_by_id = {field.id: field for field in self.child.fields}
        return tuple(
            Field(
                output,
                input_fields_by_id[ref.id].dtype,
                input_fields_by_id[ref.id].nullable,
            )
            for ref, output in self.input_output_pairs
        )

    @property
    def variables_introduced(self) -> int:
        # This operation only renames variables, doesn't actually create new ones
        return 0

    @property
    def has_multi_referenced_ids(self) -> bool:
        referenced = tuple(ref.ref.id for ref in self.input_output_pairs)
        return len(referenced) != len(set(referenced))

    # TODO: Reuse parent namespace
    # Currently, Selection node allows renaming an reusing existing names, so it must establish a
    # new namespace.
    @property
    def defines_namespace(self) -> bool:
        return True

    @property
    def row_count(self) -> Optional[int]:
        return self.child.row_count

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return tuple(id for _, id in self.input_output_pairs)

    @property
    def consumed_ids(self) -> COLUMN_SET:
        return frozenset(ref.id for ref, id in self.input_output_pairs)

    @property
    def _node_expressions(self):
        return tuple(ref for ref, id in self.input_output_pairs)

    def get_id_mapping(self) -> dict[identifiers.ColumnId, identifiers.ColumnId]:
        return {ref.id: id for ref, id in self.input_output_pairs}

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> SelectionNode:
        new_fields = tuple(
            item.remap_vars(mappings) for item in self.input_output_pairs
        )
        return dataclasses.replace(self, input_output_pairs=new_fields)

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> SelectionNode:
        new_fields = tuple(
            item.remap_refs(mappings) for item in self.input_output_pairs
        )
        return dataclasses.replace(self, input_output_pairs=new_fields)  # type: ignore


@dataclasses.dataclass(frozen=True, eq=False)
class ProjectionNode(UnaryNode, AdditiveNode):
    """Assigns new variables (without modifying existing ones)"""

    assignments: typing.Tuple[typing.Tuple[ex.Expression, identifiers.ColumnId], ...]

    def _validate(self):
        for expression, _ in self.assignments:
            # throws TypeError if invalid
            _ = ex.bind_schema_fields(expression, self.child.field_by_id).output_type
        # Cannot assign to existing variables - append only!
        assert all(name not in self.child.schema.names for _, name in self.assignments)

    @functools.cached_property
    def added_fields(self) -> Tuple[Field, ...]:
        fields = []
        for expr, id in self.assignments:
            bound_expr = ex.bind_schema_fields(expr, self.child.field_by_id)
            field = Field(
                id,
                bigframes.dtypes.dtype_for_etype(bound_expr.output_type),
                nullable=bound_expr.nullable,
            )

            # Special case until we get better nullability inference in expression objects themselves
            if bound_expr.is_identity and not any(
                self.child.field_by_id[id].nullable for id in expr.column_references
            ):
                field = field.with_nonnull()
            fields.append(field)

        return tuple(fields)

    @property
    def fields(self) -> Sequence[Field]:
        return sequences.ChainedSequence(self.child.fields, self.added_fields)

    @property
    def variables_introduced(self) -> int:
        # ignore passthrough expressions
        new_vars = sum(1 for i in self.assignments if not i[0].is_identity)
        return new_vars

    @property
    def row_count(self) -> Optional[int]:
        return self.child.row_count

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return tuple(id for _, id in self.assignments)

    @property
    def consumed_ids(self) -> COLUMN_SET:
        return frozenset(
            itertools.chain.from_iterable(
                i[0].column_references for i in self.assignments
            )
        )

    @property
    def referenced_ids(self) -> COLUMN_SET:
        return frozenset(
            itertools.chain.from_iterable(
                ex.column_references for ex, id in self.assignments
            )
        )

    @property
    def _node_expressions(self):
        return tuple(ex for ex, id in self.assignments)

    @property
    def additive_base(self) -> BigFrameNode:
        return self.child

    def transform_exprs(
        self, fn: Callable[[ex.Expression], ex.Expression]
    ) -> ProjectionNode:
        new_fields = tuple((fn(ex), id) for ex, id in self.assignments)
        return dataclasses.replace(self, assignments=new_fields)

    def replace_additive_base(self, node: BigFrameNode) -> ProjectionNode:
        return dataclasses.replace(self, child=node)

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> ProjectionNode:
        new_fields = tuple((ex, mappings.get(id, id)) for ex, id in self.assignments)
        return dataclasses.replace(self, assignments=new_fields)

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> ProjectionNode:
        new_fields = tuple(
            (ex.remap_column_refs(mappings, allow_partial_bindings=True), id)
            for ex, id in self.assignments
        )
        return dataclasses.replace(self, assignments=new_fields)


@dataclasses.dataclass(frozen=True, eq=False)
class AggregateNode(UnaryNode):
    aggregations: typing.Tuple[typing.Tuple[ex.Aggregation, identifiers.ColumnId], ...]
    by_column_ids: typing.Tuple[ex.DerefOp, ...] = tuple([])
    order_by: Tuple[OrderingExpression, ...] = ()
    dropna: bool = True

    @property
    def row_preserving(self) -> bool:
        return False

    @property
    def non_local(self) -> bool:
        return True

    @functools.cached_property
    def fields(self) -> Sequence[Field]:
        # TODO: Use child nullability to infer grouping key nullability
        by_fields = (self.child.field_by_id[ref.id] for ref in self.by_column_ids)
        if self.dropna:
            by_fields = (field.with_nonnull() for field in by_fields)
        # TODO: Label aggregate ops to determine which are guaranteed non-null
        agg_items = (
            Field(
                id,
                bigframes.dtypes.dtype_for_etype(
                    agg.output_type(self.child.field_by_id)
                ),
                nullable=True,
            )
            for agg, id in self.aggregations
        )
        return tuple(itertools.chain(by_fields, agg_items))

    @property
    def variables_introduced(self) -> int:
        return len(self.aggregations) + len(self.by_column_ids)

    @property
    def order_ambiguous(self) -> bool:
        return False

    @property
    def explicitly_ordered(self) -> bool:
        return True

    @property
    def row_count(self) -> Optional[int]:
        if not self.by_column_ids:
            return 1
        return None

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return tuple(id for _, id in self.aggregations)

    @property
    def consumed_ids(self) -> COLUMN_SET:
        by_ids = (ref.id for ref in self.by_column_ids)
        agg_inputs = itertools.chain.from_iterable(
            agg.column_references for agg, _ in self.aggregations
        )
        order_ids = itertools.chain.from_iterable(
            part.scalar_expression.column_references for part in self.order_by
        )
        return frozenset(itertools.chain(by_ids, agg_inputs, order_ids))

    @property
    def has_ordered_ops(self) -> bool:
        return not all(
            aggregate.op.order_independent for aggregate, _ in self.aggregations
        )

    @property
    def _node_expressions(self):
        by_ids = (ref for ref in self.by_column_ids)
        aggs = tuple(agg for agg, _ in self.aggregations)
        order_ids = tuple(part.scalar_expression for part in self.order_by)
        return (*by_ids, *aggs, *order_ids)

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> AggregateNode:
        new_aggs = tuple((agg, mappings.get(id, id)) for agg, id in self.aggregations)
        return dataclasses.replace(self, aggregations=new_aggs)

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> AggregateNode:
        new_aggs = tuple(
            (agg.remap_column_refs(mappings, allow_partial_bindings=True), id)
            for agg, id in self.aggregations
        )
        new_by_ids = tuple(id.remap_column_refs(mappings) for id in self.by_column_ids)
        new_order_by = tuple(part.remap_column_refs(mappings) for part in self.order_by)
        return dataclasses.replace(
            self, by_column_ids=new_by_ids, aggregations=new_aggs, order_by=new_order_by
        )


@dataclasses.dataclass(frozen=True, eq=False)
class WindowOpNode(UnaryNode, AdditiveNode):
    expression: ex.Aggregation
    window_spec: window.WindowSpec
    output_name: identifiers.ColumnId
    never_skip_nulls: bool = False
    skip_reproject_unsafe: bool = False

    def _validate(self):
        """Validate the local data in the node."""
        # Since inner order and row bounds are coupled, rank ops can't be row bounded
        assert (
            not self.window_spec.is_row_bounded
        ) or self.expression.op.implicitly_inherits_order
        assert all(ref in self.child.ids for ref in self.expression.column_references)

    @property
    def non_local(self) -> bool:
        return True

    @property
    def fields(self) -> Sequence[Field]:
        return sequences.ChainedSequence(self.child.fields, (self.added_field,))

    @property
    def variables_introduced(self) -> int:
        return 1

    @property
    def added_fields(self) -> Tuple[Field, ...]:
        return (self.added_field,)

    @property
    def relation_ops_created(self) -> int:
        # Assume that if not reprojecting, that there is a sequence of window operations sharing the same window
        return 0 if self.skip_reproject_unsafe else 4

    @property
    def row_count(self) -> Optional[int]:
        return self.child.row_count

    @functools.cached_property
    def added_field(self) -> Field:
        input_fields = self.child.field_by_id
        # TODO: Determine if output could be non-null
        return Field(
            self.output_name,
            bigframes.dtypes.dtype_for_etype(self.expression.output_type(input_fields)),
        )

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return (self.output_name,)

    @property
    def consumed_ids(self) -> COLUMN_SET:
        return frozenset(
            set(self.ids).difference([self.output_name]).union(self.referenced_ids)
        )

    @property
    def referenced_ids(self) -> COLUMN_SET:
        return (
            frozenset()
            .union(self.expression.column_references)
            .union(self.window_spec.all_referenced_columns)
        )

    @property
    def inherits_order(self) -> bool:
        # does the op both use ordering at all? and if so, can it inherit order?
        op_inherits_order = (
            not self.expression.op.order_independent
        ) and self.expression.op.implicitly_inherits_order
        # range-bounded windows do not inherit orders because their ordering are
        # already defined before rewrite time.
        return op_inherits_order or self.window_spec.is_row_bounded

    @property
    def additive_base(self) -> BigFrameNode:
        return self.child

    @property
    def _node_expressions(self):
        return (self.expression, *self.window_spec.expressions)

    def replace_additive_base(self, node: BigFrameNode) -> WindowOpNode:
        return dataclasses.replace(self, child=node)

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> WindowOpNode:
        return dataclasses.replace(
            self, output_name=mappings.get(self.output_name, self.output_name)
        )

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> WindowOpNode:
        return dataclasses.replace(
            self,
            expression=self.expression.remap_column_refs(
                mappings, allow_partial_bindings=True
            ),
            window_spec=self.window_spec.remap_column_refs(
                mappings, allow_partial_bindings=True
            ),
        )


@dataclasses.dataclass(frozen=True, eq=False)
class RandomSampleNode(UnaryNode):
    fraction: float

    @property
    def deterministic(self) -> bool:
        return False

    @property
    def row_preserving(self) -> bool:
        return False

    @property
    def variables_introduced(self) -> int:
        return 1

    @property
    def row_count(self) -> Optional[int]:
        return None

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return ()

    @property
    def referenced_ids(self) -> COLUMN_SET:
        return frozenset()

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> RandomSampleNode:
        return self

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> RandomSampleNode:
        return self


# TODO: Explode should create a new column instead of overriding the existing one
@dataclasses.dataclass(frozen=True, eq=False)
class ExplodeNode(UnaryNode):
    column_ids: typing.Tuple[ex.DerefOp, ...]
    # Offsets are generated only if this is non-null
    offsets_col: Optional[identifiers.ColumnId] = None

    def _validate(self):
        for col in self.column_ids:
            assert col.id in self.child.ids

    @property
    def row_preserving(self) -> bool:
        return False

    @property
    def fields(self) -> Sequence[Field]:
        fields = (
            Field(
                field.id,
                bigframes.dtypes.arrow_dtype_to_bigframes_dtype(
                    self.child.get_type(field.id).pyarrow_dtype.value_type  # type: ignore
                ),
                nullable=True,
            )
            if field.id in set(map(lambda x: x.id, self.column_ids))
            else field
            for field in self.child.fields
        )
        if self.offsets_col is not None:
            return tuple(
                itertools.chain(
                    fields,
                    (
                        Field(
                            self.offsets_col, bigframes.dtypes.INT_DTYPE, nullable=False
                        ),
                    ),
                )
            )
        return tuple(fields)

    @property
    def relation_ops_created(self) -> int:
        return 3

    @functools.cached_property
    def variables_introduced(self) -> int:
        return len(self.column_ids) + 1

    @property
    def row_count(self) -> Optional[int]:
        return None

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return (self.offsets_col,) if (self.offsets_col is not None) else ()

    @property
    def referenced_ids(self) -> COLUMN_SET:
        return frozenset(ref.id for ref in self.column_ids)

    @property
    def _node_expressions(self):
        return self.column_ids

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> ExplodeNode:
        if (self.offsets_col is not None) and self.offsets_col in mappings:
            return dataclasses.replace(self, offsets_col=mappings[self.offsets_col])
        return self

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> ExplodeNode:
        new_ids = tuple(id.remap_column_refs(mappings) for id in self.column_ids)
        return dataclasses.replace(self, column_ids=new_ids)  # type: ignore


# Introduced during planing/compilation
# TODO: Enforce more strictly that this should never be a child node
@dataclasses.dataclass(frozen=True, eq=False)
class ResultNode(UnaryNode):
    output_cols: tuple[tuple[ex.DerefOp, str], ...]
    order_by: Optional[RowOrdering] = None
    limit: Optional[int] = None
    # TODO: CTE definitions

    def _validate(self):
        for ref, name in self.output_cols:
            assert ref.id in self.child.ids

    @property
    def node_defined_ids(self) -> Tuple[identifiers.ColumnId, ...]:
        return ()

    def remap_vars(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> ResultNode:
        return self

    def remap_refs(
        self, mappings: Mapping[identifiers.ColumnId, identifiers.ColumnId]
    ) -> ResultNode:
        output_cols = tuple(
            (ref.remap_column_refs(mappings), name) for ref, name in self.output_cols
        )
        order_by = self.order_by.remap_column_refs(mappings) if self.order_by else None
        return dataclasses.replace(self, output_cols=output_cols, order_by=order_by)  # type: ignore

    @property
    def fields(self) -> Sequence[Field]:
        # Fields property here is for output schema, not to be consumed by a parent node.
        input_fields_by_id = {field.id: field for field in self.child.fields}
        return tuple(
            Field(
                identifiers.ColumnId(output),
                input_fields_by_id[ref.id].dtype,
                input_fields_by_id[ref.id].nullable,
            )
            for ref, output in self.output_cols
        )

    @property
    def consumed_ids(self) -> COLUMN_SET:
        out_refs = frozenset(ref.id for ref, _ in self.output_cols)
        order_refs = self.order_by.referenced_columns if self.order_by else frozenset()
        return out_refs | order_refs

    @property
    def row_count(self) -> Optional[int]:
        child_count = self.child.row_count
        if child_count is None:
            return None
        if self.limit is None:
            return child_count
        return min(self.limit, child_count)

    @property
    def variables_introduced(self) -> int:
        return 0

    @property
    def _node_expressions(self):
        return tuple(ref for ref, _ in self.output_cols)


# Tree operators
def top_down(
    root: BigFrameNode,
    transform: Callable[[BigFrameNode], BigFrameNode],
) -> BigFrameNode:
    """
    Perform a top-down transformation of the BigFrameNode tree.
    """
    return root.top_down(transform)


def bottom_up(
    root: BigFrameNode,
    transform: Callable[[BigFrameNode], BigFrameNode],
) -> BigFrameNode:
    """
    Perform a bottom-up transformation of the BigFrameNode tree.

    The `transform` function is applied to each node *after* its children
    have been transformed.  This allows for transformations that depend
    on the results of transforming subtrees.

    Returns the transformed root node.
    """
    return root.bottom_up(transform)
