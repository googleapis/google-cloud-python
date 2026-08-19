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

import pyarrow as pa


def parse_sql_type(sql: str) -> pa.DataType:
    """
    Parses a SQL type string to its PyArrow equivalence:

    For example:
        "STRING" -> pa.string()
        "ARRAY<INT64>" -> pa.list_(pa.int64())
        "STRUCT<x ARRAY<FLOAT64>, y BOOL>" -> pa.struct(
            (
                pa.field("x", pa.list_(pa.float64())),
                pa.field("y", pa.bool_()),
            )
        )
    """
    sql = sql.strip()

    if sql.upper() == "STRING":
        return pa.string()

    if sql.upper() == "INT64":
        return pa.int64()

    if sql.upper() == "FLOAT64":
        return pa.float64()

    if sql.upper() == "BOOL":
        return pa.bool_()

    if sql.upper().startswith("ARRAY<") and sql.endswith(">"):
        inner_type = sql[len("ARRAY<") : -1]
        return pa.list_(parse_sql_type(inner_type))

    if sql.upper().startswith("STRUCT<") and sql.endswith(">"):
        inner_fields = parse_sql_fields(sql[len("STRUCT<") : -1])
        return pa.struct(inner_fields)

    raise ValueError(f"Unsupported SQL type: {sql}")


def parse_sql_fields(sql: str) -> tuple[pa.Field]:
    sql = sql.strip()

    start_idx = 0
    nested_depth = 0
    fields: list[pa.field] = []

    for end_idx in range(len(sql)):
        c = sql[end_idx]

        if c == "<":
            nested_depth += 1
        elif c == ">":
            nested_depth -= 1
        elif c == "," and nested_depth == 0:
            field = sql[start_idx:end_idx]
            fields.append(parse_sql_field(field))
            start_idx = end_idx + 1

    # Append the last field
    fields.append(parse_sql_field(sql[start_idx:]))

    return tuple(sorted(fields, key=lambda f: f.name))


def parse_sql_field(sql: str) -> pa.Field:
    sql = sql.strip()

    space_idx = sql.find(" ")

    if space_idx == -1:
        raise ValueError(f"Invalid struct field: {sql}")

    return pa.field(sql[:space_idx].strip(), parse_sql_type(sql[space_idx:]))
