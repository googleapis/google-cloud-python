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

"""Private module: Helpers for I/O operations."""

from __future__ import annotations

import datetime
import textwrap
import types
import typing
from typing import Dict, Iterable, Union
import uuid

import google.cloud.bigquery as bigquery

if typing.TYPE_CHECKING:
    import bigframes.session


IO_ORDERING_ID = "bqdf_row_nums"
TEMP_TABLE_PREFIX = "bqdf{date}_{random_id}"


def create_export_csv_statement(
    table_id: str, uri: str, field_delimiter: str, header: bool
) -> str:
    return create_export_data_statement(
        table_id,
        uri,
        "CSV",
        {
            "field_delimiter": field_delimiter,
            "header": header,
        },
    )


def create_export_data_statement(
    table_id: str, uri: str, format: str, export_options: Dict[str, Union[bool, str]]
) -> str:
    all_options: Dict[str, Union[bool, str]] = {
        "uri": uri,
        "format": format,
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


def random_table(dataset: bigquery.DatasetReference) -> bigquery.TableReference:
    """Generate a random table ID with BigQuery DataFrames prefix.

    Args:
        dataset (google.cloud.bigquery.DatasetReference):
            The dataset to make the table reference in. Usually the anonymous
            dataset for the session.

    Returns:
        google.cloud.bigquery.TableReference:
            Fully qualified table ID of a table that doesn't exist.
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    random_id = uuid.uuid4().hex
    table_id = TEMP_TABLE_PREFIX.format(
        date=now.strftime("%Y%m%d"), random_id=random_id
    )
    return dataset.table(table_id)


def table_ref_to_sql(table: bigquery.TableReference) -> str:
    """Format a table reference as escaped SQL."""
    return f"`{table.project}`.`{table.dataset_id}`.`{table.table_id}`"


def create_table_clone(
    source: bigquery.TableReference,
    dataset: bigquery.DatasetReference,
    expiration: datetime.datetime,
    session: bigframes.session.Session,
    api_name: str,
) -> bigquery.TableReference:
    """Create a table clone for consistent reads."""
    # If we have an anonymous query results table, it can't be modified and
    # there isn't any BigQuery time travel.
    if source.dataset_id.startswith("_"):
        return source

    fully_qualified_source_id = table_ref_to_sql(source)
    destination = random_table(dataset)
    fully_qualified_destination_id = table_ref_to_sql(destination)

    # Include a label so that Dataplex Lineage can identify temporary
    # tables that BigQuery DataFrames creates. Googlers: See internal issue
    # 296779699.
    ddl = textwrap.dedent(
        f"""
        CREATE OR REPLACE TABLE
        {fully_qualified_destination_id}
        CLONE {fully_qualified_source_id}
        OPTIONS(
            expiration_timestamp=TIMESTAMP "{expiration.isoformat()}",
            labels=[
                ("source", "bigquery-dataframes-temp"),
                ("bigframes-api", {repr(api_name)})
            ]
        )
        """
    )
    job_config = bigquery.QueryJobConfig()
    job_config.labels = {
        "source": "bigquery-dataframes-temp",
        "bigframes-api": api_name,
    }
    session._start_query(ddl, job_config=job_config)
    return destination


def create_temp_table(
    bqclient: bigquery.Client,
    dataset: bigquery.DatasetReference,
    expiration: datetime.datetime,
) -> str:
    """Create an empty table with an expiration in the desired dataset."""
    table_ref = random_table(dataset)
    destination = bigquery.Table(table_ref)
    destination.expires = expiration
    bqclient.create_table(destination)
    return f"{table_ref.project}.{table_ref.dataset_id}.{table_ref.table_id}"


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
