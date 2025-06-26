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

"""Series is a 1 dimensional data structure."""

from __future__ import annotations

import datetime
import functools
import inspect
import itertools
import numbers
import textwrap
import typing
from typing import (
    Any,
    cast,
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
import bigframes_vendored.pandas.core.series as vendored_pandas_series
import google.cloud.bigquery as bigquery
import numpy
import pandas
from pandas.api import extensions as pd_ext
import pandas.core.dtypes.common
import pyarrow as pa
import typing_extensions

import bigframes.core
from bigframes.core import groupby, log_adapter
import bigframes.core.block_transforms as block_ops
import bigframes.core.blocks as blocks
import bigframes.core.expression as ex
import bigframes.core.indexers
import bigframes.core.indexes as indexes
import bigframes.core.ordering as order
import bigframes.core.scalar as scalars
import bigframes.core.utils as utils
import bigframes.core.validations as validations
import bigframes.core.window
from bigframes.core.window import rolling
import bigframes.core.window_spec as windows
import bigframes.dataframe
import bigframes.dtypes
import bigframes.exceptions as bfe
import bigframes.formatting_helpers as formatter
import bigframes.functions
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops
import bigframes.operations.base
import bigframes.operations.blob as blob
import bigframes.operations.datetimes as dt
import bigframes.operations.lists as lists
import bigframes.operations.plotting as plotting
import bigframes.operations.strings as strings
import bigframes.operations.structs as structs

if typing.TYPE_CHECKING:
    import bigframes.geopandas.geoseries

LevelType = typing.Union[str, int]
LevelsType = typing.Union[LevelType, typing.Sequence[LevelType]]


_bigquery_function_recommendation_message = (
    "Your functions could not be applied directly to the Series."
    " Try converting it to a BigFrames BigQuery function."
)

_list = list  # Type alias to escape Series.list property


@log_adapter.class_logger
class Series(bigframes.operations.base.SeriesMethods, vendored_pandas_series.Series):
    # Must be above 5000 for pandas to delegate to bigframes for binops
    __pandas_priority__ = 13000

    # Ensure mypy can more robustly determine the type of self._block since it
    # gets set in various places.
    _block: blocks.Block

    def __init__(self, *args, **kwargs):
        self._query_job: Optional[bigquery.QueryJob] = None
        super().__init__(*args, **kwargs)
        self._block.session._register_object(self)

    @property
    def dt(self) -> dt.DatetimeMethods:
        return dt.DatetimeMethods(self._block)

    @property
    def dtype(self):
        return self._dtype

    @property
    def dtypes(self):
        return self._dtype

    @property
    def geo(self) -> bigframes.geopandas.geoseries.GeoSeries:
        """
        Accessor object for geography properties of the Series values.

        Returns:
            bigframes.geopandas.geoseries.GeoSeries:
                An accessor containing geography methods.

        """
        import bigframes.geopandas.geoseries

        return bigframes.geopandas.geoseries.GeoSeries(self)

    @property
    @validations.requires_index
    def loc(self) -> bigframes.core.indexers.LocSeriesIndexer:
        return bigframes.core.indexers.LocSeriesIndexer(self)

    @property
    @validations.requires_ordering()
    def iloc(self) -> bigframes.core.indexers.IlocSeriesIndexer:
        return bigframes.core.indexers.IlocSeriesIndexer(self)

    @property
    @validations.requires_ordering()
    def iat(self) -> bigframes.core.indexers.IatSeriesIndexer:
        return bigframes.core.indexers.IatSeriesIndexer(self)

    @property
    @validations.requires_index
    def at(self) -> bigframes.core.indexers.AtSeriesIndexer:
        return bigframes.core.indexers.AtSeriesIndexer(self)

    @property
    def name(self) -> blocks.Label:
        return self._name

    @name.setter
    def name(self, label: blocks.Label):
        new_block = self._block.with_column_labels([label])
        self._set_block(new_block)

    @property
    def shape(self) -> typing.Tuple[int]:
        return (self._block.shape[0],)

    @property
    def size(self) -> int:
        return self.shape[0]

    @property
    def ndim(self) -> int:
        return 1

    @property
    def empty(self) -> bool:
        return self.shape[0] == 0

    @property
    def hasnans(self) -> bool:
        # Note, hasnans is actually a null check, and NaNs don't count for nullable float
        return self.isnull().any()

    @property
    def values(self) -> numpy.ndarray:
        return self.to_numpy()

    @property
    @validations.requires_index
    def index(self) -> indexes.Index:
        return indexes.Index.from_frame(self)

    @validations.requires_index
    def keys(self) -> indexes.Index:
        return self.index

    @property
    def query_job(self) -> Optional[bigquery.QueryJob]:
        """BigQuery job metadata for the most recent query.

        Returns:
            The most recent `QueryJob
            <https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob>`_.
        """
        if self._query_job is None:
            self._set_internal_query_job(self._compute_dry_run())
        return self._query_job

    @property
    def struct(self) -> structs.StructAccessor:
        return structs.StructAccessor(self._block)

    @property
    def list(self) -> lists.ListAccessor:
        return lists.ListAccessor(self._block)

    @property
    def blob(self) -> blob.BlobAccessor:
        return blob.BlobAccessor(self._block)

    @property
    @validations.requires_ordering()
    def T(self) -> Series:
        return self.transpose()

    @property
    def _info_axis(self) -> indexes.Index:
        return self.index

    @property
    def _session(self) -> bigframes.Session:
        return self._get_block().expr.session

    @property
    def _struct_fields(self) -> List[str]:
        if not bigframes.dtypes.is_struct_like(self._dtype):
            return []

        struct_type = typing.cast(pa.StructType, self._dtype.pyarrow_dtype)
        return [struct_type.field(i).name for i in range(struct_type.num_fields)]

    @validations.requires_ordering()
    def transpose(self) -> Series:
        return self

    def _set_internal_query_job(self, query_job: Optional[bigquery.QueryJob]):
        self._query_job = query_job

    def __len__(self):
        return self.shape[0]

    __len__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__len__)

    def __iter__(self) -> typing.Iterator:
        return itertools.chain.from_iterable(
            map(lambda x: x.squeeze(axis=1), self._block.to_pandas_batches())
        )

    def copy(self) -> Series:
        return Series(self._block)

    @overload
    def rename(
        self,
        index: Union[blocks.Label, Mapping[Any, Any]] = None,
    ) -> Series:
        ...

    @overload
    def rename(
        self,
        index: Union[blocks.Label, Mapping[Any, Any]] = None,
        *,
        inplace: Literal[False],
        **kwargs,
    ) -> Series:
        ...

    @overload
    def rename(
        self,
        index: Union[blocks.Label, Mapping[Any, Any]] = None,
        *,
        inplace: Literal[True],
        **kwargs,
    ) -> None:
        ...

    def rename(
        self,
        index: Union[blocks.Label, Mapping[Any, Any]] = None,
        *,
        inplace: bool = False,
        **kwargs,
    ) -> Optional[Series]:
        if len(kwargs) != 0:
            raise NotImplementedError(
                f"rename does not currently support any keyword arguments. {constants.FEEDBACK_LINK}"
            )

        # rename the index
        if isinstance(index, Mapping):
            index = typing.cast(Mapping[Any, Any], index)
            block = self._block
            for k, v in index.items():
                new_idx_ids = []
                for idx_id, idx_dtype in zip(block.index_columns, block.index.dtypes):
                    # Will throw if key type isn't compatible with index type, which leads to invalid SQL.
                    block.create_constant(k, dtype=idx_dtype)

                    # Will throw if value type isn't compatible with index type.
                    block, const_id = block.create_constant(v, dtype=idx_dtype)
                    block, cond_id = block.project_expr(
                        ops.ne_op.as_expr(idx_id, ex.const(k))
                    )
                    block, new_idx_id = block.apply_ternary_op(
                        idx_id, cond_id, const_id, ops.where_op
                    )

                    new_idx_ids.append(new_idx_id)
                    block = block.drop_columns([const_id, cond_id])

                block = block.set_index(new_idx_ids, index_labels=block.index.names)

            if inplace:
                self._block = block
                return None
            else:
                return Series(block)

        # rename the Series name
        if isinstance(index, typing.Hashable):
            # Python 3.9 doesn't allow isinstance of Optional
            index = typing.cast(Optional[str], index)
            block = self._block.with_column_labels([index])

            if inplace:
                self._block = block
                return None
            else:
                return Series(block)

        raise ValueError(f"Unsupported type of parameter index: {type(index)}")

    @overload
    def rename_axis(
        self,
        mapper: typing.Union[blocks.Label, typing.Sequence[blocks.Label]],
    ) -> Series:
        ...

    @overload
    def rename_axis(
        self,
        mapper: typing.Union[blocks.Label, typing.Sequence[blocks.Label]],
        *,
        inplace: Literal[False],
        **kwargs,
    ) -> Series:
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

    @validations.requires_index
    def rename_axis(
        self,
        mapper: typing.Union[blocks.Label, typing.Sequence[blocks.Label]],
        *,
        inplace: bool = False,
        **kwargs,
    ) -> Optional[Series]:
        if len(kwargs) != 0:
            raise NotImplementedError(
                f"rename_axis does not currently support any keyword arguments. {constants.FEEDBACK_LINK}"
            )
        # limited implementation: the new index name is simply the 'mapper' parameter
        if _is_list_like(mapper):
            labels = mapper
        else:
            labels = [mapper]

        block = self._block.with_index_labels(labels)
        if inplace:
            self._block = block
            return None
        else:
            return Series(block)

    def equals(
        self, other: typing.Union[Series, bigframes.dataframe.DataFrame]
    ) -> bool:
        # Must be same object type, same column dtypes, and same label values
        if not isinstance(other, Series):
            return False
        return block_ops.equals(self._block, other._block)

    @validations.requires_ordering()
    def reset_index(
        self,
        *,
        name: typing.Optional[str] = None,
        drop: bool = False,
    ) -> bigframes.dataframe.DataFrame | Series:
        block = self._block.reset_index(drop)
        if drop:
            return Series(block)
        else:
            if name:
                block = block.assign_label(self._value_column, name)
            return bigframes.dataframe.DataFrame(block)

    def __repr__(self) -> str:
        # Protect against errors with uninitialized Series. See:
        # https://github.com/googleapis/python-bigquery-dataframes/issues/728
        if not hasattr(self, "_block"):
            return object.__repr__(self)

        # TODO(swast): Add a timeout here? If the query is taking a long time,
        # maybe we just print the job metadata that we have so far?
        # TODO(swast): Avoid downloading the whole series by using job
        # metadata, like we do with DataFrame.
        opts = bigframes.options.display
        max_results = opts.max_rows
        # anywdiget mode uses the same display logic as the "deferred" mode
        # for faster execution
        if opts.repr_mode in ("deferred", "anywidget"):
            return formatter.repr_query_job(self._compute_dry_run())

        self._cached()
        pandas_df, _, query_job = self._block.retrieve_repr_request_results(max_results)
        self._set_internal_query_job(query_job)

        pd_series = pandas_df.iloc[:, 0]

        import pandas.io.formats

        # safe to mutate this, this dict is owned by this code, and does not affect global config
        to_string_kwargs = pandas.io.formats.format.get_series_repr_params()  # type: ignore
        if len(self._block.index_columns) == 0:
            to_string_kwargs.update({"index": False})
        repr_string = pd_series.to_string(**to_string_kwargs)

        return repr_string

    def astype(
        self,
        dtype: Union[bigframes.dtypes.DtypeString, bigframes.dtypes.Dtype],
        *,
        errors: Literal["raise", "null"] = "raise",
    ) -> Series:
        if errors not in ["raise", "null"]:
            raise ValueError("Argument 'errors' must be one of 'raise' or 'null'")
        dtype = bigframes.dtypes.bigframes_type(dtype)
        return self._apply_unary_op(
            bigframes.operations.AsTypeOp(to_type=dtype, safe=(errors == "null"))
        )

    def to_pandas(
        self,
        max_download_size: Optional[int] = None,
        sampling_method: Optional[str] = None,
        random_state: Optional[int] = None,
        *,
        ordered: bool = True,
        dry_run: bool = False,
        allow_large_results: Optional[bool] = None,
    ) -> pandas.Series:
        """Writes Series to pandas Series.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series([4, 3, 2])

        Download the data from BigQuery and convert it into an in-memory pandas Series.

            >>> s.to_pandas()
            0    4
            1    3
            2    2
            dtype: Int64

        Estimate job statistics without processing or downloading data by using `dry_run=True`.

            >>> s.to_pandas(dry_run=True) # doctest: +SKIP
            columnCount                                                            1
            columnDtypes                                               {None: Int64}
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
            creationTime                            2025-04-03 18:54:59.219000+00:00
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
                Determines whether the resulting pandas series will be  ordered.
                In some cases, unordered may result in a faster-executing query.
            dry_run (bool, default False):
                If this argument is true, this method will not process the data. Instead, it returns
                a Pandas Series containing dry run job statistics
            allow_large_results (bool, default None):
                If not None, overrides the global setting to allow or disallow large query results
                over the default size limit of 10 GB.

        Returns:
            pandas.Series: A pandas Series with all rows of this Series if the data_sampling_threshold_mb
                is not exceeded; otherwise, a pandas Series with downsampled rows of the DataFrame. If dry_run
                is set to True, a pandas Series containing dry run statistics will be returned.
        """
        if max_download_size is not None:
            msg = bfe.format_message(
                "DEPRECATED: The `max_download_size` parameters for `Series.to_pandas()` "
                "are deprecated and will be removed soon. Please use `Series.to_pandas_batches()`."
            )
            warnings.warn(msg, category=FutureWarning)
        if sampling_method is not None or random_state is not None:
            msg = bfe.format_message(
                "DEPRECATED: The `sampling_method` and `random_state` parameters for "
                "`Series.to_pandas()` are deprecated and will be removed soon. "
                "Please use `Series.sample().to_pandas()` instead for sampling."
            )
            warnings.warn(msg, category=FutureWarning)

        if dry_run:
            dry_run_stats, dry_run_job = self._block._compute_dry_run(
                max_download_size=max_download_size,
                sampling_method=sampling_method,
                random_state=random_state,
                ordered=ordered,
            )

            self._set_internal_query_job(dry_run_job)
            return dry_run_stats

        # Repeat the to_pandas() call to make mypy deduce type correctly, because mypy cannot resolve
        # Literal[True/False] to bool
        df, query_job = self._block.to_pandas(
            max_download_size=max_download_size,
            sampling_method=sampling_method,
            random_state=random_state,
            ordered=ordered,
            allow_large_results=allow_large_results,
        )

        if query_job:
            self._set_internal_query_job(query_job)

        series = df.squeeze(axis=1)
        series.name = self._name
        return series

    def to_pandas_batches(
        self,
        page_size: Optional[int] = None,
        max_results: Optional[int] = None,
        *,
        allow_large_results: Optional[bool] = None,
    ) -> Iterable[pandas.Series]:
        """Stream Series results to an iterable of pandas Series.

        page_size and max_results determine the size and number of batches,
        see https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob#google_cloud_bigquery_job_QueryJob_result

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series([4, 3, 2, 2, 3])

        Iterate through the results in batches, limiting the total rows yielded
        across all batches via `max_results`:

            >>> for s_batch in s.to_pandas_batches(max_results=3):
            ...     print(s_batch)
            0    4
            1    3
            2    2
            dtype: Int64

        Alternatively, control the approximate size of each batch using `page_size`
        and fetch batches manually using `next()`:

            >>> it = s.to_pandas_batches(page_size=2)
            >>> next(it)
            0    4
            1    3
            dtype: Int64
            >>> next(it)
            2    2
            3    2
            dtype: Int64

        Args:
            page_size (int, default None):
                The maximum number of rows of each batch. Non-positive values are ignored.
            max_results (int, default None):
                The maximum total number of rows of all batches.
            allow_large_results (bool, default None):
                If not None, overrides the global setting to allow or disallow large query results
                over the default size limit of 10 GB.

        Returns:
            Iterable[pandas.Series]:
                An iterable of smaller Series which combine to
                form the original Series. Results stream from bigquery,
                see https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.table.RowIterator#google_cloud_bigquery_table_RowIterator_to_arrow_iterable
        """
        df = self._block.to_pandas_batches(
            page_size=page_size,
            max_results=max_results,
            allow_large_results=allow_large_results,
            squeeze=True,
        )
        return df

    def _compute_dry_run(self) -> bigquery.QueryJob:
        _, query_job = self._block._compute_dry_run((self._value_column,))
        return query_job

    def drop(
        self,
        labels: typing.Any = None,
        *,
        axis: typing.Union[int, str] = 0,
        index: typing.Any = None,
        columns: Union[blocks.Label, typing.Iterable[blocks.Label]] = None,
        level: typing.Optional[LevelType] = None,
    ) -> Series:
        if (labels is None) == (index is None):
            raise ValueError("Must specify exactly one of 'labels' or 'index'")

        if labels is not None:
            index = labels

        # ignore axis, columns params
        block = self._block
        level_id = self._resolve_levels(level or 0)[0]
        if _is_list_like(index):
            block, inverse_condition_id = block.apply_unary_op(
                level_id, ops.IsInOp(values=tuple(index), match_nulls=True)
            )
            block, condition_id = block.apply_unary_op(
                inverse_condition_id, ops.invert_op
            )
        else:
            block, condition_id = block.project_expr(
                ops.ne_op.as_expr(level_id, ex.const(index))
            )
        block = block.filter_by_id(condition_id, keep_null=True)
        block = block.drop_columns([condition_id])
        return Series(block.select_column(self._value_column))

    @validations.requires_index
    def droplevel(self, level: LevelsType, axis: int | str = 0):
        resolved_level_ids = self._resolve_levels(level)
        return Series(self._block.drop_levels(resolved_level_ids))

    @validations.requires_index
    def swaplevel(self, i: int = -2, j: int = -1):
        level_i = self._block.index_columns[i]
        level_j = self._block.index_columns[j]
        mapping = {level_i: level_j, level_j: level_i}
        reordering = [
            mapping.get(index_id, index_id) for index_id in self._block.index_columns
        ]
        return Series(self._block.reorder_levels(reordering))

    @validations.requires_index
    def reorder_levels(self, order: LevelsType, axis: int | str = 0):
        resolved_level_ids = self._resolve_levels(order)
        return Series(self._block.reorder_levels(resolved_level_ids))

    def _resolve_levels(self, level: LevelsType) -> typing.Sequence[str]:
        return self._block.index.resolve_level(level)

    def between(self, left, right, inclusive="both"):
        if inclusive not in ["both", "neither", "left", "right"]:
            raise ValueError(
                "Must set 'inclusive' to one of 'both', 'neither', 'left', or 'right'"
            )
        left_op = ops.ge_op if (inclusive in ["left", "both"]) else ops.gt_op
        right_op = ops.le_op if (inclusive in ["right", "both"]) else ops.lt_op
        return self._apply_binary_op(left, left_op).__and__(
            self._apply_binary_op(right, right_op)
        )

    def case_when(self, caselist) -> Series:
        cases = []

        for condition, output in itertools.chain(caselist, [(True, self)]):
            cases.append(condition)
            cases.append(output)
            # In pandas, the default value if no case matches is the original value.
            # This makes it impossible to change the type of the column, but if
            # the condition is always True, we know it will match and no subsequent
            # conditions matter (including the fallback to `self`). This break allows
            # the type to change (see: internal issue 349926559).
            if condition is True:
                break

        return self._apply_nary_op(
            ops.case_when_op,
            cases,
            # Self is already included in "others".
            ignore_self=True,
        ).rename(self.name)

    @validations.requires_ordering()
    def cumsum(self) -> Series:
        return self._apply_window_op(agg_ops.sum_op, windows.cumulative_rows())

    @validations.requires_ordering()
    def ffill(self, *, limit: typing.Optional[int] = None) -> Series:
        window = windows.rows(start=None if limit is None else -limit, end=0)
        return self._apply_window_op(agg_ops.LastNonNullOp(), window)

    pad = ffill
    pad.__doc__ = inspect.getdoc(vendored_pandas_series.Series.ffill)

    @validations.requires_ordering()
    def bfill(self, *, limit: typing.Optional[int] = None) -> Series:
        window = windows.rows(start=0, end=limit)
        return self._apply_window_op(agg_ops.FirstNonNullOp(), window)

    @validations.requires_ordering()
    def cummax(self) -> Series:
        return self._apply_window_op(agg_ops.max_op, windows.cumulative_rows())

    @validations.requires_ordering()
    def cummin(self) -> Series:
        return self._apply_window_op(agg_ops.min_op, windows.cumulative_rows())

    @validations.requires_ordering()
    def cumprod(self) -> Series:
        return self._apply_window_op(agg_ops.product_op, windows.cumulative_rows())

    @validations.requires_ordering()
    def shift(self, periods: int = 1) -> Series:
        window_spec = windows.rows()
        return self._apply_window_op(agg_ops.ShiftOp(periods), window_spec)

    @validations.requires_ordering()
    def diff(self, periods: int = 1) -> Series:
        window_spec = windows.rows()
        return self._apply_window_op(agg_ops.DiffOp(periods), window_spec)

    @validations.requires_ordering()
    def pct_change(self, periods: int = 1) -> Series:
        # Future versions of pandas will not perfrom ffill automatically
        series = self.ffill()
        return Series(block_ops.pct_change(series._block, periods=periods))

    @validations.requires_ordering()
    def rank(
        self,
        axis=0,
        method: str = "average",
        numeric_only=False,
        na_option: str = "keep",
        ascending: bool = True,
    ) -> Series:
        return Series(block_ops.rank(self._block, method, na_option, ascending))

    def fillna(self, value=None) -> Series:
        return self._apply_binary_op(value, ops.fillna_op)

    def replace(
        self, to_replace: typing.Any, value: typing.Any = None, *, regex: bool = False
    ):
        if regex:
            # No-op unless to_replace and series dtype are both string type
            if not isinstance(to_replace, str) or not isinstance(
                self.dtype, pandas.StringDtype
            ):
                return self
            return self._regex_replace(to_replace, value)
        elif utils.is_dict_like(to_replace):
            return self._mapping_replace(to_replace)  # type: ignore
        elif utils.is_list_like(to_replace):
            replace_list = to_replace
        else:  # Scalar
            replace_list = [to_replace]
        replace_list = [
            i for i in replace_list if bigframes.dtypes.is_compatible(i, self.dtype)
        ]
        return self._simple_replace(replace_list, value) if replace_list else self

    def _regex_replace(self, to_replace: str, value: str):
        if not bigframes.dtypes.is_dtype(value, self.dtype):
            raise NotImplementedError(
                f"Cannot replace {self.dtype} elements with incompatible item {value} as mixed-type columns not supported. {constants.FEEDBACK_LINK}"
            )
        block, result_col = self._block.apply_unary_op(
            self._value_column,
            ops.RegexReplaceStrOp(to_replace, value),
            result_label=self.name,
        )
        return Series(block.select_column(result_col))

    def _simple_replace(self, to_replace_list: typing.Sequence, value):
        result_type = bigframes.dtypes.is_compatible(value, self.dtype)
        if not result_type:
            raise NotImplementedError(
                f"Cannot replace {self.dtype} elements with incompatible item {value} as mixed-type columns not supported. {constants.FEEDBACK_LINK}"
            )

        if result_type != self.dtype:
            return self.astype(result_type)._simple_replace(to_replace_list, value)

        block, cond = self._block.apply_unary_op(
            self._value_column, ops.IsInOp(tuple(to_replace_list))
        )
        block, result_col = block.project_expr(
            ops.where_op.as_expr(ex.const(value), cond, self._value_column), self.name
        )
        return Series(block.select_column(result_col))

    def _mapping_replace(self, mapping: dict[typing.Hashable, typing.Hashable]):
        if not mapping:
            return self.copy()

        tuples = []
        lcd_types: list[typing.Optional[bigframes.dtypes.Dtype]] = []
        for key, value in mapping.items():
            lcd_type = bigframes.dtypes.is_compatible(key, self.dtype)
            if not lcd_type:
                continue
            if not bigframes.dtypes.is_dtype(value, self.dtype):
                raise NotImplementedError(
                    f"Cannot replace {self.dtype} elements with incompatible item {value} as mixed-type columns not supported. {constants.FEEDBACK_LINK}"
                )
            tuples.append((key, value))
            lcd_types.append(lcd_type)

        result_dtype = functools.reduce(
            lambda t1, t2: bigframes.dtypes.lcd_type(t1, t2) if (t1 and t2) else None,
            lcd_types,
            self.dtype,
        )
        if not result_dtype:
            raise NotImplementedError(
                f"Cannot replace {self.dtype} elements with incompatible mapping {mapping} as mixed-type columns not supported. {constants.FEEDBACK_LINK}"
            )
        block, result = self._block.apply_unary_op(
            self._value_column, ops.MapOp(tuple(tuples))
        )
        replaced = Series(block.select_column(result))
        replaced.name = self.name
        return replaced

    @validations.requires_ordering()
    @validations.requires_index
    def interpolate(self, method: str = "linear") -> Series:
        if method == "pad":
            return self.ffill()
        result = block_ops.interpolate(self._block, method)
        return Series(result)

    def dropna(
        self,
        *,
        axis: int = 0,
        inplace: bool = False,
        how: typing.Optional[str] = None,
        ignore_index: bool = False,
    ) -> Series:
        if inplace:
            raise NotImplementedError("'inplace'=True not supported")
        result = block_ops.dropna(self._block, [self._value_column], how="any")
        if ignore_index:
            result = result.reset_index()
        return Series(result)

    @validations.requires_ordering(bigframes.constants.SUGGEST_PEEK_PREVIEW)
    def head(self, n: int = 5) -> Series:
        return typing.cast(Series, self.iloc[0:n])

    @validations.requires_ordering()
    def tail(self, n: int = 5) -> Series:
        return typing.cast(Series, self.iloc[-n:])

    def peek(
        self, n: int = 5, *, force: bool = True, allow_large_results=None
    ) -> pandas.Series:
        """
        Preview n arbitrary elements from the series without guarantees about row selection or ordering.

        ``Series.peek(force=False)`` will always be very fast, but will not succeed if data requires
        full data scanning. Using ``force=True`` will always succeed, but may be perform queries.
        Query results will be cached so that future steps will benefit from these queries.

        Args:
            n (int, default 5):
                The number of rows to select from the series. Which N rows are returned is non-deterministic.
            force (bool, default True):
                If the data cannot be peeked efficiently, the series will instead be fully materialized as part
                of the operation if ``force=True``. If ``force=False``, the operation will throw a ValueError.
            allow_large_results (bool, default None):
                If not None, overrides the global setting to allow or disallow large query results
                over the default size limit of 10 GB.
        Returns:
            pandas.Series: A pandas Series with n rows.

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
        as_series = maybe_result.squeeze(axis=1)
        as_series.name = self.name
        return as_series

    def item(self):
        # Docstring is in third_party/bigframes_vendored/pandas/core/series.py
        return self.peek(2).item()

    def nlargest(self, n: int = 5, keep: str = "first") -> Series:
        if keep not in ("first", "last", "all"):
            raise ValueError("'keep must be one of 'first', 'last', or 'all'")
        if keep != "all":
            validations.enforce_ordered(self, "nlargest(keep != 'all')")
        return Series(
            block_ops.nlargest(self._block, n, [self._value_column], keep=keep)
        )

    def nsmallest(self, n: int = 5, keep: str = "first") -> Series:
        if keep not in ("first", "last", "all"):
            raise ValueError("'keep must be one of 'first', 'last', or 'all'")
        if keep != "all":
            validations.enforce_ordered(self, "nsmallest(keep != 'all')")
        return Series(
            block_ops.nsmallest(self._block, n, [self._value_column], keep=keep)
        )

    def isin(self, values) -> "Series" | None:
        if isinstance(values, Series):
            return Series(self._block.isin(values._block))
        if isinstance(values, indexes.Index):
            return Series(self._block.isin(values.to_series()._block))
        if not _is_list_like(values):
            raise TypeError(
                "only list-like objects are allowed to be passed to "
                f"isin(), you passed a [{type(values).__name__}]"
            )
        return self._apply_unary_op(
            ops.IsInOp(values=tuple(values), match_nulls=True)
        ).fillna(value=False)

    def isna(self) -> "Series":
        return self._apply_unary_op(ops.isnull_op)

    isnull = isna
    isnull.__doc__ = inspect.getdoc(vendored_pandas_series.Series.isna)

    def notna(self) -> "Series":
        return self._apply_unary_op(ops.notnull_op)

    notnull = notna
    notnull.__doc__ = inspect.getdoc(vendored_pandas_series.Series.notna)

    def __and__(self, other: bool | int | Series) -> Series:
        return self._apply_binary_op(other, ops.and_op)

    __and__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__and__)

    __rand__ = __and__

    def __or__(self, other: bool | int | Series) -> Series:
        return self._apply_binary_op(other, ops.or_op)

    __or__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__or__)

    __ror__ = __or__

    def __xor__(self, other: bool | int | Series) -> Series:
        return self._apply_binary_op(other, ops.xor_op)

    __or__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__xor__)

    __rxor__ = __xor__

    def __add__(self, other: float | int | Series) -> Series:
        return self.add(other)

    __add__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__add__)

    def __radd__(self, other: float | int | Series) -> Series:
        return self.radd(other)

    __radd__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__radd__)

    def add(self, other: float | int | Series) -> Series:
        return self._apply_binary_op(other, ops.add_op)

    def radd(self, other: float | int | Series) -> Series:
        return self._apply_binary_op(other, ops.add_op, reverse=True)

    def __sub__(self, other: float | int | Series) -> Series:
        return self.sub(other)

    __sub__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__sub__)

    def __rsub__(self, other: float | int | Series) -> Series:
        return self.rsub(other)

    __rsub__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__rsub__)

    def sub(self, other) -> Series:
        return self._apply_binary_op(other, ops.sub_op)

    def rsub(self, other) -> Series:
        return self._apply_binary_op(other, ops.sub_op, reverse=True)

    subtract = sub
    subtract.__doc__ = inspect.getdoc(vendored_pandas_series.Series.sub)

    def __mul__(self, other: float | int | Series) -> Series:
        return self.mul(other)

    __mul__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__mul__)

    def __rmul__(self, other: float | int | Series) -> Series:
        return self.rmul(other)

    __rmul__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__rmul__)

    def mul(self, other: float | int | Series) -> Series:
        return self._apply_binary_op(other, ops.mul_op)

    def rmul(self, other: float | int | Series) -> Series:
        return self._apply_binary_op(other, ops.mul_op, reverse=True)

    multiply = mul
    multiply.__doc__ = inspect.getdoc(vendored_pandas_series.Series.mul)

    def __truediv__(self, other: float | int | Series) -> Series:
        return self.truediv(other)

    __truediv__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__truediv__)

    def __rtruediv__(self, other: float | int | Series) -> Series:
        return self.rtruediv(other)

    __rtruediv__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__rtruediv__)

    def truediv(self, other: float | int | Series) -> Series:
        return self._apply_binary_op(other, ops.div_op)

    def rtruediv(self, other: float | int | Series) -> Series:
        return self._apply_binary_op(other, ops.div_op, reverse=True)

    truediv.__doc__ = inspect.getdoc(vendored_pandas_series.Series.truediv)
    div = divide = truediv

    rdiv = rtruediv
    rdiv.__doc__ = inspect.getdoc(vendored_pandas_series.Series.rtruediv)

    def __floordiv__(self, other: float | int | Series) -> Series:
        return self.floordiv(other)

    __floordiv__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__floordiv__)

    def __rfloordiv__(self, other: float | int | Series) -> Series:
        return self.rfloordiv(other)

    __rfloordiv__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__rfloordiv__)

    def floordiv(self, other: float | int | Series) -> Series:
        return self._apply_binary_op(other, ops.floordiv_op)

    def rfloordiv(self, other: float | int | Series) -> Series:
        return self._apply_binary_op(other, ops.floordiv_op, reverse=True)

    def __pow__(self, other: float | int | Series) -> Series:
        return self.pow(other)

    __pow__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__pow__)

    def __rpow__(self, other: float | int | Series) -> Series:
        return self.rpow(other)

    __rpow__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__rpow__)

    def pow(self, other: float | int | Series) -> Series:
        return self._apply_binary_op(other, ops.pow_op)

    def rpow(self, other: float | int | Series) -> Series:
        return self._apply_binary_op(other, ops.pow_op, reverse=True)

    def __lt__(self, other: float | int | str | Series) -> Series:
        return self.lt(other)

    def __le__(self, other: float | int | str | Series) -> Series:
        return self.le(other)

    def lt(self, other) -> Series:
        return self._apply_binary_op(other, ops.lt_op)

    def le(self, other) -> Series:
        return self._apply_binary_op(other, ops.le_op)

    def __gt__(self, other: float | int | str | Series) -> Series:
        return self.gt(other)

    def __ge__(self, other: float | int | str | Series) -> Series:
        return self.ge(other)

    def gt(self, other) -> Series:
        return self._apply_binary_op(other, ops.gt_op)

    def ge(self, other) -> Series:
        return self._apply_binary_op(other, ops.ge_op)

    def __mod__(self, other) -> Series:  # type: ignore
        return self.mod(other)

    __mod__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__mod__)

    def __rmod__(self, other) -> Series:  # type: ignore
        return self.rmod(other)

    __rmod__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__rmod__)

    def mod(self, other) -> Series:  # type: ignore
        return self._apply_binary_op(other, ops.mod_op)

    def rmod(self, other) -> Series:  # type: ignore
        return self._apply_binary_op(other, ops.mod_op, reverse=True)

    def divmod(self, other) -> Tuple[Series, Series]:  # type: ignore
        # TODO(huanc): when self and other both has dtype int and other contains zeros,
        # the output should be dtype float, both floordiv and mod returns dtype int in this case.
        return (self.floordiv(other), self.mod(other))

    def rdivmod(self, other) -> Tuple[Series, Series]:  # type: ignore
        # TODO(huanc): when self and other both has dtype int and self contains zeros,
        # the output should be dtype float, both floordiv and mod returns dtype int in this case.
        return (self.rfloordiv(other), self.rmod(other))

    def dot(self, other):
        return (self * other).sum()

    def __matmul__(self, other):
        return self.dot(other)

    __matmul__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__matmul__)

    def __rmatmul__(self, other):
        return self.dot(other)

    __rmatmul__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__rmatmul__)

    def combine_first(self, other: Series) -> Series:
        result = self._apply_binary_op(other, ops.coalesce_op)
        result.name = self.name
        return result

    def update(self, other: Union[Series, Sequence, Mapping]) -> None:
        result = self._apply_binary_op(
            other, ops.coalesce_op, reverse=True, alignment="left"
        )
        self._set_block(result._get_block())

    def __abs__(self) -> Series:
        return self.abs()

    def abs(self) -> Series:
        return self._apply_unary_op(ops.abs_op)

    def round(self, decimals=0) -> "Series":
        return self._apply_binary_op(decimals, ops.round_op)

    def corr(self, other: Series, method="pearson", min_periods=None) -> float:
        # TODO(tbergeron): Validate early that both are numeric
        # TODO(tbergeron): Handle partially-numeric columns
        if method != "pearson":
            raise NotImplementedError(
                f"Only Pearson correlation is currently supported. {constants.FEEDBACK_LINK}"
            )
        if min_periods:
            raise NotImplementedError(
                f"min_periods not yet supported. {constants.FEEDBACK_LINK}"
            )
        return self._apply_binary_aggregation(other, agg_ops.CorrOp())

    def autocorr(self, lag: int = 1) -> float:
        return self.corr(self.shift(lag))

    def cov(self, other: Series) -> float:
        return self._apply_binary_aggregation(other, agg_ops.CovOp())

    def all(self) -> bool:
        return typing.cast(bool, self._apply_aggregation(agg_ops.all_op))

    def any(self) -> bool:
        return typing.cast(bool, self._apply_aggregation(agg_ops.any_op))

    def count(self) -> int:
        return typing.cast(int, self._apply_aggregation(agg_ops.count_op))

    def nunique(self) -> int:
        return typing.cast(int, self._apply_aggregation(agg_ops.nunique_op))

    def max(self) -> scalars.Scalar:
        return self._apply_aggregation(agg_ops.max_op)

    def min(self) -> scalars.Scalar:
        return self._apply_aggregation(agg_ops.min_op)

    def std(self) -> float:
        return typing.cast(float, self._apply_aggregation(agg_ops.std_op))

    def var(self) -> float:
        return typing.cast(float, self._apply_aggregation(agg_ops.var_op))

    def _central_moment(self, n: int) -> float:
        """Useful helper for calculating central moment statistics"""
        # Nth central moment is mean((x-mean(x))^n)
        # See: https://en.wikipedia.org/wiki/Moment_(mathematics)
        mean_deltas = self - self.mean()
        delta_powers = mean_deltas**n
        return delta_powers.mean()

    def agg(self, func: str | typing.Sequence[str]) -> scalars.Scalar | Series:
        if _is_list_like(func):
            if self.dtype not in bigframes.dtypes.NUMERIC_BIGFRAMES_TYPES_PERMISSIVE:
                raise NotImplementedError(
                    f"Multiple aggregations only supported on numeric series. {constants.FEEDBACK_LINK}"
                )
            aggregations = [agg_ops.lookup_agg_func(f) for f in func]
            return Series(
                self._block.summarize(
                    [self._value_column],
                    aggregations,
                )
            )
        else:
            return self._apply_aggregation(
                agg_ops.lookup_agg_func(typing.cast(str, func))
            )

    aggregate = agg
    aggregate.__doc__ = inspect.getdoc(vendored_pandas_series.Series.agg)

    def describe(self) -> Series:
        from bigframes.pandas.core.methods import describe

        return cast(Series, describe.describe(self, include="all"))

    def skew(self):
        count = self.count()
        if count < 3:
            return pandas.NA

        moment3 = self._central_moment(3)
        moment2 = self.var() * (count - 1) / count  # Convert sample var to pop var

        # See G1 estimator:
        # https://en.wikipedia.org/wiki/Skewness#Sample_skewness
        numerator = moment3
        denominator = moment2 ** (3 / 2)
        adjustment = (count * (count - 1)) ** 0.5 / (count - 2)

        return (numerator / denominator) * adjustment

    def kurt(self):
        count = self.count()
        if count < 4:
            return pandas.NA

        moment4 = self._central_moment(4)
        moment2 = self.var() * (count - 1) / count  # Convert sample var to pop var

        # Kurtosis is often defined as the second standardize moment: moment(4)/moment(2)**2
        # Pandas however uses Fisher’s estimator, implemented below
        numerator = (count + 1) * (count - 1) * moment4
        denominator = (count - 2) * (count - 3) * moment2**2
        adjustment = 3 * (count - 1) ** 2 / ((count - 2) * (count - 3))

        return (numerator / denominator) - adjustment

    kurtosis = kurt
    kurtosis.__doc__ = inspect.getdoc(vendored_pandas_series.Series.kurt)

    def mode(self) -> Series:
        block = self._block
        # Approach: Count each value, return each value for which count(x) == max(counts))
        block, agg_ids = block.aggregate(
            by_column_ids=[self._value_column],
            aggregations=(
                ex.UnaryAggregation(agg_ops.count_op, ex.deref(self._value_column)),
            ),
        )
        value_count_col_id = agg_ids[0]
        block, max_value_count_col_id = block.apply_window_op(
            value_count_col_id,
            agg_ops.max_op,
            window_spec=windows.unbound(),
        )
        block, is_mode_col_id = block.apply_binary_op(
            value_count_col_id,
            max_value_count_col_id,
            ops.eq_op,
        )
        block = block.filter_by_id(is_mode_col_id)
        # use temporary name for reset_index to avoid collision, restore after dropping extra columns
        block = (
            block.with_index_labels(["mode_temp_internal"])
            .order_by([order.ascending_over(self._value_column)])
            .reset_index(drop=False)
        )
        block = block.select_column(self._value_column).with_column_labels([self.name])
        mode_values_series = Series(block.select_column(self._value_column))
        return typing.cast(Series, mode_values_series)

    def mean(self) -> float:
        return typing.cast(float, self._apply_aggregation(agg_ops.mean_op))

    def median(self, *, exact: bool = True) -> float:
        if exact:
            return typing.cast(float, self.quantile(0.5))
        else:
            return typing.cast(float, self._apply_aggregation(agg_ops.median_op))

    def quantile(self, q: Union[float, Sequence[float]] = 0.5) -> Union[Series, float]:
        qs = tuple(q) if utils.is_list_like(q) else (q,)
        result = block_ops.quantile(self._block, (self._value_column,), qs=qs)
        if utils.is_list_like(q):
            # Drop the first level, since only one column
            result = result.with_column_labels(result.column_labels.droplevel(0))
            result, index_col = result.create_constant(self.name, None)
            result = result.set_index([index_col])
            return Series(
                result.transpose(original_row_index=pandas.Index([self.name]))
            )
        else:
            return cast(float, Series(result).to_pandas().squeeze())

    def sum(self) -> float:
        return typing.cast(float, self._apply_aggregation(agg_ops.sum_op))

    def prod(self) -> float:
        return typing.cast(float, self._apply_aggregation(agg_ops.product_op))

    product = prod
    product.__doc__ = inspect.getdoc(vendored_pandas_series.Series.prod)

    def __eq__(self, other: object) -> Series:  # type: ignore
        return self.eq(other)

    def __ne__(self, other: object) -> Series:  # type: ignore
        return self.ne(other)

    def __invert__(self) -> Series:
        return self._apply_unary_op(ops.invert_op)

    __invert__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__invert__)

    def __pos__(self) -> Series:
        return self._apply_unary_op(ops.pos_op)

    def __neg__(self) -> Series:
        return self._apply_unary_op(ops.neg_op)

    def __dir__(self) -> List[str]:
        return dir(type(self)) + self._struct_fields

    def eq(self, other: object) -> Series:
        # TODO: enforce stricter alignment
        return self._apply_binary_op(other, ops.eq_op)

    def ne(self, other: object) -> Series:
        # TODO: enforce stricter alignment
        return self._apply_binary_op(other, ops.ne_op)

    def items(self):
        for batch_df in self._block.to_pandas_batches():
            assert (
                batch_df.shape[1] == 1
            ), f"Expected 1 column in the dataframe, but got {batch_df.shape[1]}."
            for item in batch_df.squeeze(axis=1).items():
                yield item

    def where(self, cond, other=None):
        value_id, cond_id, other_id, block = self._align3(cond, other)
        block, result_id = block.project_expr(
            ops.where_op.as_expr(value_id, cond_id, other_id)
        )
        return Series(block.select_column(result_id).with_column_labels([self.name]))

    def clip(self, lower=None, upper=None):
        if lower is None and upper is None:
            return self
        if lower is None:
            return self._apply_binary_op(upper, ops.minimum_op, alignment="left")
        if upper is None:
            return self._apply_binary_op(lower, ops.maximum_op, alignment="left")
        # special rule to coerce scalar string args to date
        value_id, lower_id, upper_id, block = self._align3(
            lower, upper, cast_scalars=(bigframes.dtypes.is_date_like(self.dtype))
        )
        block, result_id = block.project_expr(
            ops.clip_op.as_expr(value_id, lower_id, upper_id),
        )
        return Series(block.select_column(result_id).with_column_labels([self.name]))

    @validations.requires_ordering()
    def argmax(self) -> int:
        block, row_nums = self._block.promote_offsets()
        block = block.order_by(
            [
                order.descending_over(self._value_column),
                order.ascending_over(row_nums),
            ]
        )
        return typing.cast(
            scalars.Scalar, Series(block.select_column(row_nums)).iloc[0]
        )

    @validations.requires_ordering()
    def argmin(self) -> int:
        block, row_nums = self._block.promote_offsets()
        block = block.order_by(
            [
                order.ascending_over(self._value_column),
                order.ascending_over(row_nums),
            ]
        )
        return typing.cast(
            scalars.Scalar, Series(block.select_column(row_nums)).iloc[0]
        )

    @validations.requires_index
    def unstack(self, level: LevelsType = -1):
        if isinstance(level, int) or isinstance(level, str):
            level = [level]

        block = self._block

        if self.index.nlevels == 1:
            raise ValueError("Series must have multi-index to unstack")

        # Pivot by index levels
        unstack_ids = self._resolve_levels(level)
        block = block.reset_index(drop=False)
        block = block.set_index(
            [col for col in self._block.index_columns if col not in unstack_ids]
        )

        pivot_block = block.pivot(
            columns=unstack_ids,
            values=self._block.value_columns,
            values_in_index=False,
        )
        return bigframes.dataframe.DataFrame(pivot_block)

    @validations.requires_index
    def idxmax(self) -> blocks.Label:
        block = self._block.order_by(
            [
                order.descending_over(self._value_column),
                *[
                    order.ascending_over(idx_col)
                    for idx_col in self._block.index_columns
                ],
            ]
        )
        block = block.slice(0, 1)
        return indexes.Index(block).to_pandas()[0]

    @validations.requires_index
    def idxmin(self) -> blocks.Label:
        block = self._block.order_by(
            [
                order.ascending_over(self._value_column),
                *[
                    order.ascending_over(idx_col)
                    for idx_col in self._block.index_columns
                ],
            ]
        )
        block = block.slice(0, 1)
        return indexes.Index(block).to_pandas()[0]

    @property
    @validations.requires_ordering()
    def is_monotonic_increasing(self) -> bool:
        return typing.cast(
            bool, self._block.is_monotonic_increasing(self._value_column)
        )

    @property
    @validations.requires_ordering()
    def is_monotonic_decreasing(self) -> bool:
        return typing.cast(
            bool, self._block.is_monotonic_decreasing(self._value_column)
        )

    def __getitem__(self, indexer):
        # TODO: enforce stricter alignment, should fail if indexer is missing any keys.
        use_iloc = (
            isinstance(indexer, slice)
            and all(
                isinstance(x, numbers.Integral) or (x is None)
                for x in [indexer.start, indexer.stop, indexer.step]
            )
        ) or (
            isinstance(indexer, numbers.Integral)
            and not isinstance(self._block.index.dtypes[0], pandas.Int64Dtype)
        )
        if use_iloc:
            return self.iloc[indexer]
        if isinstance(indexer, Series):
            (left, right, block) = self._align(indexer, "left")
            block = block.filter(right)
            block = block.select_column(left.id.name)
            return Series(block)
        return self.loc[indexer]

    __getitem__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__getitem__)

    def __getattr__(self, key: str):
        # Protect against recursion errors with uninitialized Series objects.
        # We use "_block" attribute to check whether the instance is initialized.
        # See:
        # https://github.com/googleapis/python-bigquery-dataframes/issues/728
        # and
        # https://nedbatchelder.com/blog/201010/surprising_getattr_recursion.html
        if key == "_block":
            raise AttributeError(key)
        elif hasattr(pandas.Series, key):
            log_adapter.submit_pandas_labels(
                self._block.session.bqclient, self.__class__.__name__, key
            )
            raise AttributeError(
                textwrap.dedent(
                    f"""
                    BigQuery DataFrames has not yet implemented an equivalent to
                    'pandas.Series.{key}'. {constants.FEEDBACK_LINK}
                    """
                )
            )
        elif key in self._struct_fields:
            return self.struct.field(key)
        else:
            raise AttributeError(key)

    def __setitem__(self, key, value) -> None:
        """Set item using direct assignment, delegating to .loc indexer."""
        self.loc[key] = value

    def _apply_aggregation(
        self, op: agg_ops.UnaryAggregateOp | agg_ops.NullaryAggregateOp
    ) -> Any:
        return self._block.get_stat(self._value_column, op)

    def _apply_window_op(
        self, op: agg_ops.UnaryWindowOp, window_spec: windows.WindowSpec
    ):
        block = self._block
        block, result_id = block.apply_window_op(
            self._value_column, op, window_spec=window_spec, result_label=self.name
        )
        return Series(block.select_column(result_id))

    def value_counts(
        self,
        normalize: bool = False,
        sort: bool = True,
        ascending: bool = False,
        *,
        dropna: bool = True,
    ):
        block = block_ops.value_counts(
            self._block,
            [self._value_column],
            normalize=normalize,
            ascending=ascending,
            dropna=dropna,
        )
        return Series(block)

    @typing.overload  # type: ignore[override]
    def sort_values(
        self,
        *,
        axis=...,
        inplace: Literal[True] = ...,
        ascending: bool | typing.Sequence[bool] = ...,
        kind: str = ...,
        na_position: typing.Literal["first", "last"] = ...,
    ) -> None:
        ...

    @typing.overload
    def sort_values(
        self,
        *,
        axis=...,
        inplace: Literal[False] = ...,
        ascending: bool | typing.Sequence[bool] = ...,
        kind: str = ...,
        na_position: typing.Literal["first", "last"] = ...,
    ) -> Series:
        ...

    def sort_values(
        self,
        *,
        axis=0,
        inplace: bool = False,
        ascending=True,
        kind: str = "quicksort",
        na_position: typing.Literal["first", "last"] = "last",
    ) -> Optional[Series]:
        if axis != 0 and axis != "index":
            raise ValueError(f"No axis named {axis} for object type Series")
        if na_position not in ["first", "last"]:
            raise ValueError("Param na_position must be one of 'first' or 'last'")
        block = self._block.order_by(
            [
                order.ascending_over(self._value_column, (na_position == "last"))
                if ascending
                else order.descending_over(self._value_column, (na_position == "last"))
            ],
        )
        if inplace:
            self._set_block(block)
            return None
        else:
            return Series(block)

    @typing.overload  # type: ignore[override]
    def sort_index(
        self, *, axis=..., inplace: Literal[False] = ..., ascending=..., na_position=...
    ) -> Series:
        ...

    @typing.overload
    def sort_index(
        self, *, axis=0, inplace: Literal[True] = ..., ascending=..., na_position=...
    ) -> None:
        ...

    @validations.requires_index
    def sort_index(
        self, *, axis=0, inplace: bool = False, ascending=True, na_position="last"
    ) -> Optional[Series]:
        # TODO(tbergeron): Support level parameter once multi-index introduced.
        if axis != 0 and axis != "index":
            raise ValueError(f"No axis named {axis} for object type Series")
        if na_position not in ["first", "last"]:
            raise ValueError("Param na_position must be one of 'first' or 'last'")
        block = self._block
        na_last = na_position == "last"
        ordering = [
            order.ascending_over(column, na_last)
            if ascending
            else order.descending_over(column, na_last)
            for column in block.index_columns
        ]
        block = block.order_by(ordering)
        if inplace:
            self._set_block(block)
            return None
        else:
            return Series(block)

    @validations.requires_ordering()
    def rolling(
        self,
        window: int | pandas.Timedelta | numpy.timedelta64 | datetime.timedelta | str,
        min_periods: int | None = None,
        closed: Literal["right", "left", "both", "neither"] = "right",
    ) -> bigframes.core.window.Window:
        if isinstance(window, int):
            # Rows rolling
            window_spec = windows.WindowSpec(
                bounds=windows.RowsWindowBounds.from_window_size(window, closed),
                min_periods=window if min_periods is None else min_periods,
            )
            return bigframes.core.window.Window(
                self._block, window_spec, self._block.value_columns, is_series=True
            )

        return rolling.create_range_window(
            block=self._block,
            window=window,
            min_periods=min_periods,
            closed=closed,
            is_series=True,
        )

    @validations.requires_ordering()
    def expanding(self, min_periods: int = 1) -> bigframes.core.window.Window:
        window_spec = windows.cumulative_rows(min_periods=min_periods)
        return bigframes.core.window.Window(
            self._block, window_spec, self._block.value_columns, is_series=True
        )

    def groupby(
        self,
        by: typing.Union[
            blocks.Label, Series, typing.Sequence[typing.Union[blocks.Label, Series]]
        ] = None,
        axis=0,
        level: typing.Optional[
            int | str | typing.Sequence[int] | typing.Sequence[str]
        ] = None,
        as_index: bool = True,
        *,
        dropna: bool = True,
    ) -> bigframes.core.groupby.SeriesGroupBy:
        if (by is not None) and (level is not None):
            raise ValueError("Do not specify both 'by' and 'level'")
        if not as_index:
            raise ValueError("as_index=False only valid with DataFrame")
        if axis:
            raise ValueError("No axis named {} for object type Series".format(level))
        if not as_index:
            raise ValueError("'as_index'=False only applies to DataFrame")
        if by is not None:
            return self._groupby_values(by, dropna)
        if level is not None:
            return self._groupby_level(level, dropna)
        else:
            raise TypeError("You have to supply one of 'by' and 'level'")

    @validations.requires_index
    def _groupby_level(
        self,
        level: int | str | typing.Sequence[int] | typing.Sequence[str],
        dropna: bool = True,
    ) -> bigframes.core.groupby.SeriesGroupBy:
        return groupby.SeriesGroupBy(
            self._block,
            self._value_column,
            by_col_ids=self._resolve_levels(level),
            value_name=self.name,
            dropna=dropna,
        )

    def _groupby_values(
        self,
        by: typing.Union[
            blocks.Label, Series, typing.Sequence[typing.Union[blocks.Label, Series]]
        ],
        dropna: bool = True,
    ) -> bigframes.core.groupby.SeriesGroupBy:
        if not isinstance(by, Series) and _is_list_like(by):
            by = list(by)
        else:
            by = [typing.cast(typing.Union[blocks.Label, Series], by)]

        block = self._block
        grouping_cols: typing.Sequence[str] = []
        value_col = self._value_column
        for key in by:
            if isinstance(key, Series):
                block, (
                    get_column_left,
                    get_column_right,
                ) = block.join(key._block, how="inner" if dropna else "left")

                value_col = get_column_left[value_col]
                grouping_cols = [
                    *[get_column_left[value] for value in grouping_cols],
                    get_column_right[key._value_column],
                ]
            else:
                # Interpret as index level
                matches = block.index_name_to_col_id.get(key, [])
                if len(matches) != 1:
                    raise ValueError(
                        f"GroupBy key {key} does not match a unique index level. BigQuery DataFrames only interprets lists of strings as index level names, not directly as per-row group assignments."
                    )
                grouping_cols = [*grouping_cols, matches[0]]

        return groupby.SeriesGroupBy(
            block,
            value_col,
            by_col_ids=grouping_cols,
            value_name=self.name,
            dropna=dropna,
        )

    def apply(
        self, func, by_row: typing.Union[typing.Literal["compat"], bool] = "compat"
    ) -> Series:
        # TODO(shobs, b/274645634): Support convert_dtype, args, **kwargs
        # is actually a ternary op

        if by_row not in ["compat", False]:
            raise ValueError("Param by_row must be one of 'compat' or False")

        if not callable(func):
            raise ValueError(
                "Only a ufunc (a function that applies to the entire Series) or"
                " a BigFrames BigQuery function that only works on single values"
                " are supported."
            )

        if not isinstance(func, bigframes.functions.BigqueryCallableRoutine):
            # It is neither a remote function nor a managed function.
            # Then it must be a vectorized function that applies to the Series
            # as a whole.
            if by_row:
                raise ValueError(
                    "You have passed a function as-is. If your intention is to "
                    "apply this function in a vectorized way (i.e. to the "
                    "entire Series as a whole, and you are sure that it "
                    "performs only the operations that are implemented for a "
                    "Series (e.g. a chain of arithmetic/logical operations, "
                    "such as `def foo(s): return s % 2 == 1`), please also "
                    "specify `by_row=False`. If your function contains "
                    "arbitrary code, it can only be applied to every element "
                    "in the Series individually, in which case you must "
                    "convert it to a BigFrames BigQuery function using "
                    "`bigframes.pandas.udf`, "
                    "or `bigframes.pandas.remote_function` before passing."
                )

            try:
                return func(self)
            except Exception as ex:
                # This could happen if any of the operators in func is not
                # supported on a Series. Let's guide the customer to use a
                # bigquery function instead
                if hasattr(ex, "message"):
                    ex.message += f"\n{_bigquery_function_recommendation_message}"
                raise

        # We are working with bigquery function at this point
        result_series = self._apply_unary_op(
            ops.RemoteFunctionOp(function_def=func.udf_def, apply_on_null=True)
        )
        result_series = func._post_process_series(result_series)
        return result_series

    def combine(
        self,
        other,
        func,
    ) -> Series:
        if not callable(func):
            raise ValueError(
                "Only a ufunc (a function that applies to the entire Series) or"
                " a BigFrames BigQuery function that only works on single values"
                " are supported."
            )

        if not isinstance(func, bigframes.functions.BigqueryCallableRoutine):
            # Keep this in sync with .apply
            try:
                return func(self, other)
            except Exception as ex:
                # This could happen if any of the operators in func is not
                # supported on a Series. Let's guide the customer to use a
                # bigquery function instead
                if hasattr(ex, "message"):
                    ex.message += f"\n{_bigquery_function_recommendation_message}"
                raise

        result_series = self._apply_binary_op(
            other, ops.BinaryRemoteFunctionOp(function_def=func.udf_def)
        )
        result_series = func._post_process_series(result_series)
        return result_series

    @validations.requires_index
    def add_prefix(self, prefix: str, axis: int | str | None = None) -> Series:
        return Series(self._get_block().add_prefix(prefix))

    @validations.requires_index
    def add_suffix(self, suffix: str, axis: int | str | None = None) -> Series:
        return Series(self._get_block().add_suffix(suffix))

    def take(
        self, indices: typing.Sequence[int], axis: int | str | None = 0, **kwargs
    ) -> Series:
        if not utils.is_list_like(indices):
            raise ValueError("indices should be a list-like object.")
        return typing.cast(Series, self.iloc[indices])

    def filter(
        self,
        items: typing.Optional[typing.Iterable] = None,
        like: typing.Optional[str] = None,
        regex: typing.Optional[str] = None,
        axis: typing.Optional[typing.Union[str, int]] = None,
    ) -> Series:
        if (axis is not None) and utils.get_axis_number(axis) != 0:
            raise ValueError(f"Invalid axis for series: {axis}")
        if sum([(items is not None), (like is not None), (regex is not None)]) != 1:
            raise ValueError(
                "Need to provide exactly one of 'items', 'like', or 'regex'"
            )
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
            block = block.select_columns([self._value_column])
            return Series(block)
        elif items is not None:
            # Behavior matches pandas 2.1+, older pandas versions would reindex
            block = self._block
            block, mask_id = block.apply_unary_op(
                self._block.index_columns[0], ops.IsInOp(values=tuple(items))
            )
            block = block.filter_by_id(mask_id)
            block = block.select_columns([self._value_column])
            return Series(block)
        else:
            raise ValueError("Need to provide 'items', 'like', or 'regex'")

    @validations.requires_index
    def reindex(self, index=None, *, validate: typing.Optional[bool] = None):
        if validate and not self.index.is_unique:
            raise ValueError("Original index must be unique to reindex")
        keep_original_names = False
        if isinstance(index, indexes.Index):
            new_indexer = bigframes.dataframe.DataFrame(data=index._block)[[]]
        else:
            if not isinstance(index, pandas.Index):
                keep_original_names = True
                index = pandas.Index(index)
            if index.nlevels != self.index.nlevels:
                raise NotImplementedError(
                    "Cannot reindex with index with different nlevels"
                )
            new_indexer = bigframes.dataframe.DataFrame(
                index=index, session=self._get_block().expr.session
            )[[]]
        # multiindex join is senstive to index names, so we will set all these
        result = new_indexer.rename_axis(range(new_indexer.index.nlevels)).join(
            self.to_frame().rename_axis(range(self.index.nlevels)),
            how="left",
        )
        # and then reset the names after the join
        result_block = result.rename_axis(
            self.index.names if keep_original_names else index.names
        )._block
        return Series(result_block)

    @validations.requires_index
    def reindex_like(self, other: Series, *, validate: typing.Optional[bool] = None):
        return self.reindex(other.index, validate=validate)

    def drop_duplicates(self, *, keep: str = "first") -> Series:
        if keep is not False:
            validations.enforce_ordered(self, "drop_duplicates(keep != False)")
        block = block_ops.drop_duplicates(self._block, (self._value_column,), keep)
        return Series(block)

    def unique(self, keep_order=True) -> Series:
        if keep_order:
            validations.enforce_ordered(self, "unique(keep_order != False)")
            return self.drop_duplicates()
        block, result = self._block.aggregate(
            [self._value_column],
            [ex.UnaryAggregation(agg_ops.AnyValueOp(), ex.deref(self._value_column))],
            column_labels=self._block.column_labels,
            dropna=False,
        )
        return Series(block.select_columns(result).reset_index())

    def duplicated(self, keep: str = "first") -> Series:
        if keep is not False:
            validations.enforce_ordered(self, "duplicated(keep != False)")
        block, indicator = block_ops.indicate_duplicates(
            self._block, (self._value_column,), keep
        )
        return Series(
            block.select_column(
                indicator,
            ).with_column_labels([self.name])
        )

    def mask(self, cond, other=None) -> Series:
        if callable(cond):
            if hasattr(cond, "bigframes_bigquery_function"):
                cond = self.apply(cond)
            else:
                # For non-BigQuery function assume that it is applicable on Series
                cond = self.apply(cond, by_row=False)

        if not isinstance(cond, Series):
            raise TypeError(
                f"Only bigframes series condition is supported, received {type(cond).__name__}. "
                f"{constants.FEEDBACK_LINK}"
            )
        return self.where(~cond, other)

    def to_frame(self, name: blocks.Label = None) -> bigframes.dataframe.DataFrame:
        provided_name = name if name else self.name
        # To be consistent with Pandas, it assigns 0 as the column name if missing. 0 is the first element of RangeIndex.
        block = self._block.with_column_labels(
            [provided_name] if provided_name else [0]
        )
        return bigframes.dataframe.DataFrame(block)

    def to_csv(
        self,
        path_or_buf=None,
        sep=",",
        *,
        header: bool = True,
        index: bool = True,
        allow_large_results: Optional[bool] = None,
    ) -> Optional[str]:
        if utils.is_gcs_path(path_or_buf):
            return self.to_frame().to_csv(
                path_or_buf,
                sep=sep,
                header=header,
                index=index,
                allow_large_results=allow_large_results,
            )
        else:
            pd_series = self.to_pandas(allow_large_results=allow_large_results)
            return pd_series.to_csv(
                path_or_buf=path_or_buf, sep=sep, header=header, index=index
            )

    def to_dict(
        self,
        into: type[dict] = dict,
        *,
        allow_large_results: Optional[bool] = None,
    ) -> typing.Mapping:
        return typing.cast(dict, self.to_pandas(allow_large_results=allow_large_results).to_dict(into))  # type: ignore

    def to_excel(
        self, excel_writer, sheet_name="Sheet1", *, allow_large_results=None, **kwargs
    ) -> None:
        return self.to_pandas(allow_large_results=allow_large_results).to_excel(
            excel_writer, sheet_name, **kwargs
        )

    def to_json(
        self,
        path_or_buf=None,
        orient: Optional[
            typing.Literal["split", "records", "index", "columns", "values", "table"]
        ] = None,
        *,
        lines: bool = False,
        index: bool = True,
        allow_large_results: Optional[bool] = None,
    ) -> Optional[str]:
        if utils.is_gcs_path(path_or_buf):
            return self.to_frame().to_json(
                path_or_buf=path_or_buf,
                orient=orient,
                lines=lines,
                index=index,
                allow_large_results=allow_large_results,
            )
        else:
            pd_series = self.to_pandas(allow_large_results=allow_large_results)
            return pd_series.to_json(
                path_or_buf=path_or_buf, orient=orient, lines=lines, index=index  # type: ignore
            )

    def to_latex(
        self,
        buf=None,
        columns=None,
        header=True,
        index=True,
        *,
        allow_large_results=None,
        **kwargs,
    ) -> typing.Optional[str]:
        return self.to_pandas(allow_large_results=allow_large_results).to_latex(
            buf, columns=columns, header=header, index=index, **kwargs
        )

    def tolist(
        self,
        *,
        allow_large_results: Optional[bool] = None,
    ) -> _list:
        return self.to_pandas(allow_large_results=allow_large_results).to_list()

    to_list = tolist
    to_list.__doc__ = inspect.getdoc(vendored_pandas_series.Series.tolist)

    def to_markdown(
        self,
        buf: typing.IO[str] | None = None,
        mode: str = "wt",
        index: bool = True,
        *,
        allow_large_results: Optional[bool] = None,
        **kwargs,
    ) -> typing.Optional[str]:
        return self.to_pandas(allow_large_results=allow_large_results).to_markdown(buf, mode=mode, index=index, **kwargs)  # type: ignore

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

    __array__.__doc__ = inspect.getdoc(vendored_pandas_series.Series.__array__)

    def to_pickle(self, path, *, allow_large_results=None, **kwargs) -> None:
        return self.to_pandas(allow_large_results=allow_large_results).to_pickle(
            path, **kwargs
        )

    def to_string(
        self,
        buf=None,
        na_rep="NaN",
        float_format=None,
        header=True,
        index=True,
        length=False,
        dtype=False,
        name=False,
        max_rows=None,
        min_rows=None,
        *,
        allow_large_results=None,
    ) -> typing.Optional[str]:
        return self.to_pandas(allow_large_results=allow_large_results).to_string(
            buf,
            na_rep,
            float_format,
            header,
            index,
            length,
            dtype,
            name,
            max_rows,
            min_rows,
        )

    def to_xarray(
        self,
        *,
        allow_large_results: Optional[bool] = None,
    ):
        return self.to_pandas(allow_large_results=allow_large_results).to_xarray()

    def _throw_if_index_contains_duplicates(
        self, error_message: typing.Optional[str] = None
    ) -> None:
        if not self.index.is_unique:
            error_message = (
                error_message
                if error_message
                else "Index contains duplicate entries, but uniqueness is required."
            )
            raise pandas.errors.InvalidIndexError(error_message)

    def map(
        self,
        arg: typing.Union[Mapping, Series],
        na_action: Optional[str] = None,
        *,
        verify_integrity: bool = False,
    ) -> Series:
        if na_action:
            raise NotImplementedError(
                f"Non-None na_action argument is not yet supported for Series.map. {constants.FEEDBACK_LINK}"
            )
        if isinstance(arg, Series):
            if verify_integrity:
                error_message = "When verify_integrity is True in Series.map, index of arg parameter must not have duplicate entries."
                arg._throw_if_index_contains_duplicates(error_message=error_message)
            map_df = bigframes.dataframe.DataFrame(arg._block)
            map_df = map_df.rename(columns={arg.name: self.name})
        elif isinstance(arg, Mapping):
            map_df = bigframes.dataframe.DataFrame(
                {"keys": list(arg.keys()), self.name: list(arg.values())},  # type: ignore
                session=self._get_block().expr.session,
            )
            map_df = map_df.set_index("keys")
        elif callable(arg):
            return self.apply(arg)
        else:
            # Mirroring pandas, call the uncallable object
            arg()  # throws TypeError: object is not callable

        self_df = self.to_frame(name="series")
        result_df = self_df.join(map_df, on="series")
        return result_df[self.name]

    @validations.requires_ordering()
    def sample(
        self,
        n: Optional[int] = None,
        frac: Optional[float] = None,
        *,
        random_state: Optional[int] = None,
        sort: Optional[bool | Literal["random"]] = "random",
    ) -> Series:
        if n is not None and frac is not None:
            raise ValueError("Only one of 'n' or 'frac' parameter can be specified.")

        ns = (n,) if n is not None else ()
        fracs = (frac,) if frac is not None else ()
        return Series(
            self._block.split(ns=ns, fracs=fracs, random_state=random_state, sort=sort)[
                0
            ]
        )

    def explode(self, *, ignore_index: Optional[bool] = False) -> Series:
        return Series(
            self._block.explode(
                column_ids=[self._value_column], ignore_index=ignore_index
            )
        )

    @validations.requires_ordering()
    def _resample(
        self,
        rule: str,
        *,
        closed: Optional[Literal["right", "left"]] = None,
        label: Optional[Literal["right", "left"]] = None,
        level: Optional[LevelsType] = None,
        origin: Union[
            Union[
                pandas.Timestamp, datetime.datetime, numpy.datetime64, int, float, str
            ],
            Literal["epoch", "start", "start_day", "end", "end_day"],
        ] = "start_day",
    ) -> bigframes.core.groupby.SeriesGroupBy:
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
        ... }
        >>> s = bpd.DataFrame(data).set_index("timestamp_col")
        >>> s._resample(rule="7s", origin="epoch").min()
                             int64_col
        2021-01-01 12:59:56          0
        2021-01-01 13:00:03          3
        2021-01-01 13:00:10         10
        2021-01-01 13:00:17         17
        2021-01-01 13:00:24         24
        <BLANKLINE>
        [5 rows x 1 columns]


        Args:
            rule (str):
                The offset string representing target conversion.
            level (str or int, default None):
                For a MultiIndex, level (name or number) to use for resampling.
                level must be datetime-like.
            origin(str, default 'start_day'):
                The timestamp on which to adjust the grouping. Must be one of the following:
                'epoch': origin is 1970-01-01
                'start': origin is the first value of the timeseries
                'start_day': origin is the first day at midnight of the timeseries
        Returns:
            SeriesGroupBy: SeriesGroupBy object.
        """
        block = self._block._generate_resample_label(
            rule=rule,
            closed=closed,
            label=label,
            on=None,
            level=level,
            origin=origin,
        )
        series = Series(block)
        return series.groupby(level=0)

    def __array_ufunc__(
        self, ufunc: numpy.ufunc, method: str, *inputs, **kwargs
    ) -> Series:
        """Used to support numpy ufuncs.
        See: https://numpy.org/doc/stable/reference/ufuncs.html
        """
        # Only __call__ supported with zero arguments
        if method != "__call__" or len(inputs) > 2 or len(kwargs) > 0:
            return NotImplemented

        if len(inputs) == 1 and ufunc in ops.NUMPY_TO_OP:
            return self._apply_unary_op(ops.NUMPY_TO_OP[ufunc])
        if len(inputs) == 2 and ufunc in ops.NUMPY_TO_BINOP:
            binop = ops.NUMPY_TO_BINOP[ufunc]
            if inputs[0] is self:
                return self._apply_binary_op(inputs[1], binop)
            else:
                return self._apply_binary_op(inputs[0], binop, reverse=True)

        return NotImplemented

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

    def _slice(
        self,
        start: typing.Optional[int] = None,
        stop: typing.Optional[int] = None,
        step: typing.Optional[int] = None,
    ) -> bigframes.series.Series:
        return bigframes.series.Series(
            self._block.slice(
                start=start, stop=stop, step=step if (step is not None) else 1
            ).select_column(self._value_column),
        )

    def cache(self):
        """
        Materializes the Series to a temporary table.

        Useful if the series will be used multiple times, as this will avoid recomputating the shared intermediate value.

        Returns:
            Series: Self
        """
        # Do not use session-aware cashing if user-requested
        return self._cached(force=True, session_aware=False)

    def _cached(self, *, force: bool = True, session_aware: bool = True) -> Series:
        self._block.cached(force=force, session_aware=session_aware)
        return self

    # Keep this at the bottom of the Series class to avoid
    # confusing type checker by overriding str
    @property
    def str(self) -> strings.StringMethods:
        return strings.StringMethods(self._block)


def _is_list_like(obj: typing.Any) -> typing_extensions.TypeGuard[typing.Sequence]:
    return pandas.api.types.is_list_like(obj)
