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

"""Helpers for the pyformat feature."""

# TODO(tswast): consolidate with pandas-gbq and bigquery-magics. See:
# https://github.com/googleapis/python-bigquery-magics/blob/main/bigquery_magics/pyformat.py

from __future__ import annotations

import string
import typing
from typing import Any, Union

import google.cloud.bigquery
import google.cloud.bigquery.table

_BQ_TABLE_TYPES = Union[
    google.cloud.bigquery.Table,
    google.cloud.bigquery.TableReference,
    google.cloud.bigquery.table.TableListItem,
]


def _table_to_sql(table: _BQ_TABLE_TYPES) -> str:
    return f"`{table.project}`.`{table.dataset_id}`.`{table.table_id}`"


def _field_to_template_value(name: str, value: Any) -> str:
    """Convert value to something embeddable in a SQL string."""
    import bigframes.core.sql  # Avoid circular imports

    _validate_type(name, value)

    table_types = typing.get_args(_BQ_TABLE_TYPES)
    if isinstance(value, table_types):
        return _table_to_sql(value)

    # TODO(tswast): convert DataFrame objects to gbq tables or a literals subquery.
    return bigframes.core.sql.simple_literal(value)


def _validate_type(name: str, value: Any):
    """Raises TypeError if value is unsupported."""
    import bigframes.core.sql  # Avoid circular imports

    if value is None:
        return  # None can't be used in isinstance, but is a valid literal.

    supported_types = typing.get_args(_BQ_TABLE_TYPES) + typing.get_args(
        bigframes.core.sql.SIMPLE_LITERAL_TYPES
    )
    if not isinstance(value, supported_types):
        raise TypeError(
            f"{name} has unsupported type: {type(value)}. "
            f"Only {supported_types} are supported."
        )


def _parse_fields(sql_template: str) -> list[str]:
    return [
        field_name
        for _, field_name, _, _ in string.Formatter().parse(sql_template)
        if field_name is not None
    ]


def pyformat(
    sql_template: str,
    *,
    pyformat_args: dict,
    # TODO: add dry_run parameter to avoid expensive API calls in conversion
    # TODO: and session to upload data / convert to table if necessary
) -> str:
    """Unsafe Python-style string formatting of SQL string.

    Only some data types supported.

    Warning: strings are **not** escaped. This allows them to be used in
    contexts such as table identifiers, where normal query parameters are not
    supported.

    Args:
        sql_template (str):
            SQL string with 0+ {var_name}-style format options.
        pyformat_args (dict):
            Variable namespace to use for formatting.

    Raises:
        TypeError: if a referenced variable is not of a supported type.
        KeyError: if a referenced variable is not found.
    """
    fields = _parse_fields(sql_template)

    format_kwargs = {}
    for name in fields:
        value = pyformat_args[name]
        format_kwargs[name] = _field_to_template_value(name, value)

    return sql_template.format(**format_kwargs)
