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

import datetime

"""Constants used across BigQuery DataFrames.

This module should not depend on any others in the package.
"""

FEEDBACK_LINK = (
    "Share your usecase with the BigQuery DataFrames team at the "
    "https://bit.ly/bigframes-feedback survey."
)

ABSTRACT_METHOD_ERROR_MESSAGE = f"Abstract method. You have likely encountered a bug. Please share this stacktrace and how you reached it with the BigQuery DataFrames team. {FEEDBACK_LINK}"

DEFAULT_EXPIRATION = datetime.timedelta(days=7)
