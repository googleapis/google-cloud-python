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

"""Block is a 2D data structure that supports data mutability and views.

These data structures are shared by DataFrame and Series. This allows views to
link in both directions (DataFrame to Series and vice versa) and prevents
circular dependencies.
"""

from __future__ import annotations

import functools
import itertools
import typing
from typing import Iterable, List, Optional, Sequence, Tuple

import geopandas as gpd  # type: ignore
import google.cloud.bigquery as bigquery
import ibis.expr.schema as ibis_schema
import ibis.expr.types as ibis_types
import numpy
import pandas as pd
import pyarrow as pa  # type: ignore

import bigframes.core as core
import bigframes.core.guid as guid
import bigframes.core.indexes as indexes
import bigframes.core.ordering as ordering
import bigframes.dtypes
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops

# Type constraint for wherever column labels are used
Label = typing.Optional[str]


class BlockHolder(typing.Protocol):
    """Interface for mutable objects with state represented by a block value object."""

    def _set_block(self, block: Block):
        """Set the underlying block value of the object"""

    def _get_block(self) -> Block:
        """Get the underlying block value of the object"""


class Block:
    """A immutable 2D data structure."""

    def __init__(
        self,
        expr: core.ArrayValue,
        index_columns: Iterable[str] = (),
        column_labels: Optional[Sequence[Label]] = None,
        index_labels: Optional[Sequence[Label]] = None,
    ):
        """Construct a block object, will create default index if no index columns specified."""
        if index_labels and (len(index_labels) != len(list(index_columns))):
            raise ValueError(
                "'index_columns' and 'index_labels' must have equal length"
            )
        if len(list(index_columns)) == 0:
            expr, new_index_col_id = expr.promote_offsets()
            index_columns = [new_index_col_id]
        self._index_columns = tuple(index_columns)
        self._index_labels = (
            tuple(index_labels)
            if index_labels
            else tuple([None for _ in index_columns])
        )
        self._expr = self._normalize_expression(expr, self._index_columns)
        # TODO(tbergeron): Force callers to provide column labels
        self._column_labels = (
            tuple(column_labels) if column_labels else tuple(self.value_columns)
        )
        if len(self.value_columns) != len(self._column_labels):
            raise ValueError(
                f"'value_columns' (size {len(self.value_columns)}) and 'column_labels' (size {len(self._column_labels)}) must have equal length"
            )

    @property
    def index(self) -> indexes.IndexValue:
        """Row identities for values in the Block."""
        return indexes.IndexValue(self)

    @functools.cached_property
    def shape(self) -> typing.Tuple[int, int]:
        """Returns dimensions as (length, width) tuple."""
        impl_length, _ = self._expr.shape()
        return (impl_length, len(self.value_columns))

    @property
    def index_columns(self) -> Sequence[str]:
        """Column(s) to use as row labels."""
        return self._index_columns

    @property
    def index_labels(self) -> Sequence[Label]:
        """Name of column(s) to use as row labels."""
        return self._index_labels

    @property
    def value_columns(self) -> Sequence[str]:
        """All value columns, mutually exclusive with index columns."""
        return [
            column
            for column in self._expr.column_names
            if column not in self.index_columns
        ]

    @property
    def column_labels(self) -> List[Label]:
        return list(self._column_labels)

    @property
    def expr(self) -> core.ArrayValue:
        """Expression representing all columns, including index columns."""
        return self._expr

    @property
    def dtypes(
        self,
    ) -> Sequence[bigframes.dtypes.Dtype]:
        """Returns the dtypes of the value columns."""
        return [self.expr.get_column_type(col) for col in self.value_columns]

    @property
    def index_dtypes(
        self,
    ) -> Sequence[bigframes.dtypes.Dtype]:
        """Returns the dtypes of the index columns."""
        return [self.expr.get_column_type(col) for col in self.index_columns]

    @functools.cached_property
    def col_id_to_label(self) -> typing.Mapping[str, Label]:
        """Get column label for value columns, or index name for index columns"""
        return {
            col_id: label
            for col_id, label in zip(self.value_columns, self._column_labels)
        }

    @functools.cached_property
    def label_to_col_id(self) -> typing.Mapping[Label, typing.Sequence[str]]:
        """Get column label for value columns, or index name for index columns"""
        mapping: typing.Dict[Label, typing.Sequence[str]] = {}
        for id, label in self.col_id_to_label.items():
            mapping[label] = (*mapping.get(label, ()), id)
        return mapping

    @functools.cached_property
    def col_id_to_index_name(self) -> typing.Mapping[str, Label]:
        """Get column label for value columns, or index name for index columns"""
        return {
            col_id: label
            for col_id, label in zip(self.index_columns, self._index_labels)
        }

    @functools.cached_property
    def index_name_to_col_id(self) -> typing.Mapping[Label, typing.Sequence[str]]:
        """Get column label for value columns, or index name for index columns"""
        mapping: typing.Dict[Label, typing.Sequence[str]] = {}
        for id, label in self.col_id_to_index_name.items():
            mapping[label] = (*mapping.get(label, ()), id)
        return mapping

    def order_by(
        self,
        by: typing.Sequence[ordering.OrderingColumnReference],
        stable: bool = False,
    ) -> Block:
        return Block(
            self._expr.order_by(by, stable=stable),
            index_columns=self.index_columns,
            column_labels=self.column_labels,
            index_labels=self.index.names,
        )

    def reversed(self) -> Block:
        return Block(
            self._expr.reversed(),
            index_columns=self.index_columns,
            column_labels=self.column_labels,
            index_labels=self.index.names,
        )

    def reset_index(self, drop: bool = True) -> Block:
        """Reset the index of the block, promoting the old index to a value column.

        Arguments:
            name: this is the column id for the new value id derived from the old index

        Returns:
            A new Block because dropping index columns can break references
            from Index classes that point to this block.
        """
        block = self
        expr, new_index_col_id = self._expr.promote_offsets()
        if drop:
            # Even though the index might be part of the ordering, keep that
            # ordering expression as reset_index shouldn't change the row
            # order.
            expr = expr.drop_columns(self.index_columns)
            block = Block(
                expr,
                index_columns=[new_index_col_id],
                column_labels=self.column_labels,
                index_labels=[None],
            )
        else:
            index_labels = self.index.names
            index_labels_rewritten = []
            for level, label in enumerate(index_labels):
                if label is None:
                    if "index" not in self.column_labels:
                        label = "index"
                    else:
                        label = f"level_{level}"

                if label in self.column_labels:
                    raise ValueError(f"cannot insert {label}, already exists")
                index_labels_rewritten.append(label)

            block = Block(
                expr,
                index_columns=[new_index_col_id],
                column_labels=[*index_labels_rewritten, *self.column_labels],
                index_labels=[None],
            )
        return block

    def set_index(
        self, col_ids: typing.Sequence[str], drop: bool = True, append: bool = False
    ) -> Block:
        """Set the index of the block to

        Arguments:
            ids: columns to be converted to index columns
            drop: whether to drop the new index columns as value columns
            append: whether to discard the existing index or add on to it

        Returns:
            Block with new index
        """
        expr = self._expr

        new_index_columns = []
        new_index_labels = []
        for col_id in col_ids:
            col_copy_id = guid.generate_guid()
            expr = expr.assign(col_id, col_copy_id)
            new_index_columns.append(col_copy_id)
            new_index_labels.append(self.col_id_to_label[col_id])

        if append:
            new_index_columns = [*self.index_columns, *new_index_columns]
            new_index_labels = [*self._index_labels, *new_index_labels]
        else:
            expr = expr.drop_columns(self.index_columns)

        block = Block(
            expr,
            index_columns=new_index_columns,
            column_labels=self.column_labels,
            index_labels=new_index_labels,
        )
        if drop:
            # These are the value columns, new index uses the copies, so this is safe
            block = block.drop_columns(col_ids)
        return block

    def drop_levels(self, ids: typing.Sequence[str]):
        for id in ids:
            if id not in self.index_columns:
                raise ValueError(f"{id} is not an index column")
        expr = self._expr.drop_columns(ids)
        remaining_index_col_ids = [
            col_id for col_id in self.index_columns if col_id not in ids
        ]
        if len(remaining_index_col_ids) == 0:
            raise ValueError("Cannot drop all index levels, at least 1 must remain.")
        level_names = [
            self.col_id_to_index_name[index_id] for index_id in remaining_index_col_ids
        ]
        return Block(expr, remaining_index_col_ids, self.column_labels, level_names)

    def reorder_levels(self, ids: typing.Sequence[str]):
        if sorted(self.index_columns) != sorted(ids):
            raise ValueError("Cannot drop or duplicate levels using reorder_levels.")
        level_names = [self.col_id_to_index_name[index_id] for index_id in ids]
        return Block(self.expr, ids, self.column_labels, level_names)

    def _to_dataframe(self, result, schema: ibis_schema.Schema) -> pd.DataFrame:
        """Convert BigQuery data to pandas DataFrame with specific dtypes."""
        df = result.to_dataframe(
            bool_dtype=pd.BooleanDtype(),
            int_dtype=pd.Int64Dtype(),
            float_dtype=pd.Float64Dtype(),
            string_dtype=pd.StringDtype(storage="pyarrow"),
            date_dtype=pd.ArrowDtype(pa.date32()),
            datetime_dtype=pd.ArrowDtype(pa.timestamp("us")),
            time_dtype=pd.ArrowDtype(pa.time64("us")),
            timestamp_dtype=pd.ArrowDtype(pa.timestamp("us", tz="UTC")),
        )

        # Convert Geography column from StringDType to GeometryDtype.
        for column_name, ibis_dtype in schema.items():
            if ibis_dtype.is_geospatial():
                df[column_name] = gpd.GeoSeries.from_wkt(
                    # https://github.com/geopandas/geopandas/issues/1879
                    df[column_name].replace({numpy.nan: None}),
                    # BigQuery geography type is based on the WGS84 reference ellipsoid.
                    crs="EPSG:4326",
                )
        return df

    def compute(
        self, value_keys: Optional[Iterable[str]] = None, max_results=None
    ) -> Tuple[pd.DataFrame, bigquery.QueryJob]:
        """Run query and download results as a pandas DataFrame."""
        df, _, query_job = self._compute_and_count(
            value_keys=value_keys, max_results=max_results
        )
        return df, query_job

    def _compute_and_count(
        self, value_keys: Optional[Iterable[str]] = None, max_results=None
    ) -> Tuple[pd.DataFrame, int, bigquery.QueryJob]:
        """Run query and download results as a pandas DataFrame. Return the total number of results as well."""
        # TODO(swast): Allow for dry run and timeout.
        expr = self._expr

        value_column_names = value_keys or self.value_columns
        if value_keys is not None:
            index_columns = (
                expr.get_column(column_name) for column_name in self._index_columns
            )
            value_columns = (expr.get_column(column_name) for column_name in value_keys)
            expr = expr.projection(itertools.chain(index_columns, value_columns))

        results_iterator, query_job = expr.start_query(max_results=max_results)
        df = self._to_dataframe(
            results_iterator,
            expr.to_ibis_expr().schema(),
        )

        df = df.loc[:, [*self.index_columns, *value_column_names]]
        if self.index_columns:
            df = df.set_index(list(self.index_columns))
            df.index.names = self.index.names  # type: ignore

        return df, results_iterator.total_rows, query_job

    def with_column_labels(self, value: typing.Iterable[Label]) -> Block:
        label_list = tuple(value)
        if len(label_list) != len(self.value_columns):
            raise ValueError(
                f"The column labels size `{len(label_list)} ` should equal to the value"
                + f"columns size: {len(self.value_columns)}."
            )
        return Block(
            self._expr,
            index_columns=self.index_columns,
            column_labels=label_list,
            index_labels=self.index.names,
        )

    def with_index_labels(self, value: typing.Sequence[Label]) -> Block:
        if len(value) != len(self.index_columns):
            raise ValueError(
                f"The index labels size `{len(value)} ` should equal to the index"
                + f"columns size: {len(self.value_columns)}."
            )
        return Block(
            self._expr,
            index_columns=self.index_columns,
            column_labels=self.column_labels,
            index_labels=tuple(value),
        )

    def get_value_col_exprs(
        self, column_names: Optional[Sequence[str]] = None
    ) -> List[ibis_types.Value]:
        """Retrive value column expressions."""
        column_names = self.value_columns if column_names is None else column_names
        return [self._expr.get_column(column_name) for column_name in column_names]

    def apply_unary_op(
        self, column: str, op: ops.UnaryOp, result_label: Label = None
    ) -> typing.Tuple[Block, str]:
        """
        Apply a unary op to the block. Creates a new column to store the result.
        """
        # TODO(tbergeron): handle labels safely so callers don't need to
        result_id = guid.generate_guid()
        expr = self._expr.project_unary_op(column, op, result_id)
        block = Block(
            expr,
            index_columns=self.index_columns,
            column_labels=[*self.column_labels, result_label],
            index_labels=self.index.names,
        )
        return (block, result_id)

    def apply_binary_op(
        self,
        left_column_id: str,
        right_column_id: str,
        op: ops.BinaryOp,
        result_label: Label = None,
    ) -> typing.Tuple[Block, str]:
        result_id = guid.generate_guid()
        expr = self._expr.project_binary_op(
            left_column_id, right_column_id, op, result_id
        )
        block = Block(
            expr,
            index_columns=self.index_columns,
            column_labels=[*self.column_labels, result_label],
            index_labels=self.index.names,
        )
        return (block, result_id)

    def apply_ternary_op(
        self,
        col_id_1: str,
        col_id_2: str,
        col_id_3: str,
        op: ops.TernaryOp,
        result_label: Label = None,
    ) -> typing.Tuple[Block, str]:
        result_id = guid.generate_guid()
        expr = self._expr.project_ternary_op(
            col_id_1, col_id_2, col_id_3, op, result_id
        )
        block = Block(
            expr,
            index_columns=self.index_columns,
            column_labels=[*self.column_labels, result_label],
            index_labels=self.index.names,
        )
        return (block, result_id)

    def multi_apply_window_op(
        self,
        columns: typing.Sequence[str],
        op: agg_ops.WindowOp,
        window_spec: core.WindowSpec,
        *,
        skip_null_groups: bool = False,
    ) -> Block:
        block = self
        for i, col_id in enumerate(columns):
            label = self.col_id_to_label[col_id]
            block, result_id = block.apply_window_op(
                col_id,
                op,
                window_spec=window_spec,
                skip_reproject_unsafe=(i + 1) < len(columns),
                result_label=label,
                skip_null_groups=skip_null_groups,
            )
            block = block.copy_values(result_id, col_id)
            block = block.drop_columns([result_id])
        return block

    def multi_apply_unary_op(
        self,
        columns: typing.Sequence[str],
        op: ops.UnaryOp,
    ) -> Block:
        block = self
        for i, col_id in enumerate(columns):
            label = self.col_id_to_label[col_id]
            block, result_id = block.apply_unary_op(
                col_id,
                op,
                result_label=label,
            )
            block = block.copy_values(result_id, col_id)
            block = block.drop_columns([result_id])
        return block

    def apply_window_op(
        self,
        column: str,
        op: agg_ops.WindowOp,
        window_spec: core.WindowSpec,
        *,
        result_label: Label = None,
        skip_null_groups: bool = False,
        skip_reproject_unsafe: bool = False,
    ) -> typing.Tuple[Block, str]:
        result_id = guid.generate_guid()
        expr = self._expr.project_window_op(
            column,
            op,
            window_spec,
            result_id,
            skip_null_groups=skip_null_groups,
            skip_reproject_unsafe=skip_reproject_unsafe,
        )
        block = Block(
            expr,
            index_columns=self.index_columns,
            column_labels=[*self.column_labels, result_label],
            index_labels=self._index_labels,
        )
        return (block, result_id)

    def copy_values(self, source_column_id: str, destination_column_id: str) -> Block:
        expr = self.expr.assign(source_column_id, destination_column_id)
        return Block(
            expr,
            index_columns=self.index_columns,
            column_labels=self.column_labels,
            index_labels=self._index_labels,
        )

    def create_constant(
        self,
        scalar_constant: typing.Any,
        label: Label = None,
        dtype: typing.Optional[bigframes.dtypes.Dtype] = None,
    ) -> typing.Tuple[Block, str]:
        result_id = guid.generate_guid()
        expr = self.expr.assign_constant(result_id, scalar_constant, dtype=dtype)
        labels = [*self.column_labels, label]
        return (
            Block(
                expr,
                index_columns=self.index_columns,
                column_labels=labels,
                index_labels=self.index.names,
            ),
            result_id,
        )

    def assign_label(self, column_id: str, new_label: Label) -> Block:
        col_index = self.value_columns.index(column_id)
        new_labels = list(self.column_labels)
        new_labels[col_index] = new_label
        return self.with_column_labels(new_labels)

    def filter(self, column_name: str):
        condition = typing.cast(
            ibis_types.BooleanValue, self._expr.get_column(column_name)
        )
        filtered_expr = self.expr.filter(condition)
        return Block(
            filtered_expr,
            index_columns=self.index_columns,
            column_labels=self.column_labels,
            index_labels=self.index.names,
        )

    def aggregate_all_and_pivot(
        self,
        operation: agg_ops.AggregateOp,
        *,
        value_col_id: str = "values",
        dropna: bool = True,
        dtype=pd.Float64Dtype(),
    ) -> Block:
        aggregations = [(col_id, operation, col_id) for col_id in self.value_columns]
        result_expr = self.expr.aggregate(
            aggregations, dropna=dropna
        ).transpose_single_row(
            labels=self.column_labels,
            index_col_id="index",
            value_col_id=value_col_id,
            dtype=dtype,
        )
        return Block(result_expr, index_columns=["index"], column_labels=[None])

    def select_column(self, id: str) -> Block:
        return self.select_columns([id])

    def select_columns(self, ids: typing.Sequence[str]) -> Block:
        expr = self._expr.select_columns([*self.index_columns, *ids])
        col_labels = self._get_labels_for_columns(ids)
        return Block(expr, self.index_columns, col_labels, self.index.names)

    def drop_columns(self, ids_to_drop: typing.Sequence[str]) -> Block:
        """Drops columns by id. Can drop index"""
        if set(ids_to_drop) & set(self.index_columns):
            raise ValueError(
                "Cannot directly drop index column. Use reset_index(drop=True)"
            )
        expr = self._expr.drop_columns(ids_to_drop)
        remaining_value_col_ids = [
            col_id for col_id in self.value_columns if (col_id not in ids_to_drop)
        ]
        labels = self._get_labels_for_columns(remaining_value_col_ids)
        return Block(expr, self.index_columns, labels, self.index.names)

    def rename(self, *, columns: typing.Mapping[Label, Label]):
        # TODO(tbergeron) Support function(Callable) as columns parameter.
        col_labels = [
            (columns.get(col_label, col_label)) for col_label in self.column_labels
        ]
        return self.with_column_labels(col_labels)

    def aggregate(
        self,
        by_column_ids: typing.Sequence[str],
        aggregations: typing.Sequence[typing.Tuple[str, agg_ops.AggregateOp]],
        *,
        as_index: bool = True,
        dropna: bool = True,
    ) -> typing.Tuple[Block, typing.Sequence[str]]:
        """
        Apply aggregations to the block. Callers responsible for setting index column(s) after.
        Arguments:
            by_column_id: column id of the aggregation key, this is preserved through the transform and used as index
            aggregations: input_column_id, operation tuples
            as_index: if True, grouping keys will be index columns in result, otherwise they will be non-index columns.
            dropna: whether null keys should be dropped
        """
        agg_specs = [
            (input_id, operation, guid.generate_guid())
            for input_id, operation in aggregations
        ]
        output_col_ids = [agg_spec[2] for agg_spec in agg_specs]
        result_expr = self.expr.aggregate(agg_specs, by_column_ids, dropna=dropna)

        aggregate_labels = self._get_labels_for_columns(
            [agg[0] for agg in aggregations]
        )
        if as_index:
            # TODO: Generalize to multi-index
            names: typing.List[Label] = []
            for by_col_id in by_column_ids:
                if by_col_id in self.index_columns:
                    # Groupby level 0 case, keep index name
                    index_name = self.col_id_to_index_name[by_col_id]
                else:
                    index_name = self.col_id_to_label[by_col_id]
                names.append(index_name)
            return (
                Block(
                    result_expr,
                    index_columns=by_column_ids,
                    column_labels=aggregate_labels,
                    index_labels=names,
                ),
                output_col_ids,
            )
        else:
            by_column_labels = self._get_labels_for_columns(by_column_ids)
            labels = (*by_column_labels, *aggregate_labels)
            return Block(result_expr, column_labels=labels), output_col_ids

    def _get_labels_for_columns(self, column_ids: typing.Sequence[str]):
        """Get column label for value columns, or index name for index columns"""
        lookup = self.col_id_to_label
        return [lookup.get(col_id, None) for col_id in column_ids]

    def _normalize_expression(
        self,
        expr: core.ArrayValue,
        index_columns: typing.Sequence[str],
        assert_value_size: typing.Optional[int] = None,
    ):
        """Normalizes expression by moving index columns to left."""
        value_columns = [
            col_id for col_id in expr.column_names.keys() if col_id not in index_columns
        ]
        if (assert_value_size is not None) and (
            len(value_columns) != assert_value_size
        ):
            raise ValueError("Unexpected number of value columns.")
        return expr.select_columns([*index_columns, *value_columns])

    def slice(
        self: bigframes.core.blocks.Block,
        start: typing.Optional[int] = None,
        stop: typing.Optional[int] = None,
        step: typing.Optional[int] = None,
    ) -> bigframes.core.blocks.Block:
        sliced_expr = self.expr.slice(start=start, stop=stop, step=step)
        # since this is slice, return a copy even if unchanged
        block = Block(
            sliced_expr,
            index_columns=self.index_columns,
            column_labels=self.column_labels,
            index_labels=self._index_labels,
        )
        return block

    def promote_offsets(self, label: Label = None) -> typing.Tuple[Block, str]:
        expr, result_id = self._expr.promote_offsets()
        return (
            Block(
                expr,
                index_columns=self.index_columns,
                column_labels=[label, *self.column_labels],
                index_labels=self._index_labels,
            ),
            result_id,
        )

    def add_prefix(self, prefix: str, axis: str | int | None = None) -> Block:
        axis_number = _get_axis_number(axis)
        if axis_number == 0:
            expr = self._expr
            for index_col in self._index_columns:
                expr = expr.project_unary_op(index_col, ops.AsTypeOp("string"))
                prefix_op = ops.BinopPartialLeft(ops.add_op, prefix)
                expr = expr.project_unary_op(index_col, prefix_op)
            return Block(
                expr,
                index_columns=self.index_columns,
                column_labels=self.column_labels,
                index_labels=self.index.names,
            )
        if axis_number == 1:
            expr = self._expr
            return Block(
                self._expr,
                index_columns=self.index_columns,
                column_labels=[f"{prefix}{label}" for label in self.column_labels],
                index_labels=self.index.names,
            )

    def add_suffix(self, suffix: str, axis: str | int | None = None) -> Block:
        axis_number = _get_axis_number(axis)
        if axis_number == 0:
            expr = self._expr
            for index_col in self._index_columns:
                expr = expr.project_unary_op(index_col, ops.AsTypeOp("string"))
                prefix_op = ops.BinopPartialRight(ops.add_op, suffix)
                expr = expr.project_unary_op(index_col, prefix_op)
            return Block(
                expr,
                index_columns=self.index_columns,
                column_labels=self.column_labels,
                index_labels=self.index.names,
            )
        if axis_number == 1:
            expr = self._expr
            return Block(
                self._expr,
                index_columns=self.index_columns,
                column_labels=[f"{label}{suffix}" for label in self.column_labels],
                index_labels=self.index.names,
            )

    def concat(
        self,
        other: typing.Iterable[Block],
        how: typing.Literal["inner", "outer"],
        ignore_index=False,
    ):
        blocks: typing.List[Block] = [self, *other]
        if ignore_index:
            blocks = [block.reset_index() for block in blocks]

        result_labels = _align_indices(blocks)

        index_nlevels = blocks[0].index.nlevels

        aligned_schema = _align_schema(blocks, how=how)
        aligned_blocks = [
            _align_block_to_schema(block, aligned_schema) for block in blocks
        ]
        result_expr = aligned_blocks[0]._expr.concat(
            [block._expr for block in aligned_blocks[1:]]
        )
        result_block = Block(
            result_expr,
            index_columns=list(result_expr.column_names.keys())[:index_nlevels],
            column_labels=aligned_blocks[0].column_labels,
            index_labels=result_labels,
        )
        if ignore_index:
            result_block = result_block.reset_index()
        return result_block


def block_from_local(data, session=None, use_index=True) -> Block:
    # TODO(tbergeron): Handle duplicate column labels
    pd_data = pd.DataFrame(data)

    column_labels = list(pd_data.columns)
    if not all((label is None) or isinstance(label, str) for label in column_labels):
        raise NotImplementedError("Only string column labels supported")

    if use_index:
        if pd_data.index.nlevels > 1:
            raise NotImplementedError("multi-indices not supported.")
        index_label = pd_data.index.name
        if (index_label is not None) and (not isinstance(index_label, str)):
            raise NotImplementedError("Only string index names supported")

        index_id = guid.generate_guid()
        pd_data = pd_data.reset_index(names=index_id)
        keys_expr = core.ArrayValue.mem_expr_from_pandas(pd_data, session)
        return Block(
            keys_expr,
            column_labels=column_labels,
            index_columns=[index_id],
            index_labels=[index_label],
        )
    else:
        keys_expr = core.ArrayValue.mem_expr_from_pandas(pd_data, session)
        # Constructor will create default range index
        return Block(keys_expr, column_labels=column_labels)


def _align_block_to_schema(
    block: Block, schema: dict[Label, bigframes.dtypes.Dtype]
) -> Block:
    """For a given schema, remap block to schema by reordering columns and inserting nulls."""
    col_ids: typing.Tuple[str, ...] = ()
    for label, dtype in schema.items():
        # TODO: Support casting to lcd type - requires mixed type support
        matching_ids: typing.Sequence[str] = block.label_to_col_id.get(label, ())
        if len(matching_ids) > 0:
            col_id = matching_ids[-1]
            col_ids = (*col_ids, col_id)
        else:
            block, null_column = block.create_constant(None, dtype=dtype)
            col_ids = (*col_ids, null_column)
    return block.select_columns(col_ids).with_column_labels(
        [item for item in schema.keys()]
    )


def _align_schema(
    blocks: typing.Iterable[Block], how: typing.Literal["inner", "outer"]
) -> typing.Dict[Label, bigframes.dtypes.Dtype]:
    schemas = [_get_block_schema(block) for block in blocks]
    reduction = _combine_schema_inner if how == "inner" else _combine_schema_outer
    return functools.reduce(reduction, schemas)


def _align_indices(blocks: typing.Sequence[Block]) -> typing.Sequence[Label]:
    """Validates that the blocks have compatible indices and returns the resulting label names."""
    names = blocks[0].index.names
    types = blocks[0].index.dtypes
    for block in blocks[1:]:
        if len(names) != block.index.nlevels:
            raise NotImplementedError(
                "Cannot combine indices with different number of levels. Use 'ignore_index'=True."
            )
        if block.index.dtypes != types:
            raise NotImplementedError(
                "Cannot combine different index dtypes. Use 'ignore_index'=True."
            )
        names = [
            lname if lname == rname else None
            for lname, rname in zip(names, block.index.names)
        ]
    return names


def _combine_schema_inner(
    left: typing.Dict[Label, bigframes.dtypes.Dtype],
    right: typing.Dict[Label, bigframes.dtypes.Dtype],
) -> typing.Dict[Label, bigframes.dtypes.Dtype]:
    result = dict()
    for label, type in left.items():
        if label in right:
            if type != right[label]:
                raise ValueError(
                    f"Cannot concat rows with label {label} due to mismatched types"
                )
            result[label] = type
    return result


def _combine_schema_outer(
    left: typing.Dict[Label, bigframes.dtypes.Dtype],
    right: typing.Dict[Label, bigframes.dtypes.Dtype],
) -> typing.Dict[Label, bigframes.dtypes.Dtype]:
    result = dict()
    for label, type in left.items():
        if (label in right) and (type != right[label]):
            raise ValueError(
                f"Cannot concat rows with label {label} due to mismatched types"
            )
        result[label] = type
    for label, type in right.items():
        if label not in left:
            result[label] = type
    return result


def _get_block_schema(
    block: Block,
) -> typing.Dict[Label, bigframes.dtypes.Dtype]:
    """Extracts the schema from the block. Where duplicate labels exist, take the last matching column."""
    result = dict()
    for label, dtype in zip(block.column_labels, block.dtypes):
        result[label] = typing.cast(bigframes.dtypes.Dtype, dtype)
    return result


def _get_axis_number(axis: str | int | None) -> typing.Literal[0, 1]:
    if axis in {0, "index", "rows", None}:
        return 0
    elif axis in {1, "columns"}:
        return 1
    else:
        raise ValueError(f"Not a valid axis: {axis}")
