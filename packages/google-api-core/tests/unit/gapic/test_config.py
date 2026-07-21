# Copyright 2017 Google LLC
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
from google.auth.exceptions import MutualTLSChannelError

try:
    import grpc  # noqa: F401
except ImportError:
    pytest.skip("No GRPC", allow_module_level=True)

from google.api_core import exceptions
from google.api_core.gapic_v1 import config

INTERFACE_CONFIG = {
    "retry_codes": {
        "idempotent": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
        "other": ["FAILED_PRECONDITION"],
        "non_idempotent": [],
    },
    "retry_params": {
        "default": {
            "initial_retry_delay_millis": 1000,
            "retry_delay_multiplier": 2.5,
            "max_retry_delay_millis": 120000,
            "initial_rpc_timeout_millis": 120000,
            "rpc_timeout_multiplier": 1.0,
            "max_rpc_timeout_millis": 120000,
            "total_timeout_millis": 600000,
        },
        "other": {
            "initial_retry_delay_millis": 1000,
            "retry_delay_multiplier": 1,
            "max_retry_delay_millis": 1000,
            "initial_rpc_timeout_millis": 1000,
            "rpc_timeout_multiplier": 1,
            "max_rpc_timeout_millis": 1000,
            "total_timeout_millis": 1000,
        },
    },
    "methods": {
        "AnnotateVideo": {
            "timeout_millis": 60000,
            "retry_codes_name": "idempotent",
            "retry_params_name": "default",
        },
        "Other": {
            "timeout_millis": 60000,
            "retry_codes_name": "other",
            "retry_params_name": "other",
        },
        "Plain": {"timeout_millis": 30000},
    },
}


def test_create_method_configs():
    method_configs = config.parse_method_configs(INTERFACE_CONFIG)

    retry, timeout = method_configs["AnnotateVideo"]
    assert retry._predicate(exceptions.DeadlineExceeded(None))
    assert retry._predicate(exceptions.ServiceUnavailable(None))
    assert retry._initial == 1.0
    assert retry._multiplier == 2.5
    assert retry._maximum == 120.0
    assert retry._deadline == 600.0
    assert timeout._initial == 120.0
    assert timeout._multiplier == 1.0
    assert timeout._maximum == 120.0

    retry, timeout = method_configs["Other"]
    assert retry._predicate(exceptions.FailedPrecondition(None))
    assert retry._initial == 1.0
    assert retry._multiplier == 1.0
    assert retry._maximum == 1.0
    assert retry._deadline == 1.0
    assert timeout._initial == 1.0
    assert timeout._multiplier == 1.0
    assert timeout._maximum == 1.0

    retry, timeout = method_configs["Plain"]
    assert retry is None
    assert timeout._timeout == 30.0


def test_use_client_cert_effective_true():
    mock_mtls = mock.Mock(spec=["should_use_client_cert"])
    mock_mtls.should_use_client_cert.return_value = True
    with mock.patch("google.api_core.gapic_v1.config.mtls", mock_mtls):
        assert config.use_client_cert_effective() is True


def test_use_client_cert_effective_false():
    mock_mtls = mock.Mock(spec=["should_use_client_cert"])
    mock_mtls.should_use_client_cert.return_value = False
    with mock.patch("google.api_core.gapic_v1.config.mtls", mock_mtls):
        assert config.use_client_cert_effective() is False


def test_use_client_cert_effective_fallback_env_true():
    mock_mtls = mock.Mock(spec=[])
    with mock.patch("google.api_core.gapic_v1.config.mtls", mock_mtls):
        with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
            assert config.use_client_cert_effective() is True


def test_use_client_cert_effective_fallback_env_false():
    mock_mtls = mock.Mock(spec=[])
    with mock.patch("google.api_core.gapic_v1.config.mtls", mock_mtls):
        with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
            assert config.use_client_cert_effective() is False


def test_use_client_cert_effective_fallback_env_invalid():
    mock_mtls = mock.Mock(spec=[])
    with mock.patch("google.api_core.gapic_v1.config.mtls", mock_mtls):
        with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "invalid"}):
            with pytest.raises(
                ValueError,
                match="Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`",
            ):
                config.use_client_cert_effective()


def test_get_client_cert_source_provided():
    source = mock.Mock()
    assert config.get_client_cert_source(source, True) == source


def test_get_client_cert_source_default():
    mock_mtls = mock.Mock(spec=["has_default_client_cert_source", "default_client_cert_source"])
    mock_mtls.has_default_client_cert_source.return_value = True
    mock_source = mock.Mock()
    mock_mtls.default_client_cert_source.return_value = mock_source
    with mock.patch("google.api_core.gapic_v1.config.mtls", mock_mtls):
        assert config.get_client_cert_source(None, True) == mock_source


def test_get_client_cert_source_none():
    mock_mtls = mock.Mock(spec=["has_default_client_cert_source", "default_client_cert_source"])
    mock_mtls.has_default_client_cert_source.return_value = False
    with mock.patch("google.api_core.gapic_v1.config.mtls", mock_mtls):
        with pytest.raises(
            ValueError,
            match="Client certificate is required for mTLS, but no client certificate source was provided or found.",
        ):
            config.get_client_cert_source(None, True)


def test_get_client_cert_source_use_cert_flag_false():
    assert config.get_client_cert_source(None, False) is None
    source = mock.Mock()
    assert config.get_client_cert_source(source, False) is None


def test_read_environment_variables():
    with mock.patch("google.api_core.gapic_v1.config.use_client_cert_effective", return_value=True):
        with mock.patch.dict(
            os.environ,
            {"GOOGLE_API_USE_MTLS_ENDPOINT": "always", "GOOGLE_CLOUD_UNIVERSE_DOMAIN": "my-universe.com"}
        ):
            use_cert, use_mtls, universe = config.read_environment_variables()
            assert use_cert is True
            assert use_mtls == "always"
            assert universe == "my-universe.com"


def test_read_environment_variables_invalid_mtls():
    with mock.patch("google.api_core.gapic_v1.config.use_client_cert_effective", return_value=True):
        with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "invalid"}):
            with pytest.raises(MutualTLSChannelError):
                config.read_environment_variables()
