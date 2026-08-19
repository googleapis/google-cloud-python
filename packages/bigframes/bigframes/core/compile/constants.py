# Copyright 2025 Google LLC
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


# Datetime constants
UNIT_TO_US_CONVERSION_FACTORS = {
    "W": 7 * 24 * 60 * 60 * 1000 * 1000,
    "d": 24 * 60 * 60 * 1000 * 1000,
    "D": 24 * 60 * 60 * 1000 * 1000,
    "h": 60 * 60 * 1000 * 1000,
    "m": 60 * 1000 * 1000,
    "s": 1000 * 1000,
    "ms": 1000,
    "us": 1,
    "ns": 1e-3,
}
