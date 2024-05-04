# Copyright 2024 Google LLC
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

"""
Private helpers for loading a BigQuery table as a BigQuery DataFrames DataFrame.
"""

from __future__ import annotations

import datetime
import itertools
import textwrap
import typing
from typing import Dict, Iterable, List, Optional, Tuple
import warnings

import bigframes_vendored.ibis.expr.operations as vendored_ibis_ops
import google.api_core.exceptions
import google.cloud.bigquery as bigquery
import ibis
import ibis.backends
import ibis.expr.datatypes as ibis_dtypes
import ibis.expr.types as ibis_types

import bigframes
import bigframes.clients
import bigframes.constants
import bigframes.core as core
import bigframes.core.compile
import bigframes.core.guid as guid
import bigframes.core.ordering as order
import bigframes.dtypes
import bigframes.session._io.bigquery.read_gbq_table
import bigframes.session.clients
import bigframes.version

# Avoid circular imports.
if typing.TYPE_CHECKING:
    import bigframes.session


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


def get_table_metadata(
    bqclient: bigquery.Client,
    table_ref: google.cloud.bigquery.table.TableReference,
    *,
    api_name: str,
    cache: Dict[bigquery.TableReference, Tuple[datetime.datetime, bigquery.Table]],
    use_cache: bool = True,
) -> Tuple[datetime.datetime, google.cloud.bigquery.table.Table]:
    """Get the table metadata, either from cache or via REST API."""

    cached_table = cache.get(table_ref)
    if use_cache and cached_table is not None:
        snapshot_timestamp, _ = cached_table

        # Cache hit could be unexpected. See internal issue 329545805.
        # Raise a warning with more information about how to avoid the
        # problems with the cache.
        warnings.warn(
            f"Reading cached table from {snapshot_timestamp} to avoid "
            "incompatibilies with previous reads of this table. To read "
            "the latest version, set `use_cache=False` or close the "
            "current session with Session.close() or "
            "bigframes.pandas.close_session().",
            # There are many layers before we get to (possibly) the user's code:
            # pandas.read_gbq_table
            # -> with_default_session
            # -> Session.read_gbq_table
            # -> _read_gbq_table
            # -> _get_snapshot_sql_and_primary_key
            # -> get_snapshot_datetime_and_table_metadata
            stacklevel=7,
        )
        return cached_table

    # TODO(swast): It's possible that the table metadata is changed between now
    # and when we run the CURRENT_TIMESTAMP() query to see when we can time
    # travel to. Find a way to fetch the table metadata and BQ's current time
    # atomically.
    table = bqclient.get_table(table_ref)

    # TODO(b/336521938): Refactor to make sure we set the "bigframes-api"
    # whereever we execute a query.
    job_config = bigquery.QueryJobConfig()
    job_config.labels["bigframes-api"] = api_name
    snapshot_timestamp = list(
        bqclient.query(
            "SELECT CURRENT_TIMESTAMP() AS `current_timestamp`",
            job_config=job_config,
        ).result()
    )[0][0]
    cached_table = (snapshot_timestamp, table)
    cache[table_ref] = cached_table
    return cached_table


def _create_time_travel_sql(
    table_ref: bigquery.TableReference, time_travel_timestamp: datetime.datetime
) -> str:
    """Query a table via 'time travel' for consistent reads."""
    # If we have an anonymous query results table, it can't be modified and
    # there isn't any BigQuery time travel.
    if table_ref.dataset_id.startswith("_"):
        return f"SELECT * FROM `{table_ref.project}`.`{table_ref.dataset_id}`.`{table_ref.table_id}`"

    return textwrap.dedent(
        f"""
        SELECT *
        FROM `{table_ref.project}`.`{table_ref.dataset_id}`.`{table_ref.table_id}`
        FOR SYSTEM_TIME AS OF TIMESTAMP({repr(time_travel_timestamp.isoformat())})
        """
    )


def get_ibis_time_travel_table(
    ibis_client: ibis.BaseBackend,
    table_ref: bigquery.TableReference,
    time_travel_timestamp: datetime.datetime,
) -> ibis_types.Table:
    try:
        return ibis_client.sql(
            _create_time_travel_sql(table_ref, time_travel_timestamp)
        )
    except google.api_core.exceptions.Forbidden as ex:
        # Ibis does a dry run to get the types of the columns from the SQL.
        if "Drive credentials" in ex.message:
            ex.message += "\nCheck https://cloud.google.com/bigquery/docs/query-drive-data#Google_Drive_permissions."
        raise


def _check_index_uniqueness(
    bqclient: bigquery.Client,
    ibis_client: ibis.BaseBackend,
    table: ibis_types.Table,
    index_cols: List[str],
    api_name: str,
) -> bool:
    distinct_table = table.select(*index_cols).distinct()
    is_unique_sql = f"""WITH full_table AS (
        {ibis_client.compile(table)}
    ),
    distinct_table AS (
        {ibis_client.compile(distinct_table)}
    )

    SELECT (SELECT COUNT(*) FROM full_table) AS `total_count`,
    (SELECT COUNT(*) FROM distinct_table) AS `distinct_count`
    """
    job_config = bigquery.QueryJobConfig()
    job_config.labels["bigframes-api"] = api_name
    results = bqclient.query_and_wait(is_unique_sql, job_config=job_config)
    row = next(iter(results))

    total_count = row["total_count"]
    distinct_count = row["distinct_count"]
    return total_count == distinct_count


def _get_primary_keys(
    table: bigquery.table.Table,
) -> List[str]:
    """Get primary keys from table if they are set."""

    primary_keys: List[str] = []
    if (
        (table_constraints := getattr(table, "table_constraints", None)) is not None
        and (primary_key := table_constraints.primary_key) is not None
        # This will be False for either None or empty list.
        # We want primary_keys = None if no primary keys are set.
        and (columns := primary_key.columns)
    ):
        primary_keys = columns if columns is not None else []

    return primary_keys


def _is_table_clustered_or_partitioned(
    table: bigquery.table.Table,
) -> bool:
    """Returns True if the table is clustered or partitioned."""

    # Could be None or an empty tuple if it's not clustered, both of which are
    # falsey.
    if table.clustering_fields:
        return True

    if (
        time_partitioning := table.time_partitioning
    ) is not None and time_partitioning.type_ is not None:
        return True

    if (
        range_partitioning := table.range_partitioning
    ) is not None and range_partitioning.field is not None:
        return True

    return False


def get_index_cols_and_uniqueness(
    bqclient: bigquery.Client,
    ibis_client: ibis.BaseBackend,
    table: bigquery.table.Table,
    table_expression: ibis_types.Table,
    index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind,
    api_name: str,
) -> Tuple[List[str], bool]:
    """
    If we can get a total ordering from the table, such as via primary key
    column(s), then return those too so that ordering generation can be
    avoided.
    """

    # Transform index_col -> index_cols so we have a variable that is
    # always a list of column names (possibly empty).
    if isinstance(index_col, bigframes.enums.DefaultIndexKind):
        if index_col == bigframes.enums.DefaultIndexKind.SEQUENTIAL_INT64:
            # User has explicity asked for a default, sequential index.
            # Use that, even if there are primary keys on the table.
            #
            # Note: This relies on the default behavior of the Block
            # constructor to create a default sequential index. If that ever
            # changes, this logic will need to be revisited.
            return [], False
        else:
            # Note: It's actually quite difficult to mock this out to unit
            # test, as it's not possible to subclass enums in Python. See:
            # https://stackoverflow.com/a/33680021/101923
            raise NotImplementedError(
                f"Got unexpected index_col {repr(index_col)}. {bigframes.constants.FEEDBACK_LINK}"
            )
    elif isinstance(index_col, str):
        index_cols: List[str] = [index_col]
    else:
        index_cols = list(index_col)

    # If the isn't an index selected, use the primary keys of the table as the
    # index. If there are no primary keys, we'll return an empty list.
    if len(index_cols) == 0:
        primary_keys = _get_primary_keys(table)

        # If table has clustering/partitioning, fail if we haven't been able to
        # find index_cols to use. This is to avoid unexpected performance and
        # resource utilization because of the default sequential index. See
        # internal issue 335727141.
        if _is_table_clustered_or_partitioned(table) and not primary_keys:
            warnings.warn(
                f"Table '{str(table.reference)}' is clustered and/or "
                "partitioned, but BigQuery DataFrames was not able to find a "
                "suitable index. To avoid this warning, set at least one of: "
                # TODO(b/338037499): Allow max_results to override this too,
                # once we make it more efficient.
                "`index_col` or `filters`.",
                category=bigframes.exceptions.DefaultIndexWarning,
            )

        # If there are primary keys defined, the query engine assumes these
        # columns are unique, even if the constraint is not enforced. We make
        # the same assumption and use these columns as the total ordering keys.
        index_cols = primary_keys
        is_index_unique = len(index_cols) != 0
    else:
        is_index_unique = _check_index_uniqueness(
            bqclient=bqclient,
            ibis_client=ibis_client,
            # TODO(b/337925142): Avoid a "SELECT *" subquery here by using
            # _create_time_travel_sql with just index_cols.
            table=table_expression,
            index_cols=index_cols,
            api_name=api_name,
        )

    return index_cols, is_index_unique


def get_time_travel_datetime_and_table_metadata(
    bqclient: bigquery.Client,
    table_ref: bigquery.TableReference,
    *,
    api_name: str,
    cache: Dict[bigquery.TableReference, Tuple[datetime.datetime, bigquery.Table]],
    use_cache: bool = True,
) -> Tuple[datetime.datetime, bigquery.Table]:
    cached_table = cache.get(table_ref)
    if use_cache and cached_table is not None:
        snapshot_timestamp, _ = cached_table

        # Cache hit could be unexpected. See internal issue 329545805.
        # Raise a warning with more information about how to avoid the
        # problems with the cache.
        warnings.warn(
            f"Reading cached table from {snapshot_timestamp} to avoid "
            "incompatibilies with previous reads of this table. To read "
            "the latest version, set `use_cache=False` or close the "
            "current session with Session.close() or "
            "bigframes.pandas.close_session().",
            # There are many layers before we get to (possibly) the user's code:
            # pandas.read_gbq_table
            # -> with_default_session
            # -> Session.read_gbq_table
            # -> _read_gbq_table
            # -> _get_snapshot_sql_and_primary_key
            # -> get_snapshot_datetime_and_table_metadata
            stacklevel=7,
        )
        return cached_table

    # TODO(swast): It's possible that the table metadata is changed between now
    # and when we run the CURRENT_TIMESTAMP() query to see when we can time
    # travel to. Find a way to fetch the table metadata and BQ's current time
    # atomically.
    table = bqclient.get_table(table_ref)

    # TODO(b/336521938): Refactor to make sure we set the "bigframes-api"
    # whereever we execute a query.
    job_config = bigquery.QueryJobConfig()
    job_config.labels["bigframes-api"] = api_name
    snapshot_timestamp = list(
        bqclient.query(
            "SELECT CURRENT_TIMESTAMP() AS `current_timestamp`",
            job_config=job_config,
        ).result()
    )[0][0]
    cached_table = (snapshot_timestamp, table)
    cache[table_ref] = cached_table
    return cached_table


def to_array_value_with_total_ordering(
    session: bigframes.session.Session,
    table_expression: ibis_types.Table,
    total_ordering_cols: List[str],
) -> core.ArrayValue:
    """Create an ArrayValue, assuming we already have a total ordering."""
    ordering = order.ExpressionOrdering(
        ordering_value_columns=tuple(
            order.ascending_over(column_id) for column_id in total_ordering_cols
        ),
        total_ordering_columns=frozenset(total_ordering_cols),
    )
    column_values = [table_expression[col] for col in table_expression.columns]
    return core.ArrayValue.from_ibis(
        session,
        table_expression,
        columns=column_values,
        hidden_ordering_columns=[],
        ordering=ordering,
    )


def to_array_value_with_default_ordering(
    session: bigframes.session.Session,
    table: ibis_types.Table,
    table_rows: Optional[int],
) -> core.ArrayValue:
    """Create an ArrayValue with a deterministic default ordering."""
    # Since this might also be used as the index, don't use the default
    # "ordering ID" name.

    # For small tables, 64 bits is enough to avoid collisions, 128 bits will never ever collide no matter what
    # Assume table is large if table row count is unknown
    use_double_hash = (table_rows is None) or (table_rows == 0) or (table_rows > 100000)

    ordering_hash_part = guid.generate_guid("bigframes_ordering_")
    ordering_hash_part2 = guid.generate_guid("bigframes_ordering_")
    ordering_rand_part = guid.generate_guid("bigframes_ordering_")

    # All inputs into hash must be non-null or resulting hash will be null
    str_values = list(
        map(lambda col: _convert_to_nonnull_string(table[col]), table.columns)
    )
    full_row_str = (
        str_values[0].concat(*str_values[1:]) if len(str_values) > 1 else str_values[0]
    )
    full_row_hash = full_row_str.hash().name(ordering_hash_part)
    # By modifying value slightly, we get another hash uncorrelated with the first
    full_row_hash_p2 = (full_row_str + "_").hash().name(ordering_hash_part2)
    # Used to disambiguate between identical rows (which will have identical hash)
    random_value = ibis.random().name(ordering_rand_part)

    order_values = (
        [full_row_hash, full_row_hash_p2, random_value]
        if use_double_hash
        else [full_row_hash, random_value]
    )

    original_column_ids = table.columns
    table_with_ordering = table.select(
        itertools.chain(original_column_ids, order_values)
    )

    ordering = order.ExpressionOrdering(
        ordering_value_columns=tuple(
            order.ascending_over(col.get_name()) for col in order_values
        ),
        total_ordering_columns=frozenset(col.get_name() for col in order_values),
    )
    columns = [table_with_ordering[col] for col in original_column_ids]
    hidden_columns = [table_with_ordering[col.get_name()] for col in order_values]
    return core.ArrayValue.from_ibis(
        session,
        table_with_ordering,
        columns,
        hidden_ordering_columns=hidden_columns,
        ordering=ordering,
    )
