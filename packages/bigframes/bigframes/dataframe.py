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

"""DataFrame is a two dimensional data structure."""

from __future__ import annotations

import datetime
import inspect
import itertools
import json
import re
import sys
import textwrap
import typing
from typing import (
    Callable,
    Dict,
    Hashable,
    Iterable,
    List,
    Literal,
    Mapping,
    Optional,
    overload,
    Sequence,
    Tuple,
    Union,
)
import warnings

import bigframes_vendored.constants as constants
import bigframes_vendored.pandas.core.frame as vendored_pandas_frame
import bigframes_vendored.pandas.pandas._typing as vendored_pandas_typing
import google.api_core.exceptions
import google.cloud.bigquery as bigquery
import numpy
import pandas
from pandas.api import extensions as pd_ext
import pandas.io.formats.format
import pyarrow
import tabulate

import bigframes._config.display_options as display_options
import bigframes.constants
import bigframes.core
from bigframes.core import log_adapter
import bigframes.core.block_transforms as block_ops
import bigframes.core.blocks as blocks
import bigframes.core.convert
import bigframes.core.explode
import bigframes.core.expression as ex
import bigframes.core.groupby as groupby
import bigframes.core.guid
import bigframes.core.indexers as indexers
import bigframes.core.indexes as indexes
import bigframes.core.ordering as order
import bigframes.core.utils as utils
import bigframes.core.validations as validations
import bigframes.core.window
from bigframes.core.window import rolling
import bigframes.core.window_spec as windows
import bigframes.dtypes
import bigframes.exceptions as bfe
import bigframes.formatting_helpers as formatter
import bigframes.functions
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops
import bigframes.operations.ai
import bigframes.operations.plotting as plotting
import bigframes.operations.semantics
import bigframes.operations.structs
import bigframes.series
import bigframes.session._io.bigquery

if typing.TYPE_CHECKING:
    from _typeshed import SupportsRichComparison

    import bigframes.session

    SingleItemValue = Union[bigframes.series.Series, int, float, str, Callable]

LevelType = typing.Hashable
LevelsType = typing.Union[LevelType, typing.Sequence[LevelType]]

ERROR_IO_ONLY_GS_PATHS = f"Only Google Cloud Storage (gs://...) paths are supported. {constants.FEEDBACK_LINK}"
ERROR_IO_REQUIRES_WILDCARD = (
    "Google Cloud Storage path must contain a wildcard '*' character. See: "
    "https://cloud.google.com/bigquery/docs/reference/standard-sql/other-statements#export_data_statement"
    f"{constants.FEEDBACK_LINK}"
)


# Inherits from pandas DataFrame so that we can use the same docstrings.
@log_adapter.class_logger
class DataFrame(vendored_pandas_frame.DataFrame):
    __doc__ = vendored_pandas_frame.DataFrame.__doc__
    # internal flag to disable cache at all
    _disable_cache_override: bool = False
    # Must be above 5000 for pandas to delegate to bigframes for binops
    __pandas_priority__ = 15000

    def __init__(
        self,
        data=None,
        index: vendored_pandas_typing.Axes | None = None,
        columns: vendored_pandas_typing.Axes | None = None,
        dtype: typing.Optional[
            bigframes.dtypes.DtypeString | bigframes.dtypes.Dtype
        ] = None,
        copy: typing.Optional[bool] = None,
        *,
        session: typing.Optional[bigframes.session.Session] = None,
    ):
        global bigframes

        self._query_job: Optional[bigquery.QueryJob] = None

        if copy is not None and not copy:
            raise ValueError(
                f"DataFrame constructor only supports copy=True. {constants.FEEDBACK_LINK}"
            )
        # Ignore object dtype if provided, as it provides no additional
        # information about what BigQuery type to use.
        if dtype is not None and bigframes.dtypes.is_object_like(dtype):
            dtype = None

        # Check to see if constructing from BigQuery-backed objects before
        # falling back to pandas constructor
        block = None
        if isinstance(data, blocks.Block):
            block = data

        elif isinstance(data, DataFrame):
            block = data._get_block()

        # Dict of Series
        elif (
            utils.is_dict_like(data)
            and len(data) >= 1
            and any(
                isinstance(data[key], bigframes.series.Series) for key in data.keys()
            )
        ):
            if not all(
                isinstance(data[key], bigframes.series.Series) for key in data.keys()
            ):
                # TODO(tbergeron): Support local list/series data by converting to memtable.
                raise NotImplementedError(
                    f"Cannot mix Series with other types. {constants.FEEDBACK_LINK}"
                )
            keys = list(data.keys())
            first_label, first_series = keys[0], data[keys[0]]
            block = (
                typing.cast(bigframes.series.Series, first_series)
                ._get_block()
                .with_column_labels([first_label])
            )

            for key in keys[1:]:
                other = typing.cast(bigframes.series.Series, data[key])
                other_block = other._block.with_column_labels([key])
                # Pandas will keep original sorting if all indices are aligned.
                # We cannot detect this easily however, and so always sort on index
                block, _ = block.join(  # type:ignore
                    other_block, how="outer", sort=True
                )

        if block:
            if index is not None:
                bf_index = indexes.Index(index)
                idx_block = bf_index._block
                idx_cols = idx_block.index_columns
                block, (_, r_mapping) = block.reset_index().join(
                    bf_index._block.reset_index(), how="inner"
                )
                block = block.set_index([r_mapping[idx_col] for idx_col in idx_cols])
            if columns:
                column_ids = [
                    block.resolve_label_exact_or_error(label) for label in list(columns)
                ]
                block = block.select_columns(column_ids)  # type:ignore
            if dtype:
                bf_dtype = bigframes.dtypes.bigframes_type(dtype)
                block = block.multi_apply_unary_op(ops.AsTypeOp(to_type=bf_dtype))

        else:
            import bigframes.pandas

            pd_dataframe = pandas.DataFrame(
                data=data,
                index=index,  # type:ignore
                columns=columns,  # type:ignore
                dtype=dtype,  # type:ignore
            )
            if session:
                block = session.read_pandas(pd_dataframe)._get_block()
            else:
                block = bigframes.pandas.read_pandas(pd_dataframe)._get_block()

        # We use _block as an indicator in __getattr__ and __setattr__ to see
        # if the object is fully initialized, so make sure we set the _block
        # attribute last.
        self._block = block
        self._block.session._register_object(self)

    def __dir__(self):
        return dir(type(self)) + [
            label
            for label in self._block.column_labels
            if label and isinstance(label, str)
        ]

    def _ipython_key_completions_(self) -> List[str]:
        return list(
            [
                label
                for label in self._block.column_labels
                if label and isinstance(label, str)
            ]
        )

    def _find_indices(
        self,
        columns: Union[blocks.Label, Sequence[blocks.Label]],
        tolerance: bool = False,
    ) -> Sequence[int]:
        """Find corresponding indices in df._block.column_labels for column name(s).
        Order is kept the same as input names order.

        Args:
            columns: column name(s)
            tolerance: True to pass through columns not found. False to raise
                ValueError.
        """
        col_ids = self._sql_names(columns, tolerance)
        return [self._block.value_columns.index(col_id) for col_id in col_ids]

    def _resolve_label_exact(self, label) -> Optional[str]:
        return self._block.resolve_label_exact(label)

    def _sql_names(
        self,
        columns: Union[blocks.Label, Sequence[blocks.Label], pandas.Index],
        tolerance: bool = False,
    ) -> Sequence[str]:
        """Retrieve sql name (column name in BQ schema) of column(s)."""
        labels = (
            columns
            if utils.is_list_like(columns) and not isinstance(columns, tuple)
            else [columns]
        )  # type:ignore
        results: Sequence[str] = []
        for label in labels:
            col_ids = self._block.label_to_col_id.get(label, [])
            if not tolerance and len(col_ids) == 0:
                raise ValueError(f"Column name {label} doesn't exist")
            results = (*results, *col_ids)
        return results

    @property
    @validations.requires_index
    def index(
        self,
    ) -> indexes.Index:
        return indexes.Index.from_frame(self)

    @index.setter
    def index(self, value):
        # TODO: Handle assigning MultiIndex
        result = self._assign_single_item("_new_bf_index", value).set_index(
            "_new_bf_index"
        )
        self._set_block(result._get_block())
        self.index.name = value.name if hasattr(value, "name") else None

    @property
    @validations.requires_index
    def loc(self) -> indexers.LocDataFrameIndexer:
        return indexers.LocDataFrameIndexer(self)

    @property
    @validations.requires_ordering()
    def iloc(self) -> indexers.ILocDataFrameIndexer:
        return indexers.ILocDataFrameIndexer(self)

    @property
    @validations.requires_ordering()
    def iat(self) -> indexers.IatDataFrameIndexer:
        return indexers.IatDataFrameIndexer(self)

    @property
    @validations.requires_index
    def at(self) -> indexers.AtDataFrameIndexer:
        return indexers.AtDataFrameIndexer(self)

    @property
    def dtypes(self) -> pandas.Series:
        return pandas.Series(data=self._block.dtypes, index=self._block.column_labels)

    @property
    def columns(self) -> pandas.Index:
        return self.dtypes.index

    @columns.setter
    def columns(self, labels: pandas.Index):
        new_block = self._block.with_column_labels(labels)
        self._set_block(new_block)

    @property
    def shape(self) -> Tuple[int, int]:
        return self._block.shape

    @property
    def size(self) -> int:
        rows, cols = self.shape
        return rows * cols

    @property
    def ndim(self) -> int:
        return 2

    @property
    def empty(self) -> bool:
        return self.size == 0

    @property
    def values(self) -> numpy.ndarray:
        return self.to_numpy()

    @property
    def bqclient(self) -> bigframes.Session:
        """BigQuery REST API Client the DataFrame uses for operations."""
        return self._session.bqclient

    @property
    def _session(self) -> bigframes.Session:
        return self._get_block().expr.session

    @property
    def _has_index(self) -> bool:
        return len(self._block.index_columns) > 0

    @property
    @validations.requires_ordering()
    def T(self) -> DataFrame:
        return DataFrame(self._get_block().transpose())

    @validations.requires_index
    @validations.requires_ordering()
    def transpose(self) -> DataFrame:
        return self.T

    def __len__(self):
        rows, _ = self.shape
        return rows

    __len__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__len__)

    def __iter__(self):
        return iter(self.columns)

    def astype(
        self,
        dtype: Union[
            bigframes.dtypes.DtypeString,
            bigframes.dtypes.Dtype,
            type,
            dict[str, Union[bigframes.dtypes.DtypeString, bigframes.dtypes.Dtype]],
        ],
        *,
        errors: Literal["raise", "null"] = "raise",
    ) -> DataFrame:
        if errors not in ["raise", "null"]:
            raise ValueError("Arg 'error' must be one of 'raise' or 'null'")

        safe_cast = errors == "null"

        if isinstance(dtype, dict):
            result = self.copy()
            for col, to_type in dtype.items():
                result[col] = result[col].astype(to_type)
            return result

        dtype = bigframes.dtypes.bigframes_type(dtype)

        return self._apply_unary_op(ops.AsTypeOp(dtype, safe_cast))

    def _should_sql_have_index(self) -> bool:
        """Should the SQL we pass to BQML and other I/O include the index?"""

        return self._has_index and (
            self.index.name is not None or len(self.index.names) > 1
        )

    def _to_placeholder_table(self, dry_run: bool = False) -> bigquery.TableReference:
        """Compiles this DataFrame's expression tree to SQL and saves it to a
        (temporary) view or table (in the case of a dry run).
        """
        return self._block.to_placeholder_table(
            include_index=self._should_sql_have_index(), dry_run=dry_run
        )

    def _to_sql_query(
        self, include_index: bool, enable_cache: bool = True
    ) -> Tuple[str, list[str], list[blocks.Label]]:
        """Compiles this DataFrame's expression tree to SQL, optionally
        including index columns.

        Args:
            include_index (bool):
                whether to include index columns.

        Returns:
            Tuple[sql_string, index_column_id_list, index_column_label_list]:
                If include_index is set to False, index_column_id_list and index_column_label_list
                return empty lists.
        """
        return self._block.to_sql_query(include_index, enable_cache=enable_cache)

    @property
    def sql(self) -> str:
        """Compiles this DataFrame's expression tree to SQL.

        Returns:
            str:
                string representing the compiled SQL.
        """
        try:
            include_index = self._should_sql_have_index()
            sql, _, _ = self._to_sql_query(include_index=include_index)
            return sql
        except AttributeError as e:
            # Workaround for a development-mode debugging issue:
            # An `AttributeError` originating *inside* this @property getter (e.g., due to
            # a typo or referencing a non-existent attribute) can be mistakenly intercepted
            # by the class's __getattr__ method if one is defined.
            # We catch the AttributeError and raise SyntaxError instead to make it clear
            # the error originates *here* in the property implementation.
            # See: https://stackoverflow.com/questions/50542177/correct-handling-of-attributeerror-in-getattr-when-using-property
            raise SyntaxError(
                "AttributeError encountered. Please check the implementation for incorrect attribute access."
            ) from e

    @property
    def query_job(self) -> Optional[bigquery.QueryJob]:
        """BigQuery job metadata for the most recent query.

        Returns:
            None or google.cloud.bigquery.QueryJob:
                The most recent `QueryJob
                <https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob>`_.
        """
        if self._query_job is None:
            self._set_internal_query_job(self._compute_dry_run())
        return self._query_job

    def memory_usage(self, index: bool = True):
        n_rows, _ = self.shape
        # like pandas, treat all variable-size objects as just 8-byte pointers, ignoring actual object
        column_sizes = self.dtypes.map(
            lambda dtype: bigframes.dtypes.DTYPE_BYTE_SIZES.get(dtype, 8) * n_rows
        )
        if index and self._has_index:
            index_size = pandas.Series([self.index._memory_usage()], index=["Index"])
            column_sizes = pandas.concat([index_size, column_sizes])
        return column_sizes

    @validations.requires_index
    def info(
        self,
        verbose: Optional[bool] = None,
        buf=None,
        max_cols: Optional[int] = None,
        memory_usage: Optional[bool] = None,
        show_counts: Optional[bool] = None,
    ):
        obuf = buf or sys.stdout

        n_rows, n_columns = self.shape

        max_cols = (
            max_cols
            if max_cols is not None
            else bigframes.options.display.max_info_columns
        )

        show_all_columns = verbose if verbose is not None else (n_columns < max_cols)

        obuf.write(f"{type(self)}\n")

        index_type = "MultiIndex" if self.index.nlevels > 1 else "Index"

        # These accessses are kind of expensive, maybe should try to skip?
        first_indice = self.index[0]
        last_indice = self.index[-1]
        obuf.write(f"{index_type}: {n_rows} entries, {first_indice} to {last_indice}\n")

        dtype_strings = self.dtypes.astype("string")
        if show_all_columns:
            obuf.write(f"Data columns (total {n_columns} columns):\n")
            column_info = self.columns.to_frame(name="Column")

            max_rows = bigframes.options.display.max_info_rows
            too_many_rows = n_rows > max_rows if max_rows is not None else False

            if show_counts if show_counts is not None else (not too_many_rows):
                non_null_counts = self.count().to_pandas()
                column_info["Non-Null Count"] = non_null_counts.map(
                    lambda x: f"{int(x)} non-null"
                )

            column_info["Dtype"] = dtype_strings

            column_info = column_info.reset_index(drop=True)
            column_info.index.name = "#"

            column_info_formatted = tabulate.tabulate(column_info, headers="keys")  # type: ignore
            obuf.write(column_info_formatted)
            obuf.write("\n")

        else:  # Just number of columns and first, last
            obuf.write(
                f"Columns: {n_columns} entries, {self.columns[0]} to {self.columns[-1]}\n"
            )
        dtype_counts = dtype_strings.value_counts().sort_index(ascending=True).items()
        dtype_counts_formatted = ", ".join(
            f"{dtype}({count})" for dtype, count in dtype_counts
        )
        obuf.write(f"dtypes: {dtype_counts_formatted}\n")

        show_memory = (
            memory_usage
            if memory_usage is not None
            else bigframes.options.display.memory_usage
        )
        if show_memory:
            # TODO: Convert to different units (kb, mb, etc.)
            obuf.write(f"memory usage: {self.memory_usage().sum()} bytes\n")

    def select_dtypes(self, include=None, exclude=None) -> DataFrame:
        # Create empty pandas dataframe with same schema and then leverage actual pandas implementation
        as_pandas = pandas.DataFrame(
            {
                col_id: pandas.Series([], dtype=dtype)
                for col_id, dtype in zip(self._block.value_columns, self._block.dtypes)
            }
        )
        selected_columns = tuple(
            as_pandas.select_dtypes(include=include, exclude=exclude).columns
        )
        return DataFrame(self._block.select_columns(selected_columns))

    def _set_internal_query_job(self, query_job: Optional[bigquery.QueryJob]):
        self._query_job = query_job

    def __getitem__(
        self,
        key: Union[
            blocks.Label,
            Sequence[blocks.Label],
            # Index of column labels can be treated the same as a sequence of column labels.
            pandas.Index,
            bigframes.series.Series,
        ],
    ):  # No return type annotations (like pandas) as type cannot always be determined statically
        # NOTE: This implements the operations described in
        # https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html

        if isinstance(key, bigframes.series.Series):
            return self._getitem_bool_series(key)

        if isinstance(key, slice):
            return self.iloc[key]

        if isinstance(key, typing.Hashable):
            return self._getitem_label(key)
        # Select a subset of columns or re-order columns.
        # In Ibis after you apply a projection, any column objects from the
        # table before the projection can't be combined with column objects
        # from the table after the projection. This is because the table after
        # a projection is considered a totally separate table expression.
        #
        # This is unexpected behavior for a pandas user, who expects their old
        # Series objects to still work with the new / mutated DataFrame. We
        # avoid applying a projection in Ibis until it's absolutely necessary
        # to provide pandas-like semantics.
        # TODO(swast): Do we need to apply implicit join when doing a
        # projection?

        # Select a number of columns as DF.
        key = key if utils.is_list_like(key) else [key]  # type:ignore

        selected_ids: Tuple[str, ...] = ()
        for label in key:
            col_ids = self._block.label_to_col_id[label]
            selected_ids = (*selected_ids, *col_ids)

        return DataFrame(self._block.select_columns(selected_ids))

    __getitem__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__getitem__)

    def _getitem_label(self, key: blocks.Label):
        col_ids = self._block.cols_matching_label(key)
        if len(col_ids) == 0:
            raise KeyError(
                f"{key} not found in DataFrame columns: {self._block.column_labels}"
            )
        block = self._block.select_columns(col_ids)
        if isinstance(self.columns, pandas.MultiIndex):
            # Multiindex should drop-level if not selecting entire
            key_levels = len(key) if isinstance(key, tuple) else 1
            index_levels = self.columns.nlevels
            if key_levels < index_levels:
                block = block.with_column_labels(
                    block.column_labels.droplevel(list(range(key_levels)))
                )
                # Force return DataFrame in this case, even if only single column
                return DataFrame(block)

        if len(col_ids) == 1:
            return bigframes.series.Series(block)
        return DataFrame(block)

    # Bool Series selects rows
    def _getitem_bool_series(self, key: bigframes.series.Series) -> DataFrame:
        if not key.dtype == pandas.BooleanDtype():
            raise NotImplementedError(
                f"Only boolean series currently supported for indexing. {constants.FEEDBACK_LINK}"
            )
            # TODO: enforce stricter alignment
        combined_index, (
            get_column_left,
            get_column_right,
        ) = self._block.join(key._block, how="left")
        block = combined_index
        filter_col_id = get_column_right[key._value_column]
        block = block.filter_by_id(filter_col_id)
        block = block.drop_columns([filter_col_id])
        return DataFrame(block)

    def __getattr__(self, key: str):
        # To allow subclasses to set private attributes before the class is
        # fully initialized, protect against recursion errors with
        # uninitialized DataFrame objects. Note: this comes at the downside
        # that columns with a leading `_` won't be treated as columns.
        #
        # See:
        # https://github.com/googleapis/python-bigquery-dataframes/issues/728
        # and
        # https://nedbatchelder.com/blog/201010/surprising_getattr_recursion.html
        if key == "_block":
            raise AttributeError(key)

        if key in self._block.column_labels:
            return self.__getitem__(key)

        if hasattr(pandas.DataFrame, key):
            log_adapter.submit_pandas_labels(
                self._block.expr.session.bqclient, self.__class__.__name__, key
            )
            raise AttributeError(
                textwrap.dedent(
                    f"""
                    BigQuery DataFrames has not yet implemented an equivalent to
                    'pandas.DataFrame.{key}'. {constants.FEEDBACK_LINK}
                    """
                )
            )
        raise AttributeError(key)

    def __setattr__(self, key: str, value):
        if key == "_block":
            object.__setattr__(self, key, value)
            return

        # To allow subclasses to set private attributes before the class is
        # fully initialized, assume anything set before `_block` is initialized
        # is a regular attribute.
        if not hasattr(self, "_block"):
            object.__setattr__(self, key, value)
            return

        # If someone has a column named the same as a normal attribute
        # (e.g. index), we want to set the normal attribute, not the column.
        # To do that, check if there is a normal attribute by using
        # __getattribute__ (not __getattr__, because that includes columns).
        # If that returns a value without raising, then we know this is a
        # normal attribute and we should prefer that.
        try:
            object.__getattribute__(self, key)
            return object.__setattr__(self, key, value)
        except AttributeError:
            pass

        # If we made it here, then we know that it's not a regular attribute
        # already, so it might be a column to update. Note: we don't allow
        # adding new columns using __setattr__, only __setitem__, that way we
        # can still add regular new attributes.
        if key in self._block.column_labels:
            self[key] = value
        else:
            object.__setattr__(self, key, value)

    def __repr__(self) -> str:
        """Converts a DataFrame to a string. Calls to_pandas.

        Only represents the first `bigframes.options.display.max_rows`.
        """
        # Protect against errors with uninitialized DataFrame. See:
        # https://github.com/googleapis/python-bigquery-dataframes/issues/728
        if not hasattr(self, "_block"):
            return object.__repr__(self)

        opts = bigframes.options.display
        max_results = opts.max_rows
        # anywdiget mode uses the same display logic as the "deferred" mode
        # for faster execution
        if opts.repr_mode in ("deferred", "anywidget"):
            return formatter.repr_query_job(self._compute_dry_run())

        # TODO(swast): pass max_columns and get the true column count back. Maybe
        # get 1 more column than we have requested so that pandas can add the
        # ... for us?
        pandas_df, row_count, query_job = self._block.retrieve_repr_request_results(
            max_results
        )

        self._set_internal_query_job(query_job)

        column_count = len(pandas_df.columns)

        with display_options.pandas_repr(opts):
            import pandas.io.formats

            # safe to mutate this, this dict is owned by this code, and does not affect global config
            to_string_kwargs = (
                pandas.io.formats.format.get_dataframe_repr_params()  # type: ignore
            )
            if not self._has_index:
                to_string_kwargs.update({"index": False})
            repr_string = pandas_df.to_string(**to_string_kwargs)

        # Modify the end of the string to reflect count.
        lines = repr_string.split("\n")
        pattern = re.compile("\\[[0-9]+ rows x [0-9]+ columns\\]")
        if pattern.match(lines[-1]):
            lines = lines[:-2]

        if row_count > len(lines) - 1:
            lines.append("...")

        lines.append("")
        lines.append(f"[{row_count} rows x {column_count} columns]")
        return "\n".join(lines)

    def _repr_html_(self) -> str:
        """
        Returns an html string primarily for use by notebooks for displaying
        a representation of the DataFrame. Displays 20 rows by default since
        many notebooks are not configured for large tables.
        """
        opts = bigframes.options.display
        max_results = opts.max_rows
        if opts.repr_mode == "deferred":
            return formatter.repr_query_job(self._compute_dry_run())

        if opts.repr_mode == "anywidget":
            import anywidget  # type: ignore

            # create an iterator for the data batches
            batches = self.to_pandas_batches()

            # get the first page result
            try:
                first_page = next(iter(batches))
            except StopIteration:
                first_page = pandas.DataFrame(columns=self.columns)

            # Instantiate and return the widget. The widget's frontend will
            # handle the display of the table and pagination
            return anywidget.AnyWidget(dataframe=first_page)

        self._cached()
        df = self.copy()
        if bigframes.options.display.blob_display:
            blob_cols = [
                series_name
                for series_name, series in df.items()
                if series.dtype == bigframes.dtypes.OBJ_REF_DTYPE
            ]
            for col in blob_cols:
                # TODO(garrettwu): Not necessary to get access urls for all the rows. Update when having a to get URLs from local data.
                df[col] = df[col].blob._get_runtime(mode="R", with_metadata=True)

        # TODO(swast): pass max_columns and get the true column count back. Maybe
        # get 1 more column than we have requested so that pandas can add the
        # ... for us?
        pandas_df, row_count, query_job = df._block.retrieve_repr_request_results(
            max_results
        )

        self._set_internal_query_job(query_job)

        column_count = len(pandas_df.columns)

        with display_options.pandas_repr(opts):
            # Allows to preview images in the DataFrame. The implementation changes the string repr as well, that it doesn't truncate strings or escape html charaters such as "<" and ">". We may need to implement a full-fledged repr module to better support types not in pandas.
            if bigframes.options.display.blob_display and blob_cols:

                def obj_ref_rt_to_html(obj_ref_rt) -> str:
                    obj_ref_rt_json = json.loads(obj_ref_rt)
                    obj_ref_details = obj_ref_rt_json["objectref"]["details"]
                    if "gcs_metadata" in obj_ref_details:
                        gcs_metadata = obj_ref_details["gcs_metadata"]
                        content_type = typing.cast(
                            str, gcs_metadata.get("content_type", "")
                        )
                        if content_type.startswith("image"):
                            size_str = ""
                            if bigframes.options.display.blob_display_width:
                                size_str = f' width="{bigframes.options.display.blob_display_width}"'
                            if bigframes.options.display.blob_display_height:
                                size_str = (
                                    size_str
                                    + f' height="{bigframes.options.display.blob_display_height}"'
                                )
                            url = obj_ref_rt_json["access_urls"]["read_url"]
                            return f'<img src="{url}"{size_str}>'

                    return f'uri: {obj_ref_rt_json["objectref"]["uri"]}, authorizer: {obj_ref_rt_json["objectref"]["authorizer"]}'

                formatters = {blob_col: obj_ref_rt_to_html for blob_col in blob_cols}

                # set max_colwidth so not to truncate the image url
                with pandas.option_context("display.max_colwidth", None):
                    max_rows = pandas.get_option("display.max_rows")
                    max_cols = pandas.get_option("display.max_columns")
                    show_dimensions = pandas.get_option("display.show_dimensions")
                    html_string = pandas_df.to_html(
                        escape=False,
                        notebook=True,
                        max_rows=max_rows,
                        max_cols=max_cols,
                        show_dimensions=show_dimensions,
                        formatters=formatters,  # type: ignore
                    )
            else:
                # _repr_html_ stub is missing so mypy thinks it's a Series. Ignore mypy.
                html_string = pandas_df._repr_html_()  # type:ignore

        html_string += f"[{row_count} rows x {column_count} columns in total]"
        return html_string

    def __delitem__(self, key: str):
        df = self.drop(columns=[key])
        self._set_block(df._get_block())

    def __setitem__(self, key: str, value: SingleItemValue):
        df = self._assign_single_item(key, value)
        self._set_block(df._get_block())

    __setitem__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__setitem__)

    def _apply_binop(
        self,
        other: float | int | bigframes.series.Series | DataFrame,
        op,
        axis: str | int = "columns",
        how: str = "outer",
        reverse: bool = False,
    ):
        if isinstance(other, bigframes.dtypes.LOCAL_SCALAR_TYPES):
            return self._apply_scalar_binop(other, op, reverse=reverse)
        elif isinstance(other, DataFrame):
            return self._apply_dataframe_binop(other, op, how=how, reverse=reverse)
        elif isinstance(other, pandas.DataFrame):
            return self._apply_dataframe_binop(
                DataFrame(other), op, how=how, reverse=reverse
            )
        elif utils.get_axis_number(axis) == 0:
            return self._apply_series_binop_axis_0(other, op, how, reverse)
        elif utils.get_axis_number(axis) == 1:
            return self._apply_series_binop_axis_1(other, op, how, reverse)
        raise NotImplementedError(
            f"binary operation is not implemented on the second operand of type {type(other).__name__}."
            f"{constants.FEEDBACK_LINK}"
        )

    def _apply_scalar_binop(
        self,
        other: bigframes.dtypes.LOCAL_SCALAR_TYPE,
        op: ops.BinaryOp,
        reverse: bool = False,
    ) -> DataFrame:
        if reverse:
            expr = op.as_expr(
                left_input=ex.const(other),
                right_input=ex.free_var("var1"),
            )
        else:
            expr = op.as_expr(
                left_input=ex.free_var("var1"),
                right_input=ex.const(other),
            )
        return DataFrame(self._block.multi_apply_unary_op(expr))

    def _apply_series_binop_axis_0(
        self,
        other,
        op: ops.BinaryOp,
        how: str = "outer",
        reverse: bool = False,
    ) -> DataFrame:
        bf_series = bigframes.core.convert.to_bf_series(
            other, self.index if self._has_index else None, self._session
        )
        aligned_block, columns, expr_pairs = self._block._align_axis_0(
            bf_series._block, how=how
        )
        result = aligned_block._apply_binop(
            op, inputs=expr_pairs, labels=columns, reverse=reverse
        )
        return DataFrame(result)

    def _apply_series_binop_axis_1(
        self,
        other,
        op: ops.BinaryOp,
        how: str = "outer",
        reverse: bool = False,
    ) -> DataFrame:
        """Align dataframe with pandas series by inlining series values as literals."""
        # If we already know the transposed schema (from the transpose cache), we don't need to materialize rows from other
        # Instead, can fully defer execution (as a cross-join)
        if (
            isinstance(other, bigframes.series.Series)
            and other._block._transpose_cache is not None
        ):
            aligned_block, columns, expr_pairs = self._block._align_series_block_axis_1(
                other._block, how=how
            )
        else:
            # Fallback path, materialize `other` locally
            pd_series = bigframes.core.convert.to_pd_series(other, self.columns)
            aligned_block, columns, expr_pairs = self._block._align_pd_series_axis_1(
                pd_series, how=how
            )
        result = aligned_block._apply_binop(
            op, inputs=expr_pairs, labels=columns, reverse=reverse
        )
        return DataFrame(result)

    def _apply_dataframe_binop(
        self,
        other: DataFrame,
        op: ops.BinaryOp,
        how: str = "outer",
        reverse: bool = False,
    ) -> DataFrame:
        aligned_block, columns, expr_pairs = self._block._align_both_axes(
            other._block, how=how
        )
        result = aligned_block._apply_binop(
            op, inputs=expr_pairs, labels=columns, reverse=reverse
        )
        return DataFrame(result)

    def eq(self, other: typing.Any, axis: str | int = "columns") -> DataFrame:
        return self._apply_binop(other, ops.eq_op, axis=axis)

    def __eq__(self, other) -> DataFrame:  # type: ignore
        return self.eq(other)

    __eq__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__eq__)

    def ne(self, other: typing.Any, axis: str | int = "columns") -> DataFrame:
        return self._apply_binop(other, ops.ne_op, axis=axis)

    def __ne__(self, other) -> DataFrame:  # type: ignore
        return self.ne(other)

    __ne__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__ne__)

    def __invert__(self) -> DataFrame:
        return self._apply_unary_op(ops.invert_op)

    __invert__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__invert__)

    def le(self, other: typing.Any, axis: str | int = "columns") -> DataFrame:
        return self._apply_binop(other, ops.le_op, axis=axis)

    def __le__(self, other) -> DataFrame:
        return self.le(other)

    __le__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__le__)

    def lt(self, other: typing.Any, axis: str | int = "columns") -> DataFrame:
        return self._apply_binop(other, ops.lt_op, axis=axis)

    def __lt__(self, other) -> DataFrame:
        return self.lt(other)

    __lt__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__lt__)

    def ge(self, other: typing.Any, axis: str | int = "columns") -> DataFrame:
        return self._apply_binop(other, ops.ge_op, axis=axis)

    def __ge__(self, other) -> DataFrame:
        return self.ge(other)

    __ge__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__ge__)

    def gt(self, other: typing.Any, axis: str | int = "columns") -> DataFrame:
        return self._apply_binop(other, ops.gt_op, axis=axis)

    def __gt__(self, other) -> DataFrame:
        return self.gt(other)

    __gt__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__gt__)

    def add(
        self,
        other: float | int | bigframes.series.Series | DataFrame,
        axis: str | int = "columns",
    ) -> DataFrame:
        # TODO(swast): Support fill_value parameter.
        # TODO(swast): Support level parameter with MultiIndex.
        return self._apply_binop(other, ops.add_op, axis=axis)

    def radd(
        self,
        other: float | int | bigframes.series.Series | DataFrame,
        axis: str | int = "columns",
    ) -> DataFrame:
        # TODO(swast): Support fill_value parameter.
        # TODO(swast): Support level parameter with MultiIndex.
        return self.add(other, axis=axis)

    def __add__(self, other) -> DataFrame:
        return self.add(other)

    __add__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__add__)

    __radd__ = __add__

    def sub(
        self,
        other: float | int | bigframes.series.Series | DataFrame,
        axis: str | int = "columns",
    ) -> DataFrame:
        return self._apply_binop(other, ops.sub_op, axis=axis)

    subtract = sub
    subtract.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.sub)

    def __sub__(self, other):
        return self.sub(other)

    __sub__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__sub__)

    def rsub(
        self,
        other: float | int | bigframes.series.Series | DataFrame,
        axis: str | int = "columns",
    ) -> DataFrame:
        return self._apply_binop(other, ops.sub_op, axis=axis, reverse=True)

    def __rsub__(self, other):
        return self.rsub(other)

    __rsub__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__rsub__)

    def mul(
        self,
        other: float | int | bigframes.series.Series | DataFrame,
        axis: str | int = "columns",
    ) -> DataFrame:
        return self._apply_binop(other, ops.mul_op, axis=axis)

    multiply = mul
    multiply.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.mul)

    def __mul__(self, other):
        return self.mul(other)

    __mul__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__mul__)

    def rmul(
        self,
        other: float | int | bigframes.series.Series | DataFrame,
        axis: str | int = "columns",
    ) -> DataFrame:
        return self.mul(other, axis=axis)

    def __rmul__(self, other):
        return self.rmul(other)

    __rmul__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__rmul__)

    def truediv(
        self,
        other: float | int | bigframes.series.Series | DataFrame,
        axis: str | int = "columns",
    ) -> DataFrame:
        return self._apply_binop(other, ops.div_op, axis=axis)

    truediv.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.truediv)
    div = divide = truediv

    def __truediv__(self, other):
        return self.truediv(other)

    __truediv__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__truediv__)

    def rtruediv(
        self,
        other: float | int | bigframes.series.Series | DataFrame,
        axis: str | int = "columns",
    ) -> DataFrame:
        return self._apply_binop(other, ops.div_op, axis=axis, reverse=True)

    rdiv = rtruediv
    rdiv.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.rtruediv)

    def __rtruediv__(self, other):
        return self.rtruediv(other)

    __rtruediv__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__rtruediv__)

    def floordiv(
        self,
        other: float | int | bigframes.series.Series | DataFrame,
        axis: str | int = "columns",
    ) -> DataFrame:
        return self._apply_binop(other, ops.floordiv_op, axis=axis)

    def __floordiv__(self, other):
        return self.floordiv(other)

    __floordiv__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__floordiv__)

    def rfloordiv(
        self,
        other: float | int | bigframes.series.Series | DataFrame,
        axis: str | int = "columns",
    ) -> DataFrame:
        return self._apply_binop(other, ops.floordiv_op, axis=axis, reverse=True)

    def __rfloordiv__(self, other):
        return self.rfloordiv(other)

    __rfloordiv__.__doc__ = inspect.getdoc(
        vendored_pandas_frame.DataFrame.__rfloordiv__
    )

    def mod(self, other: int | bigframes.series.Series | DataFrame, axis: str | int = "columns") -> DataFrame:  # type: ignore
        return self._apply_binop(other, ops.mod_op, axis=axis)

    def __mod__(self, other):
        return self.mod(other)

    __mod__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__mod__)

    def rmod(self, other: int | bigframes.series.Series | DataFrame, axis: str | int = "columns") -> DataFrame:  # type: ignore
        return self._apply_binop(other, ops.mod_op, axis=axis, reverse=True)

    def __rmod__(self, other):
        return self.rmod(other)

    __rmod__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__rmod__)

    def pow(
        self, other: int | bigframes.series.Series, axis: str | int = "columns"
    ) -> DataFrame:
        return self._apply_binop(other, ops.pow_op, axis=axis)

    def __pow__(self, other):
        return self.pow(other)

    __pow__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__pow__)

    def rpow(
        self, other: int | bigframes.series.Series, axis: str | int = "columns"
    ) -> DataFrame:
        return self._apply_binop(other, ops.pow_op, axis=axis, reverse=True)

    def __rpow__(self, other):
        return self.rpow(other)

    __rpow__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__rpow__)

    def __and__(self, other: bool | int | bigframes.series.Series) -> DataFrame:
        return self._apply_binop(other, ops.and_op)

    __and__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__and__)

    __rand__ = __and__

    def __or__(self, other: bool | int | bigframes.series.Series) -> DataFrame:
        return self._apply_binop(other, ops.or_op)

    __or__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__or__)

    __ror__ = __or__

    def __xor__(self, other: bool | int | bigframes.series.Series) -> DataFrame:
        return self._apply_binop(other, ops.xor_op)

    __xor__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__xor__)

    __rxor__ = __xor__

    def __pos__(self) -> DataFrame:
        return self._apply_unary_op(ops.pos_op)

    def __neg__(self) -> DataFrame:
        return self._apply_unary_op(ops.neg_op)

    def align(
        self,
        other: typing.Union[DataFrame, bigframes.series.Series],
        join: str = "outer",
        axis: typing.Union[str, int, None] = None,
    ) -> typing.Tuple[
        typing.Union[DataFrame, bigframes.series.Series],
        typing.Union[DataFrame, bigframes.series.Series],
    ]:
        axis_n = utils.get_axis_number(axis) if axis else None
        if axis_n == 1 and isinstance(other, bigframes.series.Series):
            raise NotImplementedError(
                f"align with series and axis=1 not supported. {constants.FEEDBACK_LINK}"
            )
        left_block, right_block = block_ops.align(
            self._block, other._block, join=join, axis=axis
        )
        return DataFrame(left_block), other.__class__(right_block)

    def update(self, other, join: str = "left", overwrite=True, filter_func=None):
        other = other if isinstance(other, DataFrame) else DataFrame(other)
        if join != "left":
            raise ValueError("Only 'left' join supported for update")

        if filter_func is not None:  # Will always take other if possible

            def update_func(
                left: bigframes.series.Series, right: bigframes.series.Series
            ) -> bigframes.series.Series:
                return left.mask(right.notna() & filter_func(left), right)

        elif overwrite:

            def update_func(
                left: bigframes.series.Series, right: bigframes.series.Series
            ) -> bigframes.series.Series:
                return left.mask(right.notna(), right)

        else:

            def update_func(
                left: bigframes.series.Series, right: bigframes.series.Series
            ) -> bigframes.series.Series:
                return left.mask(left.isna(), right)

        result = self.combine(other, update_func, how=join)

        self._set_block(result._block)

    def combine(
        self,
        other: DataFrame,
        func: typing.Callable[
            [bigframes.series.Series, bigframes.series.Series], bigframes.series.Series
        ],
        fill_value=None,
        overwrite: bool = True,
        *,
        how: str = "outer",
    ) -> DataFrame:
        l_aligned, r_aligned = block_ops.align(self._block, other._block, join=how)

        other_missing_labels = self._block.column_labels.difference(
            other._block.column_labels
        )

        l_frame = DataFrame(l_aligned)
        r_frame = DataFrame(r_aligned)
        results = []
        for (label, lseries), (_, rseries) in zip(l_frame.items(), r_frame.items()):
            if not ((label in other_missing_labels) and not overwrite):
                if fill_value is not None:
                    result = func(
                        lseries.fillna(fill_value), rseries.fillna(fill_value)
                    )
                else:
                    result = func(lseries, rseries)
            else:
                result = (
                    lseries.fillna(fill_value) if fill_value is not None else lseries
                )
            results.append(result)

        if all([isinstance(val, bigframes.series.Series) for val in results]):
            import bigframes.core.reshape.api as rs

            return rs.concat(results, axis=1)
        else:
            raise ValueError("'func' must return Series")

    def combine_first(self, other: DataFrame):
        return self._apply_dataframe_binop(other, ops.fillna_op)

    def _fast_stat_matrix(self, op: agg_ops.BinaryAggregateOp) -> DataFrame:
        """Faster corr, cov calculations, but creates more sql text, so cannot scale to many columns"""
        assert len(self.columns) * len(self.columns) < bigframes.constants.MAX_COLUMNS
        orig_columns = self.columns
        frame = self.copy()
        # Replace column names with 0 to n - 1 to keep order
        # and avoid the influence of duplicated column name
        frame.columns = pandas.Index(range(len(orig_columns)))
        frame = frame.astype(bigframes.dtypes.FLOAT_DTYPE)
        block = frame._block

        aggregations = [
            ex.BinaryAggregation(op, ex.deref(left_col), ex.deref(right_col))
            for left_col in block.value_columns
            for right_col in block.value_columns
        ]
        # unique columns stops
        uniq_orig_columns = utils.combine_indices(
            orig_columns, pandas.Index(range(len(orig_columns)))
        )
        labels = utils.cross_indices(uniq_orig_columns, uniq_orig_columns)

        block, _ = block.aggregate(aggregations=aggregations, column_labels=labels)

        block = block.stack(levels=orig_columns.nlevels + 1)
        # The aggregate operation crated a index level with just 0, need to drop it
        # Also, drop the last level of each index, which was created to guarantee uniqueness
        return DataFrame(block).droplevel(0).droplevel(-1, axis=0).droplevel(-1, axis=1)

    def corr(self, method="pearson", min_periods=None, numeric_only=False) -> DataFrame:
        if method != "pearson":
            raise NotImplementedError(
                f"Only Pearson correlation is currently supported. {constants.FEEDBACK_LINK}"
            )
        if min_periods:
            raise NotImplementedError(
                f"min_periods not yet supported. {constants.FEEDBACK_LINK}"
            )

        if not numeric_only:
            frame = self._raise_on_non_numeric("corr")
        else:
            frame = self._drop_non_numeric()

        if len(frame.columns) <= 30:
            return frame._fast_stat_matrix(agg_ops.CorrOp())

        frame = frame.copy()
        orig_columns = frame.columns
        # Replace column names with 0 to n - 1 to keep order
        # and avoid the influence of duplicated column name
        frame.columns = pandas.Index(range(len(orig_columns)))
        frame = frame.astype(bigframes.dtypes.FLOAT_DTYPE)
        block = frame._block

        # A new column that uniquely identifies each row
        block, ordering_col = frame._block.promote_offsets(label="_bigframes_idx")

        val_col_ids = [
            col_id for col_id in block.value_columns if col_id != ordering_col
        ]

        block = block.melt(
            [ordering_col], val_col_ids, ["_bigframes_variable"], "_bigframes_value"
        )

        block = block.merge(
            block,
            left_join_ids=[ordering_col],
            right_join_ids=[ordering_col],
            how="inner",
            sort=False,
        )

        frame = DataFrame(block).dropna(
            subset=["_bigframes_value_x", "_bigframes_value_y"]
        )

        paired_mean_frame = (
            frame.groupby(["_bigframes_variable_x", "_bigframes_variable_y"])
            .agg(
                _bigframes_paired_mean_x=bigframes.pandas.NamedAgg(
                    column="_bigframes_value_x", aggfunc="mean"
                ),
                _bigframes_paired_mean_y=bigframes.pandas.NamedAgg(
                    column="_bigframes_value_y", aggfunc="mean"
                ),
            )
            .reset_index()
        )

        frame = frame.merge(
            paired_mean_frame, on=["_bigframes_variable_x", "_bigframes_variable_y"]
        )
        frame["_bigframes_value_x"] -= frame["_bigframes_paired_mean_x"]
        frame["_bigframes_value_y"] -= frame["_bigframes_paired_mean_y"]

        frame["_bigframes_dividend"] = (
            frame["_bigframes_value_x"] * frame["_bigframes_value_y"]
        )
        frame["_bigframes_x_square"] = (
            frame["_bigframes_value_x"] * frame["_bigframes_value_x"]
        )
        frame["_bigframes_y_square"] = (
            frame["_bigframes_value_y"] * frame["_bigframes_value_y"]
        )

        result = (
            frame.groupby(["_bigframes_variable_x", "_bigframes_variable_y"])
            .agg(
                _bigframes_dividend_sum=bigframes.pandas.NamedAgg(
                    column="_bigframes_dividend", aggfunc="sum"
                ),
                _bigframes_x_square_sum=bigframes.pandas.NamedAgg(
                    column="_bigframes_x_square", aggfunc="sum"
                ),
                _bigframes_y_square_sum=bigframes.pandas.NamedAgg(
                    column="_bigframes_y_square", aggfunc="sum"
                ),
            )
            .reset_index()
        )
        result["_bigframes_corr"] = result["_bigframes_dividend_sum"] / (
            (
                result["_bigframes_x_square_sum"] * result["_bigframes_y_square_sum"]
            )._apply_unary_op(ops.sqrt_op)
        )
        result = result._pivot(
            index="_bigframes_variable_x",
            columns="_bigframes_variable_y",
            values="_bigframes_corr",
        )

        map_data = {
            f"_bigframes_level_{i}": orig_columns.get_level_values(i)
            for i in range(orig_columns.nlevels)
        }
        map_data["_bigframes_keys"] = range(len(orig_columns))
        map_df = bigframes.dataframe.DataFrame(
            map_data,
            session=self._get_block().expr.session,
        ).set_index("_bigframes_keys")
        result = result.join(map_df).sort_index()
        index_columns = [f"_bigframes_level_{i}" for i in range(orig_columns.nlevels)]
        result = result.set_index(index_columns)
        result.index.names = orig_columns.names
        result.columns = orig_columns

        return result

    def cov(self, *, numeric_only: bool = False) -> DataFrame:
        if not numeric_only:
            frame = self._raise_on_non_numeric("corr")
        else:
            frame = self._drop_non_numeric()

        if len(frame.columns) <= 30:
            return frame._fast_stat_matrix(agg_ops.CovOp())

        frame = frame.copy()
        orig_columns = frame.columns
        # Replace column names with 0 to n - 1 to keep order
        # and avoid the influence of duplicated column name
        frame.columns = pandas.Index(range(len(orig_columns)))
        frame = frame.astype(bigframes.dtypes.FLOAT_DTYPE)
        block = frame._block

        # A new column that uniquely identifies each row
        block, ordering_col = frame._block.promote_offsets(label="_bigframes_idx")

        val_col_ids = [
            col_id for col_id in block.value_columns if col_id != ordering_col
        ]

        block = block.melt(
            [ordering_col], val_col_ids, ["_bigframes_variable"], "_bigframes_value"
        )
        block = block.merge(
            block,
            left_join_ids=[ordering_col],
            right_join_ids=[ordering_col],
            how="inner",
            sort=False,
        )

        frame = DataFrame(block).dropna(
            subset=["_bigframes_value_x", "_bigframes_value_y"]
        )

        paired_mean_frame = (
            frame.groupby(["_bigframes_variable_x", "_bigframes_variable_y"])
            .agg(
                _bigframes_paired_mean_x=bigframes.pandas.NamedAgg(
                    column="_bigframes_value_x", aggfunc="mean"
                ),
                _bigframes_paired_mean_y=bigframes.pandas.NamedAgg(
                    column="_bigframes_value_y", aggfunc="mean"
                ),
            )
            .reset_index()
        )

        frame = frame.merge(
            paired_mean_frame, on=["_bigframes_variable_x", "_bigframes_variable_y"]
        )
        frame["_bigframes_value_x"] -= frame["_bigframes_paired_mean_x"]
        frame["_bigframes_value_y"] -= frame["_bigframes_paired_mean_y"]

        frame["_bigframes_dividend"] = (
            frame["_bigframes_value_x"] * frame["_bigframes_value_y"]
        )

        result = (
            frame.groupby(["_bigframes_variable_x", "_bigframes_variable_y"])
            .agg(
                _bigframes_dividend_sum=bigframes.pandas.NamedAgg(
                    column="_bigframes_dividend", aggfunc="sum"
                ),
                _bigframes_dividend_count=bigframes.pandas.NamedAgg(
                    column="_bigframes_dividend", aggfunc="count"
                ),
            )
            .reset_index()
        )
        result["_bigframes_cov"] = result["_bigframes_dividend_sum"] / (
            result["_bigframes_dividend_count"] - 1
        )
        result = result._pivot(
            index="_bigframes_variable_x",
            columns="_bigframes_variable_y",
            values="_bigframes_cov",
        )

        map_data = {
            f"_bigframes_level_{i}": orig_columns.get_level_values(i)
            for i in range(orig_columns.nlevels)
        }
        map_data["_bigframes_keys"] = range(len(orig_columns))
        map_df = bigframes.dataframe.DataFrame(
            map_data,
            session=self._get_block().expr.session,
        ).set_index("_bigframes_keys")
        result = result.join(map_df).sort_index()
        index_columns = [f"_bigframes_level_{i}" for i in range(orig_columns.nlevels)]
        result = result.set_index(index_columns)
        result.index.names = orig_columns.names
        result.columns = orig_columns

        return result

    def corrwith(
        self,
        other: typing.Union[DataFrame, bigframes.series.Series],
        *,
        numeric_only: bool = False,
    ):
        other_frame = other if isinstance(other, DataFrame) else other.to_frame()
        if numeric_only:
            l_frame = self._drop_non_numeric()
            r_frame = other_frame._drop_non_numeric()
        else:
            l_frame = self._raise_on_non_numeric("corrwith")
            r_frame = other_frame._raise_on_non_numeric("corrwith")

        l_block = l_frame.astype(bigframes.dtypes.FLOAT_DTYPE)._block
        r_block = r_frame.astype(bigframes.dtypes.FLOAT_DTYPE)._block

        if isinstance(other, DataFrame):
            block, labels, expr_pairs = l_block._align_both_axes(r_block, how="inner")
        else:
            assert isinstance(other, bigframes.series.Series)
            block, labels, expr_pairs = l_block._align_axis_0(r_block, how="inner")

        na_cols = l_block.column_labels.join(
            r_block.column_labels, how="outer"
        ).difference(labels)

        block, _ = block.aggregate(
            aggregations=tuple(
                ex.BinaryAggregation(agg_ops.CorrOp(), left_ex, right_ex)
                for left_ex, right_ex in expr_pairs
            ),
            column_labels=labels,
        )
        block = block.project_exprs(
            (ex.const(float("nan")),) * len(na_cols), labels=na_cols
        )
        block = block.transpose(
            original_row_index=pandas.Index([None]), single_row_mode=True
        )
        return bigframes.pandas.Series(block)

    def to_arrow(
        self,
        *,
        ordered: bool = True,
        allow_large_results: Optional[bool] = None,
    ) -> pyarrow.Table:
        """Write DataFrame to an Arrow table / record batch.

        Args:
            ordered (bool, default True):
                Determines whether the resulting Arrow table will be ordered.
                In some cases, unordered may result in a faster-executing query.
            allow_large_results (bool, default None):
                If not None, overrides the global setting to allow or disallow large query results
                over the default size limit of 10 GB.

        Returns:
            pyarrow.Table: A pyarrow Table with all rows and columns of this DataFrame.
        """
        msg = bfe.format_message(
            "to_arrow is in preview. Types and unnamed or duplicate name columns may "
            "change in future."
        )
        warnings.warn(msg, category=bfe.PreviewWarning)

        pa_table, query_job = self._block.to_arrow(
            ordered=ordered, allow_large_results=allow_large_results
        )
        if query_job:
            self._set_internal_query_job(query_job)
        return pa_table

    @overload
    def to_pandas(  # type: ignore[overload-overlap]
        self,
        max_download_size: Optional[int] = ...,
        sampling_method: Optional[str] = ...,
        random_state: Optional[int] = ...,
        *,
        ordered: bool = ...,
        dry_run: Literal[False] = ...,
        allow_large_results: Optional[bool] = ...,
    ) -> pandas.DataFrame:
        ...

    @overload
    def to_pandas(
        self,
        max_download_size: Optional[int] = ...,
        sampling_method: Optional[str] = ...,
        random_state: Optional[int] = ...,
        *,
        ordered: bool = ...,
        dry_run: Literal[True] = ...,
        allow_large_results: Optional[bool] = ...,
    ) -> pandas.Series:
        ...

    def to_pandas(
        self,
        max_download_size: Optional[int] = None,
        sampling_method: Optional[str] = None,
        random_state: Optional[int] = None,
        *,
        ordered: bool = True,
        dry_run: bool = False,
        allow_large_results: Optional[bool] = None,
    ) -> pandas.DataFrame | pandas.Series:
        """Write DataFrame to pandas DataFrame.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> df = bpd.DataFrame({'col': [4, 2, 2]})

        Download the data from BigQuery and convert it into an in-memory pandas DataFrame.

            >>> df.to_pandas()
               col
            0    4
            1    2
            2    2

        Estimate job statistics without processing or downloading data by using `dry_run=True`.

            >>> df.to_pandas(dry_run=True) # doctest: +SKIP
            columnCount                                                            1
            columnDtypes                                              {'col': Int64}
            indexLevel                                                             1
            indexDtypes                                                      [Int64]
            projectId                                                  bigframes-dev
            location                                                              US
            jobType                                                            QUERY
            destinationTable       {'projectId': 'bigframes-dev', 'datasetId': '_...
            useLegacySql                                                       False
            referencedTables                                                    None
            totalBytesProcessed                                                    0
            cacheHit                                                           False
            statementType                                                     SELECT
            creationTime                            2025-04-02 20:17:12.038000+00:00
            dtype: object

        Args:
            max_download_size (int, default None):
                .. deprecated:: 2.0.0
                    ``max_download_size`` parameter is deprecated. Please use ``to_pandas_batches()``
                    method instead.

                Download size threshold in MB. If ``max_download_size`` is exceeded when downloading data,
                the data will be downsampled if ``bigframes.options.sampling.enable_downsampling`` is
                ``True``, otherwise, an error will be raised. If set to a value other than ``None``,
                this will supersede the global config.
            sampling_method (str, default None):
                .. deprecated:: 2.0.0
                    ``sampling_method`` parameter is deprecated. Please use ``sample()`` method instead.

                Downsampling algorithms to be chosen from, the choices are: "head": This algorithm
                returns a portion of the data from the beginning. It is fast and requires minimal
                computations to perform the downsampling; "uniform": This algorithm returns uniform
                random samples of the data. If set to a value other than None, this will supersede
                the global config.
            random_state (int, default None):
                .. deprecated:: 2.0.0
                    ``random_state`` parameter is deprecated. Please use ``sample()`` method instead.

                The seed for the uniform downsampling algorithm. If provided, the uniform method may
                take longer to execute and require more computation. If set to a value other than
                None, this will supersede the global config.
            ordered (bool, default True):
                Determines whether the resulting pandas dataframe will be ordered.
                In some cases, unordered may result in a faster-executing query.
            dry_run (bool, default False):
                If this argument is true, this method will not process the data. Instead, it returns
                a Pandas Series containing dry run statistics
            allow_large_results (bool, default None):
                If not None, overrides the global setting to allow or disallow large query results
                over the default size limit of 10 GB.

        Returns:
            pandas.DataFrame: A pandas DataFrame with all rows and columns of this DataFrame if the
                data_sampling_threshold_mb is not exceeded; otherwise, a pandas DataFrame with
                downsampled rows and all columns of this DataFrame. If dry_run is set, a pandas
                Series containing dry run statistics will be returned.
        """
        if max_download_size is not None:
            msg = bfe.format_message(
                "DEPRECATED: The `max_download_size` parameters for `DataFrame.to_pandas()` "
                "are deprecated and will be removed soon. Please use `DataFrame.to_pandas_batches()`."
            )
            warnings.warn(msg, category=FutureWarning)
        if sampling_method is not None or random_state is not None:
            msg = bfe.format_message(
                "DEPRECATED: The `sampling_method` and `random_state` parameters for "
                "`DataFrame.to_pandas()` are deprecated and will be removed soon. "
                "Please use `DataFrame.sample().to_pandas()` instead for sampling."
            )
            warnings.warn(msg, category=FutureWarning, stacklevel=2)

        if dry_run:
            dry_run_stats, dry_run_job = self._block._compute_dry_run(
                max_download_size=max_download_size,
                sampling_method=sampling_method,
                random_state=random_state,
                ordered=ordered,
            )
            self._set_internal_query_job(dry_run_job)
            return dry_run_stats

        df, query_job = self._block.to_pandas(
            max_download_size=max_download_size,
            sampling_method=sampling_method,
            random_state=random_state,
            ordered=ordered,
            allow_large_results=allow_large_results,
        )
        if query_job:
            self._set_internal_query_job(query_job)
        return df.set_axis(self._block.column_labels, axis=1, copy=False)

    def to_pandas_batches(
        self,
        page_size: Optional[int] = None,
        max_results: Optional[int] = None,
        *,
        allow_large_results: Optional[bool] = None,
    ) -> Iterable[pandas.DataFrame]:
        """Stream DataFrame results to an iterable of pandas DataFrame.

        page_size and max_results determine the size and number of batches,
        see https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob#google_cloud_bigquery_job_QueryJob_result

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> df = bpd.DataFrame({'col': [4, 3, 2, 2, 3]})

        Iterate through the results in batches, limiting the total rows yielded
        across all batches via `max_results`:

            >>> for df_batch in df.to_pandas_batches(max_results=3):
            ...     print(df_batch)
               col
            0    4
            1    3
            2    2

        Alternatively, control the approximate size of each batch using `page_size`
        and fetch batches manually using `next()`:

            >>> it = df.to_pandas_batches(page_size=2)
            >>> next(it)
               col
            0    4
            1    3
            >>> next(it)
               col
            2    2
            3    2

        Args:
            page_size (int, default None):
                The maximum number of rows of each batch. Non-positive values are ignored.
            max_results (int, default None):
                The maximum total number of rows of all batches.
            allow_large_results (bool, default None):
                If not None, overrides the global setting to allow or disallow large query results
                over the default size limit of 10 GB.

        Returns:
            Iterable[pandas.DataFrame]:
                An iterable of smaller dataframes which combine to
                form the original dataframe. Results stream from bigquery,
                see https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.table.RowIterator#google_cloud_bigquery_table_RowIterator_to_arrow_iterable
        """
        return self._block.to_pandas_batches(
            page_size=page_size,
            max_results=max_results,
            allow_large_results=allow_large_results,
        )

    def _compute_dry_run(self) -> bigquery.QueryJob:
        _, query_job = self._block._compute_dry_run()
        return query_job

    def copy(self) -> DataFrame:
        return DataFrame(self._block)

    @validations.requires_ordering(bigframes.constants.SUGGEST_PEEK_PREVIEW)
    def head(self, n: int = 5) -> DataFrame:
        return typing.cast(DataFrame, self.iloc[:n])

    @validations.requires_ordering()
    def tail(self, n: int = 5) -> DataFrame:
        return typing.cast(DataFrame, self.iloc[-n:])

    def peek(
        self, n: int = 5, *, force: bool = True, allow_large_results=None
    ) -> pandas.DataFrame:
        """
        Preview n arbitrary rows from the dataframe. No guarantees about row selection or ordering.
        ``DataFrame.peek(force=False)`` will always be very fast, but will not succeed if data requires
        full data scanning. Using ``force=True`` will always succeed, but may be perform queries.
        Query results will be cached so that future steps will benefit from these queries.

        Args:
            n (int, default 5):
                The number of rows to select from the dataframe. Which N rows are returned is non-deterministic.
            force (bool, default True):
                If the data cannot be peeked efficiently, the dataframe will instead be fully materialized as part
                of the operation if ``force=True``. If ``force=False``, the operation will throw a ValueError.
            allow_large_results (bool, default None):
                If not None, overrides the global setting to allow or disallow large query results
                over the default size limit of 10 GB.
        Returns:
            pandas.DataFrame: A pandas DataFrame with n rows.

        Raises:
            ValueError: If force=False and data cannot be efficiently peeked.
        """
        maybe_result = self._block.try_peek(n, allow_large_results=allow_large_results)
        if maybe_result is None:
            if force:
                self._cached()
                maybe_result = self._block.try_peek(
                    n, force=True, allow_large_results=allow_large_results
                )
                assert maybe_result is not None
            else:
                raise ValueError(
                    "Cannot peek efficiently when data has aggregates, joins or window functions applied. Use force=True to fully compute dataframe."
                )
        return maybe_result.set_axis(self._block.column_labels, axis=1, copy=False)

    def nlargest(
        self,
        n: int,
        columns: typing.Union[blocks.Label, typing.Sequence[blocks.Label]],
        keep: str = "first",
    ) -> DataFrame:
        if keep not in ("first", "last", "all"):
            raise ValueError("'keep must be one of 'first', 'last', or 'all'")
        if keep != "all":
            validations.enforce_ordered(self, "nlargest")
        column_ids = self._sql_names(columns)
        return DataFrame(block_ops.nlargest(self._block, n, column_ids, keep=keep))

    def nsmallest(
        self,
        n: int,
        columns: typing.Union[blocks.Label, typing.Sequence[blocks.Label]],
        keep: str = "first",
    ) -> DataFrame:
        if keep not in ("first", "last", "all"):
            raise ValueError("'keep must be one of 'first', 'last', or 'all'")
        if keep != "all":
            validations.enforce_ordered(self, "nlargest")
        column_ids = self._sql_names(columns)
        return DataFrame(block_ops.nsmallest(self._block, n, column_ids, keep=keep))

    def insert(
        self,
        loc: int,
        column: blocks.Label,
        value: SingleItemValue,
        allow_duplicates: bool = False,
    ):
        column_count = len(self.columns)
        if loc > column_count:
            raise IndexError(
                f"Column index {loc} is out of bounds with {column_count} total columns."
            )
        if (column in self.columns) and not allow_duplicates:
            raise ValueError(f"cannot insert {column}, already exists")

        temp_column = bigframes.core.guid.generate_guid(prefix=str(column))
        df = self._assign_single_item(temp_column, value)

        block = df._get_block()
        value_columns = typing.cast(List, block.value_columns)
        value_columns, new_column = value_columns[:-1], value_columns[-1]
        value_columns.insert(loc, new_column)

        block = block.select_columns(value_columns)
        block = block.rename(columns={temp_column: column})

        self._set_block(block)

    def drop(
        self,
        labels: typing.Any = None,
        *,
        axis: typing.Union[int, str] = 0,
        index: typing.Any = None,
        columns: Union[blocks.Label, Sequence[blocks.Label]] = None,
        level: typing.Optional[LevelType] = None,
    ) -> DataFrame:
        if labels:
            if index or columns:
                raise ValueError("Cannot specify both 'labels' and 'index'/'columns")
            axis_n = utils.get_axis_number(axis)
            if axis_n == 0:
                index = labels
            else:
                columns = labels

        block = self._block
        if index is not None:
            self._throw_if_null_index("drop(axis=0)")
            level_id = self._resolve_levels(level or 0)[0]

            if utils.is_list_like(index):
                # Only tuple is treated as multi-index value combinations
                if isinstance(index, tuple):
                    if level is not None:
                        raise ValueError("Multi-index tuple can't specify level.")
                    condition_id = None
                    for i, idx in enumerate(index):
                        level_id = self._resolve_levels(i)[0]
                        block, condition_id_cur = block.project_expr(
                            ops.ne_op.as_expr(level_id, ex.const(idx))
                        )
                        if condition_id:
                            block, condition_id = block.apply_binary_op(
                                condition_id, condition_id_cur, ops.or_op
                            )
                        else:
                            condition_id = condition_id_cur

                    condition_id = typing.cast(str, condition_id)
                else:
                    block, inverse_condition_id = block.apply_unary_op(
                        level_id, ops.IsInOp(values=tuple(index), match_nulls=True)
                    )
                    block, condition_id = block.apply_unary_op(
                        inverse_condition_id, ops.invert_op
                    )
            elif isinstance(index, indexes.Index):
                return self._drop_by_index(index)
            else:
                block, condition_id = block.project_expr(
                    ops.ne_op.as_expr(level_id, ex.const(index))
                )
            block = block.filter_by_id(condition_id, keep_null=True).select_columns(
                self._block.value_columns
            )
        if columns:
            block = block.drop_columns(self._sql_names(columns))
        if index is None and not columns:
            raise ValueError("Must specify 'labels' or 'index'/'columns")
        return DataFrame(block)

    def _drop_by_index(self, index: indexes.Index) -> DataFrame:
        block = index._block
        block, ordering_col = block.promote_offsets()
        joined_index, (get_column_left, get_column_right) = self._block.join(block)

        new_ordering_col = get_column_right[ordering_col]
        drop_block = joined_index
        drop_block, drop_col = drop_block.apply_unary_op(
            new_ordering_col,
            ops.isnull_op,
        )

        drop_block = drop_block.filter_by_id(drop_col)
        original_columns = [
            get_column_left[column] for column in self._block.value_columns
        ]
        drop_block = drop_block.select_columns(original_columns)
        return DataFrame(drop_block)

    def droplevel(self, level: LevelsType, axis: int | str = 0):
        axis_n = utils.get_axis_number(axis)
        if axis_n == 0:
            resolved_level_ids = self._resolve_levels(level)
            return DataFrame(self._block.drop_levels(resolved_level_ids))
        else:
            if isinstance(self.columns, pandas.MultiIndex):
                new_df = self.copy()
                new_df.columns = self.columns.droplevel(level)
                return new_df
            else:
                raise ValueError("Columns must be a multiindex to drop levels.")

    def swaplevel(self, i: int = -2, j: int = -1, axis: int | str = 0):
        axis_n = utils.get_axis_number(axis)
        if axis_n == 0:
            level_i = self._block.index_columns[i]
            level_j = self._block.index_columns[j]
            mapping = {level_i: level_j, level_j: level_i}
            reordering = [
                mapping.get(index_id, index_id)
                for index_id in self._block.index_columns
            ]
            return DataFrame(self._block.reorder_levels(reordering))
        else:
            if isinstance(self.columns, pandas.MultiIndex):
                new_df = self.copy()
                new_df.columns = self.columns.swaplevel(i, j)
                return new_df
            else:
                raise ValueError("Columns must be a multiindex to reorder levels.")

    def reorder_levels(self, order: LevelsType, axis: int | str = 0):
        axis_n = utils.get_axis_number(axis)
        if axis_n == 0:
            resolved_level_ids = self._resolve_levels(order)
            return DataFrame(self._block.reorder_levels(resolved_level_ids))
        else:
            if isinstance(self.columns, pandas.MultiIndex):
                new_df = self.copy()
                new_df.columns = self.columns.reorder_levels(order)
                return new_df
            else:
                raise ValueError("Columns must be a multiindex to reorder levels.")

    def _resolve_levels(self, level: LevelsType) -> typing.Sequence[str]:
        return self._block.index.resolve_level(level)

    @overload
    def rename(self, *, columns: Mapping[blocks.Label, blocks.Label]) -> DataFrame:
        ...

    @overload
    def rename(
        self, *, columns: Mapping[blocks.Label, blocks.Label], inplace: Literal[False]
    ) -> DataFrame:
        ...

    @overload
    def rename(
        self, *, columns: Mapping[blocks.Label, blocks.Label], inplace: Literal[True]
    ) -> None:
        ...

    def rename(
        self, *, columns: Mapping[blocks.Label, blocks.Label], inplace: bool = False
    ) -> Optional[DataFrame]:
        block = self._block.rename(columns=columns)

        if inplace:
            self._block = block
            return None
        else:
            return DataFrame(block)

    @overload
    def rename_axis(
        self,
        mapper: typing.Union[blocks.Label, typing.Sequence[blocks.Label]],
    ) -> DataFrame:
        ...

    @overload
    def rename_axis(
        self,
        mapper: typing.Union[blocks.Label, typing.Sequence[blocks.Label]],
        *,
        inplace: Literal[False],
        **kwargs,
    ) -> DataFrame:
        ...

    @overload
    def rename_axis(
        self,
        mapper: typing.Union[blocks.Label, typing.Sequence[blocks.Label]],
        *,
        inplace: Literal[True],
        **kwargs,
    ) -> None:
        ...

    def rename_axis(
        self,
        mapper: typing.Union[blocks.Label, typing.Sequence[blocks.Label]],
        *,
        inplace: bool = False,
        **kwargs,
    ) -> Optional[DataFrame]:
        if len(kwargs) != 0:
            raise NotImplementedError(
                f"rename_axis does not currently support any keyword arguments. {constants.FEEDBACK_LINK}"
            )
        # limited implementation: the new index name is simply the 'mapper' parameter
        if utils.is_list_like(mapper):
            labels = mapper
        else:
            labels = [mapper]

        block = self._block.with_index_labels(labels)

        if inplace:
            self._block = block
            return None
        else:
            return DataFrame(block)

    @validations.requires_ordering()
    def equals(self, other: typing.Union[bigframes.series.Series, DataFrame]) -> bool:
        # Must be same object type, same column dtypes, and same label values
        if not isinstance(other, DataFrame):
            return False
        return block_ops.equals(self._block, other._block)

    def assign(self, **kwargs) -> DataFrame:
        # TODO(garrettwu) Support list-like values. Requires ordering.
        # TODO(garrettwu) Support callable values.

        cur = self
        for k, v in kwargs.items():
            cur = cur._assign_single_item(k, v)

        return cur

    def _assign_single_item(
        self,
        k: str,
        v: SingleItemValue,
    ) -> DataFrame:
        if isinstance(v, bigframes.series.Series):
            return self._assign_series_join_on_index(k, v)
        elif isinstance(v, bigframes.dataframe.DataFrame):
            v_df_col_count = len(v._block.value_columns)
            if v_df_col_count != 1:
                raise ValueError(
                    f"Cannot set a DataFrame with {v_df_col_count} columns to the single column {k}"
                )
            return self._assign_series_join_on_index(k, v[v.columns[0]])
        elif callable(v):
            copy = self.copy()
            copy[k] = v(copy)
            return copy
        elif utils.is_list_like(v):
            return self._assign_single_item_listlike(k, v)
        else:
            return self._assign_scalar(k, v)

    def _assign_single_item_listlike(self, k: str, v: Sequence) -> DataFrame:
        given_rows = len(v)
        actual_rows = len(self)
        assigning_to_empty_df = len(self.columns) == 0 and actual_rows == 0
        if not assigning_to_empty_df and given_rows != actual_rows:
            raise ValueError(
                f"Length of values ({given_rows}) does not match length of index ({actual_rows})"
            )

        local_df = DataFrame({k: v}, session=self._get_block().expr.session)
        # local_df is likely (but not guaranteed) to be cached locally
        # since the original list came from memory and so is probably < MAX_INLINE_DF_SIZE

        new_column_block = local_df._block
        original_index_column_ids = self._block.index_columns
        self_block = self._block.reset_index(drop=False)
        if assigning_to_empty_df:
            if len(self._block.index_columns) > 1:
                # match error raised by pandas here
                raise ValueError(
                    "Assigning listlike to a first column under multiindex is not supported."
                )
            result_block = new_column_block.with_index_labels(self._block.index.names)
            result_block = result_block.with_column_labels([k])
        else:
            result_block, (
                get_column_left,
                get_column_right,
            ) = self_block.join(new_column_block, how="left", block_identity_join=True)
            result_block = result_block.set_index(
                [get_column_left[col_id] for col_id in original_index_column_ids],
                index_labels=self._block.index.names,
            )
            src_col = get_column_right[new_column_block.value_columns[0]]
            # Check to see if key exists, and modify in place
            col_ids = self._block.cols_matching_label(k)
            for col_id in col_ids:
                result_block = result_block.copy_values(
                    src_col, get_column_left[col_id]
                )
            if len(col_ids) > 0:
                result_block = result_block.drop_columns([src_col])
        return DataFrame(result_block)

    def _assign_scalar(self, label: str, value: Union[int, float, str]) -> DataFrame:
        col_ids = self._block.cols_matching_label(label)

        block, constant_col_id = self._block.create_constant(value, label)
        for col_id in col_ids:
            block = block.copy_values(constant_col_id, col_id)

        if len(col_ids) > 0:
            block = block.drop_columns([constant_col_id])

        return DataFrame(block)

    def _assign_series_join_on_index(
        self, label: str, series: bigframes.series.Series
    ) -> DataFrame:
        block, (get_column_left, get_column_right) = self._block.join(
            series._block, how="left"
        )

        column_ids = [
            get_column_left[col_id] for col_id in self._block.cols_matching_label(label)
        ]
        source_column = get_column_right[series._value_column]

        # Replace each column matching the label
        for column_id in column_ids:
            block = block.copy_values(source_column, column_id).assign_label(
                column_id, label
            )

        if not column_ids:
            # Append case, so new column needs appropriate label
            block = block.assign_label(source_column, label)
        else:
            # Update case, remove after copying into columns
            block = block.drop_columns([source_column])

        return DataFrame(block.with_index_labels(self._block.index.names))

    def reset_index(self, *, drop: bool = False) -> DataFrame:
        block = self._block.reset_index(drop)
        return DataFrame(block)

    def set_index(
        self,
        keys: typing.Union[blocks.Label, typing.Sequence[blocks.Label]],
        append: bool = False,
        drop: bool = True,
    ) -> DataFrame:
        if not utils.is_list_like(keys):
            keys = typing.cast(typing.Sequence[blocks.Label], (keys,))
        else:
            keys = typing.cast(typing.Sequence[blocks.Label], tuple(keys))
        col_ids = [self._resolve_label_exact(key) for key in keys]
        missing = [keys[i] for i in range(len(col_ids)) if col_ids[i] is None]
        if len(missing) > 0:
            raise KeyError(f"None of {missing} are in the columns")
        # convert col_ids to non-optional strs since we just determined they are not None
        col_ids_strs: List[str] = [col_id for col_id in col_ids if col_id is not None]
        return DataFrame(self._block.set_index(col_ids_strs, append=append, drop=drop))

    @overload  # type: ignore[override]
    def sort_index(
        self,
        *,
        ascending: bool = ...,
        inplace: Literal[False] = ...,
        na_position: Literal["first", "last"] = ...,
    ) -> DataFrame:
        ...

    @overload
    def sort_index(
        self,
        *,
        ascending: bool = ...,
        inplace: Literal[True] = ...,
        na_position: Literal["first", "last"] = ...,
    ) -> None:
        ...

    @validations.requires_index
    def sort_index(
        self,
        *,
        ascending: bool = True,
        inplace: bool = False,
        na_position: Literal["first", "last"] = "last",
    ) -> Optional[DataFrame]:
        if na_position not in ["first", "last"]:
            raise ValueError("Param na_position must be one of 'first' or 'last'")
        na_last = na_position == "last"
        index_columns = self._block.index_columns
        ordering = [
            order.ascending_over(column, na_last)
            if ascending
            else order.descending_over(column, na_last)
            for column in index_columns
        ]
        block = self._block.order_by(ordering)
        if inplace:
            self._set_block(block)
            return None
        else:
            return DataFrame(block)

    @overload  # type: ignore[override]
    def sort_values(
        self,
        by: str | typing.Sequence[str],
        *,
        inplace: Literal[False] = ...,
        ascending: bool | typing.Sequence[bool] = ...,
        kind: str = ...,
        na_position: typing.Literal["first", "last"] = ...,
    ) -> DataFrame:
        ...

    @overload
    def sort_values(
        self,
        by: str | typing.Sequence[str],
        *,
        inplace: Literal[True] = ...,
        ascending: bool | typing.Sequence[bool] = ...,
        kind: str = ...,
        na_position: typing.Literal["first", "last"] = ...,
    ) -> None:
        ...

    def sort_values(
        self,
        by: str | typing.Sequence[str],
        *,
        inplace: bool = False,
        ascending: bool | typing.Sequence[bool] = True,
        kind: str = "quicksort",
        na_position: typing.Literal["first", "last"] = "last",
    ) -> Optional[DataFrame]:
        if isinstance(by, (bigframes.series.Series, indexes.Index, DataFrame)):
            raise KeyError(
                f"Invalid key type: {type(by).__name__}. Please provide valid column name(s)."
            )

        if na_position not in {"first", "last"}:
            raise ValueError("Param na_position must be one of 'first' or 'last'")

        sort_labels = list(by) if utils.is_list_like(by) else [by]
        sort_column_ids = self._sql_names(sort_labels)

        len_by = len(sort_labels)
        if not isinstance(ascending, bool):
            if len(ascending) != len_by:
                raise ValueError("Length of 'ascending' must equal length of 'by'")
            sort_directions = ascending
        else:
            sort_directions = (ascending,) * len_by

        ordering = []
        for i in range(len(sort_labels)):
            column_id = sort_column_ids[i]
            is_ascending = sort_directions[i]
            na_last = na_position == "last"
            ordering.append(
                order.ascending_over(column_id, na_last)
                if is_ascending
                else order.descending_over(column_id, na_last)
            )
        block = self._block.order_by(ordering)
        if inplace:
            self._set_block(block)
            return None
        else:
            return DataFrame(block)

    def eval(self, expr: str) -> DataFrame:
        import bigframes.core.eval as bf_eval

        return bf_eval.eval(self, expr, target=self)

    def query(self, expr: str) -> DataFrame:
        import bigframes.core.eval as bf_eval

        eval_result = bf_eval.eval(self, expr, target=None)
        return self[eval_result]

    def value_counts(
        self,
        subset: typing.Union[blocks.Label, typing.Sequence[blocks.Label]] = None,
        normalize: bool = False,
        sort: bool = True,
        ascending: bool = False,
        dropna: bool = True,
    ):
        # 'sort'=False allows arbitrary sorting, so we will sort anyways and ignore the param
        columns = self._sql_names(subset) if subset else self._block.value_columns
        block = block_ops.value_counts(
            self._block,
            columns,
            normalize=normalize,
            sort=sort,
            ascending=ascending,
            dropna=dropna,
        )
        return bigframes.series.Series(block)

    def add_prefix(self, prefix: str, axis: int | str | None = None) -> DataFrame:
        axis = 1 if axis is None else axis
        return DataFrame(self._get_block().add_prefix(prefix, axis))

    def add_suffix(self, suffix: str, axis: int | str | None = None) -> DataFrame:
        axis = 1 if axis is None else axis
        return DataFrame(self._get_block().add_suffix(suffix, axis))

    def take(
        self, indices: typing.Sequence[int], axis: int | str | None = 0, **kwargs
    ) -> DataFrame:
        if not utils.is_list_like(indices):
            raise ValueError("indices should be a list-like object.")
        if axis == 0 or axis == "index":
            return self.iloc[indices]
        elif axis == 1 or axis == "columns":
            return self.iloc[:, indices]
        else:
            raise ValueError(f"No axis named {axis} for object type DataFrame")

    def filter(
        self,
        items: typing.Optional[typing.Iterable] = None,
        like: typing.Optional[str] = None,
        regex: typing.Optional[str] = None,
        axis: int | str | None = None,
    ) -> DataFrame:
        if sum([(items is not None), (like is not None), (regex is not None)]) != 1:
            raise ValueError(
                "Need to provide exactly one of 'items', 'like', or 'regex'"
            )
        axis_n = utils.get_axis_number(axis) if (axis is not None) else 1
        if axis_n == 0:  # row labels
            return self._filter_rows(items, like, regex)
        else:  # column labels
            return self._filter_columns(items, like, regex)

    def _filter_rows(
        self,
        items: typing.Optional[typing.Iterable] = None,
        like: typing.Optional[str] = None,
        regex: typing.Optional[str] = None,
    ) -> DataFrame:
        if len(self._block.index_columns) > 1:
            raise NotImplementedError(
                f"Method filter does not support rows multiindex. {constants.FEEDBACK_LINK}"
            )
        if (like is not None) or (regex is not None):
            block = self._block
            block, label_string_id = block.apply_unary_op(
                self._block.index_columns[0],
                ops.AsTypeOp(to_type=pandas.StringDtype(storage="pyarrow")),
            )
            if like is not None:
                block, mask_id = block.apply_unary_op(
                    label_string_id, ops.StrContainsOp(pat=like)
                )
            else:  # regex
                assert regex is not None
                block, mask_id = block.apply_unary_op(
                    label_string_id, ops.StrContainsRegexOp(pat=regex)
                )

            block = block.filter_by_id(mask_id)
            block = block.select_columns(self._block.value_columns)
            return DataFrame(block)
        elif items is not None:
            # Behavior matches pandas 2.1+, older pandas versions would reindex
            block = self._block
            block, mask_id = block.apply_unary_op(
                self._block.index_columns[0], ops.IsInOp(values=tuple(items))
            )
            block = block.filter_by_id(mask_id)
            block = block.select_columns(self._block.value_columns)
            return DataFrame(block)
        else:
            raise ValueError("Need to provide 'items', 'like', or 'regex'")

    def _filter_columns(
        self,
        items: typing.Optional[typing.Iterable] = None,
        like: typing.Optional[str] = None,
        regex: typing.Optional[str] = None,
    ) -> DataFrame:
        if (like is not None) or (regex is not None):

            def label_filter(label):
                label_str = label if isinstance(label, str) else str(label)
                if like:
                    return like in label_str
                else:  # regex
                    # TODO(b/340891296): fix type error
                    return re.match(regex, label_str) is not None  # type: ignore

            cols = [
                col_id
                for col_id, label in zip(self._block.value_columns, self.columns)
                if label_filter(label)
            ]
            return DataFrame(self._block.select_columns(cols))
        if items is not None:
            # Behavior matches pandas 2.1+, older pandas versions would reorder using order of items
            new_columns = self.columns.intersection(pandas.Index(items))
            return self.reindex(columns=new_columns)
        else:
            raise ValueError("Need to provide 'items', 'like', or 'regex'")

    def reindex(
        self,
        labels=None,
        *,
        index=None,
        columns=None,
        axis: typing.Optional[typing.Union[str, int]] = None,
        validate: typing.Optional[bool] = None,
    ):
        if labels:
            if index or columns:
                raise ValueError("Cannot specify both 'labels' and 'index'/'columns")
            axis_n = utils.get_axis_number(axis) if (axis is not None) else 0
            if axis_n == 0:
                index = labels
            else:
                columns = labels
        if (index is not None) and (columns is not None):
            return self._reindex_columns(columns)._reindex_rows(
                index, validate=validate or False
            )
        if index is not None:
            return self._reindex_rows(index, validate=validate or False)
        if columns is not None:
            return self._reindex_columns(columns)

    @validations.requires_index
    def _reindex_rows(
        self,
        index,
        *,
        validate: typing.Optional[bool] = None,
    ):
        if validate and not self.index.is_unique:
            raise ValueError("Original index must be unique to reindex")
        keep_original_names = False
        if isinstance(index, indexes.Index):
            new_indexer = DataFrame(data=index._block)[[]]
        else:
            if not isinstance(index, pandas.Index):
                keep_original_names = True
                index = pandas.Index(index)
            if index.nlevels != self.index.nlevels:
                raise NotImplementedError(
                    "Cannot reindex with index with different nlevels"
                )
            new_indexer = DataFrame(index=index, session=self._session)[[]]
        # multiindex join is senstive to index names, so we will set all these
        result = new_indexer.rename_axis(range(new_indexer.index.nlevels)).join(
            self.rename_axis(range(self.index.nlevels)),
            how="left",
        )
        # and then reset the names after the join
        return result.rename_axis(
            self.index.names if keep_original_names else index.names
        )

    def _reindex_columns(self, columns):
        block = self._block
        new_column_index, indexer = self.columns.reindex(columns)

        if indexer is None:
            # The new index is the same as the old one. Do nothing.
            return self

        result_cols = []
        for label, index in zip(columns, indexer):
            if index >= 0:
                result_cols.append(self._block.value_columns[index])
            else:
                block, null_col = block.create_constant(
                    pandas.NA, label, dtype=pandas.Float64Dtype()
                )
                result_cols.append(null_col)
        result_df = DataFrame(block.select_columns(result_cols))
        result_df.columns = new_column_index
        return result_df

    @validations.requires_index
    def reindex_like(self, other: DataFrame, *, validate: typing.Optional[bool] = None):
        return self.reindex(index=other.index, columns=other.columns, validate=validate)

    @validations.requires_ordering()
    @validations.requires_index
    def interpolate(self, method: str = "linear") -> DataFrame:
        if method == "pad":
            return self.ffill()
        result = block_ops.interpolate(self._block, method)
        return DataFrame(result)

    def fillna(self, value=None) -> DataFrame:
        return self._apply_binop(value, ops.fillna_op, how="left")

    def replace(
        self, to_replace: typing.Any, value: typing.Any = None, *, regex: bool = False
    ):
        if utils.is_dict_like(value):
            return self.apply(
                lambda x: x.replace(
                    to_replace=to_replace, value=value[x.name], regex=regex
                )
                if (x.name in value)
                else x
            )
        return self.apply(
            lambda x: x.replace(to_replace=to_replace, value=value, regex=regex)
        )

    @validations.requires_ordering()
    def ffill(self, *, limit: typing.Optional[int] = None) -> DataFrame:
        window = windows.rows(start=None if limit is None else -limit, end=0)
        return self._apply_window_op(agg_ops.LastNonNullOp(), window)

    @validations.requires_ordering()
    def bfill(self, *, limit: typing.Optional[int] = None) -> DataFrame:
        window = windows.rows(start=0, end=limit)
        return self._apply_window_op(agg_ops.FirstNonNullOp(), window)

    def isin(self, values) -> DataFrame:
        if utils.is_dict_like(values):
            block = self._block
            result_ids = []
            for col, label in zip(self._block.value_columns, self._block.column_labels):
                if label in values.keys():
                    value_for_key = values[label]
                    block, result_id = block.apply_unary_op(
                        col,
                        ops.IsInOp(values=tuple(value_for_key), match_nulls=True),
                        label,
                    )
                    result_ids.append(result_id)
                else:
                    block, result_id = block.create_constant(
                        False, label=label, dtype=pandas.BooleanDtype()
                    )
                    result_ids.append(result_id)
            return DataFrame(block.select_columns(result_ids)).fillna(value=False)
        elif utils.is_list_like(values):
            return self._apply_unary_op(
                ops.IsInOp(values=tuple(values), match_nulls=True)
            ).fillna(value=False)
        else:
            raise TypeError(
                "only list-like objects are allowed to be passed to "
                f"isin(), you passed a [{type(values).__name__}]"
            )

    def keys(self) -> pandas.Index:
        return self.columns

    def items(self):
        column_ids = self._block.value_columns
        column_labels = self._block.column_labels
        for col_id, col_label in zip(column_ids, column_labels):
            yield col_label, bigframes.series.Series(self._block.select_column(col_id))

    def iterrows(self) -> Iterable[tuple[typing.Any, pandas.Series]]:
        for df in self.to_pandas_batches():
            for item in df.iterrows():
                yield item

    def itertuples(
        self, index: bool = True, name: typing.Optional[str] = "Pandas"
    ) -> Iterable[tuple[typing.Any, ...]]:
        for df in self.to_pandas_batches():
            for item in df.itertuples(index=index, name=name):
                yield item

    def where(self, cond, other=None):
        if isinstance(other, bigframes.series.Series):
            raise ValueError("Seires is not a supported replacement type!")

        if self.columns.nlevels > 1:
            raise NotImplementedError(
                "The dataframe.where() method does not support multi-column."
            )

        aligned_block, (_, _) = self._block.join(cond._block, how="left")
        # No left join is needed when 'other' is None or constant.
        if isinstance(other, bigframes.dataframe.DataFrame):
            aligned_block, (_, _) = aligned_block.join(other._block, how="left")
        self_len = len(self._block.value_columns)
        cond_len = len(cond._block.value_columns)

        ids = aligned_block.value_columns[:self_len]
        labels = aligned_block.column_labels[:self_len]
        self_col = {x: ex.deref(y) for x, y in zip(labels, ids)}

        if isinstance(cond, bigframes.series.Series) and cond.name in self_col:
            # This is when 'cond' is a valid series.
            y = aligned_block.value_columns[self_len]
            cond_col = {x: ex.deref(y) for x in self_col.keys()}
        else:
            # This is when 'cond' is a dataframe.
            ids = aligned_block.value_columns[self_len : self_len + cond_len]
            labels = aligned_block.column_labels[self_len : self_len + cond_len]
            cond_col = {x: ex.deref(y) for x, y in zip(labels, ids)}

        if isinstance(other, DataFrame):
            other_len = len(self._block.value_columns)
            ids = aligned_block.value_columns[-other_len:]
            labels = aligned_block.column_labels[-other_len:]
            other_col = {x: ex.deref(y) for x, y in zip(labels, ids)}
        else:
            # This is when 'other' is None or constant.
            labels = aligned_block.column_labels[:self_len]
            other_col = {x: ex.const(other) for x in labels}  # type: ignore

        result_series = {}
        for x, self_id in self_col.items():
            cond_id = cond_col[x] if x in cond_col else ex.const(False)
            other_id = other_col[x] if x in other_col else ex.const(None)
            result_block, result_id = aligned_block.project_expr(
                ops.where_op.as_expr(self_id, cond_id, other_id)
            )
            series = bigframes.series.Series(
                result_block.select_column(result_id).with_column_labels([x])
            )
            result_series[x] = series

        result = DataFrame(result_series)
        result.columns.name = self.columns.name
        result.columns.names = self.columns.names
        return result

    def mask(self, cond, other=None):
        return self.where(~cond, other=other)

    def dropna(
        self,
        *,
        axis: int | str = 0,
        how: str = "any",
        subset: typing.Union[None, blocks.Label, Sequence[blocks.Label]] = None,
        inplace: bool = False,
        ignore_index=False,
    ) -> DataFrame:
        if inplace:
            raise NotImplementedError(
                f"'inplace'=True not supported. {constants.FEEDBACK_LINK}"
            )
        if how not in ("any", "all"):
            raise ValueError("'how' must be one of 'any', 'all'")

        axis_n = utils.get_axis_number(axis)

        if subset is not None and axis_n != 0:
            raise NotImplementedError(
                f"subset only supported when axis=0. {constants.FEEDBACK_LINK}"
            )

        if axis_n == 0:
            # subset needs to be converted into column IDs, not column labels.
            if subset is None:
                subset_ids = None
            elif not utils.is_list_like(subset):
                subset_ids = [id_ for id_ in self._block.label_to_col_id[subset]]
            else:
                subset_ids = [
                    id_
                    for label in subset
                    for id_ in self._block.label_to_col_id[label]
                ]

            result = block_ops.dropna(self._block, self._block.value_columns, how=how, subset=subset_ids)  # type: ignore
            if ignore_index:
                result = result.reset_index()
            return DataFrame(result)
        else:
            isnull_block = self._block.multi_apply_unary_op(ops.isnull_op)
            if how == "any":
                null_locations = DataFrame(isnull_block).any().to_pandas()
            else:  # 'all'
                null_locations = DataFrame(isnull_block).all().to_pandas()
            keep_columns = [
                col
                for col, to_drop in zip(self._block.value_columns, null_locations)
                if not to_drop
            ]
            return DataFrame(self._block.select_columns(keep_columns))

    def any(
        self,
        *,
        axis: typing.Union[str, int] = 0,
        bool_only: bool = False,
    ) -> bigframes.series.Series:
        if not bool_only:
            frame = self._raise_on_non_boolean("any")
        else:
            frame = self._drop_non_bool()
        block = frame._block.aggregate_all_and_stack(agg_ops.any_op, axis=axis)
        return bigframes.series.Series(block)

    def all(
        self, axis: typing.Union[str, int] = 0, *, bool_only: bool = False
    ) -> bigframes.series.Series:
        if not bool_only:
            frame = self._raise_on_non_boolean("all")
        else:
            frame = self._drop_non_bool()
        block = frame._block.aggregate_all_and_stack(agg_ops.all_op, axis=axis)
        return bigframes.series.Series(block)

    def sum(
        self, axis: typing.Union[str, int] = 0, *, numeric_only: bool = False
    ) -> bigframes.series.Series:
        if not numeric_only:
            frame = self._raise_on_non_numeric("sum")
        else:
            frame = self._drop_non_numeric()
        block = frame._block.aggregate_all_and_stack(agg_ops.sum_op, axis=axis)
        return bigframes.series.Series(block)

    def mean(
        self, axis: typing.Union[str, int] = 0, *, numeric_only: bool = False
    ) -> bigframes.series.Series:
        if not numeric_only:
            frame = self._raise_on_non_numeric("mean")
        else:
            frame = self._drop_non_numeric()
        block = frame._block.aggregate_all_and_stack(agg_ops.mean_op, axis=axis)
        return bigframes.series.Series(block)

    def median(
        self, *, numeric_only: bool = False, exact: bool = True
    ) -> bigframes.series.Series:
        if not numeric_only:
            frame = self._raise_on_non_numeric("median")
        else:
            frame = self._drop_non_numeric()
        if exact:
            result = frame.quantile()
            result.name = None
            return result
        else:
            block = frame._block.aggregate_all_and_stack(agg_ops.median_op)
            return bigframes.series.Series(block)

    def quantile(
        self, q: Union[float, Sequence[float]] = 0.5, *, numeric_only: bool = False
    ):
        if not numeric_only:
            frame = self._raise_on_non_numeric("median")
        else:
            frame = self._drop_non_numeric()
        multi_q = utils.is_list_like(q)
        result = block_ops.quantile(
            frame._block, frame._block.value_columns, qs=tuple(q) if multi_q else (q,)  # type: ignore
        )
        if multi_q:
            return DataFrame(result.stack()).droplevel(0)
        else:
            # Drop the last level, which contains q, unnecessary since only one q
            result = result.with_column_labels(result.column_labels.droplevel(-1))
            result, index_col = result.create_constant(q, None)
            result = result.set_index([index_col])
            return bigframes.series.Series(
                result.transpose(original_row_index=pandas.Index([q]))
            )

    def std(
        self, axis: typing.Union[str, int] = 0, *, numeric_only: bool = False
    ) -> bigframes.series.Series:
        if not numeric_only:
            frame = self._raise_on_non_numeric("std")
        else:
            frame = self._drop_non_numeric()
        block = frame._block.aggregate_all_and_stack(agg_ops.std_op, axis=axis)
        return bigframes.series.Series(block)

    def var(
        self, axis: typing.Union[str, int] = 0, *, numeric_only: bool = False
    ) -> bigframes.series.Series:
        if not numeric_only:
            frame = self._raise_on_non_numeric("var")
        else:
            frame = self._drop_non_numeric()
        block = frame._block.aggregate_all_and_stack(agg_ops.var_op, axis=axis)
        return bigframes.series.Series(block)

    def min(
        self, axis: typing.Union[str, int] = 0, *, numeric_only: bool = False
    ) -> bigframes.series.Series:
        if not numeric_only:
            frame = self._raise_on_non_numeric("min")
        else:
            frame = self._drop_non_numeric()
        block = frame._block.aggregate_all_and_stack(agg_ops.min_op, axis=axis)
        return bigframes.series.Series(block)

    def max(
        self, axis: typing.Union[str, int] = 0, *, numeric_only: bool = False
    ) -> bigframes.series.Series:
        if not numeric_only:
            frame = self._raise_on_non_numeric("max")
        else:
            frame = self._drop_non_numeric()
        block = frame._block.aggregate_all_and_stack(agg_ops.max_op, axis=axis)
        return bigframes.series.Series(block)

    def prod(
        self, axis: typing.Union[str, int] = 0, *, numeric_only: bool = False
    ) -> bigframes.series.Series:
        if not numeric_only:
            frame = self._raise_on_non_numeric("prod")
        else:
            frame = self._drop_non_numeric()
        block = frame._block.aggregate_all_and_stack(agg_ops.product_op, axis=axis)
        return bigframes.series.Series(block)

    product = prod
    product.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.prod)

    def count(self, *, numeric_only: bool = False) -> bigframes.series.Series:
        if not numeric_only:
            frame = self
        else:
            frame = self._drop_non_numeric()
        block = frame._block.aggregate_all_and_stack(agg_ops.count_op)
        return bigframes.series.Series(block)

    def nunique(self) -> bigframes.series.Series:
        block = self._block.aggregate_all_and_stack(agg_ops.nunique_op)
        return bigframes.series.Series(block)

    def agg(
        self,
        func: str
        | typing.Sequence[str]
        | typing.Mapping[blocks.Label, typing.Sequence[str] | str],
    ) -> DataFrame | bigframes.series.Series:
        if utils.is_dict_like(func):
            # Must check dict-like first because dictionaries are list-like
            # according to Pandas.

            aggs = []
            labels = []
            funcnames = []
            for col_label, agg_func in func.items():
                agg_func_list = agg_func if utils.is_list_like(agg_func) else [agg_func]
                col_id = self._block.resolve_label_exact(col_label)
                if col_id is None:
                    raise KeyError(f"Column {col_label} does not exist")
                for agg_func in agg_func_list:
                    agg_op = agg_ops.lookup_agg_func(typing.cast(str, agg_func))
                    agg_expr = (
                        ex.UnaryAggregation(agg_op, ex.deref(col_id))
                        if isinstance(agg_op, agg_ops.UnaryAggregateOp)
                        else ex.NullaryAggregation(agg_op)
                    )
                    aggs.append(agg_expr)
                    labels.append(col_label)
                    funcnames.append(agg_func)

            # if any list in dict values, format output differently
            if any(utils.is_list_like(v) for v in func.values()):
                new_index, _ = self.columns.reindex(labels)
                new_index = utils.combine_indices(new_index, pandas.Index(funcnames))
                agg_block, _ = self._block.aggregate(
                    aggregations=aggs, column_labels=new_index
                )
                return DataFrame(agg_block).stack().droplevel(0, axis="index")
            else:
                new_index, _ = self.columns.reindex(labels)
                agg_block, _ = self._block.aggregate(
                    aggregations=aggs, column_labels=new_index
                )
                return bigframes.series.Series(
                    agg_block.transpose(
                        single_row_mode=True, original_row_index=pandas.Index([None])
                    )
                )
        elif utils.is_list_like(func):
            aggregations = [agg_ops.lookup_agg_func(f) for f in func]

            for dtype, agg in itertools.product(self.dtypes, aggregations):
                agg.output_type(
                    dtype
                )  # Raises exception if the agg does not support the dtype.

            return DataFrame(
                self._block.summarize(
                    self._block.value_columns,
                    aggregations,
                )
            )

        else:  # function name string
            return bigframes.series.Series(
                self._block.aggregate_all_and_stack(
                    agg_ops.lookup_agg_func(typing.cast(str, func))
                )
            )

    aggregate = agg
    aggregate.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.agg)

    @validations.requires_index
    @validations.requires_ordering()
    def idxmin(self) -> bigframes.series.Series:
        return bigframes.series.Series(block_ops.idxmin(self._block))

    @validations.requires_index
    @validations.requires_ordering()
    def idxmax(self) -> bigframes.series.Series:
        return bigframes.series.Series(block_ops.idxmax(self._block))

    @validations.requires_ordering()
    def melt(
        self,
        id_vars: typing.Optional[typing.Iterable[typing.Hashable]] = None,
        value_vars: typing.Optional[typing.Iterable[typing.Hashable]] = None,
        var_name: typing.Union[
            typing.Hashable, typing.Sequence[typing.Hashable]
        ] = None,
        value_name: typing.Hashable = "value",
    ):
        if var_name is None:
            # Determine default var_name. Attempt to use column labels if they are unique
            if self.columns.nlevels > 1:
                if len(set(self.columns.names)) == len(self.columns.names):
                    var_name = self.columns.names
                else:
                    var_name = [f"variable_{i}" for i in range(len(self.columns.names))]
            else:
                var_name = self.columns.name or "variable"

        var_name = tuple(var_name) if utils.is_list_like(var_name) else (var_name,)

        if id_vars is not None:
            id_col_ids = [self._resolve_label_exact(col) for col in id_vars]
        else:
            id_col_ids = []
        if value_vars is not None:
            val_col_ids = [self._resolve_label_exact(col) for col in value_vars]
        else:
            val_col_ids = [
                col_id
                for col_id in self._block.value_columns
                if col_id not in id_col_ids
            ]

        return DataFrame(
            self._block.melt(id_col_ids, val_col_ids, var_name, value_name)
        )

    def describe(self, include: None | Literal["all"] = None) -> DataFrame:
        from bigframes.pandas.core.methods import describe

        return typing.cast(DataFrame, describe.describe(self, include))

    def skew(self, *, numeric_only: bool = False):
        if not numeric_only:
            frame = self._raise_on_non_numeric("skew")
        else:
            frame = self._drop_non_numeric()
        result_block = block_ops.skew(frame._block, frame._block.value_columns)
        return bigframes.series.Series(result_block)

    def kurt(self, *, numeric_only: bool = False):
        if not numeric_only:
            frame = self._raise_on_non_numeric("kurt")
        else:
            frame = self._drop_non_numeric()
        result_block = block_ops.kurt(frame._block, frame._block.value_columns)
        return bigframes.series.Series(result_block)

    kurtosis = kurt
    kurtosis.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.kurt)

    def _pivot(
        self,
        *,
        columns: typing.Union[blocks.Label, Sequence[blocks.Label]],
        columns_unique_values: typing.Optional[
            typing.Union[pandas.Index, Sequence[object]]
        ] = None,
        index: typing.Optional[
            typing.Union[blocks.Label, Sequence[blocks.Label]]
        ] = None,
        values: typing.Optional[
            typing.Union[blocks.Label, Sequence[blocks.Label]]
        ] = None,
    ) -> DataFrame:
        if index:
            block = self.set_index(index)._block
        else:
            block = self._block

        column_ids = self._sql_names(columns)
        if values:
            value_col_ids = self._sql_names(values)
        else:
            value_col_ids = [
                col for col in block.value_columns if col not in column_ids
            ]

        pivot_block = block.pivot(
            columns=column_ids,
            values=value_col_ids,
            columns_unique_values=columns_unique_values,
            values_in_index=utils.is_list_like(values),
        )
        return DataFrame(pivot_block)

    @validations.requires_index
    @validations.requires_ordering()
    def pivot(
        self,
        *,
        columns: typing.Union[blocks.Label, Sequence[blocks.Label]],
        index: typing.Optional[
            typing.Union[blocks.Label, Sequence[blocks.Label]]
        ] = None,
        values: typing.Optional[
            typing.Union[blocks.Label, Sequence[blocks.Label]]
        ] = None,
    ) -> DataFrame:
        return self._pivot(columns=columns, index=index, values=values)

    @validations.requires_index
    @validations.requires_ordering()
    def pivot_table(
        self,
        values: typing.Optional[
            typing.Union[blocks.Label, Sequence[blocks.Label]]
        ] = None,
        index: typing.Optional[
            typing.Union[blocks.Label, Sequence[blocks.Label]]
        ] = None,
        columns: typing.Union[blocks.Label, Sequence[blocks.Label]] = None,
        aggfunc: str = "mean",
    ) -> DataFrame:
        if isinstance(index, Iterable) and not (
            isinstance(index, blocks.Label) and index in self.columns
        ):
            index = list(index)
        else:
            index = [index]

        if isinstance(columns, Iterable) and not (
            isinstance(columns, blocks.Label) and columns in self.columns
        ):
            columns = list(columns)
        else:
            columns = [columns]

        if isinstance(values, Iterable) and not (
            isinstance(values, blocks.Label) and values in self.columns
        ):
            values = list(values)
        else:
            values = [values]

        # Unlike pivot, pivot_table has values always ordered.
        values.sort(key=lambda val: typing.cast("SupportsRichComparison", val))

        keys = index + columns
        agged = self.groupby(keys, dropna=True)[values].agg(aggfunc)

        if isinstance(agged, bigframes.series.Series):
            agged = agged.to_frame()

        agged = agged.dropna(how="all")

        if len(values) == 1:
            agged = agged.rename(columns={agged.columns[0]: values[0]})

        agged = agged.reset_index()

        pivoted = agged.pivot(
            columns=columns,
            index=index,
            values=values if len(values) > 1 else None,
        ).sort_index()

        # TODO: Remove the reordering step once the issue is resolved.
        # The pivot_table method results in multi-index columns that are always ordered.
        # However, the order of the pivoted result columns is not guaranteed to be sorted.
        # Sort and reorder.
        return pivoted[pivoted.columns.sort_values()]

    def stack(self, level: LevelsType = -1):
        if not isinstance(self.columns, pandas.MultiIndex):
            if level not in [0, -1, self.columns.name]:
                raise IndexError(f"Invalid level {level} for single-level index")
            return self._stack_mono()
        return self._stack_multi(level)

    def _stack_mono(self):
        result_block = self._block.stack()
        return bigframes.series.Series(result_block)

    def _stack_multi(self, level: LevelsType = -1):
        n_levels = self.columns.nlevels
        if not utils.is_list_like(level):
            level = [level]
        level_indices = []
        for level_ref in level:
            if isinstance(level_ref, int):
                if level_ref < 0:
                    level_indices.append(n_levels + level_ref)
                else:
                    level_indices.append(level_ref)
            else:  # str
                level_indices.append(self.columns.names.index(level_ref))  # type: ignore

        new_order = [
            *[i for i in range(n_levels) if i not in level_indices],
            *level_indices,
        ]

        original_columns = typing.cast(pandas.MultiIndex, self.columns)
        new_columns = original_columns.reorder_levels(new_order)

        block = self._block.with_column_labels(new_columns)

        block = block.stack(levels=len(level))
        return DataFrame(block)

    @validations.requires_index
    @validations.requires_ordering()
    def unstack(self, level: LevelsType = -1):
        if not utils.is_list_like(level):
            level = [level]

        block = self._block
        # Special case, unstack with mono-index transpose into a series
        if self.index.nlevels == 1:
            block = block.stack(how="right", levels=self.columns.nlevels)
            return bigframes.series.Series(block)

        # Pivot by index levels
        unstack_ids = self._resolve_levels(level)
        block = block.reset_index(drop=False)
        block = block.set_index(
            [col for col in self._block.index_columns if col not in unstack_ids]
        )

        pivot_block = block.pivot(
            columns=unstack_ids,
            values=self._block.value_columns,
            values_in_index=True,
        )
        return DataFrame(pivot_block)

    def _drop_non_numeric(self, permissive=True) -> DataFrame:
        numeric_types = (
            set(bigframes.dtypes.NUMERIC_BIGFRAMES_TYPES_PERMISSIVE)
            if permissive
            else set(bigframes.dtypes.NUMERIC_BIGFRAMES_TYPES_RESTRICTIVE)
        )
        non_numeric_cols = [
            col_id
            for col_id, dtype in zip(self._block.value_columns, self._block.dtypes)
            if dtype not in numeric_types
        ]
        return DataFrame(self._block.drop_columns(non_numeric_cols))

    def _drop_non_bool(self) -> DataFrame:
        non_bool_cols = [
            col_id
            for col_id, dtype in zip(self._block.value_columns, self._block.dtypes)
            if dtype not in bigframes.dtypes.BOOL_BIGFRAMES_TYPES
        ]
        return DataFrame(self._block.drop_columns(non_bool_cols))

    def _raise_on_non_numeric(self, op: str):
        if not all(
            dtype in bigframes.dtypes.NUMERIC_BIGFRAMES_TYPES_PERMISSIVE
            for dtype in self._block.dtypes
        ):
            raise NotImplementedError(
                f"'{op}' does not support non-numeric columns. "
                f"Set 'numeric_only'=True to ignore non-numeric columns. {constants.FEEDBACK_LINK}"
            )
        return self

    def _raise_on_non_boolean(self, op: str):
        if not all(
            dtype in bigframes.dtypes.BOOL_BIGFRAMES_TYPES
            for dtype in self._block.dtypes
        ):
            raise NotImplementedError(
                f"'{op}' does not support non-bool columns. "
                f"Set 'bool_only'=True to ignore non-bool columns. {constants.FEEDBACK_LINK}"
            )
        return self

    def merge(
        self,
        right: DataFrame,
        how: Literal[
            "inner",
            "left",
            "outer",
            "right",
            "cross",
        ] = "inner",
        on: Union[blocks.Label, Sequence[blocks.Label], None] = None,
        *,
        left_on: Union[blocks.Label, Sequence[blocks.Label], None] = None,
        right_on: Union[blocks.Label, Sequence[blocks.Label], None] = None,
        sort: bool = False,
        suffixes: tuple[str, str] = ("_x", "_y"),
    ) -> DataFrame:
        if how == "cross":
            if on is not None:
                raise ValueError("'on' is not supported for cross join.")
            result_block = self._block.merge(
                right._block,
                left_join_ids=[],
                right_join_ids=[],
                suffixes=suffixes,
                how=how,
                sort=True,
            )
            return DataFrame(result_block)

        if on is None:
            if left_on is None or right_on is None:
                raise ValueError("Must specify `on` or `left_on` + `right_on`.")
        else:
            if left_on is not None or right_on is not None:
                raise ValueError(
                    "Can not pass both `on` and `left_on` + `right_on` params."
                )
            left_on, right_on = on, on

        if utils.is_list_like(left_on):
            left_on = list(left_on)  # type: ignore
        else:
            left_on = [left_on]

        if utils.is_list_like(right_on):
            right_on = list(right_on)  # type: ignore
        else:
            right_on = [right_on]

        left_join_ids = []
        for label in left_on:  # type: ignore
            left_col_id = self._resolve_label_exact(label)
            # 0 elements already throws an exception
            if not left_col_id:
                raise ValueError(f"No column {label} found in self.")
            left_join_ids.append(left_col_id)

        right_join_ids = []
        for label in right_on:  # type: ignore
            right_col_id = right._resolve_label_exact(label)
            if not right_col_id:
                raise ValueError(f"No column {label} found in other.")
            right_join_ids.append(right_col_id)

        block = self._block.merge(
            right._block,
            how,
            left_join_ids,
            right_join_ids,
            sort=sort,
            suffixes=suffixes,
        )
        return DataFrame(block)

    def join(
        self,
        other: Union[DataFrame, bigframes.series.Series],
        *,
        on: Optional[str] = None,
        how: str = "left",
    ) -> DataFrame:
        if isinstance(other, bigframes.series.Series):
            other = other.to_frame()

        left, right = self, other

        if not left.columns.intersection(right.columns).empty:
            raise NotImplementedError(
                f"Deduping column names is not implemented. {constants.FEEDBACK_LINK}"
            )
        if how == "cross":
            if on is not None:
                raise ValueError("'on' is not supported for cross join.")
            result_block = left._block.merge(
                right._block,
                left_join_ids=[],
                right_join_ids=[],
                suffixes=("", ""),
                how="cross",
                sort=True,
            )
            return DataFrame(result_block)

        # Join left columns with right index
        if on is not None:
            if other._block.index.nlevels != 1:
                raise ValueError(
                    "Join on columns must match the index level of the other DataFrame. Join on column with multi-index haven't been supported."
                )
            # Switch left index with on column
            left_columns = left.columns
            left_idx_original_names = left.index.names if left._has_index else ()
            left_idx_names_in_cols = [
                f"bigframes_left_idx_name_{i}"
                for i in range(len(left_idx_original_names))
            ]
            if left._has_index:
                left.index.names = left_idx_names_in_cols
            left = left.reset_index(drop=False)
            left = left.set_index(on)

            # Join on index and switch back
            combined_df = left._perform_join_by_index(right, how=how)
            combined_df.index.name = on
            combined_df = combined_df.reset_index(drop=False)
            combined_df = combined_df.set_index(left_idx_names_in_cols)

            # To be consistent with Pandas
            if combined_df._has_index:
                combined_df.index.names = (
                    left_idx_original_names
                    if how in ("inner", "left")
                    else ([None] * len(combined_df.index.names))
                )

            # Reorder columns
            combined_df = combined_df[list(left_columns) + list(right.columns)]
            return combined_df

        # Join left index with right index
        if left._block.index.nlevels != right._block.index.nlevels:
            raise ValueError("Index to join on must have the same number of levels.")

        return left._perform_join_by_index(right, how=how)

    def _perform_join_by_index(
        self,
        other: Union[DataFrame, indexes.Index],
        *,
        how: str = "left",
        always_order: bool = False,
    ):
        block, _ = self._block.join(
            other._block, how=how, block_identity_join=True, always_order=always_order
        )
        return DataFrame(block)

    @validations.requires_ordering()
    def rolling(
        self,
        window: int | pandas.Timedelta | numpy.timedelta64 | datetime.timedelta | str,
        min_periods=None,
        on: str | None = None,
        closed: Literal["right", "left", "both", "neither"] = "right",
    ) -> bigframes.core.window.Window:
        if isinstance(window, int):
            window_def = windows.WindowSpec(
                bounds=windows.RowsWindowBounds.from_window_size(window, closed),
                min_periods=min_periods if min_periods is not None else window,
            )
            skip_agg_col_id = (
                None if on is None else self._block.resolve_label_exact_or_error(on)
            )
            return bigframes.core.window.Window(
                self._block,
                window_def,
                self._block.value_columns,
                skip_agg_column_id=skip_agg_col_id,
            )

        return rolling.create_range_window(
            self._block,
            window,
            min_periods=min_periods,
            on=on,
            closed=closed,
            is_series=False,
        )

    @validations.requires_ordering()
    def expanding(self, min_periods: int = 1) -> bigframes.core.window.Window:
        window = windows.cumulative_rows(min_periods=min_periods)
        return bigframes.core.window.Window(
            self._block, window, self._block.value_columns
        )

    def groupby(
        self,
        by: typing.Union[
            blocks.Label,
            bigframes.series.Series,
            typing.Sequence[typing.Union[blocks.Label, bigframes.series.Series]],
            None,
        ] = None,
        *,
        level: typing.Optional[LevelsType] = None,
        as_index: bool = True,
        dropna: bool = True,
    ) -> groupby.DataFrameGroupBy:
        if (by is not None) and (level is not None):
            raise ValueError("Do not specify both 'by' and 'level'")
        if by is not None:
            return self._groupby_series(by, as_index=as_index, dropna=dropna)
        if level is not None:
            return self._groupby_level(level, as_index=as_index, dropna=dropna)
        else:
            raise TypeError("You have to supply one of 'by' and 'level'")

    @validations.requires_index
    def _groupby_level(
        self,
        level: LevelsType,
        as_index: bool = True,
        dropna: bool = True,
    ):
        return groupby.DataFrameGroupBy(
            self._block,
            by_col_ids=self._resolve_levels(level),
            as_index=as_index,
            dropna=dropna,
        )

    def _groupby_series(
        self,
        by: typing.Union[
            blocks.Label,
            bigframes.series.Series,
            typing.Sequence[typing.Union[blocks.Label, bigframes.series.Series]],
        ],
        as_index: bool = True,
        dropna: bool = True,
    ):
        if not isinstance(by, bigframes.series.Series) and utils.is_list_like(by):
            by = list(by)
        else:
            by = [typing.cast(typing.Union[blocks.Label, bigframes.series.Series], by)]

        block = self._block
        col_ids: typing.Sequence[str] = []
        for key in by:
            if isinstance(key, bigframes.series.Series):
                block, (
                    get_column_left,
                    get_column_right,
                ) = block.join(key._block, how="inner" if dropna else "left")
                col_ids = [
                    *[get_column_left[value] for value in col_ids],
                    get_column_right[key._value_column],
                ]
            else:
                # Interpret as index level or column name
                col_matches = block.label_to_col_id.get(key, [])
                level_matches = block.index_name_to_col_id.get(key, [])
                matches = [*col_matches, *level_matches]
                if len(matches) != 1:
                    raise ValueError(
                        f"GroupBy key {key} does not match a unique column or index level. BigQuery DataFrames only interprets lists of strings as column or index names, not directly as per-row group assignments."
                    )
                col_ids = [*col_ids, matches[0]]

        return groupby.DataFrameGroupBy(
            block,
            by_col_ids=col_ids,
            as_index=as_index,
            dropna=dropna,
        )

    def abs(self) -> DataFrame:
        return self._apply_unary_op(ops.abs_op)

    def round(self, decimals: Union[int, dict[Hashable, int]] = 0) -> DataFrame:
        is_mapping = utils.is_dict_like(decimals)
        if not (is_mapping or isinstance(decimals, int)):
            raise TypeError("'decimals' must be either a dict-like or integer.")
        block = self._block
        exprs = []
        for label, col_id, dtype in zip(
            block.column_labels, block.value_columns, block.dtypes
        ):
            if dtype in set(bigframes.dtypes.NUMERIC_BIGFRAMES_TYPES_PERMISSIVE) - {
                bigframes.dtypes.BOOL_DTYPE
            }:
                if is_mapping:
                    if label in decimals:  # type: ignore
                        exprs.append(
                            ops.round_op.as_expr(
                                col_id,
                                ex.const(
                                    decimals[label], dtype=bigframes.dtypes.INT_DTYPE  # type: ignore
                                ),
                            )
                        )
                    else:
                        exprs.append(ex.deref(col_id))
                else:
                    exprs.append(
                        ops.round_op.as_expr(
                            col_id,
                            ex.const(
                                typing.cast(int, decimals),
                                dtype=bigframes.dtypes.INT_DTYPE,
                            ),
                        )
                    )
            else:
                exprs.append(ex.deref(col_id))

        return DataFrame(
            block.project_exprs(exprs, labels=block.column_labels, drop=True)
        )

    def isna(self) -> DataFrame:
        return self._apply_unary_op(ops.isnull_op)

    isnull = isna
    isnull.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.isna)

    def notna(self) -> DataFrame:
        return self._apply_unary_op(ops.notnull_op)

    notnull = notna
    notnull.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.notna)

    @validations.requires_ordering()
    def cumsum(self):
        is_numeric_types = [
            (dtype in bigframes.dtypes.NUMERIC_BIGFRAMES_TYPES_PERMISSIVE)
            for _, dtype in self.dtypes.items()
        ]
        if not all(is_numeric_types):
            raise ValueError("All values must be numeric to apply cumsum.")
        return self._apply_window_op(
            agg_ops.sum_op,
            windows.cumulative_rows(),
        )

    @validations.requires_ordering()
    def cumprod(self) -> DataFrame:
        is_numeric_types = [
            (dtype in bigframes.dtypes.NUMERIC_BIGFRAMES_TYPES_PERMISSIVE)
            for _, dtype in self.dtypes.items()
        ]
        if not all(is_numeric_types):
            raise ValueError("All values must be numeric to apply cumsum.")
        return self._apply_window_op(
            agg_ops.product_op,
            windows.cumulative_rows(),
        )

    @validations.requires_ordering()
    def cummin(self) -> DataFrame:
        return self._apply_window_op(
            agg_ops.min_op,
            windows.cumulative_rows(),
        )

    @validations.requires_ordering()
    def cummax(self) -> DataFrame:
        return self._apply_window_op(
            agg_ops.max_op,
            windows.cumulative_rows(),
        )

    @validations.requires_ordering()
    def shift(self, periods: int = 1) -> DataFrame:
        window_spec = windows.rows()
        return self._apply_window_op(agg_ops.ShiftOp(periods), window_spec)

    @validations.requires_ordering()
    def diff(self, periods: int = 1) -> DataFrame:
        window_spec = windows.rows()
        return self._apply_window_op(agg_ops.DiffOp(periods), window_spec)

    @validations.requires_ordering()
    def pct_change(self, periods: int = 1) -> DataFrame:
        # Future versions of pandas will not perfrom ffill automatically
        df = self.ffill()
        return DataFrame(block_ops.pct_change(df._block, periods=periods))

    def _apply_window_op(
        self,
        op: agg_ops.UnaryWindowOp,
        window_spec: windows.WindowSpec,
    ):
        block, result_ids = self._block.multi_apply_window_op(
            self._block.value_columns,
            op,
            window_spec=window_spec,
        )
        return DataFrame(block.select_columns(result_ids))

    @validations.requires_ordering()
    def sample(
        self,
        n: Optional[int] = None,
        frac: Optional[float] = None,
        *,
        random_state: Optional[int] = None,
        sort: Optional[bool | Literal["random"]] = "random",
    ) -> DataFrame:
        if n is not None and frac is not None:
            raise ValueError("Only one of 'n' or 'frac' parameter can be specified.")

        ns = (n,) if n is not None else ()
        fracs = (frac,) if frac is not None else ()
        return DataFrame(
            self._block.split(ns=ns, fracs=fracs, random_state=random_state, sort=sort)[
                0
            ]
        )

    def explode(
        self,
        column: typing.Union[blocks.Label, typing.Sequence[blocks.Label]],
        *,
        ignore_index: Optional[bool] = False,
    ) -> DataFrame:
        column_labels = bigframes.core.explode.check_column(column)

        column_ids = [self._resolve_label_exact(label) for label in column_labels]
        missing = [
            column_labels[i] for i in range(len(column_ids)) if column_ids[i] is None
        ]
        if len(missing) > 0:
            raise KeyError(f"None of {missing} are in the columns")

        return DataFrame(
            self._block.explode(
                column_ids=typing.cast(typing.Sequence[str], tuple(column_ids)),
                ignore_index=ignore_index,
            )
        )

    def _split(
        self,
        ns: Iterable[int] = (),
        fracs: Iterable[float] = (),
        *,
        random_state: Optional[int] = None,
    ) -> List[DataFrame]:
        """Internal function to support splitting DF to multiple parts along index axis.

        At most one of ns and fracs can be passed in. If neither, default to ns = (1,).
        Return a list of sampled DataFrames.
        """
        blocks = self._block.split(ns=ns, fracs=fracs, random_state=random_state)
        return [DataFrame(block) for block in blocks]

    @validations.requires_ordering()
    def _resample(
        self,
        rule: str,
        *,
        on: blocks.Label = None,
        level: Optional[LevelsType] = None,
        origin: Union[
            Union[
                pandas.Timestamp, datetime.datetime, numpy.datetime64, int, float, str
            ],
            Literal["epoch", "start", "start_day", "end", "end_day"],
        ] = "start_day",
    ) -> bigframes.core.groupby.DataFrameGroupBy:
        """Internal function to support resample. Resample time-series data.

        **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import pandas as pd
        >>> bpd.options.display.progress_bar = None

        >>> data = {
        ...     "timestamp_col": pd.date_range(
        ...         start="2021-01-01 13:00:00", periods=30, freq="1s"
        ...     ),
        ...     "int64_col": range(30),
        ...     "int64_too": range(10, 40),
        ... }

        Resample on a DataFrame with index:

        >>> df = bpd.DataFrame(data).set_index("timestamp_col")
        >>> df._resample(rule="7s").min()
                             int64_col  int64_too
        2021-01-01 12:59:55          0         10
        2021-01-01 13:00:02          2         12
        2021-01-01 13:00:09          9         19
        2021-01-01 13:00:16         16         26
        2021-01-01 13:00:23         23         33
        <BLANKLINE>
        [5 rows x 2 columns]

        Resample with column and origin set to 'start':

        >>> df = bpd.DataFrame(data)
        >>> df._resample(rule="7s", on = "timestamp_col", origin="start").min()
                             int64_col  int64_too
        2021-01-01 13:00:00          0         10
        2021-01-01 13:00:07          7         17
        2021-01-01 13:00:14         14         24
        2021-01-01 13:00:21         21         31
        2021-01-01 13:00:28         28         38
        <BLANKLINE>
        [5 rows x 2 columns]

        Args:
            rule (str):
                The offset string representing target conversion.
            on (str, default None):
                For a DataFrame, column to use instead of index for resampling. Column
                must be datetime-like.
            level (str or int, default None):
                For a MultiIndex, level (name or number) to use for resampling.
                level must be datetime-like.
            origin(str, default 'start_day'):
                The timestamp on which to adjust the grouping. Must be one of the following:
                'epoch': origin is 1970-01-01
                'start': origin is the first value of the timeseries
                'start_day': origin is the first day at midnight of the timeseries
        Returns:
            DataFrameGroupBy: DataFrameGroupBy object.
        """
        block = self._block._generate_resample_label(
            rule=rule,
            on=on,
            level=level,
            origin=origin,
        )
        df = DataFrame(block)
        return df.groupby(level=0)

    @classmethod
    def from_dict(
        cls,
        data: dict,
        orient: str = "columns",
        dtype=None,
        columns=None,
    ) -> DataFrame:
        return cls(pandas.DataFrame.from_dict(data, orient, dtype, columns))  # type: ignore

    @classmethod
    def from_records(
        cls,
        data,
        index=None,
        exclude=None,
        columns=None,
        coerce_float: bool = False,
        nrows: int | None = None,
    ) -> DataFrame:
        return cls(
            pandas.DataFrame.from_records(
                data, index, exclude, columns, coerce_float, nrows
            )
        )

    def to_csv(
        self,
        path_or_buf=None,
        sep=",",
        *,
        header: bool = True,
        index: bool = True,
        allow_large_results: Optional[bool] = None,
    ) -> Optional[str]:
        # TODO(swast): Can we support partition columns argument?
        # TODO(chelsealin): Support local file paths.
        # TODO(swast): Some warning that wildcard is recommended for large
        # query results? See:
        # https://cloud.google.com/bigquery/docs/exporting-data#limit_the_exported_file_size
        if not utils.is_gcs_path(path_or_buf):
            pd_df = self.to_pandas(allow_large_results=allow_large_results)
            return pd_df.to_csv(path_or_buf, sep=sep, header=header, index=index)
        if "*" not in path_or_buf:
            raise NotImplementedError(ERROR_IO_REQUIRES_WILDCARD)

        export_array, id_overrides = self._prepare_export(
            index=index and self._has_index,
            ordering_id=bigframes.session._io.bigquery.IO_ORDERING_ID,
        )
        options = {
            "field_delimiter": sep,
            "header": header,
        }
        query_job = self._session._executor.export_gcs(
            export_array.rename_columns(id_overrides),
            path_or_buf,
            format="csv",
            export_options=options,
        )
        self._set_internal_query_job(query_job)
        return None

    def to_json(
        self,
        path_or_buf=None,
        orient: Optional[
            Literal["split", "records", "index", "columns", "values", "table"]
        ] = None,
        *,
        lines: bool = False,
        index: bool = True,
        allow_large_results: Optional[bool] = None,
    ) -> Optional[str]:
        # TODO(swast): Can we support partition columns argument?
        if not utils.is_gcs_path(path_or_buf):
            pd_df = self.to_pandas(allow_large_results=allow_large_results)
            return pd_df.to_json(
                path_or_buf,
                orient=orient,
                lines=lines,
                index=index,
                default_handler=str,
            )
        if "*" not in path_or_buf:
            raise NotImplementedError(ERROR_IO_REQUIRES_WILDCARD)

        # TODO(ashleyxu) Support lines=False for small tables with arrays and TO_JSON_STRING.
        # See: https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#to_json_string
        if lines is False:
            raise NotImplementedError(
                f"Only newline-delimited JSON is supported. Add `lines=True` to your function call. {constants.FEEDBACK_LINK}"
            )

        if lines is True and orient != "records":
            raise ValueError(
                "'lines' keyword is only valid when 'orient' is 'records'."
            )

        export_array, id_overrides = self._prepare_export(
            index=index and self._has_index,
            ordering_id=bigframes.session._io.bigquery.IO_ORDERING_ID,
        )
        query_job = self._session._executor.export_gcs(
            export_array.rename_columns(id_overrides),
            path_or_buf,
            format="json",
            export_options={},
        )
        self._set_internal_query_job(query_job)
        return None

    def to_gbq(
        self,
        destination_table: Optional[str] = None,
        *,
        if_exists: Optional[Literal["fail", "replace", "append"]] = None,
        index: bool = True,
        ordering_id: Optional[str] = None,
        clustering_columns: Union[pandas.Index, Iterable[typing.Hashable]] = (),
        labels: dict[str, str] = {},
    ) -> str:
        index = index and self._has_index
        temp_table_ref = None

        if destination_table is None:
            if if_exists is not None and if_exists != "replace":
                raise ValueError(
                    f"Got invalid value {repr(if_exists)} for if_exists. "
                    "When no destination table is specified, a new table is always created. "
                    "None or 'replace' are the only valid options in this case."
                )
            if_exists = "replace"

            # The client code owns this table reference now
            temp_table_ref = (
                self._session._anon_dataset_manager.generate_unique_resource_id()
            )
            destination_table = f"{temp_table_ref.project}.{temp_table_ref.dataset_id}.{temp_table_ref.table_id}"

        table_parts = destination_table.split(".")
        default_project = self._block.expr.session.bqclient.project

        if len(table_parts) == 2:
            destination_dataset = f"{default_project}.{table_parts[0]}"
        elif len(table_parts) == 3:
            destination_dataset = f"{table_parts[0]}.{table_parts[1]}"
        else:
            raise ValueError(
                f"Got invalid value for destination_table {repr(destination_table)}. "
                "Should be of the form 'datasetId.tableId' or 'projectId.datasetId.tableId'."
            )

        if if_exists is None:
            if_exists = "fail"

        valid_if_exists = ["fail", "replace", "append"]
        if if_exists not in valid_if_exists:
            raise ValueError(
                f"Got invalid value {repr(if_exists)} for if_exists. "
                f"Valid options include None or one of {valid_if_exists}."
            )

        try:
            self._session.bqclient.get_dataset(destination_dataset)
        except google.api_core.exceptions.NotFound:
            self._session.bqclient.create_dataset(destination_dataset, exists_ok=True)

        clustering_fields = self._map_clustering_columns(
            clustering_columns, index=index
        )

        export_array, id_overrides = self._prepare_export(
            index=index and self._has_index, ordering_id=ordering_id
        )
        destination: bigquery.table.TableReference = (
            bigquery.table.TableReference.from_string(
                destination_table,
                default_project=default_project,
            )
        )

        query_job = self._session._executor.export_gbq(
            export_array.rename_columns(id_overrides),
            destination=destination,
            cluster_cols=clustering_fields,
            if_exists=if_exists,
        )
        self._set_internal_query_job(query_job)

        # The query job should have finished, so there should be always be a result table.
        result_table = query_job.destination
        assert result_table is not None

        if temp_table_ref:
            bigframes.session._io.bigquery.set_table_expiration(
                self._session.bqclient,
                temp_table_ref,
                datetime.datetime.now(datetime.timezone.utc)
                + bigframes.constants.DEFAULT_EXPIRATION,
            )

        if len(labels) != 0:
            table = bigquery.Table(result_table)
            table.labels = labels
            self._session.bqclient.update_table(table, ["labels"])

        return destination_table

    def to_numpy(
        self,
        dtype=None,
        copy=False,
        na_value=pd_ext.no_default,
        *,
        allow_large_results=None,
        **kwargs,
    ) -> numpy.ndarray:
        return self.to_pandas(allow_large_results=allow_large_results).to_numpy(
            dtype, copy, na_value, **kwargs
        )

    def __array__(self, dtype=None, copy: Optional[bool] = None) -> numpy.ndarray:
        if copy is False:
            raise ValueError("Cannot convert to array without copy.")
        return self.to_numpy(dtype=dtype)

    __array__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__array__)

    def to_parquet(
        self,
        path=None,
        *,
        compression: Optional[Literal["snappy", "gzip"]] = "snappy",
        index: bool = True,
        allow_large_results: Optional[bool] = None,
    ) -> Optional[bytes]:
        # TODO(swast): Can we support partition columns argument?
        # TODO(chelsealin): Support local file paths.
        # TODO(swast): Some warning that wildcard is recommended for large
        # query results? See:
        # https://cloud.google.com/bigquery/docs/exporting-data#limit_the_exported_file_size
        if not utils.is_gcs_path(path):
            pd_df = self.to_pandas(allow_large_results=allow_large_results)
            return pd_df.to_parquet(path, compression=compression, index=index)
        if "*" not in path:
            raise NotImplementedError(ERROR_IO_REQUIRES_WILDCARD)

        if compression not in {None, "snappy", "gzip"}:
            raise ValueError("'{0}' is not valid for compression".format(compression))

        export_options: Dict[str, Union[bool, str]] = {}
        if compression:
            export_options["compression"] = compression.upper()

        export_array, id_overrides = self._prepare_export(
            index=index and self._has_index,
            ordering_id=bigframes.session._io.bigquery.IO_ORDERING_ID,
        )
        query_job = self._session._executor.export_gcs(
            export_array.rename_columns(id_overrides),
            path,
            format="parquet",
            export_options=export_options,
        )
        self._set_internal_query_job(query_job)
        return None

    def to_dict(
        self,
        orient: Literal[
            "dict", "list", "series", "split", "tight", "records", "index"
        ] = "dict",
        into: type[dict] = dict,
        *,
        allow_large_results: Optional[bool] = None,
        **kwargs,
    ) -> dict | list[dict]:
        return self.to_pandas(allow_large_results=allow_large_results).to_dict(orient, into, **kwargs)  # type: ignore

    def to_excel(
        self,
        excel_writer,
        sheet_name: str = "Sheet1",
        *,
        allow_large_results: Optional[bool] = None,
        **kwargs,
    ) -> None:
        return self.to_pandas(allow_large_results=allow_large_results).to_excel(
            excel_writer, sheet_name, **kwargs
        )

    def to_latex(
        self,
        buf=None,
        columns: Sequence | None = None,
        header: bool | Sequence[str] = True,
        index: bool = True,
        *,
        allow_large_results: Optional[bool] = None,
        **kwargs,
    ) -> str | None:
        return self.to_pandas(allow_large_results=allow_large_results).to_latex(
            buf, columns=columns, header=header, index=index, **kwargs  # type: ignore
        )

    def to_records(
        self,
        index: bool = True,
        column_dtypes=None,
        index_dtypes=None,
        *,
        allow_large_results=None,
    ) -> numpy.recarray:
        return self.to_pandas(allow_large_results=allow_large_results).to_records(
            index, column_dtypes, index_dtypes
        )

    def to_string(
        self,
        buf=None,
        columns: Sequence[str] | None = None,
        col_space=None,
        header: bool | Sequence[str] = True,
        index: bool = True,
        na_rep: str = "NaN",
        formatters=None,
        float_format=None,
        sparsify: bool | None = None,
        index_names: bool = True,
        justify: str | None = None,
        max_rows: int | None = None,
        max_cols: int | None = None,
        show_dimensions: bool = False,
        decimal: str = ".",
        line_width: int | None = None,
        min_rows: int | None = None,
        max_colwidth: int | None = None,
        encoding: str | None = None,
        *,
        allow_large_results: Optional[bool] = None,
    ) -> str | None:
        return self.to_pandas(allow_large_results=allow_large_results).to_string(
            buf,
            columns,  # type: ignore
            col_space,
            header,  # type: ignore
            index,
            na_rep,
            formatters,
            float_format,
            sparsify,
            index_names,
            justify,
            max_rows,
            max_cols,
            show_dimensions,
            decimal,
            line_width,
            min_rows,
            max_colwidth,
            encoding,
        )

    def to_html(
        self,
        buf=None,
        columns: Sequence[str] | None = None,
        col_space=None,
        header: bool = True,
        index: bool = True,
        na_rep: str = "NaN",
        formatters=None,
        float_format=None,
        sparsify: bool | None = None,
        index_names: bool = True,
        justify: str | None = None,
        max_rows: int | None = None,
        max_cols: int | None = None,
        show_dimensions: bool = False,
        decimal: str = ".",
        bold_rows: bool = True,
        classes: str | list | tuple | None = None,
        escape: bool = True,
        notebook: bool = False,
        border: int | None = None,
        table_id: str | None = None,
        render_links: bool = False,
        encoding: str | None = None,
        *,
        allow_large_results: bool | None = None,
    ) -> str:
        return self.to_pandas(allow_large_results=allow_large_results).to_html(
            buf,
            columns,  # type: ignore
            col_space,
            header,
            index,
            na_rep,
            formatters,
            float_format,
            sparsify,
            index_names,
            justify,  # type: ignore
            max_rows,
            max_cols,
            show_dimensions,
            decimal,
            bold_rows,
            classes,
            escape,
            notebook,
            border,
            table_id,
            render_links,
            encoding,
        )

    def to_markdown(
        self,
        buf=None,
        mode: str = "wt",
        index: bool = True,
        *,
        allow_large_results: Optional[bool] = None,
        **kwargs,
    ) -> str | None:
        return self.to_pandas(allow_large_results=allow_large_results).to_markdown(buf, mode, index, **kwargs)  # type: ignore

    def to_pickle(self, path, *, allow_large_results=None, **kwargs) -> None:
        return self.to_pandas(allow_large_results=allow_large_results).to_pickle(
            path, **kwargs
        )

    def to_orc(self, path=None, *, allow_large_results=None, **kwargs) -> bytes | None:
        as_pandas = self.to_pandas(allow_large_results=allow_large_results)
        # to_orc only works with default index
        as_pandas_default_index = as_pandas.reset_index()
        return as_pandas_default_index.to_orc(path, **kwargs)

    def _apply_unary_op(self, operation: ops.UnaryOp) -> DataFrame:
        block = self._block.multi_apply_unary_op(operation)
        return DataFrame(block)

    def _map_clustering_columns(
        self,
        clustering_columns: Union[pandas.Index, Iterable[typing.Hashable]],
        index: bool,
    ) -> List[str]:
        """Maps the provided clustering columns to the existing columns in the DataFrame."""

        def map_columns_on_occurrence(columns):
            mapped_columns = []
            for col in clustering_columns:
                if col in columns:
                    count = columns.count(col)
                    mapped_columns.extend([col] * count)
            return mapped_columns

        if not clustering_columns:
            return []

        if len(list(clustering_columns)) != len(set(clustering_columns)):
            raise ValueError("Duplicates are not supported in clustering_columns")

        all_possible_columns = (
            (set(self.columns) | set(self.index.names)) if index else set(self.columns)
        )
        missing_columns = set(clustering_columns) - all_possible_columns
        if missing_columns:
            raise ValueError(
                f"Clustering columns not found in DataFrame: {missing_columns}"
            )

        clustering_columns_for_df = map_columns_on_occurrence(
            list(self._block.column_labels)
        )
        clustering_columns_for_index = (
            map_columns_on_occurrence(list(self.index.names)) if index else []
        )

        (
            clustering_columns_for_df,
            clustering_columns_for_index,
        ) = utils.get_standardized_ids(
            clustering_columns_for_df, clustering_columns_for_index
        )

        return clustering_columns_for_index + clustering_columns_for_df

    def _prepare_export(
        self, index: bool, ordering_id: Optional[str]
    ) -> Tuple[bigframes.core.ArrayValue, Dict[str, str]]:
        array_value = self._block.expr

        new_col_labels, new_idx_labels = utils.get_standardized_ids(
            self._block.column_labels, self._block.index.names
        )

        columns = list(self._block.value_columns)
        column_labels = new_col_labels
        # This code drops unnamed indexes to keep consistent with the behavior of
        # most pandas write APIs. The exception is `pandas.to_csv`, which keeps
        # unnamed indexes as `Unnamed: 0`.
        # TODO(chelsealin): check if works for multiple indexes.
        if index and self.index.name is not None:
            columns.extend(self._block.index_columns)
            column_labels.extend(new_idx_labels)
        else:
            array_value = array_value.drop_columns(self._block.index_columns)

        # Make columns in SQL reflect _labels_ not _ids_. Note: This may use
        # the arbitrary unicode column labels feature in BigQuery, which is
        # currently (June 2023) in preview.
        id_overrides = {
            col_id: col_label
            for col_id, col_label in zip(columns, column_labels)
            if (col_id != col_label)
        }

        if ordering_id is not None:
            array_value, internal_ordering_id = array_value.promote_offsets()
            id_overrides[internal_ordering_id] = ordering_id
        return array_value, id_overrides

    def map(self, func, na_action: Optional[str] = None) -> DataFrame:
        if not isinstance(func, bigframes.functions.BigqueryCallableRoutine):
            raise TypeError("the first argument must be callable")

        if na_action not in {None, "ignore"}:
            raise ValueError(f"na_action={na_action} not supported")

        # TODO(shobs): Support **kwargs
        return self._apply_unary_op(
            ops.RemoteFunctionOp(
                function_def=func.udf_def, apply_on_null=(na_action is None)
            )
        )

    def apply(self, func, *, axis=0, args: typing.Tuple = (), **kwargs):
        # In Bigframes BigQuery function, DataFrame '.apply' method is specifically
        # designed to work with row-wise or column-wise operations, where the input
        # to the applied function should be a Series, not a scalar.

        if utils.get_axis_number(axis) == 1:
            msg = bfe.format_message(
                "DataFrame.apply with parameter axis=1 scenario is in preview."
            )
            warnings.warn(msg, category=bfe.FunctionAxisOnePreviewWarning)

            if not isinstance(
                func,
                (
                    bigframes.functions.BigqueryCallableRoutine,
                    bigframes.functions.BigqueryCallableRowRoutine,
                ),
            ):
                raise ValueError(
                    "For axis=1 a BigFrames BigQuery function must be used."
                )

            if func.is_row_processor:
                # Early check whether the dataframe dtypes are currently supported
                # in the bigquery function
                # NOTE: Keep in sync with the value converters used in the gcf code
                # generated in function_template.py
                bigquery_function_supported_dtypes = (
                    bigframes.dtypes.INT_DTYPE,
                    bigframes.dtypes.FLOAT_DTYPE,
                    bigframes.dtypes.BOOL_DTYPE,
                    bigframes.dtypes.BYTES_DTYPE,
                    bigframes.dtypes.STRING_DTYPE,
                )
                supported_dtypes_types = tuple(
                    type(dtype)
                    for dtype in bigquery_function_supported_dtypes
                    if not isinstance(dtype, pandas.ArrowDtype)
                )
                # Check ArrowDtype separately since multiple BigQuery types map to
                # ArrowDtype, including BYTES and TIMESTAMP.
                supported_arrow_types = tuple(
                    dtype.pyarrow_dtype
                    for dtype in bigquery_function_supported_dtypes
                    if isinstance(dtype, pandas.ArrowDtype)
                )
                supported_dtypes_hints = tuple(
                    str(dtype) for dtype in bigquery_function_supported_dtypes
                )

                for dtype in self.dtypes:
                    if (
                        # Not one of the pandas/numpy types.
                        not isinstance(dtype, supported_dtypes_types)
                        # And not one of the arrow types.
                        and not (
                            isinstance(dtype, pandas.ArrowDtype)
                            and any(
                                dtype.pyarrow_dtype.equals(arrow_type)
                                for arrow_type in supported_arrow_types
                            )
                        )
                    ):
                        raise NotImplementedError(
                            f"DataFrame has a column of dtype '{dtype}' which is not supported with axis=1."
                            f" Supported dtypes are {supported_dtypes_hints}."
                        )

                # Serialize the rows as json values
                block = self._get_block()
                rows_as_json_series = bigframes.series.Series(
                    block._get_rows_as_json_values()
                )

                # Apply the function
                result_series = rows_as_json_series._apply_unary_op(
                    ops.RemoteFunctionOp(function_def=func.udf_def, apply_on_null=True)
                )
            else:
                # This is a special case where we are providing not-pandas-like
                # extension. If the bigquery function can take one or more
                # params then we assume that here the user intention is to use
                # the column values of the dataframe as arguments to the
                # function. For this to work the following condition must be
                # true:
                #   1. The number or input params in the function must be same
                #      as the number of columns in the dataframe
                #   2. The dtypes of the columns in the dataframe must be
                #      compatible with the data types of the input params
                #   3. The order of the columns in the dataframe must correspond
                #      to the order of the input params in the function
                udf_input_dtypes = func.udf_def.signature.bf_input_types
                if len(udf_input_dtypes) != len(self.columns):
                    raise ValueError(
                        f"BigFrames BigQuery function takes {len(udf_input_dtypes)}"
                        f" arguments but DataFrame has {len(self.columns)} columns."
                    )
                if udf_input_dtypes != tuple(self.dtypes.to_list()):
                    raise ValueError(
                        f"BigFrames BigQuery function takes arguments of types "
                        f"{udf_input_dtypes} but DataFrame dtypes are {tuple(self.dtypes)}."
                    )

                series_list = [self[col] for col in self.columns]
                result_series = series_list[0]._apply_nary_op(
                    ops.NaryRemoteFunctionOp(function_def=func.udf_def), series_list[1:]
                )
            result_series.name = None

            result_series = func._post_process_series(result_series)
            return result_series

        # At this point column-wise or element-wise bigquery function operation will
        # be performed (not supported).
        if hasattr(func, "bigframes_bigquery_function"):
            raise formatter.create_exception_with_feedback_link(
                NotImplementedError,
                "BigFrames DataFrame '.apply()' does not support BigFrames "
                "BigQuery function for column-wise (i.e. with axis=0) "
                "operations, please use a regular python function instead. For "
                "element-wise operations of the BigFrames BigQuery function, "
                "please use '.map()'.",
            )

        # Per-column apply
        results = {name: func(col, *args, **kwargs) for name, col in self.items()}

        if all(
            [
                isinstance(val, bigframes.series.Series) or utils.is_list_like(val)
                for val in results.values()
            ]
        ):
            return DataFrame(data=results)
        else:
            return pandas.Series(data=results)

    def drop_duplicates(
        self,
        subset: typing.Union[blocks.Label, typing.Sequence[blocks.Label]] = None,
        *,
        keep: str = "first",
    ) -> DataFrame:
        if keep is not False:
            validations.enforce_ordered(self, "drop_duplicates(keep != False)")
        if subset is None:
            column_ids = self._block.value_columns
        elif utils.is_list_like(subset):
            column_ids = [
                id for label in subset for id in self._block.label_to_col_id[label]
            ]
        else:
            # interpret as single label
            column_ids = self._block.label_to_col_id[typing.cast(blocks.Label, subset)]
        block = block_ops.drop_duplicates(self._block, column_ids, keep)
        return DataFrame(block)

    def duplicated(self, subset=None, keep: str = "first") -> bigframes.series.Series:
        if keep is not False:
            validations.enforce_ordered(self, "duplicated(keep != False)")
        if subset is None:
            column_ids = self._block.value_columns
        else:
            column_ids = [
                id for label in subset for id in self._block.label_to_col_id[label]
            ]
        block, indicator = block_ops.indicate_duplicates(self._block, column_ids, keep)
        return bigframes.series.Series(
            block.select_column(
                indicator,
            )
        )

    def rank(
        self,
        axis=0,
        method: str = "average",
        numeric_only=False,
        na_option: str = "keep",
        ascending=True,
    ) -> DataFrame:
        df = self._drop_non_numeric() if numeric_only else self
        return DataFrame(block_ops.rank(df._block, method, na_option, ascending))

    def first_valid_index(self):
        return

    applymap = map
    applymap.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.map)

    def _slice(
        self,
        start: typing.Optional[int] = None,
        stop: typing.Optional[int] = None,
        step: typing.Optional[int] = None,
    ) -> DataFrame:
        block = self._block.slice(
            start=start, stop=stop, step=step if (step is not None) else 1
        )
        return DataFrame(block)

    def __array_ufunc__(
        self, ufunc: numpy.ufunc, method: str, *inputs, **kwargs
    ) -> DataFrame:
        """Used to support numpy ufuncs.
        See: https://numpy.org/doc/stable/reference/ufuncs.html
        """
        if method != "__call__" or len(inputs) > 2 or len(kwargs) > 0:
            return NotImplemented

        if len(inputs) == 1 and ufunc in ops.NUMPY_TO_OP:
            return self._apply_unary_op(ops.NUMPY_TO_OP[ufunc])
        if len(inputs) == 2 and ufunc in ops.NUMPY_TO_BINOP:
            binop = ops.NUMPY_TO_BINOP[ufunc]
            if inputs[0] is self:
                return self._apply_binop(inputs[1], binop)
            else:
                return self._apply_binop(inputs[0], binop, reverse=True)

        return NotImplemented

    def _set_block(self, block: blocks.Block):
        self._block = block

    def _get_block(self) -> blocks.Block:
        return self._block

    def cache(self):
        """
        Materializes the DataFrame to a temporary table.

        Useful if the dataframe will be used multiple times, as this will avoid recomputating the shared intermediate value.

        Returns:
            bigframes.pandas.DataFrame: DataFrame
        """
        return self._cached(force=True)

    def _cached(self, *, force: bool = False) -> DataFrame:
        """Materialize dataframe to a temporary table.
        No-op if the dataframe represents a trivial transformation of an existing materialization.
        Force=True is used for BQML integration where need to copy data rather than use snapshot.
        """
        if self._disable_cache_override:
            return self
        self._block.cached(force=force)
        return self

    _DataFrameOrSeries = typing.TypeVar("_DataFrameOrSeries")

    @validations.requires_ordering()
    def dot(self, other: _DataFrameOrSeries) -> _DataFrameOrSeries:
        if not isinstance(other, (DataFrame, bigframes.series.Series)):
            raise NotImplementedError(
                f"Only DataFrame or Series operand is supported. {constants.FEEDBACK_LINK}"
            )

        if len(self.index.names) > 1 or len(other.index.names) > 1:
            raise NotImplementedError(
                f"Multi-index input is not supported. {constants.FEEDBACK_LINK}"
            )

        if len(self.columns.names) > 1 or (
            isinstance(other, DataFrame) and len(other.columns.names) > 1
        ):
            raise NotImplementedError(
                f"Multi-level column input is not supported. {constants.FEEDBACK_LINK}"
            )

        # Convert the dataframes into cell-value-decomposed representation, i.e.
        # each cell value is present in a separate row
        row_id = "row"
        col_id = "col"
        val_id = "val"
        left_suffix = "_left"
        right_suffix = "_right"
        cvd_columns = [row_id, col_id, val_id]

        def get_left_id(id):
            return f"{id}{left_suffix}"

        def get_right_id(id):
            return f"{id}{right_suffix}"

        other_frame = other if isinstance(other, DataFrame) else other.to_frame()

        left = self.stack().reset_index()
        left.columns = cvd_columns

        right = other_frame.stack().reset_index()
        right.columns = cvd_columns

        merged = left.merge(
            right,
            left_on=col_id,
            right_on=row_id,
            suffixes=(left_suffix, right_suffix),
        )

        left_row_id = get_left_id(row_id)
        right_col_id = get_right_id(col_id)

        aggregated = (
            merged.assign(
                val=merged[get_left_id(val_id)] * merged[get_right_id(val_id)]
            )[[left_row_id, right_col_id, val_id]]
            .groupby([left_row_id, right_col_id])
            .sum(numeric_only=True)
        )
        aggregated_noindex = aggregated.reset_index()
        aggregated_noindex.columns = cvd_columns
        result = aggregated_noindex._pivot(
            columns=col_id, columns_unique_values=other_frame.columns, index=row_id
        )

        # Set the index names to match the left side matrix
        result.index.names = self.index.names

        # Pivot has the result columns ordered alphabetically. It should still
        # match the columns in the right sided matrix. Let's reorder them as per
        # the right side matrix
        if not result.columns.difference(other_frame.columns).empty:
            raise RuntimeError(
                f"Could not construct all columns. {constants.FEEDBACK_LINK}"
            )
        result = result[other_frame.columns]

        if isinstance(other, bigframes.series.Series):
            # There should be exactly one column in the result
            result = result[result.columns[0]].rename()

        return result

    @property
    def plot(self):
        return plotting.PlotAccessor(self)

    def hist(
        self, by: typing.Optional[typing.Sequence[str]] = None, bins: int = 10, **kwargs
    ):
        return self.plot.hist(by=by, bins=bins, **kwargs)

    hist.__doc__ = inspect.getdoc(plotting.PlotAccessor.hist)

    def line(
        self,
        x: typing.Optional[typing.Hashable] = None,
        y: typing.Optional[typing.Hashable] = None,
        **kwargs,
    ):
        return self.plot.line(x=x, y=y, **kwargs)

    line.__doc__ = inspect.getdoc(plotting.PlotAccessor.line)

    def area(
        self,
        x: typing.Optional[typing.Hashable] = None,
        y: typing.Optional[typing.Hashable] = None,
        stacked: bool = True,
        **kwargs,
    ):
        return self.plot.area(x=x, y=y, stacked=stacked, **kwargs)

    area.__doc__ = inspect.getdoc(plotting.PlotAccessor.area)

    def bar(
        self,
        x: typing.Optional[typing.Hashable] = None,
        y: typing.Optional[typing.Hashable] = None,
        **kwargs,
    ):
        return self.plot.bar(x=x, y=y, **kwargs)

    bar.__doc__ = inspect.getdoc(plotting.PlotAccessor.bar)

    def scatter(
        self,
        x: typing.Optional[typing.Hashable] = None,
        y: typing.Optional[typing.Hashable] = None,
        s: typing.Union[typing.Hashable, typing.Sequence[typing.Hashable]] = None,
        c: typing.Union[typing.Hashable, typing.Sequence[typing.Hashable]] = None,
        **kwargs,
    ):
        return self.plot.scatter(x=x, y=y, s=s, c=c, **kwargs)

    scatter.__doc__ = inspect.getdoc(plotting.PlotAccessor.scatter)

    def __matmul__(self, other) -> DataFrame:
        return self.dot(other)

    __matmul__.__doc__ = inspect.getdoc(vendored_pandas_frame.DataFrame.__matmul__)

    @property
    def struct(self):
        return bigframes.operations.structs.StructFrameAccessor(self)

    def _throw_if_null_index(self, opname: str):
        if not self._has_index:
            raise bigframes.exceptions.NullIndexError(
                f"DataFrame cannot perform {opname} as it has no index. Set an index using set_index."
            )

    @property
    def semantics(self):
        msg = bfe.format_message(
            "The 'semantics' property will be removed. Please use 'ai' instead."
        )
        warnings.warn(msg, category=FutureWarning)
        return bigframes.operations.semantics.Semantics(self)

    @property
    def ai(self):
        """Returns the accessor for AI operators."""
        return bigframes.operations.ai.AIAccessor(self)
