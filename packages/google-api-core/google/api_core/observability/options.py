"""Observability environment variable and client options resolution helpers."""

import os
from typing import Any, Dict, Optional, Union

# Allowed truthy and falsy patterns for environment variables
_TRUTHY_VALUES = ("y", "yes", "t", "true", "on", "1")
_FALSY_VALUES = ("n", "no", "f", "false", "off", "0")


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


_TEST_ENV_OVERRIDES: Dict[str, bool] = {}


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
    """Retrieve the boolean value of an environment variable, checking dev/exp fallbacks first."""
    if name.startswith("GOOGLE_CLOUD_"):
        exp_name = name.replace("GOOGLE_CLOUD_", "GOOGLE_CLOUD_EXPERIMENTAL_", 1)
        val = _get_env_bool(exp_name)
        if val is not None:
            return val
    return _get_env_bool(name)


def is_signal_enabled(
    signal_type: str,
    client_options: Optional[Union[Dict[str, Any], Any]] = None,
    default: bool = False,
) -> bool:
    """Determines if a telemetry signal is enabled.

    Resolves settings in the following order of precedence:
    1. Programmatic overrides in client_options (checks tracer_provider)
    2. Language-wide Environment Variable: GOOGLE_CLOUD_PYTHON_TRACING_ENABLED
       (natively checks for an EXPERIMENTAL prefix variant first)
    3. Default fallback

    Args:
        signal_type: The signal type: must be 'tracing'.
        client_options: A dictionary or object representing client configuration.
        default: Fallback boolean if no options or env variables match.

    Returns:
        bool: True if the signal is resolved to enabled, False otherwise.
    """
    if signal_type != "tracing":
        raise ValueError(
            f"Invalid signal_type: {signal_type!r}. Only 'tracing' is supported."
        )

    # 1. Resolve Programmatic Options First
    if client_options is not None:
        options_dict = (
            client_options
            if isinstance(client_options, dict)
            else getattr(client_options, "__dict__", {})
        )

        if options_dict.get("tracer_provider") is not None:
            return True

    # 2. Check Language-Wide Environment Variable
    val = _get_env_bool_with_dev_fallback("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED")
    if val is not None:
        return val

    # 3. Default Fallback
    return default
