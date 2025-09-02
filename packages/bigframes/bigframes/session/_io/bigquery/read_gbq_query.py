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

"""Private helpers for implementing read_gbq_query."""

from __future__ import annotations

from typing import cast, Iterable, Optional, Tuple

from google.cloud import bigquery
import google.cloud.bigquery.table
import pandas

from bigframes import dataframe
from bigframes.core import local_data, pyarrow_utils
import bigframes.core as core
import bigframes.core.blocks as blocks
import bigframes.core.guid
import bigframes.core.schema as schemata
import bigframes.enums
import bigframes.session


def create_dataframe_from_query_job_stats(
    query_job: Optional[bigquery.QueryJob], *, session: bigframes.session.Session
) -> dataframe.DataFrame:
    """Convert a QueryJob into a DataFrame with key statistics about the query.

    Any changes you make here, please try to keep in sync with pandas-gbq.
    """
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
        session=session,
    )


def create_dataframe_from_row_iterator(
    rows: google.cloud.bigquery.table.RowIterator,
    *,
    session: bigframes.session.Session,
    index_col: Iterable[str] | str | bigframes.enums.DefaultIndexKind,
    columns: Iterable[str],
) -> dataframe.DataFrame:
    """Convert a RowIterator into a DataFrame wrapping a LocalNode.

    This allows us to create a DataFrame from query results, even in the
    'jobless' case where there's no destination table.
    """
    pa_table = rows.to_arrow()
    bq_schema = list(rows.schema)
    is_default_index = not index_col or isinstance(
        index_col, bigframes.enums.DefaultIndexKind
    )

    if is_default_index:
        # We get a sequential index for free, so use that if no index is specified.
        # TODO(tswast): Use array_value.promote_offsets() instead once that node is
        # supported by the local engine.
        offsets_col = bigframes.core.guid.generate_guid()
        pa_table = pyarrow_utils.append_offsets(pa_table, offsets_col=offsets_col)
        bq_schema += [bigquery.SchemaField(offsets_col, "INTEGER")]
        index_columns: Tuple[str, ...] = (offsets_col,)
        index_labels: Tuple[Optional[str], ...] = (None,)
    elif isinstance(index_col, str):
        index_columns = (index_col,)
        index_labels = (index_col,)
    else:
        index_col = cast(Iterable[str], index_col)
        index_columns = tuple(index_col)
        index_labels = cast(Tuple[Optional[str], ...], tuple(index_col))

    # We use the ManagedArrowTable constructor directly, because the
    # results of to_arrow() should be the source of truth with regards
    # to canonical formats since it comes from either the BQ Storage
    # Read API or has been transformed by google-cloud-bigquery to look
    # like the output of the BQ Storage Read API.
    mat = local_data.ManagedArrowTable(
        pa_table,
        schemata.ArraySchema.from_bq_schema(bq_schema),
    )
    mat.validate()

    column_labels = [
        field.name for field in rows.schema if field.name not in index_columns
    ]

    array_value = core.ArrayValue.from_managed(mat, session)
    block = blocks.Block(
        array_value,
        index_columns=index_columns,
        column_labels=column_labels,
        index_labels=index_labels,
    )
    df = dataframe.DataFrame(block)

    if columns:
        df = df[list(columns)]

    if not is_default_index:
        df = df.sort_index()

    return df
