# Copyright 2025 Google LLC
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
from __future__ import annotations

import copy
from typing import Any, Dict, List, Sequence

from google.cloud import bigquery
import pandas

from bigframes import dtypes


def get_table_stats(table: bigquery.Table) -> pandas.Series:
    values: List[Any] = []
    index: List[Any] = []

    # Indicate that no query is executed.
    index.append("isQuery")
    values.append(False)

    # Populate column and index types
    col_dtypes = dtypes.bf_type_from_type_kind(table.schema)
    index.append("columnCount")
    values.append(len(col_dtypes))
    index.append("columnDtypes")
    values.append(col_dtypes)

    # Add raw BQ schema
    index.append("bigquerySchema")
    values.append(table.schema)

    for key in ("numBytes", "numRows", "location", "type"):
        index.append(key)
        values.append(table._properties[key])

    index.append("creationTime")
    values.append(table.created)

    index.append("lastModifiedTime")
    values.append(table.modified)

    return pandas.Series(values, index=index)


def get_query_stats_with_inferred_dtypes(
    query_job: bigquery.QueryJob,
    value_cols: Sequence[str],
    index_cols: Sequence[str],
) -> pandas.Series:
    if query_job.schema is None:
        # If the schema is not available, don't bother inferring dtypes.
        return get_query_stats(query_job)

    col_dtypes = dtypes.bf_type_from_type_kind(query_job.schema)

    if value_cols:
        value_col_dtypes = {
            col: col_dtypes[col] for col in value_cols if col in col_dtypes
        }
    else:
        # Use every column that is not mentioned as an index column
        value_col_dtypes = {
            col: dtype
            for col, dtype in col_dtypes.items()
            if col not in set(index_cols)
        }

    index_dtypes = [col_dtypes[col] for col in index_cols]

    return get_query_stats_with_dtypes(query_job, value_col_dtypes, index_dtypes)


def get_query_stats_with_dtypes(
    query_job: bigquery.QueryJob,
    column_dtypes: Dict[str, dtypes.Dtype],
    index_dtypes: Sequence[dtypes.Dtype],
) -> pandas.Series:
    index = ["columnCount", "columnDtypes", "indexLevel", "indexDtypes"]
    values = [len(column_dtypes), column_dtypes, len(index_dtypes), index_dtypes]

    s = pandas.Series(values, index=index)

    return pandas.concat([s, get_query_stats(query_job)])


def get_query_stats(
    query_job: bigquery.QueryJob,
) -> pandas.Series:
    """Returns important stats from the query job as a Pandas Series."""

    index: List[Any] = []
    values: List[Any] = []

    # Add raw BQ schema
    index.append("bigquerySchema")
    values.append(query_job.schema)

    job_api_repr = copy.deepcopy(query_job._properties)

    # jobReference might not be populated for "job optional" queries.
    job_ref = job_api_repr.get("jobReference", {})
    for key, val in job_ref.items():
        index.append(key)
        values.append(val)

    configuration = job_api_repr.get("configuration", {})
    index.append("jobType")
    values.append(configuration.get("jobType", None))
    index.append("dispatchedSql")
    values.append(configuration.get("query", {}).get("query", None))

    query_config = configuration.get("query", {})
    for key in ("destinationTable", "useLegacySql"):
        index.append(key)
        values.append(query_config.get(key, None))

    statistics = job_api_repr.get("statistics", {})
    query_stats = statistics.get("query", {})
    for key in (
        "referencedTables",
        "totalBytesProcessed",
        "cacheHit",
        "statementType",
    ):
        index.append(key)
        values.append(query_stats.get(key, None))

    creation_time = statistics.get("creationTime", None)
    index.append("creationTime")
    values.append(
        pandas.Timestamp(creation_time, unit="ms", tz="UTC")
        if creation_time is not None
        else None
    )

    return pandas.Series(values, index=index)
