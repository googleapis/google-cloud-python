# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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
from unittest import mock

import pytest

# We need to skip this test module if grpc is not installed because importing
# gapic_v1._config_helpers will load gapic_v1/__init__, which unconditionally
# imports gapic_v1.config, which imports grpc.
try:
    import grpc  # noqa: F401
except ImportError:
    pytest.skip("No GRPC", allow_module_level=True)

from google.auth.exceptions import MutualTLSChannelError

from google.api_core.gapic_v1._config_helpers import _read_environment_variables


@mock.patch(
    "google.api_core.gapic_v1._config_helpers._use_client_cert_effective"
)  # noqa: E501
@mock.patch.dict(os.environ, clear=True)
def test_read_environment_variables(mock_effective):
    mock_effective.return_value = True
    os.environ["GOOGLE_API_USE_MTLS_ENDPOINT"] = "always"
    os.environ["GOOGLE_CLOUD_UNIVERSE_DOMAIN"] = "custom.com"

    cert, mtls, domain = _read_environment_variables()
    assert cert is True
    assert mtls == "always"
    assert domain == "custom.com"


@mock.patch.dict(os.environ, clear=True)
def test_read_environment_variables_invalid_mtls():
    os.environ["GOOGLE_API_USE_MTLS_ENDPOINT"] = "invalid"
    with pytest.raises(
        MutualTLSChannelError, match="must be `never`, `auto` or `always`"
    ):
        _read_environment_variables()
