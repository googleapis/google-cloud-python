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

from __future__ import annotations

from importlib import resources
import functools
import math
from typing import Any, Dict, Iterator, List, Optional, Type
import uuid

import pandas as pd

import bigframes

# anywidget and traitlets are optional dependencies. We don't want the import of this
# module to fail if they aren't installed, though. Instead, we try to limit the surface that
# these packages could affect. This makes unit testing easier and ensures we don't
# accidentally make these required packages.
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


class TableWidget(WIDGET_BASE):
    """
    An interactive, paginated table widget for BigFrames DataFrames.
    """

    def __init__(self, dataframe: bigframes.dataframe.DataFrame):
        """Initialize the TableWidget.

        Args:
            dataframe: The Bigframes Dataframe to display in the widget.
        """
        if not ANYWIDGET_INSTALLED:
            raise ImportError(
                "Please `pip install anywidget traitlets` or `pip install 'bigframes[anywidget]'` to use TableWidget."
            )

        super().__init__()
        self._dataframe = dataframe

        # respect display options
        self.page_size = bigframes.options.display.max_rows

        # Initialize data fetching attributes.
        self._batches = dataframe.to_pandas_batches(page_size=self.page_size)

        # Use list of DataFrames to avoid memory copies from concatenation
        self._cached_batches: List[pd.DataFrame] = []

        # Unique identifier for HTML table element
        self._table_id = str(uuid.uuid4())
        self._all_data_loaded = False
        # Renamed from _batch_iterator to _batch_iter to avoid naming conflict
        self._batch_iter: Optional[Iterator[pd.DataFrame]] = None

        # len(dataframe) is expensive, since it will trigger a
        # SELECT COUNT(*) query. It is a must have however.
        # TODO(b/428238610): Start iterating over the result of `to_pandas_batches()`
        # before we get here so that the count might already be cached.
        self.row_count = len(dataframe)

        # get the initial page
        self._set_table_html()

    @functools.cached_property
    def _esm(self):
        """Load JavaScript code from external file."""
        return resources.read_text(bigframes.display, "table_widget.js")

    page = traitlets.Int(0).tag(sync=True)
    page_size = traitlets.Int(25).tag(sync=True)
    row_count = traitlets.Int(0).tag(sync=True)
    table_html = traitlets.Unicode().tag(sync=True)

    @traitlets.validate("page")
    def _validate_page(self, proposal: Dict[str, Any]):
        """Validate and clamp the page number to a valid range.

        Args:
            proposal: A dictionary from the traitlets library containing the
                proposed change. The new value is in proposal["value"].
        """

        value = proposal["value"]
        if self.row_count == 0 or self.page_size == 0:
            return 0

        # Calculate the zero-indexed maximum page number.
        max_page = max(0, math.ceil(self.row_count / self.page_size) - 1)

        # Clamp the proposed value to the valid range [0, max_page].
        return max(0, min(value, max_page))

    def _get_next_batch(self) -> bool:
        """
        Gets the next batch of data from the generator and appends to cache.

        Return:
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
            self._batch_iter = iter(self._batches)
        return self._batch_iter

    @property
    def _cached_data(self) -> pd.DataFrame:
        """Combine all cached batches into a single DataFrame."""
        if not self._cached_batches:
            return pd.DataFrame(columns=self._dataframe.columns)
        return pd.concat(self._cached_batches, ignore_index=True)

    def _set_table_html(self):
        """Sets the current html data based on the current page and page size."""
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
        page_data = cached_data.iloc[start:end]

        # Generate HTML table
        self.table_html = page_data.to_html(
            index=False,
            max_rows=None,
            table_id=f"table-{self._table_id}",
            classes="table table-striped table-hover",
            escape=False,
        )

    @traitlets.observe("page")
    def _page_changed(self, change):
        """Handler for when the page number is changed from the frontend."""
        self._set_table_html()
