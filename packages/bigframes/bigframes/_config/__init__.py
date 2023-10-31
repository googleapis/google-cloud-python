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

"""
Configuration for BigQuery DataFrames. Do not depend on other parts of BigQuery
DataFrames from this package.
"""

import bigframes._config.bigquery_options as bigquery_options
import bigframes._config.compute_options as compute_options
import bigframes._config.display_options as display_options
import bigframes._config.sampling_options as sampling_options
import third_party.bigframes_vendored.pandas._config.config as pandas_config


class Options:
    """Global options affecting BigQuery DataFrames behavior."""

    def __init__(self):
        self._bigquery_options = bigquery_options.BigQueryOptions()
        self._display_options = display_options.DisplayOptions()
        self._sampling_options = sampling_options.SamplingOptions()
        self._compute_options = compute_options.ComputeOptions()

    @property
    def bigquery(self) -> bigquery_options.BigQueryOptions:
        """Options to use with the BigQuery engine."""
        return self._bigquery_options

    @property
    def display(self) -> display_options.DisplayOptions:
        """Options controlling object representation."""
        return self._display_options

    @property
    def sampling(self) -> sampling_options.SamplingOptions:
        """Options controlling downsampling when downloading data
        to memory. The data will be downloaded into memory explicitly
        (e.g., to_pandas, to_numpy, values) or implicitly (e.g.,
        matplotlib plotting). This option can be overriden by
        parameters in specific functions."""
        return self._sampling_options

    @property
    def compute(self) -> compute_options.ComputeOptions:
        """Options controlling object computation."""
        return self._compute_options


options = Options()
"""Global options for default session."""


__all__ = (
    "Options",
    "options",
)


option_context = pandas_config.option_context
