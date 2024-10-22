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

"""Session manages the connection to BigQuery."""

from __future__ import annotations

import logging
import os
import secrets
import typing
from typing import (
    Any,
    Callable,
    Dict,
    IO,
    Iterable,
    Literal,
    Mapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Union,
)
import warnings
import weakref

import bigframes_vendored.constants as constants
import bigframes_vendored.ibis.backends.bigquery  # noqa
import bigframes_vendored.pandas.io.gbq as third_party_pandas_gbq
import bigframes_vendored.pandas.io.parquet as third_party_pandas_parquet
import bigframes_vendored.pandas.io.parsers.readers as third_party_pandas_readers
import bigframes_vendored.pandas.io.pickle as third_party_pandas_pickle
import google.cloud.bigquery as bigquery
import google.cloud.storage as storage  # type: ignore
import ibis
import ibis.backends.bigquery as ibis_bigquery
import numpy as np
import pandas
from pandas._typing import (
    CompressionOptions,
    FilePath,
    ReadPickleBuffer,
    StorageOptions,
)
import pyarrow as pa

import bigframes._config.bigquery_options as bigquery_options
import bigframes.clients
import bigframes.core as core
import bigframes.core.blocks as blocks
import bigframes.core.compile
import bigframes.core.guid
import bigframes.core.pruning

# Even though the ibis.backends.bigquery import is unused, it's needed
# to register new and replacement ops with the Ibis BigQuery backend.
import bigframes.dataframe
import bigframes.dtypes
import bigframes.exceptions
import bigframes.functions._remote_function_session as bigframes_rf_session
import bigframes.functions.remote_function as bigframes_rf
import bigframes.session._io.bigquery as bf_io_bigquery
import bigframes.session.clients
import bigframes.session.executor
import bigframes.session.loader
import bigframes.session.metrics
import bigframes.session.planner
import bigframes.session.temp_storage
import bigframes.version

# Avoid circular imports.
if typing.TYPE_CHECKING:
    import bigframes.core.indexes
    import bigframes.dataframe as dataframe
    import bigframes.series
    import bigframes.streaming.dataframe as streaming_dataframe

_BIGFRAMES_DEFAULT_CONNECTION_ID = "bigframes-default-connection"

# TODO(swast): Need to connect to regional endpoints when performing remote
# functions operations (BQ Connection IAM, Cloud Run / Cloud Functions).
# Also see if resource manager client library supports regional endpoints.

_VALID_ENCODINGS = {
    "UTF-8",
    "ISO-8859-1",
    "UTF-16BE",
    "UTF-16LE",
    "UTF-32BE",
    "UTF-32LE",
}

# BigQuery has 1 MB query size limit. Don't want to take up more than a few % of that inlining a table.
# Also must assume that text encoding as literals is much less efficient than in-memory representation.
MAX_INLINE_DF_BYTES = 5000

logger = logging.getLogger(__name__)

# Excludes geography, bytes, and nested (array, struct) datatypes
INLINABLE_DTYPES: Sequence[bigframes.dtypes.Dtype] = (
    pandas.BooleanDtype(),
    pandas.Float64Dtype(),
    pandas.Int64Dtype(),
    pandas.StringDtype(storage="pyarrow"),
    pandas.ArrowDtype(pa.date32()),
    pandas.ArrowDtype(pa.time64("us")),
    pandas.ArrowDtype(pa.timestamp("us")),
    pandas.ArrowDtype(pa.timestamp("us", tz="UTC")),
    pandas.ArrowDtype(pa.decimal128(38, 9)),
    pandas.ArrowDtype(pa.decimal256(76, 38)),
)


class Session(
    third_party_pandas_gbq.GBQIOMixin,
    third_party_pandas_parquet.ParquetIOMixin,
    third_party_pandas_pickle.PickleIOMixin,
    third_party_pandas_readers.ReaderIOMixin,
):
    """Establishes a BigQuery connection to capture a group of job activities related to
    DataFrames.

    Args:
        context (bigframes._config.bigquery_options.BigQueryOptions):
            Configuration adjusting how to connect to BigQuery and related
            APIs. Note that some options are ignored if ``clients_provider`` is
            set.
        clients_provider (bigframes.session.clients.ClientsProvider):
            An object providing client library objects.
    """

    def __init__(
        self,
        context: Optional[bigquery_options.BigQueryOptions] = None,
        clients_provider: Optional[bigframes.session.clients.ClientsProvider] = None,
    ):
        if context is None:
            context = bigquery_options.BigQueryOptions()

        if context.location is None:
            self._location = "US"
            warnings.warn(
                f"No explicit location is set, so using location {self._location} for the session.",
                # User's code
                # -> get_global_session()
                # -> connect()
                # -> Session()
                #
                # Note: We could also have:
                # User's code
                # -> read_gbq()
                # -> with_default_session()
                # -> get_global_session()
                # -> connect()
                # -> Session()
                # but we currently have no way to disambiguate these
                # situations.
                stacklevel=4,
                category=bigframes.exceptions.DefaultLocationWarning,
            )
        else:
            self._location = context.location

        self._bq_kms_key_name = context.kms_key_name

        # Instantiate a clients provider to help with cloud clients that will be
        # used in the future operations in the session
        if clients_provider:
            self._clients_provider = clients_provider
        else:
            self._clients_provider = bigframes.session.clients.ClientsProvider(
                project=context.project,
                location=self._location,
                use_regional_endpoints=context.use_regional_endpoints,
                credentials=context.credentials,
                application_name=context.application_name,
                bq_kms_key_name=self._bq_kms_key_name,
            )

        # TODO(shobs): Remove this logic after https://github.com/ibis-project/ibis/issues/8494
        # has been fixed. The ibis client changes the default query job config
        # so we are going to remember the current config and restore it after
        # the ibis client has been created
        original_default_query_job_config = self.bqclient.default_query_job_config

        # Only used to fetch remote function metadata.
        # TODO: Remove in favor of raw bq client
        self.ibis_client = typing.cast(
            ibis_bigquery.Backend,
            ibis.bigquery.connect(
                project_id=context.project,
                client=self.bqclient,
                storage_client=self.bqstoragereadclient,
            ),
        )

        self.bqclient.default_query_job_config = original_default_query_job_config

        # Resolve the BQ connection for remote function and Vertex AI integration
        self._bq_connection = context.bq_connection or _BIGFRAMES_DEFAULT_CONNECTION_ID
        self._skip_bq_connection_check = context._skip_bq_connection_check

        # Now that we're starting the session, don't allow the options to be
        # changed.
        context._session_started = True

        # unique session identifier, short enough to be human readable
        # only needs to be unique among sessions created by the same user
        # at the same time in the same region
        self._session_id: str = "session" + secrets.token_hex(3)
        # store table ids and delete them when the session is closed

        self._objects: list[
            weakref.ReferenceType[
                Union[
                    bigframes.core.indexes.Index,
                    bigframes.series.Series,
                    dataframe.DataFrame,
                ]
            ]
        ] = []
        # Whether this session treats objects as totally ordered.
        # Will expose as feature later, only False for internal testing
        self._strictly_ordered: bool = context.ordering_mode != "partial"
        if not self._strictly_ordered:
            warnings.warn(
                "Partial ordering mode is a preview feature and is subject to change.",
                bigframes.exceptions.OrderingModePartialPreviewWarning,
            )

        self._allow_ambiguity = not self._strictly_ordered
        self._default_index_type = (
            bigframes.enums.DefaultIndexKind.SEQUENTIAL_INT64
            if self._strictly_ordered
            else bigframes.enums.DefaultIndexKind.NULL
        )

        self._metrics = bigframes.session.metrics.ExecutionMetrics()
        self._remote_function_session = bigframes_rf_session.RemoteFunctionSession()
        self._temp_storage_manager = (
            bigframes.session.temp_storage.TemporaryGbqStorageManager(
                self._clients_provider.bqclient,
                location=self._location,
                session_id=self._session_id,
                kms_key=self._bq_kms_key_name,
            )
        )
        self._executor = bigframes.session.executor.BigQueryCachingExecutor(
            bqclient=self._clients_provider.bqclient,
            bqstoragereadclient=self._clients_provider.bqstoragereadclient,
            storage_manager=self._temp_storage_manager,
            strictly_ordered=self._strictly_ordered,
            metrics=self._metrics,
        )
        self._loader = bigframes.session.loader.GbqDataLoader(
            session=self,
            bqclient=self._clients_provider.bqclient,
            storage_manager=self._temp_storage_manager,
            default_index_type=self._default_index_type,
            scan_index_uniqueness=self._strictly_ordered,
            metrics=self._metrics,
        )

    def __del__(self):
        """Automatic cleanup of internal resources"""
        self.close()

    @property
    def bqclient(self):
        return self._clients_provider.bqclient

    @property
    def bqconnectionclient(self):
        return self._clients_provider.bqconnectionclient

    @property
    def bqstoragereadclient(self):
        return self._clients_provider.bqstoragereadclient

    @property
    def cloudfunctionsclient(self):
        return self._clients_provider.cloudfunctionsclient

    @property
    def resourcemanagerclient(self):
        return self._clients_provider.resourcemanagerclient

    _bq_connection_manager: Optional[bigframes.clients.BqConnectionManager] = None

    @property
    def bqconnectionmanager(self):
        if not self._skip_bq_connection_check and not self._bq_connection_manager:
            self._bq_connection_manager = bigframes.clients.BqConnectionManager(
                self.bqconnectionclient, self.resourcemanagerclient
            )
        return self._bq_connection_manager

    @property
    def session_id(self):
        return self._session_id

    @property
    def objects(
        self,
    ) -> Iterable[
        Union[
            bigframes.core.indexes.Index, bigframes.series.Series, dataframe.DataFrame
        ]
    ]:
        still_alive = [i for i in self._objects if i() is not None]
        self._objects = still_alive
        # Create a set with strong references, be careful not to hold onto this needlessly, as will prevent garbage collection.
        return tuple(i() for i in self._objects if i() is not None)  # type: ignore

    @property
    def _project(self):
        return self.bqclient.project

    @property
    def bytes_processed_sum(self):
        """The sum of all bytes processed by bigquery jobs using this session."""
        return self._metrics.bytes_processed

    @property
    def slot_millis_sum(self):
        """The sum of all slot time used by bigquery jobs in this session."""
        return self._metrics.slot_millis

    @property
    def _allows_ambiguity(self) -> bool:
        return self._allow_ambiguity

    @property
    def _anonymous_dataset(self):
        return self._temp_storage_manager.dataset

    def __hash__(self):
        # Stable hash needed to use in expression tree
        return hash(str(self._session_id))

    def close(self):
        """Delete resources that were created with this session's session_id.
        This includes BigQuery tables, remote functions and cloud functions
        serving the remote functions."""
        self._temp_storage_manager.clean_up_tables()
        self._remote_function_session.clean_up(
            self.bqclient, self.cloudfunctionsclient, self.session_id
        )

    def read_gbq(
        self,
        query_or_table: str,
        *,
        index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = (),
        columns: Iterable[str] = (),
        configuration: Optional[Dict] = None,
        max_results: Optional[int] = None,
        filters: third_party_pandas_gbq.FiltersType = (),
        use_cache: Optional[bool] = None,
        col_order: Iterable[str] = (),
        # Add a verify index argument that fails if the index is not unique.
    ) -> dataframe.DataFrame:
        # TODO(b/281571214): Generate prompt to show the progress of read_gbq.
        if columns and col_order:
            raise ValueError(
                "Must specify either columns (preferred) or col_order, not both"
            )
        elif col_order:
            columns = col_order

        if bf_io_bigquery.is_query(query_or_table):
            return self._loader.read_gbq_query(
                query_or_table,
                index_col=index_col,
                columns=columns,
                configuration=configuration,
                max_results=max_results,
                api_name="read_gbq",
                use_cache=use_cache,
                filters=filters,
            )
        else:
            if configuration is not None:
                raise ValueError(
                    "The 'configuration' argument is not allowed when "
                    "directly reading from a table. Please remove "
                    "'configuration' or use a query."
                )

            return self._loader.read_gbq_table(
                query_or_table,
                index_col=index_col,
                columns=columns,
                max_results=max_results,
                api_name="read_gbq",
                use_cache=use_cache if use_cache is not None else True,
                filters=filters,
            )

    def _register_object(
        self,
        object: Union[
            bigframes.core.indexes.Index, bigframes.series.Series, dataframe.DataFrame
        ],
    ):
        self._objects.append(weakref.ref(object))

    def read_gbq_query(
        self,
        query: str,
        *,
        index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = (),
        columns: Iterable[str] = (),
        configuration: Optional[Dict] = None,
        max_results: Optional[int] = None,
        use_cache: Optional[bool] = None,
        col_order: Iterable[str] = (),
        filters: third_party_pandas_gbq.FiltersType = (),
    ) -> dataframe.DataFrame:
        """Turn a SQL query into a DataFrame.

        Note: Because the results are written to a temporary table, ordering by
        ``ORDER BY`` is not preserved. A unique `index_col` is recommended. Use
        ``row_number() over ()`` if there is no natural unique index or you
        want to preserve ordering.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Simple query input:

            >>> df = bpd.read_gbq_query('''
            ...    SELECT
            ...       pitcherFirstName,
            ...       pitcherLastName,
            ...       pitchSpeed,
            ...    FROM `bigquery-public-data.baseball.games_wide`
            ... ''')

        Preserve ordering in a query input.

            >>> df = bpd.read_gbq_query('''
            ...    SELECT
            ...       -- Instead of an ORDER BY clause on the query, use
            ...       -- ROW_NUMBER() to create an ordered DataFrame.
            ...       ROW_NUMBER() OVER (ORDER BY AVG(pitchSpeed) DESC)
            ...         AS rowindex,
            ...
            ...       pitcherFirstName,
            ...       pitcherLastName,
            ...       AVG(pitchSpeed) AS averagePitchSpeed
            ...     FROM `bigquery-public-data.baseball.games_wide`
            ...     WHERE year = 2016
            ...     GROUP BY pitcherFirstName, pitcherLastName
            ... ''', index_col="rowindex")
            >>> df.head(2)
                     pitcherFirstName pitcherLastName  averagePitchSpeed
            rowindex
            1                Albertin         Chapman          96.514113
            2                 Zachary         Britton          94.591039
            <BLANKLINE>
            [2 rows x 3 columns]

        See also: :meth:`Session.read_gbq`.

        Returns:
            bigframes.pandas.DataFrame:
                A DataFrame representing results of the query or table.

        Raises:
            ValueError:
                When both columns (preferred) and col_order are specified.
        """
        # NOTE: This method doesn't (yet) exist in pandas or pandas-gbq, so
        # these docstrings are inline.
        if columns and col_order:
            raise ValueError(
                "Must specify either columns (preferred) or col_order, not both"
            )
        elif col_order:
            columns = col_order

        return self._loader.read_gbq_query(
            query=query,
            index_col=index_col,
            columns=columns,
            configuration=configuration,
            max_results=max_results,
            api_name="read_gbq_query",
            use_cache=use_cache,
            filters=filters,
        )

    def read_gbq_table(
        self,
        query: str,
        *,
        index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = (),
        columns: Iterable[str] = (),
        max_results: Optional[int] = None,
        filters: third_party_pandas_gbq.FiltersType = (),
        use_cache: bool = True,
        col_order: Iterable[str] = (),
    ) -> dataframe.DataFrame:
        """Turn a BigQuery table into a DataFrame.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Read a whole table, with arbitrary ordering or ordering corresponding to the primary key(s).

            >>> df = bpd.read_gbq_table("bigquery-public-data.ml_datasets.penguins")

        See also: :meth:`Session.read_gbq`.

        Returns:
            bigframes.pandas.DataFrame:
                A DataFrame representing results of the query or table.

        Raises:
            ValueError:
                When both columns (preferred) and col_order are specified.
        """
        # NOTE: This method doesn't (yet) exist in pandas or pandas-gbq, so
        # these docstrings are inline.
        if columns and col_order:
            raise ValueError(
                "Must specify either columns (preferred) or col_order, not both"
            )
        elif col_order:
            columns = col_order

        return self._loader.read_gbq_table(
            query=query,
            index_col=index_col,
            columns=columns,
            max_results=max_results,
            api_name="read_gbq_table",
            use_cache=use_cache,
            filters=filters,
        )

    def read_gbq_table_streaming(
        self, table: str
    ) -> streaming_dataframe.StreamingDataFrame:
        """Turn a BigQuery table into a StreamingDataFrame.

        .. note::

            The bigframes.streaming module is a preview feature, and subject to change.

        **Examples:**

            >>> import bigframes.streaming as bst
            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> sdf = bst.read_gbq_table("bigquery-public-data.ml_datasets.penguins")

        Returns:
            bigframes.streaming.dataframe.StreamingDataFrame:
               A StreamingDataFrame representing results of the table.
        """
        warnings.warn(
            "The bigframes.streaming module is a preview feature, and subject to change.",
            stacklevel=1,
            category=bigframes.exceptions.PreviewWarning,
        )

        import bigframes.streaming.dataframe as streaming_dataframe

        df = self._loader.read_gbq_table(
            table,
            api_name="read_gbq_table_steaming",
            enable_snapshot=False,
            index_col=bigframes.enums.DefaultIndexKind.NULL,
        )

        return streaming_dataframe.StreamingDataFrame._from_table_df(df)

    def read_gbq_model(self, model_name: str):
        """Loads a BigQuery ML model from BigQuery.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Read an existing BigQuery ML model.

            >>> model_name = "bigframes-dev.bqml_tutorial.penguins_model"
            >>> model = bpd.read_gbq_model(model_name)

        Args:
            model_name (str):
                the model's name in BigQuery in the format
                `project_id.dataset_id.model_id`, or just `dataset_id.model_id`
                to load from the default project.

        Returns:
            A bigframes.ml Model, Transformer or Pipeline wrapping the model.
        """
        import bigframes.ml.loader

        model_ref = bigquery.ModelReference.from_string(
            model_name, default_project=self.bqclient.project
        )
        model = self.bqclient.get_model(model_ref)
        return bigframes.ml.loader.from_bq(self, model)

    @typing.overload
    def read_pandas(
        self, pandas_dataframe: pandas.Index
    ) -> bigframes.core.indexes.Index:
        ...

    @typing.overload
    def read_pandas(self, pandas_dataframe: pandas.Series) -> bigframes.series.Series:
        ...

    @typing.overload
    def read_pandas(self, pandas_dataframe: pandas.DataFrame) -> dataframe.DataFrame:
        ...

    def read_pandas(
        self, pandas_dataframe: Union[pandas.DataFrame, pandas.Series, pandas.Index]
    ):
        """Loads DataFrame from a pandas DataFrame.

        The pandas DataFrame will be persisted as a temporary BigQuery table, which can be
        automatically recycled after the Session is closed.

        .. note::
            Data is inlined in the query SQL if it is small enough (roughly 5MB
            or less in memory). Larger size data is loaded to a BigQuery table
            instead.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import pandas as pd
            >>> bpd.options.display.progress_bar = None

            >>> d = {'col1': [1, 2], 'col2': [3, 4]}
            >>> pandas_df = pd.DataFrame(data=d)
            >>> df = bpd.read_pandas(pandas_df)
            >>> df
               col1  col2
            0     1     3
            1     2     4
            <BLANKLINE>
            [2 rows x 2 columns]

        Args:
            pandas_dataframe (pandas.DataFrame, pandas.Series, or pandas.Index):
                a pandas DataFrame/Series/Index object to be loaded.

        Returns:
            An equivalent bigframes.pandas.(DataFrame/Series/Index) object

        Raises:
            ValueError:
                When the object is not a Pandas DataFrame.
        """
        import bigframes.series as series

        # Try to handle non-dataframe pandas objects as well
        if isinstance(pandas_dataframe, pandas.Series):
            bf_df = self._read_pandas(pandas.DataFrame(pandas_dataframe), "read_pandas")
            bf_series = series.Series(bf_df._block)
            # wrapping into df can set name to 0 so reset to original object name
            bf_series.name = pandas_dataframe.name
            return bf_series
        if isinstance(pandas_dataframe, pandas.Index):
            return self._read_pandas(
                pandas.DataFrame(index=pandas_dataframe), "read_pandas"
            ).index
        if isinstance(pandas_dataframe, pandas.DataFrame):
            return self._read_pandas(pandas_dataframe, "read_pandas")
        else:
            raise ValueError(
                f"read_pandas() expects a pandas.DataFrame, but got a {type(pandas_dataframe)}"
            )

    def _read_pandas(
        self, pandas_dataframe: pandas.DataFrame, api_name: str
    ) -> dataframe.DataFrame:
        import bigframes.dataframe as dataframe

        if isinstance(pandas_dataframe, dataframe.DataFrame):
            raise ValueError(
                "read_pandas() expects a pandas.DataFrame, but got a "
                "bigframes.pandas.DataFrame."
            )

        inline_df = self._read_pandas_inline(pandas_dataframe)
        if inline_df is not None:
            return inline_df
        try:
            return self._loader.read_pandas_load_job(pandas_dataframe, api_name)
        except pa.ArrowInvalid as e:
            raise pa.ArrowInvalid(
                f"Could not convert with a BigQuery type: `{e}`. "
            ) from e

    def _read_pandas_inline(
        self, pandas_dataframe: pandas.DataFrame
    ) -> Optional[dataframe.DataFrame]:
        import bigframes.dataframe as dataframe

        if pandas_dataframe.memory_usage(deep=True).sum() > MAX_INLINE_DF_BYTES:
            return None

        try:
            local_block = blocks.Block.from_local(pandas_dataframe, self)
            inline_df = dataframe.DataFrame(local_block)
        except pa.ArrowInvalid:  # Thrown by arrow for unsupported types, such as geo.
            return None
        except ValueError:  # Thrown by ibis for some unhandled types
            return None
        except pa.ArrowTypeError:  # Thrown by arrow for types without mapping (geo).
            return None

        inline_types = inline_df._block.expr.schema.dtypes
        # Ibis has problems escaping bytes literals, which will cause syntax errors server-side.
        if all(dtype in INLINABLE_DTYPES for dtype in inline_types):
            return inline_df
        return None

    def read_csv(
        self,
        filepath_or_buffer: str | IO["bytes"],
        *,
        sep: Optional[str] = ",",
        header: Optional[int] = 0,
        names: Optional[
            Union[MutableSequence[Any], np.ndarray[Any, Any], Tuple[Any, ...], range]
        ] = None,
        index_col: Optional[
            Union[
                int,
                str,
                Sequence[Union[str, int]],
                bigframes.enums.DefaultIndexKind,
                Literal[False],
            ]
        ] = None,
        usecols: Optional[
            Union[
                MutableSequence[str],
                Tuple[str, ...],
                Sequence[int],
                pandas.Series,
                pandas.Index,
                np.ndarray[Any, Any],
                Callable[[Any], bool],
            ]
        ] = None,
        dtype: Optional[Dict] = None,
        engine: Optional[
            Literal["c", "python", "pyarrow", "python-fwf", "bigquery"]
        ] = None,
        encoding: Optional[str] = None,
        **kwargs,
    ) -> dataframe.DataFrame:
        table = self._temp_storage_manager._random_table()

        if engine is not None and engine == "bigquery":
            if any(param is not None for param in (dtype, names)):
                not_supported = ("dtype", "names")
                raise NotImplementedError(
                    f"BigQuery engine does not support these arguments: {not_supported}. "
                    f"{constants.FEEDBACK_LINK}"
                )

            # TODO(b/338089659): Looks like we can relax this 1 column
            # restriction if we check the contents of an iterable are strings
            # not integers.
            if (
                # Empty tuples, None, and False are allowed and falsey.
                index_col
                and not isinstance(index_col, bigframes.enums.DefaultIndexKind)
                and not isinstance(index_col, str)
            ):
                raise NotImplementedError(
                    "BigQuery engine only supports a single column name for `index_col`, "
                    f"got: {repr(index_col)}. {constants.FEEDBACK_LINK}"
                )

            # None and False cannot be passed to read_gbq.
            # TODO(b/338400133): When index_col is None, we should be using the
            # first column of the CSV as the index to be compatible with the
            # pandas engine. According to the pandas docs, only "False"
            # indicates a default sequential index.
            if not index_col:
                index_col = ()

            index_col = typing.cast(
                Union[
                    Sequence[str],  # Falsey values
                    bigframes.enums.DefaultIndexKind,
                    str,
                ],
                index_col,
            )

            # usecols should only be an iterable of strings (column names) for use as columns in read_gbq.
            columns: Tuple[Any, ...] = tuple()
            if usecols is not None:
                if isinstance(usecols, Iterable) and all(
                    isinstance(col, str) for col in usecols
                ):
                    columns = tuple(col for col in usecols)
                else:
                    raise NotImplementedError(
                        "BigQuery engine only supports an iterable of strings for `usecols`. "
                        f"{constants.FEEDBACK_LINK}"
                    )

            if encoding is not None and encoding not in _VALID_ENCODINGS:
                raise NotImplementedError(
                    f"BigQuery engine only supports the following encodings: {_VALID_ENCODINGS}. "
                    f"{constants.FEEDBACK_LINK}"
                )

            job_config = bigquery.LoadJobConfig()
            job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED
            job_config.source_format = bigquery.SourceFormat.CSV
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_EMPTY
            job_config.autodetect = True
            job_config.field_delimiter = sep
            job_config.encoding = encoding
            job_config.labels = {"bigframes-api": "read_csv"}

            # We want to match pandas behavior. If header is 0, no rows should be skipped, so we
            # do not need to set `skip_leading_rows`. If header is None, then there is no header.
            # Setting skip_leading_rows to 0 does that. If header=N and N>0, we want to skip N rows.
            if header is None:
                job_config.skip_leading_rows = 0
            elif header > 0:
                job_config.skip_leading_rows = header

            return self._loader._read_bigquery_load_job(
                filepath_or_buffer,
                table,
                job_config=job_config,
                index_col=index_col,
                columns=columns,
            )
        else:
            if isinstance(index_col, bigframes.enums.DefaultIndexKind):
                raise NotImplementedError(
                    f"With index_col={repr(index_col)}, only engine='bigquery' is supported. "
                    f"{constants.FEEDBACK_LINK}"
                )
            if any(arg in kwargs for arg in ("chunksize", "iterator")):
                raise NotImplementedError(
                    "'chunksize' and 'iterator' arguments are not supported. "
                    f"{constants.FEEDBACK_LINK}"
                )

            if isinstance(filepath_or_buffer, str):
                self._check_file_size(filepath_or_buffer)
            pandas_df = pandas.read_csv(
                filepath_or_buffer,
                sep=sep,
                header=header,
                names=names,
                index_col=index_col,
                usecols=usecols,  # type: ignore
                dtype=dtype,
                engine=engine,
                encoding=encoding,
                **kwargs,
            )
            return self._read_pandas(pandas_df, "read_csv")  # type: ignore

    def read_pickle(
        self,
        filepath_or_buffer: FilePath | ReadPickleBuffer,
        compression: CompressionOptions = "infer",
        storage_options: StorageOptions = None,
    ):
        pandas_obj = pandas.read_pickle(
            filepath_or_buffer,
            compression=compression,
            storage_options=storage_options,
        )

        if isinstance(pandas_obj, pandas.Series):
            if pandas_obj.name is None:
                pandas_obj.name = "0"
            bigframes_df = self._read_pandas(pandas_obj.to_frame(), "read_pickle")
            return bigframes_df[bigframes_df.columns[0]]
        return self._read_pandas(pandas_obj, "read_pickle")

    def read_parquet(
        self,
        path: str | IO["bytes"],
        *,
        engine: str = "auto",
    ) -> dataframe.DataFrame:
        table = self._temp_storage_manager._random_table()

        if engine == "bigquery":
            job_config = bigquery.LoadJobConfig()
            job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED
            job_config.source_format = bigquery.SourceFormat.PARQUET
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_EMPTY
            job_config.labels = {"bigframes-api": "read_parquet"}

            return self._loader._read_bigquery_load_job(
                path, table, job_config=job_config
            )
        else:
            read_parquet_kwargs: Dict[str, Any] = {}
            if pandas.__version__.startswith("1."):
                read_parquet_kwargs["use_nullable_dtypes"] = True
            else:
                read_parquet_kwargs["dtype_backend"] = "pyarrow"

            pandas_obj = pandas.read_parquet(
                path,
                engine=engine,  # type: ignore
                **read_parquet_kwargs,
            )
            return self._read_pandas(pandas_obj, "read_parquet")

    def read_json(
        self,
        path_or_buf: str | IO["bytes"],
        *,
        orient: Literal[
            "split", "records", "index", "columns", "values", "table"
        ] = "columns",
        dtype: Optional[Dict] = None,
        encoding: Optional[str] = None,
        lines: bool = False,
        engine: Literal["ujson", "pyarrow", "bigquery"] = "ujson",
        **kwargs,
    ) -> dataframe.DataFrame:
        table = self._temp_storage_manager._random_table()

        if engine == "bigquery":

            if dtype is not None:
                raise NotImplementedError(
                    "BigQuery engine does not support the dtype arguments."
                )

            if not lines:
                raise NotImplementedError(
                    "Only newline delimited JSON format is supported."
                )

            if encoding is not None and encoding not in _VALID_ENCODINGS:
                raise NotImplementedError(
                    f"BigQuery engine only supports the following encodings: {_VALID_ENCODINGS}"
                )

            if lines and orient != "records":
                raise ValueError(
                    "'lines' keyword is only valid when 'orient' is 'records'."
                )

            job_config = bigquery.LoadJobConfig()
            job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED
            job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_EMPTY
            job_config.autodetect = True
            job_config.encoding = encoding
            job_config.labels = {"bigframes-api": "read_json"}

            return self._loader._read_bigquery_load_job(
                path_or_buf,
                table,
                job_config=job_config,
            )
        else:
            if any(arg in kwargs for arg in ("chunksize", "iterator")):
                raise NotImplementedError(
                    "'chunksize' and 'iterator' arguments are not supported."
                )

            if isinstance(path_or_buf, str):
                self._check_file_size(path_or_buf)

            if engine == "ujson":
                pandas_df = pandas.read_json(  # type: ignore
                    path_or_buf,
                    orient=orient,
                    dtype=dtype,
                    encoding=encoding,
                    lines=lines,
                    **kwargs,
                )

            else:
                pandas_df = pandas.read_json(  # type: ignore
                    path_or_buf,
                    orient=orient,
                    dtype=dtype,
                    encoding=encoding,
                    lines=lines,
                    engine=engine,
                    **kwargs,
                )
            return self._read_pandas(pandas_df, "read_json")

    def _check_file_size(self, filepath: str):
        max_size = 1024 * 1024 * 1024  # 1 GB in bytes
        if filepath.startswith("gs://"):  # GCS file path
            client = storage.Client()
            bucket_name, blob_name = filepath.split("/", 3)[2:]
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.reload()
            file_size = blob.size
        elif os.path.exists(filepath):  # local file path
            file_size = os.path.getsize(filepath)
        else:
            file_size = None

        if file_size is not None and file_size > max_size:
            # Convert to GB
            file_size = round(file_size / (1024**3), 1)
            max_size = int(max_size / 1024**3)
            logger.warning(
                f"File size {file_size}GB exceeds {max_size}GB. "
                "It is recommended to use engine='bigquery' "
                "for large files to avoid loading the file into local memory."
            )

    def remote_function(
        self,
        input_types: Union[None, type, Sequence[type]] = None,
        output_type: Optional[type] = None,
        dataset: Optional[str] = None,
        bigquery_connection: Optional[str] = None,
        reuse: bool = True,
        name: Optional[str] = None,
        packages: Optional[Sequence[str]] = None,
        cloud_function_service_account: Optional[str] = None,
        cloud_function_kms_key_name: Optional[str] = None,
        cloud_function_docker_repository: Optional[str] = None,
        max_batching_rows: Optional[int] = 1000,
        cloud_function_timeout: Optional[int] = 600,
        cloud_function_max_instances: Optional[int] = None,
        cloud_function_vpc_connector: Optional[str] = None,
        cloud_function_memory_mib: Optional[int] = 1024,
        cloud_function_ingress_settings: Literal[
            "all", "internal-only", "internal-and-gclb"
        ] = "all",
    ):
        """Decorator to turn a user defined function into a BigQuery remote function. Check out
        the code samples at: https://cloud.google.com/bigquery/docs/remote-functions#bigquery-dataframes.

        .. note::
            ``input_types=Series`` scenario is in preview. It currently only
            supports dataframe with column types ``Int64``/``Float64``/``boolean``/
            ``string``/``binary[pyarrow]``.

        .. note::
            Please make sure following is setup before using this API:

        1. Have the below APIs enabled for your project:

            * BigQuery Connection API
            * Cloud Functions API
            * Cloud Run API
            * Cloud Build API
            * Artifact Registry API
            * Cloud Resource Manager API

           This can be done from the cloud console (change `PROJECT_ID` to yours):
           https://console.cloud.google.com/apis/enableflow?apiid=bigqueryconnection.googleapis.com,cloudfunctions.googleapis.com,run.googleapis.com,cloudbuild.googleapis.com,artifactregistry.googleapis.com,cloudresourcemanager.googleapis.com&project=PROJECT_ID

           Or from the gcloud CLI:

           `$ gcloud services enable bigqueryconnection.googleapis.com cloudfunctions.googleapis.com run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com cloudresourcemanager.googleapis.com`

        2. Have following IAM roles enabled for you:

            * BigQuery Data Editor (roles/bigquery.dataEditor)
            * BigQuery Connection Admin (roles/bigquery.connectionAdmin)
            * Cloud Functions Developer (roles/cloudfunctions.developer)
            * Service Account User (roles/iam.serviceAccountUser) on the service account `PROJECT_NUMBER-compute@developer.gserviceaccount.com`
            * Storage Object Viewer (roles/storage.objectViewer)
            * Project IAM Admin (roles/resourcemanager.projectIamAdmin) (Only required if the bigquery connection being used is not pre-created and is created dynamically with user credentials.)

        3. Either the user has setIamPolicy privilege on the project, or a BigQuery connection is pre-created with necessary IAM role set:

            1. To create a connection, follow https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#create_a_connection
            2. To set up IAM, follow https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#grant_permission_on_function

               Alternatively, the IAM could also be setup via the gcloud CLI:

               `$ gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:CONNECTION_SERVICE_ACCOUNT_ID" --role="roles/run.invoker"`.

        Args:
            input_types (type or sequence(type)):
                For scalar user defined function it should be the input type or
                sequence of input types. For row processing user defined function,
                type `Series` should be specified.
            output_type (type):
                Data type of the output in the user defined function.
            dataset (str, Optional):
                Dataset in which to create a BigQuery remote function. It should be in
                `<project_id>.<dataset_name>` or `<dataset_name>` format. If this
                parameter is not provided then session dataset id is used.
            bigquery_connection (str, Optional):
                Name of the BigQuery connection. You should either have the
                connection already created in the `location` you have chosen, or
                you should have the Project IAM Admin role to enable the service
                to create the connection for you if you need it. If this parameter is
                not provided then the BigQuery connection from the session is used.
            reuse (bool, Optional):
                Reuse the remote function if already exists.
                `True` by default, which will result in reusing an existing remote
                function and corresponding cloud function that was previously
                created (if any) for the same udf.
                Please note that for an unnamed (i.e. created without an explicit
                `name` argument) remote function, the BigQuery DataFrames
                session id is attached in the cloud artifacts names. So for the
                effective reuse across the sessions it is recommended to create
                the remote function with an explicit `name`.
                Setting it to `False` would force creating a unique remote function.
                If the required remote function does not exist then it would be
                created irrespective of this param.
            name (str, Optional):
                Explicit name of the persisted BigQuery remote function. Use it
                with caution, because more than one users working in the same
                project and dataset could overwrite each other's remote
                functions if they use the same persistent name. When an explicit
                name is provided, any session specific clean up (
                ``bigframes.session.Session.close``/
                ``bigframes.pandas.close_session``/
                ``bigframes.pandas.reset_session``/
                ``bigframes.pandas.clean_up_by_session_id``) does not clean up
                the function, and leaves it for the user to manage the function
                and the associated cloud function directly.
            packages (str[], Optional):
                Explicit name of the external package dependencies. Each dependency
                is added to the `requirements.txt` as is, and can be of the form
                supported in https://pip.pypa.io/en/stable/reference/requirements-file-format/.
            cloud_function_service_account (str, Optional):
                Service account to use for the cloud functions. If not provided
                then the default service account would be used. See
                https://cloud.google.com/functions/docs/securing/function-identity
                for more details. Please make sure the service account has the
                necessary IAM permissions configured as described in
                https://cloud.google.com/functions/docs/reference/iam/roles#additional-configuration.
            cloud_function_kms_key_name (str, Optional):
                Customer managed encryption key to protect cloud functions and
                related data at rest. This is of the format
                projects/PROJECT_ID/locations/LOCATION/keyRings/KEYRING/cryptoKeys/KEY.
                Read https://cloud.google.com/functions/docs/securing/cmek for
                more details including granting necessary service accounts
                access to the key.
            cloud_function_docker_repository (str, Optional):
                Docker repository created with the same encryption key as
                `cloud_function_kms_key_name` to store encrypted artifacts
                created to support the cloud function. This is of the format
                projects/PROJECT_ID/locations/LOCATION/repositories/REPOSITORY_NAME.
                For more details see
                https://cloud.google.com/functions/docs/securing/cmek#before_you_begin.
            max_batching_rows (int, Optional):
                The maximum number of rows to be batched for processing in the
                BQ remote function. Default value is 1000. A lower number can be
                passed to avoid timeouts in case the user code is too complex to
                process large number of rows fast enough. A higher number can be
                used to increase throughput in case the user code is fast enough.
                `None` can be passed to let BQ remote functions service apply
                default batching. See for more details
                https://cloud.google.com/bigquery/docs/remote-functions#limiting_number_of_rows_in_a_batch_request.
            cloud_function_timeout (int, Optional):
                The maximum amount of time (in seconds) BigQuery should wait for
                the cloud function to return a response. See for more details
                https://cloud.google.com/functions/docs/configuring/timeout.
                Please note that even though the cloud function (2nd gen) itself
                allows seeting up to 60 minutes of timeout, BigQuery remote
                function can wait only up to 20 minutes, see for more details
                https://cloud.google.com/bigquery/quotas#remote_function_limits.
                By default BigQuery DataFrames uses a 10 minute timeout. `None`
                can be passed to let the cloud functions default timeout take effect.
            cloud_function_max_instances (int, Optional):
                The maximumm instance count for the cloud function created. This
                can be used to control how many cloud function instances can be
                active at max at any given point of time. Lower setting can help
                control the spike in the billing. Higher setting can help
                support processing larger scale data. When not specified, cloud
                function's default setting applies. For more details see
                https://cloud.google.com/functions/docs/configuring/max-instances.
            cloud_function_vpc_connector (str, Optional):
                The VPC connector you would like to configure for your cloud
                function. This is useful if your code needs access to data or
                service(s) that are on a VPC network. See for more details
                https://cloud.google.com/functions/docs/networking/connecting-vpc.
            cloud_function_memory_mib (int, Optional):
                The amounts of memory (in mebibytes) to allocate for the cloud
                function (2nd gen) created. This also dictates a corresponding
                amount of allocated CPU for the function. By default a memory of
                1024 MiB is set for the cloud functions created to support
                BigQuery DataFrames remote function. If you want to let the
                default memory of cloud functions be allocated, pass `None`. See
                for more details
                https://cloud.google.com/functions/docs/configuring/memory.
            cloud_function_ingress_settings (str, Optional):
                Ingress settings controls dictating what traffic can reach the
                function. By default `all` will be used. It must be one of:
                `all`, `internal-only`, `internal-and-gclb`. See for more details
                https://cloud.google.com/functions/docs/networking/network-settings#ingress_settings.
        Returns:
            callable: A remote function object pointing to the cloud assets created
            in the background to support the remote execution. The cloud assets can be
            located through the following properties set in the object:

            `bigframes_cloud_function` - The google cloud function deployed for the user defined code.

            `bigframes_remote_function` - The bigquery remote function capable of calling into `bigframes_cloud_function`.
        """
        return self._remote_function_session.remote_function(
            input_types,
            output_type,
            session=self,
            dataset=dataset,
            bigquery_connection=bigquery_connection,
            reuse=reuse,
            name=name,
            packages=packages,
            cloud_function_service_account=cloud_function_service_account,
            cloud_function_kms_key_name=cloud_function_kms_key_name,
            cloud_function_docker_repository=cloud_function_docker_repository,
            max_batching_rows=max_batching_rows,
            cloud_function_timeout=cloud_function_timeout,
            cloud_function_max_instances=cloud_function_max_instances,
            cloud_function_vpc_connector=cloud_function_vpc_connector,
            cloud_function_memory_mib=cloud_function_memory_mib,
            cloud_function_ingress_settings=cloud_function_ingress_settings,
        )

    def read_gbq_function(
        self,
        function_name: str,
        is_row_processor: bool = False,
    ):
        """Loads a BigQuery function from BigQuery.

        Then it can be applied to a DataFrame or Series.

        .. note::
            The return type of the function must be explicitly specified in the
            function's original definition even if not otherwise required.

        BigQuery Utils provides many public functions under the ``bqutil`` project on Google Cloud Platform project
        (See: https://github.com/GoogleCloudPlatform/bigquery-utils/tree/master/udfs#using-the-udfs).
        You can checkout Community UDFs to use community-contributed functions.
        (See: https://github.com/GoogleCloudPlatform/bigquery-utils/tree/master/udfs/community#community-udfs).

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Use the [cw_lower_case_ascii_only](https://github.com/GoogleCloudPlatform/bigquery-utils/blob/master/udfs/community/README.md#cw_lower_case_ascii_onlystr-string)
        function from Community UDFs.

            >>> func = bpd.read_gbq_function("bqutil.fn.cw_lower_case_ascii_only")

        You can run it on scalar input. Usually you would do so to verify that
        it works as expected before applying to all values in a Series.

            >>> func('AURÉLIE')
            'aurÉlie'

        You can apply it to a BigQuery DataFrames Series.

            >>> df = bpd.DataFrame({'id': [1, 2, 3], 'name': ['AURÉLIE', 'CÉLESTINE', 'DAPHNÉ']})
            >>> df
               id       name
            0   1    AURÉLIE
            1   2  CÉLESTINE
            2   3     DAPHNÉ
            <BLANKLINE>
            [3 rows x 2 columns]

            >>> df1 = df.assign(new_name=df['name'].apply(func))
            >>> df1
               id       name   new_name
            0   1    AURÉLIE    aurÉlie
            1   2  CÉLESTINE  cÉlestine
            2   3     DAPHNÉ     daphnÉ
            <BLANKLINE>
            [3 rows x 3 columns]

        You can even use a function with multiple inputs. For example,
        [cw_regexp_replace_5](https://github.com/GoogleCloudPlatform/bigquery-utils/blob/master/udfs/community/README.md#cw_regexp_replace_5haystack-string-regexp-string-replacement-string-offset-int64-occurrence-int64)
        from Community UDFs.

            >>> func = bpd.read_gbq_function("bqutil.fn.cw_regexp_replace_5")
            >>> func('TestStr123456', 'Str', 'Cad$', 1, 1)
            'TestCad$123456'

            >>> df = bpd.DataFrame({
            ...     "haystack" : ["TestStr123456", "TestStr123456Str", "TestStr123456Str"],
            ...     "regexp" : ["Str", "Str", "Str"],
            ...     "replacement" : ["Cad$", "Cad$", "Cad$"],
            ...     "offset" : [1, 1, 1],
            ...     "occurrence" : [1, 2, 1]
            ... })
            >>> df
                       haystack regexp replacement  offset  occurrence
            0     TestStr123456    Str        Cad$       1           1
            1  TestStr123456Str    Str        Cad$       1           2
            2  TestStr123456Str    Str        Cad$       1           1
            <BLANKLINE>
            [3 rows x 5 columns]
            >>> df.apply(func, axis=1)
            0       TestCad$123456
            1    TestStr123456Cad$
            2    TestCad$123456Str
            dtype: string

        Args:
            function_name (str):
                The function's name in BigQuery in the format
                `project_id.dataset_id.function_name`, or
                `dataset_id.function_name` to load from the default project, or
                `function_name` to load from the default project and the dataset
                associated with the current session.
            is_row_processor (bool, default False):
                Whether the function is a row processor. This is set to True
                for a function which receives an entire row of a DataFrame as
                a pandas Series.

        Returns:
            callable: A function object pointing to the BigQuery function read
            from BigQuery.

            The object is similar to the one created by the `remote_function`
            decorator, including the `bigframes_remote_function` property, but
            not including the `bigframes_cloud_function` property.
        """

        return bigframes_rf.read_gbq_function(
            function_name=function_name,
            session=self,
            is_row_processor=is_row_processor,
        )

    def _prepare_copy_job_config(self) -> bigquery.CopyJobConfig:
        # Create a copy so that we don't mutate the original config passed
        job_config = bigquery.CopyJobConfig()

        if self._bq_kms_key_name:
            job_config.destination_encryption_configuration = (
                bigquery.EncryptionConfiguration(kms_key_name=self._bq_kms_key_name)
            )

        return job_config

    def _start_query_ml_ddl(
        self,
        sql: str,
    ) -> Tuple[bigquery.table.RowIterator, bigquery.QueryJob]:
        """
        Starts BigQuery ML DDL query job (CREATE MODEL/ALTER MODEL/...) and
        waits for results.
        """
        job_config = typing.cast(bigquery.QueryJobConfig, bigquery.QueryJobConfig())
        if bigframes.options.compute.maximum_bytes_billed is not None:
            job_config.maximum_bytes_billed = (
                bigframes.options.compute.maximum_bytes_billed
            )

        # BQML expects kms_key_name through OPTIONS and not through job config,
        # so we must reset any encryption set in the job config
        # https://cloud.google.com/bigquery/docs/customer-managed-encryption#encrypt-model
        job_config.destination_encryption_configuration = None

        return bf_io_bigquery.start_query_with_client(
            self.bqclient, sql, job_config, metrics=self._metrics
        )

    def _export(
        self,
        array_value: core.ArrayValue,
        destination: bigquery.TableReference,
        *,
        if_exists: Literal["fail", "replace", "append"] = "fail",
        col_id_overrides: Mapping[str, str] = {},
        cluster_cols: Sequence[str],
    ) -> tuple[bigquery.table.RowIterator, bigquery.QueryJob]:
        # Note: cluster_cols use pre-override column ids
        return self._executor.export_gbq(
            array_value,
            destination=destination,
            col_id_overrides=col_id_overrides,
            if_exists=if_exists,
            cluster_cols=cluster_cols,
        )


def connect(context: Optional[bigquery_options.BigQueryOptions] = None) -> Session:
    return Session(context)
