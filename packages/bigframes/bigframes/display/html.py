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
import json
import traceback
import typing
import warnings
from typing import Any, Union

import pandas as pd
import pandas.api.types

import bigframes
import bigframes.formatting_helpers as formatter
from bigframes._config import display_options, options
from bigframes.display import plaintext

if typing.TYPE_CHECKING:
    import bigframes.dataframe
    import bigframes.series


def _is_dtype_numeric(dtype: Any) -> bool:
    """Check if a dtype is numeric for alignment purposes."""
    return pandas.api.types.is_numeric_dtype(dtype)


def render_html(
    *,
    dataframe: pd.DataFrame,
    table_id: str,
    orderable_columns: list[str] | None = None,
    max_columns: int | None = None,
) -> str:
    """Render a pandas DataFrame to HTML with specific styling."""
    orderable_columns = orderable_columns or []
    classes = "dataframe table table-striped table-hover"
    table_html_parts = [f'<table border="1" class="{classes}" id="{table_id}">']

    # Handle column truncation
    columns = list(dataframe.columns)
    if max_columns is not None and max_columns > 0 and len(columns) > max_columns:
        half = max_columns // 2
        left_columns = columns[:half]
        # Ensure we don't take more than available if half is 0 or calculation is weird,
        # but typical case is safe.
        right_count = max_columns - half
        right_columns = columns[-right_count:] if right_count > 0 else []
        show_ellipsis = True
    else:
        left_columns = columns
        right_columns = []
        show_ellipsis = False

    table_html_parts.append(
        _render_table_header(
            dataframe, orderable_columns, left_columns, right_columns, show_ellipsis
        )
    )
    table_html_parts.append(
        _render_table_body(dataframe, left_columns, right_columns, show_ellipsis)
    )
    table_html_parts.append("</table>")
    return "".join(table_html_parts)


def _render_table_header(
    dataframe: pd.DataFrame,
    orderable_columns: list[str],
    left_columns: list[Any],
    right_columns: list[Any],
    show_ellipsis: bool,
) -> str:
    """Render the header of the HTML table."""
    header_parts = ["  <thead>", "    <tr>"]

    def render_col_header(col):
        th_classes = []
        if col in orderable_columns:
            th_classes.append("sortable")
        class_str = f'class="{" ".join(th_classes)}"' if th_classes else ""
        header_parts.append(
            f'      <th {class_str}><div class="bf-header-content">'
            f"{html.escape(str(col))}</div></th>"
        )

    for col in left_columns:
        render_col_header(col)

    if show_ellipsis:
        header_parts.append(
            '      <th><div class="bf-header-content" style="cursor: default;">...</div></th>'
        )

    for col in right_columns:
        render_col_header(col)

    header_parts.extend(["    </tr>", "  </thead>"])
    return "\n".join(header_parts)


def _render_table_body(
    dataframe: pd.DataFrame,
    left_columns: list[Any],
    right_columns: list[Any],
    show_ellipsis: bool,
) -> str:
    """Render the body of the HTML table."""
    body_parts = ["  <tbody>"]
    precision = options.display.precision

    for i in range(len(dataframe)):
        body_parts.append("    <tr>")
        row = dataframe.iloc[i]

        def render_col_cell(col_name):
            value = row[col_name]
            dtype = dataframe.dtypes.loc[col_name]  # type: ignore
            align = "right" if _is_dtype_numeric(dtype) else "left"

            # TODO(b/438181139): Consider semi-exploding ARRAY/STRUCT columns
            # into multiple rows/columns like the BQ UI does.
            if pandas.api.types.is_scalar(value) and pd.isna(value):
                body_parts.append(
                    f'      <td class="cell-align-{align}">'
                    '<em class="null-value">&lt;NA&gt;</em></td>'
                )
            else:
                if isinstance(value, float):
                    cell_content = f"{value:.{precision}f}"
                else:
                    cell_content = str(value)
                body_parts.append(
                    f'      <td class="cell-align-{align}">'
                    f"{html.escape(cell_content)}</td>"
                )

        for col in left_columns:
            render_col_cell(col)

        if show_ellipsis:
            # Ellipsis cell
            body_parts.append('      <td class="cell-align-left">...</td>')

        for col in right_columns:
            render_col_cell(col)

        body_parts.append("    </tr>")
    body_parts.append("  </tbody>")
    return "\n".join(body_parts)


def _obj_ref_rt_to_html(obj_ref_rt: str) -> str:
    obj_ref_rt_json = json.loads(obj_ref_rt)
    obj_ref_details = obj_ref_rt_json["objectref"]["details"]
    if "gcs_metadata" in obj_ref_details:
        gcs_metadata = obj_ref_details["gcs_metadata"]
        content_type = typing.cast(str, gcs_metadata.get("content_type", ""))
        if content_type.startswith("image"):
            size_str = ""
            if options.display.blob_display_width:
                size_str = f' width="{options.display.blob_display_width}"'
            if options.display.blob_display_height:
                size_str = size_str + f' height="{options.display.blob_display_height}"'
            url = obj_ref_rt_json["access_urls"]["read_url"]
            return f'<img src="{url}"{size_str}>'

    return f"uri: {obj_ref_rt_json['objectref']['uri']}, authorizer: {obj_ref_rt_json['objectref']['authorizer']}"


def create_html_representation(
    obj: Union[bigframes.dataframe.DataFrame, bigframes.series.Series],
    pandas_df: pd.DataFrame,
    total_rows: int,
    total_columns: int,
) -> str:
    """Create an HTML representation of the DataFrame or Series."""
    import bigframes.series

    opts = options.display
    with display_options.pandas_repr(opts):
        if isinstance(obj, bigframes.series.Series):
            pd_series = pandas_df.iloc[:, 0]
            try:
                html_string = pd_series._repr_html_()
            except AttributeError:
                html_string = f"<pre>{pd_series.to_string()}</pre>"

            is_truncated = total_rows is not None and total_rows > len(pandas_df)
            if is_truncated:
                html_string += f"<p>[{total_rows} rows]</p>"
            return html_string
        else:
            # _repr_html_ stub is missing so mypy thinks it's a Series. Ignore mypy.
            html_string = pandas_df._repr_html_()  # type:ignore

            html_string += f"[{total_rows} rows x {total_columns} columns in total]"
            return html_string


def _get_obj_metadata(
    obj: Union[bigframes.dataframe.DataFrame, bigframes.series.Series],
) -> tuple[bool, bool]:
    import bigframes.series

    is_series = isinstance(obj, bigframes.series.Series)
    if is_series:
        has_index = len(obj._block.index_columns) > 0
    else:
        has_index = obj._has_index
    return is_series, has_index


def get_anywidget_bundle(
    obj: Union[bigframes.dataframe.DataFrame, bigframes.series.Series],
    include=None,
    exclude=None,
    dry_run_info: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Helper method to create and return the anywidget mimebundle.
    This function encapsulates the logic for anywidget display.
    """
    import bigframes.series
    from bigframes import display

    if isinstance(obj, bigframes.series.Series):
        df = obj.to_frame()
    else:
        df = obj

    from bigframes.session import deferred

    if (
        not isinstance(df, deferred.DeferredBigQueryDataFrame)
        and bigframes.options.display.repr_mode != "deferred"
    ):
        display_df = df._prepare_display_df()
    else:
        display_df = df

    widget = display.TableWidget(display_df, dry_run_info=dry_run_info)
    widget_repr_result = widget._repr_mimebundle_(include=include, exclude=exclude)

    if isinstance(widget_repr_result, tuple):
        widget_repr, widget_metadata = widget_repr_result
    else:
        widget_repr = widget_repr_result
        widget_metadata = {}

    widget_repr = dict(widget_repr)

    # Use cached data from widget to render HTML and plain text versions.
    cached_pd = widget._cached_data
    total_rows = widget.row_count
    total_columns = len(df.columns)

    if dry_run_info:
        widget_repr["text/plain"] = dry_run_info
    else:
        widget_repr["text/html"] = create_html_representation(
            obj,
            cached_pd,
            total_rows,
            total_columns,
        )
        is_series, has_index = _get_obj_metadata(obj)
        widget_repr["text/plain"] = plaintext.create_text_representation(
            cached_pd,
            total_rows,
            is_series=is_series,
            has_index=has_index,
            column_count=len(df.columns) if not is_series else 0,
        )

    return widget_repr, widget_metadata


def repr_mimebundle_deferred(
    obj: Union[bigframes.dataframe.DataFrame, bigframes.series.Series],
) -> dict[str, str]:
    return {
        "text/plain": formatter.repr_query_job(obj._compute_dry_run()),
        "text/html": formatter.repr_query_job_html(obj._compute_dry_run()),
    }


def repr_mimebundle_head(
    obj: Union[bigframes.dataframe.DataFrame, bigframes.series.Series],
) -> dict[str, str]:
    import bigframes.series

    opts = options.display
    if isinstance(obj, bigframes.series.Series):
        df = obj.to_frame()
    else:
        df = obj

    df = df._prepare_display_df()
    pandas_df, row_count, query_job = df._block.retrieve_repr_request_results(
        opts.max_rows
    )

    obj._set_internal_query_job(query_job)
    column_count = len(pandas_df.columns)

    html_string = create_html_representation(obj, pandas_df, row_count, column_count)

    is_series, has_index = _get_obj_metadata(obj)
    text_representation = plaintext.create_text_representation(
        pandas_df,
        row_count,
        is_series=is_series,
        has_index=has_index,
        column_count=len(pandas_df.columns) if not is_series else 0,
    )

    return {"text/html": html_string, "text/plain": text_representation}


def repr_mimebundle(
    obj: Union[bigframes.dataframe.DataFrame, bigframes.series.Series],
    include=None,
    exclude=None,
):
    """Custom display method for IPython/Jupyter environments."""
    # TODO(b/467647693): Anywidget integration has been tested in Jupyter, VS Code, and
    # BQ Studio, but there is a known compatibility issue with Marimo that needs to be addressed.

    opts = options.display
    if (
        opts.render_mode == "anywidget"
        or opts.repr_mode == "anywidget"
        or opts.repr_mode == "deferred"
    ):
        try:
            with bigframes.option_context("display.progress_bar", None):
                with warnings.catch_warnings():
                    warnings.simplefilter(
                        "ignore", category=bigframes.exceptions.JSONDtypeWarning
                    )
                    warnings.simplefilter("ignore", category=FutureWarning)
                    dry_run_info = None
                    if opts.repr_mode == "deferred":
                        dry_run_job = obj._compute_dry_run()
                        dry_run_info = formatter.repr_query_job(dry_run_job)
                    return get_anywidget_bundle(
                        obj,
                        include=include,
                        exclude=exclude,
                        dry_run_info=dry_run_info,
                    )
        except Exception:
            # Anywidget is an optional dependency, so warn rather than fail.
            # TODO(shuowei): When Anywidget becomes the default for all repr modes,
            # remove this warning.
            warnings.warn(
                "Anywidget mode is not available or failed to load. "
                "Please `pip install anywidget traitlets` or "
                "`pip install 'bigframes[anywidget]'` to use interactive tables. "
                f"Falling back to static HTML. Error: {traceback.format_exc()}"
            )
            if opts.repr_mode == "deferred":
                return repr_mimebundle_deferred(obj)

    bundle = repr_mimebundle_head(obj)
    if opts.render_mode == "plaintext":
        bundle.pop("text/html", None)

    return bundle
