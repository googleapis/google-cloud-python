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

from typing import Optional, Sequence

import bigframes_vendored.pandas.plotting._core as vendordt

import bigframes.constants as constants
import bigframes.operations._matplotlib as bfplt


class PlotAccessor:
    __doc__ = vendordt.PlotAccessor.__doc__

    def __init__(self, data) -> None:
        self._parent = data

    def hist(self, by: Optional[Sequence[str]] = None, bins: int = 10, **kwargs):
        if kwargs.pop("backend", None) is not None:
            raise NotImplementedError(
                f"Only support matplotlib backend for now. {constants.FEEDBACK_LINK}"
            )
        # Calls matplotlib backend to plot the data.
        return bfplt.plot(self._parent.copy(), kind="hist", by=by, bins=bins, **kwargs)
