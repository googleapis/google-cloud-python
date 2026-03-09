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


def create_external_table_ddl(
    table_name: str,
    *,
    replace: bool = False,
    if_not_exists: bool = False,
    columns: Optional[Mapping[str, str]] = None,
    partition_columns: Optional[Mapping[str, str]] = None,
    connection_name: Optional[str] = None,
    options: Mapping[str, Union[str, int, float, bool, list]],
) -> str:
    """Generates the CREATE EXTERNAL TABLE DDL statement."""
    statement = ["CREATE"]
    if replace:
        statement.append("OR REPLACE")
    statement.append("EXTERNAL TABLE")
    if if_not_exists:
        statement.append("IF NOT EXISTS")
    statement.append(table_name)

    if columns:
        column_defs = ", ".join([f"{name} {typ}" for name, typ in columns.items()])
        statement.append(f"({column_defs})")

    if connection_name:
        statement.append(f"WITH CONNECTION `{connection_name}`")

    if partition_columns:
        part_defs = ", ".join(
            [f"{name} {typ}" for name, typ in partition_columns.items()]
        )
        statement.append(f"WITH PARTITION COLUMNS ({part_defs})")

    if options:
        opts = []
        for key, value in options.items():
            if isinstance(value, str):
                value_sql = repr(value)
                opts.append(f"{key} = {value_sql}")
            elif isinstance(value, bool):
                opts.append(f"{key} = {str(value).upper()}")
            elif isinstance(value, list):
                list_str = ", ".join([repr(v) for v in value])
                opts.append(f"{key} = [{list_str}]")
            else:
                opts.append(f"{key} = {value}")
        options_str = ", ".join(opts)
        statement.append(f"OPTIONS ({options_str})")

    return " ".join(statement)
