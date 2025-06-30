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

from collections import abc
import datetime
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
    MutableSequence,
    Optional,
    overload,
    Sequence,
    Tuple,
    Union,
)
import warnings
import weakref

import bigframes_vendored.constants as constants
import bigframes_vendored.ibis.backends.bigquery as ibis_bigquery  # noqa
import bigframes_vendored.pandas.io.gbq as third_party_pandas_gbq
import bigframes_vendored.pandas.io.parquet as third_party_pandas_parquet
import bigframes_vendored.pandas.io.parsers.readers as third_party_pandas_readers
import bigframes_vendored.pandas.io.pickle as third_party_pandas_pickle
import google.cloud.bigquery as bigquery
import google.cloud.storage as storage  # type: ignore
import numpy as np
import pandas
from pandas._typing import (
    CompressionOptions,
    FilePath,
    ReadPickleBuffer,
    StorageOptions,
)
import pyarrow as pa

from bigframes import exceptions as bfe
from bigframes import version
import bigframes._config.bigquery_options as bigquery_options
import bigframes.clients
import bigframes.constants
import bigframes.core
from bigframes.core import blocks, log_adapter, utils
import bigframes.core.pyformat

# Even though the ibis.backends.bigquery import is unused, it's needed
# to register new and replacement ops with the Ibis BigQuery backend.
import bigframes.functions._function_session as bff_session
import bigframes.functions.function as bff
from bigframes.session import bigquery_session, bq_caching_executor, executor
import bigframes.session._io.bigquery as bf_io_bigquery
import bigframes.session.anonymous_dataset
import bigframes.session.clients
import bigframes.session.loader
import bigframes.session.metrics
import bigframes.session.validation

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


@log_adapter.class_logger
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
        _warn_if_bf_version_is_obsolete()

        if context is None:
            context = bigquery_options.BigQueryOptions()

        if context.location is None:
            self._location = "US"
            msg = bfe.format_message(
                f"No explicit location is set, so using location {self._location} for the session."
            )
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
            warnings.warn(msg, stacklevel=4, category=bfe.DefaultLocationWarning)
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
                client_endpoints_override=context.client_endpoints_override,
                requests_transport_adapters=context.requests_transport_adapters,
            )

        # TODO(shobs): Remove this logic after https://github.com/ibis-project/ibis/issues/8494
        # has been fixed. The ibis client changes the default query job config
        # so we are going to remember the current config and restore it after
        # the ibis client has been created
        original_default_query_job_config = self.bqclient.default_query_job_config

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
        self._allow_ambiguity = not self._strictly_ordered
        self._default_index_type = (
            bigframes.enums.DefaultIndexKind.SEQUENTIAL_INT64
            if self._strictly_ordered
            else bigframes.enums.DefaultIndexKind.NULL
        )

        self._metrics = bigframes.session.metrics.ExecutionMetrics()
        self._function_session = bff_session.FunctionSession()
        self._anon_dataset_manager = (
            bigframes.session.anonymous_dataset.AnonymousDatasetManager(
                self._clients_provider.bqclient,
                location=self._location,
                session_id=self._session_id,
                kms_key=self._bq_kms_key_name,
            )
        )
        # Session temp tables don't support specifying kms key, so use anon dataset if kms key specified
        self._session_resource_manager = (
            bigquery_session.SessionResourceManager(
                self.bqclient,
                self._location,
            )
            if (self._bq_kms_key_name is None)
            else None
        )
        self._temp_storage_manager = (
            self._session_resource_manager or self._anon_dataset_manager
        )
        self._loader = bigframes.session.loader.GbqDataLoader(
            session=self,
            bqclient=self._clients_provider.bqclient,
            storage_manager=self._temp_storage_manager,
            write_client=self._clients_provider.bqstoragewriteclient,
            default_index_type=self._default_index_type,
            scan_index_uniqueness=self._strictly_ordered,
            force_total_order=self._strictly_ordered,
            metrics=self._metrics,
        )
        self._executor: executor.Executor = bq_caching_executor.BigQueryCachingExecutor(
            bqclient=self._clients_provider.bqclient,
            bqstoragereadclient=self._clients_provider.bqstoragereadclient,
            loader=self._loader,
            storage_manager=self._temp_storage_manager,
            strictly_ordered=self._strictly_ordered,
            metrics=self._metrics,
            enable_polars_execution=context.enable_polars_execution,
        )

    def __del__(self):
        """Automatic cleanup of internal resources."""
        self.close()

    def __enter__(self):
        """Enter the runtime context of the Session object.

        See [With Statement Context Managers](https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers)
        for more details.
        """
        return self

    def __exit__(self, *_):
        """Exit the runtime context of the Session object.

        See [With Statement Context Managers](https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers)
        for more details.
        """
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
        msg = bfe.format_message(
            "Queries executed with `allow_large_results=False` within the session will not "
            "have their slot milliseconds counted in this sum.  If you need precise slot "
            "milliseconds information, query the `INFORMATION_SCHEMA` tables "
            "to get relevant metrics.",
        )
        warnings.warn(msg, UserWarning)
        return self._metrics.slot_millis

    @property
    def _allows_ambiguity(self) -> bool:
        return self._allow_ambiguity

    @property
    def _anonymous_dataset(self):
        return self._anon_dataset_manager.dataset

    def __hash__(self):
        # Stable hash needed to use in expression tree
        return hash(str(self._session_id))

    def close(self):
        """Delete resources that were created with this session's session_id.
        This includes BigQuery tables, remote functions and cloud functions
        serving the remote functions."""

        # Protect against failure when the Session is a fake for testing or
        # failed to initialize.
        if anon_dataset_manager := getattr(self, "_anon_dataset_manager", None):
            anon_dataset_manager.close()

        if session_resource_manager := getattr(self, "_session_resource_manager", None):
            session_resource_manager.close()

        remote_function_session = getattr(self, "_function_session", None)
        if remote_function_session:
            self._function_session.clean_up(
                self.bqclient, self.cloudfunctionsclient, self.session_id
            )

    @overload
    def read_gbq(  # type: ignore[overload-overlap]
        self,
        query_or_table: str,
        *,
        index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = ...,
        columns: Iterable[str] = ...,
        configuration: Optional[Dict] = ...,
        max_results: Optional[int] = ...,
        filters: third_party_pandas_gbq.FiltersType = ...,
        use_cache: Optional[bool] = ...,
        col_order: Iterable[str] = ...,
        dry_run: Literal[False] = ...,
    ) -> dataframe.DataFrame:
        ...

    @overload
    def read_gbq(
        self,
        query_or_table: str,
        *,
        index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = ...,
        columns: Iterable[str] = ...,
        configuration: Optional[Dict] = ...,
        max_results: Optional[int] = ...,
        filters: third_party_pandas_gbq.FiltersType = ...,
        use_cache: Optional[bool] = ...,
        col_order: Iterable[str] = ...,
        dry_run: Literal[True] = ...,
    ) -> pandas.Series:
        ...

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
        dry_run: bool = False
        # Add a verify index argument that fails if the index is not unique.
    ) -> dataframe.DataFrame | pandas.Series:
        # TODO(b/281571214): Generate prompt to show the progress of read_gbq.
        if columns and col_order:
            raise ValueError(
                "Must specify either columns (preferred) or col_order, not both"
            )
        elif col_order:
            columns = col_order

        if bf_io_bigquery.is_query(query_or_table):
            return self._loader.read_gbq_query(  # type: ignore # for dry_run overload
                query_or_table,
                index_col=index_col,
                columns=columns,
                configuration=configuration,
                max_results=max_results,
                use_cache=use_cache,
                filters=filters,
                dry_run=dry_run,
            )
        else:
            if configuration is not None:
                raise ValueError(
                    "The 'configuration' argument is not allowed when "
                    "directly reading from a table. Please remove "
                    "'configuration' or use a query."
                )

            return self._loader.read_gbq_table(  # type: ignore # for dry_run overload
                query_or_table,
                index_col=index_col,
                columns=columns,
                max_results=max_results,
                use_cache=use_cache if use_cache is not None else True,
                filters=filters,
                dry_run=dry_run,
            )

    def _register_object(
        self,
        object: Union[
            bigframes.core.indexes.Index, bigframes.series.Series, dataframe.DataFrame
        ],
    ):
        self._objects.append(weakref.ref(object))

    @overload
    def _read_gbq_colab(
        self,
        query: str,
        *,
        pyformat_args: Optional[Dict[str, Any]] = None,
        dry_run: Literal[False] = ...,
    ) -> dataframe.DataFrame:
        ...

    @overload
    def _read_gbq_colab(
        self,
        query: str,
        *,
        pyformat_args: Optional[Dict[str, Any]] = None,
        dry_run: Literal[True] = ...,
    ) -> pandas.Series:
        ...

    @log_adapter.log_name_override("read_gbq_colab")
    def _read_gbq_colab(
        self,
        query: str,
        # TODO: Add a callback parameter that takes some kind of Event object.
        *,
        pyformat_args: Optional[Dict[str, Any]] = None,
        dry_run: bool = False,
    ) -> Union[dataframe.DataFrame, pandas.Series]:
        """A version of read_gbq that has the necessary default values for use in colab integrations.

        This includes, no ordering, no index, no progress bar, always use string
        formatting for embedding local variables / dataframes.

        Args:
            query (str):
                A SQL query string to execute. Results (if any) are turned into
                a DataFrame.
            pyformat_args (dict):
                A dictionary of potential variables to replace in ``query``.
                Note: strings are _not_ escaped. Use query parameters for these,
                instead. Note: unlike read_gbq / read_gbq_query, even if set to
                None, this function always assumes {var} refers to a variable
                that is supposed to be supplied in this dictionary.
        """
        if pyformat_args is None:
            pyformat_args = {}

        query = bigframes.core.pyformat.pyformat(
            query,
            pyformat_args=pyformat_args,
            session=self,
            dry_run=dry_run,
        )

        return self._loader.read_gbq_query(
            query=query,
            index_col=bigframes.enums.DefaultIndexKind.NULL,
            force_total_order=False,
            dry_run=typing.cast(Union[Literal[False], Literal[True]], dry_run),
            # TODO(tswast): we may need to allow allow_large_results to be overwritten
            # or possibly a general configuration object for an explicit
            # destination table and write disposition.
            allow_large_results=False,
        )

    @overload
    def read_gbq_query(  # type: ignore[overload-overlap]
        self,
        query: str,
        *,
        index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = ...,
        columns: Iterable[str] = ...,
        configuration: Optional[Dict] = ...,
        max_results: Optional[int] = ...,
        use_cache: Optional[bool] = ...,
        col_order: Iterable[str] = ...,
        filters: third_party_pandas_gbq.FiltersType = ...,
        dry_run: Literal[False] = ...,
    ) -> dataframe.DataFrame:
        ...

    @overload
    def read_gbq_query(
        self,
        query: str,
        *,
        index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = ...,
        columns: Iterable[str] = ...,
        configuration: Optional[Dict] = ...,
        max_results: Optional[int] = ...,
        use_cache: Optional[bool] = ...,
        col_order: Iterable[str] = ...,
        filters: third_party_pandas_gbq.FiltersType = ...,
        dry_run: Literal[True] = ...,
    ) -> pandas.Series:
        ...

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
        dry_run: bool = False,
    ) -> dataframe.DataFrame | pandas.Series:
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
                When both ``columns`` and ``col_order`` are specified.
        """
        # NOTE: This method doesn't (yet) exist in pandas or pandas-gbq, so
        # these docstrings are inline.
        if columns and col_order:
            raise ValueError(
                "Must specify either columns (preferred) or col_order, not both"
            )
        elif col_order:
            columns = col_order

        return self._loader.read_gbq_query(  # type: ignore # for dry_run overload
            query=query,
            index_col=index_col,
            columns=columns,
            configuration=configuration,
            max_results=max_results,
            use_cache=use_cache,
            filters=filters,
            dry_run=dry_run,
        )

    @overload
    def read_gbq_table(  # type: ignore[overload-overlap]
        self,
        query: str,
        *,
        index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = ...,
        columns: Iterable[str] = ...,
        max_results: Optional[int] = ...,
        filters: third_party_pandas_gbq.FiltersType = ...,
        use_cache: bool = ...,
        col_order: Iterable[str] = ...,
        dry_run: Literal[False] = ...,
    ) -> dataframe.DataFrame:
        ...

    @overload
    def read_gbq_table(
        self,
        query: str,
        *,
        index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = ...,
        columns: Iterable[str] = ...,
        max_results: Optional[int] = ...,
        filters: third_party_pandas_gbq.FiltersType = ...,
        use_cache: bool = ...,
        col_order: Iterable[str] = ...,
        dry_run: Literal[True] = ...,
    ) -> pandas.Series:
        ...

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
        dry_run: bool = False,
    ) -> dataframe.DataFrame | pandas.Series:
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
                When both ``columns`` and ``col_order`` are specified.
        """
        # NOTE: This method doesn't (yet) exist in pandas or pandas-gbq, so
        # these docstrings are inline.
        if columns and col_order:
            raise ValueError(
                "Must specify either columns (preferred) or col_order, not both"
            )
        elif col_order:
            columns = col_order

        return self._loader.read_gbq_table(  # type: ignore # for dry_run overload
            table_id=query,
            index_col=index_col,
            columns=columns,
            max_results=max_results,
            use_cache=use_cache,
            filters=filters,
            dry_run=dry_run,
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
        msg = bfe.format_message(
            "The bigframes.streaming module is a preview feature, and subject to change."
        )
        warnings.warn(msg, stacklevel=1, category=bfe.PreviewWarning)

        import bigframes.streaming.dataframe as streaming_dataframe

        df = self._loader.read_gbq_table(
            table,
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
        self,
        pandas_dataframe: pandas.Index,
        *,
        write_engine: constants.WriteEngineType = "default",
    ) -> bigframes.core.indexes.Index:
        ...

    @typing.overload
    def read_pandas(
        self,
        pandas_dataframe: pandas.Series,
        *,
        write_engine: constants.WriteEngineType = "default",
    ) -> bigframes.series.Series:
        ...

    @typing.overload
    def read_pandas(
        self,
        pandas_dataframe: pandas.DataFrame,
        *,
        write_engine: constants.WriteEngineType = "default",
    ) -> dataframe.DataFrame:
        ...

    def read_pandas(
        self,
        pandas_dataframe: Union[pandas.DataFrame, pandas.Series, pandas.Index],
        *,
        write_engine: constants.WriteEngineType = "default",
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
            write_engine (str):
                How data should be written to BigQuery (if at all). Supported
                values:

                * "default":
                  (Recommended) Select an appropriate mechanism to write data
                  to BigQuery. Depends on data size and supported data types.
                * "bigquery_inline":
                  Inline data in BigQuery SQL. Use this when you know the data
                  is small enough to fit within BigQuery's 1 MB query text size
                  limit.
                * "bigquery_load":
                  Use a BigQuery load job. Use this for larger data sizes.
                * "bigquery_streaming":
                  Use the BigQuery streaming JSON API. Use this if your
                  workload is such that you exhaust the BigQuery load job
                  quota and your data cannot be embedded in SQL due to size or
                  data type limitations.
                * "bigquery_write":
                  [Preview] Use the BigQuery Storage Write API. This feature
                  is in public preview.
        Returns:
            An equivalent bigframes.pandas.(DataFrame/Series/Index) object

        Raises:
            ValueError:
                When the object is not a Pandas DataFrame.
        """
        import bigframes.series as series

        # Try to handle non-dataframe pandas objects as well
        if isinstance(pandas_dataframe, pandas.Series):
            bf_df = self._read_pandas(
                pandas.DataFrame(pandas_dataframe),
                write_engine=write_engine,
            )
            bf_series = series.Series(bf_df._block)
            # wrapping into df can set name to 0 so reset to original object name
            bf_series.name = pandas_dataframe.name
            return bf_series
        if isinstance(pandas_dataframe, pandas.Index):
            return self._read_pandas(
                pandas.DataFrame(index=pandas_dataframe),
                write_engine=write_engine,
            ).index
        if isinstance(pandas_dataframe, pandas.DataFrame):
            return self._read_pandas(pandas_dataframe, write_engine=write_engine)
        else:
            raise ValueError(
                f"read_pandas() expects a pandas.DataFrame, but got a {type(pandas_dataframe)}"
            )

    def _read_pandas(
        self,
        pandas_dataframe: pandas.DataFrame,
        *,
        write_engine: constants.WriteEngineType = "default",
    ) -> dataframe.DataFrame:
        import bigframes.dataframe as dataframe

        if isinstance(pandas_dataframe, dataframe.DataFrame):
            raise ValueError(
                "read_pandas() expects a pandas.DataFrame, but got a "
                "bigframes.pandas.DataFrame."
            )

        mem_usage = pandas_dataframe.memory_usage(deep=True).sum()
        if write_engine == "default":
            write_engine = (
                "bigquery_load"
                if mem_usage > bigframes.constants.MAX_INLINE_BYTES
                else "bigquery_inline"
            )

        if write_engine == "bigquery_inline":
            if mem_usage > bigframes.constants.MAX_INLINE_BYTES:
                raise ValueError(
                    f"DataFrame size ({mem_usage} bytes) exceeds the maximum allowed "
                    f"for inline data ({bigframes.constants.MAX_INLINE_BYTES} bytes)."
                )
            return self._read_pandas_inline(pandas_dataframe)
        elif write_engine == "bigquery_load":
            return self._loader.read_pandas(pandas_dataframe, method="load")
        elif write_engine == "bigquery_streaming":
            return self._loader.read_pandas(pandas_dataframe, method="stream")
        elif write_engine == "bigquery_write":
            return self._loader.read_pandas(pandas_dataframe, method="write")
        elif write_engine == "_deferred":
            import bigframes.dataframe as dataframe

            return dataframe.DataFrame(blocks.Block.from_local(pandas_dataframe, self))
        else:
            raise ValueError(f"Got unexpected write_engine '{write_engine}'")

    def _read_pandas_inline(
        self, pandas_dataframe: pandas.DataFrame
    ) -> dataframe.DataFrame:
        import bigframes.dataframe as dataframe

        local_block = blocks.Block.from_local(pandas_dataframe, self)
        return dataframe.DataFrame(local_block)

    def read_arrow(self, pa_table: pa.Table) -> bigframes.dataframe.DataFrame:
        """Load a PyArrow Table to a BigQuery DataFrames DataFrame.

        Args:
            pa_table (pyarrow.Table):
                PyArrow table to load data from.

        Returns:
            bigframes.dataframe.DataFrame:
                A new DataFrame representing the data from the PyArrow table.
        """
        import bigframes.dataframe as dataframe

        local_block = blocks.Block.from_pyarrow(pa_table, self)
        return dataframe.DataFrame(local_block)

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
        write_engine: constants.WriteEngineType = "default",
        **kwargs,
    ) -> dataframe.DataFrame:
        bigframes.session.validation.validate_engine_compatibility(
            engine=engine,
            write_engine=write_engine,
        )

        if engine != "bigquery":
            # Using pandas.read_csv by default and warning about potential issues with
            # large files.
            return self._read_csv_w_pandas_engines(
                filepath_or_buffer,
                sep=sep,
                header=header,
                names=names,
                index_col=index_col,
                usecols=usecols,  # type: ignore
                dtype=dtype,
                engine=engine,
                encoding=encoding,
                write_engine=write_engine,
                **kwargs,
            )
        else:
            return self._read_csv_w_bigquery_engine(
                filepath_or_buffer,
                sep=sep,
                header=header,
                names=names,
                index_col=index_col,
                usecols=usecols,  # type: ignore
                dtype=dtype,
                encoding=encoding,
            )

    def _read_csv_w_pandas_engines(
        self,
        filepath_or_buffer,
        *,
        sep,
        header,
        names,
        index_col,
        usecols,
        dtype,
        engine,
        encoding,
        write_engine,
        **kwargs,
    ) -> dataframe.DataFrame:
        """Reads a CSV file using pandas engines into a BigQuery DataFrames.

        This method serves as the implementation backend for read_csv when the
        specified engine is one supported directly by pandas ('c', 'python',
        'pyarrow').
        """
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
        return self._read_pandas(pandas_df, write_engine=write_engine)  # type: ignore

    def _read_csv_w_bigquery_engine(
        self,
        filepath_or_buffer,
        *,
        sep,
        header,
        names,
        index_col,
        usecols,
        dtype,
        encoding,
    ) -> dataframe.DataFrame:
        """Reads a CSV file using the BigQuery engine into a BigQuery DataFrames.

        This method serves as the implementation backend for read_csv when the
        'bigquery' engine is specified or inferred. It leverages BigQuery's
        native CSV loading capabilities, making it suitable for large datasets
        that may not fit into local memory.
        """
        if dtype is not None and not utils.is_dict_like(dtype):
            raise ValueError("dtype should be a dict-like object.")

        if names is not None:
            if len(names) != len(set(names)):
                raise ValueError("Duplicated names are not allowed.")
            if not (
                bigframes.core.utils.is_list_like(names, allow_sets=False)
                or isinstance(names, abc.KeysView)
            ):
                raise ValueError("Names should be an ordered collection.")

        if index_col is True:
            raise ValueError("The value of index_col couldn't be 'True'")

        # None and False cannot be passed to read_gbq.
        if index_col is None or index_col is False:
            index_col = ()

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
        job_config.source_format = bigquery.SourceFormat.CSV
        job_config.autodetect = True
        job_config.field_delimiter = sep
        job_config.encoding = encoding
        job_config.labels = {"bigframes-api": "read_csv"}

        # b/409070192: When header > 0, pandas and BigFrames returns different column naming.

        # We want to match pandas behavior. If header is 0, no rows should be skipped, so we
        # do not need to set `skip_leading_rows`. If header is None, then there is no header.
        # Setting skip_leading_rows to 0 does that. If header=N and N>0, we want to skip N rows.
        if header is None:
            job_config.skip_leading_rows = 0
        elif header > 0:
            job_config.skip_leading_rows = header + 1

        table_id = self._loader.load_file(filepath_or_buffer, job_config=job_config)
        df = self._loader.read_gbq_table(
            table_id,
            index_col=index_col,
            columns=columns,
            names=names,
            index_col_in_columns=True,
        )

        if dtype is not None:
            for column, dtype in dtype.items():
                if column in df.columns:
                    df[column] = df[column].astype(dtype)
        return df

    def read_pickle(
        self,
        filepath_or_buffer: FilePath | ReadPickleBuffer,
        compression: CompressionOptions = "infer",
        storage_options: StorageOptions = None,
        *,
        write_engine: constants.WriteEngineType = "default",
    ):
        pandas_obj = pandas.read_pickle(
            filepath_or_buffer,
            compression=compression,
            storage_options=storage_options,
        )

        if isinstance(pandas_obj, pandas.Series):
            if pandas_obj.name is None:
                pandas_obj.name = 0
            bigframes_df = self._read_pandas(pandas_obj.to_frame())
            return bigframes_df[bigframes_df.columns[0]]
        return self._read_pandas(pandas_obj, write_engine=write_engine)

    def read_parquet(
        self,
        path: str | IO["bytes"],
        *,
        engine: str = "auto",
        write_engine: constants.WriteEngineType = "default",
    ) -> dataframe.DataFrame:
        bigframes.session.validation.validate_engine_compatibility(
            engine=engine,
            write_engine=write_engine,
        )
        if engine == "bigquery":
            job_config = bigquery.LoadJobConfig()
            job_config.source_format = bigquery.SourceFormat.PARQUET

            # Ensure we can load pyarrow.list_ / BQ ARRAY type.
            # See internal issue 414374215.
            parquet_options = bigquery.ParquetOptions()
            parquet_options.enable_list_inference = True
            job_config.parquet_options = parquet_options

            job_config.labels = {"bigframes-api": "read_parquet"}
            table_id = self._loader.load_file(path, job_config=job_config)
            return self._loader.read_gbq_table(table_id)
        else:
            if "*" in path:
                raise ValueError(
                    "The provided path contains a wildcard character (*), which is not "
                    "supported by the current engine. To read files from wildcard paths, "
                    "please use the 'bigquery' engine by setting `engine='bigquery'` in "
                    "your configuration."
                )

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
            return self._read_pandas(pandas_obj, write_engine=write_engine)

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
        write_engine: constants.WriteEngineType = "default",
        **kwargs,
    ) -> dataframe.DataFrame:
        bigframes.session.validation.validate_engine_compatibility(
            engine=engine,
            write_engine=write_engine,
        )
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
            job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
            job_config.autodetect = True
            job_config.encoding = encoding
            job_config.labels = {"bigframes-api": "read_json"}

            table_id = self._loader.load_file(path_or_buf, job_config=job_config)
            return self._loader.read_gbq_table(table_id)
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
            return self._read_pandas(pandas_df, write_engine=write_engine)

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

    def deploy_remote_function(
        self,
        func,
        **kwargs,
    ):
        """Orchestrates the creation of a BigQuery remote function that deploys immediately.

        This method ensures that the remote function is created and available for
        use in BigQuery as soon as this call is made.

        Args:
            func:
                Function to deploy.
            kwargs:
                All arguments are passed directly to
                :meth:`~bigframes.session.Session.remote_function`.  Please see
                its docstring for parameter details.

        Returns:
            A wrapped remote function, usable in
            :meth:`~bigframes.series.Series.apply`.
        """
        return self._function_session.deploy_remote_function(
            func,
            # Session-provided arguments.
            session=self,
            bigquery_client=self._clients_provider.bqclient,
            bigquery_connection_client=self._clients_provider.bqconnectionclient,
            cloud_functions_client=self._clients_provider.cloudfunctionsclient,
            resource_manager_client=self._clients_provider.resourcemanagerclient,
            # User-provided arguments.
            **kwargs,
        )

    def remote_function(
        self,
        # Make sure that the input/output types, and dataset can be used
        # positionally. This avoids the worst of the breaking change from 1.x to
        # 2.x while still preventing possible mixups between consecutive str
        # parameters.
        input_types: Union[None, type, Sequence[type]] = None,
        output_type: Optional[type] = None,
        dataset: Optional[str] = None,
        *,
        bigquery_connection: Optional[str] = None,
        reuse: bool = True,
        name: Optional[str] = None,
        packages: Optional[Sequence[str]] = None,
        cloud_function_service_account: str,
        cloud_function_kms_key_name: Optional[str] = None,
        cloud_function_docker_repository: Optional[str] = None,
        max_batching_rows: Optional[int] = 1000,
        cloud_function_timeout: Optional[int] = 600,
        cloud_function_max_instances: Optional[int] = None,
        cloud_function_vpc_connector: Optional[str] = None,
        cloud_function_memory_mib: Optional[int] = 1024,
        cloud_function_ingress_settings: Literal[
            "all", "internal-only", "internal-and-gclb"
        ] = "internal-only",
        cloud_build_service_account: Optional[str] = None,
    ):
        """Decorator to turn a user defined function into a BigQuery remote function. Check out
        the code samples at: https://cloud.google.com/bigquery/docs/remote-functions#bigquery-dataframes.

        .. note::
            ``input_types=Series`` scenario is in preview. It currently only
            supports dataframe with column types ``Int64``/``Float64``/``boolean``/
            ``string``/``binary[pyarrow]``.

        .. warning::
            To use remote functions with Bigframes 2.0 and onwards, please (preferred)
            set an explicit user-managed ``cloud_function_service_account`` or (discouraged)
            set ``cloud_function_service_account`` to use the Compute Engine service account
            by setting it to `"default"`.

            See, https://cloud.google.com/functions/docs/securing/function-identity.

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
            input_types (type or sequence(type), Optional):
                For scalar user defined function it should be the input type or
                sequence of input types. The supported scalar input types are
                `bool`, `bytes`, `float`, `int`, `str`. For row processing user
                defined function (i.e. functions that receive a single input
                representing a row in form of a Series), type `Series` should be
                specified.
            output_type (type, Optional):
                Data type of the output in the user defined function. If the
                user defined function returns an array, then `list[type]` should
                be specified. The supported output types are `bool`, `bytes`,
                `float`, `int`, `str`, `list[bool]`, `list[float]`, `list[int]`
                and `list[str]`.
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
            cloud_function_service_account (str):
                Service account to use for the cloud functions. If "default" provided
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
                function. Options are: `all`, `internal-only`, or `internal-and-gclb`.
                If no setting is provided, `internal-only` will be used by default.
                See for more details
                https://cloud.google.com/functions/docs/networking/network-settings#ingress_settings.
            cloud_build_service_account (str, Optional):
                Service account in the fully qualified format
                `projects/PROJECT_ID/serviceAccounts/SERVICE_ACCOUNT_EMAIL`, or
                just the SERVICE_ACCOUNT_EMAIL. The latter would be interpreted
                as belonging to the BigQuery DataFrames session project. This is
                to be used by Cloud Build to build the function source code into
                a deployable artifact. If not provided, the default Cloud Build
                service account is used. See
                https://cloud.google.com/build/docs/cloud-build-service-account
                for more details.
        Returns:
            collections.abc.Callable:
                A remote function object pointing to the cloud assets created
                in the background to support the remote execution. The cloud assets can be
                located through the following properties set in the object:

                `bigframes_cloud_function` - The google cloud function deployed for the user defined code.

                `bigframes_remote_function` - The bigquery remote function capable of calling into `bigframes_cloud_function`.
        """
        return self._function_session.remote_function(
            # Session-provided arguments.
            session=self,
            bigquery_client=self._clients_provider.bqclient,
            bigquery_connection_client=self._clients_provider.bqconnectionclient,
            cloud_functions_client=self._clients_provider.cloudfunctionsclient,
            resource_manager_client=self._clients_provider.resourcemanagerclient,
            # User-provided arguments.
            input_types=input_types,
            output_type=output_type,
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
            cloud_build_service_account=cloud_build_service_account,
        )

    def deploy_udf(
        self,
        func,
        **kwargs,
    ):
        """Orchestrates the creation of a BigQuery UDF that deploys immediately.

        This method ensures that the UDF is created and available for
        use in BigQuery as soon as this call is made.

        Args:
            func:
                Function to deploy.
            kwargs:
                All arguments are passed directly to
                :meth:`~bigframes.session.Session.udf`.  Please see
                its docstring for parameter details.

        Returns:
            A wrapped Python user defined function, usable in
            :meth:`~bigframes.series.Series.apply`.
        """
        return self._function_session.deploy_udf(
            func,
            # Session-provided arguments.
            session=self,
            bigquery_client=self._clients_provider.bqclient,
            # User-provided arguments.
            **kwargs,
        )

    def udf(
        self,
        *,
        input_types: Union[None, type, Sequence[type]] = None,
        output_type: Optional[type] = None,
        dataset: str,
        bigquery_connection: Optional[str] = None,
        name: str,
        packages: Optional[Sequence[str]] = None,
    ):
        """Decorator to turn a Python user defined function (udf) into a
        [BigQuery managed user-defined function](https://cloud.google.com/bigquery/docs/user-defined-functions-python).

        .. note::
            This feature is in preview. The code in the udf must be
            (1) self-contained, i.e. it must not contain any
            references to an import or variable defined outside the function
            body, and
            (2) Python 3.11 compatible, as that is the environment
            in which the code is executed in the cloud.

        .. note::
            Please have BigQuery Data Editor (roles/bigquery.dataEditor) IAM
            role enabled for you.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import datetime
            >>> bpd.options.display.progress_bar = None

        Turning an arbitrary python function into a BigQuery managed python udf:

            >>> bq_name = datetime.datetime.now().strftime("bigframes_%Y%m%d%H%M%S%f")
            >>> @bpd.udf(dataset="bigfranes_testing", name=bq_name)
            ... def minutes_to_hours(x: int) -> float:
            ...     return x/60

            >>> minutes = bpd.Series([0, 30, 60, 90, 120])
            >>> minutes
            0      0
            1     30
            2     60
            3     90
            4    120
            dtype: Int64

            >>> hours = minutes.apply(minutes_to_hours)
            >>> hours
            0    0.0
            1    0.5
            2    1.0
            3    1.5
            4    2.0
            dtype: Float64

        To turn a user defined function with external package dependencies into
        a BigQuery managed python udf, you would provide the names of the
        packages (optionally with the package version) via `packages` param.

            >>> bq_name = datetime.datetime.now().strftime("bigframes_%Y%m%d%H%M%S%f")
            >>> @bpd.udf(
            ...     dataset="bigfranes_testing",
            ...     name=bq_name,
            ...     packages=["cryptography"]
            ... )
            ... def get_hash(input: str) -> str:
            ...     from cryptography.fernet import Fernet
            ...
            ...     # handle missing value
            ...     if input is None:
            ...         input = ""
            ...
            ...     key = Fernet.generate_key()
            ...     f = Fernet(key)
            ...     return f.encrypt(input.encode()).decode()

            >>> names = bpd.Series(["Alice", "Bob"])
            >>> hashes = names.apply(get_hash)

        You can clean-up the BigQuery functions created above using the BigQuery
        client from the BigQuery DataFrames session:

            >>> session = bpd.get_global_session()
            >>> session.bqclient.delete_routine(minutes_to_hours.bigframes_bigquery_function)
            >>> session.bqclient.delete_routine(get_hash.bigframes_bigquery_function)

        Args:
            input_types (type or sequence(type), Optional):
                For scalar user defined function it should be the input type or
                sequence of input types. The supported scalar input types are
                `bool`, `bytes`, `float`, `int`, `str`.
            output_type (type, Optional):
                Data type of the output in the user defined function. If the
                user defined function returns an array, then `list[type]` should
                be specified. The supported output types are `bool`, `bytes`,
                `float`, `int`, `str`, `list[bool]`, `list[float]`, `list[int]`
                and `list[str]`.
            dataset (str):
                Dataset in which to create a BigQuery managed function. It
                should be in `<project_id>.<dataset_name>` or `<dataset_name>`
                format.
            bigquery_connection (str, Optional):
                Name of the BigQuery connection. It is used to provide an
                identity to the serverless instances running the user code. It
                helps BigQuery manage and track the resources used by the udf.
                This connection is required for internet access and for
                interacting with other GCP services. To access GCP services, the
                appropriate IAM permissions must also be granted to the
                connection's Service Account. When it defaults to None, the udf
                will be created without any connection. A udf without a
                connection has no internet access and no access to other GCP
                services.
            name (str):
                Explicit name of the persisted BigQuery managed function. Use it
                with caution, because more than one users working in the same
                project and dataset could overwrite each other's managed
                functions if they use the same persistent name. Please note that
                any session specific clean up (
                ``bigframes.session.Session.close``/
                ``bigframes.pandas.close_session``/
                ``bigframes.pandas.reset_session``/
                ``bigframes.pandas.clean_up_by_session_id``) does not clean up
                this function, and leaves it for the user to manage the function
                directly.
            packages (str[], Optional):
                Explicit name of the external package dependencies. Each
                dependency is added to the `requirements.txt` as is, and can be
                of the form supported in
                https://pip.pypa.io/en/stable/reference/requirements-file-format/.
        Returns:
            collections.abc.Callable:
                A managed function object pointing to the cloud assets created
                in the background to support the remote execution. The cloud
                ssets can be located through the following properties set in the
                object:

                `bigframes_bigquery_function` - The bigquery managed function
                deployed for the user defined code.
        """
        return self._function_session.udf(
            # Session-provided arguments.
            session=self,
            bigquery_client=self._clients_provider.bqclient,
            # User-provided arguments.
            input_types=input_types,
            output_type=output_type,
            dataset=dataset,
            bigquery_connection=bigquery_connection,
            name=name,
            packages=packages,
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

        Another use case is to define your own remote function and use it later.
        For example, define the remote function:

            >>> @bpd.remote_function(cloud_function_service_account="default")
            ... def tenfold(num: int) -> float:
            ...     return num * 10

        Then, read back the deployed BQ remote function:

            >>> tenfold_ref = bpd.read_gbq_function(
            ...     tenfold.bigframes_remote_function,
            ... )

            >>> df = bpd.DataFrame({'a': [1, 2], 'b': [3, 4], 'c': [5, 6]})
            >>> df
                a   b   c
            0   1   3   5
            1   2   4   6
            <BLANKLINE>
            [2 rows x 3 columns]

            >>> df['a'].apply(tenfold_ref)
            0    10.0
            1    20.0
            Name: a, dtype: Float64

        It also supports row processing by using `is_row_processor=True`. Please
        note, row processor implies that the function has only one input
        parameter.

            >>> @bpd.remote_function(cloud_function_service_account="default")
            ... def row_sum(s: bpd.Series) -> float:
            ...     return s['a'] + s['b'] + s['c']

            >>> row_sum_ref = bpd.read_gbq_function(
            ...     row_sum.bigframes_remote_function,
            ...     is_row_processor=True,
            ... )

            >>> df = bpd.DataFrame({'a': [1, 2], 'b': [3, 4], 'c': [5, 6]})
            >>> df
                a   b   c
            0   1   3   5
            1   2   4   6
            <BLANKLINE>
            [2 rows x 3 columns]

            >>> df.apply(row_sum_ref, axis=1)
            0     9.0
            1    12.0
            dtype: Float64

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
            collections.abc.Callable:
                A function object pointing to the BigQuery function read
                from BigQuery.

                The object is similar to the one created by the `remote_function`
                decorator, including the `bigframes_remote_function` property, but
                not including the `bigframes_cloud_function` property.
        """

        return bff.read_gbq_function(
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
        iterator, query_job = bf_io_bigquery.start_query_with_client(
            self.bqclient,
            sql,
            job_config=job_config,
            metrics=self._metrics,
            location=None,
            project=None,
            timeout=None,
            query_with_job=True,
        )
        return iterator, query_job

    def _create_object_table(self, path: str, connection: str) -> str:
        """Create a random id Object Table from the input path and connection."""
        table = str(self._anon_dataset_manager.generate_unique_resource_id())

        import textwrap

        sql = textwrap.dedent(
            f"""
            CREATE EXTERNAL TABLE `{table}`
            WITH CONNECTION `{connection}`
            OPTIONS(
                object_metadata = 'SIMPLE',
                uris = ['{path}']);
            """
        )
        bf_io_bigquery.start_query_with_client(
            self.bqclient,
            sql,
            job_config=bigquery.QueryJobConfig(),
            metrics=self._metrics,
            location=None,
            project=None,
            timeout=None,
            query_with_job=True,
        )

        return table

    def _create_temp_view(self, sql: str) -> bigquery.TableReference:
        """Create a random id view from the sql string."""
        return self._anon_dataset_manager.create_temp_view(sql)

    def _create_temp_table(
        self, schema: Sequence[bigquery.SchemaField], cluster_cols: Sequence[str] = []
    ) -> bigquery.TableReference:
        """Allocate a random temporary table with the desired schema."""
        return self._temp_storage_manager.create_temp_table(
            schema=schema, cluster_cols=cluster_cols
        )

    def from_glob_path(
        self, path: str, *, connection: Optional[str] = None, name: Optional[str] = None
    ) -> dataframe.DataFrame:
        r"""Create a BigFrames DataFrame that contains a BigFrames Blob column from a global wildcard path.
        This operation creates a temporary BQ Object Table under the hood and requires bigquery.connections.delegate permission or BigQuery Connection Admin role.
        If you have an existing BQ Object Table, use read_gbq_object_table().

        .. note::
            BigFrames Blob is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
            Service Specific Terms(https://cloud.google.com/terms/service-terms#1). Pre-GA products and features are available "as is"
            and might have limited support. For more information, see the launch stage descriptions
            (https://cloud.google.com/products#product-launch-stages).

        Args:
            path (str):
                The wildcard global path, such as "gs://<bucket>/<folder>/\*".
            connection (str or None, default None):
                Connection to connect with remote service. str of the format <PROJECT_NUMBER/PROJECT_ID>.<LOCATION>.<CONNECTION_ID>.
                If None, use default connection in session context. BigQuery DataFrame will try to create the connection and attach
                permission if the connection isn't fully set up.
            name (str):
                The column name of the Blob column.
        Returns:
            bigframes.pandas.DataFrame:
                Result BigFrames DataFrame.
        """
        # TODO(garrettwu): switch to pseudocolumn when b/374988109 is done.
        connection = self._create_bq_connection(connection=connection)

        table = self._create_object_table(path, connection)

        s = self._loader.read_gbq_table(table)["uri"].str.to_blob(connection)
        return s.rename(name).to_frame()

    def _create_bq_connection(
        self,
        *,
        connection: Optional[str] = None,
        iam_role: Optional[str] = None,
    ) -> str:
        """Create the connection with the session settings and try to attach iam role to the connection SA.
        If any of project, location or connection isn't specified, use the session defaults. Returns fully-qualified connection name."""
        connection = self._bq_connection if not connection else connection
        connection = bigframes.clients.get_canonical_bq_connection_id(
            connection_id=connection,
            default_project=self._project,
            default_location=self._location,
        )
        connection_parts = connection.split(".")
        assert len(connection_parts) == 3

        self.bqconnectionmanager.create_bq_connection(
            project_id=connection_parts[0],
            location=connection_parts[1],
            connection_id=connection_parts[2],
            iam_role=iam_role,
        )

        return connection

    def read_gbq_object_table(
        self, object_table: str, *, name: Optional[str] = None
    ) -> dataframe.DataFrame:
        """Read an existing object table to create a BigFrames Blob DataFrame. Use the connection of the object table for the connection of the blob.
        This function dosen't retrieve the object table data. If you want to read the data, use read_gbq() instead.

        .. note::
            BigFrames Blob is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
            Service Specific Terms(https://cloud.google.com/terms/service-terms#1). Pre-GA products and features are available "as is"
            and might have limited support. For more information, see the launch stage descriptions
            (https://cloud.google.com/products#product-launch-stages).

        Args:
            object_table (str): name of the object table of form <PROJECT_ID>.<DATASET_ID>.<TABLE_ID>.
            name (str or None): the returned blob column name.

        Returns:
            bigframes.pandas.DataFrame:
                Result BigFrames DataFrame.
        """
        # TODO(garrettwu): switch to pseudocolumn when b/374988109 is done.
        table = self.bqclient.get_table(object_table)
        connection = table._properties["externalDataConfiguration"]["connectionId"]

        s = self._loader.read_gbq_table(object_table)["uri"].str.to_blob(connection)
        return s.rename(name).to_frame()


def connect(context: Optional[bigquery_options.BigQueryOptions] = None) -> Session:
    return Session(context)


def _warn_if_bf_version_is_obsolete():
    today = datetime.datetime.today()
    release_date = datetime.datetime.strptime(version.__release_date__, "%Y-%m-%d")
    if today - release_date > datetime.timedelta(days=365):
        msg = f"Your BigFrames version {version.__version__} is more than 1 year old. Please update to the lastest version."
        warnings.warn(msg, bfe.ObsoleteVersionWarning)
