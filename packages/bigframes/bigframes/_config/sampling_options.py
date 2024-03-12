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

"""Options for downsampling."""

from __future__ import annotations

import dataclasses
from typing import Literal, Optional

import bigframes_vendored.pandas.core.config_init as vendored_pandas_config


@dataclasses.dataclass
class SamplingOptions:
    __doc__ = vendored_pandas_config.sampling_options_doc

    max_download_size: Optional[int] = 500
    # Enable downsampling
    enable_downsampling: bool = False
    sampling_method: Literal["head", "uniform"] = "uniform"
    random_state: Optional[int] = None

    def with_max_download_size(self, max_rows: Optional[int]) -> SamplingOptions:
        return SamplingOptions(
            max_rows, self.enable_downsampling, self.sampling_method, self.random_state
        )

    def with_method(self, method: Literal["head", "uniform"]) -> SamplingOptions:
        return SamplingOptions(self.max_download_size, True, method, self.random_state)

    def with_random_state(self, state: Optional[int]) -> SamplingOptions:
        return SamplingOptions(
            self.max_download_size,
            self.enable_downsampling,
            self.sampling_method,
            state,
        )

    def with_disabled(self) -> SamplingOptions:
        return SamplingOptions(
            self.max_download_size, False, self.sampling_method, self.random_state
        )
