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
from typing import Any, Dict, List, Sequence, Union

from google.cloud import bigquery
import pandas

from bigframes import dtypes
from bigframes.core import bigframe_node, bq_data, nodes


def get_table_stats(
    table: Union[bq_data.GbqNativeTable, bq_data.BiglakeIcebergTable]
) -> pandas.Series:
    values: List[Any] = []
    index: List[Any] = []

    # Indicate that no query is executed.
    index.append("isQuery")
    values.append(False)

    # Populate column and index types
    col_dtypes = dtypes.bf_type_from_type_kind(table.physical_schema)
    index.append("columnCount")
    values.append(len(col_dtypes))
    index.append("columnDtypes")
    values.append(col_dtypes)

    # Add raw BQ schema
    index.append("bigquerySchema")
    values.append(table.physical_schema)

    index.append("numBytes")
    values.append(table.metadata.numBytes)
    index.append("numRows")
    values.append(table.metadata.numRows)
    index.append("location")
    values.append(table.metadata.location)
    index.append("type")
    values.append(table.metadata.type)

    index.append("creationTime")
    values.append(table.metadata.created_time)

    index.append("lastModifiedTime")
    values.append(table.metadata.modified_time)

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
    expr_root: bigframe_node.BigFrameNode | None = None,
) -> pandas.Series:
    """
    Returns important stats from the query job as a Pandas Series. The dtypes information is added too.

    Args:
        expr_root (Optional):
            The root of the expression tree that may contain local data, whose size is added to the
            total bytes count if available.

    """
    index = ["columnCount", "columnDtypes", "indexLevel", "indexDtypes"]
    values = [len(column_dtypes), column_dtypes, len(index_dtypes), index_dtypes]

    s = pandas.Series(values, index=index)

    result = pandas.concat([s, get_query_stats(query_job)])
    if expr_root is not None:
        result["totalBytesProcessed"] += get_local_bytes(expr_root)
    return result


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

    result = pandas.Series(values, index=index)
    if result["totalBytesProcessed"] is None:
        result["totalBytesProcessed"] = 0
    else:
        result["totalBytesProcessed"] = int(result["totalBytesProcessed"])

    return result


def get_local_bytes(root: bigframe_node.BigFrameNode) -> int:
    def get_total_bytes(
        root: bigframe_node.BigFrameNode, child_results: tuple[int, ...]
    ) -> int:
        child_bytes = sum(child_results)

        if isinstance(root, nodes.ReadLocalNode):
            return child_bytes + root.local_data_source.data.get_total_buffer_size()

        return child_bytes

    return root.reduce_up(get_total_bytes)
