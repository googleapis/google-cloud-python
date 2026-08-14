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
from typing import Any, Optional, Tuple, Union

import google.cloud.bigquery
import pandas

import bigframes.core.local_data
import bigframes.session
from bigframes.core import utils
from bigframes.core.tools import bigquery_schema

_BQ_TABLE_TYPES = Union[
    google.cloud.bigquery.Table,
    google.cloud.bigquery.TableReference,
    google.cloud.bigquery.table.TableListItem,
]


def _table_to_sql(table: _BQ_TABLE_TYPES) -> str:
    # BiglakeIcebergTable IDs have 4 parts. BigFrames packs catalog.namespace
    # into the dataset_id.
    dataset_parts = table.dataset_id.split(".")
    dataset_sql = ".".join(f"`{part}`" for part in dataset_parts)
    return f"`{table.project}`.{dataset_sql}.`{table.table_id}`"


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
    import bigframes.core.compile.sqlglot.sql as sql  # Avoid circular imports
    import bigframes.dataframe  # Avoid circular imports

    _validate_type(name, value)

    table_types = typing.get_args(_BQ_TABLE_TYPES)
    if isinstance(value, table_types):
        return _table_to_sql(value)

    if isinstance(value, pandas.DataFrame):
        return _pandas_df_to_sql(value, session=session, dry_run=dry_run, name=name)

    if isinstance(value, bigframes.dataframe.DataFrame):
        import bigframes.core.bq_data as bq_data
        import bigframes.core.nodes as nodes

        # TODO(b/493608478): Remove this workaround for BigLake/Iceberg tables,
        # which cannot currently be used in views, once a fix rolls out.
        def is_biglake(
            node: nodes.BigFrameNode, child_results: Tuple[bool, ...]
        ) -> bool:
            if isinstance(node, nodes.ReadTableNode):
                return isinstance(node.source.table, bq_data.BiglakeIcebergTable)
            return any(child_results)

        contains_biglake = value._block.expr.node.reduce_up(is_biglake)

        if contains_biglake:
            sql_query, _, _ = value._to_sql_query(include_index=True)
            return f"({sql_query})"

        return _table_to_sql(value._to_placeholder_table(dry_run=dry_run))

    if isinstance(value, str):
        return value

    return sql.to_sql(sql.literal(value))


def _validate_type(name: str, value: Any):
    """Raises TypeError if value is unsupported."""
    import bigframes.dataframe  # Avoid circular imports
    import bigframes.dtypes  # Avoid circular imports

    if value is None:
        return  # None can't be used in isinstance, but is a valid literal.

    supported_types = (
        typing.get_args(_BQ_TABLE_TYPES)
        + bigframes.dtypes.SUPPORTED_LITERAL_TYPES
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


def _is_escaped_open_brace(sql_template: str, idx: int, literal_char: str) -> bool:
    """Checks if the character at idx in sql_template is an escaped open brace '{{'."""
    return sql_template[idx : idx + 2] == "{{" and literal_char == "{"


def _is_escaped_close_brace(sql_template: str, idx: int, literal_char: str) -> bool:
    """Checks if the character at idx in sql_template is an escaped close brace '}}'."""
    return sql_template[idx : idx + 2] == "}}" and literal_char == "}"


def _consume_literal(sql_template: str, current_idx: int, literal_text: str) -> int:
    """Advances current_idx past literal_text in sql_template, accounting for escaped braces.

    A **literal** (or literal text) is the static part of the template string that
    does not contain formatting placeholders. The string.Formatter parser resolves
    escaped braces ('{{' and '}}') into single braces ('{' and '}') in its output
    literal_text.

    This function aligns the resolved literal_text back to the original
    sql_template by consuming 2 characters from sql_template ('{{' or '}}') for
    every single escaped brace character in literal_text, and 1 character for
    everything else.

    Returns:
        int: the advanced current_idx in sql_template.
    """
    lit_idx = 0
    while lit_idx < len(literal_text):
        if _is_escaped_open_brace(sql_template, current_idx, literal_text[lit_idx]):
            current_idx += 2
            lit_idx += 1
        elif _is_escaped_close_brace(sql_template, current_idx, literal_text[lit_idx]):
            current_idx += 2
            lit_idx += 1
        elif (
            current_idx < len(sql_template)
            and sql_template[current_idx] == literal_text[lit_idx]
        ):
            current_idx += 1
            lit_idx += 1
        else:
            raise RuntimeError(
                "Internal error: failed to align parsed SQL template with original query. "
                f"Expected {literal_text[lit_idx]!r} at position {current_idx} in template, "
                f"but found {sql_template[current_idx : current_idx + 2]!r}."
            )
    return current_idx


def _is_escaped_brace(sql_template: str, idx: int) -> bool:
    """Checks if the template has an escaped brace ('{{' or '}}') at the given index."""
    return sql_template[idx : idx + 2] in ("{{", "}}")


def _advance_past_field(sql_template: str, current_idx: int) -> int:
    """Advances current_idx past the format field starting at current_idx.

    A **field** (or replacement field) is a placeholder in the template enclosed
    in braces (e.g., "{my_var}" or "{json_col: { "val": 1 } }").

    This function assumes current_idx points to the opening '{' of a field.
    It parses forward, tracking nested braces to find the matching closing '}'
    that terminates the field, while ignoring escaped braces ('{{' and '}}')
    which do not affect the nesting level.

    Returns:
        int: the index immediately after the closing '}' of the field.
    """
    assert sql_template[current_idx] == "{"
    brace_count = 1
    current_idx += 1  # past '{'

    while brace_count > 0 and current_idx < len(sql_template):
        if _is_escaped_brace(sql_template, current_idx):
            current_idx += 2
        elif sql_template[current_idx] == "{":
            brace_count += 1
            current_idx += 1
        elif sql_template[current_idx] == "}":
            brace_count -= 1
            current_idx += 1
        else:
            current_idx += 1

    return current_idx


def _find_all_field_positions(sql_template: str) -> dict[tuple[str, int], int]:
    """Finds the character positions of all fields in the sql_template.

    Returns:
        dict: a dict mapping (field_name, occurrence_idx) to character index.
    """
    formatter = string.Formatter()
    current_idx = 0
    seen_counts: dict[str, int] = {}
    positions: dict[tuple[str, int], int] = {}

    for literal_text, field_name, _, _ in formatter.parse(sql_template):
        current_idx = _consume_literal(sql_template, current_idx, literal_text)

        if field_name is not None:
            occurrence_idx = seen_counts.get(field_name, 0)
            seen_counts[field_name] = occurrence_idx + 1

            positions[(field_name, occurrence_idx)] = current_idx

            current_idx = _advance_past_field(sql_template, current_idx)

    return positions


def get_error_context_at_pos(sql_template: str, pos: int) -> str:
    """Create a helpful 'pointer' to where the problematic position is
    in the original SQL.

    This should make the error message a lot friendlier, by providing more
    context towards the problematic syntax.
    """
    if pos == -1:
        return ""

    lines = sql_template.splitlines(keepends=True)

    char_count = 0
    target_line_idx = -1
    for i, line in enumerate(lines):
        if char_count <= pos < char_count + len(line):
            target_line_idx = i
            break
        char_count += len(line)

    if target_line_idx == -1:
        return ""

    col_offset = pos - char_count

    context_lines = []
    start_line = max(0, target_line_idx - 2)
    end_line = min(len(lines), target_line_idx + 3)

    for i in range(start_line, end_line):
        line_num = i + 1
        line_content = lines[i].rstrip("\r\n")
        if i == target_line_idx:
            context_lines.append(f"{line_num:4d}: {line_content}")
            indent = 6 + col_offset
            context_lines.append(" " * indent + "^")
        else:
            context_lines.append(f"{line_num:4d}: {line_content}")

    return "\n".join(context_lines)


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
        ValueError:
            if a referenced variable is not found (KeyError is caught and raised
            as ValueError with context).
    """
    try:
        fields = _parse_fields(sql_template)
    except ValueError as e:
        raise ValueError(
            "Failed to parse SQL template. "
            "Did you mean to escape '{' and '}' by doubling them?\n"
            f"Error details: {e}"
        ) from e

    format_kwargs: dict[str, str] = {}
    seen_counts: dict[str, int] = {}
    for name in fields:
        seen_counts[name] = seen_counts.get(name, 0) + 1
        try:
            value = pyformat_args[name]
        except KeyError as e:
            positions = _find_all_field_positions(sql_template)
            occurrence_idx = seen_counts[name] - 1
            pos = positions.get((name, occurrence_idx), -1)
            context = get_error_context_at_pos(sql_template, pos)
            raise ValueError(
                f"Undetected variable {name!r} in SQL template. "
                "Did you mean to escape '{' and '}' by doubling them?\n"
                f"{context}"
            ) from e

        format_kwargs[name] = _field_to_template_value(
            name, value, session=session, dry_run=dry_run
        )

    return sql_template.format(**format_kwargs)
