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

"""Interactive, paginated table widget for BigFrames DataFrames."""

from __future__ import annotations

import dataclasses
import functools
import logging

logger = logging.getLogger(__name__)
import math
import threading
import uuid
import warnings
from importlib import resources
from typing import Any, Iterator, Optional

import pandas as pd

import bigframes
import bigframes.dataframe
import bigframes.display.html
import bigframes.dtypes as dtypes
from bigframes.core import blocks

# anywidget and traitlets are optional dependencies. We don't want the import of
# this module to fail if they aren't installed, though. Instead, we try to
# limit the surface that these packages could affect. This makes unit testing
# easier and ensures we don't accidentally make these required packages.
try:
    import anywidget
    import traitlets

    _ANYWIDGET_INSTALLED = True
except Exception:
    _ANYWIDGET_INSTALLED = False

_WIDGET_BASE: type[Any]
if _ANYWIDGET_INSTALLED:
    _WIDGET_BASE = anywidget.AnyWidget
else:
    _WIDGET_BASE = object


@dataclasses.dataclass(frozen=True)
class _SortState:
    columns: tuple[str, ...]
    ascending: tuple[bool, ...]


@dataclasses.dataclass
class _ExecutionResult:
    df_to_set: Optional[bigframes.dataframe.DataFrame] = None
    orderable_cols: Optional[list[str]] = None
    batches: Optional[blocks.PandasBatches] = None
    batch_iter: Optional[Iterator[pd.DataFrame]] = None
    cached_batches: Optional[list[pd.DataFrame]] = None
    all_data_loaded: bool = False
    total_rows: Optional[int] = None
    initial_html: Optional[str] = None
    error_message: Optional[str] = None


class TableWidget(_WIDGET_BASE):
    """An interactive, paginated table widget for BigFrames DataFrames.

    This widget provides a user-friendly way to display and navigate through
    large BigQuery DataFrames within a Jupyter environment.
    """

    page = traitlets.Int(0).tag(sync=True)
    page_size = traitlets.Int(0).tag(sync=True)
    max_columns = traitlets.Int(allow_none=True, default_value=None).tag(sync=True)
    row_count = traitlets.Int(allow_none=True, default_value=None).tag(sync=True)
    table_html = traitlets.Unicode("").tag(sync=True)
    sort_context = traitlets.List(traitlets.Dict(), default_value=[]).tag(sync=True)
    orderable_columns = traitlets.List(traitlets.Unicode(), []).tag(sync=True)
    _initial_load_complete = traitlets.Bool(False).tag(sync=True)
    _batches: Optional[blocks.PandasBatches] = None
    _error_message = traitlets.Unicode(allow_none=True, default_value=None).tag(
        sync=True
    )
    start_execution = traitlets.Bool(False).tag(sync=True)
    is_deferred_mode = traitlets.Bool(False).tag(sync=True)
    dry_run_info = traitlets.Unicode("").tag(sync=True)
    ping = traitlets.Int(0).tag(sync=True)

    def __init__(
        self,
        dataframe: (
            bigframes.dataframe.DataFrame
            | bigframes.session.deferred.DeferredBigQueryDataFrame
        ),
        dry_run_info: Optional[str] = None,
    ):
        """Initialize the TableWidget.

        Args:
            dataframe: The Bigframes Dataframe to display in the widget.
        """
        if not _ANYWIDGET_INSTALLED:
            raise ImportError(
                "Please `pip install anywidget traitlets` or "
                "`pip install 'bigframes[anywidget]'` to use TableWidget."
            )

        # Enable third-party widgets manager in Google Colab environment.
        try:
            import sys

            if "google.colab" in sys.modules:
                from google.colab import output

                output.enable_custom_widget_manager()
        except Exception:
            pass

        from bigframes.session import deferred

        is_deferred = False
        deferred_df = None
        df = None

        if isinstance(dataframe, deferred.DeferredBigQueryDataFrame):
            is_deferred = True
            deferred_df = dataframe
        elif bigframes.options.display.repr_mode == "deferred":
            is_deferred = True
            df = dataframe
        else:
            df = dataframe

        from bigframes.core.utils import get_ipython_execution_count

        self._cell_execution_count = get_ipython_execution_count()

        super().__init__()

        self.is_deferred_mode = is_deferred
        self._deferred_dataframe = deferred_df
        self._dataframe = df

        if dry_run_info:
            self.dry_run_info = dry_run_info

        # Initialize attributes that might be needed by observers first
        self._table_id = str(uuid.uuid4())
        self._all_data_loaded = False
        self._batch_iter: Optional[Iterator[pd.DataFrame]] = None
        self._cached_batches: list[pd.DataFrame] = []
        self._last_sort_state: Optional[_SortState] = None
        self._execution_result: Optional[_ExecutionResult] = None
        # Lock to ensure only one thread at a time is updating the table HTML.
        self._setting_html_lock = threading.Lock()

        # respect display options for initial page size
        initial_page_size = bigframes.options.display.max_rows
        initial_max_columns = bigframes.options.display.max_columns

        self.page_size = initial_page_size
        self.max_columns = initial_max_columns

        if not self.is_deferred_mode:
            self._initialize_from_dataframe()

        # Signals to the frontend that the initial data load is complete.
        # Also used as a guard to prevent observers from firing during initialization.
        self._initial_load_complete = True

    @traitlets.observe("start_execution")
    def _on_start_execution(self, change: dict[str, Any]):
        if change["new"]:
            import asyncio

            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                try:
                    import tornado.ioloop  # type: ignore[import-not-found]

                    loop = tornado.ioloop.IOLoop.current().asyncio_loop  # type: ignore[attr-defined]
                except Exception:
                    loop = None

            def run_execution():
                try:
                    self._error_message = None
                    df = None
                    if self.is_deferred_mode:
                        if self._deferred_dataframe is not None:
                            result = self._deferred_dataframe.execute()
                            if isinstance(result, bigframes.series.Series):
                                df = result.to_frame()
                            elif isinstance(result, bigframes.dataframe.DataFrame):
                                df = result
                            else:
                                raise TypeError(
                                    f"Unexpected result type: {type(result)}"
                                )
                        elif self._dataframe is not None:
                            df = self._dataframe
                    else:
                        df = self._dataframe

                    if df is None:
                        raise ValueError("No DataFrame to execute.")

                    df_to_set = df._prepare_display_df()
                    orderable_cols = self._get_orderable_columns(df_to_set)

                    with bigframes.option_context("display.progress_bar", None):
                        batches = df_to_set.to_pandas_batches(
                            page_size=self.page_size,
                            cell_execution_count=self._cell_execution_count,
                        )

                    total_rows = getattr(batches, "total_rows", None)

                    # Fetch the first batch
                    batch_iter = iter(batches)
                    try:
                        initial_batch = next(batch_iter)
                        cached_batches = [initial_batch]
                        all_data_loaded = False
                    except StopIteration:
                        initial_batch = pd.DataFrame(columns=df_to_set.columns)
                        cached_batches = []
                        all_data_loaded = True

                    # Render the HTML
                    page_data = initial_batch.copy()
                    start = 0
                    if df_to_set._block.has_index:
                        is_unnamed_single_index = (
                            page_data.index.name is None
                            and not isinstance(page_data.index, pd.MultiIndex)
                        )
                        page_data = page_data.reset_index()
                        if is_unnamed_single_index and "index" in page_data.columns:
                            page_data.rename(columns={"index": ""}, inplace=True)
                    else:
                        page_data.insert(
                            0, "Row", range(start + 1, start + len(page_data) + 1)
                        )

                    initial_html = bigframes.display.html.render_html(
                        dataframe=page_data,
                        table_id=f"table-{self._table_id}",
                        orderable_columns=orderable_cols,
                        max_columns=self.max_columns,
                    )

                    self._execution_result = _ExecutionResult(
                        df_to_set=df_to_set,
                        orderable_cols=orderable_cols,
                        batches=batches,
                        batch_iter=batch_iter,
                        cached_batches=cached_batches,
                        all_data_loaded=all_data_loaded,
                        total_rows=total_rows,
                        initial_html=initial_html,
                    )
                except Exception as e:
                    logger.warning(f"Error in background execution: {e}")
                    self._execution_result = _ExecutionResult(error_message=str(e))

                import sys

                is_colab = "google.colab" in sys.modules

                if loop is not None and loop.is_running() and not is_colab:
                    loop.call_soon_threadsafe(self._apply_execution_result)
                elif is_colab:
                    # In Google Colab, background thread updates to traitlets are not automatically
                    # synchronized to the frontend. We rely on the frontend's active pinging
                    # (which triggers `_on_ping` on the main kernel thread) to apply the result.
                    pass
                else:
                    self._apply_execution_result()

            self._execution_thread = threading.Thread(target=run_execution, daemon=True)
            self._execution_thread.start()

    def _apply_execution_result(self) -> None:
        if self._execution_result is None:
            return

        result = self._execution_result
        self._execution_result = None

        with self.hold_sync():
            if result.error_message is not None:
                self._error_message = result.error_message
                self.start_execution = False
            else:
                self._dataframe = result.df_to_set
                self.orderable_columns = result.orderable_cols or []
                self._batches = result.batches
                self._batch_iter = result.batch_iter
                self._cached_batches = result.cached_batches or []
                self._all_data_loaded = result.all_data_loaded
                self._last_sort_state = _SortState((), ())
                self.row_count = result.total_rows
                self.table_html = result.initial_html or ""
                self.is_deferred_mode = False
                self.start_execution = False

    @traitlets.observe("ping")
    def _on_ping(self, _change: dict[str, Any]):
        self._apply_execution_result()

    def _initialize_from_dataframe(self):
        if self._dataframe is None:
            return

        self.orderable_columns = self._get_orderable_columns(self._dataframe)

        self._initial_load()

    def _get_orderable_columns(
        self, dataframe: bigframes.dataframe.DataFrame
    ) -> list[str]:
        """Determine which columns can be used for client-side sorting."""
        # TODO(b/469861913): Nested columns from structs (e.g., 'struct_col.name') are not currently sortable.
        # TODO(b/463754889): Support non-string column labels for sorting.
        if not all(isinstance(col, str) for col in dataframe.columns):
            return []

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", bigframes.exceptions.JSONDtypeWarning)
            warnings.simplefilter("ignore", category=FutureWarning)
            return [
                str(col_name)
                for col_name, dtype in dataframe.dtypes.items()
                if dtypes.is_orderable(dtype)
            ]

    def _initial_load(self) -> None:
        """Get initial data and row count."""
        # obtain the row counts
        # TODO(b/428238610): Start iterating over the result of `to_pandas_batches()`
        # before we get here so that the count might already be cached.
        with bigframes.option_context("display.progress_bar", None):
            self._reset_batches_for_new_page_size()

            if self._batches is None:
                self._error_message = (
                    "Could not retrieve data batches. Data might be unavailable or "
                    "an error occurred."
                )
                self.row_count = None
            elif self._batches.total_rows is None:
                # Total rows is unknown, this is an expected state.
                # TODO(b/461536343): Cheaply discover if we have exactly 1 page.
                # There are cases where total rows is not set, but there are no additional
                # pages. We could disable the "next" button in these cases.
                self.row_count = None
            else:
                self.row_count = self._batches.total_rows

            # get the initial page
            self._set_table_html()

    @traitlets.observe("_initial_load_complete")
    def _on_initial_load_complete(self, change: dict[str, Any]):
        if change["new"]:
            self._set_table_html()

    @functools.cached_property
    def _esm(self):
        """Load JavaScript code from the compiled Angular hybrid bundle."""
        return resources.read_text(bigframes.display, "table_widget_angular.js")

    @functools.cached_property
    def _css(self):
        """Load CSS code from external file."""
        return resources.read_text(bigframes.display, "table_widget.css")

    @traitlets.validate("page")
    def _validate_page(self, proposal: dict[str, Any]) -> int:
        """Validate and clamp the page number to a valid range.

        Args:
            proposal: A dictionary from the traitlets library containing the
                proposed change. The new value is in proposal["value"].

        Returns:
            The validated and clamped page number as an integer.
        """
        value = proposal["value"]

        if value < 0:
            raise ValueError("Page number cannot be negative.")

        # If truly empty or invalid page size, stay on page 0.
        # This handles cases where row_count is 0 or page_size is 0, preventing
        # division by zero or nonsensical pagination, regardless of row_count being None.
        if self.row_count == 0 or self.page_size == 0:
            return 0

        # If row count is unknown, allow any non-negative page. The previous check
        # ensures that invalid page_size (0) is already handled.
        if self.row_count is None:
            return value

        # Calculate the zero-indexed maximum page number.
        max_page = max(0, math.ceil(self.row_count / self.page_size) - 1)

        # Clamp the proposed value to the valid range [0, max_page].
        return max(0, min(value, max_page))

    @traitlets.validate("page_size")
    def _validate_page_size(self, proposal: dict[str, Any]) -> int:
        """Validate page size to ensure it's positive and reasonable.

        Args:
            proposal: A dictionary from the traitlets library containing the
                proposed change. The new value is in proposal["value"].

        Returns:
            The validated page size as an integer.
        """
        value = proposal["value"]

        # Ensure page size is positive and within reasonable bounds
        if value <= 0:
            return self.page_size  # Keep current value

        # Cap at reasonable maximum to prevent performance issues
        max_page_size = 1000
        return min(value, max_page_size)

    @traitlets.validate("max_columns")
    def _validate_max_columns(self, proposal: dict[str, Any]) -> int:
        """Validate max columns to ensure it's positive or 0 (for all)."""
        value = proposal["value"]
        if value is None:
            return 0  # Normalize None to 0 for traitlet
        return max(0, value)

    def _get_next_batch(self) -> bool:
        """
        Gets the next batch of data from the generator and appends to cache.

        Returns:
            True if a batch was successfully loaded, False otherwise.
        """
        if self._all_data_loaded:
            return False

        try:
            iterator = self._batch_iterator
            batch = next(iterator)
            self._cached_batches.append(batch)
            return True
        except StopIteration:
            self._all_data_loaded = True
            return False

    @property
    def _batch_iterator(self) -> Iterator[pd.DataFrame]:
        """Lazily initializes and returns the batch iterator."""
        if self._batch_iter is None:
            if self._batches is None:
                self._batch_iter = iter([])
            else:
                self._batch_iter = iter(self._batches)
        return self._batch_iter

    @property
    def _cached_data(self) -> pd.DataFrame:
        """Combine all cached batches into a single DataFrame."""
        if not self._cached_batches:
            if self._dataframe is not None:
                return pd.DataFrame(columns=self._dataframe.columns)
            return pd.DataFrame()
        return pd.concat(self._cached_batches)

    def _reset_batch_cache(self) -> None:
        """Resets batch caching attributes."""
        self._cached_batches = []
        self._batch_iter = None
        self._all_data_loaded = False

    def _reset_batches_for_new_page_size(self) -> None:
        """Reset the batch iterator when page size changes."""
        if self._dataframe is None:
            return
        with bigframes.option_context("display.progress_bar", None):
            self._batches = self._dataframe.to_pandas_batches(
                page_size=self.page_size,
                cell_execution_count=self._cell_execution_count,
            )

        self._reset_batch_cache()

    def _set_table_html(self) -> None:
        """Sets the current html data based on the current page and page size."""
        if self.is_deferred_mode:
            return

        new_page = None
        with (
            self._setting_html_lock,
            bigframes.option_context("display.progress_bar", None),
        ):
            if self._error_message:
                self.table_html = (
                    f"<div class='bigframes-error-message'>{self._error_message}</div>"
                )
                return

            if self._dataframe is None:
                self.table_html = "<div class='bigframes-error-message'>Internal Error: DataFrame is missing.</div>"
                return

            # Apply sorting if a column is selected
            df_to_display = self._dataframe
            sort_columns = [item["column"] for item in self.sort_context]
            sort_ascending = [item["ascending"] for item in self.sort_context]

            if sort_columns:
                # TODO(b/463715504): Support sorting by index columns.
                df_to_display = df_to_display.sort_values(
                    by=sort_columns, ascending=sort_ascending
                )

            # Reset batches when sorting changes
            current_sort_state = _SortState(tuple(sort_columns), tuple(sort_ascending))
            if self._last_sort_state != current_sort_state:
                self._batches = df_to_display.to_pandas_batches(
                    page_size=self.page_size,
                    cell_execution_count=self._cell_execution_count,
                )
                self._reset_batch_cache()
                self._last_sort_state = current_sort_state
                if self.page != 0:
                    new_page = 0  # Reset to first page

            if new_page is None:
                start = self.page * self.page_size
                end = start + self.page_size

                # fetch more data if the requested page is outside our cache
                cached_data = self._cached_data
                while len(cached_data) < end and not self._all_data_loaded:
                    if self._get_next_batch():
                        cached_data = self._cached_data
                    else:
                        break

                # Get the data for the current page
                page_data = cached_data.iloc[start:end].copy()

                # Handle case where user navigated beyond available data with unknown row count
                is_unknown_count = self.row_count is None
                is_beyond_data = (
                    self._all_data_loaded and len(page_data) == 0 and self.page > 0
                )
                if is_unknown_count and is_beyond_data:
                    # Calculate the last valid page (zero-indexed)
                    total_rows = len(cached_data)
                    last_valid_page = max(0, math.ceil(total_rows / self.page_size) - 1)
                    if self.page != last_valid_page:
                        new_page = last_valid_page

            if new_page is None:
                # Handle index display
                if self._dataframe._block.has_index:
                    is_unnamed_single_index = (
                        page_data.index.name is None
                        and not isinstance(page_data.index, pd.MultiIndex)
                    )
                    page_data = page_data.reset_index()
                    if is_unnamed_single_index and "index" in page_data.columns:
                        page_data.rename(columns={"index": ""}, inplace=True)

                # Default index - include as "Row" column if no index was present originally
                if not self._dataframe._block.has_index:
                    page_data.insert(
                        0, "Row", range(start + 1, start + len(page_data) + 1)
                    )

                # Generate HTML table
                self.table_html = bigframes.display.html.render_html(
                    dataframe=page_data,
                    table_id=f"table-{self._table_id}",
                    orderable_columns=self.orderable_columns,
                    max_columns=self.max_columns,
                )

        if new_page is not None:
            # Navigate to the new page. This triggers the observer, which will
            # re-enter _set_table_html. Since we've released the lock, this is safe.
            self.page = new_page

    @traitlets.observe("sort_context")
    def _sort_changed(self, _change: dict[str, Any]):
        """Handler for when sorting parameters change from the frontend."""
        self._set_table_html()

    @traitlets.observe("page")
    def _page_changed(self, _change: dict[str, Any]) -> None:
        """Handler for when the page number is changed from the frontend."""
        if not self._initial_load_complete:
            return
        self._set_table_html()

    @traitlets.observe("page_size")
    def _page_size_changed(self, _change: dict[str, Any]) -> None:
        """Handler for when the page size is changed from the frontend."""
        if not self._initial_load_complete:
            return
        # Reset the page to 0 when page size changes to avoid invalid page states
        self.page = 0
        # Reset the sort state to default (no sort)
        self.sort_context = []

        # Reset batches to use new page size for future data fetching
        self._reset_batches_for_new_page_size()

        # Update the table display
        self._set_table_html()

    @traitlets.observe("max_columns")
    def _max_columns_changed(self, _change: dict[str, Any]) -> None:
        """Handler for when max columns is changed from the frontend."""
        if not self._initial_load_complete:
            return
        self._set_table_html()
