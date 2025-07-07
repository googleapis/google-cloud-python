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

import ast
import dataclasses
import datetime
import functools
import itertools
import random
import textwrap
import typing
from typing import Iterable, List, Literal, Mapping, Optional, Sequence, Tuple, Union
import warnings

import bigframes_vendored.constants as constants
import google.cloud.bigquery as bigquery
import numpy
import pandas as pd
import pyarrow as pa

from bigframes import session
from bigframes._config import sampling_options
import bigframes.constants
from bigframes.core import local_data
import bigframes.core as core
import bigframes.core.compile.googlesql as googlesql
import bigframes.core.expression as ex
import bigframes.core.expression as scalars
import bigframes.core.guid as guid
import bigframes.core.identifiers
import bigframes.core.join_def as join_defs
import bigframes.core.ordering as ordering
import bigframes.core.pyarrow_utils as pyarrow_utils
import bigframes.core.schema as bf_schema
import bigframes.core.sql as sql
import bigframes.core.utils as utils
import bigframes.core.window_spec as windows
import bigframes.dtypes
import bigframes.exceptions as bfe
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops
from bigframes.session import dry_runs
from bigframes.session import executor as executors

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
    allow_large_results: Optional[bool] = None
    ordered: bool = True


class Block:
    """A immutable 2D data structure."""

    def __init__(
        self,
        expr: core.ArrayValue,
        index_columns: Iterable[str],
        column_labels: typing.Union[pd.Index, typing.Iterable[Label]],
        index_labels: typing.Union[pd.Index, typing.Iterable[Label], None] = None,
        *,
        transpose_cache: Optional[Block] = None,
    ):
        """Construct a block object, will create default index if no index columns specified."""
        index_columns = list(index_columns)
        if index_labels is not None:
            index_labels = list(index_labels)
            if len(index_labels) != len(index_columns):
                raise ValueError(
                    f"'index_columns' (size {len(index_columns)}) and 'index_labels' (size {len(index_labels)}) must have equal length"
                )

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
        self._transpose_cache: Optional[Block] = transpose_cache
        self._view_ref: Optional[bigquery.TableReference] = None
        self._view_ref_dry_run: Optional[bigquery.TableReference] = None

    @classmethod
    def from_pyarrow(
        cls,
        data: pa.Table,
        session: bigframes.Session,
    ) -> Block:
        column_labels = data.column_names

        # TODO(tswast): Use array_value.promote_offsets() instead once that node is
        # supported by the local engine.
        offsets_col = bigframes.core.guid.generate_guid()
        index_ids = [offsets_col]
        index_labels = [None]

        # TODO(https://github.com/googleapis/python-bigquery-dataframes/issues/859):
        # Allow users to specify the "total ordering" column(s) or allow multiple
        # such columns.
        data = pyarrow_utils.append_offsets(data, offsets_col=offsets_col)

        # from_pyarrow will normalize the types for us.
        managed_data = local_data.ManagedArrowTable.from_pyarrow(data)
        array_value = core.ArrayValue.from_managed(managed_data, session=session)
        block = cls(
            array_value,
            column_labels=column_labels,
            index_columns=index_ids,
            index_labels=index_labels,
        )
        return block

    @classmethod
    def from_local(
        cls,
        data: pd.DataFrame,
        session: bigframes.Session,
        *,
        cache_transpose: bool = True,
    ) -> Block:
        # Assumes caller has already converted datatypes to bigframes ones.
        pd_data = data
        column_labels = pd_data.columns
        index_labels = list(pd_data.index.names)

        # unique internal ids
        column_ids = [f"column_{i}" for i in range(len(pd_data.columns))]
        index_ids = [f"level_{level}" for level in range(pd_data.index.nlevels)]

        pd_data = pd_data.set_axis(column_ids, axis=1)
        pd_data = pd_data.reset_index(names=index_ids)
        managed_data = local_data.ManagedArrowTable.from_pandas(pd_data)
        array_value = core.ArrayValue.from_managed(managed_data, session=session)
        block = cls(
            array_value,
            column_labels=column_labels,
            index_columns=index_ids,
            index_labels=index_labels,
        )
        if cache_transpose:
            try:
                # this cache will help when aligning on axis=1
                block = block.with_transpose_cache(
                    cls.from_local(data.T, session, cache_transpose=False)
                )
            except Exception:
                pass
        return block

    @property
    def index(self) -> BlockIndexProperties:
        """Row identities for values in the Block."""
        return BlockIndexProperties(self)

    @functools.cached_property
    def shape(self) -> typing.Tuple[int, int]:
        """Returns dimensions as (length, width) tuple."""
        # Support zero-query for hermetic unit tests.
        if self.expr.session is None and self.expr.node.row_count:
            try:
                return self.expr.node.row_count
            except Exception:
                pass

        row_count = self.session._executor.execute(self.expr.row_count()).to_py_scalar()
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
    def session(self) -> session.Session:
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

    def resolve_label_exact(self, label: Label) -> Optional[str]:
        """Returns the column id matching the label if there is exactly
        one such column. If there are multiple columns with the same name,
        raises an error. If there is no such a column, returns None."""
        matches = self.label_to_col_id.get(label, [])
        if len(matches) > 1:
            raise ValueError(
                f"Multiple columns matching id {label} were found. {constants.FEEDBACK_LINK}"
            )
        return matches[0] if len(matches) != 0 else None

    def resolve_label_exact_or_error(self, label: Label) -> str:
        """Returns the column id matching the label if there is exactly
        one such column. If there are multiple columns with the same name,
        raises an error. If there is no such a column, raises an error too."""
        col_id = self.resolve_label_exact(label)
        if col_id is None:
            raise ValueError(f"Label {label} not found. {constants.FEEDBACK_LINK}")
        return col_id

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

    @property
    def explicitly_ordered(self) -> bool:
        return self.expr.explicitly_ordered

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
        expr = self._expr
        if (
            self.session._default_index_type
            == bigframes.enums.DefaultIndexKind.SEQUENTIAL_INT64
        ):
            expr, new_index_col_id = expr.promote_offsets()
            new_index_cols = [new_index_col_id]
        elif self.session._default_index_type == bigframes.enums.DefaultIndexKind.NULL:
            new_index_cols = []
        else:
            raise ValueError(
                f"Unrecognized default index kind: {self.session._default_index_type}"
            )

        if drop:
            # Even though the index might be part of the ordering, keep that
            # ordering expression as reset_index shouldn't change the row
            # order.
            expr = expr.drop_columns(self.index_columns)
            return Block(
                expr,
                index_columns=new_index_cols,
                column_labels=self.column_labels,
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
                index_columns=new_index_cols,
                column_labels=column_labels_modified,
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

    def to_arrow(
        self,
        *,
        ordered: bool = True,
        allow_large_results: Optional[bool] = None,
    ) -> Tuple[pa.Table, Optional[bigquery.QueryJob]]:
        """Run query and download results as a pyarrow Table."""
        execute_result = self.session._executor.execute(
            self.expr, ordered=ordered, use_explicit_destination=allow_large_results
        )
        pa_table = execute_result.to_arrow_table()

        pa_index_labels = []
        for index_level, index_label in enumerate(self._index_labels):
            if isinstance(index_label, str):
                pa_index_labels.append(index_label)
            else:
                pa_index_labels.append(f"__index_level_{index_level}__")

        # pa.Table.from_pandas puts index columns last, so update to match.
        pa_table = pa_table.select([*self.value_columns, *self.index_columns])
        pa_table = pa_table.rename_columns(list(self.column_labels) + pa_index_labels)
        return pa_table, execute_result.query_job

    def to_pandas(
        self,
        max_download_size: Optional[int] = None,
        sampling_method: Optional[str] = None,
        random_state: Optional[int] = None,
        *,
        ordered: bool = True,
        allow_large_results: Optional[bool] = None,
    ) -> Tuple[pd.DataFrame, Optional[bigquery.QueryJob]]:
        """Run query and download results as a pandas DataFrame.

        Args:
            max_download_size (int, default None):
                Download size threshold in MB. If max_download_size is exceeded when downloading data
                (e.g., to_pandas()), the data will be downsampled if
                bigframes.options.sampling.enable_downsampling is True, otherwise, an error will be
                raised. If set to a value other than None, this will supersede the global config.
            sampling_method (str, default None):
                Downsampling algorithms to be chosen from, the choices are: "head": This algorithm
                returns a portion of the data from the beginning. It is fast and requires minimal
                computations to perform the downsampling; "uniform": This algorithm returns uniform
                random samples of the data. If set to a value other than None, this will supersede
                the global config.
            random_state (int, default None):
                The seed for the uniform downsampling algorithm. If provided, the uniform method may
                take longer to execute and require more computation. If set to a value other than
                None, this will supersede the global config.
            ordered (bool, default True):
                Determines whether the resulting pandas dataframe will be ordered.
                Whether the row ordering is deterministics depends on whether session ordering is strict.

        Returns:
            pandas.DataFrame, QueryJob
        """
        sampling = self._get_sampling_option(
            max_download_size, sampling_method, random_state
        )

        df, query_job = self._materialize_local(
            materialize_options=MaterializationOptions(
                downsampling=sampling,
                allow_large_results=allow_large_results,
                ordered=ordered,
            )
        )
        df.set_axis(self.column_labels, axis=1, copy=False)
        return df, query_job

    def _get_sampling_option(
        self,
        max_download_size: Optional[int] = None,
        sampling_method: Optional[str] = None,
        random_state: Optional[int] = None,
    ) -> sampling_options.SamplingOptions:

        if (sampling_method is not None) and (sampling_method not in _SAMPLING_METHODS):
            raise NotImplementedError(
                f"The downsampling method {sampling_method} is not implemented, "
                f"please choose from {','.join(_SAMPLING_METHODS)}."
            )

        sampling = bigframes.options.sampling.with_max_download_size(max_download_size)
        if sampling_method is None:
            return sampling.with_disabled()

        return sampling.with_method(sampling_method).with_random_state(  # type: ignore
            random_state
        )

    def try_peek(
        self, n: int = 20, force: bool = False, allow_large_results=None
    ) -> typing.Optional[pd.DataFrame]:
        if force or self.expr.supports_fast_peek:
            result = self.session._executor.peek(
                self.expr, n, use_explicit_destination=allow_large_results
            )
            df = result.to_pandas()
            self._copy_index_to_pandas(df)
            return df
        else:
            return None

    def to_pandas_batches(
        self,
        page_size: Optional[int] = None,
        max_results: Optional[int] = None,
        allow_large_results: Optional[bool] = None,
        squeeze: Optional[bool] = False,
    ):
        """Download results one message at a time.

        page_size and max_results determine the size and number of batches,
        see https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob#google_cloud_bigquery_job_QueryJob_result"""
        execute_result = self.session._executor.execute(
            self.expr,
            ordered=True,
            use_explicit_destination=allow_large_results,
        )

        total_batches = 0
        for df in execute_result.to_pandas_batches(
            page_size=page_size, max_results=max_results
        ):
            total_batches += 1
            self._copy_index_to_pandas(df)
            if squeeze:
                yield df.squeeze(axis=1)
            else:
                yield df

        # To reduce the number of edge cases to consider when working with the
        # results of this, always return at least one DataFrame. See:
        # b/428918844.
        if total_batches == 0:
            df = pd.DataFrame(
                {
                    col: pd.Series([], dtype=self.expr.get_column_type(col))
                    for col in itertools.chain(self.value_columns, self.index_columns)
                }
            )
            self._copy_index_to_pandas(df)
            yield df

    def _copy_index_to_pandas(self, df: pd.DataFrame):
        """Set the index on pandas DataFrame to match this block.

        Warning: This method modifies ``df`` inplace.
        """
        # Note: If BigQuery DataFrame has null index, a default one will be created for the local materialization.
        if len(self.index_columns) > 0:
            df.set_index(list(self.index_columns), inplace=True)
            # Pandas names is annotated as list[str] rather than the more
            # general Sequence[Label] that BigQuery DataFrames has.
            # See: https://github.com/pandas-dev/pandas-stubs/issues/804
            df.index.names = self.index.names  # type: ignore
        df.columns = self.column_labels

    def _materialize_local(
        self, materialize_options: MaterializationOptions = MaterializationOptions()
    ) -> Tuple[pd.DataFrame, Optional[bigquery.QueryJob]]:
        """Run query and download results as a pandas DataFrame. Return the total number of results as well."""
        # TODO(swast): Allow for dry run and timeout.
        execute_result = self.session._executor.execute(
            self.expr,
            ordered=materialize_options.ordered,
            use_explicit_destination=materialize_options.allow_large_results,
        )
        sample_config = materialize_options.downsampling
        if execute_result.total_bytes is not None:
            table_mb = execute_result.total_bytes / _BYTES_TO_MEGABYTES
            max_download_size = sample_config.max_download_size
            fraction = (
                max_download_size / table_mb
                if (max_download_size is not None) and (table_mb != 0)
                else 2
            )
        else:
            # Since we cannot acquire the table size without a query_job,
            # we skip the sampling.
            if sample_config.enable_downsampling:
                msg = bfe.format_message(
                    "Sampling is disabled and there is no download size limit when 'allow_large_results' is set to "
                    "False. To prevent downloading excessive data, it is recommended to use the peek() method, or "
                    "limit the data with methods like .head() or .sample() before proceeding with downloads."
                )
                warnings.warn(msg, category=UserWarning)
            fraction = 2

        # TODO: Maybe materialize before downsampling
        # Some downsampling methods
        if fraction < 1 and (execute_result.total_rows is not None):
            if not sample_config.enable_downsampling:
                raise RuntimeError(
                    f"The data size ({table_mb:.2f} MB) exceeds the maximum download limit of "
                    f"{max_download_size} MB. You can:\n\t* Enable downsampling in global options:\n"
                    "\t\t`bigframes.options.sampling.enable_downsampling = True`\n"
                    "\t* Update the global `max_download_size` option. Please make sure "
                    "there is enough memory available:\n"
                    "\t\t`bigframes.options.sampling.max_download_size = desired_size`"
                    " # Setting it to None will download all the data\n"
                    f"{constants.FEEDBACK_LINK}"
                )
            msg = bfe.format_message(
                f"The data size ({table_mb:.2f} MB) exceeds the maximum download limit of"
                f"({max_download_size} MB). It will be downsampled to {max_download_size} "
                "MB for download.\nPlease refer to the documentation for configuring "
                "the downloading limit."
            )
            warnings.warn(msg, category=UserWarning)
            total_rows = execute_result.total_rows
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
            df = execute_result.to_pandas()
            self._copy_index_to_pandas(df)

        return df, execute_result.query_job

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
            block = self.split(
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

    def split(
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
            ordering_col, ops.AsTypeOp(to_type=bigframes.dtypes.STRING_DTYPE)
        )

        # Apply hash method to sum col and order by it.
        block, string_sum_col = block.apply_binary_op(
            string_ordering_col, random_state_col, ops.strconcat_op
        )
        block, hash_string_sum_col = block.apply_unary_op(string_sum_col, ops.hash_op)
        block = block.order_by(
            [ordering.OrderingExpression(ex.deref(hash_string_sum_col))]
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
                        ordering.OrderingExpression(ex.deref(idx_col))
                        for idx_col in sliced_block.index_columns
                    ]
                )
                for sliced_block in sliced_blocks
            ]
        elif sort is False:
            sliced_blocks = [
                sliced_block.order_by(
                    [ordering.OrderingExpression(ex.deref(ordering_col))]
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
        self,
        value_keys: Optional[Iterable[str]] = None,
        *,
        ordered: bool = True,
        max_download_size: Optional[int] = None,
        sampling_method: Optional[str] = None,
        random_state: Optional[int] = None,
    ) -> typing.Tuple[pd.Series, bigquery.QueryJob]:
        sampling = self._get_sampling_option(
            max_download_size, sampling_method, random_state
        )
        if sampling.enable_downsampling:
            raise NotImplementedError("Dry run with sampling is not supported")

        expr = self._apply_value_keys_to_expr(value_keys=value_keys)
        query_job = self.session._executor.dry_run(expr, ordered)

        column_dtypes = {
            col: self.expr.get_column_type(self.resolve_label_exact_or_error(col))
            for col in self.column_labels
        }

        dry_run_stats = dry_runs.get_query_stats_with_dtypes(
            query_job, column_dtypes, self.index.dtypes
        )
        return dry_run_stats, query_job

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
        block = Block(
            self._expr,
            index_columns=self.index_columns,
            column_labels=label_list,
            index_labels=self.index.names,
        )
        singleton_label = len(list(value)) == 1 and list(value)[0]
        if singleton_label is not None and self._transpose_cache is not None:
            new_cache, label_id = self._transpose_cache.create_constant(singleton_label)
            new_cache = new_cache.set_index([label_id])
            block = block.with_transpose_cache(new_cache)
        return block

    def with_transpose_cache(self, transposed: Block):
        return Block(
            self._expr,
            index_columns=self.index_columns,
            column_labels=self._column_labels,
            index_labels=self.index.names,
            transpose_cache=transposed,
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
        array_val, result_id = self._expr.project_to_id(expr)
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

    def apply_nary_op(
        self,
        columns: Iterable[str],
        op: ops.NaryOp,
        result_label: Label = None,
    ) -> typing.Tuple[Block, str]:
        expr = op.as_expr(*columns)
        return self.project_expr(expr, result_label)

    def multi_apply_window_op(
        self,
        columns: typing.Sequence[str],
        op: agg_ops.UnaryWindowOp,
        window_spec: windows.WindowSpec,
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
        op: Union[ops.UnaryOp, ex.Expression],
    ) -> Block:
        if isinstance(op, ops.UnaryOp):
            input_varname = guid.generate_guid()
            expr = op.as_expr(ex.free_var(input_varname))
        else:
            input_varnames = op.free_variables
            assert len(input_varnames) == 1
            expr = op
            input_varname = input_varnames[0]

        block = self

        exprs = [
            expr.bind_variables({input_varname: ex.deref(col_id)})
            for col_id in self.value_columns
        ]
        block = self.project_exprs(exprs, labels=self.column_labels, drop=True)

        # Special case, we can preserve transpose cache for full-frame unary ops
        if self._transpose_cache is not None:
            new_transpose_cache = self._transpose_cache.multi_apply_unary_op(op)
            block = block.with_transpose_cache(new_transpose_cache)
        return block

    def project_exprs(
        self,
        exprs: Sequence[ex.Expression],
        labels: Union[Sequence[Label], pd.Index],
        drop=False,
    ) -> Block:
        new_array, _ = self.expr.compute_values(exprs)
        if drop:
            new_array = new_array.drop_columns(self.value_columns)

        return Block(
            new_array,
            index_columns=self.index_columns,
            column_labels=labels
            if drop
            else self.column_labels.append(pd.Index(labels)),
            index_labels=self._index_labels,
        )

    def apply_window_op(
        self,
        column: str,
        op: agg_ops.UnaryWindowOp,
        window_spec: windows.WindowSpec,
        *,
        result_label: Label = None,
        skip_null_groups: bool = False,
        skip_reproject_unsafe: bool = False,
        never_skip_nulls: bool = False,
    ) -> typing.Tuple[Block, str]:
        agg_expr = ex.UnaryAggregation(op, ex.deref(column))
        return self.apply_analytic(
            agg_expr,
            window_spec,
            result_label,
            skip_reproject_unsafe=skip_reproject_unsafe,
            never_skip_nulls=never_skip_nulls,
            skip_null_groups=skip_null_groups,
        )

    def apply_analytic(
        self,
        agg_expr: ex.Aggregation,
        window: windows.WindowSpec,
        result_label: Label,
        *,
        skip_reproject_unsafe: bool = False,
        never_skip_nulls: bool = False,
        skip_null_groups: bool = False,
    ) -> typing.Tuple[Block, str]:
        block = self
        if skip_null_groups:
            for key in window.grouping_keys:
                block = block.filter(ops.notnull_op.as_expr(key.id.name))
        expr, result_id = block._expr.project_window_expr(
            agg_expr,
            window,
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
        expr, result_id = self.expr.create_constant(scalar_constant, dtype=dtype)
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
        operation: typing.Union[agg_ops.UnaryAggregateOp, agg_ops.NullaryAggregateOp],
        *,
        axis: int | str = 0,
        dropna: bool = True,
    ) -> Block:
        axis_n = utils.get_axis_number(axis)
        if axis_n == 0:
            aggregations = [
                (
                    ex.UnaryAggregation(operation, ex.deref(col_id))
                    if isinstance(operation, agg_ops.UnaryAggregateOp)
                    else ex.NullaryAggregation(operation),
                    col_id,
                )
                for col_id in self.value_columns
            ]
            result_expr, index_id = self.expr.aggregate(
                aggregations, dropna=dropna
            ).create_constant(None, None)
            # Transpose as last operation so that final block has valid transpose cache
            return Block(
                result_expr,
                index_columns=[index_id],
                column_labels=self.column_labels,
                index_labels=[None],
            ).transpose(original_row_index=pd.Index([None]), single_row_mode=True)
        else:  # axis_n == 1
            # using offsets as identity to group on.
            # TODO: Allow to promote identity/total_order columns instead for better perf
            expr_with_offsets, offset_col = self.expr.promote_offsets()
            stacked_expr, (_, value_col_ids, passthrough_cols,) = unpivot(
                expr_with_offsets,
                row_labels=self.column_labels,
                unpivot_columns=[tuple(self.value_columns)],
                passthrough_columns=[*self.index_columns, offset_col],
            )
            # these corresponed to passthrough_columns provided to unpivot
            index_cols = passthrough_cols[:-1]
            og_offset_col = passthrough_cols[-1]
            index_aggregations = [
                (
                    ex.UnaryAggregation(agg_ops.AnyValueOp(), ex.deref(col_id)),
                    col_id,
                )
                for col_id in index_cols
            ]
            # TODO: may need add NullaryAggregation in main_aggregation
            # when agg add support for axis=1, needed for agg("size", axis=1)
            assert isinstance(
                operation, agg_ops.UnaryAggregateOp
            ), f"Expected a unary operation, but got {operation}. Please report this error and how you got here to the BigQuery DataFrames team (bit.ly/bigframes-feedback)."
            main_aggregation = (
                ex.UnaryAggregation(operation, ex.deref(value_col_ids[0])),
                value_col_ids[0],
            )
            # Drop row identity after aggregating over it
            result_expr = stacked_expr.aggregate(
                [*index_aggregations, main_aggregation],
                by_column_ids=[og_offset_col],
                dropna=dropna,
            ).drop_columns([og_offset_col])
            return Block(
                result_expr,
                index_columns=index_cols,
                column_labels=[None],
                index_labels=self.index.names,
            )

    def aggregate_size(
        self,
        by_column_ids: typing.Sequence[str] = (),
        *,
        dropna: bool = True,
    ):
        """Returns a block object to compute the size(s) of groups."""
        agg_specs = [
            (ex.NullaryAggregation(agg_ops.SizeOp()), guid.generate_guid()),
        ]
        output_col_ids = [agg_spec[1] for agg_spec in agg_specs]
        result_expr = self.expr.aggregate(agg_specs, by_column_ids, dropna=dropna)
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
                column_labels=["size"],
                index_labels=names,
            ),
            output_col_ids,
        )

    def select_column(self, id: str) -> Block:
        return self.select_columns([id])

    def select_columns(self, ids: typing.Sequence[str]) -> Block:
        # Allow renames as may end up selecting same columns multiple times
        expr = self._expr.select_columns(
            [*self.index_columns, *ids], allow_renames=True
        )
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
        aggregations: typing.Sequence[ex.Aggregation] = (),
        column_labels: Optional[pd.Index] = None,
        *,
        dropna: bool = True,
    ) -> typing.Tuple[Block, typing.Sequence[str]]:
        """
        Apply aggregations to the block.
        Arguments:
            by_column_id: column id of the aggregation key, this is preserved through the transform and used as index.
            aggregations: input_column_id, operation tuples
            dropna: whether null keys should be dropped
        """
        if column_labels is None:
            column_labels = pd.Index(range(len(aggregations)))

        agg_specs = [
            (
                aggregation,
                guid.generate_guid(),
            )
            for aggregation in aggregations
        ]
        output_col_ids = [agg_spec[1] for agg_spec in agg_specs]
        result_expr = self.expr.aggregate(agg_specs, by_column_ids, dropna=dropna)

        names: typing.List[Label] = []
        if len(by_column_ids) == 0:
            result_expr, label_id = result_expr.create_constant(0, pd.Int64Dtype())
            index_columns = (label_id,)
            names = [None]
        else:
            index_columns = tuple(by_column_ids)  # type: ignore
            for by_col_id in by_column_ids:
                if by_col_id in self.value_columns:
                    names.append(self.col_id_to_label[by_col_id])
                else:
                    names.append(self.col_id_to_index_name[by_col_id])

        return (
            Block(
                result_expr,
                index_columns=index_columns,
                column_labels=column_labels,
                index_labels=names,
            ),
            output_col_ids,
        )

    def get_stat(
        self,
        column_id: str,
        stat: typing.Union[agg_ops.UnaryAggregateOp, agg_ops.NullaryAggregateOp],
    ):
        """Gets aggregates immediately, and caches it"""
        if stat.name in self._stats_cache[column_id]:
            return self._stats_cache[column_id][stat.name]

        # TODO: Convert nonstandard stats into standard stats where possible (popvar, etc.)
        # if getting a standard stat, just go get the rest of them
        standard_stats = typing.cast(
            typing.Sequence[
                typing.Union[agg_ops.UnaryAggregateOp, agg_ops.NullaryAggregateOp]
            ],
            self._standard_stats(column_id),
        )
        stats_to_fetch = standard_stats if stat in standard_stats else [stat]

        aggregations = [
            (
                ex.UnaryAggregation(stat, ex.deref(column_id))
                if isinstance(stat, agg_ops.UnaryAggregateOp)
                else ex.NullaryAggregation(stat),
                stat.name,
            )
            for stat in stats_to_fetch
        ]
        expr = self.expr.aggregate(aggregations)
        expr, offset_index_id = expr.promote_offsets()
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
                    stat, ex.deref(column_id_left), ex.deref(column_id_right)
                ),
                f"{stat.name}_{column_id_left}{column_id_right}",
            )
        ]
        expr = self.expr.aggregate(aggregations)
        expr, offset_index_id = expr.promote_offsets()
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
        stats: typing.Sequence[
            typing.Union[agg_ops.UnaryAggregateOp, agg_ops.NullaryAggregateOp]
        ],
    ):
        """Get a list of stats as a deferred block object."""
        labels = pd.Index([stat.name for stat in stats])
        aggregations = [
            (
                ex.UnaryAggregation(stat, ex.deref(col_id))
                if isinstance(stat, agg_ops.UnaryAggregateOp)
                else ex.NullaryAggregation(stat),
                f"{col_id}-{stat.name}",
            )
            for stat in stats
            for col_id in column_ids
        ]
        columns = [
            (tuple(f"{col_id}-{stat.name}" for stat in stats)) for col_id in column_ids
        ]
        expr, (index_cols, _, _) = unpivot(
            self.expr.aggregate(aggregations),
            labels,
            unpivot_columns=tuple(columns),
        )
        return Block(
            expr,
            column_labels=self._get_labels_for_columns(column_ids),
            index_columns=index_cols,
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
            expr = expr.drop_columns(self.index_columns)
            expr, new_index_ids = expr.promote_offsets()
            return Block(
                expr,
                column_labels=self.column_labels,
                # Initiates default index creation using the block constructor.
                index_columns=[new_index_ids],
            )
        else:
            return Block(
                expr,
                column_labels=self.column_labels,
                index_columns=self.index_columns,
                index_labels=self._index_labels,
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
        if bigframes.dtypes.is_orderable(dtype):
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

    def grouped_head(
        self,
        by_column_ids: typing.Sequence[str],
        value_columns: typing.Sequence[str],
        n: int,
    ):
        window_spec = windows.cumulative_rows(grouping_keys=tuple(by_column_ids))

        block, result_id = self.apply_window_op(
            value_columns[0],
            agg_ops.count_op,
            window_spec=window_spec,
        )

        cond = ops.lt_op.as_expr(result_id, ex.const(n + 1))
        block, cond_id = block.project_expr(cond)
        block = block.filter_by_id(cond_id)
        if value_columns:
            return block.select_columns(value_columns)

    def slice(
        self,
        start: typing.Optional[int] = None,
        stop: typing.Optional[int] = None,
        step: int = 1,
    ) -> Block:
        if step == 0:
            raise ValueError("Slice step size must be non-zero")
        return Block(
            self.expr.slice(start, stop, step),
            index_columns=self.index_columns,
            column_labels=self.column_labels,
            index_labels=self._index_labels,
        )

    # Using cache to optimize for Jupyter Notebook's behavior where both '__repr__'
    # and '__repr_html__' are called in a single display action, reducing redundant
    # queries.
    @functools.cache
    def retrieve_repr_request_results(
        self, max_results: int
    ) -> Tuple[pd.DataFrame, int, Optional[bigquery.QueryJob]]:
        """
        Retrieves a pandas dataframe containing only max_results many rows for use
        with printing methods.

        Returns a tuple of the dataframe and the overall number of rows of the query.
        """

        # head caches full underlying expression, so row_count will be free after
        executor = self.session._executor
        executor.cached(
            array_value=self.expr,
            config=executors.CacheConfig(optimize_for="head", if_cached="reuse-strict"),
        )
        head_result = self.session._executor.execute(
            self.expr.slice(start=None, stop=max_results, step=None)
        )
        row_count = self.session._executor.execute(self.expr.row_count()).to_py_scalar()

        head_df = head_result.to_pandas()
        self._copy_index_to_pandas(head_df)
        return head_df, row_count, head_result.query_job

    def promote_offsets(self, label: Label = None) -> typing.Tuple[Block, str]:
        expr, result_id = self._expr.promote_offsets()
        return (
            Block(
                expr,
                index_columns=self.index_columns,
                column_labels=self.column_labels.insert(len(self.column_labels), label),
                index_labels=self._index_labels,
            ),
            result_id,
        )

    def add_prefix(self, prefix: str, axis: str | int | None = None) -> Block:
        axis_number = utils.get_axis_number("rows" if (axis is None) else axis)
        if axis_number == 0:
            expr = self._expr
            new_index_cols = []
            for index_col in self._index_columns:
                expr, new_col = expr.project_to_id(
                    expression=ops.add_op.as_expr(
                        ex.const(prefix),
                        ops.AsTypeOp(to_type=bigframes.dtypes.STRING_DTYPE).as_expr(
                            index_col
                        ),
                    ),
                )
                new_index_cols.append(new_col)
            expr = expr.select_columns((*new_index_cols, *self.value_columns))

            return Block(
                expr,
                index_columns=new_index_cols,
                column_labels=self.column_labels,
                index_labels=self.index.names,
            )
        if axis_number == 1:
            return self.rename(columns=lambda label: f"{prefix}{label}")

    def add_suffix(self, suffix: str, axis: str | int | None = None) -> Block:
        axis_number = utils.get_axis_number("rows" if (axis is None) else axis)
        if axis_number == 0:
            expr = self._expr
            new_index_cols = []
            for index_col in self._index_columns:
                expr, new_col = expr.project_to_id(
                    expression=ops.add_op.as_expr(
                        ops.AsTypeOp(to_type=bigframes.dtypes.STRING_DTYPE).as_expr(
                            index_col
                        ),
                        ex.const(suffix),
                    ),
                )
                new_index_cols.append(new_col)
            expr = expr.select_columns((*new_index_cols, *self.value_columns))
            return Block(
                expr,
                index_columns=new_index_cols,
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
        aggregations = [
            ex.UnaryAggregation(agg_ops.AnyValueOp(), ex.deref(col_id))
            for col_id in column_ids
        ]
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

        if col_labels is None:
            result_index: pd.Index = pd.Index([None])
            result_col_labels: Sequence[Tuple] = list([()])
        elif (col_labels.nlevels == 1) and all(
            col_labels.isna()
        ):  # isna not implemented for MultiIndex for newer pandas versions
            result_index = pd.Index([None])
            result_col_labels = utils.index_as_tuples(col_labels.drop_duplicates())
        else:
            result_index = col_labels.drop_duplicates().dropna(how="all")
            result_col_labels = utils.index_as_tuples(result_index)

        # Get matching columns
        unpivot_columns: List[Tuple[Optional[str], ...]] = []
        for val in result_col_labels:
            input_columns, _ = self._create_stack_column(val, row_labels)
            unpivot_columns.append(input_columns)

        unpivot_expr, (added_index_columns, _, passthrough_cols) = unpivot(
            self._expr,
            row_labels=row_labels,
            passthrough_columns=self.index_columns,
            unpivot_columns=unpivot_columns,
            join_side=how,
        )
        new_index_level_names = self.column_labels.names[-levels:]
        if how == "left":
            index_columns = [*passthrough_cols, *added_index_columns]
            index_labels = [*self._index_labels, *new_index_level_names]
        else:
            index_columns = [*added_index_columns, *passthrough_cols]
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
        *,
        create_offsets_index: bool = True,
    ):
        """
        Unpivot columns to produce longer, narrower dataframe.
        Arguments correspond to pandas.melt arguments.
        """
        # TODO: Implement col_level and ignore_index
        value_labels: pd.Index = pd.Index(
            [self.col_id_to_label[col_id] for col_id in value_vars]
        )
        id_labels = [self.col_id_to_label[col_id] for col_id in id_vars]

        unpivot_expr, (var_col_ids, unpivot_out, passthrough_cols) = unpivot(
            self._expr,
            row_labels=value_labels,
            passthrough_columns=id_vars,
            unpivot_columns=(tuple(value_vars),),  # single unpivot col
            join_side="right",
        )

        if create_offsets_index:
            unpivot_expr, index_id = unpivot_expr.promote_offsets()
            index_cols = [index_id]
        else:
            index_cols = []

        # Need to reorder to get id_vars before var_col and unpivot_col
        unpivot_expr = unpivot_expr.select_columns(
            [*index_cols, *passthrough_cols, *var_col_ids, *unpivot_out]
        )

        return Block(
            unpivot_expr,
            column_labels=[*id_labels, *var_names, value_name],
            index_columns=index_cols,
        )

    def transpose(
        self,
        *,
        original_row_index: Optional[pd.Index] = None,
        single_row_mode: bool = False,
    ) -> Block:
        """Transpose the block. Will fail if dtypes aren't coercible to a common type or too many rows.
        Can provide the original_row_index directly if it is already known, otherwise a query is needed.
        """
        if self._transpose_cache is not None:
            return self._transpose_cache.with_transpose_cache(self)

        original_col_index = self.column_labels
        original_row_index = (
            original_row_index
            if original_row_index is not None
            else self.index.to_pandas(ordered=True)[0]
        )
        original_row_count = len(original_row_index)
        if original_row_count > bigframes.constants.MAX_COLUMNS:
            raise NotImplementedError(
                f"Object has {original_row_count} rows and is too large to transpose."
            )

        # Add row numbers to both axes to disambiguate, clean them up later
        block = self
        numbered_block = block.with_column_labels(
            utils.combine_indices(
                block.column_labels, pd.Index(range(len(block.column_labels)))
            )
        )
        # TODO: Determine if single row from expression tree (after aggregation without groupby)
        if single_row_mode:
            numbered_block, offsets = numbered_block.create_constant(0)
        else:
            numbered_block, offsets = numbered_block.promote_offsets()

        stacked_block = numbered_block.melt(
            id_vars=(offsets,),
            var_names=(
                *[name for name in original_col_index.names],
                "col_offset",
            ),
            value_vars=block.value_columns,
            create_offsets_index=False,
        )
        row_offset = stacked_block.value_columns[0]
        col_labels = stacked_block.value_columns[-2 - original_col_index.nlevels : -2]
        col_offset = stacked_block.value_columns[-2]  # disambiguator we created earlier
        cell_values = stacked_block.value_columns[-1]
        # Groupby source column
        stacked_block = stacked_block.set_index(
            [*col_labels, col_offset]
        )  # col index is now row index
        result = stacked_block.pivot(
            columns=[row_offset],
            values=[cell_values],
            columns_unique_values=tuple(range(original_row_count)),
        )
        # Drop the offsets from both axes before returning
        return (
            result.with_column_labels(original_row_index)
            .order_by([ordering.ascending_over(result.index_columns[-1])])
            .drop_levels([result.index_columns[-1]])
            .with_transpose_cache(self)
        )

    def _generate_sequence(
        self,
        start,
        stop,
        step: int = 1,
    ):
        range_expr = self.expr.from_range(
            start,
            stop,
            step,
        )

        return Block(
            range_expr,
            column_labels=["min"],
            index_columns=[],
        )

    def _generate_resample_label(
        self,
        rule: str,
        closed: Optional[Literal["right", "left"]] = None,
        label: Optional[Literal["right", "left"]] = None,
        on: Optional[Label] = None,
        level: typing.Union[LevelType, typing.Sequence[LevelType]] = None,
        origin: Union[
            Union[pd.Timestamp, datetime.datetime, numpy.datetime64, int, float, str],
            Literal["epoch", "start", "start_day", "end", "end_day"],
        ] = "start_day",
    ) -> Block:
        # Validate and resolve the index or column to use for grouping
        if on is None:
            if len(self.index_columns) == 0:
                raise ValueError(
                    f"No index for resampling. Expected {bigframes.dtypes.DATETIME_DTYPE} or "
                    f"{bigframes.dtypes.TIMESTAMP_DTYPE} index or 'on' parameter specifying a column."
                )
            if len(self.index_columns) > 1 and (level is None):
                raise ValueError(
                    "Multiple indices are not supported for this operation"
                    " when 'level' is not set."
                )
            level = level or 0
            col_id = self.index.resolve_level(level)[0]
            # Reset index to make the resampling level a column, then drop all other index columns.
            # This simplifies processing by focusing solely on the column required for resampling.
            block = self.reset_index(drop=False)
            block = block.drop_columns(
                [col for col in self.index.column_ids if col != col_id]
            )
        elif level is not None:
            raise ValueError("The Grouper cannot specify both a key and a level!")
        else:
            matches = self.label_to_col_id.get(on, [])
            if len(matches) > 1:
                raise ValueError(
                    f"Multiple columns matching id {on} were found. {constants.FEEDBACK_LINK}"
                )
            if len(matches) == 0:
                raise KeyError(f"The grouper name {on} is not found")

            col_id = matches[0]
            block = self
        if level is None:
            dtype = self._column_type(col_id)
        elif isinstance(level, int):
            dtype = self.index.dtypes[level]
        else:
            dtype = self.index.dtypes[self.index.names.index(level)]

        if dtype not in (
            bigframes.dtypes.DATETIME_DTYPE,
            bigframes.dtypes.TIMESTAMP_DTYPE,
        ):
            raise TypeError(
                f"Invalid column type: {dtype}. Expected types are "
                f"{bigframes.dtypes.DATETIME_DTYPE}, or "
                f"{bigframes.dtypes.TIMESTAMP_DTYPE}."
            )

        freq = pd.tseries.frequencies.to_offset(rule)
        assert freq is not None

        if origin not in ("epoch", "start", "start_day"):
            raise ValueError(
                "'origin' should be equal to 'epoch', 'start' or 'start_day'"
                f". Got '{origin}' instead."
            )

        agg_specs = [
            (
                ex.UnaryAggregation(agg_ops.min_op, ex.deref(col_id)),
                guid.generate_guid(),
            ),
        ]
        origin_block = Block(
            block.expr.aggregate(agg_specs, dropna=True),
            column_labels=["origin"],
            index_columns=[],
        )

        col_level = block.value_columns.index(col_id)

        block = block.merge(
            origin_block, how="cross", left_join_ids=[], right_join_ids=[], sort=True
        )

        # After merging, the original column ids are altered. 'col_level' is the index of
        # the datetime column used for resampling. 'block.value_columns[-1]' is the
        # 'origin' column, which is the minimum datetime value.
        block, label_col_id = block.apply_binary_op(
            block.value_columns[col_level],
            block.value_columns[-1],
            op=ops.DatetimeToIntegerLabelOp(freq=freq, closed=closed, origin=origin),
        )
        block = block.drop_columns([block.value_columns[-2]])

        # Generate integer label sequence.
        min_agg_specs = [
            (
                ex.UnaryAggregation(agg_ops.min_op, ex.deref(label_col_id)),
                guid.generate_guid(),
            ),
        ]
        max_agg_specs = [
            (
                ex.UnaryAggregation(agg_ops.max_op, ex.deref(label_col_id)),
                guid.generate_guid(),
            ),
        ]
        label_start = block.expr.aggregate(min_agg_specs, dropna=True)
        label_stop = block.expr.aggregate(max_agg_specs, dropna=True)

        label_block = block._generate_sequence(
            start=label_start,
            stop=label_stop,
        )

        label_block = label_block.merge(
            origin_block, how="cross", left_join_ids=[], right_join_ids=[], sort=True
        )

        block = label_block.merge(
            block,
            how="left",
            left_join_ids=[label_block.value_columns[0]],
            right_join_ids=[label_col_id],
            sort=True,
        )

        block, resample_label_id = block.apply_binary_op(
            block.value_columns[0],
            block.value_columns[1],
            op=ops.IntegerLabelToDatetimeOp(freq=freq, label=label, origin=origin),
        )

        # After multiple merges, the columns:
        # - block.value_columns[0] is the integer label sequence,
        # - block.value_columns[1] is the origin column (minimum datetime value),
        # - col_level+2 represents the datetime column used for resampling,
        # - block.value_columns[-2] is the integer label column derived from the datetime column.
        # These columns are no longer needed.
        block = block.drop_columns(
            [
                block.value_columns[0],
                block.value_columns[1],
                block.value_columns[col_level + 2],
                block.value_columns[-2],
            ]
        )

        return block.set_index([resample_label_id])

    def _create_stack_column(self, col_label: typing.Tuple, stack_labels: pd.Index):
        input_dtypes = []
        input_columns: list[Optional[str]] = []
        for uvalue in utils.index_as_tuples(stack_labels):
            label_to_match = (*col_label, *uvalue)
            label_to_match = (
                label_to_match[0] if len(label_to_match) == 1 else label_to_match
            )
            matching_ids = self.label_to_col_id.get(label_to_match, [])
            input_id = matching_ids[0] if len(matching_ids) > 0 else None
            if input_id:
                input_dtypes.append(self._column_type(input_id))
            input_columns.append(input_id)
            # Input column i is the first one that
        if len(input_dtypes) > 0:
            output_dtype = bigframes.dtypes.lcd_type(*input_dtypes)
            if output_dtype is None:
                raise NotImplementedError(
                    "Cannot stack columns with non-matching dtypes."
                )
        else:
            output_dtype = pd.Float64Dtype()
        return tuple(input_columns), output_dtype

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

    def isin(self, other: Block):
        # TODO: Support multiple other columns and match on label
        assert len(other.value_columns) == 1
        unique_other_values = other.expr.select_columns(
            [other.value_columns[0]]
        ).aggregate((), by_column_ids=(other.value_columns[0],), dropna=False)
        block = self
        # for each original column, join with other
        for i in range(len(self.value_columns)):
            block = block._isin_inner(block.value_columns[i], unique_other_values)
        return block

    def _isin_inner(self: Block, col: str, unique_values: core.ArrayValue) -> Block:
        expr, matches = self._expr.isin(unique_values, col, unique_values.column_ids[0])

        new_value_cols = tuple(
            val_col if val_col != col else matches for val_col in self.value_columns
        )
        expr = expr.select_columns((*self.index_columns, *new_value_cols))
        return Block(
            expr,
            index_columns=self.index_columns,
            column_labels=self.column_labels,
            index_labels=self._index_labels,
        )

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
        conditions = tuple(
            (lid, rid) for lid, rid in zip(left_join_ids, right_join_ids)
        )
        joined_expr, (get_column_left, get_column_right) = self.expr.relational_join(
            other.expr, type=how, conditions=conditions
        )
        result_columns = []
        matching_join_labels = []

        left_post_join_ids = tuple(get_column_left[id] for id in left_join_ids)
        right_post_join_ids = tuple(get_column_right[id] for id in right_join_ids)

        joined_expr, coalesced_ids = coalesce_columns(
            joined_expr, left_post_join_ids, right_post_join_ids, how=how, drop=False
        )

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
                if other.col_id_to_label[col_id] in matching_join_labels:
                    pass
                else:
                    result_columns.append(get_column_right[col_id])
            else:
                result_columns.append(get_column_right[col_id])

        if sort:
            # sort uses coalesced join keys always
            joined_expr = joined_expr.order_by(
                [
                    ordering.OrderingExpression(ex.deref(col_id))
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

        # Construct a default index only if this object and the other both have
        # indexes. In other words, joining anything to a NULL index object
        # keeps everything as a NULL index.
        #
        # This keeps us from generating an index if the user joins a large
        # BigQuery table against small local data, for example.
        if (
            self.index.is_null
            or other.index.is_null
            or self.session._default_index_type == bigframes.enums.DefaultIndexKind.NULL
        ):
            expr = joined_expr
            index_columns = []
        else:
            expr, offset_index_id = joined_expr.promote_offsets()
            index_columns = [offset_index_id]

        return Block(expr, index_columns=index_columns, column_labels=labels)

    def _align_both_axes(
        self, other: Block, how: str
    ) -> Tuple[Block, pd.Index, Sequence[Tuple[ex.RefOrConstant, ex.RefOrConstant]]]:
        # Join rows
        aligned_block, (get_column_left, get_column_right) = self.join(other, how=how)
        # join columns schema
        # indexers will be none for exact match
        if self.column_labels.equals(other.column_labels):
            columns, lcol_indexer, rcol_indexer = self.column_labels, None, None
        else:
            columns, lcol_indexer, rcol_indexer = self.column_labels.join(
                other.column_labels, how=how, return_indexers=True
            )
        lcol_indexer = (
            lcol_indexer if (lcol_indexer is not None) else range(len(columns))
        )
        rcol_indexer = (
            rcol_indexer if (rcol_indexer is not None) else range(len(columns))
        )

        left_input_lookup = (
            lambda index: ex.deref(get_column_left[self.value_columns[index]])
            if index != -1
            else ex.const(None)
        )
        righ_input_lookup = (
            lambda index: ex.deref(get_column_right[other.value_columns[index]])
            if index != -1
            else ex.const(None)
        )

        left_inputs = [left_input_lookup(i) for i in lcol_indexer]
        right_inputs = [righ_input_lookup(i) for i in rcol_indexer]
        return aligned_block, columns, tuple(zip(left_inputs, right_inputs))  # type: ignore

    def _align_axis_0(
        self, other: Block, how: str
    ) -> Tuple[Block, pd.Index, Sequence[Tuple[ex.DerefOp, ex.DerefOp]]]:
        assert len(other.value_columns) == 1
        aligned_block, (get_column_left, get_column_right) = self.join(other, how=how)

        series_column_id = other.value_columns[0]
        inputs = tuple(
            (
                ex.deref(get_column_left[col]),
                ex.deref(get_column_right[series_column_id]),
            )
            for col in self.value_columns
        )
        return aligned_block, self.column_labels, inputs

    def _align_series_block_axis_1(
        self, other: Block, how: str
    ) -> Tuple[Block, pd.Index, Sequence[Tuple[ex.RefOrConstant, ex.RefOrConstant]]]:
        assert len(other.value_columns) == 1
        if other._transpose_cache is None:
            raise ValueError(
                "Wrong align method, this approach requires transpose cache"
            )

        # Join rows
        aligned_block, (get_column_left, get_column_right) = join_with_single_row(
            self, other.transpose()
        )
        # join columns schema
        # indexers will be none for exact match
        if self.column_labels.equals(other.transpose().column_labels):
            columns, lcol_indexer, rcol_indexer = self.column_labels, None, None
        else:
            columns, lcol_indexer, rcol_indexer = self.column_labels.join(
                other.transpose().column_labels, how=how, return_indexers=True
            )
        lcol_indexer = (
            lcol_indexer if (lcol_indexer is not None) else range(len(columns))
        )
        rcol_indexer = (
            rcol_indexer if (rcol_indexer is not None) else range(len(columns))
        )

        left_input_lookup = (
            lambda index: ex.deref(get_column_left[self.value_columns[index]])
            if index != -1
            else ex.const(None)
        )
        righ_input_lookup = (
            lambda index: ex.deref(
                get_column_right[other.transpose().value_columns[index]]
            )
            if index != -1
            else ex.const(None)
        )

        left_inputs = [left_input_lookup(i) for i in lcol_indexer]
        right_inputs = [righ_input_lookup(i) for i in rcol_indexer]
        return aligned_block, columns, tuple(zip(left_inputs, right_inputs))  # type: ignore

    def _align_pd_series_axis_1(
        self, other: pd.Series, how: str
    ) -> Tuple[Block, pd.Index, Sequence[Tuple[ex.RefOrConstant, ex.RefOrConstant]]]:
        if self.column_labels.equals(other.index):
            columns, lcol_indexer, rcol_indexer = self.column_labels, None, None
        else:
            if not (self.column_labels.is_unique and other.index.is_unique):
                raise ValueError("Cannot align non-unique indices")
            columns, lcol_indexer, rcol_indexer = self.column_labels.join(
                other.index, how=how, return_indexers=True
            )
        lcol_indexer = (
            lcol_indexer if (lcol_indexer is not None) else range(len(columns))
        )
        rcol_indexer = (
            rcol_indexer if (rcol_indexer is not None) else range(len(columns))
        )

        left_input_lookup = (
            lambda index: ex.deref(self.value_columns[index])
            if index != -1
            else ex.const(None)
        )
        righ_input_lookup = (
            lambda index: ex.const(other.iloc[index]) if index != -1 else ex.const(None)
        )

        left_inputs = [left_input_lookup(i) for i in lcol_indexer]
        right_inputs = [righ_input_lookup(i) for i in rcol_indexer]
        return self, columns, tuple(zip(left_inputs, right_inputs))  # type: ignore

    def _apply_binop(
        self,
        op: ops.BinaryOp,
        inputs: Sequence[Tuple[ex.Expression, ex.Expression]],
        labels: pd.Index,
        reverse: bool = False,
    ) -> Block:
        exprs = []
        for left_input, right_input in inputs:
            exprs.append(
                op.as_expr(right_input, left_input)
                if reverse
                else op.as_expr(left_input, right_input)
            )

        return self.project_exprs(exprs, labels=labels, drop=True)

    # TODO: Re-implement join in terms of merge (requires also adding remaining merge args)
    def join(
        self,
        other: Block,
        *,
        how="left",
        sort: bool = False,
        block_identity_join: bool = False,
        always_order: bool = False,
    ) -> Tuple[Block, Tuple[Mapping[str, str], Mapping[str, str]],]:
        """
        Join two blocks objects together, and provide mappings between source columns and output columns.

        Args:
            other (Block):
                The right operand of the join operation
            how (str):
                Describes the join type. 'inner', 'outer', 'left', or 'right'
            sort (bool):
                if true will sort result by index
            block_identity_join (bool):
                If true, will not convert join to a projection (implicitly assuming unique indices)
            always_order (bool):
                If true, will always preserve input ordering, even if ordering mode is partial

        Returns:
            Block, (left_mapping, right_mapping): Result block and mappers from input column ids to result column ids.
        """

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
        # Handle null index, which only supports row join
        # This is the canonical way of aligning on null index, so always allow (ignore block_identity_join)
        if self.index.nlevels == other.index.nlevels == 0:
            result = try_legacy_row_join(self, other, how=how) or try_new_row_join(
                self, other
            )
            if result is not None:
                return result
            raise bigframes.exceptions.NullIndexError(
                "Cannot implicitly align objects. Set an explicit index using set_index."
            )

        # Oddly, pandas row-wise join ignores right index names
        if (
            not block_identity_join
            and (self.index.nlevels == other.index.nlevels)
            and (self.index.dtypes == other.index.dtypes)
        ):
            result = try_legacy_row_join(self, other, how=how) or try_new_row_join(
                self, other
            )
            if result is not None:
                return result

        self._throw_if_null_index("join")
        other._throw_if_null_index("join")
        if self.index.nlevels == other.index.nlevels == 1:
            return join_mono_indexed(
                self, other, how=how, sort=sort, propogate_order=always_order
            )
        else:  # Handles cases where one or both sides are multi-indexed
            # Always sort mult-index join
            return join_multi_indexed(
                self, other, how=how, sort=sort, propogate_order=always_order
            )

    def is_monotonic_increasing(
        self, column_id: typing.Union[str, Sequence[str]]
    ) -> bool:
        return self._is_monotonic(column_id, increasing=True)

    def is_monotonic_decreasing(
        self, column_id: typing.Union[str, Sequence[str]]
    ) -> bool:
        return self._is_monotonic(column_id, increasing=False)

    def _array_value_for_output(
        self, *, include_index: bool
    ) -> Tuple[bigframes.core.ArrayValue, list[str], list[Label]]:
        """
        Creates the expression tree with user-visible column names, such as for
        SQL output.

        Args:
            include_index (bool):
                whether to include index columns.

        Returns:
            a tuple of (ArrayValue, index_column_id_list, index_column_label_list).
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

        return (
            array_value.rename_columns(substitutions),
            new_ids[: len(idx_labels)],
            idx_labels,
        )

    def to_sql_query(
        self, include_index: bool, enable_cache: bool = True
    ) -> Tuple[str, list[str], list[Label]]:
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
        array_value, idx_ids, idx_labels = self._array_value_for_output(
            include_index=include_index
        )

        # Note: this uses the sql from the executor, so is coupled tightly to execution
        # implementaton. It will reference cached tables instead of original data sources.
        # Maybe should just compile raw BFET? Depends on user intent.
        sql = self.session._executor.to_sql(array_value, enable_cache=enable_cache)
        return (
            sql,
            idx_ids,
            idx_labels,
        )

    def to_placeholder_table(
        self, include_index: bool, *, dry_run: bool = False
    ) -> bigquery.TableReference:
        """
        Creates a temporary BigQuery VIEW (or empty table if dry_run) with the
        SQL corresponding to this block.
        """
        if self._view_ref is not None:
            return self._view_ref

        # Prefer the real view if it exists, but since dry_run might be called
        # many times before the real query, we cache that empty table reference
        # with the correct schema too.
        if dry_run:
            if self._view_ref_dry_run is not None:
                return self._view_ref_dry_run

            # Create empty temp table with the right schema.
            array_value, _, _ = self._array_value_for_output(
                include_index=include_index
            )
            temp_table_schema = array_value.schema.to_bigquery()
            self._view_ref_dry_run = self.session._create_temp_table(
                schema=temp_table_schema
            )
            return self._view_ref_dry_run

        # We shouldn't run `to_sql_query` if we have a `dry_run`, because it
        # could cause us to make unnecessary API calls to upload local node
        # data.
        sql, _, _ = self.to_sql_query(include_index=include_index)
        self._view_ref = self.session._create_temp_view(sql)
        return self._view_ref

    def cached(self, *, force: bool = False, session_aware: bool = False) -> None:
        """Write the block to a session table."""
        # use a heuristic for whether something needs to be cached
        self.session._executor.cached(
            self.expr,
            config=executors.CacheConfig(
                optimize_for="auto"
                if session_aware
                else executors.HierarchicalKey(tuple(self.index_columns)),
                if_cached="replace" if force else "reuse-any",
            ),
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
        window_spec = windows.rows()

        # any NaN value means not monotonic
        block, last_notna_id = self.apply_unary_op(column_ids[0], ops.notnull_op)
        for column_id in column_ids[1:]:
            block, notna_id = block.apply_unary_op(column_id, ops.notnull_op)
            old_last_notna_id = last_notna_id
            block, last_notna_id = block.apply_binary_op(
                old_last_notna_id, notna_id, ops.and_op
            )
            block.drop_columns([notna_id, old_last_notna_id])

        # loop over all columns to check monotonicity
        last_result_id = None
        for column_id in column_ids[::-1]:
            block, lag_result_id = block.apply_window_op(
                column_id, agg_ops.ShiftOp(period), window_spec
            )
            block, strict_monotonic_id = block.apply_binary_op(
                column_id, lag_result_id, ops.gt_op if increasing else ops.lt_op
            )
            block, equal_id = block.apply_binary_op(column_id, lag_result_id, ops.eq_op)
            block = block.drop_columns([lag_result_id])
            if last_result_id is None:
                block, last_result_id = block.apply_binary_op(
                    equal_id, strict_monotonic_id, ops.or_op
                )
                block = block.drop_columns([equal_id, strict_monotonic_id])
            else:
                block, equal_monotonic_id = block.apply_binary_op(
                    equal_id, last_result_id, ops.and_op
                )
                block = block.drop_columns([equal_id, last_result_id])
                block, last_result_id = block.apply_binary_op(
                    equal_monotonic_id, strict_monotonic_id, ops.or_op
                )
                block = block.drop_columns([equal_monotonic_id, strict_monotonic_id])

        block, monotonic_result_id = block.apply_binary_op(
            last_result_id, last_notna_id, ops.and_op  # type: ignore
        )
        if last_result_id is not None:
            block = block.drop_columns([last_result_id, last_notna_id])
        result = block.get_stat(monotonic_result_id, agg_ops.all_op)
        self._stats_cache[column_name].update({op_name: result})
        return result

    def _throw_if_null_index(self, opname: str):
        if len(self.index_columns) == 0:
            raise bigframes.exceptions.NullIndexError(
                f"Cannot do {opname} without an index. Set an index using set_index."
            )

    def _get_rows_as_json_values(self) -> Block:
        # We want to preserve any ordering currently present before turning to
        # direct SQL manipulation. We will restore the ordering when we rebuild
        # expression.
        # TODO(shobs): Replace direct SQL manipulation by structured expression
        # manipulation
        expr, ordering_column_name = self.expr.promote_offsets()
        expr_sql = self.session._executor.to_sql(expr)

        # Names of the columns to serialize for the row.
        # We will use the repr-eval pattern to serialize a value here and
        # deserialize in the cloud function. Let's make sure that would work.
        column_names = []
        for col in list(self.index_columns) + [col for col in self.column_labels]:
            serialized_column_name = repr(col)
            try:
                ast.literal_eval(serialized_column_name)
            except Exception:
                raise NameError(
                    f"Column name type '{type(col).__name__}' is not supported for row serialization."
                    " Please consider using a name for which literal_eval(repr(name)) works."
                )

            column_names.append(serialized_column_name)
        column_names_csv = sql.csv(map(sql.simple_literal, column_names))

        # index columns count
        index_columns_count = len(self.index_columns)

        # column references to form the array of values for the row
        column_types = list(self.index.dtypes) + list(self.dtypes)
        column_references = []
        for type_, col in zip(column_types, self.expr.column_ids):
            if isinstance(type_, pd.ArrowDtype) and pa.types.is_binary(
                type_.pyarrow_dtype
            ):
                column_references.append(sql.to_json_string(col))
            else:
                column_references.append(sql.cast_as_string(col))

        column_references_csv = sql.csv(column_references)

        # types of the columns to serialize for the row
        column_types_csv = sql.csv(
            [sql.simple_literal(str(typ)) for typ in column_types]
        )

        # row dtype to use for deserializing the row as pandas series
        pandas_row_dtype = bigframes.dtypes.lcd_type(*column_types)
        if pandas_row_dtype is None:
            pandas_row_dtype = "object"
        pandas_row_dtype = sql.simple_literal(str(pandas_row_dtype))

        # create a json column representing row through SQL manipulation
        row_json_column_name = guid.generate_guid()
        select_columns = (
            [ordering_column_name] + list(self.index_columns) + [row_json_column_name]
        )
        select_columns_csv = sql.csv(
            [googlesql.identifier(col) for col in select_columns]
        )
        json_sql = f"""\
With T0 AS (
{textwrap.indent(expr_sql, "    ")}
),
T1 AS (
    SELECT *,
           TO_JSON_STRING(JSON_OBJECT(
               "names", [{column_names_csv}],
               "types", [{column_types_csv}],
               "values", [{column_references_csv}],
               "indexlength", {index_columns_count},
               "dtype", {pandas_row_dtype}
           )) AS {googlesql.identifier(row_json_column_name)} FROM T0
)
SELECT {select_columns_csv} FROM T1
"""
        # The only ways this code is used is through df.apply(axis=1) cope path
        destination, query_job = self.session._loader._query_to_destination(
            json_sql, cluster_candidates=[ordering_column_name]
        )
        if not destination:
            raise ValueError(f"Query job {query_job} did not produce result table")

        new_schema = (
            self.expr.schema.select([*self.index_columns])
            .append(
                bf_schema.SchemaItem(
                    row_json_column_name, bigframes.dtypes.STRING_DTYPE
                )
            )
            .append(
                bf_schema.SchemaItem(ordering_column_name, bigframes.dtypes.INT_DTYPE)
            )
        )

        dest_table = self.session.bqclient.get_table(destination)
        expr = core.ArrayValue.from_table(
            dest_table,
            schema=new_schema,
            session=self.session,
            offsets_col=ordering_column_name,
            n_rows=dest_table.num_rows,
        ).drop_columns([ordering_column_name])
        block = Block(
            expr,
            index_columns=self.index_columns,
            column_labels=[row_json_column_name],
            index_labels=self._index_labels,
        )
        return block


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
    def session(self) -> session.Session:
        return self._expr.session

    @property
    def column_ids(self) -> Sequence[str]:
        """Column(s) to use as row labels."""
        return self._block._index_columns

    @property
    def is_null(self) -> bool:
        return len(self._block._index_columns) == 0

    def to_pandas(
        self,
        *,
        ordered: Optional[bool] = None,
        allow_large_results: Optional[bool] = None,
    ) -> Tuple[pd.Index, Optional[bigquery.QueryJob]]:
        """Executes deferred operations and downloads the results."""
        if len(self.column_ids) == 0:
            raise bigframes.exceptions.NullIndexError(
                "Cannot materialize index, as this object does not have an index. Set index column(s) using set_index."
            )
        ordered = ordered if ordered is not None else True

        df, query_job = self._block.select_columns([]).to_pandas(
            ordered=ordered,
            allow_large_results=allow_large_results,
        )
        return df.index, query_job

    def _compute_dry_run(
        self, *, ordered: bool = True
    ) -> Tuple[pd.Series, bigquery.QueryJob]:
        return self._block.select_columns([])._compute_dry_run(ordered=ordered)

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


def try_new_row_join(
    left: Block, right: Block
) -> Optional[Tuple[Block, Tuple[Mapping[str, str], Mapping[str, str]],]]:
    join_keys = tuple(
        (left_id, right_id)
        for left_id, right_id in zip(left.index_columns, right.index_columns)
    )
    join_result = left.expr.try_row_join(right.expr, join_keys)
    if join_result is None:  # did not succeed
        return None
    combined_expr, (get_column_left, get_column_right) = join_result
    # Keep the left index column, and drop the matching right column
    index_cols_post_join = [get_column_left[id] for id in left.index_columns]
    combined_expr = combined_expr.drop_columns(
        [get_column_right[id] for id in right.index_columns]
    )
    block = Block(
        combined_expr,
        index_columns=index_cols_post_join,
        column_labels=left.column_labels.append(right.column_labels),
        index_labels=left.index.names,
    )
    return (
        block,
        (get_column_left, get_column_right),
    )


def try_legacy_row_join(
    left: Block,
    right: Block,
    *,
    how="left",
) -> Optional[Tuple[Block, Tuple[Mapping[str, str], Mapping[str, str]],]]:
    """Joins two blocks that have a common root expression by merging the projections."""
    left_expr = left.expr
    right_expr = right.expr
    # Create a new array value, mapping from both, then left, and then right
    join_keys = tuple(
        join_defs.CoalescedColumnMapping(
            left_source_id=left_id,
            right_source_id=right_id,
            destination_id=guid.generate_guid(),
        )
        for left_id, right_id in zip(left.index_columns, right.index_columns)
    )
    left_mappings = [
        join_defs.JoinColumnMapping(
            source_table=join_defs.JoinSide.LEFT,
            source_id=id,
            destination_id=guid.generate_guid(),
        )
        for id in left.value_columns
    ]
    right_mappings = [
        join_defs.JoinColumnMapping(
            source_table=join_defs.JoinSide.RIGHT,
            source_id=id,
            destination_id=guid.generate_guid(),
        )
        for id in right.value_columns
    ]
    combined_expr = left_expr.try_legacy_row_join(
        right_expr,
        join_type=how,
        join_keys=join_keys,
        mappings=(*left_mappings, *right_mappings),
    )
    if combined_expr is None:
        return None
    get_column_left = {m.source_id: m.destination_id for m in left_mappings}
    get_column_right = {m.source_id: m.destination_id for m in right_mappings}
    block = Block(
        combined_expr,
        column_labels=[*left.column_labels, *right.column_labels],
        index_columns=(key.destination_id for key in join_keys),
        index_labels=left.index.names,
    )
    return (
        block,
        (get_column_left, get_column_right),
    )


def join_with_single_row(
    left: Block,
    single_row_block: Block,
) -> Tuple[Block, Tuple[Mapping[str, str], Mapping[str, str]],]:
    """
    Special join case where other is a single row block.
    This property is not validated, caller responsible for not passing multi-row block.
    Preserves index of the left block, ignoring label of other.
    """
    left_expr = left.expr
    # ignore index columns by dropping them
    right_expr = single_row_block.expr.select_columns(single_row_block.value_columns)
    combined_expr, (get_column_left, get_column_right) = left_expr.relational_join(
        right_expr,
        type="cross",
    )
    # Drop original indices from each side. and used the coalesced combination generated by the join.
    index_cols_post_join = [get_column_left[id] for id in left.index_columns]

    block = Block(
        combined_expr,
        index_columns=index_cols_post_join,
        column_labels=left.column_labels.append(single_row_block.column_labels),
        index_labels=left.index.names,
    )
    return (
        block,
        (get_column_left, get_column_right),
    )


def join_mono_indexed(
    left: Block,
    right: Block,
    *,
    how="left",
    sort: bool = False,
    propogate_order: bool = False,
) -> Tuple[Block, Tuple[Mapping[str, str], Mapping[str, str]],]:
    left_expr = left.expr
    right_expr = right.expr

    combined_expr, (get_column_left, get_column_right) = left_expr.relational_join(
        right_expr,
        type=how,
        conditions=(
            join_defs.JoinCondition(left.index_columns[0], right.index_columns[0]),
        ),
        propogate_order=propogate_order,
    )

    left_index = get_column_left[left.index_columns[0]]
    right_index = get_column_right[right.index_columns[0]]
    # Drop original indices from each side. and used the coalesced combination generated by the join.
    combined_expr, coalesced_join_cols = coalesce_columns(
        combined_expr, [left_index], [right_index], how=how
    )
    if sort:
        combined_expr = combined_expr.order_by(
            [
                ordering.OrderingExpression(ex.deref(col_id))
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
    sort: bool = False,
    propogate_order: bool = False,
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

    left_expr = left.expr
    right_expr = right.expr

    combined_expr, (get_column_left, get_column_right) = left_expr.relational_join(
        right_expr,
        type=how,
        conditions=tuple(
            join_defs.JoinCondition(left, right)
            for left, right in zip(left_join_ids, right_join_ids)
        ),
        propogate_order=propogate_order,
    )

    left_ids_post_join = [get_column_left[id] for id in left_join_ids]
    right_ids_post_join = [get_column_right[id] for id in right_join_ids]
    # Drop original indices from each side. and used the coalesced combination generated by the join.
    combined_expr, coalesced_join_cols = coalesce_columns(
        combined_expr, left_ids_post_join, right_ids_post_join, how=how
    )
    if sort:
        combined_expr = combined_expr.order_by(
            [
                ordering.OrderingExpression(ex.deref(col_id))
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


# TODO: Rewrite just to return expressions
def coalesce_columns(
    expr: core.ArrayValue,
    left_ids: typing.Sequence[str],
    right_ids: typing.Sequence[str],
    how: str,
    drop: bool = True,
) -> Tuple[core.ArrayValue, Sequence[str]]:
    result_ids = []
    for left_id, right_id in zip(left_ids, right_ids):
        if how == "left" or how == "inner" or how == "cross":
            result_ids.append(left_id)
            if drop:
                expr = expr.drop_columns([right_id])
        elif how == "right":
            result_ids.append(right_id)
            if drop:
                expr = expr.drop_columns([left_id])
        elif how == "outer":
            coalesced_id = guid.generate_guid()
            expr, coalesced_id = expr.project_to_id(
                ops.coalesce_op.as_expr(left_id, right_id)
            )
            if drop:
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


## Unpivot helpers
def unpivot(
    array_value: core.ArrayValue,
    row_labels: pd.Index,
    unpivot_columns: Sequence[Tuple[Optional[str], ...]],
    *,
    passthrough_columns: typing.Sequence[str] = (),
    join_side: Literal["left", "right"] = "left",
) -> Tuple[core.ArrayValue, Tuple[Tuple[str, ...], Tuple[str, ...], Tuple[str, ...]]]:
    """
    Unpivot ArrayValue columns.

    Args:
        row_labels: Identifies the source of the row. Must be equal to length to source column list in unpivot_columns argument.
        unpivot_columns: Sequence of column ids tuples. Each tuple of columns will be combined into a single output column
        passthrough_columns: Columns that will not be unpivoted. Column id will be preserved.
        index_col_id (str): The column id to be used for the row labels.

    Returns:
        ArrayValue, (index_cols, unpivot_cols, passthrough_cols): The unpivoted ArrayValue and resulting column ids.
    """
    # There will be N labels, used to disambiguate which of N source columns produced each output row
    labels_array = _pd_index_to_array_value(
        session=array_value.session, index=row_labels
    )

    # Unpivot creates N output rows for each input row, labels disambiguate these N rows
    # Join_side is necessary to produce desired row ordering
    if join_side == "left":
        joined_array, (column_mapping, labels_mapping) = array_value.relational_join(
            labels_array, type="cross"
        )
    else:
        joined_array, (labels_mapping, column_mapping) = labels_array.relational_join(
            array_value, type="cross"
        )
    new_passthrough_cols = [column_mapping[col] for col in passthrough_columns]
    # Last column is offsets
    index_col_ids = [labels_mapping[col] for col in labels_array.column_ids[:-1]]
    explode_offsets_id = labels_mapping[labels_array.column_ids[-1]]

    # Build the output rows as a case statment that selects between the N input columns
    unpivot_exprs: List[ex.Expression] = []
    # Supports producing multiple stacked ouput columns for stacking only part of hierarchical index
    for input_ids in unpivot_columns:
        # row explode offset used to choose the input column
        # we use offset instead of label as labels are not necessarily unique
        cases = itertools.chain(
            *(
                (
                    ops.eq_op.as_expr(explode_offsets_id, ex.const(i)),
                    ex.deref(column_mapping[id_or_null])
                    if (id_or_null is not None)
                    else ex.const(None),
                )
                for i, id_or_null in enumerate(input_ids)
            )
        )
        col_expr = ops.case_when_op.as_expr(*cases)
        unpivot_exprs.append(col_expr)

    joined_array, unpivot_col_ids = joined_array.compute_values(unpivot_exprs)

    return joined_array.select_columns(
        [*index_col_ids, *unpivot_col_ids, *new_passthrough_cols]
    ), (tuple(index_col_ids), tuple(unpivot_col_ids), tuple(new_passthrough_cols))


def _pd_index_to_array_value(
    session: session.Session,
    index: pd.Index,
) -> core.ArrayValue:
    """
    Create an ArrayValue from a list of label tuples.
    The last column will be row offsets.
    """
    rows = []
    labels_as_tuples = utils.index_as_tuples(index)
    for row_offset in range(len(index)):
        id_gen = bigframes.core.identifiers.standard_id_strings()
        row_label = labels_as_tuples[row_offset]
        row_label = (row_label,) if not isinstance(row_label, tuple) else row_label
        row = {}
        for label_part, id in zip(row_label, id_gen):
            row[id] = label_part if pd.notnull(label_part) else None
        row[next(id_gen)] = row_offset
        rows.append(row)

    return core.ArrayValue.from_pyarrow(pa.Table.from_pylist(rows), session=session)
