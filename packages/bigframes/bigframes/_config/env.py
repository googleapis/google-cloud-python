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

from typing import Optional
from bigframes._config import options
import bigframes._config.bigquery_options as bigquery_options

_BIGFRAMES_SPECIFIC_ENV_DEFAULT_PROJECT = "BIGFRAMES_DEFAULT_PROJECT"
_GOOGLE_CLOUD_PROJECT = "GOOGLE_CLOUD_PROJECT"


def resolve_credentials_and_project(options: bigquery_options.BigQueryOptions) -> tuple[google.auth.credentials.Credentials, str]:
    if project is None:
        project = bigframes._config.env.get_default_project_id(context)

    if credentials is None:
        credentials, cred_project = bigframes._config.auth.get_default_credentials_with_project()
        if project is None:
            project = cred_project

    if project is None:
        raise ValueError(
            "Project must be set to initialize BigQuery client. "
            "Try setting `bigframes.options.bigquery.project` first."
        )
    return credentials, project


def get_default_project_id() -> Optional[str]:
    # Prefer the project in this order:
    # 1. Project explicitly specified by the user
    # 2. Project set in the environment
    # 3. Project associated with the default credentials
    return (
        bigframes._config.options.project
        or os.getenv(_BIGFRAMES_SPECIFIC_ENV_DEFAULT_PROJECT)
        or os.getenv(_GOOGLE_CLOUD_PROJECT)
    )