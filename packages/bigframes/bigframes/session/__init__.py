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

import datetime
import itertools
import logging
import os
import re
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
from bigframes.core import log_adapter
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
import third_party.bigframes_vendored.ibis.expr.operations as vendored_ibis_ops
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

        self._create_bq_datasets()
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
        self._df_snapshot: Dict[bigquery.TableReference, datetime.datetime] = {}

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
    def _project(self):
        return self.bqclient.project

    def __hash__(self):
        # Stable hash needed to use in expression tree
        return hash(str(self._anonymous_dataset))

    def _create_bq_datasets(self):
        """Create and identify dataset(s) for temporary BQ resources."""
        query_job = self.bqclient.query("SELECT 1", location=self._location)
        query_job.result()  # blocks until finished

        # The anonymous dataset is used by BigQuery to write query results and
        # session tables. BigQuery DataFrames also writes temp tables directly
        # to the dataset, no BigQuery Session required. Note: there is a
        # different anonymous dataset per location. See:
        # https://cloud.google.com/bigquery/docs/cached-results#how_cached_results_are_stored
        query_destination = query_job.destination
        self._anonymous_dataset = bigquery.DatasetReference(
            query_destination.project,
            query_destination.dataset_id,
        )

    def close(self):
        """No-op. Temporary resources are deleted after 7 days."""

    def read_gbq(
        self,
        query_or_table: str,
        *,
        index_col: Iterable[str] | str = (),
        col_order: Iterable[str] = (),
        max_results: Optional[int] = None,
        use_cache: bool = True,
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
                use_cache=use_cache,
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
                use_cache=use_cache,
            )

    def _query_to_destination(
        self,
        query: str,
        index_cols: List[str],
        api_name: str,
        use_cache: bool = True,
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
        cluster_cols = [
            item.name
            for item in schema
            if (item.name in index_cols) and _can_cluster_bq(item)
        ][:_MAX_CLUSTER_COLUMNS]
        temp_table = self._create_empty_temp_table(schema, cluster_cols)

        job_config = bigquery.QueryJobConfig()
        job_config.labels["bigframes-api"] = api_name
        job_config.destination = temp_table
        job_config.use_query_cache = use_cache

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
        use_cache: bool = True,
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
        return self._read_gbq_query(
            query=query,
            index_col=index_col,
            col_order=col_order,
            max_results=max_results,
            api_name="read_gbq_query",
            use_cache=use_cache,
        )

    def _read_gbq_query(
        self,
        query: str,
        *,
        index_col: Iterable[str] | str = (),
        col_order: Iterable[str] = (),
        max_results: Optional[int] = None,
        api_name: str = "read_gbq_query",
        use_cache: bool = True,
    ) -> dataframe.DataFrame:
        if isinstance(index_col, str):
            index_cols = [index_col]
        else:
            index_cols = list(index_col)

        destination, query_job = self._query_to_destination(
            query,
            index_cols,
            api_name=api_name,
            use_cache=use_cache,
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
            use_cache=use_cache,
        )

    def read_gbq_table(
        self,
        query: str,
        *,
        index_col: Iterable[str] | str = (),
        col_order: Iterable[str] = (),
        max_results: Optional[int] = None,
        use_cache: bool = True,
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
        return self._read_gbq_table(
            query=query,
            index_col=index_col,
            col_order=col_order,
            max_results=max_results,
            api_name="read_gbq_table",
            use_cache=use_cache,
        )

    def _get_snapshot_sql_and_primary_key(
        self,
        table_ref: bigquery.table.TableReference,
        *,
        api_name: str,
        use_cache: bool = True,
    ) -> Tuple[ibis_types.Table, Optional[Sequence[str]]]:
        """Create a read-only Ibis table expression representing a table.

        If we can get a total ordering from the table, such as via primary key
        column(s), then return those too so that ordering generation can be
        avoided.
        """
        # If there are primary keys defined, the query engine assumes these
        # columns are unique, even if the constraint is not enforced. We make
        # the same assumption and use these columns as the total ordering keys.
        table = self.bqclient.get_table(table_ref)

        if table.location.casefold() != self._location.casefold():
            raise ValueError(
                f"Current session is in {self._location} but dataset '{table.project}.{table.dataset_id}' is located in {table.location}"
            )

        # TODO(b/305264153): Use public properties to fetch primary keys once
        # added to google-cloud-bigquery.
        primary_keys = (
            table._properties.get("tableConstraints", {})
            .get("primaryKey", {})
            .get("columns")
        )

        job_config = bigquery.QueryJobConfig()
        job_config.labels["bigframes-api"] = api_name
        if use_cache and table_ref in self._df_snapshot.keys():
            snapshot_timestamp = self._df_snapshot[table_ref]
        else:
            snapshot_timestamp = list(
                self.bqclient.query(
                    "SELECT CURRENT_TIMESTAMP() AS `current_timestamp`",
                    job_config=job_config,
                ).result()
            )[0][0]
            self._df_snapshot[table_ref] = snapshot_timestamp
        table_expression = self.ibis_client.sql(
            bigframes_io.create_snapshot_sql(table_ref, snapshot_timestamp)
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
        use_cache: bool = True,
    ) -> dataframe.DataFrame:
        if max_results and max_results <= 0:
            raise ValueError("`max_results` should be a positive number.")

        table_ref = bigquery.table.TableReference.from_string(
            query, default_project=self.bqclient.project
        )

        (
            table_expression,
            total_ordering_cols,
        ) = self._get_snapshot_sql_and_primary_key(
            table_ref, api_name=api_name, use_cache=use_cache
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

        for key in index_cols:
            if key not in table_expression.columns:
                raise ValueError(
                    f"Column `{key}` of `index_col` not found in this table."
                )

        if col_order:
            table_expression = table_expression.select([*index_cols, *col_order])

        # If the index is unique and sortable, then we don't need to generate
        # an ordering column.
        ordering = None
        if total_ordering_cols is not None:
            # Note: currently, a table has a total ordering only when the
            # primary key(s) are set on a table. The query engine assumes such
            # columns are unique, even if not enforced.
            ordering = orderings.ExpressionOrdering(
                ordering_value_columns=tuple(
                    core.OrderingColumnReference(column_id)
                    for column_id in total_ordering_cols
                ),
                total_ordering_columns=frozenset(total_ordering_cols),
            )
            column_values = [table_expression[col] for col in table_expression.columns]
            array_value = core.ArrayValue.from_ibis(
                self,
                table_expression,
                columns=column_values,
                hidden_ordering_columns=[],
                ordering=ordering,
            )

        elif len(index_cols) != 0:
            # We have index columns, lets see if those are actually total_order_columns
            ordering = orderings.ExpressionOrdering(
                ordering_value_columns=tuple(
                    [
                        core.OrderingColumnReference(column_id)
                        for column_id in index_cols
                    ]
                ),
                total_ordering_columns=frozenset(index_cols),
            )
            is_total_ordering = self._check_index_uniqueness(
                table_expression, index_cols
            )
            if is_total_ordering:
                column_values = [
                    table_expression[col] for col in table_expression.columns
                ]
                array_value = core.ArrayValue.from_ibis(
                    self,
                    table_expression,
                    columns=column_values,
                    hidden_ordering_columns=[],
                    ordering=ordering,
                )
            else:
                array_value = self._create_total_ordering(table_expression)
        else:
            array_value = self._create_total_ordering(table_expression)

        value_columns = [col for col in array_value.column_ids if col not in index_cols]
        block = blocks.Block(
            array_value,
            index_columns=index_cols,
            column_labels=value_columns,
            index_labels=index_cols,
        )
        if max_results:
            block = block.slice(stop=max_results)
        df = dataframe.DataFrame(block)

        # If user provided index columns, should sort over it
        if len(index_cols) > 0:
            df.sort_index()
        return df

    def _check_index_uniqueness(
        self, table: ibis_types.Table, index_cols: List[str]
    ) -> bool:
        distinct_table = table.select(*index_cols).distinct()
        is_unique_sql = f"""WITH full_table AS (
            {self.ibis_client.compile(table)}
        ),
        distinct_table AS (
            {self.ibis_client.compile(distinct_table)}
        )

        SELECT (SELECT COUNT(*) FROM full_table) AS `total_count`,
        (SELECT COUNT(*) FROM distinct_table) AS `distinct_count`
        """
        results, _ = self._start_query(is_unique_sql)
        row = next(iter(results))

        total_count = row["total_count"]
        distinct_count = row["distinct_count"]
        return total_count == distinct_count

    def _read_bigquery_load_job(
        self,
        filepath_or_buffer: str | IO["bytes"],
        table: Union[bigquery.Table, bigquery.TableReference],
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
            col_order=col_order,
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

        load_table_destination = bigframes_io.random_table(self._anonymous_dataset)
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
        table_expression = self.ibis_client.table(
            load_table_destination.table_id,
            database=f"{load_table_destination.project}.{load_table_destination.dataset_id}",
        )

        # b/297590178 Potentially a bug in bqclient.load_table_from_dataframe(), that only when the DF is empty, the index columns disappear in table_expression.
        if any(
            [new_idx_id not in table_expression.columns for new_idx_id in new_idx_ids]
        ):
            new_idx_ids, idx_labels = [], []

        column_values = [
            table_expression[col]
            for col in table_expression.columns
            if col != ordering_col
        ]
        array_value = core.ArrayValue.from_ibis(
            self,
            table_expression,
            columns=column_values,
            hidden_ordering_columns=[table_expression[ordering_col]],
            ordering=ordering,
        )

        block = blocks.Block(
            array_value,
            index_columns=new_idx_ids,
            column_labels=col_labels,
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
        table = bigframes_io.random_table(self._anonymous_dataset)

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
        table = bigframes_io.random_table(self._anonymous_dataset)

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
        table = bigframes_io.random_table(self._anonymous_dataset)

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

    def _create_empty_temp_table(
        self,
        schema: Iterable[bigquery.SchemaField],
        cluster_cols: List[str],
    ) -> bigquery.TableReference:
        # Can't set a table in _SESSION as destination via query job API, so we
        # run DDL, instead.
        dataset = self._anonymous_dataset
        expiration = (
            datetime.datetime.now(datetime.timezone.utc) + constants.DEFAULT_EXPIRATION
        )

        table = bigframes_io.create_temp_table(
            self.bqclient,
            dataset,
            expiration,
            schema=schema,
            cluster_columns=cluster_cols,
        )
        return bigquery.TableReference.from_string(table)

    def _create_total_ordering(
        self,
        table: ibis_types.Table,
    ) -> core.ArrayValue:
        # Since this might also be used as the index, don't use the default
        # "ordering ID" name.
        ordering_hash_part = guid.generate_guid("bigframes_ordering_")
        ordering_rand_part = guid.generate_guid("bigframes_ordering_")

        # All inputs into hash must be non-null or resulting hash will be null
        str_values = list(
            map(lambda col: _convert_to_nonnull_string(table[col]), table.columns)
        )
        full_row_str = (
            str_values[0].concat(*str_values[1:])
            if len(str_values) > 1
            else str_values[0]
        )
        full_row_hash = full_row_str.hash().name(ordering_hash_part)
        # Used to disambiguate between identical rows (which will have identical hash)
        random_value = ibis.random().name(ordering_rand_part)

        original_column_ids = table.columns
        table_with_ordering = table.select(
            itertools.chain(original_column_ids, [full_row_hash, random_value])
        )

        ordering_ref1 = core.OrderingColumnReference(ordering_hash_part)
        ordering_ref2 = core.OrderingColumnReference(ordering_rand_part)
        ordering = orderings.ExpressionOrdering(
            ordering_value_columns=(ordering_ref1, ordering_ref2),
            total_ordering_columns=frozenset([ordering_hash_part, ordering_rand_part]),
        )
        columns = [table_with_ordering[col] for col in original_column_ids]
        hidden_columns = [
            table_with_ordering[ordering_hash_part],
            table_with_ordering[ordering_rand_part],
        ]
        return core.ArrayValue.from_ibis(
            self,
            table_with_ordering,
            columns,
            hidden_ordering_columns=hidden_columns,
            ordering=ordering,
        )

    def _ibis_to_temp_table(
        self,
        table: ibis_types.Table,
        cluster_cols: Iterable[str],
        api_name: str,
    ) -> bigquery.TableReference:
        destination, _ = self._query_to_destination(
            self.ibis_client.compile(table),
            index_cols=list(cluster_cols),
            api_name=api_name,
        )
        # There should always be a destination table for this query type.
        return typing.cast(bigquery.TableReference, destination)

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
        api_methods = log_adapter.get_and_reset_api_methods()
        job_config.labels = bigframes_io.create_job_configs_labels(
            job_configs_labels=job_config.labels, api_methods=api_methods
        )
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
        if job_config is None:
            job_config = bigquery.QueryJobConfig()
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


def _convert_to_nonnull_string(column: ibis_types.Column) -> ibis_types.StringValue:
    col_type = column.type()
    if (
        col_type.is_numeric()
        or col_type.is_boolean()
        or col_type.is_binary()
        or col_type.is_temporal()
    ):
        result = column.cast(ibis_dtypes.String(nullable=True))
    elif col_type.is_geospatial():
        result = typing.cast(ibis_types.GeoSpatialColumn, column).as_text()
    elif col_type.is_string():
        result = column
    else:
        # TO_JSON_STRING works with all data types, but isn't the most efficient
        # Needed for JSON, STRUCT and ARRAY datatypes
        result = vendored_ibis_ops.ToJsonString(column).to_expr()  # type: ignore
    # Escape backslashes and use backslash as delineator
    escaped = typing.cast(ibis_types.StringColumn, result.fillna("")).replace("\\", "\\\\")  # type: ignore
    return typing.cast(ibis_types.StringColumn, ibis.literal("\\")).concat(escaped)
