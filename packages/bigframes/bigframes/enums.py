# Copyright 2024 Google LLC
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

"""Public enums used across BigQuery DataFrames."""

# NOTE: This module should not depend on any others in the package.


import enum


class OrderingMode(enum.Enum):
    """[Preview] Values used to determine the ordering mode.

    Default is 'strict'.
    """

    STRICT = "strict"
    PARTIAL = "partial"


class DefaultIndexKind(enum.Enum):
    """Sentinel values used to override default indexing behavior."""

    #: Use consecutive integers as the index. This is ``0``, ``1``, ``2``, ...,
    #: ``n - 3``, ``n - 2``, ``n - 1``, where ``n`` is the number of items in
    #: the index.
    SEQUENTIAL_INT64 = enum.auto()
    # A completely null index incapable of indexing or alignment.
    NULL = enum.auto()
