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
        return self.axes


class SamplingPlot(MPLPlot):
    @abc.abstractproperty
    def _kind(self):
        pass

    def __init__(self, data, **kwargs) -> None:
        self.kwargs = kwargs
        self.data = self._compute_plot_data(data)

    def generate(self) -> None:
        self.axes = self.data.plot(kind=self._kind, **self.kwargs)

    def _compute_plot_data(self, data):
        # TODO: Cache the sampling data in the PlotAccessor.
        sampling_n = self.kwargs.pop("sampling_n", DEFAULT_SAMPLING_N)
        sampling_random_state = self.kwargs.pop(
            "sampling_random_state", DEFAULT_SAMPLING_STATE
        )
        return data.sample(
            n=sampling_n,
            random_state=sampling_random_state,
            sort=False,
        ).to_pandas()


class LinePlot(SamplingPlot):
    @property
    def _kind(self) -> typing.Literal["line"]:
        return "line"


class AreaPlot(SamplingPlot):
    @property
    def _kind(self) -> typing.Literal["area"]:
        return "area"


class ScatterPlot(SamplingPlot):
    @property
    def _kind(self) -> typing.Literal["scatter"]:
        return "scatter"
