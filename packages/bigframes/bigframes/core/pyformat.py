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
from typing import Any, Optional, Union

import google.cloud.bigquery
import pandas

from bigframes.core import utils
import bigframes.core.local_data
from bigframes.core.tools import bigquery_schema
import bigframes.session

_BQ_TABLE_TYPES = Union[
    google.cloud.bigquery.Table,
    google.cloud.bigquery.TableReference,
    google.cloud.bigquery.table.TableListItem,
]


def _table_to_sql(table: _BQ_TABLE_TYPES) -> str:
    return f"`{table.project}`.`{table.dataset_id}`.`{table.table_id}`"


def _pandas_df_to_sql_dry_run(pd_df: pandas.DataFrame) -> str:
    # Ensure there are no duplicate column labels.
    #
    # Please make sure this stays in sync with the logic used to_gbq(). See
    # bigframes.dataframe.DataFrame._prepare_export().
    new_col_labels, new_idx_labels = utils.get_standardized_ids(
        pd_df.columns, pd_df.index.names
    )
    pd_copy = pd_df.copy()
    pd_copy.columns = pandas.Index(new_col_labels)
    pd_copy.index.names = new_idx_labels

    managed_table = bigframes.core.local_data.ManagedArrowTable.from_pandas(pd_copy)
    bqschema = managed_table.schema.to_bigquery()
    return bigquery_schema.to_sql_dry_run(bqschema)


def _pandas_df_to_sql(
    df_pd: pandas.DataFrame,
    *,
    name: str,
    session: Optional[bigframes.session.Session] = None,
    dry_run: bool = False,
) -> str:
    if session is None:
        if not dry_run:
            message = (
                f"Can't embed pandas DataFrame {name} in a SQL "
                "string without a bigframes session except if for a dry run."
            )
            raise ValueError(message)

        return _pandas_df_to_sql_dry_run(df_pd)

    # Use the _deferred engine to avoid loading data too often during dry run.
    df = session.read_pandas(df_pd, write_engine="_deferred")
    return _table_to_sql(df._to_placeholder_table(dry_run=dry_run))


def _field_to_template_value(
    name: str,
    value: Any,
    *,
    session: Optional[bigframes.session.Session] = None,
    dry_run: bool = False,
) -> str:
    """Convert value to something embeddable in a SQL string."""
    import bigframes.core.sql  # Avoid circular imports
    import bigframes.dataframe  # Avoid circular imports

    _validate_type(name, value)

    table_types = typing.get_args(_BQ_TABLE_TYPES)
    if isinstance(value, table_types):
        return _table_to_sql(value)

    if isinstance(value, pandas.DataFrame):
        return _pandas_df_to_sql(value, session=session, dry_run=dry_run, name=name)

    if isinstance(value, bigframes.dataframe.DataFrame):
        return _table_to_sql(value._to_placeholder_table(dry_run=dry_run))

    return bigframes.core.sql.simple_literal(value)


def _validate_type(name: str, value: Any):
    """Raises TypeError if value is unsupported."""
    import bigframes.core.sql  # Avoid circular imports
    import bigframes.dataframe  # Avoid circular imports

    if value is None:
        return  # None can't be used in isinstance, but is a valid literal.

    supported_types = (
        typing.get_args(_BQ_TABLE_TYPES)
        + typing.get_args(bigframes.core.sql.SIMPLE_LITERAL_TYPES)
        + (bigframes.dataframe.DataFrame,)
        + (pandas.DataFrame,)
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
    session: Optional[bigframes.session.Session] = None,
    dry_run: bool = False,
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
        format_kwargs[name] = _field_to_template_value(
            name, value, session=session, dry_run=dry_run
        )

    return sql_template.format(**format_kwargs)
