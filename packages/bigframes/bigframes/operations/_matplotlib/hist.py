# Copyright 2023 Google LLC
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

import itertools
from typing import Literal

import bigframes_vendored.constants as constants
import numpy as np
import pandas as pd

import bigframes.operations._matplotlib.core as bfplt


class HistPlot(bfplt.MPLPlot):
    @property
    def _kind(self) -> Literal["hist"]:
        return "hist"

    def __init__(
        self,
        data,
        bins: int = 10,
        **kwargs,
    ) -> None:
        self.bins = bins
        self.label = kwargs.get("label", None)
        self.by = kwargs.pop("by", None)
        self.kwargs = kwargs

        if self.by is not None:
            raise NotImplementedError(
                f"Non-none `by` argument is not yet supported. {constants.FEEDBACK_LINK}"
            )
        if not isinstance(self.bins, int):
            raise NotImplementedError(
                f"Only integer values are supported for the `bins` argument. {constants.FEEDBACK_LINK}"
            )
        if kwargs.get("weight", None) is not None:
            raise NotImplementedError(
                f"Non-none `weight` argument is not yet supported. {constants.FEEDBACK_LINK}"
            )

        self.data = self._compute_plot_data(data)

    def generate(self) -> None:
        """
        Calculates weighted histograms through BigQuery and plots them through pandas
        native histogram plot.
        """
        hist_bars = self._calculate_hist_bars(self.data, self.bins)
        bin_edges = self._calculate_bin_edges(
            hist_bars, self.bins, self.kwargs.get("range", None)
        )

        weights = {
            col_name: hist_bar.values for col_name, hist_bar in hist_bars.items()
        }
        hist_x = {
            col_name: pd.Series(
                (
                    hist_bar.index.get_level_values("left_exclusive")
                    + hist_bar.index.get_level_values("right_inclusive")
                )
                / 2.0
            )
            for col_name, hist_bar in hist_bars.items()
        }

        # Align DataFrames for plotting despite potential differences in column
        # lengths, filling shorter columns with zeros.
        hist_x_pd = pd.DataFrame(
            list(itertools.zip_longest(*hist_x.values())), columns=list(hist_x.keys())
        ).sort_index(axis=1)[self.data.columns.values]
        weights_pd = pd.DataFrame(
            list(itertools.zip_longest(*weights.values())), columns=list(weights.keys())
        ).sort_index(axis=1)[self.data.columns.values]

        # Prevents pandas from dropping NA values and causing length mismatches by
        # filling them with zeros.
        hist_x_pd.fillna(0, inplace=True)
        weights_pd.fillna(0, inplace=True)

        self.axes = hist_x_pd.plot.hist(
            bins=bin_edges,
            weights=np.array(weights_pd.values),
            **self.kwargs,
        )  # type: ignore

    def _compute_plot_data(self, data):
        """
        Prepares data for plotting, focusing on numeric data types.

        Raises:
            TypeError: If the input data contains no numeric columns.
        """
        # Importing at the top of the file causes a circular import.
        import bigframes.series as series

        if isinstance(data, series.Series):
            label = self.label
            if label is None and data.name is None:
                label = ""
            if label is None:
                data = data.to_frame()
            else:
                data = data.to_frame(name=label)

        # TODO(chelsealin): Support timestamp/date types here.
        include_type = ["number"]
        numeric_data = data.select_dtypes(include=include_type)
        try:
            is_empty = numeric_data.columns.empty
        except AttributeError:
            is_empty = not len(numeric_data)

        if is_empty:
            raise TypeError("no numeric data to plot")

        return numeric_data

    @staticmethod
    def _calculate_hist_bars(data, bins):
        """
        Calculates histogram bars for each column in a BigFrames DataFrame, and
        returns a dictionary where keys are column names and values are pandas
        Series. The series values are the histogram bins' heights with a
        multi-index defining 'left_exclusive' and 'right_inclusive' bin edges.
        """
        import bigframes.pandas as bpd

        # TODO: Optimize this by batching multiple jobs into one.
        hist_bar = {}
        for _, col in enumerate(data.columns):
            cutted_data = bpd.cut(data[col], bins=bins, labels=None)
            hist_bar[col] = (
                cutted_data.struct.explode()
                .value_counts()
                .to_pandas()
                .sort_index(level="left_exclusive")
            )
        return hist_bar

    @staticmethod
    def _calculate_bin_edges(hist_bars, bins, range):
        """
        Calculate bin edges from the histogram bars.
        """
        bin_edges = None
        for _, hist_bar in hist_bars.items():
            left = hist_bar.index.get_level_values("left_exclusive")
            right = hist_bar.index.get_level_values("right_inclusive")
            if bin_edges is None:
                bin_edges = left.union(right)
            else:
                bin_edges = left.union(right).union(bin_edges)

        if bin_edges is None:
            return None

        _, bins = np.histogram(bin_edges, bins=bins, range=range)
        return bins
