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




def test_resolve_feature_flags_ga_enabled_via_env():
    """Verify that a GA feature is enabled if its environment variable is True."""
    # Setup: We pass a GA environment variable set to True
    set_test_env_override("GOOGLE_SDK_PYTHON_TRACING_ENABLED", True)

    # Action
    result = options.resolve_feature_flags(
        env_var="GOOGLE_SDK_PYTHON_TRACING_ENABLED",
        provider_key="tracer_provider",
        client_options=None
    )

    # Assertion
    assert result is True


@pytest.mark.parametrize("gate_value", [None, False])
def test_resolve_feature_flags_exp_blocked_with_provider_fails_fast(gate_value):
    """Verify that passing a provider to an experimental feature without the gate raises ValueError."""
    # Setup: Experimental env var is set to gate_value (None means not set)
    set_test_env_override("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", gate_value)
    client_options = {"tracer_provider": object()}

    # Action & Assertion
    with pytest.raises(ValueError, match="Experimental feature"):
        options.resolve_feature_flags(
            env_var="GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED",
            provider_key="tracer_provider",
            client_options=client_options
        )


def test_resolve_feature_flags_exp_enabled_with_provider():
    """Verify that experimental feature is enabled if gate is True, even with provider."""
    set_test_env_override("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", True)
    client_options = {"tracer_provider": object()}

    result = options.resolve_feature_flags(
        env_var="GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED",
        provider_key="tracer_provider",
        client_options=client_options
    )
    assert result is True


def test_resolve_feature_flags_ga_enabled_via_provider():
    """Verify that a GA feature is enabled if a provider is passed, bypassing env var."""
    # Env var is False, but provider is present
    set_test_env_override("GOOGLE_SDK_PYTHON_TRACING_ENABLED", False)
    client_options = {"tracer_provider": object()}

    result = options.resolve_feature_flags(
        env_var="GOOGLE_SDK_PYTHON_TRACING_ENABLED",
        provider_key="tracer_provider",
        client_options=client_options
    )
    assert result is True


@pytest.mark.parametrize("env_val", [None, False], ids=["env_not_set", "env_explicit_false"])
def test_resolve_feature_flags_ga_fallback_to_false(env_val):
    """Verify that a GA feature returns False if no flags are present."""
    set_test_env_override("GOOGLE_SDK_PYTHON_TRACING_ENABLED", env_val)
    result = options.resolve_feature_flags(
        env_var="GOOGLE_SDK_PYTHON_TRACING_ENABLED",
        provider_key="tracer_provider",
        client_options=None
    )
    assert result is False


class _MockOptions:
    def __init__(self):
        self.other_option = "value"


@pytest.mark.parametrize(
    "client_options",
    [
        {"other_option": "value"},
        _MockOptions(),
    ],
    ids=["dict_without_key", "object_without_key"]
)
def test_resolve_feature_flags_options_without_key(client_options):
    """Verify behavior when client_options is present but missing the provider key."""
    # GA Path: should fall through to env var / fallback
    result = options.resolve_feature_flags(
        env_var="GOOGLE_SDK_PYTHON_TRACING_ENABLED",
        provider_key="tracer_provider",
        client_options=client_options
    )
    assert result is False
