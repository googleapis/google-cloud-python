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
import sys

import google.auth.credentials

# special case python < 3.8
if sys.version_info.major == 3 and sys.version_info.minor < 8:
    import mock
else:
    from unittest import mock

import pytest


@pytest.fixture
def creds():
    """
    Provide test creds to unit tests so that they can run without
    GOOGLE_APPLICATION_CREDENTIALS set.
    """
    yield mock.Mock(spec=google.auth.credentials.Credentials)
