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
#

"""Observability environment variable and client options resolution helpers."""

import os
from typing import Any, Dict, Optional, Union

# Allowed truthy and falsy patterns for environment variables
_TRUTHY_VALUES = ("y", "yes", "t", "true", "on", "1")
_FALSY_VALUES = ("n", "no", "f", "false", "off", "0")

# Test-only overrides for environment variables.
# This is intended ONLY for unit/integration testing to prevent mutating
# os.environ.
_TEST_ENV_OVERRIDES: Dict[str, bool] = {}


def _strtobool(val: str) -> Optional[bool]:
    """Convert a string representation of truth to a boolean."""
    clean_val = val.lower().strip()
    if not clean_val:
        return None
    if clean_val in _TRUTHY_VALUES:
        return True
    if clean_val in _FALSY_VALUES:
        return False
    raise ValueError(f"Invalid truth value: {val!r}")


def set_test_env_override(name: str, value: Optional[bool]) -> None:
    """Sets a test-only override for a specific environment variable.

    This is intended ONLY for unit/integration testing to prevent mutating
    os.environ.
    """
    if value is None:
        _TEST_ENV_OVERRIDES.pop(name, None)
    else:
        _TEST_ENV_OVERRIDES[name] = value


def clear_test_env_overrides() -> None:
    """Clears all test-only overrides."""
    _TEST_ENV_OVERRIDES.clear()


def _get_env_bool(name: str) -> Optional[bool]:
    """Retrieve the boolean value of an environment variable."""
    if name in _TEST_ENV_OVERRIDES:
        return _TEST_ENV_OVERRIDES[name]

    val = os.getenv(name)
    if val is None:
        return None
    try:
        return _strtobool(val)
    except ValueError:
        return None


def _get_env_bool_with_dev_fallback(name: str) -> Optional[bool]:
    """Retrieve the boolean value of an environment variable, checking experimental fallbacks first."""
    if name.startswith("GOOGLE_SDK_"):
        exp_name = name.replace("GOOGLE_SDK_", "GOOGLE_SDK_EXPERIMENTAL_", 1)
        val = _get_env_bool(exp_name)
        if val is not None:
            return val
    return _get_env_bool(name)


def resolve_feature_flags(
    feature_name: str,
    client_options: Optional[Union[Dict[str, Any], Any]] = None,
    default: bool = False,
) -> bool:
    """Determines if a telemetry signal is enabled.

    Resolves settings in the following order of precedence:
    1. Programmatic overrides in client_options (checks tracer_provider)
    2. Language-wide Environment Variable: GOOGLE_SDK_PYTHON_TRACING_ENABLED
       (natively checks for a variant with an "EXPERIMENTAL" token first)
    3. Default fallback

    Args:
        feature_name: The feature name: must be 'tracing'.
        client_options: A dictionary or object containing client configuration.
        default: Fallback boolean if no options or env variables match.

    Returns:
        bool: True if the signal is resolved to enabled, False otherwise.
    """
    if feature_name != "tracing":
        raise ValueError(
            f"Invalid feature_name: {feature_name!r}. Only 'tracing' is supported at this time."
        )

    # 1. Experimental Gate
    exp_var = "GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED"
    exp_val = _get_env_bool(exp_var)

    has_provider = False
    if client_options is not None:
        options_dict = (
            client_options
            if isinstance(client_options, dict)
            else getattr(client_options, "__dict__", {})
        )
        if options_dict.get("tracer_provider") is not None:
            has_provider = True

    if exp_val is not True:
        if has_provider:
            raise ValueError(
                f"Experimental feature {feature_name!r} requires {exp_var} to be set to 'true' to use programmatic providers."
            )
        return False # Blocked

    # If we are here, exp_val IS True.
    return True
