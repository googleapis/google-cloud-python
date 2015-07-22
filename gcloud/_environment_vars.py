# Copyright 2015 Google Inc. All rights reserved.
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

"""Comprehensive list of environment variables used in gcloud.

These enable many types of implicit behavior in both production
and tests.
"""

_PROJECT_ENV_VAR_NAME = 'GCLOUD_PROJECT'
"""Environment variable defining default project."""

_TESTS_PROJECT_ENV_VAR_NAME = 'GCLOUD_TESTS_PROJECT_ID'
"""Environment variable defining project for tests."""

_DATASET_ENV_VAR_NAME = 'GCLOUD_DATASET_ID'
"""Environment variable defining default dataset ID."""

_GCD_DATASET_ENV_VAR_NAME = 'DATASTORE_DATASET'
"""Environment variable defining default dataset ID under GCD."""

_GCD_HOST_ENV_VAR_NAME = 'DATASTORE_HOST'
"""Environment variable defining host for GCD dataset server."""

_TESTS_DATASET_ENV_VAR_NAME = 'GCLOUD_TESTS_DATASET_ID'
"""Environment variable defining dataset ID for tests."""

_CREDENTIALS_ENV_VAR_NAME = 'GOOGLE_APPLICATION_CREDENTIALS'
"""Environment variable defining location of Google credentials."""
