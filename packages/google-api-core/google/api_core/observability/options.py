"""Observability environment variable and client options resolution helpers."""

import os
import warnings
from typing import Any, Dict, List, Optional, Union

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
    service_name: str,
    signal_type: str,
    client_options: Optional[Union[Dict[str, Any], Any]] = None,
    default: bool = False,
    legacy_vars: Optional[List[str]] = None,
) -> bool:
    """Determines if a telemetry signal is enabled."""
    service_upper = service_name.upper().replace("-", "_")
    signal_upper = signal_type.upper()

    # 1. Resolve Programmatic Options First
    if client_options is not None:
        options_dict = (
            client_options
            if isinstance(client_options, dict)
            else getattr(client_options, "__dict__", {})
        )
        option_key = f"enable_{signal_type.lower()}"
        provider_key = f"{signal_type.rstrip('s').lower()}_provider"

        if options_dict.get(option_key) is not None:
            return bool(options_dict.get(option_key))
        if options_dict.get(provider_key) is not None:
            return True

    # 2. Language & Service-specific
    val = _get_env_bool_with_dev_fallback(
        f"GOOGLE_CLOUD_PYTHON_{service_upper}_{signal_upper}_ENABLED"
    )
    if val is not None:
        return val

    # 3. Language-wide Global
    val = _get_env_bool_with_dev_fallback(f"GOOGLE_CLOUD_PYTHON_{signal_upper}_ENABLED")
    if val is not None:
        return val

    # 4. Cross-language Service-specific
    val = _get_env_bool_with_dev_fallback(
        f"GOOGLE_CLOUD_{service_upper}_{signal_upper}_ENABLED"
    )
    if val is not None:
        return val

    # 5. Cross-language Global
    val = _get_env_bool_with_dev_fallback(f"GOOGLE_CLOUD_{signal_upper}_ENABLED")
    if val is not None:
        return val

    # 6. Legacy Variables
    if legacy_vars:
        for legacy_var in legacy_vars:
            val = _get_env_bool(legacy_var)
            if val is not None:
                warnings.warn(
                    f"Environment variable {legacy_var!r} is deprecated and will be removed "
                    "in a future release. Please migrate to the standardized "
                    f"GOOGLE_CLOUD_PYTHON_{service_upper}_{signal_upper}_ENABLED instead.",
                    DeprecationWarning,
                    stacklevel=2,
                )
                return val

    # 7. Default Fallback
    return default
