# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from os import path

import google.auth
import google.auth.credentials
import google.auth.transport.requests
import google.auth.transport.urllib3

MTLS_ENDPOINT = "https://pubsub.mtls.googleapis.com/v1/projects/{}/topics"
REGULAR_ENDPOINT = "https://pubsub.googleapis.com/v1/projects/{}/topics"


def check_context_aware_metadata():
    metadata_path = path.expanduser("~/.secureConnect/context_aware_metadata.json")
    return path.exists(metadata_path)


def test_requests():
    credentials, project_id = google.auth.default()
    credentials = google.auth.credentials.with_scopes_if_required(
        credentials, ["https://www.googleapis.com/auth/pubsub"]
    )

    authed_session = google.auth.transport.requests.AuthorizedSession(credentials)
    authed_session.configure_mtls_channel()

    # If the devices has context aware metadata, then a mutual TLS channel is
    # supposed to be created.
    assert authed_session.is_mtls == check_context_aware_metadata()

    if authed_session.is_mtls:
        response = authed_session.get(MTLS_ENDPOINT.format(project_id))
    else:
        response = authed_session.get(REGULAR_ENDPOINT.format(project_id))

    assert response.ok


def test_urllib3():
    credentials, project_id = google.auth.default()
    credentials = google.auth.credentials.with_scopes_if_required(
        credentials, ["https://www.googleapis.com/auth/pubsub"]
    )

    authed_http = google.auth.transport.urllib3.AuthorizedHttp(credentials)
    is_mtls = authed_http.configure_mtls_channel()

    # If the devices has context aware metadata, then a mutual TLS channel is
    # supposed to be created.
    assert is_mtls == check_context_aware_metadata()

    if is_mtls:
        response = authed_http.request("GET", MTLS_ENDPOINT.format(project_id))
    else:
        response = authed_http.request("GET", REGULAR_ENDPOINT.format(project_id))

    assert response.status == 200
