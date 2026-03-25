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

from __future__ import annotations

import threading
from typing import Optional

import google.auth.credentials
import google.auth.transport.requests
import pydata_google_auth

_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

# Put the lock here rather than in BigQueryOptions so that BigQueryOptions
# remains deepcopy-able.
_AUTH_LOCK = threading.Lock()
_cached_credentials: Optional[google.auth.credentials.Credentials] = None
_cached_project_default: Optional[str] = None


def get_default_credentials_with_project() -> (
    tuple[google.auth.credentials.Credentials, Optional[str]]
):
    global _AUTH_LOCK, _cached_credentials, _cached_project_default

    with _AUTH_LOCK:
        if _cached_credentials is not None:
            return _cached_credentials, _cached_project_default

        _cached_credentials, _cached_project_default = pydata_google_auth.default(
            scopes=_SCOPES, use_local_webserver=False
        )

        # Ensure an access token is available.
        _cached_credentials.refresh(google.auth.transport.requests.Request())

    return _cached_credentials, _cached_project_default


def reset_default_credentials_and_project():
    global _AUTH_LOCK, _cached_credentials, _cached_project_default

    with _AUTH_LOCK:
        _cached_credentials = None
        _cached_project_default = None
