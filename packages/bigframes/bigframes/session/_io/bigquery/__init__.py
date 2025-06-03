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

"""Private module: Helpers for BigQuery I/O operations."""

from __future__ import annotations

import datetime
import itertools
import re
import textwrap
import types
import typing
from typing import Dict, Iterable, Literal, Mapping, Optional, overload, Tuple, Union

import bigframes_vendored.pandas.io.gbq as third_party_pandas_gbq
import google.api_core.exceptions
import google.cloud.bigquery as bigquery

from bigframes.core import log_adapter
import bigframes.core.compile.googlesql as googlesql
import bigframes.core.sql
import bigframes.formatting_helpers as formatting_helpers
import bigframes.session.metrics

CHECK_DRIVE_PERMISSIONS = "\nCheck https://cloud.google.com/bigquery/docs/query-drive-data#Google_Drive_permissions."


IO_ORDERING_ID = "bqdf_row_nums"
_LIST_TABLES_LIMIT = 10000  # calls to bqclient.list_tables
# will be limited to this many tables

_MAX_CLUSTER_COLUMNS = 4


def create_job_configs_labels(
    job_configs_labels: Optional[Dict[str, str]],
    api_methods: typing.List[str],
) -> Dict[str, str]:
    if job_configs_labels is None:
        job_configs_labels = {}

    # If the user has labels they wish to set, make sure we set those first so
    # they are preserved.
    for key, value in bigframes.options.compute.extra_query_labels.items():
        job_configs_labels[key] = value

    if api_methods and "bigframes-api" not in job_configs_labels:
        job_configs_labels["bigframes-api"] = api_methods[0]
        del api_methods[0]

    # Make sure we always populate bigframes-api with _something_, even if we
    # have a code path which doesn't populate the list of api_methods. See
    # internal issue 336521938.
    job_configs_labels.setdefault("bigframes-api", "unknown")

    labels = list(
        itertools.chain(
            job_configs_labels.keys(),
            (f"recent-bigframes-api-{i}" for i in range(len(api_methods))),
        )
    )
    values = list(itertools.chain(job_configs_labels.values(), api_methods))
    return dict(
        zip(
            labels[: log_adapter.MAX_LABELS_COUNT],
            values[: log_adapter.MAX_LABELS_COUNT],
        )
    )


def create_export_data_statement(
    table_id: str, uri: str, format: str, export_options: Dict[str, Union[bool, str]]
) -> str:
    all_options: Dict[str, Union[bool, str]] = {
        "uri": uri,
        "format": format.upper(),
        # TODO(swast): Does pandas have an option not to overwrite files?
        "overwrite": True,
    }
    all_options.update(export_options)
    export_options_str = ", ".join(
        format_option(key, value) for key, value in all_options.items()
    )
    # Manually generate ORDER BY statement since ibis will not always generate
    # it in the top level statement. This causes BigQuery to then run
    # non-distributed sort and run out of memory.
    return textwrap.dedent(
        f"""
        EXPORT DATA
        OPTIONS (
            {export_options_str}
        ) AS
        SELECT * EXCEPT ({IO_ORDERING_ID})
        FROM `{table_id}`
        ORDER BY {IO_ORDERING_ID}
        """
    )


def table_ref_to_sql(table: bigquery.TableReference) -> str:
    """Format a table reference as escaped SQL."""
    return f"`{table.project}`.`{table.dataset_id}`.`{table.table_id}`"


def create_temp_table(
    bqclient: bigquery.Client,
    table_ref: bigquery.TableReference,
    expiration: datetime.datetime,
    *,
    schema: Optional[Iterable[bigquery.SchemaField]] = None,
    cluster_columns: Optional[list[str]] = None,
    kms_key: Optional[str] = None,
) -> str:
    """Create an empty table with an expiration in the desired session.

    The table will be deleted when the session is closed or the expiration
    is reached.
    """
    destination = bigquery.Table(table_ref)
    destination.expires = expiration
    destination.schema = schema
    if cluster_columns:
        destination.clustering_fields = cluster_columns
    if kms_key:
        destination.encryption_configuration = bigquery.EncryptionConfiguration(
            kms_key_name=kms_key
        )
    # Ok if already exists, since this will only happen from retries internal to this method
    # as the requested table id has a random UUID4 component.
    bqclient.create_table(destination, exists_ok=True)
    return f"{table_ref.project}.{table_ref.dataset_id}.{table_ref.table_id}"


def create_temp_view(
    bqclient: bigquery.Client,
    table_ref: bigquery.TableReference,
    *,
    expiration: datetime.datetime,
    sql: str,
) -> str:
    """Create an empty table with an expiration in the desired session.

    The table will be deleted when the session is closed or the expiration
    is reached.
    """
    destination = bigquery.Table(table_ref)
    destination.expires = expiration
    destination.view_query = sql

    # Ok if already exists, since this will only happen from retries internal to this method
    # as the requested table id has a random UUID4 component.
    bqclient.create_table(destination, exists_ok=True)
    return f"{table_ref.project}.{table_ref.dataset_id}.{table_ref.table_id}"


def set_table_expiration(
    bqclient: bigquery.Client,
    table_ref: bigquery.TableReference,
    expiration: datetime.datetime,
) -> None:
    """Set an expiration time for an existing BigQuery table."""
    table = bqclient.get_table(table_ref)
    table.expires = expiration
    bqclient.update_table(table, ["expires"])


# BigQuery REST API returns types in Legacy SQL format
# https://cloud.google.com/bigquery/docs/data-types but we use Standard SQL
# names
# https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types
BQ_STANDARD_TYPES = types.MappingProxyType(
    {
        "BOOLEAN": "BOOL",
        "INTEGER": "INT64",
        "FLOAT": "FLOAT64",
    }
)


def bq_field_to_type_sql(field: bigquery.SchemaField):
    if field.mode == "REPEATED":
        nested_type = bq_field_to_type_sql(
            bigquery.SchemaField(
                field.name, field.field_type, mode="NULLABLE", fields=field.fields
            )
        )
        return f"ARRAY<{nested_type}>"

    if field.field_type == "RECORD":
        nested_fields_sql = ", ".join(
            bq_field_to_sql(child_field) for child_field in field.fields
        )
        return f"STRUCT<{nested_fields_sql}>"

    type_ = field.field_type
    return BQ_STANDARD_TYPES.get(type_, type_)


def bq_field_to_sql(field: bigquery.SchemaField):
    name = field.name
    type_ = bq_field_to_type_sql(field)
    return f"`{name}` {type_}"


def bq_schema_to_sql(schema: Iterable[bigquery.SchemaField]):
    return ", ".join(bq_field_to_sql(field) for field in schema)


def format_option(key: str, value: Union[bool, str]) -> str:
    if isinstance(value, bool):
        return f"{key}=true" if value else f"{key}=false"
    return f"{key}={repr(value)}"


def add_and_trim_labels(job_config):
    """
    Add additional labels to the job configuration and trim the total number of labels
    to ensure they do not exceed MAX_LABELS_COUNT labels per job.
    """
    api_methods = log_adapter.get_and_reset_api_methods(dry_run=job_config.dry_run)
    job_config.labels = create_job_configs_labels(
        job_configs_labels=job_config.labels,
        api_methods=api_methods,
    )


@overload
def start_query_with_client(
    bq_client: bigquery.Client,
    sql: str,
    *,
    job_config: bigquery.QueryJobConfig,
    location: Optional[str],
    project: Optional[str],
    timeout: Optional[float],
    metrics: Optional[bigframes.session.metrics.ExecutionMetrics] = None,
    query_with_job: Literal[True],
) -> Tuple[bigquery.table.RowIterator, bigquery.QueryJob]:
    ...


@overload
def start_query_with_client(
    bq_client: bigquery.Client,
    sql: str,
    *,
    job_config: bigquery.QueryJobConfig,
    location: Optional[str],
    project: Optional[str],
    timeout: Optional[float],
    metrics: Optional[bigframes.session.metrics.ExecutionMetrics] = None,
    query_with_job: Literal[False],
) -> Tuple[bigquery.table.RowIterator, Optional[bigquery.QueryJob]]:
    ...


def start_query_with_client(
    bq_client: bigquery.Client,
    sql: str,
    *,
    job_config: bigquery.QueryJobConfig,
    location: Optional[str] = None,
    project: Optional[str] = None,
    timeout: Optional[float] = None,
    metrics: Optional[bigframes.session.metrics.ExecutionMetrics] = None,
    query_with_job: bool = True,
) -> Tuple[bigquery.table.RowIterator, Optional[bigquery.QueryJob]]:
    """
    Starts query job and waits for results.
    """
    try:
        # Note: Ensure no additional labels are added to job_config after this
        # point, as `add_and_trim_labels` ensures the label count does not
        # exceed MAX_LABELS_COUNT.
        add_and_trim_labels(job_config)
        if not query_with_job:
            results_iterator = bq_client.query_and_wait(
                sql,
                job_config=job_config,
                location=location,
                project=project,
                api_timeout=timeout,
            )
            if metrics is not None:
                metrics.count_job_stats(row_iterator=results_iterator)
            return results_iterator, None

        query_job = bq_client.query(
            sql,
            job_config=job_config,
            location=location,
            project=project,
            timeout=timeout,
        )
    except google.api_core.exceptions.Forbidden as ex:
        if "Drive credentials" in ex.message:
            ex.message += CHECK_DRIVE_PERMISSIONS
        raise

    opts = bigframes.options.display
    if opts.progress_bar is not None and not query_job.configuration.dry_run:
        results_iterator = formatting_helpers.wait_for_query_job(
            query_job,
            progress_bar=opts.progress_bar,
        )
    else:
        results_iterator = query_job.result()

    if metrics is not None:
        metrics.count_job_stats(query_job=query_job)
    return results_iterator, query_job


def delete_tables_matching_session_id(
    client: bigquery.Client, dataset: bigquery.DatasetReference, session_id: str
) -> None:
    """Searches within the dataset for tables conforming to the
    expected session_id form, and instructs bigquery to delete them.

    Args:
        client (bigquery.Client):
            The client to use to list tables
        dataset (bigquery.DatasetReference):
            The dataset to search in
        session_id (str):
            The session id to match on in the table name

    Returns:
        None
    """

    tables = client.list_tables(
        dataset, max_results=_LIST_TABLES_LIMIT, page_size=_LIST_TABLES_LIMIT
    )
    for table in tables:
        split_id = table.table_id.split("_")
        if not split_id[0].startswith("bqdf") or len(split_id) < 2:
            continue
        found_session_id = split_id[1]
        if found_session_id == session_id:
            client.delete_table(table, not_found_ok=True)
            print("Deleting temporary table '{}'.".format(table.table_id))


def create_bq_dataset_reference(
    bq_client: bigquery.Client,
    location: Optional[str] = None,
    project: Optional[str] = None,
) -> bigquery.DatasetReference:
    """Create and identify dataset(s) for temporary BQ resources.

    bq_client project and location will be used unless kwargs "project"
    and/or "location" are given. If given, location and project
    will be passed through to
    https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client#google_cloud_bigquery_client_Client_query

    Args:
        bq_client (bigquery.Client):
            The bigquery.Client to use for the http request to
            create the dataset reference.
        location (str, default None):
            The location of the project to create the dataset in.
        project (str, default None):
            The project id of the project to create the dataset in.

    Returns:
        bigquery.DatasetReference: The constructed reference to the anonymous dataset.
    """
    job_config = google.cloud.bigquery.QueryJobConfig()

    _, query_job = start_query_with_client(
        bq_client,
        "SELECT 1",
        location=location,
        job_config=job_config,
        project=project,
        timeout=None,
        metrics=None,
        query_with_job=True,
    )

    # The anonymous dataset is used by BigQuery to write query results and
    # session tables. BigQuery DataFrames also writes temp tables directly
    # to the dataset, no BigQuery Session required. Note: there is a
    # different anonymous dataset per location. See:
    # https://cloud.google.com/bigquery/docs/cached-results#how_cached_results_are_stored
    query_destination = query_job.destination
    return bigquery.DatasetReference(
        query_destination.project,
        query_destination.dataset_id,
    )


def is_query(query_or_table: str) -> bool:
    """Determine if `query_or_table` is a table ID or a SQL string"""
    return re.search(r"\s", query_or_table.strip(), re.MULTILINE) is not None


def is_table_with_wildcard_suffix(query_or_table: str) -> bool:
    """Determine if `query_or_table` is a table and contains a wildcard suffix."""
    return not is_query(query_or_table) and query_or_table.endswith("*")


def to_query(
    query_or_table: str,
    columns: Iterable[str],
    sql_predicate: Optional[str],
    max_results: Optional[int] = None,
    time_travel_timestamp: Optional[datetime.datetime] = None,
) -> str:
    """Compile query_or_table with conditions(filters, wildcards) to query."""
    sub_query = (
        f"({query_or_table})" if is_query(query_or_table) else f"`{query_or_table}`"
    )

    # TODO(b/338111344): Generate an index based on DefaultIndexKind if we
    # don't have index columns specified.
    if columns:
        # We only reduce the selection if columns is set, but we always
        # want to make sure index_cols is also included.
        select_clause = "SELECT " + ", ".join(f"`{column}`" for column in columns)
    else:
        select_clause = "SELECT *"

    time_travel_clause = ""
    if time_travel_timestamp is not None:
        time_travel_literal = bigframes.core.sql.simple_literal(time_travel_timestamp)
        time_travel_clause = f" FOR SYSTEM_TIME AS OF {time_travel_literal}"

    limit_clause = ""
    if max_results is not None:
        limit_clause = f" LIMIT {bigframes.core.sql.simple_literal(max_results)}"

    where_clause = f" WHERE {sql_predicate}" if sql_predicate else ""

    return (
        f"{select_clause} "
        f"FROM {sub_query}"
        f"{time_travel_clause}{where_clause}{limit_clause}"
    )


def compile_filters(filters: third_party_pandas_gbq.FiltersType) -> str:
    """Compiles a set of filters into a boolean sql expression"""
    if not filters:
        return ""
    filter_string = ""
    valid_operators: Mapping[third_party_pandas_gbq.FilterOps, str] = {
        "in": "IN",
        "not in": "NOT IN",
        "LIKE": "LIKE",
        "==": "=",
        ">": ">",
        "<": "<",
        ">=": ">=",
        "<=": "<=",
        "!=": "!=",
    }

    # If single layer filter, add another pseudo layer. So the single layer represents "and" logic.
    filters_list: list = list(filters)
    if isinstance(filters_list[0], tuple) and (
        len(filters_list[0]) == 0 or not isinstance(list(filters_list[0])[0], tuple)
    ):
        filter_items = [filters_list]
    else:
        filter_items = filters_list

    for group in filter_items:
        if not isinstance(group, Iterable):
            group = [group]

        and_expression = ""
        for filter_item in group:
            if not isinstance(filter_item, tuple) or (len(filter_item) != 3):
                raise ValueError(
                    f"Elements of filters must be tuples of length 3, but got {repr(filter_item)}.",
                )

            column, operator, value = filter_item

            if not isinstance(column, str):
                raise ValueError(
                    f"Column name should be a string, but received '{column}' of type {type(column).__name__}."
                )

            if operator not in valid_operators:
                raise ValueError(f"Operator {operator} is not valid.")

            operator_str = valid_operators[operator]

            column_ref = googlesql.identifier(column)
            if operator_str in ["IN", "NOT IN"]:
                value_literal = bigframes.core.sql.multi_literal(*value)
            else:
                value_literal = bigframes.core.sql.simple_literal(value)
            expression = bigframes.core.sql.infix_op(
                operator_str, column_ref, value_literal
            )
            if and_expression:
                and_expression = bigframes.core.sql.infix_op(
                    "AND", and_expression, expression
                )
            else:
                and_expression = expression

        if filter_string:
            filter_string = bigframes.core.sql.infix_op(
                "OR", filter_string, and_expression
            )
        else:
            filter_string = and_expression

    return filter_string


def select_cluster_cols(
    schema: typing.Sequence[bigquery.SchemaField],
    cluster_candidates: typing.Sequence[str],
) -> typing.Sequence[str]:
    return [
        item.name
        for item in schema
        if (item.name in cluster_candidates) and _can_cluster_bq(item)
    ][:_MAX_CLUSTER_COLUMNS]


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
