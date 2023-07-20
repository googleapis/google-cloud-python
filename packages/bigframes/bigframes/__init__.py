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

"""BigQuery DataFrames provides a DataFrame API scaled by the BigQuery engine."""

from bigframes._config import options
from bigframes._config.bigquery_options import BigQueryOptions
from bigframes.session import connect, Session
from bigframes.version import __version__

__all__ = [
    "BigQueryOptions",
    "connect",
    "options",
    "Session",
    "__version__",
]
