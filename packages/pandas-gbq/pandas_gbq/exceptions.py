class AccessDenied(ValueError):
    """
    Raised when invalid credentials are provided, or tokens have expired.
    """

    pass


class InvalidPrivateKeyFormat(ValueError):
    """
    Raised when provided private key has invalid format.
    """

    pass


class PerformanceWarning(RuntimeWarning):
    """
    Raised when a performance-related feature is requested, but unsupported.

    Such warnings can occur when dependencies for the requested feature
    aren't up-to-date.
    """
