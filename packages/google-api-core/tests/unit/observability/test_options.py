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

import pytest

from google.api_core.observability import options
from google.api_core.observability.options import (
    _get_env_bool,
    _strtobool,
    clear_test_env_overrides,
    set_test_env_override,
)


@pytest.fixture(autouse=True)
def clean_overrides():
    yield
    clear_test_env_overrides()


@pytest.mark.parametrize(
    "value,expected",
    [
        # Truthy values
        ("y", True),
        ("yes", True),
        ("t", True),
        ("true", True),
        ("on", True),
        ("1", True),
        ("  True  ", True),
        # Falsy values
        ("n", False),
        ("no", False),
        ("f", False),
        ("false", False),
        ("off", False),
        ("0", False),
        (" FALSE ", False),
        # Empty string
        ("", None),
    ],
)
def test_strtobool(value, expected):
    assert _strtobool(value) is expected


def test_strtobool_invalid():
    with pytest.raises(ValueError):
        _strtobool("invalid")


def test_get_env_bool(monkeypatch):
    monkeypatch.setenv("TEST_VAR", "true")
    assert _get_env_bool("TEST_VAR") is True

    monkeypatch.setenv("TEST_VAR", "invalid")
    assert _get_env_bool("TEST_VAR") is None

    monkeypatch.delenv("TEST_VAR", raising=False)
    assert _get_env_bool("TEST_VAR") is None


def test_set_test_env_override_clear_specific():
    """Verify that setting an override to None clears that specific override.

    This is important to ensure tests can reset individual environment overrides
    without affecting other overrides that might be set for other tests running
    concurrently or subsequently.
    """
    set_test_env_override("TEST_A", True)
    set_test_env_override("TEST_B", True)
    assert _get_env_bool("TEST_A") is True
    assert _get_env_bool("TEST_B") is True

    # Clear only TEST_A
    set_test_env_override("TEST_A", None)

    # Verify TEST_A is cleared but TEST_B remains
    assert _get_env_bool("TEST_A") is None
    assert _get_env_bool("TEST_B") is True


def test_get_env_bool_with_dev_fallback_other_prefix(monkeypatch):
    """Verify that environment variables without the 'GOOGLE_CLOUD_' prefix fall back directly.

    This is important to ensure that generic or non-GCP environment variables
    are handled correctly by the fallback logic without triggering GCP-specific
    replacement logic.
    """
    monkeypatch.setenv("OTHER_PREFIX_VAR", "true")
    assert options._get_env_bool_with_dev_fallback("OTHER_PREFIX_VAR") is True


@pytest.mark.parametrize(
    "signal_type, env_vars, client_options, default_val, expected",
    [
        # Default fallback tests
        ("tracing", {}, None, False, False),
        ("tracing", {}, None, True, True),
        # Global env var
        ("tracing", {"GOOGLE_CLOUD_PYTHON_TRACING_ENABLED": True}, None, False, True),
        ("tracing", {"GOOGLE_CLOUD_PYTHON_TRACING_ENABLED": False}, None, True, False),
        # Experimental fallback
        (
            "tracing",
            {"GOOGLE_CLOUD_EXPERIMENTAL_PYTHON_TRACING_ENABLED": True},
            None,
            False,
            True,
        ),
        (
            "tracing",
            {"GOOGLE_CLOUD_EXPERIMENTAL_PYTHON_TRACING_ENABLED": False},
            None,
            True,
            False,
        ),
        # Implicit opt-in with provider
        (
            "tracing",
            {"GOOGLE_CLOUD_PYTHON_TRACING_ENABLED": False},
            {"tracer_provider": object()},
            False,
            True,
        ),
        # Programmatic boolean flags are NOT supported in client_options
        # (should default/fallback to False)
        (
            "tracing",
            {"GOOGLE_CLOUD_PYTHON_TRACING_ENABLED": False},
            {"enable_metrics": True},
            False,
            False,
        ),
        (
            "tracing",
            {"GOOGLE_CLOUD_PYTHON_TRACING_ENABLED": False},
            {"enable_tracing": True},
            False,
            False,
        ),
    ],
)
def test_is_signal_enabled(
    signal_type, env_vars, client_options, default_val, expected
):
    # Setup environment variables using our test overrides
    for k, v in env_vars.items():
        set_test_env_override(k, v)

    result = options.is_signal_enabled(
        signal_type, client_options=client_options, default=default_val
    )
    assert result is expected


def test_is_signal_enabled_invalid_signal():
    with pytest.raises(ValueError, match="Only 'tracing' is supported"):
        options.is_signal_enabled("metrics")
