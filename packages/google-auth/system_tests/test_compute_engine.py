# Copyright 2016 Google Inc.
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

import pytest

import google.auth
from google.auth import _helpers
from google.auth import compute_engine
from google.auth import exceptions
from google.auth.compute_engine import _metadata


@pytest.fixture(autouse=True)
def check_gce_environment(http_request):
    try:
        _metadata.get_service_account_info(http_request)
    except exceptions.TransportError:
        pytest.skip('Compute Engine metadata service is not available.')


def test_refresh(http_request, token_info):
    credentials = compute_engine.Credentials()

    credentials.refresh(http_request)

    assert credentials.token is not None
    assert credentials.service_account_email is not None

    info = token_info(credentials.token)
    info_scopes = _helpers.string_to_scopes(info['scope'])
    assert set(info_scopes) == set(credentials.scopes)


def test_default(verify_refresh):
    credentials, project_id = google.auth.default()

    assert project_id is not None
    assert isinstance(credentials, compute_engine.Credentials)
    verify_refresh(credentials)
