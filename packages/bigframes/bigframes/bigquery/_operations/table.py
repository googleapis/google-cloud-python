# Copyright 2026 Google LLC
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

from typing import Mapping, Optional, Union

import bigframes_vendored.constants
import google.cloud.bigquery
import pandas as pd

import bigframes.core.logging.log_adapter as log_adapter
import bigframes.core.sql.table
import bigframes.session


def _get_table_metadata(
    *,
    bqclient: google.cloud.bigquery.Client,
    table_name: str,
) -> pd.Series:
    table_metadata = bqclient.get_table(table_name)
    table_dict = table_metadata.to_api_repr()
    return pd.Series(table_dict)


@log_adapter.method_logger(custom_base_name="bigquery_table")
def create_external_table(
    table_name: str,
    *,
    replace: bool = False,
    if_not_exists: bool = False,
    columns: Optional[Mapping[str, str]] = None,
    partition_columns: Optional[Mapping[str, str]] = None,
    connection_name: Optional[str] = None,
    options: Mapping[str, Union[str, int, float, bool, list]],
    session: Optional[bigframes.session.Session] = None,
) -> pd.Series:
    """
    Creates a BigQuery external table.

    See the `BigQuery CREATE EXTERNAL TABLE DDL syntax
    <https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_external_table_statement>`_
    for additional reference.

    Args:
        table_name (str):
            The name of the table in BigQuery.
        replace (bool, default False):
            Whether to replace the table if it already exists.
        if_not_exists (bool, default False):
            Whether to ignore the error if the table already exists.
        columns (Mapping[str, str], optional):
            The table's schema.
        partition_columns (Mapping[str, str], optional):
            The table's partition columns.
        connection_name (str, optional):
            The connection to use for the table.
        options (Mapping[str, Union[str, int, float, bool, list]]):
            The OPTIONS clause, which specifies the table options.
        session (bigframes.session.Session, optional):
            The session to use. If not provided, the default session is used.

    Returns:
        pandas.Series:
            A Series with object dtype containing the table metadata. Reference
            the `BigQuery Table REST API reference
            <https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#Table>`_
            for available fields.
    """
    import bigframes.pandas as bpd

    sql = bigframes.core.sql.table.create_external_table_ddl(
        table_name=table_name,
        replace=replace,
        if_not_exists=if_not_exists,
        columns=columns,
        partition_columns=partition_columns,
        connection_name=connection_name,
        options=options,
    )

    if session is None:
        bpd.read_gbq_query(sql)
        session = bpd.get_global_session()
        assert (
            session is not None
        ), f"Missing connection to BigQuery. Please report how you encountered this error at {bigframes_vendored.constants.FEEDBACK_LINK}."
    else:
        session.read_gbq_query(sql)

    return _get_table_metadata(bqclient=session.bqclient, table_name=table_name)
