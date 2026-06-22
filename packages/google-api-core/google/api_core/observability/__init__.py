from .options import is_signal_enabled

try:
    # Tell flake8 that it's okay this is unused, it's just being exposed to the package namespace.
    from .tracing import OtelSpanEnricher  # noqa: F401

    __all__ = ["is_signal_enabled", "OtelSpanEnricher"]
except ImportError:
    __all__ = ["is_signal_enabled"]
