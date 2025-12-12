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
from importlib import resources
import functools
import math
from typing import Any, Dict, Iterator, List, Optional, Type
import uuid

import pandas as pd

import bigframes
from bigframes.core import blocks
import bigframes.dataframe
import bigframes.display.html
import bigframes.dtypes as dtypes

# anywidget and traitlets are optional dependencies. We don't want the import of
# this module to fail if they aren't installed, though. Instead, we try to
# limit the surface that these packages could affect. This makes unit testing
# easier and ensures we don't accidentally make these required packages.
try:
    import anywidget
    import traitlets

    ANYWIDGET_INSTALLED = True
except Exception:
    ANYWIDGET_INSTALLED = False

WIDGET_BASE: Type[Any]
if ANYWIDGET_INSTALLED:
    WIDGET_BASE = anywidget.AnyWidget
else:
    WIDGET_BASE = object


@dataclasses.dataclass(frozen=True)
class _SortState:
    column: str
    ascending: bool


class TableWidget(WIDGET_BASE):
    """An interactive, paginated table widget for BigFrames DataFrames.

    This widget provides a user-friendly way to display and navigate through
    large BigQuery DataFrames within a Jupyter environment.
    """

    page = traitlets.Int(0).tag(sync=True)
    page_size = traitlets.Int(0).tag(sync=True)
    row_count = traitlets.Union(
        [traitlets.Int(), traitlets.Instance(type(None))],
        default_value=None,
        allow_none=True,
    ).tag(sync=True)
    table_html = traitlets.Unicode().tag(sync=True)
    sort_column = traitlets.Unicode("").tag(sync=True)
    sort_ascending = traitlets.Bool(True).tag(sync=True)
    orderable_columns = traitlets.List(traitlets.Unicode(), []).tag(sync=True)
    _initial_load_complete = traitlets.Bool(False).tag(sync=True)
    _batches: Optional[blocks.PandasBatches] = None
    _error_message = traitlets.Unicode(allow_none=True, default_value=None).tag(
        sync=True
    )

    def __init__(self, dataframe: bigframes.dataframe.DataFrame):
        """Initialize the TableWidget.

        Args:
            dataframe: The Bigframes Dataframe to display in the widget.
        """
        if not ANYWIDGET_INSTALLED:
            raise ImportError(
                "Please `pip install anywidget traitlets` or `pip install 'bigframes[anywidget]'` to use TableWidget."
            )

        self._dataframe = dataframe

        super().__init__()

        # Initialize attributes that might be needed by observers first
        self._table_id = str(uuid.uuid4())
        self._all_data_loaded = False
        self._batch_iter: Optional[Iterator[pd.DataFrame]] = None
        self._cached_batches: List[pd.DataFrame] = []
        self._last_sort_state: Optional[_SortState] = None

        # respect display options for initial page size
        initial_page_size = bigframes.options.display.max_rows

        # set traitlets properties that trigger observers
        # TODO(b/462525985): Investigate and improve TableWidget UX for DataFrames with a large number of columns.
        self.page_size = initial_page_size
        # TODO(b/463754889): Support non-string column labels for sorting.
        if all(isinstance(col, str) for col in dataframe.columns):
            self.orderable_columns = [
                str(col_name)
                for col_name, dtype in dataframe.dtypes.items()
                if dtypes.is_orderable(dtype)
            ]
        else:
            self.orderable_columns = []

        # obtain the row counts
        # TODO(b/428238610): Start iterating over the result of `to_pandas_batches()`
        # before we get here so that the count might already be cached.
        self._reset_batches_for_new_page_size()

        if self._batches is None:
            self._error_message = "Could not retrieve data batches. Data might be unavailable or an error occurred."
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

        # Signals to the frontend that the initial data load is complete.
        # Also used as a guard to prevent observers from firing during initialization.
        self._initial_load_complete = True

    @traitlets.observe("_initial_load_complete")
    def _on_initial_load_complete(self, change: Dict[str, Any]):
        if change["new"]:
            self._set_table_html()

    @functools.cached_property
    def _esm(self):
        """Load JavaScript code from external file."""
        return resources.read_text(bigframes.display, "table_widget.js")

    @functools.cached_property
    def _css(self):
        """Load CSS code from external file."""
        return resources.read_text(bigframes.display, "table_widget.css")

    @traitlets.validate("page")
    def _validate_page(self, proposal: Dict[str, Any]) -> int:
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
    def _validate_page_size(self, proposal: Dict[str, Any]) -> int:
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
            return pd.DataFrame(columns=self._dataframe.columns)
        return pd.concat(self._cached_batches)

    def _reset_batch_cache(self) -> None:
        """Resets batch caching attributes."""
        self._cached_batches = []
        self._batch_iter = None
        self._all_data_loaded = False

    def _reset_batches_for_new_page_size(self) -> None:
        """Reset the batch iterator when page size changes."""
        self._batches = self._dataframe._to_pandas_batches(page_size=self.page_size)

        self._reset_batch_cache()

    def _set_table_html(self) -> None:
        """Sets the current html data based on the current page and page size."""
        if self._error_message:
            self.table_html = (
                f"<div class='bigframes-error-message'>{self._error_message}</div>"
            )
            return

        # Apply sorting if a column is selected
        df_to_display = self._dataframe
        if self.sort_column:
            # TODO(b/463715504): Support sorting by index columns.
            df_to_display = df_to_display.sort_values(
                by=self.sort_column, ascending=self.sort_ascending
            )

        # Reset batches when sorting changes
        if self._last_sort_state != _SortState(self.sort_column, self.sort_ascending):
            self._batches = df_to_display._to_pandas_batches(page_size=self.page_size)
            self._reset_batch_cache()
            self._last_sort_state = _SortState(self.sort_column, self.sort_ascending)
            self.page = 0  # Reset to first page

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

        # Handle index display
        # TODO(b/438181139): Add tests for custom multiindex
        if self._dataframe._block.has_index:
            index_name = page_data.index.name
            page_data.insert(
                0, index_name if index_name is not None else "", page_data.index
            )
        else:
            # Default index - include as "Row" column
            page_data.insert(0, "Row", range(start + 1, start + len(page_data) + 1))
        # Handle case where user navigated beyond available data with unknown row count
        is_unknown_count = self.row_count is None
        is_beyond_data = self._all_data_loaded and len(page_data) == 0 and self.page > 0
        if is_unknown_count and is_beyond_data:
            # Calculate the last valid page (zero-indexed)
            total_rows = len(cached_data)
            if total_rows > 0:
                last_valid_page = max(0, math.ceil(total_rows / self.page_size) - 1)
                # Navigate back to the last valid page
                self.page = last_valid_page
                # Recursively call to display the correct page
                return self._set_table_html()
            else:
                # If no data at all, stay on page 0 with empty display
                self.page = 0
                return self._set_table_html()

        # Generate HTML table
        self.table_html = bigframes.display.html.render_html(
            dataframe=page_data,
            table_id=f"table-{self._table_id}",
            orderable_columns=self.orderable_columns,
        )

    @traitlets.observe("sort_column", "sort_ascending")
    def _sort_changed(self, _change: Dict[str, Any]):
        """Handler for when sorting parameters change from the frontend."""
        self._set_table_html()

    @traitlets.observe("page")
    def _page_changed(self, _change: Dict[str, Any]) -> None:
        """Handler for when the page number is changed from the frontend."""
        if not self._initial_load_complete:
            return
        self._set_table_html()

    @traitlets.observe("page_size")
    def _page_size_changed(self, _change: Dict[str, Any]) -> None:
        """Handler for when the page size is changed from the frontend."""
        if not self._initial_load_complete:
            return
        # Reset the page to 0 when page size changes to avoid invalid page states
        self.page = 0
        # Reset the sort state to default (no sort)
        self.sort_column = ""
        self.sort_ascending = True

        # Reset batches to use new page size for future data fetching
        self._reset_batches_for_new_page_size()

        # Update the table display
        self._set_table_html()
