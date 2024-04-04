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

import dataclasses
import functools
import itertools
import random
import typing
from typing import Iterable, List, Literal, Mapping, Optional, Sequence, Tuple
import warnings

import google.cloud.bigquery as bigquery
import pandas as pd
import pyarrow as pa

import bigframes._config.sampling_options as sampling_options
import bigframes.constants as constants
import bigframes.core as core
import bigframes.core.expression as ex
import bigframes.core.expression as scalars
import bigframes.core.guid as guid
import bigframes.core.join_def as join_defs
import bigframes.core.ordering as ordering
import bigframes.core.tree_properties as tree_properties
import bigframes.core.utils
import bigframes.core.utils as utils
import bigframes.dtypes
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops
import bigframes.session._io.pandas

# Type constraint for wherever column labels are used
Label = typing.Hashable

# Bytes to Megabyte Conversion
_BYTES_TO_KILOBYTES = 1024
_BYTES_TO_MEGABYTES = _BYTES_TO_KILOBYTES * 1024

# This is the max limit of physical columns in BQ
# May choose to set smaller limit for number of block columns to allow overhead for ordering, etc.
_BQ_MAX_COLUMNS = 10000

# All sampling method
_HEAD = "head"
_UNIFORM = "uniform"
_SAMPLING_METHODS = (_HEAD, _UNIFORM)

# Monotonic Cache Names
_MONOTONIC_INCREASING = "monotonic_increasing"
_MONOTONIC_DECREASING = "monotonic_decreasing"


LevelType = typing.Hashable
LevelsType = typing.Union[LevelType, typing.Sequence[LevelType]]


class BlockHolder(typing.Protocol):
    """Interface for mutable objects with state represented by a block value object."""

    def _set_block(self, block: Block):
        """Set the underlying block value of the object"""

    def _get_block(self) -> Block:
        """Get the underlying block value of the object"""


@dataclasses.dataclass()
class MaterializationOptions:
    downsampling: sampling_options.SamplingOptions = dataclasses.field(
        default_factory=sampling_options.SamplingOptions
    )
    ordered: bool = True


class Block:
    """A immutable 2D data structure."""

    def __init__(
        self,
        expr: core.ArrayValue,
        index_columns: Iterable[str],
        column_labels: typing.Union[pd.Index, typing.Iterable[Label]],
        index_labels: typing.Union[pd.Index, typing.Iterable[Label], None] = None,
    ):
        """Construct a block object, will create default index if no index columns specified."""
        index_columns = list(index_columns)
        if index_labels is not None:
            index_labels = list(index_labels)
            if len(index_labels) != len(index_columns):
                raise ValueError(
                    f"'index_columns' (size {len(index_columns)}) and 'index_labels' (size {len(index_labels)}) must have equal length"
                )
        if len(index_columns) == 0:
            new_index_col_id = guid.generate_guid()
            expr = expr.promote_offsets(new_index_col_id)
            index_columns = [new_index_col_id]
        self._index_columns = tuple(index_columns)
        # Index labels don't need complicated hierarchical access so can store as tuple
        self._index_labels = (
            tuple(index_labels)
            if index_labels
            else tuple([None for _ in index_columns])
        )
        self._expr = self._normalize_expression(expr, self._index_columns)
        # Use pandas index to more easily replicate column indexing, especially for hierarchical column index
        self._column_labels = (
            column_labels.copy()
            if isinstance(column_labels, pd.Index)
            else pd.Index(column_labels)
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
        # TODO(kemppeterson) Add a cache for corr to parallel the single-column stats.

        self._stats_cache[" ".join(self.index_columns)] = {}

    @classmethod
    def from_local(cls, data: pd.DataFrame, session: bigframes.Session) -> Block:
        # Assumes caller has already converted datatypes to bigframes ones.
        pd_data = data
        column_labels = pd_data.columns
        index_labels = list(pd_data.index.names)

        # unique internal ids
        column_ids = [f"column_{i}" for i in range(len(pd_data.columns))]
        index_ids = [f"level_{level}" for level in range(pd_data.index.nlevels)]

        pd_data = pd_data.set_axis(column_ids, axis=1)
        pd_data = pd_data.reset_index(names=index_ids)
        as_pyarrow = pa.Table.from_pandas(pd_data, preserve_index=False)
        array_value = core.ArrayValue.from_pyarrow(as_pyarrow, session=session)
        return cls(
            array_value,
            column_labels=column_labels,
            index_columns=index_ids,
            index_labels=index_labels,
        )

    @property
    def index(self) -> BlockIndexProperties:
        """Row identities for values in the Block."""
        return BlockIndexProperties(self)

    @functools.cached_property
    def shape(self) -> typing.Tuple[int, int]:
        """Returns dimensions as (length, width) tuple."""
        row_count_expr = self.expr.row_count()

        # Support in-memory engines for hermetic unit tests.
        if self.expr.node.session is None:
            try:
                row_count = row_count_expr._try_evaluate_local().squeeze()
                return (row_count, len(self.value_columns))
            except Exception:
                pass

        iter, _ = self.session._execute(row_count_expr, sorted=False)
        row_count = next(iter)[0]
        return (row_count, len(self.value_columns))

    @property
    def index_columns(self) -> Sequence[str]:
        """Column(s) to use as row labels."""
        return self._index_columns

    @property
    def value_columns(self) -> Sequence[str]:
        """All value columns, mutually exclusive with index columns."""
        return [
            column
            for column in self._expr.column_ids
            if column not in self.index_columns
        ]

    @property
    def column_labels(self) -> pd.Index:
        return self._column_labels

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
    def session(self) -> core.Session:
        return self._expr.session

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

    def cols_matching_label(self, partial_label: Label) -> typing.Sequence[str]:
        """
        Unlike label_to_col_id, this works with partial labels for multi-index.

        Only some methods, like __getitem__ can use a partial key to get columns
        from a dataframe. These methods should use cols_matching_label, while
        methods that require exact label matches should use label_to_col_id.
        """
        # TODO(tbergeron): Refactor so that all label lookups use this method
        if partial_label not in self.column_labels:
            return []
        loc = self.column_labels.get_loc(partial_label)
        if isinstance(loc, int):
            return [self.value_columns[loc]]
        if isinstance(loc, slice):
            return self.value_columns[loc]
        return [col for col, is_present in zip(self.value_columns, loc) if is_present]

    def order_by(
        self,
        by: typing.Sequence[ordering.OrderingExpression],
    ) -> Block:
        return Block(
            self._expr.order_by(by),
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
        new_index_col_id = guid.generate_guid()
        expr = self._expr.promote_offsets(new_index_col_id)
        if drop:
            # Even though the index might be part of the ordering, keep that
            # ordering expression as reset_index shouldn't change the row
            # order.
            expr = expr.drop_columns(self.index_columns)
            return Block(
                expr,
                index_columns=[new_index_col_id],
                column_labels=self.column_labels,
                index_labels=[None],
            )
        else:
            # Add index names to column index
            index_labels = self.index.names
            column_labels_modified = self.column_labels
            for level, label in enumerate(index_labels):
                if label is None:
                    if "index" not in self.column_labels and len(index_labels) <= 1:
                        label = "index"
                    else:
                        label = f"level_{level}"

                if label in self.column_labels:
                    raise ValueError(f"cannot insert {label}, already exists")
                if isinstance(self.column_labels, pd.MultiIndex):
                    nlevels = self.column_labels.nlevels
                    label = tuple(label if i == 0 else "" for i in range(nlevels))
                # Create index copy with label inserted
                # See: https://pandas.pydata.org/docs/reference/api/pandas.Index.insert.html
                column_labels_modified = column_labels_modified.insert(level, label)

            return Block(
                expr,
                index_columns=[new_index_col_id],
                column_labels=column_labels_modified,
                index_labels=[None],
            )

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

    def _to_dataframe(self, result) -> pd.DataFrame:
        """Convert BigQuery data to pandas DataFrame with specific dtypes."""
        dtypes = dict(zip(self.index_columns, self.index.dtypes))
        dtypes.update(zip(self.value_columns, self.dtypes))
        return self.session._rows_to_dataframe(result, dtypes)

    def to_pandas(
        self,
        max_download_size: Optional[int] = None,
        sampling_method: Optional[str] = None,
        random_state: Optional[int] = None,
        *,
        ordered: bool = True,
    ) -> Tuple[pd.DataFrame, bigquery.QueryJob]:
        """Run query and download results as a pandas DataFrame."""
        if (sampling_method is not None) and (sampling_method not in _SAMPLING_METHODS):
            raise NotImplementedError(
                f"The downsampling method {sampling_method} is not implemented, "
                f"please choose from {','.join(_SAMPLING_METHODS)}."
            )

        sampling = bigframes.options.sampling.with_max_download_size(max_download_size)
        if sampling_method is not None:
            sampling = sampling.with_method(sampling_method).with_random_state(  # type: ignore
                random_state
            )
        else:
            sampling = sampling.with_disabled()

        df, query_job = self._materialize_local(
            materialize_options=MaterializationOptions(
                downsampling=sampling, ordered=ordered
            )
        )
        df.set_axis(self.column_labels, axis=1, copy=False)
        return df, query_job

    def try_peek(
        self, n: int = 20, force: bool = False
    ) -> typing.Optional[pd.DataFrame]:
        if force or tree_properties.peekable(self.expr.node):
            iterator, _ = self.session._peek(self.expr, n)
            df = self._to_dataframe(iterator)
            self._copy_index_to_pandas(df)
            return df
        else:
            return None

    def to_pandas_batches(self):
        """Download results one message at a time."""
        dtypes = dict(zip(self.index_columns, self.index.dtypes))
        dtypes.update(zip(self.value_columns, self.dtypes))
        results_iterator, _ = self.session._execute(self.expr, sorted=True)
        for arrow_table in results_iterator.to_arrow_iterable(
            bqstorage_client=self.session.bqstoragereadclient
        ):
            df = bigframes.session._io.pandas.arrow_to_pandas(arrow_table, dtypes)
            self._copy_index_to_pandas(df)
            yield df

    def _copy_index_to_pandas(self, df: pd.DataFrame):
        """Set the index on pandas DataFrame to match this block.

        Warning: This method modifies ``df`` inplace.
        """
        if self.index_columns:
            df.set_index(list(self.index_columns), inplace=True)
            # Pandas names is annotated as list[str] rather than the more
            # general Sequence[Label] that BigQuery DataFrames has.
            # See: https://github.com/pandas-dev/pandas-stubs/issues/804
            df.index.names = self.index.names  # type: ignore
        df.columns = self.column_labels

    def _materialize_local(
        self, materialize_options: MaterializationOptions = MaterializationOptions()
    ) -> Tuple[pd.DataFrame, bigquery.QueryJob]:
        """Run query and download results as a pandas DataFrame. Return the total number of results as well."""
        # TODO(swast): Allow for dry run and timeout.
        results_iterator, query_job = self.session._execute(
            self.expr, sorted=materialize_options.ordered
        )
        table_size = (
            self.session._get_table_size(query_job.destination) / _BYTES_TO_MEGABYTES
        )
        sample_config = materialize_options.downsampling
        max_download_size = sample_config.max_download_size
        fraction = (
            max_download_size / table_size
            if (max_download_size is not None) and (table_size != 0)
            else 2
        )

        # TODO: Maybe materialize before downsampling
        # Some downsampling methods
        if fraction < 1:
            if not sample_config.enable_downsampling:
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
            total_rows = results_iterator.total_rows
            # Remove downsampling config from subsequent invocations, as otherwise could result in many
            # iterations if downsampling undershoots
            return self._downsample(
                total_rows=total_rows,
                sampling_method=sample_config.sampling_method,
                fraction=fraction,
                random_state=sample_config.random_state,
            )._materialize_local(
                MaterializationOptions(ordered=materialize_options.ordered)
            )
        else:
            total_rows = results_iterator.total_rows
            df = self._to_dataframe(results_iterator)
            self._copy_index_to_pandas(df)

        return df, query_job

    def _downsample(
        self, total_rows: int, sampling_method: str, fraction: float, random_state
    ) -> Block:
        # either selecting fraction or number of rows
        if sampling_method == _HEAD:
            filtered_block = self.slice(stop=int(total_rows * fraction))
            return filtered_block
        elif (sampling_method == _UNIFORM) and (random_state is None):
            filtered_expr = self.expr._uniform_sampling(fraction)
            block = Block(
                filtered_expr,
                index_columns=self.index_columns,
                column_labels=self.column_labels,
                index_labels=self.index.names,
            )
            return block
        elif sampling_method == _UNIFORM:
            block = self._split(
                fracs=(fraction,),
                random_state=random_state,
                sort=False,
            )[0]
            return block
        else:
            # This part should never be called, just in case.
            raise NotImplementedError(
                f"The downsampling method {sampling_method} is not implemented, "
                f"please choose from {','.join(_SAMPLING_METHODS)}."
            )

    def _split(
        self,
        ns: Iterable[int] = (),
        fracs: Iterable[float] = (),
        *,
        random_state: Optional[int] = None,
        sort: Optional[bool | Literal["random"]] = "random",
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
            ordering_col, ops.AsTypeOp(to_type="string[pyarrow]")
        )

        # Apply hash method to sum col and order by it.
        block, string_sum_col = block.apply_binary_op(
            string_ordering_col, random_state_col, ops.strconcat_op
        )
        block, hash_string_sum_col = block.apply_unary_op(string_sum_col, ops.hash_op)
        block = block.order_by(
            [ordering.OrderingExpression(ex.free_var(hash_string_sum_col))]
        )

        intervals = []
        cur = 0

        for sample_size in sample_sizes:
            intervals.append((cur, cur + sample_size))
            cur += sample_size

        sliced_blocks = [
            typing.cast(Block, block.slice(start=lower, stop=upper))
            for lower, upper in intervals
        ]

        if sort is True:
            sliced_blocks = [
                sliced_block.order_by(
                    [
                        ordering.OrderingExpression(ex.free_var(idx_col))
                        for idx_col in sliced_block.index_columns
                    ]
                )
                for sliced_block in sliced_blocks
            ]
        elif sort is False:
            sliced_blocks = [
                sliced_block.order_by(
                    [ordering.OrderingExpression(ex.free_var(ordering_col))]
                )
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
        _, query_job = self.session._execute(expr, job_config=job_config, dry_run=True)
        return query_job

    def _apply_value_keys_to_expr(self, value_keys: Optional[Iterable[str]] = None):
        expr = self._expr
        if value_keys is not None:
            expr = expr.select_columns(itertools.chain(self._index_columns, value_keys))
        return expr

    def with_column_labels(
        self,
        value: typing.Union[pd.Index, typing.Iterable[Label]],
    ) -> Block:
        label_list = value.copy() if isinstance(value, pd.Index) else pd.Index(value)
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
                f"The index labels size `{len(value)} ` should equal to the index "
                + f"columns size: {len(self.index_columns)}."
            )
        return Block(
            self._expr,
            index_columns=self.index_columns,
            column_labels=self.column_labels,
            index_labels=tuple(value),
        )

    def project_expr(
        self, expr: ex.Expression, label: Label = None
    ) -> typing.Tuple[Block, str]:
        """
        Apply a scalar expression to the block. Creates a new column to store the result.
        """
        # TODO(tbergeron): handle labels safely so callers don't need to
        result_id = guid.generate_guid()
        array_val = self._expr.project_to_id(expr, result_id)
        block = Block(
            array_val,
            index_columns=self.index_columns,
            column_labels=self.column_labels.insert(len(self.column_labels), label),
            index_labels=self.index.names,
        )
        return (block, result_id)

    def apply_unary_op(
        self, column: str, op: ops.UnaryOp, result_label: Label = None
    ) -> typing.Tuple[Block, str]:
        """
        Apply a unary op to the block. Creates a new column to store the result.
        """
        expr = op.as_expr(column)
        return self.project_expr(expr, result_label)

    def apply_binary_op(
        self,
        left_column_id: str,
        right_column_id: str,
        op: ops.BinaryOp,
        result_label: Label = None,
    ) -> typing.Tuple[Block, str]:
        expr = op.as_expr(left_column_id, right_column_id)
        return self.project_expr(expr, result_label)

    def apply_ternary_op(
        self,
        col_id_1: str,
        col_id_2: str,
        col_id_3: str,
        op: ops.TernaryOp,
        result_label: Label = None,
    ) -> typing.Tuple[Block, str]:
        expr = op.as_expr(col_id_1, col_id_2, col_id_3)
        return self.project_expr(expr, result_label)

    def multi_apply_window_op(
        self,
        columns: typing.Sequence[str],
        op: agg_ops.WindowOp,
        window_spec: core.WindowSpec,
        *,
        skip_null_groups: bool = False,
        never_skip_nulls: bool = False,
    ) -> typing.Tuple[Block, typing.Sequence[str]]:
        block = self
        result_ids = []
        for i, col_id in enumerate(columns):
            label = self.col_id_to_label[col_id]
            block, result_id = block.apply_window_op(
                col_id,
                op,
                window_spec=window_spec,
                skip_reproject_unsafe=(i + 1) < len(columns),
                result_label=label,
                skip_null_groups=skip_null_groups,
                never_skip_nulls=never_skip_nulls,
            )
            result_ids.append(result_id)
        return block, result_ids

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
        never_skip_nulls: bool = False,
    ) -> typing.Tuple[Block, str]:
        block = self
        if skip_null_groups:
            for key in window_spec.grouping_keys:
                block, not_null_id = block.apply_unary_op(key, ops.notnull_op)
                block = block.filter_by_id(not_null_id).drop_columns([not_null_id])
        result_id = guid.generate_guid()
        expr = block._expr.project_window_op(
            column,
            op,
            window_spec,
            result_id,
            skip_reproject_unsafe=skip_reproject_unsafe,
            never_skip_nulls=never_skip_nulls,
        )
        block = Block(
            expr,
            index_columns=self.index_columns,
            column_labels=self.column_labels.insert(
                len(self.column_labels), result_label
            ),
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
        # Create index copy with label inserted
        # See: https://pandas.pydata.org/docs/reference/api/pandas.Index.insert.html
        labels = self.column_labels.insert(len(self.column_labels), label)
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
        # Create index copy with label inserted
        # See: https://pandas.pydata.org/docs/reference/api/pandas.Index.insert.html
        new_labels = self.column_labels.insert(col_index, new_label).delete(
            col_index + 1
        )
        return self.with_column_labels(new_labels)

    def filter_by_id(self, column_id: str, keep_null: bool = False):
        return Block(
            self._expr.filter_by_id(column_id, keep_null),
            index_columns=self.index_columns,
            column_labels=self.column_labels,
            index_labels=self.index.names,
        )

    def filter(self, predicate: scalars.Expression):
        return Block(
            self._expr.filter(predicate),
            index_columns=self.index_columns,
            column_labels=self.column_labels,
            index_labels=self.index.names,
        )

    def aggregate_all_and_stack(
        self,
        operation: agg_ops.UnaryAggregateOp,
        *,
        axis: int | str = 0,
        value_col_id: str = "values",
        dropna: bool = True,
        dtype: typing.Union[
            bigframes.dtypes.Dtype, typing.Tuple[bigframes.dtypes.Dtype, ...]
        ] = pd.Float64Dtype(),
    ) -> Block:
        axis_n = utils.get_axis_number(axis)
        if axis_n == 0:
            aggregations = [
                (ex.UnaryAggregation(operation, ex.free_var(col_id)), col_id)
                for col_id in self.value_columns
            ]
            index_col_ids = [
                guid.generate_guid() for i in range(self.column_labels.nlevels)
            ]
            result_expr = self.expr.aggregate(aggregations, dropna=dropna).unpivot(
                row_labels=self.column_labels.to_list(),
                index_col_ids=index_col_ids,
                unpivot_columns=tuple([(value_col_id, tuple(self.value_columns))]),
                dtype=dtype,
            )
            return Block(
                result_expr,
                index_columns=index_col_ids,
                column_labels=[None],
                index_labels=self.column_labels.names,
            )
        else:  # axis_n == 1
            # using offsets as identity to group on.
            # TODO: Allow to promote identity/total_order columns instead for better perf
            offset_col = guid.generate_guid()
            expr_with_offsets = self.expr.promote_offsets(offset_col)
            stacked_expr = expr_with_offsets.unpivot(
                row_labels=self.column_labels.to_list(),
                index_col_ids=[guid.generate_guid()],
                unpivot_columns=[(value_col_id, tuple(self.value_columns))],
                passthrough_columns=[*self.index_columns, offset_col],
                dtype=dtype,
            )
            index_aggregations = [
                (ex.UnaryAggregation(agg_ops.AnyValueOp(), ex.free_var(col_id)), col_id)
                for col_id in [*self.index_columns]
            ]
            main_aggregation = (
                ex.UnaryAggregation(operation, ex.free_var(value_col_id)),
                value_col_id,
            )
            result_expr = stacked_expr.aggregate(
                [*index_aggregations, main_aggregation],
                by_column_ids=[offset_col],
                dropna=dropna,
            )
            return Block(
                result_expr.drop_columns([offset_col]),
                self.index_columns,
                column_labels=[None],
                index_labels=self.index.names,
            )

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

    def rename(
        self,
        *,
        columns: typing.Mapping[Label, Label] | typing.Callable[[typing.Any], Label],
    ):
        if isinstance(columns, typing.Mapping):

            def remap_f(x):
                return columns.get(x, x)

        else:
            remap_f = columns
        if isinstance(self.column_labels, pd.MultiIndex):
            col_labels: list[Label] = []
            for col_label in self.column_labels:
                # Mapper applies to each level separately
                modified_label = tuple(remap_f(part) for part in col_label)
                col_labels.append(modified_label)
        else:
            col_labels = []
            for col_label in self.column_labels:
                col_labels.append(remap_f(col_label))
        return self.with_column_labels(col_labels)

    def aggregate(
        self,
        by_column_ids: typing.Sequence[str] = (),
        aggregations: typing.Sequence[typing.Tuple[str, agg_ops.UnaryAggregateOp]] = (),
        *,
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
            (
                ex.UnaryAggregation(operation, ex.free_var(input_id)),
                guid.generate_guid(),
            )
            for input_id, operation in aggregations
        ]
        output_col_ids = [agg_spec[1] for agg_spec in agg_specs]
        result_expr = self.expr.aggregate(agg_specs, by_column_ids, dropna=dropna)

        aggregate_labels = self._get_labels_for_columns(
            [agg[0] for agg in aggregations]
        )
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

    def get_stat(self, column_id: str, stat: agg_ops.UnaryAggregateOp):
        """Gets aggregates immediately, and caches it"""
        if stat.name in self._stats_cache[column_id]:
            return self._stats_cache[column_id][stat.name]

        # TODO: Convert nonstandard stats into standard stats where possible (popvar, etc.)
        # if getting a standard stat, just go get the rest of them
        standard_stats = self._standard_stats(column_id)
        stats_to_fetch = standard_stats if stat in standard_stats else [stat]

        aggregations = [
            (ex.UnaryAggregation(stat, ex.free_var(column_id)), stat.name)
            for stat in stats_to_fetch
        ]
        expr = self.expr.aggregate(aggregations)
        offset_index_id = guid.generate_guid()
        expr = expr.promote_offsets(offset_index_id)
        block = Block(
            expr,
            index_columns=[offset_index_id],
            column_labels=[s.name for s in stats_to_fetch],
        )
        df, _ = block.to_pandas()

        # Carefully extract stats such that they aren't coerced to a common type
        stats_map = {stat_name: df.loc[0, stat_name] for stat_name in df.columns}
        self._stats_cache[column_id].update(stats_map)
        return stats_map[stat.name]

    def get_binary_stat(
        self, column_id_left: str, column_id_right: str, stat: agg_ops.BinaryAggregateOp
    ):
        # TODO(kemppeterson): Clean up the column names for DataFrames.corr support
        # TODO(kemppeterson): Add a cache here.
        aggregations = [
            (
                ex.BinaryAggregation(
                    stat, ex.free_var(column_id_left), ex.free_var(column_id_right)
                ),
                f"{stat.name}_{column_id_left}{column_id_right}",
            )
        ]
        expr = self.expr.aggregate(aggregations)
        offset_index_id = guid.generate_guid()
        expr = expr.promote_offsets(offset_index_id)
        block = Block(
            expr,
            index_columns=[offset_index_id],
            column_labels=[a[1] for a in aggregations],
        )
        df, _ = block.to_pandas()
        return df.loc[0, f"{stat.name}_{column_id_left}{column_id_right}"]

    def summarize(
        self,
        column_ids: typing.Sequence[str],
        stats: typing.Sequence[agg_ops.UnaryAggregateOp],
    ):
        """Get a list of stats as a deferred block object."""
        label_col_id = guid.generate_guid()
        labels = [stat.name for stat in stats]
        aggregations = [
            (ex.UnaryAggregation(stat, ex.free_var(col_id)), f"{col_id}-{stat.name}")
            for stat in stats
            for col_id in column_ids
        ]
        columns = [
            (col_id, tuple(f"{col_id}-{stat.name}" for stat in stats))
            for col_id in column_ids
        ]
        expr = self.expr.aggregate(aggregations).unpivot(
            labels,
            unpivot_columns=tuple(columns),
            index_col_ids=tuple([label_col_id]),
        )
        return Block(
            expr,
            column_labels=self._get_labels_for_columns(column_ids),
            index_columns=[label_col_id],
        )

    def calculate_pairwise_metric(self, op=agg_ops.CorrOp()):
        """
        Returns a block object to compute pairwise metrics among all value columns in this block.

        The metric to be computed is specified by the `op` parameter, which can be either a
        correlation operation (default) or a covariance operation.
        """
        if len(self.value_columns) > 30:
            raise NotImplementedError(
                "This function supports dataframes with 30 columns or fewer. "
                f"Provided dataframe has {len(self.value_columns)} columns. {constants.FEEDBACK_LINK}"
            )

        aggregations = [
            (
                ex.BinaryAggregation(op, ex.free_var(left_col), ex.free_var(right_col)),
                f"{left_col}-{right_col}",
            )
            for left_col in self.value_columns
            for right_col in self.value_columns
        ]
        expr = self.expr.aggregate(aggregations)

        index_col_ids = [
            guid.generate_guid() for i in range(self.column_labels.nlevels)
        ]
        input_count = len(self.value_columns)
        unpivot_columns = tuple(
            (
                guid.generate_guid(),
                tuple(expr.column_ids[input_count * i : input_count * (i + 1)]),
            )
            for i in range(input_count)
        )
        labels = self._get_labels_for_columns(self.value_columns)

        expr = expr.unpivot(
            row_labels=labels,
            index_col_ids=index_col_ids,
            unpivot_columns=unpivot_columns,
        )

        return Block(
            expr,
            column_labels=self.column_labels,
            index_columns=index_col_ids,
            index_labels=self.column_labels.names,
        )

    def explode(
        self,
        column_ids: typing.Sequence[str],
        ignore_index: Optional[bool],
    ) -> Block:
        column_ids = [
            column_id
            for column_id in column_ids
            if bigframes.dtypes.is_array_like(self.expr.get_column_type(column_id))
        ]
        if len(column_ids) == 0:
            expr = self.expr
        else:
            expr = self.expr.explode(column_ids)

        if ignore_index:
            return Block(
                expr.drop_columns(self.index_columns),
                column_labels=self.column_labels,
                # Initiates default index creation using the block constructor.
                index_columns=[],
            )
        else:
            return Block(
                expr,
                column_labels=self.column_labels,
                index_columns=self.index_columns,
                index_labels=self.column_labels.names,
            )

    def _standard_stats(self, column_id) -> typing.Sequence[agg_ops.UnaryAggregateOp]:
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
        stats: list[agg_ops.UnaryAggregateOp] = [agg_ops.count_op]
        if dtype not in bigframes.dtypes.UNORDERED_DTYPES:
            stats += [agg_ops.min_op, agg_ops.max_op]
        if dtype in bigframes.dtypes.NUMERIC_BIGFRAMES_TYPES_PERMISSIVE:
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

    def _get_labels_for_columns(self, column_ids: typing.Sequence[str]) -> pd.Index:
        """Get column label for value columns, or index name for index columns"""
        indices = [self.value_columns.index(col_id) for col_id in column_ids]
        return self.column_labels.take(indices, allow_fill=False)

    def _normalize_expression(
        self,
        expr: core.ArrayValue,
        index_columns: typing.Sequence[str],
        assert_value_size: typing.Optional[int] = None,
    ):
        """Normalizes expression by moving index columns to left."""
        value_columns = [
            col_id for col_id in expr.column_ids if col_id not in index_columns
        ]
        if (assert_value_size is not None) and (
            len(value_columns) != assert_value_size
        ):
            raise ValueError("Unexpected number of value columns.")
        return expr.select_columns([*index_columns, *value_columns])

    def slice(
        self,
        start: typing.Optional[int] = None,
        stop: typing.Optional[int] = None,
        step: typing.Optional[int] = None,
    ) -> bigframes.core.blocks.Block:
        if step is None:
            step = 1
        if step == 0:
            raise ValueError("slice step cannot be zero")
        if step < 0:
            reverse_start = (-start - 1) if start else 0
            reverse_stop = (-stop - 1) if stop else None
            reverse_step = -step
            return self.reversed()._forward_slice(
                reverse_start, reverse_stop, reverse_step
            )
        return self._forward_slice(start or 0, stop, step)

    def _forward_slice(self, start: int = 0, stop=None, step: int = 1):
        """Performs slice but only for positive step size."""
        if step <= 0:
            raise ValueError("forward_slice only supports positive step size")

        use_postive_offsets = (
            (start > 0)
            or ((stop is not None) and (stop >= 0))
            or ((step > 1) and (start >= 0))
        )
        use_negative_offsets = (
            (start < 0) or (stop and (stop < 0)) or ((step > 1) and (start < 0))
        )

        block = self

        # only generate offsets that are used
        positive_offsets = None
        negative_offsets = None

        if use_postive_offsets:
            block, positive_offsets = self.promote_offsets()
        if use_negative_offsets:
            block, negative_offsets = block.reversed().promote_offsets()
            block = block.reversed()

        conditions = []
        if start != 0:
            if start > 0:
                assert positive_offsets
                conditions.append(ops.ge_op.as_expr(positive_offsets, ex.const(start)))
            else:
                assert negative_offsets
                conditions.append(
                    ops.le_op.as_expr(negative_offsets, ex.const(-start - 1))
                )
        if stop is not None:
            if stop >= 0:
                assert positive_offsets
                conditions.append(ops.lt_op.as_expr(positive_offsets, ex.const(stop)))
            else:
                assert negative_offsets
                conditions.append(
                    ops.gt_op.as_expr(negative_offsets, ex.const(-stop - 1))
                )
        if step > 1:
            if start >= 0:
                assert positive_offsets
                start_diff = ops.sub_op.as_expr(positive_offsets, ex.const(start))
            else:
                assert negative_offsets
                start_diff = ops.sub_op.as_expr(negative_offsets, ex.const(-start + 1))
            step_cond = ops.eq_op.as_expr(
                ops.mod_op.as_expr(start_diff, ex.const(step)), ex.const(0)
            )
            conditions.append(step_cond)

        for cond in conditions:
            block, cond_id = block.project_expr(cond)
            block = block.filter_by_id(cond_id)

        return block.select_columns(self.value_columns)

    # Using cache to optimize for Jupyter Notebook's behavior where both '__repr__'
    # and '__repr_html__' are called in a single display action, reducing redundant
    # queries.
    @functools.cache
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
        else:
            head_block = self
        computed_df, query_job = head_block.to_pandas()
        formatted_df = computed_df.set_axis(self.column_labels, axis=1)
        # we reset the axis and substitute the bf index name(s) for the default
        formatted_df.index.names = self.index.names  # type: ignore
        return formatted_df, count, query_job

    def promote_offsets(self, label: Label = None) -> typing.Tuple[Block, str]:
        result_id = guid.generate_guid()
        expr = self._expr.promote_offsets(result_id)
        return (
            Block(
                expr,
                index_columns=self.index_columns,
                column_labels=self.column_labels.insert(0, label),
                index_labels=self._index_labels,
            ),
            result_id,
        )

    def add_prefix(self, prefix: str, axis: str | int | None = None) -> Block:
        axis_number = bigframes.core.utils.get_axis_number(
            "rows" if (axis is None) else axis
        )
        if axis_number == 0:
            expr = self._expr
            for index_col in self._index_columns:
                expr = expr.project_to_id(
                    expression=ops.add_op.as_expr(
                        ex.const(prefix),
                        ops.AsTypeOp(to_type="string").as_expr(index_col),
                    ),
                    output_id=index_col,
                )
            return Block(
                expr,
                index_columns=self.index_columns,
                column_labels=self.column_labels,
                index_labels=self.index.names,
            )
        if axis_number == 1:
            return self.rename(columns=lambda label: f"{prefix}{label}")

    def add_suffix(self, suffix: str, axis: str | int | None = None) -> Block:
        axis_number = bigframes.core.utils.get_axis_number(
            "rows" if (axis is None) else axis
        )
        if axis_number == 0:
            expr = self._expr
            for index_col in self._index_columns:
                expr = expr.project_to_id(
                    expression=ops.add_op.as_expr(
                        ops.AsTypeOp(to_type="string").as_expr(index_col),
                        ex.const(suffix),
                    ),
                    output_id=index_col,
                )
            return Block(
                expr,
                index_columns=self.index_columns,
                column_labels=self.column_labels,
                index_labels=self.index.names,
            )
        if axis_number == 1:
            return self.rename(columns=lambda label: f"{label}{suffix}")

    def pivot(
        self,
        *,
        columns: Sequence[str],
        values: Sequence[str],
        columns_unique_values: typing.Optional[
            typing.Union[pd.Index, Sequence[object]]
        ] = None,
        values_in_index: typing.Optional[bool] = None,
    ):
        # We need the unique values from the pivot columns to turn them into
        # column ids. It can be deteremined by running a SQL query on the
        # underlying data. However, the caller can save that if they know the
        # unique values upfront by providing them explicitly.
        if columns_unique_values is None:
            # Columns+index should uniquely identify rows
            # Warning: This is not validated, breaking this constraint will
            # result in silently non-deterministic behavior.
            # -1 to allow for ordering column in addition to pivot columns
            max_unique_value = (_BQ_MAX_COLUMNS - 1) // len(values)
            columns_values = self._get_unique_values(columns, max_unique_value)
        else:
            columns_values = (
                columns_unique_values
                if isinstance(columns_unique_values, pd.Index)
                else pd.Index(columns_unique_values)
            )
        column_index = columns_values

        column_ids: list[str] = []
        block = self
        for value in values:
            for uvalue in columns_values:
                block, masked_id = self._create_pivot_col(block, columns, value, uvalue)
                column_ids.append(masked_id)

        block = block.select_columns(column_ids)
        aggregations = [(col_id, agg_ops.AnyValueOp()) for col_id in column_ids]
        result_block, _ = block.aggregate(
            by_column_ids=self.index_columns,
            aggregations=aggregations,
            dropna=True,
        )

        if values_in_index or len(values) > 1:
            value_labels = self._get_labels_for_columns(values)
            column_index = self._create_pivot_column_index(value_labels, columns_values)
            return result_block.with_column_labels(column_index)
        else:
            return result_block.with_column_labels(columns_values)

    def stack(self, how="left", levels: int = 1):
        """Unpivot last column axis level into row axis"""
        if levels == 0:
            return self

        # These are the values that will be turned into rows

        col_labels, row_labels = utils.split_index(self.column_labels, levels=levels)
        row_labels = row_labels.drop_duplicates()

        row_label_tuples = utils.index_as_tuples(row_labels)

        if col_labels is not None:
            result_index = col_labels.drop_duplicates().dropna(how="all")
            result_col_labels = utils.index_as_tuples(result_index)
        else:
            result_index = pd.Index([None])
            result_col_labels = list([()])

        # Get matching columns
        unpivot_columns: List[Tuple[str, List[str]]] = []
        dtypes = []
        for val in result_col_labels:
            col_id = guid.generate_guid("unpivot_")
            input_columns, dtype = self._create_stack_column(val, row_label_tuples)
            unpivot_columns.append((col_id, input_columns))
            if dtype:
                dtypes.append(dtype or pd.Float64Dtype())

        added_index_columns = [guid.generate_guid() for _ in range(row_labels.nlevels)]
        unpivot_expr = self._expr.unpivot(
            row_labels=row_label_tuples,
            passthrough_columns=self.index_columns,
            unpivot_columns=unpivot_columns,
            index_col_ids=added_index_columns,
            dtype=tuple(dtypes),
            how=how,
        )
        new_index_level_names = self.column_labels.names[-levels:]
        if how == "left":
            index_columns = [*self.index_columns, *added_index_columns]
            index_labels = [*self._index_labels, *new_index_level_names]
        else:
            index_columns = [*added_index_columns, *self.index_columns]
            index_labels = [*new_index_level_names, *self._index_labels]

        return Block(
            unpivot_expr,
            index_columns=index_columns,
            column_labels=result_index,
            index_labels=index_labels,
        )

    def melt(
        self,
        id_vars=typing.Sequence[str],
        value_vars=typing.Sequence[str],
        var_names=typing.Sequence[typing.Hashable],
        value_name: typing.Hashable = "value",
    ):
        # TODO: Implement col_level and ignore_index
        unpivot_col_id = guid.generate_guid()
        var_col_ids = tuple([guid.generate_guid() for _ in var_names])
        # single unpivot col
        unpivot_col = (unpivot_col_id, tuple(value_vars))
        value_labels = [self.col_id_to_label[col_id] for col_id in value_vars]
        id_labels = [self.col_id_to_label[col_id] for col_id in id_vars]

        dtype = self._expr.get_column_type(value_vars[0])

        unpivot_expr = self._expr.unpivot(
            row_labels=value_labels,
            passthrough_columns=id_vars,
            unpivot_columns=(unpivot_col,),
            index_col_ids=var_col_ids,
            dtype=dtype,
            how="right",
        )
        index_id = guid.generate_guid()
        unpivot_expr = unpivot_expr.promote_offsets(index_id)
        # Need to reorder to get id_vars before var_col and unpivot_col
        unpivot_expr = unpivot_expr.select_columns(
            [index_id, *id_vars, *var_col_ids, unpivot_col_id]
        )

        return Block(
            unpivot_expr,
            column_labels=[*id_labels, *var_names, value_name],
            index_columns=[index_id],
        )

    def _create_stack_column(
        self, col_label: typing.Tuple, stack_labels: typing.Sequence[typing.Tuple]
    ):
        dtype = None
        input_columns: list[Optional[str]] = []
        for uvalue in stack_labels:
            label_to_match = (*col_label, *uvalue)
            label_to_match = (
                label_to_match[0] if len(label_to_match) == 1 else label_to_match
            )
            matching_ids = self.label_to_col_id.get(label_to_match, [])
            input_id = matching_ids[0] if len(matching_ids) > 0 else None
            if input_id:
                if dtype and dtype != self._column_type(input_id):
                    raise NotImplementedError(
                        "Cannot stack columns with non-matching dtypes."
                    )
                else:
                    dtype = self._column_type(input_id)
            input_columns.append(input_id)
            # Input column i is the first one that
        return tuple(input_columns), dtype or pd.Float64Dtype()

    def _column_type(self, col_id: str) -> bigframes.dtypes.Dtype:
        col_offset = self.value_columns.index(col_id)
        dtype = self.dtypes[col_offset]
        return dtype

    @staticmethod
    def _create_pivot_column_index(
        value_labels: pd.Index, columns_values: pd.Index
    ) -> pd.Index:
        index_parts = []
        for value in value_labels:
            as_frame = columns_values.to_frame()
            as_frame.insert(0, None, value)  # type: ignore
            ipart = pd.MultiIndex.from_frame(
                as_frame, names=(None, *columns_values.names)
            )
            index_parts.append(ipart)
        return functools.reduce(lambda x, y: x.append(y), index_parts)

    @staticmethod
    def _create_pivot_col(
        block: Block, columns: typing.Sequence[str], value_col: str, value
    ) -> typing.Tuple[Block, str]:
        condition: typing.Optional[ex.Expression] = None
        nlevels = len(columns)
        for i in range(len(columns)):
            uvalue_level = value[i] if nlevels > 1 else value
            if pd.isna(uvalue_level):
                equality = ops.isnull_op.as_expr(columns[i])
            else:
                equality = ops.eq_op.as_expr(columns[i], ex.const(uvalue_level))
            if condition is not None:
                condition = ops.and_op.as_expr(equality, condition)
            else:
                condition = equality

        assert condition is not None
        return block.project_expr(
            ops.where_op.as_expr(value_col, condition, ex.const(None))
        )

    def _get_unique_values(
        self, columns: Sequence[str], max_unique_values: int
    ) -> pd.Index:
        """Gets N unique values for a column immediately."""
        # Importing here to avoid circular import
        import bigframes.core.block_transforms as block_tf
        import bigframes.dataframe as df

        unique_value_block = block_tf.drop_duplicates(
            self.select_columns(columns), columns
        )
        pd_values = (
            df.DataFrame(unique_value_block).head(max_unique_values + 1).to_pandas()
        )
        if len(pd_values) > max_unique_values:
            raise ValueError(f"Too many unique values: {pd_values}")

        if len(columns) > 1:
            return pd.MultiIndex.from_frame(pd_values)
        else:
            return pd.Index(pd_values.squeeze(axis=1).sort_values(na_position="first"))

    def concat(
        self,
        other: typing.Iterable[Block],
        how: typing.Literal["inner", "outer"],
        ignore_index=False,
    ):
        blocks: typing.List[Block] = [self, *other]
        if ignore_index:
            blocks = [block.reset_index() for block in blocks]
            level_names = None
        else:
            level_names, level_types = _align_indices(blocks)
            blocks = [_cast_index(block, level_types) for block in blocks]

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
            index_columns=list(result_expr.column_ids)[:index_nlevels],
            column_labels=aligned_blocks[0].column_labels,
            index_labels=level_names,
        )
        if ignore_index:
            result_block = result_block.reset_index()
        return result_block

    def merge(
        self,
        other: Block,
        how: typing.Literal[
            "inner",
            "left",
            "outer",
            "right",
            "cross",
        ],
        left_join_ids: typing.Sequence[str],
        right_join_ids: typing.Sequence[str],
        sort: bool,
        suffixes: tuple[str, str] = ("_x", "_y"),
    ) -> Block:
        left_mappings = [
            join_defs.JoinColumnMapping(
                source_table=join_defs.JoinSide.LEFT,
                source_id=id,
                destination_id=guid.generate_guid(),
            )
            for id in self.expr.column_ids
        ]
        right_mappings = [
            join_defs.JoinColumnMapping(
                source_table=join_defs.JoinSide.RIGHT,
                source_id=id,
                destination_id=guid.generate_guid(),
            )
            for id in other.expr.column_ids
        ]

        join_def = join_defs.JoinDefinition(
            conditions=tuple(
                join_defs.JoinCondition(left, right)
                for left, right in zip(left_join_ids, right_join_ids)
            ),
            mappings=(*left_mappings, *right_mappings),
            type=how,
        )
        joined_expr = self.expr.join(other.expr, join_def=join_def)
        result_columns = []
        matching_join_labels = []

        coalesced_ids = []
        get_column_left = join_def.get_left_mapping()
        get_column_right = join_def.get_right_mapping()
        for left_id, right_id in zip(left_join_ids, right_join_ids):
            coalesced_id = guid.generate_guid()
            joined_expr = joined_expr.project_to_id(
                ops.coalesce_op.as_expr(
                    get_column_left[left_id], get_column_right[right_id]
                ),
                coalesced_id,
            )
            coalesced_ids.append(coalesced_id)

        for col_id in self.value_columns:
            if col_id in left_join_ids:
                key_part = left_join_ids.index(col_id)
                matching_right_id = right_join_ids[key_part]
                if (
                    self.col_id_to_label[col_id]
                    == other.col_id_to_label[matching_right_id]
                ):
                    matching_join_labels.append(self.col_id_to_label[col_id])
                    result_columns.append(coalesced_ids[key_part])
                else:
                    result_columns.append(get_column_left[col_id])
            else:
                result_columns.append(get_column_left[col_id])
        for col_id in other.value_columns:
            if col_id in right_join_ids:
                key_part = right_join_ids.index(col_id)
                if other.col_id_to_label[matching_right_id] in matching_join_labels:
                    pass
                else:
                    result_columns.append(get_column_right[col_id])
            else:
                result_columns.append(get_column_right[col_id])

        if sort:
            # sort uses coalesced join keys always
            joined_expr = joined_expr.order_by(
                [
                    ordering.OrderingExpression(ex.free_var(col_id))
                    for col_id in coalesced_ids
                ],
            )

        joined_expr = joined_expr.select_columns(result_columns)
        labels = utils.merge_column_labels(
            self.column_labels,
            other.column_labels,
            coalesce_labels=matching_join_labels,
            suffixes=suffixes,
        )
        # Constructs default index
        offset_index_id = guid.generate_guid()
        expr = joined_expr.promote_offsets(offset_index_id)
        return Block(expr, index_columns=[offset_index_id], column_labels=labels)

    def join(
        self,
        other: Block,
        *,
        how="left",
        sort=False,
        block_identity_join: bool = False,
    ) -> Tuple[Block, Tuple[Mapping[str, str], Mapping[str, str]],]:
        if not isinstance(other, Block):
            # TODO(swast): We need to improve this error message to be more
            # actionable for the user. For example, it's possible they
            # could call set_index and try again to resolve this error.
            raise ValueError(
                f"Tried to join with an unexpected type: {type(other)}. {constants.FEEDBACK_LINK}"
            )

        # TODO(swast): Support cross-joins (requires reindexing).
        if how not in {"outer", "left", "right", "inner"}:
            raise NotImplementedError(
                f"Only how='outer','left','right','inner' currently supported. {constants.FEEDBACK_LINK}"
            )
        if self.index.nlevels == other.index.nlevels == 1:
            return join_mono_indexed(
                self, other, how=how, sort=sort, block_identity_join=block_identity_join
            )
        else:
            # Always sort mult-index join
            return join_multi_indexed(
                self, other, how=how, sort=sort, block_identity_join=block_identity_join
            )

    def _force_reproject(self) -> Block:
        """Forces a reprojection of the underlying tables expression. Used to force predicate/order application before subsequent operations."""
        return Block(
            self._expr._reproject_to_table(),
            index_columns=self.index_columns,
            column_labels=self.column_labels,
            index_labels=self.index.names,
        )

    def is_monotonic_increasing(
        self, column_id: typing.Union[str, Sequence[str]]
    ) -> bool:
        return self._is_monotonic(column_id, increasing=True)

    def is_monotonic_decreasing(
        self, column_id: typing.Union[str, Sequence[str]]
    ) -> bool:
        return self._is_monotonic(column_id, increasing=False)

    def to_sql_query(
        self, include_index: bool
    ) -> typing.Tuple[str, list[str], list[Label]]:
        """
        Compiles this DataFrame's expression tree to SQL, optionally
        including index columns.

        Args:
            include_index (bool):
                whether to include index columns.

        Returns:
            a tuple of (sql_string, index_column_id_list, index_column_label_list).
                If include_index is set to False, index_column_id_list and index_column_label_list
                return empty lists.
        """
        array_value = self._expr
        col_labels, idx_labels = list(self.column_labels), list(self.index.names)
        old_col_ids, old_idx_ids = list(self.value_columns), list(self.index_columns)

        if not include_index:
            idx_labels, old_idx_ids = [], []
            array_value = array_value.drop_columns(self.index_columns)

        old_ids = old_idx_ids + old_col_ids

        new_col_ids, new_idx_ids = utils.get_standardized_ids(col_labels, idx_labels)
        new_ids = new_idx_ids + new_col_ids

        substitutions = {}
        for old_id, new_id in zip(old_ids, new_ids):
            # TODO(swast): Do we need to further escape this, or can we rely on
            # the BigQuery unicode column name feature?
            substitutions[old_id] = new_id

        sql = self.session._to_sql(array_value, col_id_overrides=substitutions)
        return (
            sql,
            new_ids[: len(idx_labels)],
            idx_labels,
        )

    def cached(self, *, optimize_offsets=False, force: bool = False) -> Block:
        """Write the block to a session table and create a new block object that references it."""
        # use a heuristic for whether something needs to be cached
        if (not force) and self.session._is_trivially_executable(self.expr):
            return self
        if optimize_offsets:
            expr = self.session._cache_with_offsets(self.expr)
        else:
            expr = self.session._cache_with_cluster_cols(
                self.expr, cluster_cols=self.index_columns
            )
        return self.swap_array_expr(expr)

    def swap_array_expr(self, expr: core.ArrayValue) -> Block:
        # TODO: Validate schema unchanged
        return Block(
            expr,
            index_columns=self.index_columns,
            column_labels=self.column_labels,
            index_labels=self.index.names,
        )

    def _is_monotonic(
        self, column_ids: typing.Union[str, Sequence[str]], increasing: bool
    ) -> bool:
        if isinstance(column_ids, str):
            column_ids = (column_ids,)

        op_name = _MONOTONIC_INCREASING if increasing else _MONOTONIC_DECREASING

        column_name = " ".join(column_ids)
        if op_name in self._stats_cache[column_name]:
            return self._stats_cache[column_name][op_name]

        period = 1
        window = bigframes.core.WindowSpec(
            preceding=period,
            following=None,
        )

        # any NaN value means not monotonic
        block, last_notna_id = self.apply_unary_op(column_ids[0], ops.notnull_op)
        for column_id in column_ids[1:]:
            block, notna_id = block.apply_unary_op(column_id, ops.notnull_op)
            block, last_notna_id = block.apply_binary_op(
                last_notna_id, notna_id, ops.and_op
            )

        # loop over all columns to check monotonicity
        last_result_id = None
        for column_id in column_ids[::-1]:
            block, lag_result_id = block.apply_window_op(
                column_id, agg_ops.ShiftOp(period), window
            )
            block, strict_monotonic_id = block.apply_binary_op(
                column_id, lag_result_id, ops.gt_op if increasing else ops.lt_op
            )
            block, equal_id = block.apply_binary_op(column_id, lag_result_id, ops.eq_op)
            if last_result_id is None:
                block, last_result_id = block.apply_binary_op(
                    equal_id, strict_monotonic_id, ops.or_op
                )
                continue
            block, equal_monotonic_id = block.apply_binary_op(
                equal_id, last_result_id, ops.and_op
            )
            block, last_result_id = block.apply_binary_op(
                equal_monotonic_id, strict_monotonic_id, ops.or_op
            )

        block, monotonic_result_id = block.apply_binary_op(
            last_result_id, last_notna_id, ops.and_op  # type: ignore
        )
        result = block.get_stat(monotonic_result_id, agg_ops.all_op)
        self._stats_cache[column_name].update({op_name: result})
        return result


class BlockIndexProperties:
    """Accessor for the index-related block properties."""

    def __init__(self, block: Block):
        self._block = block

    @property
    def _expr(self) -> core.ArrayValue:
        return self._block.expr

    @property
    def name(self) -> Label:
        return self._block._index_labels[0]

    @property
    def names(self) -> typing.Sequence[Label]:
        return self._block._index_labels

    @property
    def nlevels(self) -> int:
        return len(self._block._index_columns)

    @property
    def dtypes(
        self,
    ) -> typing.Sequence[bigframes.dtypes.Dtype]:
        return [
            self._block.expr.get_column_type(col) for col in self._block.index_columns
        ]

    @property
    def session(self) -> core.Session:
        return self._expr.session

    @property
    def column_ids(self) -> Sequence[str]:
        """Column(s) to use as row labels."""
        return self._block._index_columns

    def __repr__(self) -> str:
        """Converts an Index to a string."""
        # TODO(swast): Add a timeout here? If the query is taking a long time,
        # maybe we just print the job metadata that we have so far?
        # TODO(swast): Avoid downloading the whole index by using job
        # metadata, like we do with DataFrame.
        preview = self.to_pandas()
        return repr(preview)

    def to_pandas(self) -> pd.Index:
        """Executes deferred operations and downloads the results."""
        # Project down to only the index column. So the query can be cached to visualize other data.
        index_columns = list(self._block.index_columns)
        dtypes = dict(zip(index_columns, self.dtypes))
        expr = self._expr.select_columns(index_columns)
        results, _ = self.session._execute(expr)
        df = expr.session._rows_to_dataframe(results, dtypes)
        df = df.set_index(index_columns)
        index = df.index
        index.names = list(self._block._index_labels)  # type:ignore
        return index

    def resolve_level(self, level: LevelsType) -> typing.Sequence[str]:
        if utils.is_list_like(level):
            levels = list(level)
        else:
            levels = [level]
        resolved_level_ids = []
        for level_ref in levels:
            if isinstance(level_ref, int):
                resolved_level_ids.append(self._block.index_columns[level_ref])
            elif isinstance(level_ref, typing.Hashable):
                matching_ids = self._block.index_name_to_col_id.get(level_ref, [])
                if len(matching_ids) != 1:
                    raise ValueError("level name cannot be found or is ambiguous")
                resolved_level_ids.append(matching_ids[0])
            else:
                raise ValueError(f"Unexpected level: {level_ref}")
        return resolved_level_ids

    def resolve_level_exact(self: BlockIndexProperties, label: Label) -> str:
        matches = self._block.index_name_to_col_id.get(label, [])
        if len(matches) > 1:
            raise ValueError(f"Ambiguous index level name {label}")
        if len(matches) == 0:
            raise ValueError(f"Cannot resolve index level name {label}")
        return matches[0]

    def is_uniquely_named(self: BlockIndexProperties):
        return len(set(self.names)) == len(self.names)


def join_mono_indexed(
    left: Block,
    right: Block,
    *,
    how="left",
    sort=False,
    block_identity_join: bool = False,
) -> Tuple[Block, Tuple[Mapping[str, str], Mapping[str, str]],]:
    left_expr = left.expr
    right_expr = right.expr
    left_mappings = [
        join_defs.JoinColumnMapping(
            source_table=join_defs.JoinSide.LEFT,
            source_id=id,
            destination_id=guid.generate_guid(),
        )
        for id in left_expr.column_ids
    ]
    right_mappings = [
        join_defs.JoinColumnMapping(
            source_table=join_defs.JoinSide.RIGHT,
            source_id=id,
            destination_id=guid.generate_guid(),
        )
        for id in right_expr.column_ids
    ]

    join_def = join_defs.JoinDefinition(
        conditions=(
            join_defs.JoinCondition(left.index_columns[0], right.index_columns[0]),
        ),
        mappings=(*left_mappings, *right_mappings),
        type=how,
    )
    combined_expr = left_expr.join(
        right_expr,
        join_def=join_def,
        allow_row_identity_join=(not block_identity_join),
    )
    get_column_left = join_def.get_left_mapping()
    get_column_right = join_def.get_right_mapping()
    # Drop original indices from each side. and used the coalesced combination generated by the join.
    left_index = get_column_left[left.index_columns[0]]
    right_index = get_column_right[right.index_columns[0]]
    # Drop original indices from each side. and used the coalesced combination generated by the join.
    combined_expr, coalesced_join_cols = coalesce_columns(
        combined_expr, [left_index], [right_index], how=how
    )
    if sort:
        combined_expr = combined_expr.order_by(
            [
                ordering.OrderingExpression(ex.free_var(col_id))
                for col_id in coalesced_join_cols
            ]
        )
    block = Block(
        combined_expr,
        index_columns=coalesced_join_cols,
        column_labels=[*left.column_labels, *right.column_labels],
        index_labels=[left.index.name]
        if left.index.name == right.index.name
        else [None],
    )
    return (
        block,
        (get_column_left, get_column_right),
    )


def join_multi_indexed(
    left: Block,
    right: Block,
    *,
    how="left",
    sort=False,
    block_identity_join: bool = False,
) -> Tuple[Block, Tuple[Mapping[str, str], Mapping[str, str]],]:
    if not (left.index.is_uniquely_named() and right.index.is_uniquely_named()):
        raise ValueError("Joins not supported on indices with non-unique level names")

    common_names = [name for name in left.index.names if name in right.index.names]
    if len(common_names) == 0:
        raise ValueError("Cannot join without a index level in common.")

    left_only_names = [
        name for name in left.index.names if name not in right.index.names
    ]
    right_only_names = [
        name for name in right.index.names if name not in left.index.names
    ]

    left_join_ids = [left.index.resolve_level_exact(name) for name in common_names]
    right_join_ids = [right.index.resolve_level_exact(name) for name in common_names]

    names_fully_match = len(left_only_names) == 0 and len(right_only_names) == 0

    left_expr = left.expr
    right_expr = right.expr

    left_mappings = [
        join_defs.JoinColumnMapping(
            source_table=join_defs.JoinSide.LEFT,
            source_id=id,
            destination_id=guid.generate_guid(),
        )
        for id in left_expr.column_ids
    ]
    right_mappings = [
        join_defs.JoinColumnMapping(
            source_table=join_defs.JoinSide.RIGHT,
            source_id=id,
            destination_id=guid.generate_guid(),
        )
        for id in right_expr.column_ids
    ]

    join_def = join_defs.JoinDefinition(
        conditions=tuple(
            join_defs.JoinCondition(left, right)
            for left, right in zip(left_join_ids, right_join_ids)
        ),
        mappings=(*left_mappings, *right_mappings),
        type=how,
    )

    combined_expr = left_expr.join(
        right_expr,
        join_def=join_def,
        # If we're only joining on a subset of the index columns, we need to
        # perform a true join.
        allow_row_identity_join=(names_fully_match and not block_identity_join),
    )
    get_column_left = join_def.get_left_mapping()
    get_column_right = join_def.get_right_mapping()
    left_ids_post_join = [get_column_left[id] for id in left_join_ids]
    right_ids_post_join = [get_column_right[id] for id in right_join_ids]
    # Drop original indices from each side. and used the coalesced combination generated by the join.
    combined_expr, coalesced_join_cols = coalesce_columns(
        combined_expr, left_ids_post_join, right_ids_post_join, how=how
    )
    if sort:
        combined_expr = combined_expr.order_by(
            [
                ordering.OrderingExpression(ex.free_var(col_id))
                for col_id in coalesced_join_cols
            ]
        )

    if left.index.nlevels == 1:
        index_labels = right.index.names
    elif right.index.nlevels == 1:
        index_labels = left.index.names
    else:
        index_labels = [*common_names, *left_only_names, *right_only_names]

    def resolve_label_id(label: Label) -> str:
        # if name is shared between both blocks, coalesce the values
        if label in common_names:
            return coalesced_join_cols[common_names.index(label)]
        if label in left_only_names:
            return get_column_left[left.index.resolve_level_exact(label)]
        if label in right_only_names:
            return get_column_right[right.index.resolve_level_exact(label)]
        raise ValueError(f"Unexpected label: {label}")

    index_columns = [resolve_label_id(label) for label in index_labels]

    block = Block(
        combined_expr,
        index_columns=index_columns,
        column_labels=[*left.column_labels, *right.column_labels],
        index_labels=index_labels,
    )
    return (
        block,
        (get_column_left, get_column_right),
    )


def coalesce_columns(
    expr: core.ArrayValue,
    left_ids: typing.Sequence[str],
    right_ids: typing.Sequence[str],
    how: str,
) -> Tuple[core.ArrayValue, Sequence[str]]:
    result_ids = []
    for left_id, right_id in zip(left_ids, right_ids):
        if how == "left" or how == "inner":
            result_ids.append(left_id)
            expr = expr.drop_columns([right_id])
        elif how == "right":
            result_ids.append(right_id)
            expr = expr.drop_columns([left_id])
        elif how == "outer":
            coalesced_id = guid.generate_guid()
            expr = expr.project_to_id(
                ops.coalesce_op.as_expr(left_id, right_id), coalesced_id
            )
            expr = expr.drop_columns([left_id, right_id])
            result_ids.append(coalesced_id)
        else:
            raise ValueError(f"Unexpected join type: {how}. {constants.FEEDBACK_LINK}")
    return expr, result_ids


def _cast_index(block: Block, dtypes: typing.Sequence[bigframes.dtypes.Dtype]):
    original_block = block
    result_ids = []
    for idx_id, idx_dtype, target_dtype in zip(
        block.index_columns, block.index.dtypes, dtypes
    ):
        if idx_dtype != target_dtype:
            block, result_id = block.apply_unary_op(idx_id, ops.AsTypeOp(target_dtype))
            result_ids.append(result_id)
        else:
            result_ids.append(idx_id)

    expr = block.expr.select_columns((*result_ids, *original_block.value_columns))
    return Block(
        expr,
        index_columns=result_ids,
        column_labels=original_block.column_labels,
        index_labels=original_block.index.names,
    )


### Schema alignment Utils
### TODO: Pull out to separate module?
def _align_block_to_schema(
    block: Block, schema: dict[Label, bigframes.dtypes.Dtype]
) -> Block:
    """For a given schema, remap block to schema by reordering columns,  and inserting nulls."""
    col_ids: typing.Tuple[str, ...] = ()
    for label, dtype in schema.items():
        matching_ids: typing.Sequence[str] = block.label_to_col_id.get(label, ())
        if len(matching_ids) > 0:
            col_id = matching_ids[-1]
            col_dtype = block.expr.get_column_type(col_id)
            if dtype != col_dtype:
                # If _align_schema worked properly, this should always be an upcast
                block, col_id = block.apply_unary_op(col_id, ops.AsTypeOp(dtype))
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


def _align_indices(
    blocks: typing.Sequence[Block],
) -> typing.Tuple[typing.Sequence[Label], typing.Sequence[bigframes.dtypes.Dtype]]:
    """Validates that the blocks have compatible indices and returns the resulting label names and dtypes."""
    names = blocks[0].index.names
    types = blocks[0].index.dtypes

    for block in blocks[1:]:
        if len(names) != block.index.nlevels:
            raise NotImplementedError(
                f"Cannot combine indices with different number of levels. Use 'ignore_index'=True. {constants.FEEDBACK_LINK}"
            )
        names = [
            lname if lname == rname else None
            for lname, rname in zip(names, block.index.names)
        ]
        types = [
            bigframes.dtypes.lcd_type_or_throw(ltype, rtype)
            for ltype, rtype in zip(types, block.index.dtypes)
        ]
    types = typing.cast(typing.Sequence[bigframes.dtypes.Dtype], types)
    return names, types


def _combine_schema_inner(
    left: typing.Dict[Label, bigframes.dtypes.Dtype],
    right: typing.Dict[Label, bigframes.dtypes.Dtype],
) -> typing.Dict[Label, bigframes.dtypes.Dtype]:
    result = dict()
    for label, left_type in left.items():
        if label in right:
            right_type = right[label]
            output_type = bigframes.dtypes.lcd_type(left_type, right_type)
            if output_type is None:
                raise ValueError(
                    f"Cannot concat rows with label {label} due to mismatched types. {constants.FEEDBACK_LINK}"
                )
            result[label] = output_type
    return result


def _combine_schema_outer(
    left: typing.Dict[Label, bigframes.dtypes.Dtype],
    right: typing.Dict[Label, bigframes.dtypes.Dtype],
) -> typing.Dict[Label, bigframes.dtypes.Dtype]:
    result = dict()
    for label, left_type in left.items():
        if label not in right:
            result[label] = left_type
        else:
            right_type = right[label]
            output_type = bigframes.dtypes.lcd_type(left_type, right_type)
            if output_type is None:
                raise NotImplementedError(
                    f"Cannot concat rows with label {label} due to mismatched types. {constants.FEEDBACK_LINK}"
                )
            result[label] = output_type
    for label, right_type in right.items():
        if label not in left:
            result[label] = right_type
    return result


def _get_block_schema(
    block: Block,
) -> typing.Dict[Label, bigframes.dtypes.Dtype]:
    """Extracts the schema from the block. Where duplicate labels exist, take the last matching column."""
    result = dict()
    for label, dtype in zip(block.column_labels, block.dtypes):
        result[label] = typing.cast(bigframes.dtypes.Dtype, dtype)
    return result
