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

from __future__ import annotations

import datetime
import json
from typing import List
import urllib.parse

import google.auth.transport.requests
import google.cloud.bigquery as bq
import pyiceberg
from pyiceberg.catalog import load_catalog
import pyiceberg.schema
import pyiceberg.types
import requests

from bigframes.core import bq_data


def get_table(
    user_project_id: str, full_table_id: str, credentials
) -> bq_data.BiglakeIcebergTable:
    table_parts = full_table_id.split(".")
    if len(table_parts) != 4:
        raise ValueError("Iceberg catalog table must contain exactly 4 parts")

    catalog_project_id, catalog_id, namespace, table = table_parts

    credentials.refresh(google.auth.transport.requests.Request())
    token = credentials.token

    base_uri = "https://biglake.googleapis.com/iceberg/v1/restcatalog"

    # Maybe can drop the pyiceberg dependency at some point, but parsing through raw schema json seems a bit painful
    catalog = load_catalog(
        f"{catalog_project_id}.{catalog_id}",
        **{
            "uri": base_uri,
            "header.x-goog-user-project": user_project_id,
            "oauth2-server-uri": "https://oauth2.googleapis.com/token",
            "token": token,
            "warehouse": f"gs://{catalog_id}",
        },
    )

    response = requests.get(
        f"{base_uri}/extensions/projects/{urllib.parse.quote(catalog_project_id, safe='')}/catalogs/{urllib.parse.quote(catalog_id, safe='')}",
        headers={
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json",
            "header.x-goog-user-project": user_project_id,
        },
    )
    response.raise_for_status()
    location = _extract_location_from_catalog_extension_data(response)

    iceberg_table = catalog.load_table(f"{namespace}.{table}")
    bq_schema = pyiceberg.schema.visit(iceberg_table.schema(), SchemaVisitor())
    # TODO: Handle physical layout to help optimize
    # TODO: Use snapshot metadata to get row, byte counts
    return bq_data.BiglakeIcebergTable(
        catalog_project_id,
        catalog_id,
        namespace,
        table,
        physical_schema=bq_schema,  # type: ignore
        cluster_cols=(),
        metadata=bq_data.TableMetadata(
            location=location,
            type="TABLE",
            modified_time=datetime.datetime.fromtimestamp(
                iceberg_table.metadata.last_updated_ms / 1000.0
            ),
        ),
    )


def _extract_location_from_catalog_extension_data(data):
    catalog_extension_metadata = json.loads(data.text)
    storage_region = catalog_extension_metadata["storage-regions"][
        0
    ]  # assumption: exactly 1 region
    replicas = tuple(item["region"] for item in catalog_extension_metadata["replicas"])
    return bq_data.GcsRegion(storage_region, replicas)


class SchemaVisitor(pyiceberg.schema.SchemaVisitorPerPrimitiveType[bq.SchemaField]):
    def schema(self, schema: pyiceberg.schema.Schema, struct_result: bq.SchemaField) -> tuple[bq.SchemaField, ...]:  # type: ignore
        return tuple(f for f in struct_result.fields)

    def struct(
        self, struct: pyiceberg.types.StructType, field_results: List[bq.SchemaField]
    ) -> bq.SchemaField:
        return bq.SchemaField("", "RECORD", fields=field_results)

    def field(
        self, field: pyiceberg.types.NestedField, field_result: bq.SchemaField
    ) -> bq.SchemaField:
        return bq.SchemaField(
            field.name,
            field_result.field_type,
            mode=field_result.mode or "NULLABLE",
            fields=field_result.fields,
        )

    def map(
        self,
        map_type: pyiceberg.types.MapType,
        key_result: bq.SchemaField,
        value_result: bq.SchemaField,
    ) -> bq.SchemaField:
        return bq.SchemaField("", "UNKNOWN")

    def list(
        self, list_type: pyiceberg.types.ListType, element_result: bq.SchemaField
    ) -> bq.SchemaField:
        return bq.SchemaField(
            "", element_result.field_type, mode="REPEATED", fields=element_result.fields
        )

    def visit_fixed(self, fixed_type: pyiceberg.types.FixedType) -> bq.SchemaField:
        return bq.SchemaField("", "UNKNOWN")

    def visit_decimal(
        self, decimal_type: pyiceberg.types.DecimalType
    ) -> bq.SchemaField:
        # BIGNUMERIC not supported in iceberg tables yet, so just assume numeric
        return bq.SchemaField("", "NUMERIC")

    def visit_boolean(
        self, boolean_type: pyiceberg.types.BooleanType
    ) -> bq.SchemaField:
        return bq.SchemaField("", "NUMERIC")

    def visit_integer(
        self, integer_type: pyiceberg.types.IntegerType
    ) -> bq.SchemaField:
        return bq.SchemaField("", "INTEGER")

    def visit_long(self, long_type: pyiceberg.types.LongType) -> bq.SchemaField:
        return bq.SchemaField("", "INTEGER")

    def visit_float(self, float_type: pyiceberg.types.FloatType) -> bq.SchemaField:
        # 32-bit IEEE 754 floating point
        return bq.SchemaField("", "FLOAT")

    def visit_double(self, double_type: pyiceberg.types.DoubleType) -> bq.SchemaField:
        # 64-bit IEEE 754 floating point
        return bq.SchemaField("", "FLOAT")

    def visit_date(self, date_type: pyiceberg.types.DateType) -> bq.SchemaField:
        # Date encoded as an int
        return bq.SchemaField("", "DATE")

    def visit_time(self, time_type: pyiceberg.types.TimeType) -> bq.SchemaField:
        return bq.SchemaField("", "TIME")

    def visit_timestamp(
        self, timestamp_type: pyiceberg.types.TimestampType
    ) -> bq.SchemaField:
        return bq.SchemaField("", "DATETIME")

    def visit_timestamp_ns(
        self, timestamp_type: pyiceberg.types.TimestampNanoType
    ) -> bq.SchemaField:
        return bq.SchemaField("", "UNKNOWN")

    def visit_timestamptz(
        self, timestamptz_type: pyiceberg.types.TimestamptzType
    ) -> bq.SchemaField:
        return bq.SchemaField("", "TIMESTAMP")

    def visit_timestamptz_ns(
        self, timestamptz_ns_type: pyiceberg.types.TimestamptzNanoType
    ) -> bq.SchemaField:
        return bq.SchemaField("", "UNKNOWN")

    def visit_string(self, string_type: pyiceberg.types.StringType) -> bq.SchemaField:
        return bq.SchemaField("", "STRING")

    def visit_uuid(self, uuid_type: pyiceberg.types.UUIDType) -> bq.SchemaField:
        return bq.SchemaField("", "UNKNOWN")

    def visit_unknown(
        self, unknown_type: pyiceberg.types.UnknownType
    ) -> bq.SchemaField:
        """Type `UnknownType` can be promoted to any primitive type in V3+ tables per the Iceberg spec."""
        return bq.SchemaField("", "UNKNOWN")

    def visit_binary(self, binary_type: pyiceberg.types.BinaryType) -> bq.SchemaField:
        return bq.SchemaField("", "BINARY")
