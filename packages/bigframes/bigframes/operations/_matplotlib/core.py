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

import abc
import typing
import warnings

import bigframes_vendored.constants as constants
import pandas as pd

import bigframes.dtypes as dtypes
import bigframes.exceptions as bfe

DEFAULT_SAMPLING_N = 1000
DEFAULT_SAMPLING_STATE = 0


class MPLPlot(abc.ABC):
    @abc.abstractmethod
    def generate(self):
        pass

    def draw(self) -> None:
        # This import can fail with "Matplotlib failed to acquire the
        # following lock file" so import here to reduce the chance of
        # our parallel test suite from triggering this.
        import matplotlib.pyplot as plt

        plt.draw_if_interactive()

    @property
    def result(self):
        if hasattr(self, "axes"):
            return self.axes
        else:
            raise AttributeError("Axes not defined")


class SamplingPlot(MPLPlot):
    @property
    @abc.abstractmethod
    def _kind(self):
        pass

    @property
    def _sampling_warning_msg(self) -> typing.Optional[str]:
        return None

    def __init__(self, data, **kwargs) -> None:
        self.kwargs = kwargs
        self.data = data

    def generate(self) -> None:
        plot_data = self._compute_plot_data()
        self.axes = plot_data.plot(kind=self._kind, **self.kwargs)

    def _compute_sample_data(self, data):
        # TODO: Cache the sampling data in the PlotAccessor.
        sampling_n = self.kwargs.pop("sampling_n", DEFAULT_SAMPLING_N)
        if self._sampling_warning_msg is not None:
            total_n = data.shape[0]
            if sampling_n < total_n:
                msg = bfe.format_message(
                    self._sampling_warning_msg.format(
                        sampling_n=sampling_n, total_n=total_n
                    )
                )
                warnings.warn(msg, category=UserWarning)

        sampling_random_state = self.kwargs.pop(
            "sampling_random_state", DEFAULT_SAMPLING_STATE
        )
        return data.sample(
            n=sampling_n,
            random_state=sampling_random_state,
            sort=False,
        ).to_pandas()

    def _compute_plot_data(self):
        return self._compute_sample_data(self.data)


class AreaPlot(SamplingPlot):
    @property
    def _kind(self) -> typing.Literal["area"]:
        return "area"


class BarPlot(SamplingPlot):
    @property
    def _kind(self) -> typing.Literal["bar"]:
        return "bar"

    @property
    def _sampling_warning_msg(self) -> typing.Optional[str]:
        return (
            "To optimize plotting performance, your data has been downsampled to {sampling_n} "
            "rows from the original {total_n} rows. This may result in some data points "
            "not being displayed. For a more comprehensive view, consider pre-processing "
            "your data by aggregating it or selecting the top categories."
        )


class LinePlot(SamplingPlot):
    @property
    def _kind(self) -> typing.Literal["line"]:
        return "line"


class ScatterPlot(SamplingPlot):
    @property
    def _kind(self) -> typing.Literal["scatter"]:
        return "scatter"

    def __init__(self, data, **kwargs) -> None:
        super().__init__(data, **kwargs)

        c = self.kwargs.get("c", None)
        if self._is_sequence_arg(c):
            raise NotImplementedError(
                f"Only support a single color string or a column name/posision. {constants.FEEDBACK_LINK}"
            )

        s = self.kwargs.get("s", None)
        if self._is_sequence_arg(s):
            raise NotImplementedError(
                f"Only support a single color string or a column name/posision. {constants.FEEDBACK_LINK}"
            )

    def _compute_plot_data(self):
        sample = self._compute_sample_data(self.data)

        # Works around a pandas bug:
        # https://github.com/pandas-dev/pandas/commit/45b937d64f6b7b6971856a47e379c7c87af7e00a
        c = self.kwargs.get("c", None)
        if pd.core.dtypes.common.is_integer(c):
            c = self.data.columns[c]
        if self._is_column_name(c, sample) and sample[c].dtype == dtypes.STRING_DTYPE:
            sample[c] = sample[c].astype("object")

        # To avoid Matplotlib's automatic conversion of `Float64` or `Int64` columns
        # to `object` types (which breaks float-like behavior), this code proactively
        # converts the column to a compatible format.
        s = self.kwargs.get("s", None)
        if pd.core.dtypes.common.is_integer(s):
            s = self.data.columns[s]
        if self._is_column_name(s, sample):
            if sample[s].dtype == dtypes.INT_DTYPE:
                sample[s] = sample[s].astype("int64")
            elif sample[s].dtype == dtypes.FLOAT_DTYPE:
                sample[s] = sample[s].astype("float64")

        return sample

    def _is_sequence_arg(self, arg):
        return (
            arg is not None
            and not isinstance(arg, str)
            and isinstance(arg, typing.Iterable)
        )

    def _is_column_name(self, arg, data):
        return (
            arg is not None
            and pd.core.dtypes.common.is_hashable(arg)
            and arg in data.columns
        )
