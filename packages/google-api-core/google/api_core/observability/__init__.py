try:
    # Tell flake8 that it's okay this is unused, it's just being exposed to the package namespace.
    from .tracing import OtelUnaryClientInterceptor  # noqa: F401

    __all__ = [
        "OtelUnaryClientInterceptor",
    ]
except ImportError:
    __all__ = []
