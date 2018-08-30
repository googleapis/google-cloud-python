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
