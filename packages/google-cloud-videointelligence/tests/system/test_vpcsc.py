# Copyright 2017, Google LLC All rights reserved.
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
"""Verify videointelligence requests are blocked by VPCSC policy."""

import json
import os
import requests

from google.auth.transport import requests as goog_auth_requests
from google.oauth2 import service_account
import pytest

from test_utils.vpcsc_config import vpcsc_config

CLOUD_PLATFORM_SCOPE = "https://www.googleapis.com/auth/cloud-platform"
CREDENTIALS_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
API_ENDPOINT_URL = "https://videointelligence.googleapis.com/v1/videos:annotate"
BUCKET_INSIDE = os.environ.get("GOOGLE_CLOUD_TESTS_VPCSC_INSIDE_PERIMETER_BUCKET")


@pytest.fixture(scope="module")
def access_token():
    """Generate access token using the provided service account key file."""
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=[CLOUD_PLATFORM_SCOPE]
    )
    with requests.Session() as session:
        creds.refresh(goog_auth_requests.Request(session=session))

    return creds.token


@pytest.fixture(scope="module")
def headers(access_token):
    return {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }


def _make_body(bucket_name):
    return json.dumps(
        {
            "features": ["LABEL_DETECTION"],
            "location_id": "us-west1",
            "input_uri": "gs://{}/cat.mp4".format(bucket_name),
        }
    )


@vpcsc_config.skip_unless_inside_vpcsc
def test_outside_perimeter_blocked(headers):
    body = _make_body(bucket_name=vpcsc_config.bucket_outside)

    response = requests.post(url=API_ENDPOINT_URL, data=body, headers=headers)

    assert response.json()["error"]["code"] == 403
    assert response.json()["error"]["status"] == "PERMISSION_DENIED"


@vpcsc_config.skip_unless_inside_vpcsc
def test_inside_perimeter_allowed(headers):
    body = _make_body(bucket_name=BUCKET_INSIDE)

    response = requests.post(url=API_ENDPOINT_URL, data=body, headers=headers)

    operation = response.json()
    op_url = "https://videointelligence.googleapis.com/v1/{}".format(operation["name"])
    op_response = requests.get(url=op_url, headers=headers)
    # Assert that we do not get an error.
    assert op_response.json()["name"] == operation["name"]
