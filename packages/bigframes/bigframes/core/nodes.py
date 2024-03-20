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
from dataclasses import dataclass, field, fields
import functools
import itertools
import typing
from typing import Tuple

import pandas

import bigframes.core.expression as ex
import bigframes.core.guid
from bigframes.core.join_def import JoinColumnMapping, JoinDefinition, JoinSide
from bigframes.core.ordering import OrderingColumnReference
import bigframes.core.schema as schemata
import bigframes.core.window_spec as window
import bigframes.dtypes
import bigframes.operations.aggregations as agg_ops

if typing.TYPE_CHECKING:
    import ibis.expr.types as ibis_types

    import bigframes.core.ordering as orderings
    import bigframes.session


@dataclass(frozen=True)
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

    # BigFrameNode trees can be very deep so its important avoid recalculating the hash from scratch
    # Each subclass of BigFrameNode should use this property to implement __hash__
    # The default dataclass-generated __hash__ method is not cached
    @functools.cached_property
    def _node_hash(self):
        return hash(tuple(hash(getattr(self, field.name)) for field in fields(self)))

    @property
    def peekable(self) -> bool:
        """Indicates whether the node can be sampled efficiently"""
        return all(child.peekable for child in self.child_nodes)

    @property
    def roots(self) -> typing.Set[BigFrameNode]:
        roots = itertools.chain.from_iterable(
            map(lambda child: child.roots, self.child_nodes)
        )
        return set(roots)

    @property
    @abc.abstractmethod
    def schema(self) -> schemata.ArraySchema:
        ...


@dataclass(frozen=True)
class UnaryNode(BigFrameNode):
    child: BigFrameNode

    @property
    def child_nodes(self) -> typing.Sequence[BigFrameNode]:
        return (self.child,)

    @functools.cached_property
    def schema(self) -> schemata.ArraySchema:
        return self.child.schema


@dataclass(frozen=True)
class JoinNode(BigFrameNode):
    left_child: BigFrameNode
    right_child: BigFrameNode
    join: JoinDefinition
    allow_row_identity_join: bool = False

    @property
    def row_preserving(self) -> bool:
        return False

    @property
    def non_local(self) -> bool:
        return True

    @property
    def child_nodes(self) -> typing.Sequence[BigFrameNode]:
        return (self.left_child, self.right_child)

    def __hash__(self):
        return self._node_hash

    @property
    def peekable(self) -> bool:
        children_peekable = all(child.peekable for child in self.child_nodes)
        single_root = len(self.roots) == 1
        return children_peekable and single_root

    @functools.cached_property
    def schema(self) -> schemata.ArraySchema:
        def join_mapping_to_schema_item(mapping: JoinColumnMapping):
            result_id = mapping.destination_id
            result_dtype = (
                self.left_child.schema.get_type(mapping.source_id)
                if mapping.source_table == JoinSide.LEFT
                else self.right_child.schema.get_type(mapping.source_id)
            )
            return schemata.SchemaItem(result_id, result_dtype)

        items = tuple(
            join_mapping_to_schema_item(mapping) for mapping in self.join.mappings
        )
        return schemata.ArraySchema(items)


@dataclass(frozen=True)
class ConcatNode(BigFrameNode):
    children: Tuple[BigFrameNode, ...]

    def __post_init__(self):
        if len(self.children) == 0:
            raise ValueError("Concat requires at least one input table. Zero provided.")
        child_schemas = [child.schema.dtypes for child in self.children]
        if not len(set(child_schemas)) == 1:
            raise ValueError("All inputs must have identical dtypes. {child_schemas}")

    @property
    def child_nodes(self) -> typing.Sequence[BigFrameNode]:
        return self.children

    def __hash__(self):
        return self._node_hash

    @functools.cached_property
    def schema(self) -> schemata.ArraySchema:
        # TODO: Output names should probably be aligned beforehand or be part of concat definition
        items = tuple(
            schemata.SchemaItem(f"column_{i}", dtype)
            for i, dtype in enumerate(self.children[0].schema.dtypes)
        )
        return schemata.ArraySchema(items)


# Input Nodex
@dataclass(frozen=True)
class ReadLocalNode(BigFrameNode):
    feather_bytes: bytes
    data_schema: schemata.ArraySchema
    session: typing.Optional[bigframes.session.Session] = None

    def __hash__(self):
        return self._node_hash

    @property
    def peekable(self) -> bool:
        return True

    @property
    def roots(self) -> typing.Set[BigFrameNode]:
        return {self}

    @functools.cached_property
    def schema(self) -> schemata.ArraySchema:
        return self.data_schema


# TODO: Refactor to take raw gbq object reference
@dataclass(frozen=True)
class ReadGbqNode(BigFrameNode):
    table: ibis_types.Table = field()
    table_session: bigframes.session.Session = field()
    columns: Tuple[ibis_types.Value, ...] = field()
    hidden_ordering_columns: Tuple[ibis_types.Value, ...] = field()
    ordering: orderings.ExpressionOrdering = field()

    @property
    def session(self):
        return self.table_session

    def __hash__(self):
        return self._node_hash

    @property
    def peekable(self) -> bool:
        return True

    @property
    def roots(self) -> typing.Set[BigFrameNode]:
        return {self}

    @functools.cached_property
    def schema(self) -> schemata.ArraySchema:
        items = tuple(
            schemata.SchemaItem(
                value.get_name(),
                bigframes.dtypes.ibis_dtype_to_bigframes_dtype(value.type()),
            )
            for value in self.columns
        )
        return schemata.ArraySchema(items)


# Unary nodes
@dataclass(frozen=True)
class PromoteOffsetsNode(UnaryNode):
    col_id: str

    def __hash__(self):
        return self._node_hash

    @property
    def peekable(self) -> bool:
        return False

    @property
    def non_local(self) -> bool:
        return False

    @property
    def schema(self) -> schemata.ArraySchema:
        return self.child.schema.prepend(
            schemata.SchemaItem(self.col_id, bigframes.dtypes.INT_DTYPE)
        )


@dataclass(frozen=True)
class FilterNode(UnaryNode):
    predicate: ex.Expression

    @property
    def row_preserving(self) -> bool:
        return False

    def __hash__(self):
        return self._node_hash


@dataclass(frozen=True)
class OrderByNode(UnaryNode):
    by: Tuple[OrderingColumnReference, ...]

    def __hash__(self):
        return self._node_hash


@dataclass(frozen=True)
class ReversedNode(UnaryNode):
    # useless field to make sure has distinct hash
    reversed: bool = True

    def __hash__(self):
        return self._node_hash


@dataclass(frozen=True)
class ProjectionNode(UnaryNode):
    assignments: typing.Tuple[typing.Tuple[ex.Expression, str], ...]

    def __hash__(self):
        return self._node_hash

    @functools.cached_property
    def schema(self) -> schemata.ArraySchema:
        input_types = self.child.schema._mapping
        items = tuple(
            schemata.SchemaItem(
                id, bigframes.dtypes.dtype_for_etype(ex.output_type(input_types))
            )
            for ex, id in self.assignments
        )
        return schemata.ArraySchema(items)


# TODO: Merge RowCount into Aggregate Node?
# Row count can be compute from table metadata sometimes, so it is a bit special.
@dataclass(frozen=True)
class RowCountNode(UnaryNode):
    @property
    def row_preserving(self) -> bool:
        return False

    @property
    def non_local(self) -> bool:
        return True

    @functools.cached_property
    def schema(self) -> schemata.ArraySchema:
        return schemata.ArraySchema(
            (schemata.SchemaItem("count", bigframes.dtypes.INT_DTYPE),)
        )


@dataclass(frozen=True)
class AggregateNode(UnaryNode):
    aggregations: typing.Tuple[typing.Tuple[ex.Aggregation, str], ...]
    by_column_ids: typing.Tuple[str, ...] = tuple([])
    dropna: bool = True

    @property
    def row_preserving(self) -> bool:
        return False

    def __hash__(self):
        return self._node_hash

    @property
    def peekable(self) -> bool:
        return False

    @property
    def non_local(self) -> bool:
        return True

    @functools.cached_property
    def schema(self) -> schemata.ArraySchema:
        by_items = tuple(
            schemata.SchemaItem(id, self.child.schema.get_type(id))
            for id in self.by_column_ids
        )
        input_types = self.child.schema._mapping
        agg_items = tuple(
            schemata.SchemaItem(
                id, bigframes.dtypes.dtype_for_etype(agg.output_type(input_types))
            )
            for agg, id in self.aggregations
        )
        return schemata.ArraySchema(tuple([*by_items, *agg_items]))


@dataclass(frozen=True)
class WindowOpNode(UnaryNode):
    column_name: str
    op: agg_ops.UnaryWindowOp
    window_spec: window.WindowSpec
    output_name: typing.Optional[str] = None
    never_skip_nulls: bool = False
    skip_reproject_unsafe: bool = False

    def __hash__(self):
        return self._node_hash

    @property
    def peekable(self) -> bool:
        return False

    @property
    def non_local(self) -> bool:
        return True

    @functools.cached_property
    def schema(self) -> schemata.ArraySchema:
        input_type = self.child.schema.get_type(self.column_name)
        new_item_dtype = self.op.output_type(input_type)
        if self.output_name is None:
            return self.child.schema.update_dtype(self.column_name, new_item_dtype)
        if self.output_name in self.child.schema.names:
            return self.child.schema.update_dtype(self.output_name, new_item_dtype)
        return self.child.schema.append(
            schemata.SchemaItem(self.output_name, new_item_dtype)
        )


@dataclass(frozen=True)
class ReprojectOpNode(UnaryNode):
    def __hash__(self):
        return self._node_hash


@dataclass(frozen=True)
class UnpivotNode(UnaryNode):
    # TODO: Refactor unpivot
    row_labels: typing.Tuple[typing.Hashable, ...]
    unpivot_columns: typing.Tuple[
        typing.Tuple[str, typing.Tuple[typing.Optional[str], ...]], ...
    ]
    passthrough_columns: typing.Tuple[str, ...] = ()
    index_col_ids: typing.Tuple[str, ...] = ("index",)
    dtype: typing.Union[
        bigframes.dtypes.Dtype, typing.Tuple[bigframes.dtypes.Dtype, ...]
    ] = (pandas.Float64Dtype(),)
    how: typing.Literal["left", "right"] = "left"

    def __hash__(self):
        return self._node_hash

    @property
    def row_preserving(self) -> bool:
        return False

    @property
    def non_local(self) -> bool:
        return True

    @property
    def peekable(self) -> bool:
        return False

    @functools.cached_property
    def schema(self) -> schemata.ArraySchema:
        def infer_dtype(
            values: typing.Iterable[typing.Hashable],
        ) -> bigframes.dtypes.Dtype:
            item_types = map(lambda x: bigframes.dtypes.infer_literal_type(x), values)
            etype = functools.reduce(
                lambda t1, t2: bigframes.dtypes.lcd_type(t1, t2)
                if (t1 and t2)
                else None,
                item_types,
            )
            return bigframes.dtypes.dtype_for_etype(etype)

        label_tuples = [
            label if isinstance(label, tuple) else (label,) for label in self.row_labels
        ]
        idx_dtypes = [
            infer_dtype(map(lambda x: typing.cast(tuple, x)[i], label_tuples))
            for i in range(len(self.index_col_ids))
        ]

        index_items = [
            schemata.SchemaItem(id, dtype)
            for id, dtype in zip(self.index_col_ids, idx_dtypes)
        ]
        value_dtypes = (
            self.dtype
            if isinstance(self.dtype, tuple)
            else (self.dtype,) * len(self.unpivot_columns)
        )
        value_items = [
            schemata.SchemaItem(col[0], dtype)
            for col, dtype in zip(self.unpivot_columns, value_dtypes)
        ]
        passthrough_items = [
            schemata.SchemaItem(id, self.child.schema.get_type(id))
            for id in self.passthrough_columns
        ]
        return schemata.ArraySchema((*index_items, *value_items, *passthrough_items))


@dataclass(frozen=True)
class RandomSampleNode(UnaryNode):
    fraction: float

    @property
    def deterministic(self) -> bool:
        return False

    @property
    def row_preserving(self) -> bool:
        return False

    def __hash__(self):
        return self._node_hash
