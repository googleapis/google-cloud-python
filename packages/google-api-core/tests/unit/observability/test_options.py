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
        ("y", True),
        ("yes", True),
        ("t", True),
        ("true", True),
        ("on", True),
        ("1", True),
        ("n", False),
        ("no", False),
        ("f", False),
        ("false", False),
        ("off", False),
        ("0", False),
        ("  True  ", True),
        (" FALSE ", False),
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


@pytest.mark.parametrize(
    "env_vars, client_options, default_val, expected",
    [
        # Default fallback tests
        ({}, None, False, False),
        ({}, None, True, True),
        # Service-specific env var
        ({"GOOGLE_CLOUD_PYTHON_TRANSLATE_TRACES_ENABLED": True}, None, False, True),
        ({"GOOGLE_CLOUD_PYTHON_TRANSLATE_TRACES_ENABLED": False}, None, True, False),
        # Experimental fallback
        (
            {"GOOGLE_CLOUD_EXPERIMENTAL_PYTHON_TRANSLATE_TRACES_ENABLED": True},
            None,
            False,
            True,
        ),
        # Precedence: Service specific overrides global
        (
            {
                "GOOGLE_CLOUD_PYTHON_TRACES_ENABLED": True,
                "GOOGLE_CLOUD_PYTHON_TRANSLATE_TRACES_ENABLED": False,
            },
            None,
            False,
            False,
        ),
        (
            {
                "GOOGLE_CLOUD_PYTHON_TRACES_ENABLED": False,
                "GOOGLE_CLOUD_PYTHON_TRANSLATE_TRACES_ENABLED": True,
            },
            None,
            False,
            True,
        ),
        # Precedence: Client options override env vars
        (
            {"GOOGLE_CLOUD_PYTHON_TRANSLATE_TRACES_ENABLED": False},
            {"enable_traces": True},
            False,
            True,
        ),
    ],
)
def test_is_signal_enabled(env_vars, client_options, default_val, expected):
    # Setup environment variables using our test overrides
    for k, v in env_vars.items():
        set_test_env_override(k, v)

    result = options.is_signal_enabled(
        "translate", "traces", client_options=client_options, default=default_val
    )
    assert result is expected


def test_legacy_var_with_warning():
    set_test_env_override("LEGACY_TRACE_VAR", True)

    with pytest.warns(DeprecationWarning, match="LEGACY_TRACE_VAR"):
        result = options.is_signal_enabled(
            "translate", "traces", legacy_vars=["LEGACY_TRACE_VAR"]
        )
        assert result is True
