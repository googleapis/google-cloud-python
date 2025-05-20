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

from __future__ import annotations

import copy
from dataclasses import dataclass, field
import threading
from typing import Optional

import bigframes_vendored.pandas._config.config as pandas_config

import bigframes._config.bigquery_options as bigquery_options
import bigframes._config.compute_options as compute_options
import bigframes._config.display_options as display_options
import bigframes._config.experiment_options as experiment_options
import bigframes._config.sampling_options as sampling_options


@dataclass
class ThreadLocalConfig(threading.local):
    # If unset, global settings will be used
    bigquery_options: Optional[bigquery_options.BigQueryOptions] = None
    # Note: use default factory instead of default instance so each thread initializes to default values
    display_options: display_options.DisplayOptions = field(
        default_factory=display_options.DisplayOptions
    )
    sampling_options: sampling_options.SamplingOptions = field(
        default_factory=sampling_options.SamplingOptions
    )
    compute_options: compute_options.ComputeOptions = field(
        default_factory=compute_options.ComputeOptions
    )
    experiment_options: experiment_options.ExperimentOptions = field(
        default_factory=experiment_options.ExperimentOptions
    )


class Options:
    """Global options affecting BigQuery DataFrames behavior."""

    def __init__(self):
        self.reset()

    def reset(self) -> Options:
        """Reset the option settings to defaults.

        Returns:
            bigframes._config.Options: Options object with default values.
        """
        self._local = ThreadLocalConfig()

        # BigQuery options are special because they can only be set once per
        # session, so we need an indicator as to whether we are using the
        # thread-local session or the global session.
        self._bigquery_options = bigquery_options.BigQueryOptions()
        return self

    def _init_bigquery_thread_local(self):
        """Initialize thread-local options, based on current global options."""

        # Already thread-local, so don't reset any options that have been set
        # already. No locks needed since this only modifies thread-local
        # variables.
        if self._local.bigquery_options is not None:
            return

        self._local.bigquery_options = copy.deepcopy(self._bigquery_options)
        self._local.bigquery_options._session_started = False

    @property
    def bigquery(self) -> bigquery_options.BigQueryOptions:
        """Options to use with the BigQuery engine.

        Returns:
            bigframes._config.bigquery_options.BigQueryOptions:
                Options for BigQuery engine.
        """
        if self._local.bigquery_options is not None:
            # The only way we can get here is if someone called
            # _init_bigquery_thread_local.
            return self._local.bigquery_options

        return self._bigquery_options

    @property
    def display(self) -> display_options.DisplayOptions:
        """Options controlling object representation.

        Returns:
            bigframes._config.display_options.DisplayOptions:
                Options for controlling object representation.
        """
        return self._local.display_options

    @property
    def sampling(self) -> sampling_options.SamplingOptions:
        """Options controlling downsampling when downloading data
        to memory.

        The data can be downloaded into memory explicitly
        (e.g., to_pandas, to_numpy, values) or implicitly (e.g.,
        matplotlib plotting). This option can be overridden by
        parameters in specific functions.

        Returns:
            bigframes._config.sampling_options.SamplingOptions:
                Options for controlling downsampling.
        """
        return self._local.sampling_options

    @property
    def compute(self) -> compute_options.ComputeOptions:
        """Thread-local options controlling object computation.

        Returns:
            bigframes._config.compute_options.ComputeOptions:
                Thread-local options for controlling object computation
        """
        return self._local.compute_options

    @property
    def experiments(self) -> experiment_options.ExperimentOptions:
        """Options controlling experiments

        Returns:
            bigframes._config.experiment_options.ExperimentOptions:
               Thread-local options for controlling experiments
        """
        return self._local.experiment_options

    @property
    def is_bigquery_thread_local(self) -> bool:
        """Indicator that we're using a thread-local session.

        A thread-local session can be started by using
        `with bigframes.option_context("bigquery.some_option", "some-value"):`.

        Returns:
            bool:
                A boolean value, where a value is True if a thread-local session
                is in use; otherwise False.
        """
        return self._local.bigquery_options is not None

    @property
    def _allow_large_results(self) -> bool:
        """The effective 'allow_large_results' setting.

        This value is `self.compute.allow_large_results` if set (not `None`),
        otherwise it defaults to `self.bigquery.allow_large_results`.

        Returns:
            bool:
                Whether large query results are permitted.
                - `True`: The BigQuery result size limit (e.g., 10 GB) is removed.
                - `False`: Results are restricted to this limit (potentially faster).
                BigQuery will raise an error if this limit is exceeded.
        """
        if self.compute.allow_large_results is None:
            return self.bigquery.allow_large_results
        return self.compute.allow_large_results


options = Options()
"""Global options for default session."""

option_context = pandas_config.option_context


__all__ = (
    "Options",
    "options",
    "option_context",
)
