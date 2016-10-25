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

from google.auth import _helpers
from google.auth import compute_engine
from google.auth.compute_engine import _metadata


@pytest.fixture(autouse=True)
def check_gce_environment(request):
    if not _metadata.ping(request):
        pytest.skip('Compute Engine metadata service is not available.')


def test_refresh(request, token_info):
    credentials = compute_engine.Credentials()

    credentials.refresh(request)

    assert credentials.token is not None
    assert credentials._service_account_email is not None

    info = token_info(credentials.token)
    info_scopes = _helpers.string_to_scopes(info['scope'])
    assert set(info_scopes) == set(credentials.scopes)
