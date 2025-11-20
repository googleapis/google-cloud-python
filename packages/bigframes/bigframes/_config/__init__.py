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

from bigframes._config.bigquery_options import BigQueryOptions
from bigframes._config.compute_options import ComputeOptions
from bigframes._config.display_options import DisplayOptions
from bigframes._config.experiment_options import ExperimentOptions
from bigframes._config.global_options import option_context, Options
import bigframes._config.global_options as global_options
from bigframes._config.sampling_options import SamplingOptions

options = global_options.options
"""Global options for the default session."""

__all__ = (
    "Options",
    "options",
    "option_context",
    "BigQueryOptions",
    "ComputeOptions",
    "DisplayOptions",
    "ExperimentOptions",
    "SamplingOptions",
)
