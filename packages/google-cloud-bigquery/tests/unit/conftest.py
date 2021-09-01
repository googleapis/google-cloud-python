# Copyright 2021 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock
import pytest

from .helpers import make_client


@pytest.fixture
def client():
    yield make_client()


@pytest.fixture
def PROJECT():
    yield "PROJECT"


@pytest.fixture
def DS_ID():
    yield "DATASET_ID"


@pytest.fixture
def LOCATION():
    yield "us-central"


def noop_add_server_timeout_header(headers, kwargs):
    if headers:
        kwargs["headers"] = headers
    return kwargs


@pytest.fixture(autouse=True)
def disable_add_server_timeout_header(request):
    if "enable_add_server_timeout_header" in request.keywords:
        yield
    else:
        with mock.patch(
            "google.cloud.bigquery.client._add_server_timeout_header",
            noop_add_server_timeout_header,
        ):
            yield
