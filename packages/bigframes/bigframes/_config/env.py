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

import os

from bigframes._config import options

_BIGFRAMES_SPECIFIC_ENV_DEFAULT_PROJECT = "BIGFRAMES_DEFAULT_PROJECT"
_GOOGLE_CLOUD_PROJECT = "GOOGLE_CLOUD_PROJECT"


def get_default_project_id() -> str:
    # Prefer the project in this order:
    # 1. Project explicitly specified by the user
    # 2. Project set in the environment
    # 3. Project associated with the default credentials
    maybe_from_env = (
        options.bigquery.project
        or os.getenv(_BIGFRAMES_SPECIFIC_ENV_DEFAULT_PROJECT)
        or os.getenv(_GOOGLE_CLOUD_PROJECT)
    )
    if maybe_from_env:
        return maybe_from_env

    import bigframes._config.auth as auth

    _, creds_project = auth.get_default_credentials_with_project()

    if not creds_project:
        raise ValueError(
            "Project must be set to initialize BigQuery client. "
            "Try setting `bigframes.options.bigquery.project` first."
        )

    return creds_project
