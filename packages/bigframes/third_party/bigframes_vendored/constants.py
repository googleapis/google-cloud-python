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

"""Constants used across BigQuery DataFrames and bigframes_vendored.

This module should not depend on any others in the package.
"""

import typing
from typing import Literal

import bigframes_vendored.version

FEEDBACK_LINK = (
    "Share your usecase with the BigQuery DataFrames team at the "
    "https://bit.ly/bigframes-feedback survey. "
    f"You are currently running BigFrames version {bigframes_vendored.version.__version__}."
)

ABSTRACT_METHOD_ERROR_MESSAGE = (
    "Abstract method. You have likely encountered a bug. "
    "Please share this stacktrace and how you reached it with the BigQuery DataFrames team. "
    f"{FEEDBACK_LINK}"
)

WRITE_ENGINE_TEMPLATE = (
    "Can't use parsing engine={engine} with write_engine={write_engine}, which "
)
WRITE_ENGINE_REQUIRES_LOCAL_ENGINE_TEMPLATE = (
    WRITE_ENGINE_TEMPLATE + "requires a local parsing engine. " + FEEDBACK_LINK
)
WRITE_ENGINE_REQUIRES_BIGQUERY_ENGINE_TEMPLATE = (
    WRITE_ENGINE_TEMPLATE
    + "requires the engine='bigquery' parsing engine. "
    + FEEDBACK_LINK
)

WriteEngineType = Literal[
    "default",
    "bigquery_inline",
    "bigquery_load",
    "bigquery_streaming",
    "bigquery_write",
    "_deferred",
]
VALID_WRITE_ENGINES = typing.get_args(WriteEngineType)
