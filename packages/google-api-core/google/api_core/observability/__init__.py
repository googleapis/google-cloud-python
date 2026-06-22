from .options import (
    clear_test_env_overrides,
    is_signal_enabled,
    set_test_env_override,
)

try:
    # Tell flake8 that it's okay this is unused, it's just being exposed to the package namespace.
    from .tracing import OtelSpanEnricher  # noqa: F401

    __all__ = [
        "is_signal_enabled",
        "set_test_env_override",
        "clear_test_env_overrides",
        "OtelSpanEnricher",
    ]
except ImportError:
    __all__ = [
        "is_signal_enabled",
        "set_test_env_override",
        "clear_test_env_overrides",
    ]
