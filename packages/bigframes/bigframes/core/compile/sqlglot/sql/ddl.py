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

import bigframes_vendored.sqlglot as sg
import bigframes_vendored.sqlglot.expressions as sge

from bigframes.core.compile.sqlglot.sql import base


def load_data(
    table_name: str,
    *,
    write_disposition: str = "INTO",
    columns: Optional[Mapping[str, str]] = None,
    partition_by: Optional[list[str]] = None,
    cluster_by: Optional[list[str]] = None,
    table_options: Optional[Mapping[str, Union[str, int, float, bool, list]]] = None,
    from_files_options: Mapping[str, Union[str, int, float, bool, list]],
    with_partition_columns: Optional[Mapping[str, str]] = None,
    connection_name: Optional[str] = None,
) -> sge.LoadData:
    """Generates the LOAD DATA DDL statement."""
    # We use a Table with a simple identifier for the table name.
    # Quoting is handled by the dialect.
    table_expr = sge.Table(this=base.identifier(table_name))

    sge_partition_by = (
        sge.PartitionedByProperty(
            this=base.identifier(partition_by[0])
            if len(partition_by) == 1
            else sge.Tuple(expressions=[base.identifier(col) for col in partition_by])
        )
        if partition_by
        else None
    )

    sge_cluster_by = (
        sge.Cluster(expressions=[base.identifier(col) for col in cluster_by])
        if cluster_by
        else None
    )

    sge_from_files = sge.Tuple(
        expressions=[
            sge.Property(this=base.identifier(k), value=base.literal(v))
            for k, v in from_files_options.items()
        ]
    )

    sge_connection = base.identifier(connection_name) if connection_name else None

    return sge.LoadData(
        this=table_expr,
        overwrite=(write_disposition == "OVERWRITE"),
        inpath=sge.convert("fake"),  # satisfy sqlglot's required inpath arg
        columns=_get_sge_schema(columns),
        partition_by=sge_partition_by,
        cluster_by=sge_cluster_by,
        options=_get_sge_properties(table_options),
        from_files=sge_from_files,
        with_partition_columns=_get_sge_schema(with_partition_columns),
        connection=sge_connection,
    )


def create_external_table(
    table_name: str,
    *,
    replace: bool = False,
    if_not_exists: bool = False,
    columns: Optional[Mapping[str, str]] = None,
    partition_columns: Optional[Mapping[str, str]] = None,
    connection_name: Optional[str] = None,
    options: Optional[Mapping[str, Union[str, int, float, bool, list]]] = None,
) -> sge.Create:
    """Generates the CREATE EXTERNAL TABLE DDL statement."""
    sge_connection = base.identifier(connection_name) if connection_name else None

    table_expr = sge.Table(this=base.identifier(table_name))

    # sqlglot.expressions.Create usually takes 'this' (Table or Schema)
    sge_schema = _get_sge_schema(columns)
    this: sge.Table | sge.Schema
    if sge_schema:
        sge_schema.set("this", table_expr)
        this = sge_schema
    else:
        this = table_expr

    return sge.Create(
        this=this,
        kind="EXTERNAL TABLE",
        replace=replace,
        exists_ok=if_not_exists,
        properties=_get_sge_properties(options),
        connection=sge_connection,
        partition_columns=_get_sge_schema(partition_columns),
    )


def _get_sge_schema(
    columns: Optional[Mapping[str, str]] = None
) -> Optional[sge.Schema]:
    if not columns:
        return None

    return sge.Schema(
        this=None,
        expressions=[
            sge.ColumnDef(
                this=base.identifier(name),
                kind=sge.DataType.build(typ, dialect=base.DIALECT),
            )
            for name, typ in columns.items()
        ],
    )


def _get_sge_properties(
    options: Optional[Mapping[str, Union[str, int, float, bool, list]]] = None
) -> Optional[sge.Properties]:
    if not options:
        return None

    return sge.Properties(
        expressions=[
            sge.Property(this=base.identifier(k), value=base.literal(v))
            for k, v in options.items()
        ]
    )


def _loaddata_sql(self: sg.Generator, expression: sge.LoadData) -> str:
    out = ["LOAD DATA"]
    if expression.args.get("overwrite"):
        out.append("OVERWRITE")

    out.append(f"INTO {self.sql(expression, 'this').strip()}")

    # We ignore inpath as it's just a dummy to satisfy sqlglot requirements
    # but BigQuery uses FROM FILES instead.

    columns = self.sql(expression, "columns").strip()
    if columns:
        out.append(columns)

    partition_by = self.sql(expression, "partition_by").strip()
    if partition_by:
        out.append(partition_by)

    cluster_by = self.sql(expression, "cluster_by").strip()
    if cluster_by:
        out.append(cluster_by)

    options = self.sql(expression, "options").strip()
    if options:
        out.append(options)

    from_files = self.sql(expression, "from_files").strip()
    if from_files:
        out.append(f"FROM FILES {from_files}")

    with_partition_columns = self.sql(expression, "with_partition_columns").strip()
    if with_partition_columns:
        out.append(f"WITH PARTITION COLUMNS {with_partition_columns}")

    connection = self.sql(expression, "connection").strip()
    if connection:
        out.append(f"WITH CONNECTION {connection}")

    return " ".join(out)


def _create_sql(self: sg.Generator, expression: sge.Create) -> str:
    kind = expression.args.get("kind")
    if kind != "EXTERNAL TABLE":
        return self.create_sql(expression)

    out = ["CREATE"]
    if expression.args.get("replace"):
        out.append("OR REPLACE")
    out.append("EXTERNAL TABLE")
    if expression.args.get("exists_ok"):
        out.append("IF NOT EXISTS")

    out.append(self.sql(expression, "this"))

    connection = self.sql(expression, "connection").strip()
    if connection:
        out.append(f"WITH CONNECTION {connection}")

    partition_columns = self.sql(expression, "partition_columns").strip()
    if partition_columns:
        out.append(f"WITH PARTITION COLUMNS {partition_columns}")

    properties = self.sql(expression, "properties").strip()
    if properties:
        out.append(properties)

    return " ".join(out)


# Register the transform for BigQuery generator
base.DIALECT.Generator.TRANSFORMS[sge.LoadData] = _loaddata_sql
base.DIALECT.Generator.TRANSFORMS[sge.Create] = _create_sql
