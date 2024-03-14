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

import bigframes.operations._matplotlib.core as core
import bigframes.operations._matplotlib.hist as hist

PLOT_CLASSES: dict[str, type[core.MPLPlot]] = {
    "hist": hist.HistPlot,
    "line": core.LinePlot,
    "area": core.AreaPlot,
    "scatter": core.ScatterPlot,
}


def plot(data, kind, **kwargs):
    plot_obj = PLOT_CLASSES[kind](data, **kwargs)
    plot_obj.generate()
    plot_obj.draw()
    return plot_obj.result


__all__ = ["plot"]
