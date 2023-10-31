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
import re
import textwrap
import typing
from typing import (
    Any,
    Callable,
    Dict,
    IO,
    Iterable,
    List,
    Literal,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Union,
)
import uuid
import warnings

import google.api_core.client_info
import google.api_core.client_options
import google.api_core.exceptions
import google.api_core.gapic_v1.client_info
import google.auth.credentials
import google.cloud.bigquery as bigquery
import google.cloud.bigquery_connection_v1
import google.cloud.bigquery_storage_v1
import google.cloud.functions_v2
import google.cloud.resourcemanager_v3
import google.cloud.storage as storage  # type: ignore
import ibis
import ibis.backends.bigquery as ibis_bigquery
import ibis.expr.datatypes as ibis_dtypes
import ibis.expr.types as ibis_types
import numpy as np
import pandas
from pandas._typing import (
    CompressionOptions,
    FilePath,
    ReadPickleBuffer,
    StorageOptions,
)

import bigframes._config.bigquery_options as bigquery_options
import bigframes.constants as constants
import bigframes.core as core
import bigframes.core.blocks as blocks
import bigframes.core.guid as guid
from bigframes.core.ordering import IntegerEncoding, OrderingColumnReference
import bigframes.core.ordering as orderings
import bigframes.core.utils as utils
import bigframes.dataframe as dataframe
import bigframes.formatting_helpers as formatting_helpers
from bigframes.remote_function import read_gbq_function as bigframes_rgf
from bigframes.remote_function import remote_function as bigframes_rf
import bigframes.session._io.bigquery as bigframes_io
import bigframes.session.clients
import bigframes.version

# Even though the ibis.backends.bigquery.registry import is unused, it's needed
# to register new and replacement ops with the Ibis BigQuery backend.
import third_party.bigframes_vendored.ibis.backends.bigquery.registry  # noqa
import third_party.bigframes_vendored.pandas.io.gbq as third_party_pandas_gbq
import third_party.bigframes_vendored.pandas.io.parquet as third_party_pandas_parquet
import third_party.bigframes_vendored.pandas.io.parsers.readers as third_party_pandas_readers
import third_party.bigframes_vendored.pandas.io.pickle as third_party_pandas_pickle

_BIGFRAMES_DEFAULT_CONNECTION_ID = "bigframes-default-connection"

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

logger = logging.getLogger(__name__)


def _is_query(query_or_table: str) -> bool:
    """Determine if `query_or_table` is a table ID or a SQL string"""
    return re.search(r"\s", query_or_table.strip(), re.MULTILINE) is not None


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
        clients_provider (bigframes.session.bigframes.session.clients.ClientsProvider):
            An object providing client library objects.
    """

    def __init__(
        self,
        context: Optional[bigquery_options.BigQueryOptions] = None,
        clients_provider: Optional[bigframes.session.clients.ClientsProvider] = None,
    ):
        if context is None:
            context = bigquery_options.BigQueryOptions()

        # TODO(swast): Get location from the environment.
        if context is None or context.location is None:
            self._location = "US"
            warnings.warn(
                f"No explicit location is set, so using location {self._location} for the session.",
                stacklevel=2,
            )
        else:
            self._location = context.location

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
            )

        self._create_and_bind_bq_session()
        self.ibis_client = typing.cast(
            ibis_bigquery.Backend,
            ibis.bigquery.connect(
                project_id=context.project,
                client=self.bqclient,
                storage_client=self.bqstoragereadclient,
            ),
        )

        self._bq_connection = context.bq_connection or _BIGFRAMES_DEFAULT_CONNECTION_ID

        # Now that we're starting the session, don't allow the options to be
        # changed.
        context._session_started = True

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

    @property
    def _session_dataset_id(self):
        """A dataset for storing temporary objects local to the session
        This is a workaround for remote functions that do not
        yet support session-temporary instances."""
        return self._session_dataset.dataset_id

    @property
    def _project(self):
        return self.bqclient.project

    def __hash__(self):
        # Stable hash needed to use in expression tree
        return hash(self._session_id)

    def _create_and_bind_bq_session(self):
        """Create a BQ session and bind the session id with clients to capture BQ activities:
        go/bigframes-transient-data"""
        job_config = bigquery.QueryJobConfig(create_session=True)
        # Make sure the session is a new one, not one associated with another query.
        job_config.use_query_cache = False
        query_job = self.bqclient.query(
            "SELECT 1", job_config=job_config, location=self._location
        )
        query_job.result()  # blocks until finished
        self._session_id = query_job.session_info.session_id

        self.bqclient.default_query_job_config = bigquery.QueryJobConfig(
            connection_properties=[
                bigquery.ConnectionProperty("session_id", self._session_id)
            ]
        )
        self.bqclient.default_load_job_config = bigquery.LoadJobConfig(
            connection_properties=[
                bigquery.ConnectionProperty("session_id", self._session_id)
            ]
        )

        # Dataset for storing remote functions, which don't yet
        # support proper session temporary storage yet
        self._session_dataset = bigquery.Dataset(
            f"{self.bqclient.project}.bigframes_temp_{self._location.lower().replace('-', '_')}"
        )
        self._session_dataset.location = self._location

    def close(self):
        """Terminated the BQ session, otherwises the session will be terminated automatically after
        24 hours of inactivity or after 7 days."""
        if self._session_id is not None and self.bqclient is not None:
            abort_session_query = "CALL BQ.ABORT_SESSION('{}')".format(self._session_id)
            try:
                query_job = self.bqclient.query(abort_session_query)
                query_job.result()  # blocks until finished
            except google.api_core.exceptions.BadRequest as exc:
                # Ignore the exception when the BQ session itself has expired
                # https://cloud.google.com/bigquery/docs/sessions-terminating#auto-terminate_a_session
                if not exc.message.startswith(
                    f"Session {self._session_id} has expired and is no longer available."
                ):
                    raise
            except google.auth.exceptions.RefreshError:
                # The refresh token may itself have been invalidated or expired
                # https://developers.google.com/identity/protocols/oauth2#expiration
                # Don't raise the exception in this case while closing the
                # BigFrames session, so that the end user has a path for getting
                # out of a bad session due to unusable credentials.
                pass
            self._session_id = None

    def read_gbq(
        self,
        query_or_table: str,
        *,
        index_col: Iterable[str] | str = (),
        col_order: Iterable[str] = (),
        max_results: Optional[int] = None,
        # Add a verify index argument that fails if the index is not unique.
    ) -> dataframe.DataFrame:
        # TODO(b/281571214): Generate prompt to show the progress of read_gbq.
        if _is_query(query_or_table):
            return self._read_gbq_query(
                query_or_table,
                index_col=index_col,
                col_order=col_order,
                max_results=max_results,
                api_name="read_gbq",
            )
        else:
            # TODO(swast): Query the snapshot table but mark it as a
            # deterministic query so we can avoid serializing if we have a
            # unique index.
            return self._read_gbq_table(
                query_or_table,
                index_col=index_col,
                col_order=col_order,
                max_results=max_results,
                api_name="read_gbq",
            )

    def _query_to_destination(
        self,
        query: str,
        index_cols: List[str],
        api_name: str,
    ) -> Tuple[Optional[bigquery.TableReference], Optional[bigquery.QueryJob]]:
        # If a dry_run indicates this is not a query type job, then don't
        # bother trying to do a CREATE TEMP TABLE ... AS SELECT ... statement.
        dry_run_config = bigquery.QueryJobConfig()
        dry_run_config.dry_run = True
        _, dry_run_job = self._start_query(query, job_config=dry_run_config)
        if dry_run_job.statement_type != "SELECT":
            _, query_job = self._start_query(query)
            return query_job.destination, query_job

        # Create a table to workaround BigQuery 10 GB query results limit. See:
        # internal issue 303057336.
        # Since we have a `statement_type == 'SELECT'`, schema should be populated.
        schema = typing.cast(Iterable[bigquery.SchemaField], dry_run_job.schema)
        temp_table = self._create_session_table_empty(api_name, schema, index_cols)

        job_config = bigquery.QueryJobConfig()
        job_config.destination = temp_table

        try:
            # Write to temp table to workaround BigQuery 10 GB query results
            # limit. See: internal issue 303057336.
            _, query_job = self._start_query(query, job_config=job_config)
            return query_job.destination, query_job
        except google.api_core.exceptions.BadRequest:
            # Some SELECT statements still aren't compatible with cluster
            # tables as the destination. For example, if the query has a
            # top-level ORDER BY, this conflicts with our ability to cluster
            # the table by the index column(s).
            _, query_job = self._start_query(query)
            return query_job.destination, query_job

    def read_gbq_query(
        self,
        query: str,
        *,
        index_col: Iterable[str] | str = (),
        col_order: Iterable[str] = (),
        max_results: Optional[int] = None,
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
            >>> df.head(2)
              pitcherFirstName pitcherLastName  pitchSpeed
            0                                            0
            1                                            0
            <BLANKLINE>
            [2 rows x 3 columns]

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
        return self._read_gbq_query(
            query=query,
            index_col=index_col,
            col_order=col_order,
            max_results=max_results,
            api_name="read_gbq_query",
        )

    def _read_gbq_query(
        self,
        query: str,
        *,
        index_col: Iterable[str] | str = (),
        col_order: Iterable[str] = (),
        max_results: Optional[int] = None,
        api_name: str,
    ) -> dataframe.DataFrame:
        if isinstance(index_col, str):
            index_cols = [index_col]
        else:
            index_cols = list(index_col)

        destination, query_job = self._query_to_destination(
            query, index_cols, api_name="read_gbq_query"
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

        return self.read_gbq_table(
            f"{destination.project}.{destination.dataset_id}.{destination.table_id}",
            index_col=index_cols,
            col_order=col_order,
            max_results=max_results,
        )

    def read_gbq_table(
        self,
        query: str,
        *,
        index_col: Iterable[str] | str = (),
        col_order: Iterable[str] = (),
        max_results: Optional[int] = None,
    ) -> dataframe.DataFrame:
        """Turn a BigQuery table into a DataFrame.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Read a whole table, with arbitrary ordering or ordering corresponding to the primary key(s).

            >>> df = bpd.read_gbq_table("bigquery-public-data.ml_datasets.penguins")
            >>> df.head(2)
                                                 species island  culmen_length_mm  \\
            0        Adelie Penguin (Pygoscelis adeliae)  Dream              36.6
            1        Adelie Penguin (Pygoscelis adeliae)  Dream              39.8
            <BLANKLINE>
               culmen_depth_mm  flipper_length_mm  body_mass_g     sex
            0             18.4              184.0       3475.0  FEMALE
            1             19.1              184.0       4650.0    MALE
            <BLANKLINE>
            [2 rows x 7 columns]

        See also: :meth:`Session.read_gbq`.
        """
        # NOTE: This method doesn't (yet) exist in pandas or pandas-gbq, so
        # these docstrings are inline.
        return self._read_gbq_table(
            query=query,
            index_col=index_col,
            col_order=col_order,
            max_results=max_results,
            api_name="read_gbq_table",
        )

    def _read_gbq_table_to_ibis_with_total_ordering(
        self,
        table_ref: bigquery.table.TableReference,
        *,
        api_name: str,
    ) -> Tuple[ibis_types.Table, Optional[Sequence[str]]]:
        """Create a read-only Ibis table expression representing a table.

        If we can get a total ordering from the table, such as via primary key
        column(s), then return those too so that ordering generation can be
        avoided.
        """
        if table_ref.dataset_id.upper() == "_SESSION":
            # _SESSION tables aren't supported by the tables.get REST API.
            return (
                self.ibis_client.sql(
                    f"SELECT * FROM `_SESSION`.`{table_ref.table_id}`"
                ),
                None,
            )

        table_expression = self.ibis_client.table(
            table_ref.table_id,
            database=f"{table_ref.project}.{table_ref.dataset_id}",
        )

        # If there are primary keys defined, the query engine assumes these
        # columns are unique, even if the constraint is not enforced. We make
        # the same assumption and use these columns as the total ordering keys.
        table = self.bqclient.get_table(table_ref)

        # TODO(b/305264153): Use public properties to fetch primary keys once
        # added to google-cloud-bigquery.
        primary_keys = (
            table._properties.get("tableConstraints", {})
            .get("primaryKey", {})
            .get("columns")
        )

        if not primary_keys:
            return table_expression, None
        else:
            # Read from a snapshot since we won't have to copy the table data to create a total ordering.
            job_config = bigquery.QueryJobConfig()
            job_config.labels["bigframes-api"] = api_name
            current_timestamp = list(
                self.bqclient.query(
                    "SELECT CURRENT_TIMESTAMP() AS `current_timestamp`",
                    job_config=job_config,
                ).result()
            )[0][0]
            table_expression = self.ibis_client.sql(
                bigframes_io.create_snapshot_sql(table_ref, current_timestamp)
            )
            return table_expression, primary_keys

    def _read_gbq_table(
        self,
        query: str,
        *,
        index_col: Iterable[str] | str = (),
        col_order: Iterable[str] = (),
        max_results: Optional[int] = None,
        api_name: str,
    ) -> dataframe.DataFrame:
        if max_results and max_results <= 0:
            raise ValueError("`max_results` should be a positive number.")

        # TODO(swast): Can we re-use the temp table from other reads in the
        # session, if the original table wasn't modified?
        table_ref = bigquery.table.TableReference.from_string(
            query, default_project=self.bqclient.project
        )

        (
            table_expression,
            total_ordering_cols,
        ) = self._read_gbq_table_to_ibis_with_total_ordering(
            table_ref,
            api_name=api_name,
        )

        for key in col_order:
            if key not in table_expression.columns:
                raise ValueError(
                    f"Column '{key}' of `col_order` not found in this table."
                )

        if isinstance(index_col, str):
            index_cols: List[str] = [index_col]
        else:
            index_cols = list(index_col)

        hidden_cols: typing.Sequence[str] = ()

        for key in index_cols:
            if key not in table_expression.columns:
                raise ValueError(
                    f"Column `{key}` of `index_col` not found in this table."
                )

        # If the index is unique and sortable, then we don't need to generate
        # an ordering column.
        ordering = None
        is_total_ordering = False

        if total_ordering_cols is not None:
            # Note: currently, this a table has a total ordering only when the
            # primary key(s) are set on a table. The query engine assumes such
            # columns are unique, even if not enforced.
            is_total_ordering = True
            ordering = orderings.ExpressionOrdering(
                ordering_value_columns=tuple(
                    [
                        core.OrderingColumnReference(column_id)
                        for column_id in total_ordering_cols
                    ]
                ),
                total_ordering_columns=frozenset(total_ordering_cols),
            )

            if len(index_cols) != 0:
                index_labels = typing.cast(List[Optional[str]], index_cols)
            else:
                # Use the total_ordering_cols to project offsets to use as the default index.
                table_expression = table_expression.order_by(index_cols)
                default_index_id = guid.generate_guid("bigframes_index_")
                default_index_col = (
                    ibis.row_number().cast(ibis_dtypes.int64).name(default_index_id)
                )
                table_expression = table_expression.mutate(
                    **{default_index_id: default_index_col}
                )
                index_cols = [default_index_id]
                index_labels = [None]
        elif len(index_cols) != 0:
            index_labels = typing.cast(List[Optional[str]], index_cols)
            distinct_table = table_expression.select(*index_cols).distinct()
            is_unique_sql = f"""WITH full_table AS (
                {self.ibis_client.compile(table_expression)}
            ),
            distinct_table AS (
                {self.ibis_client.compile(distinct_table)}
            )

            SELECT (SELECT COUNT(*) FROM full_table) AS `total_count`,
            (SELECT COUNT(*) FROM distinct_table) AS `distinct_count`
            """
            results, query_job = self._start_query(is_unique_sql)
            row = next(iter(results))

            total_count = row["total_count"]
            distinct_count = row["distinct_count"]
            is_total_ordering = total_count == distinct_count

            ordering = orderings.ExpressionOrdering(
                ordering_value_columns=tuple(
                    [
                        core.OrderingColumnReference(column_id)
                        for column_id in index_cols
                    ]
                ),
                total_ordering_columns=frozenset(index_cols),
            )

            # We have a total ordering, so query via "time travel" so that
            # the underlying data doesn't mutate.
            if is_total_ordering:
                # Get the timestamp from the job metadata rather than the query
                # text so that the query for determining uniqueness of the ID
                # columns can be cached.
                current_timestamp = query_job.started

                # The job finished, so we should have a start time.
                assert current_timestamp is not None
                table_expression = self.ibis_client.sql(
                    bigframes_io.create_snapshot_sql(table_ref, current_timestamp)
                )
            else:
                # Make sure when we generate an ordering, the row_number()
                # coresponds to the index columns.
                table_expression = table_expression.order_by(index_cols)
                warnings.warn(
                    textwrap.dedent(
                        f"""
                        Got a non-unique index. A consistent ordering is not
                        guaranteed. DataFrame has {total_count} rows,
                        but only {distinct_count} distinct index values.
                        """,
                    )
                )

            # When ordering by index columns, apply limit after ordering to
            # make limit more predictable.
            if max_results is not None:
                table_expression = table_expression.limit(max_results)
        else:
            if max_results is not None:
                # Apply limit before generating rownums and creating temp table
                # This makes sure the offsets are valid and limits the number of
                # rows for which row numbers must be generated
                table_expression = table_expression.limit(max_results)
            table_expression, ordering = self._create_sequential_ordering(
                table=table_expression,
                api_name=api_name,
            )
            hidden_cols = (
                (ordering.total_order_col.column_id,)
                if ordering.total_order_col
                else ()
            )
            assert len(ordering.ordering_value_columns) > 0
            is_total_ordering = True
            # Block constructor will generate default index if passed empty
            index_cols = []
            index_labels = []

        return self._read_gbq_with_ordering(
            table_expression=table_expression,
            col_order=col_order,
            index_cols=index_cols,
            index_labels=index_labels,
            hidden_cols=hidden_cols,
            ordering=ordering,
            is_total_ordering=is_total_ordering,
            api_name=api_name,
        )

    def _read_gbq_with_ordering(
        self,
        table_expression: ibis_types.Table,
        *,
        col_order: Iterable[str] = (),
        col_labels: Iterable[Optional[str]] = (),
        index_cols: Iterable[str] = (),
        index_labels: Iterable[Optional[str]] = (),
        hidden_cols: Iterable[str] = (),
        ordering: orderings.ExpressionOrdering,
        is_total_ordering: bool = False,
        api_name: str,
    ) -> dataframe.DataFrame:
        """Internal helper method that loads DataFrame from Google BigQuery given an ordering column.

        Args:
            table_expression:
                an ibis table expression to be executed in BigQuery.
            col_order:
                List of BigQuery column ids in the desired order for results DataFrame.
            col_labels:
                List of column labels as the column names.
            index_cols:
                List of index ids to use as the index or multi-index.
            index_labels:
                List of index labels as names of index.
            hidden_cols:
                Columns that should be hidden. Ordering columns may (not always) be hidden
            ordering:
                Column name to be used for ordering. If not supplied, a default ordering is generated.
            api_name:
                The name of the API method.

        Returns:
            A DataFrame representing results of the query or table.
        """
        index_cols, index_labels = list(index_cols), list(index_labels)
        if len(index_cols) != len(index_labels):
            raise ValueError(
                "Needs same number of index labels are there are index columns. "
                f"Got {len(index_labels)}, expected {len(index_cols)}."
            )

        # Logic:
        # no total ordering, index -> create sequential order, ordered by index, use for both ordering and index
        # total ordering, index -> use ordering as ordering, index as index

        # This code block ensures the existence of a total ordering.
        column_keys = list(col_order)
        if len(column_keys) == 0:
            non_value_columns = set([*index_cols, *hidden_cols])
            column_keys = [
                key for key in table_expression.columns if key not in non_value_columns
            ]
        if not is_total_ordering:
            # Rows are not ordered, we need to generate a default ordering and materialize it
            table_expression, ordering = self._create_sequential_ordering(
                table=table_expression,
                index_cols=index_cols,
                api_name=api_name,
            )
        index_col_values = [table_expression[index_id] for index_id in index_cols]
        if not col_labels:
            col_labels = column_keys
        return self._read_ibis(
            table_expression,
            index_col_values,
            index_labels,
            column_keys,
            col_labels,
            ordering=ordering,
        )

    def _read_bigquery_load_job(
        self,
        filepath_or_buffer: str | IO["bytes"],
        table: bigquery.Table,
        *,
        job_config: bigquery.LoadJobConfig,
        index_col: Iterable[str] | str = (),
        col_order: Iterable[str] = (),
    ) -> dataframe.DataFrame:
        if isinstance(index_col, str):
            index_cols = [index_col]
        else:
            index_cols = list(index_col)

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

        # The BigQuery REST API for tables.get doesn't take a session ID, so we
        # can't get the schema for a temp table that way.
        return self.read_gbq_table(
            f"{table.project}.{table.dataset_id}.{table.table_id}",
            index_col=index_col,
            col_order=col_order,
        )

    def _read_ibis(
        self,
        table_expression: ibis_types.Table,
        index_cols: Iterable[ibis_types.Value],
        index_labels: Iterable[blocks.Label],
        column_keys: Iterable[str],
        column_labels: Iterable[blocks.Label],
        ordering: orderings.ExpressionOrdering,
    ) -> dataframe.DataFrame:
        """Turns a table expression (plus index column) into a DataFrame."""

        columns = list(index_cols)
        for key in column_keys:
            if key not in table_expression.columns:
                raise ValueError(f"Column '{key}' not found in this table.")
            columns.append(table_expression[key])

        non_hidden_ids = [col.get_name() for col in columns]
        hidden_ordering_columns = []
        for ref in ordering.all_ordering_columns:
            if ref.column_id not in non_hidden_ids:
                hidden_ordering_columns.append(table_expression[ref.column_id])

        block = blocks.Block(
            core.ArrayValue.from_ibis(
                self, table_expression, columns, hidden_ordering_columns, ordering
            ),
            index_columns=[index_col.get_name() for index_col in index_cols],
            column_labels=column_labels,
            index_labels=index_labels,
        )

        return dataframe.DataFrame(block)

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
            A bigframes.ml Model wrapping the model.
        """
        import bigframes.ml.loader

        model_ref = bigquery.ModelReference.from_string(
            model_name, default_project=self.bqclient.project
        )
        model = self.bqclient.get_model(model_ref)
        return bigframes.ml.loader.from_bq(self, model)

    def read_pandas(self, pandas_dataframe: pandas.DataFrame) -> dataframe.DataFrame:
        """Loads DataFrame from a pandas DataFrame.

        The pandas DataFrame will be persisted as a temporary BigQuery table, which can be
        automatically recycled after the Session is closed.

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
            pandas_dataframe (pandas.DataFrame):
                a pandas DataFrame object to be loaded.

        Returns:
            bigframes.dataframe.DataFrame: The BigQuery DataFrame.
        """
        return self._read_pandas(pandas_dataframe, "read_pandas")

    def _read_pandas(
        self, pandas_dataframe: pandas.DataFrame, api_name: str
    ) -> dataframe.DataFrame:
        col_labels, idx_labels = (
            pandas_dataframe.columns.to_list(),
            pandas_dataframe.index.names,
        )
        new_col_ids, new_idx_ids = utils.get_standardized_ids(col_labels, idx_labels)

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

        # Specify the datetime dtypes, which is auto-detected as timestamp types.
        schema: list[bigquery.SchemaField] = []
        for column, dtype in zip(pandas_dataframe.columns, pandas_dataframe.dtypes):
            if dtype == "timestamp[us][pyarrow]":
                schema.append(
                    bigquery.SchemaField(column, bigquery.enums.SqlTypeNames.DATETIME)
                )

        # Clustering probably not needed anyways as pandas tables are small
        cluster_cols = [ordering_col]

        job_config = bigquery.LoadJobConfig(schema=schema)
        job_config.clustering_fields = cluster_cols
        job_config.labels = {"bigframes-api": api_name}

        load_table_destination = self._create_session_table()
        load_job = self.bqclient.load_table_from_dataframe(
            pandas_dataframe_copy,
            load_table_destination,
            job_config=job_config,
        )
        self._start_generic_job(load_job)

        ordering = orderings.ExpressionOrdering(
            ordering_value_columns=tuple([OrderingColumnReference(ordering_col)]),
            total_ordering_columns=frozenset([ordering_col]),
            integer_encoding=IntegerEncoding(True, is_sequential=True),
        )
        table_expression = self.ibis_client.sql(
            f"SELECT * FROM `{load_table_destination.table_id}`"
        )

        # b/297590178 Potentially a bug in bqclient.load_table_from_dataframe(), that only when the DF is empty, the index columns disappear in table_expression.
        if any(
            [new_idx_id not in table_expression.columns for new_idx_id in new_idx_ids]
        ):
            new_idx_ids, idx_labels = [], []

        df = self._read_gbq_with_ordering(
            table_expression=table_expression,
            col_labels=col_labels,
            index_cols=new_idx_ids,
            index_labels=idx_labels,
            hidden_cols=(ordering_col,),
            ordering=ordering,
            is_total_ordering=True,
            api_name=api_name,
        )
        return df

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
            Union[int, str, Sequence[Union[str, int]], Literal[False]]
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
        table = bigquery.Table(self._create_session_table())

        if engine is not None and engine == "bigquery":
            if any(param is not None for param in (dtype, names)):
                not_supported = ("dtype", "names")
                raise NotImplementedError(
                    f"BigQuery engine does not support these arguments: {not_supported}. "
                    f"{constants.FEEDBACK_LINK}"
                )

            if index_col is not None and (
                not index_col or not isinstance(index_col, str)
            ):
                raise NotImplementedError(
                    "BigQuery engine only supports a single column name for `index_col`. "
                    f"{constants.FEEDBACK_LINK}"
                )

            # None value for index_col cannot be passed to read_gbq
            if index_col is None:
                index_col = ()

            # usecols should only be an iterable of strings (column names) for use as col_order in read_gbq.
            col_order: Tuple[Any, ...] = tuple()
            if usecols is not None:
                if isinstance(usecols, Iterable) and all(
                    isinstance(col, str) for col in usecols
                ):
                    col_order = tuple(col for col in usecols)
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

            return self._read_bigquery_load_job(
                filepath_or_buffer,
                table,
                job_config=job_config,
                index_col=index_col,
                col_order=col_order,
            )
        else:
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
                usecols=usecols,
                dtype=dtype,
                engine=engine,
                encoding=encoding,
                **kwargs,
            )
            return self.read_pandas(pandas_df)

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
            bigframes_df = self.read_pandas(pandas_obj.to_frame())
            return bigframes_df[bigframes_df.columns[0]]
        return self._read_pandas(pandas_obj, "read_pickle")

    def read_parquet(
        self,
        path: str | IO["bytes"],
    ) -> dataframe.DataFrame:
        # Note: "engine" is omitted because it is redundant. Loading a table
        # from a pandas DataFrame will just create another parquet file + load
        # job anyway.
        table = bigquery.Table(self._create_session_table())

        job_config = bigquery.LoadJobConfig()
        job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED
        job_config.source_format = bigquery.SourceFormat.PARQUET
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_EMPTY
        job_config.labels = {"bigframes-api": "read_parquet"}

        return self._read_bigquery_load_job(path, table, job_config=job_config)

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
        table = bigquery.Table(self._create_session_table())

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
            return self.read_pandas(pandas_df)

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

    def _create_session_table(self) -> bigquery.TableReference:
        table_name = f"{uuid.uuid4().hex}"
        dataset = bigquery.Dataset(
            bigquery.DatasetReference(self.bqclient.project, "_SESSION")
        )
        return dataset.table(table_name)

    def _create_session_table_empty(
        self,
        api_name: str,
        schema: Iterable[bigquery.SchemaField],
        cluster_cols: List[str],
    ) -> bigquery.TableReference:
        # Can't set a table in _SESSION as destination via query job API, so we
        # run DDL, instead.
        table = self._create_session_table()
        schema_sql = bigframes_io.bq_schema_to_sql(schema)

        clusterable_cols = [
            col.name
            for col in schema
            if col.name in cluster_cols and _can_cluster_bq(col)
        ][:_MAX_CLUSTER_COLUMNS]

        if clusterable_cols:
            cluster_cols_sql = ", ".join(
                f"`{cluster_col}`" for cluster_col in clusterable_cols
            )
            cluster_sql = f"CLUSTER BY {cluster_cols_sql}"
        else:
            cluster_sql = ""

        ddl_text = f"""
        CREATE TEMP TABLE
        `_SESSION`.`{table.table_id}`
        ({schema_sql})
        {cluster_sql}
        """

        job_config = bigquery.QueryJobConfig()

        # Include a label so that Dataplex Lineage can identify temporary
        # tables that BigQuery DataFrames creates. Googlers: See internal issue
        # 296779699. We're labeling the job instead of the table because
        # otherwise we get `BadRequest: 400 OPTIONS on temporary tables are not
        # supported`.
        job_config.labels = {"source": "bigquery-dataframes-temp"}
        job_config.labels["bigframes-api"] = api_name

        _, query_job = self._start_query(ddl_text, job_config=job_config)

        # Use fully-qualified name instead of `_SESSION` name so that the
        # created table can be used as the destination table.
        return query_job.destination

    def _create_sequential_ordering(
        self,
        table: ibis_types.Table,
        index_cols: Iterable[str] = (),
        api_name: str = "",
    ) -> Tuple[ibis_types.Table, orderings.ExpressionOrdering]:
        # Since this might also be used as the index, don't use the default
        # "ordering ID" name.
        default_ordering_name = guid.generate_guid("bigframes_ordering_")
        default_ordering_col = (
            ibis.row_number().cast(ibis_dtypes.int64).name(default_ordering_name)
        )
        table = table.mutate(**{default_ordering_name: default_ordering_col})
        table_ref = self._ibis_to_session_table(
            table,
            cluster_cols=list(index_cols) + [default_ordering_name],
            api_name=api_name,
        )
        table = self.ibis_client.table(
            f"{table_ref.project}.{table_ref.dataset_id}.{table_ref.table_id}"
        )
        ordering_reference = core.OrderingColumnReference(default_ordering_name)
        ordering = orderings.ExpressionOrdering(
            ordering_value_columns=tuple([ordering_reference]),
            total_ordering_columns=frozenset([default_ordering_name]),
            integer_encoding=IntegerEncoding(is_encoded=True, is_sequential=True),
        )
        return table, ordering

    def _ibis_to_session_table(
        self,
        table: ibis_types.Table,
        cluster_cols: Iterable[str],
        api_name: str,
    ) -> bigquery.TableReference:
        desination, _ = self._query_to_destination(
            self.ibis_client.compile(table),
            index_cols=list(cluster_cols),
            api_name=api_name,
        )
        # There should always be a destination table for this query type.
        return typing.cast(bigquery.TableReference, desination)

    def remote_function(
        self,
        input_types: List[type],
        output_type: type,
        dataset: Optional[str] = None,
        bigquery_connection: Optional[str] = None,
        reuse: bool = True,
        name: Optional[str] = None,
        packages: Optional[Sequence[str]] = None,
    ):
        """Decorator to turn a user defined function into a BigQuery remote function. Check out
        the code samples at: https://cloud.google.com/bigquery/docs/remote-functions#bigquery-dataframes.

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
            input_types (list(type)):
                List of input data types in the user defined function.
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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> function_name = "bqutil.fn.cw_lower_case_ascii_only"
            >>> func = bpd.read_gbq_function(function_name=function_name)
            >>> func.bigframes_remote_function
            'bqutil.fn.cw_lower_case_ascii_only'

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

    def _start_query(
        self,
        sql: str,
        job_config: Optional[bigquery.job.QueryJobConfig] = None,
        max_results: Optional[int] = None,
    ) -> Tuple[bigquery.table.RowIterator, bigquery.QueryJob]:
        """
        Starts query job and waits for results.
        """
        job_config = self._prepare_job_config(job_config)
        query_job = self.bqclient.query(sql, job_config=job_config)

        opts = bigframes.options.display
        if opts.progress_bar is not None and not query_job.configuration.dry_run:
            results_iterator = formatting_helpers.wait_for_query_job(
                query_job, max_results, opts.progress_bar
            )
        else:
            results_iterator = query_job.result(max_results=max_results)
        return results_iterator, query_job

    def _get_table_size(self, destination_table):
        table = self.bqclient.get_table(destination_table)
        return table.num_bytes

    def _rows_to_dataframe(
        self, row_iterator: bigquery.table.RowIterator, dtypes: Dict
    ) -> pandas.DataFrame:
        arrow_table = row_iterator.to_arrow()
        return bigframes.session._io.pandas.arrow_to_pandas(arrow_table, dtypes)

    def _start_generic_job(self, job: formatting_helpers.GenericJob):
        if bigframes.options.display.progress_bar is not None:
            formatting_helpers.wait_for_job(
                job, bigframes.options.display.progress_bar
            )  # Wait for the job to complete
        else:
            job.result()

    def _prepare_job_config(
        self, job_config: Optional[bigquery.QueryJobConfig] = None
    ) -> bigquery.QueryJobConfig:
        if job_config is None:
            job_config = self.bqclient.default_query_job_config
        if bigframes.options.compute.maximum_bytes_billed is not None:
            job_config.maximum_bytes_billed = (
                bigframes.options.compute.maximum_bytes_billed
            )
        return job_config


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
