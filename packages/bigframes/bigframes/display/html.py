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

"""HTML rendering for DataFrames and other objects."""

from __future__ import annotations

import html
from typing import Any

import pandas as pd
import pandas.api.types

from bigframes._config import options


def _is_dtype_numeric(dtype: Any) -> bool:
    """Check if a dtype is numeric for alignment purposes."""
    return pandas.api.types.is_numeric_dtype(dtype)


def render_html(
    *,
    dataframe: pd.DataFrame,
    table_id: str,
    orderable_columns: list[str] | None = None,
) -> str:
    """Render a pandas DataFrame to HTML with specific styling."""
    classes = "dataframe table table-striped table-hover"
    table_html = [f'<table border="1" class="{classes}" id="{table_id}">']
    precision = options.display.precision
    orderable_columns = orderable_columns or []

    # Render table head
    table_html.append("  <thead>")
    table_html.append('    <tr style="text-align: left;">')
    for col in dataframe.columns:
        th_classes = []
        if col in orderable_columns:
            th_classes.append("sortable")
        class_str = f'class="{" ".join(th_classes)}"' if th_classes else ""
        header_div = (
            '<div style="resize: horizontal; overflow: auto; '
            "box-sizing: border-box; width: 100%; height: 100%; "
            'padding: 0.5em;">'
            f"{html.escape(str(col))}"
            "</div>"
        )
        table_html.append(
            f'      <th style="text-align: left;" {class_str}>{header_div}</th>'
        )
    table_html.append("    </tr>")
    table_html.append("  </thead>")

    # Render table body
    table_html.append("  <tbody>")
    for i in range(len(dataframe)):
        table_html.append("    <tr>")
        row = dataframe.iloc[i]
        for col_name, value in row.items():
            dtype = dataframe.dtypes.loc[col_name]  # type: ignore
            align = "right" if _is_dtype_numeric(dtype) else "left"
            table_html.append(
                '      <td style="text-align: {}; padding: 0.5em;">'.format(align)
            )

            # TODO(b/438181139): Consider semi-exploding ARRAY/STRUCT columns
            # into multiple rows/columns like the BQ UI does.
            if pandas.api.types.is_scalar(value) and pd.isna(value):
                table_html.append('        <em style="color: gray;">&lt;NA&gt;</em>')
            else:
                if isinstance(value, float):
                    formatted_value = f"{value:.{precision}f}"
                    table_html.append(f"        {html.escape(formatted_value)}")
                else:
                    table_html.append(f"        {html.escape(str(value))}")
            table_html.append("      </td>")
        table_html.append("    </tr>")
    table_html.append("  </tbody>")
    table_html.append("</table>")

    return "\n".join(table_html)
