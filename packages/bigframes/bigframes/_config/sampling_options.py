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


@dataclasses.dataclass
class SamplingOptions:
    """
    Encapsulates the configuration for data sampling.
    """

    max_download_size: Optional[int] = 500
    """
    Download size threshold in MB. Default 500.

    If value set to None, the download size won't be checked.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> bpd.options.sampling.max_download_size = 1000  # doctest: +SKIP
    """

    enable_downsampling: bool = False
    """
    Whether to enable downsampling. Default False.

    If max_download_size is exceeded when downloading data (e.g., to_pandas()),
    the data will be downsampled if enable_downsampling is True, otherwise, an
    error will be raised.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> bpd.options.sampling.enable_downsampling = True  # doctest: +SKIP
    """

    sampling_method: Literal["head", "uniform"] = "uniform"
    """
    Downsampling algorithms to be chosen from. Default "uniform".

    The choices are: "head": This algorithm returns a portion of the data from
    the beginning. It is fast and requires minimal computations to perform the
    downsampling.; "uniform": This algorithm returns uniform random samples of
    the data.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> bpd.options.sampling.sampling_method = "head"  # doctest: +SKIP
    """

    random_state: Optional[int] = None
    """
    The seed for the uniform downsampling algorithm. Default None.

    If provided, the uniform method may take longer to execute and require more
    computation.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> bpd.options.sampling.random_state = 42  # doctest: +SKIP
    """

    def with_max_download_size(self, max_rows: Optional[int]) -> SamplingOptions:
        """Configures the maximum download size for data sampling in MB

        Args:
            max_rows (None or int):
                An int value for the maximum row size.

        Returns:
            bigframes._config.sampling_options.SamplingOptions:
                The configuration for data sampling.
        """
        return SamplingOptions(
            max_rows, self.enable_downsampling, self.sampling_method, self.random_state
        )

    def with_method(self, method: Literal["head", "uniform"]) -> SamplingOptions:
        """Configures the downsampling algorithms to be chosen from

        Args:
            method (None or Literal):
                A literal string value of either head or uniform data sampling method.

        Returns:
            bigframes._config.sampling_options.SamplingOptions:
                The configuration for data sampling.
        """
        return SamplingOptions(self.max_download_size, True, method, self.random_state)

    def with_random_state(self, state: Optional[int]) -> SamplingOptions:
        """Configures the seed for the uniform downsampling algorithm

        Args:
            state (None or int):
                An int value for the data sampling random state

        Returns:
            bigframes._config.sampling_options.SamplingOptions:
                The configuration for data sampling.
        """
        return SamplingOptions(
            self.max_download_size,
            self.enable_downsampling,
            self.sampling_method,
            state,
        )

    def with_disabled(self) -> SamplingOptions:
        """Configures whether to disable downsampling

        Returns:
            bigframes._config.sampling_options.SamplingOptions:
                The configuration for data sampling.
        """
        return SamplingOptions(
            self.max_download_size, False, self.sampling_method, self.random_state
        )
