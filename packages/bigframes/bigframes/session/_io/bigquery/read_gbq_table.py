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
import typing
from typing import Dict, Iterable, Optional, Sequence, Tuple, Union
import warnings

import bigframes_vendored.constants as constants
import google.api_core.exceptions
import google.cloud.bigquery as bigquery

import bigframes.core
from bigframes.core import bq_data
import bigframes.core.events
import bigframes.exceptions as bfe
import bigframes.session._io.bigquery

# Avoid circular imports.
if typing.TYPE_CHECKING:
    import bigframes.session


def _convert_information_schema_table_id_to_table_reference(
    table_id: str,
    default_project: Optional[str],
) -> bigquery.TableReference:
    """Squeeze an INFORMATION_SCHEMA reference into a TableReference.
    This is kind-of a hack. INFORMATION_SCHEMA is a view that isn't available
    via the tables.get REST API.
    """
    parts = table_id.split(".")
    parts_casefold = [part.casefold() for part in parts]
    dataset_index = parts_casefold.index("INFORMATION_SCHEMA".casefold())

    if dataset_index == 0:
        project = default_project
    else:
        project = ".".join(parts[:dataset_index])

    if project is None:
        message = (
            "Could not determine project ID. "
            "Please provide a project or region in your INFORMATION_SCHEMA table ID, "
            "For example, 'region-REGION_NAME.INFORMATION_SCHEMA.JOBS'."
        )
        raise ValueError(message)

    dataset = "INFORMATION_SCHEMA"
    table_id_short = ".".join(parts[dataset_index + 1 :])
    return bigquery.TableReference(
        bigquery.DatasetReference(project, dataset),
        table_id_short,
    )


def get_information_schema_metadata(
    bqclient: bigquery.Client,
    table_id: str,
    default_project: Optional[str],
) -> bigquery.Table:
    job_config = bigquery.QueryJobConfig(dry_run=True)
    job = bqclient.query(
        f"SELECT * FROM `{table_id}`",
        job_config=job_config,
    )
    table_ref = _convert_information_schema_table_id_to_table_reference(
        table_id=table_id,
        default_project=default_project,
    )
    table = bigquery.Table.from_api_repr(
        {
            "tableReference": table_ref.to_api_repr(),
            "location": job.location,
            # Prevent ourselves from trying to read the table with the BQ
            # Storage API.
            "type": "VIEW",
        }
    )
    table.schema = job.schema
    return table


def is_information_schema(table_id: str):
    table_id_casefold = table_id.casefold()
    # Include the "."s to ensure we don't have false positives for some user
    # defined dataset like MY_INFORMATION_SCHEMA or tables called
    # INFORMATION_SCHEMA.
    return (
        ".INFORMATION_SCHEMA.".casefold() in table_id_casefold
        or table_id_casefold.startswith("INFORMATION_SCHEMA.".casefold())
    )


def is_time_travel_eligible(
    bqclient: bigquery.Client,
    table: Union[bq_data.GbqNativeTable, bq_data.BiglakeIcebergTable],
    columns: Optional[Sequence[str]],
    snapshot_time: datetime.datetime,
    filter_str: Optional[str] = None,
    *,
    should_warn: bool,
    should_dry_run: bool,
    publisher: bigframes.core.events.Publisher,
):
    """Check if a table is eligible to use time-travel.


    Args:
        table: BigQuery table to check.
        should_warn:
            If true, raises a warning when time travel is disabled and the
            underlying table is likely mutable.

    Return:
        bool:
            True if there is a chance that time travel may be supported on this
            table. If ``should_dry_run`` is True, then this is validated with a
            ``dry_run`` query.
    """

    # user code
    # -> pandas.read_gbq_table
    # -> with_default_session
    # -> session.read_gbq_table
    # -> session._read_gbq_table
    # -> loader.read_gbq_table
    # -> is_time_travel_eligible
    stacklevel = 7

    if isinstance(table, bq_data.GbqNativeTable):
        # Anonymous dataset, does not support snapshot ever
        if table.dataset_id.startswith("_"):
            return False

        # Only true tables support time travel
        if table.table_id.endswith("*"):
            if should_warn:
                msg = bfe.format_message(
                    "Wildcard tables do not support FOR SYSTEM_TIME AS OF queries. "
                    "Attempting query without time travel. Be aware that "
                    "modifications to the underlying data may result in errors or "
                    "unexpected behavior."
                )
                warnings.warn(
                    msg, category=bfe.TimeTravelDisabledWarning, stacklevel=stacklevel
                )
            return False
        elif table.metadata.type != "TABLE":
            if table.metadata.type == "MATERIALIZED_VIEW":
                if should_warn:
                    msg = bfe.format_message(
                        "Materialized views do not support FOR SYSTEM_TIME AS OF queries. "
                        "Attempting query without time travel. Be aware that as materialized views "
                        "are updated periodically, modifications to the underlying data in the view may "
                        "result in errors or unexpected behavior."
                    )
                    warnings.warn(
                        msg,
                        category=bfe.TimeTravelDisabledWarning,
                        stacklevel=stacklevel,
                    )
                return False
            elif table.metadata.type == "VIEW":
                return False

    # table might support time travel, lets do a dry-run query with time travel
    if should_dry_run:
        snapshot_sql = bigframes.session._io.bigquery.to_query(
            query_or_table=table.get_full_id(
                quoted=False
            ),  # to_query will quote for us
            columns=columns or (),
            sql_predicate=filter_str,
            time_travel_timestamp=snapshot_time,
        )
        try:
            # If this succeeds, we know that time travel will for sure work.
            bigframes.session._io.bigquery.start_query_with_client(
                bq_client=bqclient,
                sql=snapshot_sql,
                job_config=bigquery.QueryJobConfig(dry_run=True),
                location=None,
                project=None,
                timeout=None,
                metrics=None,
                query_with_job=False,
                publisher=publisher,
            )
            return True

        except google.api_core.exceptions.NotFound:
            # If system time isn't supported, it returns NotFound error?
            # Note that a notfound caused by a simple typo will be
            # caught above when the metadata is fetched, not here.
            if should_warn:
                msg = bfe.format_message(
                    "NotFound error when reading table with time travel."
                    " Attempting query without time travel. Warning: Without"
                    " time travel, modifications to the underlying table may"
                    " result in errors or unexpected behavior."
                )
                warnings.warn(
                    msg, category=bfe.TimeTravelDisabledWarning, stacklevel=stacklevel
                )

        # If we make it to here, we know for sure that time travel won't work.
        return False
    else:
        # We haven't validated it, but there's a chance that time travel could work.
        return True


def infer_unique_columns(
    table: Union[bq_data.GbqNativeTable, bq_data.BiglakeIcebergTable],
    index_cols: Sequence[str],
) -> Tuple[str, ...]:
    """Return a set of columns that can provide a unique row key or empty if none can be inferred.

    Note: primary keys are not enforced, but these are assumed to be unique
    by the query engine, so we make the same assumption here.
    """
    # If index_cols contain the primary_keys, the query engine assumes they are
    # provide a unique index.
    primary_keys = table.primary_key or ()
    if (len(primary_keys) > 0) and frozenset(primary_keys) <= frozenset(index_cols):
        # Essentially, just reordering the primary key to match the index col order
        return tuple(index_col for index_col in index_cols if index_col in primary_keys)

    if primary_keys:
        return primary_keys

    return ()


def check_if_index_columns_are_unique(
    bqclient: bigquery.Client,
    table: Union[bq_data.GbqNativeTable, bq_data.BiglakeIcebergTable],
    index_cols: Sequence[str],
    *,
    publisher: bigframes.core.events.Publisher,
) -> Tuple[str, ...]:
    import bigframes.core.sql
    import bigframes.session._io.bigquery

    # TODO(b/337925142): Avoid a "SELECT *" subquery here by ensuring
    # table_expression only selects just index_cols.
    is_unique_sql = bigframes.core.sql.is_distinct_sql(
        index_cols, table.get_table_ref()
    )
    job_config = bigquery.QueryJobConfig()
    results, _ = bigframes.session._io.bigquery.start_query_with_client(
        bq_client=bqclient,
        sql=is_unique_sql,
        job_config=job_config,
        timeout=None,
        location=None,
        project=None,
        metrics=None,
        query_with_job=False,
        publisher=publisher,
    )
    row = next(iter(results))

    if row["total_count"] == row["distinct_count"]:
        return tuple(index_cols)
    return ()


def get_index_cols(
    table: Union[bq_data.GbqNativeTable, bq_data.BiglakeIcebergTable],
    index_col: Iterable[str]
    | str
    | Iterable[int]
    | int
    | bigframes.enums.DefaultIndexKind,
    *,
    rename_to_schema: Optional[Dict[str, str]] = None,
    default_index_type: bigframes.enums.DefaultIndexKind = bigframes.enums.DefaultIndexKind.SEQUENTIAL_INT64,
) -> Sequence[str]:
    """
    If we can get a total ordering from the table, such as via primary key
    column(s), then return those too so that ordering generation can be
    avoided.
    """
    # Transform index_col -> index_cols so we have a variable that is
    # always a list of column names (possibly empty).
    schema_len = len(table.physical_schema)

    index_cols = []
    if isinstance(index_col, bigframes.enums.DefaultIndexKind):
        if index_col == bigframes.enums.DefaultIndexKind.SEQUENTIAL_INT64:
            # User has explicity asked for a default, sequential index.
            # Use that, even if there are primary keys on the table.
            return []
        if index_col == bigframes.enums.DefaultIndexKind.NULL:
            return []
        else:
            # Note: It's actually quite difficult to mock this out to unit
            # test, as it's not possible to subclass enums in Python. See:
            # https://stackoverflow.com/a/33680021/101923
            raise NotImplementedError(
                f"Got unexpected index_col {repr(index_col)}. {constants.FEEDBACK_LINK}"
            )
    elif isinstance(index_col, str):
        if rename_to_schema is not None:
            index_col = rename_to_schema.get(index_col, index_col)
        index_cols = [index_col]
    elif isinstance(index_col, int):
        if not 0 <= index_col < schema_len:
            raise ValueError(
                f"Integer index {index_col} is out of bounds "
                f"for table with {schema_len} columns (must be >= 0 and < {schema_len})."
            )
        index_cols = [table.physical_schema[index_col].name]
    elif isinstance(index_col, Iterable):
        for item in index_col:
            if isinstance(item, str):
                if rename_to_schema is not None:
                    item = rename_to_schema.get(item, item)
                index_cols.append(item)
            elif isinstance(item, int):
                if not 0 <= item < schema_len:
                    raise ValueError(
                        f"Integer index {item} is out of bounds "
                        f"for table with {schema_len} columns (must be >= 0 and < {schema_len})."
                    )
                index_cols.append(table.physical_schema[item].name)
            else:
                raise TypeError(
                    "If index_col is an iterable, it must contain either strings "
                    "(column names) or integers (column positions)."
                )
    else:
        raise TypeError(
            f"Unsupported type for index_col: {type(index_col).__name__}. Expected"
            "an integer, an string, an iterable of strings, or an iterable of integers."
        )

    # If the isn't an index selected, use the primary keys of the table as the
    # index. If there are no primary keys, we'll return an empty list.
    if len(index_cols) == 0:
        primary_keys = table.primary_key or ()

        # If table has clustering/partitioning, fail if we haven't been able to
        # find index_cols to use. This is to avoid unexpected performance and
        # resource utilization because of the default sequential index. See
        # internal issue 335727141.
        if (
            (table.partition_col is not None or table.cluster_cols)
            and not primary_keys
            and default_index_type == bigframes.enums.DefaultIndexKind.SEQUENTIAL_INT64
        ):
            msg = bfe.format_message(
                f"Table '{str(table.get_full_id())}' is clustered and/or "
                "partitioned, but BigQuery DataFrames was not able to find a "
                "suitable index. To avoid this warning, set at least one of: "
                # TODO(b/338037499): Allow max_results to override this too,
                # once we make it more efficient.
                "`index_col` or `filters`."
            )
            warnings.warn(msg, category=bfe.DefaultIndexWarning)

        # If there are primary keys defined, the query engine assumes these
        # columns are unique, even if the constraint is not enforced. We make
        # the same assumption and use these columns as the total ordering keys.
        index_cols = list(primary_keys)

    return index_cols
