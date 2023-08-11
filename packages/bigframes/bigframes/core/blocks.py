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
import random
import typing
from typing import Iterable, List, Optional, Sequence, Tuple
import warnings

import geopandas as gpd  # type: ignore
import google.cloud.bigquery as bigquery
import ibis.expr.schema as ibis_schema
import ibis.expr.types as ibis_types
import numpy
import pandas as pd
import pyarrow as pa  # type: ignore

import bigframes.constants as constants
import bigframes.core as core
import bigframes.core.guid as guid
import bigframes.core.indexes as indexes
import bigframes.core.ordering as ordering
import bigframes.core.utils
import bigframes.dtypes
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops

# Type constraint for wherever column labels are used
Label = typing.Optional[str]

# Bytes to Megabyte Conversion
_BYTES_TO_KILOBYTES = 1024
_BYTES_TO_MEGABYTES = _BYTES_TO_KILOBYTES * 1024

# All sampling method
_HEAD = "head"
_UNIFORM = "uniform"
_SAMPLING_METHODS = (_HEAD, _UNIFORM)


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
        # col_id -> [stat_name -> scalar]
        # TODO: Preserve cache under safe transforms (eg. drop column, reorder)
        self._stats_cache: dict[str, dict[str, typing.Any]] = {
            col_id: {} for col_id in self.value_columns
        }

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
        self,
        col_ids: typing.Sequence[str],
        drop: bool = True,
        append: bool = False,
        index_labels: typing.Sequence[Label] = (),
    ) -> Block:
        """Set the index of the block to

        Arguments:
            ids: columns to be converted to index columns
            drop: whether to drop the new index columns as value columns
            append: whether to discard the existing index or add on to it
            index_labels: new index labels

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

        if index_labels:
            new_index_labels = list(index_labels)

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

    def to_pandas(
        self,
        value_keys: Optional[Iterable[str]] = None,
        max_results: Optional[int] = None,
        max_download_size: Optional[int] = None,
        sampling_method: Optional[str] = None,
        random_state: Optional[int] = None,
    ) -> Tuple[pd.DataFrame, bigquery.QueryJob]:
        """Run query and download results as a pandas DataFrame."""
        if max_download_size is None:
            max_download_size = bigframes.options.sampling.max_download_size
        if sampling_method is None:
            sampling_method = (
                bigframes.options.sampling.sampling_method
                if bigframes.options.sampling.sampling_method is not None
                else _UNIFORM
            )
        if random_state is None:
            random_state = bigframes.options.sampling.random_state

        sampling_method = sampling_method.lower()
        if sampling_method not in _SAMPLING_METHODS:
            raise NotImplementedError(
                f"The downsampling method {sampling_method} is not implemented, "
                f"please choose from {','.join(_SAMPLING_METHODS)}."
            )

        df, _, query_job = self._compute_and_count(
            value_keys=value_keys,
            max_results=max_results,
            max_download_size=max_download_size,
            sampling_method=sampling_method,
            random_state=random_state,
        )
        return df, query_job

    def _compute_and_count(
        self,
        value_keys: Optional[Iterable[str]] = None,
        max_results: Optional[int] = None,
        max_download_size: Optional[int] = None,
        sampling_method: Optional[str] = None,
        random_state: Optional[int] = None,
    ) -> Tuple[pd.DataFrame, int, bigquery.QueryJob]:
        """Run query and download results as a pandas DataFrame. Return the total number of results as well."""
        # TODO(swast): Allow for dry run and timeout.
        expr = self._apply_value_keys_to_expr(value_keys=value_keys)

        results_iterator, query_job = expr.start_query(
            max_results=max_results, expose_extra_columns=True
        )

        table_size = expr._get_table_size(query_job.destination) / _BYTES_TO_MEGABYTES
        fraction = (
            max_download_size / table_size
            if (max_download_size is not None) and (table_size != 0)
            else 2
        )

        if fraction < 1:
            if not bigframes.options.sampling.enable_downsampling:
                raise RuntimeError(
                    f"The data size ({table_size:.2f} MB) exceeds the maximum download limit of "
                    f"{max_download_size} MB. You can:\n\t* Enable downsampling in global options:\n"
                    "\t\t`bigframes.options.sampling.enable_downsampling = True`\n"
                    "\t* Update the global `max_download_size` option. Please make sure "
                    "there is enough memory available:\n"
                    "\t\t`bigframes.options.sampling.max_download_size = desired_size`"
                    " # Setting it to None will download all the data\n"
                    f"{constants.FEEDBACK_LINK}"
                )

            warnings.warn(
                f"The data size ({table_size:.2f} MB) exceeds the maximum download limit of"
                f"({max_download_size} MB). It will be downsampled to {max_download_size} MB for download."
                "\nPlease refer to the documentation for configuring the downloading limit.",
                UserWarning,
            )
            if sampling_method == _HEAD:
                total_rows = int(results_iterator.total_rows * fraction)
                results_iterator.max_results = total_rows
                df = self._to_dataframe(results_iterator, expr.to_ibis_expr().schema())

                if self.index_columns:
                    df.set_index(list(self.index_columns), inplace=True)
                    df.index.names = self.index.names  # type: ignore

                df.drop(
                    [col for col in df.columns if col not in self.value_columns],
                    axis=1,
                    inplace=True,
                )
            elif (sampling_method == _UNIFORM) and (random_state is None):
                filtered_expr = self.expr._uniform_sampling(fraction)
                block = Block(
                    filtered_expr,
                    index_columns=self.index_columns,
                    column_labels=self.column_labels,
                    index_labels=self.index.names,
                )
                df, total_rows, _ = block._compute_and_count(max_download_size=None)
            elif sampling_method == _UNIFORM:
                block = self._split(
                    fracs=(max_download_size / table_size,),
                    random_state=random_state,
                    preserve_order=True,
                )[0]
                df, total_rows, _ = block._compute_and_count(max_download_size=None)
            else:
                # This part should never be called, just in case.
                raise NotImplementedError(
                    f"The downsampling method {sampling_method} is not implemented, "
                    f"please choose from {','.join(_SAMPLING_METHODS)}."
                )
        else:
            total_rows = results_iterator.total_rows
            df = self._to_dataframe(results_iterator, expr.to_ibis_expr().schema())

            if self.index_columns:
                df.set_index(list(self.index_columns), inplace=True)
                df.index.names = self.index.names  # type: ignore

            df.drop(
                [col for col in df.columns if col not in self.value_columns],
                axis=1,
                inplace=True,
            )

        return df, total_rows, query_job

    def _split(
        self,
        ns: Iterable[int] = (),
        fracs: Iterable[float] = (),
        *,
        random_state: Optional[int] = None,
        preserve_order: Optional[bool] = False,
    ) -> List[Block]:
        """Internal function to support splitting Block to multiple parts along index axis.

        At most one of ns and fracs can be passed in. If neither, default to ns = (1,).
        Return a list of sampled Blocks.
        """
        block = self
        if ns and fracs:
            raise ValueError("Only one of 'ns' or 'fracs' parameter must be specified.")

        if not ns and not fracs:
            ns = (1,)

        if ns:
            sample_sizes = ns
        else:
            total_rows = block.shape[0]
            # Round to nearest integer. "round half to even" rule applies.
            # At least to be 1.
            sample_sizes = [round(frac * total_rows) or 1 for frac in fracs]

        if random_state is None:
            random_state = random.randint(-(2**63), 2**63 - 1)

        # Create a new column with random_state value.
        block, random_state_col = block.create_constant(str(random_state))

        # Create an ordering col and convert to string
        block, ordering_col = block.promote_offsets()
        block, string_ordering_col = block.apply_unary_op(
            ordering_col, ops.AsTypeOp("string[pyarrow]")
        )

        # Apply hash method to sum col and order by it.
        block, string_sum_col = block.apply_binary_op(
            string_ordering_col, random_state_col, ops.concat_op
        )
        block, hash_string_sum_col = block.apply_unary_op(string_sum_col, ops.hash_op)
        block = block.order_by([ordering.OrderingColumnReference(hash_string_sum_col)])

        intervals = []
        cur = 0

        for sample_size in sample_sizes:
            intervals.append((cur, cur + sample_size))
            cur += sample_size

        sliced_blocks = [
            typing.cast(Block, block.slice(start=lower, stop=upper))
            for lower, upper in intervals
        ]
        if preserve_order:
            sliced_blocks = [
                sliced_block.order_by([ordering.OrderingColumnReference(ordering_col)])
                for sliced_block in sliced_blocks
            ]

        drop_cols = [
            random_state_col,
            ordering_col,
            string_ordering_col,
            string_sum_col,
            hash_string_sum_col,
        ]
        return [sliced_block.drop_columns(drop_cols) for sliced_block in sliced_blocks]

    def _compute_dry_run(
        self, value_keys: Optional[Iterable[str]] = None
    ) -> bigquery.QueryJob:
        expr = self._apply_value_keys_to_expr(value_keys=value_keys)
        job_config = bigquery.QueryJobConfig(dry_run=True)
        _, query_job = expr.start_query(job_config=job_config)
        return query_job

    def _apply_value_keys_to_expr(self, value_keys: Optional[Iterable[str]] = None):
        expr = self._expr
        if value_keys is not None:
            expr = expr.select_columns(itertools.chain(self._index_columns, value_keys))
        return expr

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

    def filter(self, column_name: str, keep_null: bool = False):
        condition = typing.cast(
            ibis_types.BooleanValue, self._expr.get_column(column_name)
        )
        if keep_null:
            condition = typing.cast(
                ibis_types.BooleanValue,
                condition.fillna(
                    typing.cast(ibis_types.BooleanScalar, ibis_types.literal(True))
                ),
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
        ).unpivot_single_row(
            row_labels=self.column_labels,
            index_col_id="index",
            unpivot_columns=[(value_col_id, self.value_columns)],
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
        by_column_ids: typing.Sequence[str] = (),
        aggregations: typing.Sequence[typing.Tuple[str, agg_ops.AggregateOp]] = (),
        *,
        as_index: bool = True,
        dropna: bool = True,
    ) -> typing.Tuple[Block, typing.Sequence[str]]:
        """
        Apply aggregations to the block. Callers responsible for setting index column(s) after.
        Arguments:
            by_column_id: column id of the aggregation key, this is preserved through the transform and used as index.
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
            names: typing.List[Label] = []
            for by_col_id in by_column_ids:
                if by_col_id in self.value_columns:
                    names.append(self.col_id_to_label[by_col_id])
                else:
                    names.append(self.col_id_to_index_name[by_col_id])
            return (
                Block(
                    result_expr,
                    index_columns=by_column_ids,
                    column_labels=aggregate_labels,
                    index_labels=names,
                ),
                output_col_ids,
            )
        else:  # as_index = False
            # If as_index=False, drop grouping levels, but keep grouping value columns
            by_value_columns = [
                col for col in by_column_ids if col in self.value_columns
            ]
            by_column_labels = self._get_labels_for_columns(by_value_columns)
            labels = (*by_column_labels, *aggregate_labels)
            result_expr_pruned = result_expr.select_columns(
                [*by_value_columns, *output_col_ids]
            )
            return Block(result_expr_pruned, column_labels=labels), output_col_ids

    def get_stat(self, column_id: str, stat: agg_ops.AggregateOp):
        """Gets aggregates immediately, and caches it"""
        if stat.name in self._stats_cache[column_id]:
            return self._stats_cache[column_id][stat.name]

        # TODO: Convert nonstandard stats into standard stats where possible (popvar, etc.)
        # if getting a standard stat, just go get the rest of them
        standard_stats = self._standard_stats(column_id)
        stats_to_fetch = standard_stats if stat in standard_stats else [stat]

        aggregations = [(column_id, stat, stat.name) for stat in stats_to_fetch]
        expr = self.expr.aggregate(aggregations)
        block = Block(expr, column_labels=[s.name for s in stats_to_fetch])
        df, _ = block.to_pandas()

        # Carefully extract stats such that they aren't coerced to a common type
        stats_map = {stat_name: df.loc[0, stat_name] for stat_name in df.columns}
        self._stats_cache[column_id].update(stats_map)
        return stats_map[stat.name]

    def summarize(
        self,
        column_ids: typing.Sequence[str],
        stats: typing.Sequence[agg_ops.AggregateOp],
    ):
        """Get a list of stats as a deferred block object."""
        label_col_id = guid.generate_guid()
        labels = [stat.name for stat in stats]
        aggregations = [
            (col_id, stat, f"{col_id}-{stat.name}")
            for stat in stats
            for col_id in column_ids
        ]
        columns = [
            (col_id, [f"{col_id}-{stat.name}" for stat in stats])
            for col_id in column_ids
        ]
        expr = self.expr.aggregate(aggregations).unpivot_single_row(
            labels,
            unpivot_columns=columns,
            index_col_id=label_col_id,
        )
        labels = self._get_labels_for_columns(column_ids)
        return Block(expr, column_labels=labels, index_columns=[label_col_id])

    def _standard_stats(self, column_id) -> typing.Sequence[agg_ops.AggregateOp]:
        """
        Gets a standard set of stats to preemptively fetch for a column if
        any other stat is fetched.
        Helps prevent repeat scanning of the same column to fetch statistics.
        Standard stats should be:
            - commonly used
            - efficiently computable.
        """
        # TODO: annotate aggregations themself with this information
        dtype = self.expr.get_column_type(column_id)
        stats: list[agg_ops.AggregateOp] = [agg_ops.count_op]
        if dtype not in bigframes.dtypes.UNORDERED_DTYPES:
            stats += [agg_ops.min_op, agg_ops.max_op]
        if dtype in bigframes.dtypes.NUMERIC_BIGFRAMES_TYPES:
            # Notable exclusions:
            # prod op tends to cause overflows
            # Also, var_op is redundant as can be derived from std
            stats += [
                agg_ops.std_op,
                agg_ops.mean_op,
                agg_ops.var_op,
                agg_ops.sum_op,
            ]

        return stats

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

    def retrieve_repr_request_results(
        self, max_results: int
    ) -> Tuple[pd.DataFrame, int, bigquery.QueryJob]:
        """
        Retrieves a pandas dataframe containing only max_results many rows for use
        with printing methods.

        Returns a tuple of the dataframe and the overall number of rows of the query.
        """
        # TODO(swast): Select a subset of columns if max_columns is less than the
        # number of columns in the schema.
        count = self.shape[0]
        if count > max_results:
            head_block = self.slice(0, max_results)
            computed_df, query_job = head_block.to_pandas(max_results=max_results)
        else:
            head_block = self
            computed_df, query_job = head_block.to_pandas()
        formatted_df = computed_df.set_axis(self.column_labels, axis=1)
        # we reset the axis and substitute the bf index name for the default
        formatted_df.index.name = self.index.name
        return formatted_df, count, query_job

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
        axis_number = bigframes.core.utils.get_axis_number(axis)
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
        axis_number = bigframes.core.utils.get_axis_number(axis)
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

    def _force_reproject(self) -> Block:
        """Forces a reprojection of the underlying tables expression. Used to force predicate/order application before subsequent operations."""
        return Block(
            self._expr._reproject_to_table(),
            index_columns=self.index_columns,
            column_labels=self.column_labels,
            index_labels=self.index.names,
        )


def block_from_local(data, session=None, use_index=True) -> Block:
    # TODO(tbergeron): Handle duplicate column labels
    pd_data = pd.DataFrame(data)

    column_labels = list(pd_data.columns)
    if not all((label is None) or isinstance(label, str) for label in column_labels):
        raise NotImplementedError(
            f"Only string column labels supported. {constants.FEEDBACK_LINK}"
        )

    if use_index:
        if pd_data.index.nlevels > 1:
            raise NotImplementedError(
                f"multi-indices not supported. {constants.FEEDBACK_LINK}"
            )
        index_label = pd_data.index.name
        if (index_label is not None) and (not isinstance(index_label, str)):
            raise NotImplementedError(
                f"Only string index names supported. {constants.FEEDBACK_LINK}"
            )

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
                f"Cannot combine indices with different number of levels. Use 'ignore_index'=True. {constants.FEEDBACK_LINK}"
            )
        if block.index.dtypes != types:
            raise NotImplementedError(
                f"Cannot combine different index dtypes. Use 'ignore_index'=True. {constants.FEEDBACK_LINK}"
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
                    f"Cannot concat rows with label {label} due to mismatched types. {constants.FEEDBACK_LINK}"
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
                f"Cannot concat rows with label {label} due to mismatched types. {constants.FEEDBACK_LINK}"
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
