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

import copy
import datetime
import itertools
import logging
import math
import os
import secrets
import typing
from typing import (
    Any,
    Callable,
    Dict,
    Hashable,
    IO,
    Iterable,
    List,
    Literal,
    Mapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Union,
)
import uuid
import warnings
import weakref

import bigframes_vendored.ibis.backends.bigquery  # noqa
import bigframes_vendored.pandas.io.gbq as third_party_pandas_gbq
import bigframes_vendored.pandas.io.parquet as third_party_pandas_parquet
import bigframes_vendored.pandas.io.parsers.readers as third_party_pandas_readers
import bigframes_vendored.pandas.io.pickle as third_party_pandas_pickle
import google.api_core.client_info
import google.api_core.client_options
import google.api_core.exceptions
import google.api_core.gapic_v1.client_info
import google.auth.credentials
import google.cloud.bigquery as bigquery
import google.cloud.bigquery.table
import google.cloud.bigquery_connection_v1
import google.cloud.bigquery_storage_v1
import google.cloud.functions_v2
import google.cloud.resourcemanager_v3
import google.cloud.storage as storage  # type: ignore
import ibis
import ibis.backends.bigquery as ibis_bigquery
import jellyfish
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
import bigframes.constants as constants
import bigframes.core as core
import bigframes.core.blocks as blocks
import bigframes.core.compile
import bigframes.core.guid
import bigframes.core.nodes as nodes
import bigframes.core.ordering as order
import bigframes.core.pruning
import bigframes.core.schema as schemata
import bigframes.core.tree_properties as traversals
import bigframes.core.tree_properties as tree_properties
import bigframes.core.utils as utils

# Even though the ibis.backends.bigquery import is unused, it's needed
# to register new and replacement ops with the Ibis BigQuery backend.
import bigframes.dataframe
import bigframes.dtypes
import bigframes.exceptions
import bigframes.formatting_helpers as formatting_helpers
from bigframes.functions.remote_function import read_gbq_function as bigframes_rgf
from bigframes.functions.remote_function import remote_function as bigframes_rf
import bigframes.session._io.bigquery as bf_io_bigquery
import bigframes.session._io.bigquery.read_gbq_table as bf_read_gbq_table
import bigframes.session.clients
import bigframes.session.planner
import bigframes.version

# Avoid circular imports.
if typing.TYPE_CHECKING:
    import bigframes.core.indexes
    import bigframes.dataframe as dataframe
    import bigframes.series

_BIGFRAMES_DEFAULT_CONNECTION_ID = "bigframes-default-connection"

_TEMP_TABLE_ID_FORMAT = "bqdf{date}_{session_id}_{random_id}"

_MAX_CLUSTER_COLUMNS = 4

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

# Max complexity that should be executed as a single query
QUERY_COMPLEXITY_LIMIT = 1e7
# Number of times to factor out subqueries before giving up.
MAX_SUBTREE_FACTORINGS = 5

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


def _to_index_cols(
    index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = (),
) -> List[str]:
    """Convert index_col into a list of column names."""
    if isinstance(index_col, bigframes.enums.DefaultIndexKind):
        index_cols: List[str] = []
    elif isinstance(index_col, str):
        index_cols = [index_col]
    else:
        index_cols = list(index_col)

    return index_cols


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

        self._anonymous_dataset = (
            bigframes.session._io.bigquery.create_bq_dataset_reference(
                self.bqclient,
                location=self._location,
                api_name="session-__init__",
            )
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
        self._df_snapshot: Dict[
            bigquery.TableReference, Tuple[datetime.datetime, bigquery.Table]
        ] = {}

        # unique session identifier, short enough to be human readable
        # only needs to be unique among sessions created by the same user
        # at the same time in the same region
        self._session_id: str = "session" + secrets.token_hex(3)
        self._table_ids: List[str] = []
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
        self._cached_executions: weakref.WeakKeyDictionary[
            nodes.BigFrameNode, nodes.BigFrameNode
        ] = weakref.WeakKeyDictionary()

        # performance logging
        self._bytes_processed_sum = 0
        self._slot_millis_sum = 0
        self._execution_count = 0
        # Whether this session treats objects as totally ordered.
        # Will expose as feature later, only False for internal testing
        self._strictly_ordered: bool = context._strictly_ordered
        # Sequential index needs total ordering to generate, so use null index with unstrict ordering.
        self._default_index_type: bigframes.enums.DefaultIndexKind = (
            bigframes.enums.DefaultIndexKind.SEQUENTIAL_INT64
            if context._strictly_ordered
            else bigframes.enums.DefaultIndexKind.NULL
        )

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
        return self._bytes_processed_sum

    @property
    def slot_millis_sum(self):
        """The sum of all slot time used by bigquery jobs in this session."""
        return self._slot_millis_sum

    def _add_bytes_processed(self, amount: int):
        """Increment bytes_processed_sum by amount."""
        self._bytes_processed_sum += amount

    def _add_slot_millis(self, amount: int):
        """Increment slot_millis_sum by amount."""
        self._slot_millis_sum += amount

    def _add_execution(self, amount: int = 1):
        """Increment slot_millis_sum by amount."""
        self._execution_count += amount

    def __hash__(self):
        # Stable hash needed to use in expression tree
        return hash(str(self._anonymous_dataset))

    def close(self):
        """Delete tables that were created with this session's session_id."""
        client = self.bqclient
        project_id = self._anonymous_dataset.project
        dataset_id = self._anonymous_dataset.dataset_id

        for table_id in self._table_ids:
            full_id = ".".join([project_id, dataset_id, table_id])
            client.delete_table(full_id, not_found_ok=True)

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
            return self._read_gbq_query(
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

            return self._read_gbq_table(
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

    def _query_to_destination(
        self,
        query: str,
        index_cols: List[str],
        api_name: str,
        configuration: dict = {"query": {"useQueryCache": True}},
        do_clustering=True,
    ) -> Tuple[Optional[bigquery.TableReference], bigquery.QueryJob]:
        self._add_execution(1)
        # If a dry_run indicates this is not a query type job, then don't
        # bother trying to do a CREATE TEMP TABLE ... AS SELECT ... statement.
        dry_run_config = bigquery.QueryJobConfig()
        dry_run_config.dry_run = True
        _, dry_run_job = self._start_query(
            query, job_config=dry_run_config, api_name=api_name
        )
        if dry_run_job.statement_type != "SELECT":
            _, query_job = self._start_query(query, api_name=api_name)
            return query_job.destination, query_job

        # Create a table to workaround BigQuery 10 GB query results limit. See:
        # internal issue 303057336.
        # Since we have a `statement_type == 'SELECT'`, schema should be populated.
        schema = typing.cast(Iterable[bigquery.SchemaField], dry_run_job.schema)
        if do_clustering:
            cluster_cols = [
                item.name
                for item in schema
                if (item.name in index_cols) and _can_cluster_bq(item)
            ][:_MAX_CLUSTER_COLUMNS]
        else:
            cluster_cols = []
        temp_table = self._create_empty_temp_table(schema, cluster_cols)

        timeout_ms = configuration.get("jobTimeoutMs") or configuration["query"].get(
            "timeoutMs"
        )

        # Convert timeout_ms to seconds, ensuring a minimum of 0.1 seconds to avoid
        # the program getting stuck on too-short timeouts.
        timeout = max(int(timeout_ms) * 1e-3, 0.1) if timeout_ms else None

        job_config = typing.cast(
            bigquery.QueryJobConfig,
            bigquery.QueryJobConfig.from_api_repr(configuration),
        )
        job_config.destination = temp_table

        try:
            # Write to temp table to workaround BigQuery 10 GB query results
            # limit. See: internal issue 303057336.
            job_config.labels["error_caught"] = "true"
            _, query_job = self._start_query(
                query,
                job_config=job_config,
                timeout=timeout,
                api_name=api_name,
            )
            return query_job.destination, query_job
        except google.api_core.exceptions.BadRequest:
            # Some SELECT statements still aren't compatible with cluster
            # tables as the destination. For example, if the query has a
            # top-level ORDER BY, this conflicts with our ability to cluster
            # the table by the index column(s).
            _, query_job = self._start_query(query, timeout=timeout, api_name=api_name)
            return query_job.destination, query_job

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
        """
        # NOTE: This method doesn't (yet) exist in pandas or pandas-gbq, so
        # these docstrings are inline.
        if columns and col_order:
            raise ValueError(
                "Must specify either columns (preferred) or col_order, not both"
            )
        elif col_order:
            columns = col_order

        return self._read_gbq_query(
            query=query,
            index_col=index_col,
            columns=columns,
            configuration=configuration,
            max_results=max_results,
            api_name="read_gbq_query",
            use_cache=use_cache,
            filters=filters,
        )

    def _read_gbq_query(
        self,
        query: str,
        *,
        index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = (),
        columns: Iterable[str] = (),
        configuration: Optional[Dict] = None,
        max_results: Optional[int] = None,
        api_name: str = "read_gbq_query",
        use_cache: Optional[bool] = None,
        filters: third_party_pandas_gbq.FiltersType = (),
    ) -> dataframe.DataFrame:
        import bigframes.dataframe as dataframe

        configuration = _transform_read_gbq_configuration(configuration)

        if "query" not in configuration:
            configuration["query"] = {}

        if "query" in configuration["query"]:
            raise ValueError(
                "The query statement must not be included in the ",
                "'configuration' because it is already provided as",
                " a separate parameter.",
            )

        if "useQueryCache" in configuration["query"]:
            if use_cache is not None:
                raise ValueError(
                    "'useQueryCache' in 'configuration' conflicts with"
                    " 'use_cache' parameter. Please specify only one."
                )
        else:
            configuration["query"]["useQueryCache"] = (
                True if use_cache is None else use_cache
            )

        index_cols = _to_index_cols(index_col)

        filters = list(filters)
        if len(filters) != 0 or max_results is not None:
            # TODO(b/338111344): If we are running a query anyway, we might as
            # well generate ROW_NUMBER() at the same time.
            all_columns = itertools.chain(index_cols, columns) if columns else ()
            query = bf_io_bigquery.to_query(
                query,
                all_columns,
                bf_io_bigquery.compile_filters(filters) if filters else None,
                max_results=max_results,
                # We're executing the query, so we don't need time travel for
                # determinism.
                time_travel_timestamp=None,
            )

        destination, query_job = self._query_to_destination(
            query,
            index_cols,
            api_name=api_name,
            configuration=configuration,
        )

        # If there was no destination table, that means the query must have
        # been DDL or DML. Return some job metadata, instead.
        if not destination:
            return dataframe.DataFrame(
                data=pandas.DataFrame(
                    {
                        "statement_type": [
                            query_job.statement_type if query_job else "unknown"
                        ],
                        "job_id": [query_job.job_id if query_job else "unknown"],
                        "location": [query_job.location if query_job else "unknown"],
                    }
                ),
                session=self,
            )

        return self._read_gbq_table(
            f"{destination.project}.{destination.dataset_id}.{destination.table_id}",
            index_col=index_col,
            columns=columns,
            use_cache=configuration["query"]["useQueryCache"],
            api_name=api_name,
            # max_results and filters are omitted because they are already
            # handled by to_query(), above.
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
        """
        # NOTE: This method doesn't (yet) exist in pandas or pandas-gbq, so
        # these docstrings are inline.
        if columns and col_order:
            raise ValueError(
                "Must specify either columns (preferred) or col_order, not both"
            )
        elif col_order:
            columns = col_order

        return self._read_gbq_table(
            query=query,
            index_col=index_col,
            columns=columns,
            max_results=max_results,
            api_name="read_gbq_table",
            use_cache=use_cache,
            filters=filters,
        )

    def _read_gbq_table(
        self,
        query: str,
        *,
        index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = (),
        columns: Iterable[str] = (),
        max_results: Optional[int] = None,
        api_name: str,
        use_cache: bool = True,
        filters: third_party_pandas_gbq.FiltersType = (),
    ) -> dataframe.DataFrame:
        import bigframes.dataframe as dataframe

        # ---------------------------------
        # Validate and transform parameters
        # ---------------------------------

        if max_results and max_results <= 0:
            raise ValueError(
                f"`max_results` should be a positive number, got {max_results}."
            )

        table_ref = bigquery.table.TableReference.from_string(
            query, default_project=self.bqclient.project
        )

        columns = list(columns)
        filters = list(filters)

        # ---------------------------------
        # Fetch table metadata and validate
        # ---------------------------------

        time_travel_timestamp, table = bf_read_gbq_table.get_table_metadata(
            self.bqclient,
            table_ref=table_ref,
            api_name=api_name,
            cache=self._df_snapshot,
            use_cache=use_cache,
        )
        table_column_names = {field.name for field in table.schema}

        if table.location.casefold() != self._location.casefold():
            raise ValueError(
                f"Current session is in {self._location} but dataset '{table.project}.{table.dataset_id}' is located in {table.location}"
            )

        for key in columns:
            if key not in table_column_names:
                possibility = min(
                    table_column_names,
                    key=lambda item: jellyfish.levenshtein_distance(key, item),
                )
                raise ValueError(
                    f"Column '{key}' of `columns` not found in this table. Did you mean '{possibility}'?"
                )

        # Converting index_col into a list of column names requires
        # the table metadata because we might use the primary keys
        # when constructing the index.
        index_cols = bf_read_gbq_table.get_index_cols(
            table=table,
            index_col=index_col,
        )

        for key in index_cols:
            if key not in table_column_names:
                possibility = min(
                    table_column_names,
                    key=lambda item: jellyfish.levenshtein_distance(key, item),
                )
                raise ValueError(
                    f"Column '{key}' of `index_col` not found in this table. Did you mean '{possibility}'?"
                )

        # -----------------------------
        # Optionally, execute the query
        # -----------------------------

        # max_results introduces non-determinism and limits the cost on
        # clustered tables, so fallback to a query. We do this here so that
        # the index is consistent with tables that have primary keys, even
        # when max_results is set.
        # TODO(b/338419730): We don't need to fallback to a query for wildcard
        # tables if we allow some non-determinism when time travel isn't supported.
        if max_results is not None or bf_io_bigquery.is_table_with_wildcard_suffix(
            query
        ):
            # TODO(b/338111344): If we are running a query anyway, we might as
            # well generate ROW_NUMBER() at the same time.
            all_columns = itertools.chain(index_cols, columns) if columns else ()
            query = bf_io_bigquery.to_query(
                query,
                columns=all_columns,
                sql_predicate=bf_io_bigquery.compile_filters(filters)
                if filters
                else None,
                max_results=max_results,
                # We're executing the query, so we don't need time travel for
                # determinism.
                time_travel_timestamp=None,
            )

            return self._read_gbq_query(
                query,
                index_col=index_cols,
                columns=columns,
                api_name="read_gbq_table",
                use_cache=use_cache,
            )

        # -----------------------------------------
        # Validate table access and features
        # -----------------------------------------

        # Use a time travel to make sure the DataFrame is deterministic, even
        # if the underlying table changes.

        # If a dry run query fails with time travel but
        # succeeds without it, omit the time travel clause and raise a warning
        # about potential non-determinism if the underlying tables are modified.
        filter_str = bf_io_bigquery.compile_filters(filters) if filters else None
        all_columns = (
            ()
            if len(columns) == 0
            else (*columns, *[col for col in index_cols if col not in columns])
        )

        supports_snapshot = bf_read_gbq_table.validate_table(
            self.bqclient, table_ref, all_columns, time_travel_timestamp, filter_str
        )

        # ----------------------------
        # Create ordering and validate
        # ----------------------------

        # TODO(b/337925142): Generate a new subquery with just the index_cols
        # in the Ibis table expression so we don't have a "SELECT *" subquery
        # in the query that checks for index uniqueness.
        # TODO(b/338065601): Provide a way to assume uniqueness and avoid this
        # check.
        is_index_unique = bf_read_gbq_table.are_index_cols_unique(
            bqclient=self.bqclient,
            table=table,
            index_cols=index_cols,
            api_name=api_name,
        )
        schema = schemata.ArraySchema.from_bq_table(table)
        if columns:
            schema = schema.select(index_cols + columns)
        array_value = core.ArrayValue.from_table(
            table,
            schema=schema,
            predicate=filter_str,
            at_time=time_travel_timestamp if supports_snapshot else None,
            primary_key=index_cols if is_index_unique else (),
            session=self,
        )

        # ----------------------------------------------------
        # Create Default Sequential Index if still have no index
        # ----------------------------------------------------

        # If no index columns provided or found, fall back to session default
        if (index_col != bigframes.enums.DefaultIndexKind.NULL) and len(
            index_cols
        ) == 0:
            index_col = self._default_index_type

        index_names: Sequence[Hashable] = index_cols
        if index_col == bigframes.enums.DefaultIndexKind.SEQUENTIAL_INT64:
            sequential_index_col = bigframes.core.guid.generate_guid("index_")
            array_value = array_value.promote_offsets(sequential_index_col)
            index_cols = [sequential_index_col]
            index_names = [None]

        value_columns = [col for col in array_value.column_ids if col not in index_cols]
        block = blocks.Block(
            array_value,
            index_columns=index_cols,
            column_labels=value_columns,
            index_labels=index_names,
        )
        if max_results:
            block = block.slice(stop=max_results)
        df = dataframe.DataFrame(block)

        # If user provided index columns, should sort over it
        if len(index_cols) > 0:
            df.sort_index()
        return df

    def _read_bigquery_load_job(
        self,
        filepath_or_buffer: str | IO["bytes"],
        table: Union[bigquery.Table, bigquery.TableReference],
        *,
        job_config: bigquery.LoadJobConfig,
        index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind = (),
        columns: Iterable[str] = (),
    ) -> dataframe.DataFrame:
        index_cols = _to_index_cols(index_col)

        if not job_config.clustering_fields and index_cols:
            job_config.clustering_fields = index_cols[:_MAX_CLUSTER_COLUMNS]

        if isinstance(filepath_or_buffer, str):
            if filepath_or_buffer.startswith("gs://"):
                load_job = self.bqclient.load_table_from_uri(
                    filepath_or_buffer, table, job_config=job_config
                )
            else:
                with open(filepath_or_buffer, "rb") as source_file:
                    load_job = self.bqclient.load_table_from_file(
                        source_file, table, job_config=job_config
                    )
        else:
            load_job = self.bqclient.load_table_from_file(
                filepath_or_buffer, table, job_config=job_config
            )

        self._start_generic_job(load_job)
        table_id = f"{table.project}.{table.dataset_id}.{table.table_id}"

        # Update the table expiration so we aren't limited to the default 24
        # hours of the anonymous dataset.
        table_expiration = bigquery.Table(table_id)
        table_expiration.expires = (
            datetime.datetime.now(datetime.timezone.utc) + constants.DEFAULT_EXPIRATION
        )
        self.bqclient.update_table(table_expiration, ["expires"])

        # The BigQuery REST API for tables.get doesn't take a session ID, so we
        # can't get the schema for a temp table that way.
        return self.read_gbq_table(
            table_id,
            index_col=index_col,
            columns=columns,
        )

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
            return self._read_pandas_load_job(pandas_dataframe, api_name)
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
        except pa.ArrowInvalid as e:
            raise pa.ArrowInvalid(
                f"Could not convert with a BigQuery type: `{e}`. "
            ) from e
        except ValueError:  # Thrown by ibis for some unhandled types
            return None
        except pa.ArrowTypeError:  # Thrown by arrow for types without mapping (geo).
            return None

        inline_types = inline_df._block.expr.schema.dtypes
        # Ibis has problems escaping bytes literals, which will cause syntax errors server-side.
        if all(dtype in INLINABLE_DTYPES for dtype in inline_types):
            return inline_df
        return None

    def _read_pandas_load_job(
        self, pandas_dataframe: pandas.DataFrame, api_name: str
    ) -> dataframe.DataFrame:
        import bigframes.dataframe as dataframe

        col_index = pandas_dataframe.columns.copy()
        col_labels, idx_labels = (
            col_index.to_list(),
            pandas_dataframe.index.names,
        )
        new_col_ids, new_idx_ids = utils.get_standardized_ids(
            col_labels,
            idx_labels,
            # Loading parquet files into BigQuery with special column names
            # is only supported under an allowlist.
            strict=True,
        )

        # Add order column to pandas DataFrame to preserve order in BigQuery
        ordering_col = "rowid"
        columns = frozenset(col_labels + idx_labels)
        suffix = 2
        while ordering_col in columns:
            ordering_col = f"rowid_{suffix}"
            suffix += 1

        pandas_dataframe_copy = pandas_dataframe.copy()
        pandas_dataframe_copy.index.names = new_idx_ids
        pandas_dataframe_copy.columns = pandas.Index(new_col_ids)
        pandas_dataframe_copy[ordering_col] = np.arange(pandas_dataframe_copy.shape[0])

        job_config = self._prepare_load_job_config()

        # Specify the datetime dtypes, which is auto-detected as timestamp types.
        schema: list[bigquery.SchemaField] = []
        for column, dtype in zip(new_col_ids, pandas_dataframe.dtypes):
            if dtype == "timestamp[us][pyarrow]":
                schema.append(
                    bigquery.SchemaField(column, bigquery.enums.SqlTypeNames.DATETIME)
                )
        job_config.schema = schema

        # Clustering probably not needed anyways as pandas tables are small
        cluster_cols = [ordering_col]
        job_config.clustering_fields = cluster_cols

        job_config.labels = {"bigframes-api": api_name}

        load_table_destination = self._random_table()
        load_job = self.bqclient.load_table_from_dataframe(
            pandas_dataframe_copy,
            load_table_destination,
            job_config=job_config,
        )
        self._start_generic_job(load_job)

        destination_table = self.bqclient.get_table(load_table_destination)
        array_value = core.ArrayValue.from_table(
            table=destination_table,
            # TODO: Generate this directly from original pandas df.
            schema=schemata.ArraySchema.from_bq_table(destination_table),
            session=self,
            offsets_col=ordering_col,
        ).drop_columns([ordering_col])

        block = blocks.Block(
            array_value,
            index_columns=new_idx_ids,
            column_labels=col_index,
            index_labels=idx_labels,
        )
        return dataframe.DataFrame(block)

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
        table = self._random_table()

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

            job_config = self._prepare_load_job_config()
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

            return self._read_bigquery_load_job(
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
        table = self._random_table()

        if engine == "bigquery":
            job_config = self._prepare_load_job_config()
            job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED
            job_config.source_format = bigquery.SourceFormat.PARQUET
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_EMPTY
            job_config.labels = {"bigframes-api": "read_parquet"}

            return self._read_bigquery_load_job(path, table, job_config=job_config)
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
        table = self._random_table()

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

            job_config = self._prepare_load_job_config()
            job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED
            job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_EMPTY
            job_config.autodetect = True
            job_config.encoding = encoding
            job_config.labels = {"bigframes-api": "read_json"}

            return self._read_bigquery_load_job(
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
        else:  # local file path
            file_size = os.path.getsize(filepath)

        if file_size > max_size:
            # Convert to GB
            file_size = round(file_size / (1024**3), 1)
            max_size = int(max_size / 1024**3)
            logger.warning(
                f"File size {file_size}GB exceeds {max_size}GB. "
                "It is recommended to use engine='bigquery' "
                "for large files to avoid loading the file into local memory."
            )

    def _create_empty_temp_table(
        self,
        schema: Iterable[bigquery.SchemaField],
        cluster_cols: List[str],
    ) -> bigquery.TableReference:
        # Can't set a table in _SESSION as destination via query job API, so we
        # run DDL, instead.
        expiration = (
            datetime.datetime.now(datetime.timezone.utc) + constants.DEFAULT_EXPIRATION
        )

        table = bf_io_bigquery.create_temp_table(
            self,
            expiration,
            schema=schema,
            cluster_columns=cluster_cols,
        )
        return bigquery.TableReference.from_string(table)

    def _sql_to_temp_table(
        self,
        sql: str,
        cluster_cols: Iterable[str],
        api_name: str,
    ) -> bigquery.TableReference:
        destination, _ = self._query_to_destination(
            sql,
            index_cols=list(cluster_cols),
            api_name=api_name,
        )
        # There should always be a destination table for this query type.
        return typing.cast(bigquery.TableReference, destination)

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
                function and corresponding cloud function (if any) that was
                previously created for the same udf.
                Setting it to `False` would force creating a unique remote function.
                If the required remote function does not exist then it would be
                created irrespective of this param.
            name (str, Optional):
                Explicit name of the persisted BigQuery remote function. Use it with
                caution, because two users working in the same project and dataset
                could overwrite each other's remote functions if they use the same
                persistent name.
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
        Returns:
            callable: A remote function object pointing to the cloud assets created
            in the background to support the remote execution. The cloud assets can be
            located through the following properties set in the object:

            `bigframes_cloud_function` - The google cloud function deployed for the user defined code.

            `bigframes_remote_function` - The bigquery remote function capable of calling into `bigframes_cloud_function`.
        """
        return bigframes_rf(
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
        )

    def read_gbq_function(
        self,
        function_name: str,
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

        Use the ``cw_lower_case_ascii_only`` function from Community UDFs.
        (https://github.com/GoogleCloudPlatform/bigquery-utils/blob/master/udfs/community/cw_lower_case_ascii_only.sqlx)

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'id': [1, 2, 3], 'name': ['AURÉLIE', 'CÉLESTINE', 'DAPHNÉ']})
            >>> df
               id       name
            0   1    AURÉLIE
            1   2  CÉLESTINE
            2   3     DAPHNÉ
            <BLANKLINE>
            [3 rows x 2 columns]

            >>> func = bpd.read_gbq_function("bqutil.fn.cw_lower_case_ascii_only")
            >>> df1 = df.assign(new_name=df['name'].apply(func))
            >>> df1
               id       name   new_name
            0   1    AURÉLIE    aurÉlie
            1   2  CÉLESTINE  cÉlestine
            2   3     DAPHNÉ     daphnÉ
            <BLANKLINE>
            [3 rows x 3 columns]

        Args:
            function_name (str):
                the function's name in BigQuery in the format
                `project_id.dataset_id.function_name`, or
                `dataset_id.function_name` to load from the default project, or
                `function_name` to load from the default project and the dataset
                associated with the current session.

        Returns:
            callable: A function object pointing to the BigQuery function read
            from BigQuery.

            The object is similar to the one created by the `remote_function`
            decorator, including the `bigframes_remote_function` property, but
            not including the `bigframes_cloud_function` property.
        """

        return bigframes_rgf(
            function_name=function_name,
            session=self,
        )

    def _prepare_query_job_config(
        self,
        job_config: Optional[bigquery.QueryJobConfig] = None,
    ) -> bigquery.QueryJobConfig:
        if job_config is None:
            job_config = bigquery.QueryJobConfig()
        else:
            # Create a copy so that we don't mutate the original config passed
            job_config = typing.cast(
                bigquery.QueryJobConfig,
                bigquery.QueryJobConfig.from_api_repr(job_config.to_api_repr()),
            )

        if bigframes.options.compute.maximum_bytes_billed is not None:
            job_config.maximum_bytes_billed = (
                bigframes.options.compute.maximum_bytes_billed
            )

        if self._bq_kms_key_name:
            job_config.destination_encryption_configuration = (
                bigquery.EncryptionConfiguration(kms_key_name=self._bq_kms_key_name)
            )

        return job_config

    def _prepare_load_job_config(self) -> bigquery.LoadJobConfig:
        # Create a copy so that we don't mutate the original config passed
        job_config = bigquery.LoadJobConfig()

        if self._bq_kms_key_name:
            job_config.destination_encryption_configuration = (
                bigquery.EncryptionConfiguration(kms_key_name=self._bq_kms_key_name)
            )

        return job_config

    def _prepare_copy_job_config(self) -> bigquery.CopyJobConfig:
        # Create a copy so that we don't mutate the original config passed
        job_config = bigquery.CopyJobConfig()

        if self._bq_kms_key_name:
            job_config.destination_encryption_configuration = (
                bigquery.EncryptionConfiguration(kms_key_name=self._bq_kms_key_name)
            )

        return job_config

    def _start_query(
        self,
        sql: str,
        job_config: Optional[bigquery.job.QueryJobConfig] = None,
        max_results: Optional[int] = None,
        timeout: Optional[float] = None,
        api_name: Optional[str] = None,
    ) -> Tuple[bigquery.table.RowIterator, bigquery.QueryJob]:
        """
        Starts BigQuery query job and waits for results.
        """
        job_config = self._prepare_query_job_config(job_config)
        try:
            return bigframes.session._io.bigquery.start_query_with_client(
                self,
                sql,
                job_config,
                max_results,
                timeout,
                api_name=api_name,
            )
        except google.api_core.exceptions.BadRequest as e:
            # Unfortunately, this error type does not have a separate error code or exception type
            if "Resources exceeded during query execution" in e.message:
                new_message = "Computation is too complex to execute as a single query. Try using DataFrame.cache() on intermediate results, or setting bigframes.options.compute.enable_multi_query_execution."
                raise bigframes.exceptions.QueryComplexityError(new_message) from e
            else:
                raise

    def _start_query_ml_ddl(
        self,
        sql: str,
    ) -> Tuple[bigquery.table.RowIterator, bigquery.QueryJob]:
        """
        Starts BigQuery ML DDL query job (CREATE MODEL/ALTER MODEL/...) and
        waits for results.
        """
        job_config = self._prepare_query_job_config()

        # BQML expects kms_key_name through OPTIONS and not through job config,
        # so we must reset any encryption set in the job config
        # https://cloud.google.com/bigquery/docs/customer-managed-encryption#encrypt-model
        job_config.destination_encryption_configuration = None

        return bigframes.session._io.bigquery.start_query_with_client(
            self, sql, job_config
        )

    def _cache_with_cluster_cols(
        self, array_value: core.ArrayValue, cluster_cols: typing.Sequence[str]
    ):
        """Executes the query and uses the resulting table to rewrite future executions."""
        # TODO: Use this for all executions? Problem is that caching materializes extra
        # ordering columns
        # TODO: May want to support some partial ordering info even for non-strict ordering mode
        keep_order_info = self._strictly_ordered

        sql, ordering_info = bigframes.core.compile.compile_raw(
            self._with_cached_executions(array_value.node)
        )
        tmp_table = self._sql_to_temp_table(
            sql, cluster_cols=cluster_cols, api_name="cached"
        )
        cached_replacement = array_value.as_cached(
            cache_table=self.bqclient.get_table(tmp_table),
            ordering=ordering_info if keep_order_info else None,
        ).node
        self._cached_executions[array_value.node] = cached_replacement

    def _cache_with_offsets(self, array_value: core.ArrayValue):
        """Executes the query and uses the resulting table to rewrite future executions."""
        # TODO: Use this for all executions? Problem is that caching materializes extra
        # ordering columns
        if not self._strictly_ordered:
            raise ValueError(
                "Caching with offsets only supported in strictly ordered mode."
            )
        offset_column = bigframes.core.guid.generate_guid("bigframes_offsets")
        sql = bigframes.core.compile.compile_unordered(
            self._with_cached_executions(
                array_value.promote_offsets(offset_column).node
            )
        )

        tmp_table = self._sql_to_temp_table(
            sql, cluster_cols=[offset_column], api_name="cached"
        )
        cached_replacement = array_value.as_cached(
            cache_table=self.bqclient.get_table(tmp_table),
            ordering=order.ExpressionOrdering.from_offset_col(offset_column),
        ).node
        self._cached_executions[array_value.node] = cached_replacement

    def _cache_with_session_awareness(self, array_value: core.ArrayValue) -> None:
        # this is the occurence count across the whole session
        forest = [obj._block.expr.node for obj in self.objects]
        # These node types are cheap to re-compute
        target, cluster_cols = bigframes.session.planner.session_aware_cache_plan(
            array_value.node, forest
        )
        if len(cluster_cols) > 0:
            self._cache_with_cluster_cols(core.ArrayValue(target), cluster_cols)
        else:
            self._cache_with_offsets(core.ArrayValue(target))

    def _simplify_with_caching(self, array_value: core.ArrayValue):
        """Attempts to handle the complexity by caching duplicated subtrees and breaking the query into pieces."""
        # Apply existing caching first
        if not bigframes.options.compute.enable_multi_query_execution:
            return

        for _ in range(MAX_SUBTREE_FACTORINGS):
            node_with_cache = self._with_cached_executions(array_value.node)
            if node_with_cache.planning_complexity < QUERY_COMPLEXITY_LIMIT:
                return

            did_cache = self._cache_most_complex_subtree(array_value.node)
            if not did_cache:
                return

    def _cache_most_complex_subtree(self, node: nodes.BigFrameNode) -> bool:
        # TODO: If query fails, retry with lower complexity limit
        selection = traversals.select_cache_target(
            node,
            min_complexity=(QUERY_COMPLEXITY_LIMIT / 500),
            max_complexity=QUERY_COMPLEXITY_LIMIT,
            cache=dict(self._cached_executions),
            # Heuristic: subtree_compleixty * (copies of subtree)^2
            heuristic=lambda complexity, count: math.log(complexity)
            + 2 * math.log(count),
        )
        if selection is None:
            # No good subtrees to cache, just return original tree
            return False

        self._cache_with_cluster_cols(core.ArrayValue(selection), [])
        return True

    def _with_cached_executions(self, node: nodes.BigFrameNode) -> nodes.BigFrameNode:
        return traversals.replace_nodes(node, (dict(self._cached_executions)))

    def _is_trivially_executable(self, array_value: core.ArrayValue):
        """
        Can the block be evaluated very cheaply?
        If True, the array_value probably is not worth caching.
        """
        # Once rewriting is available, will want to rewrite before
        # evaluating execution cost.
        return traversals.is_trivially_executable(
            self._with_cached_executions(array_value.node)
        )

    def _execute(
        self,
        array_value: core.ArrayValue,
        job_config: Optional[bigquery.job.QueryJobConfig] = None,
        *,
        ordered: bool = True,
        dry_run=False,
        col_id_overrides: Mapping[str, str] = {},
    ) -> tuple[bigquery.table.RowIterator, bigquery.QueryJob]:
        if not dry_run:
            self._add_execution(1)
        sql = self._to_sql(
            array_value, ordered=ordered, col_id_overrides=col_id_overrides
        )  # type:ignore
        if job_config is None:
            job_config = bigquery.QueryJobConfig(dry_run=dry_run)
        else:
            job_config.dry_run = dry_run

        # TODO(swast): plumb through the api_name of the user-facing api that
        # caused this query.
        return self._start_query(
            sql=sql,
            job_config=job_config,
        )

    def _peek(
        self, array_value: core.ArrayValue, n_rows: int
    ) -> tuple[bigquery.table.RowIterator, bigquery.QueryJob]:
        """A 'peek' efficiently accesses a small number of rows in the dataframe."""
        if not tree_properties.peekable(self._with_cached_executions(array_value.node)):
            warnings.warn("Peeking this value cannot be done efficiently.")
        sql = bigframes.core.compile.compile_peek(
            self._with_cached_executions(array_value.node), n_rows
        )

        # TODO(swast): plumb through the api_name of the user-facing api that
        # caused this query.
        return self._start_query(
            sql=sql,
        )

    def _to_sql(
        self,
        array_value: core.ArrayValue,
        offset_column: typing.Optional[str] = None,
        col_id_overrides: typing.Mapping[str, str] = {},
        ordered: bool = False,
    ) -> str:
        if offset_column:
            array_value = array_value.promote_offsets(offset_column)
        node_w_cached = self._with_cached_executions(array_value.node)
        if ordered:
            return bigframes.core.compile.compile_ordered(
                node_w_cached, col_id_overrides=col_id_overrides
            )
        return bigframes.core.compile.compile_unordered(
            node_w_cached, col_id_overrides=col_id_overrides
        )

    def _get_table_size(self, destination_table):
        table = self.bqclient.get_table(destination_table)
        return table.num_bytes

    def _rows_to_dataframe(
        self, row_iterator: bigquery.table.RowIterator, dtypes: Dict
    ) -> pandas.DataFrame:
        # Can ignore inferred datatype until dtype emulation breaks 1:1 mapping between BQ types and bigframes types
        dtypes_from_bq = bigframes.dtypes.bf_type_from_type_kind(row_iterator.schema)
        arrow_table = row_iterator.to_arrow()
        return bigframes.session._io.pandas.arrow_to_pandas(arrow_table, dtypes_from_bq)

    def _start_generic_job(self, job: formatting_helpers.GenericJob):
        if bigframes.options.display.progress_bar is not None:
            formatting_helpers.wait_for_job(
                job, bigframes.options.display.progress_bar
            )  # Wait for the job to complete
        else:
            job.result()

    def _random_table(self, skip_cleanup: bool = False) -> bigquery.TableReference:
        """Generate a random table ID with BigQuery DataFrames prefix.

        The generated ID will be stored and checked for deletion when the
        session is closed, unless skip_cleanup is True.

        Args:
            skip_cleanup (bool, default False):
                If True, do not add the generated ID to the list of tables
                to clean up when the session is closed.

        Returns:
            google.cloud.bigquery.TableReference:
                Fully qualified table ID of a table that doesn't exist.
        """
        dataset = self._anonymous_dataset
        session_id = self.session_id
        now = datetime.datetime.now(datetime.timezone.utc)
        random_id = uuid.uuid4().hex
        table_id = _TEMP_TABLE_ID_FORMAT.format(
            date=now.strftime("%Y%m%d"), session_id=session_id, random_id=random_id
        )
        if not skip_cleanup:
            self._table_ids.append(table_id)
        return dataset.table(table_id)


def connect(context: Optional[bigquery_options.BigQueryOptions] = None) -> Session:
    return Session(context)


def _can_cluster_bq(field: bigquery.SchemaField):
    # https://cloud.google.com/bigquery/docs/clustered-tables
    # Notably, float is excluded
    type_ = field.field_type
    return type_ in (
        "INTEGER",
        "INT64",
        "STRING",
        "NUMERIC",
        "DECIMAL",
        "BIGNUMERIC",
        "BIGDECIMAL",
        "DATE",
        "DATETIME",
        "TIMESTAMP",
        "BOOL",
        "BOOLEAN",
    )


def _transform_read_gbq_configuration(configuration: Optional[dict]) -> dict:
    """
    For backwards-compatibility, convert any previously client-side only
    parameters such as timeoutMs to the property name expected by the REST API.

    Makes a copy of configuration if changes are needed.
    """

    if configuration is None:
        return {}

    timeout_ms = configuration.get("query", {}).get("timeoutMs")
    if timeout_ms is not None:
        # Transform timeoutMs to an actual server-side configuration.
        # https://github.com/googleapis/python-bigquery-pandas/issues/479
        configuration = copy.deepcopy(configuration)
        del configuration["query"]["timeoutMs"]
        configuration["jobTimeoutMs"] = timeout_ms

    return configuration
