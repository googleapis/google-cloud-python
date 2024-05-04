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

"""Public exceptions and warnings used across BigQuery DataFrames."""

# NOTE: This module should not depend on any others in the package.


class UnknownLocationWarning(Warning):
    """The location is set to an unknown value."""


class CleanupFailedWarning(Warning):
    """Bigframes failed to clean up a table resource."""


class DefaultIndexWarning(Warning):
    """Default index may cause unexpected costs."""
