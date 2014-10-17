"""Custom exceptions for gcloud.storage package."""


class StorageError(Exception):
    """Base error class for gcloud errors."""


class ConnectionError(StorageError):
    """Exception corresponding to a bad HTTP/RPC connection."""

    def __init__(self, response, content):
        message = str(response) + content
        super(ConnectionError, self).__init__(message)
        # suppress deprecation warning under 2.6.x
        self.message = message


class NotFoundError(StorageError):
    """Exception corresponding to a 404 not found bad connection."""

    def __init__(self, response):
        super(NotFoundError, self).__init__('')
        # suppress deprecation warning under 2.6.x
        self.message = 'Request returned a 404. Headers: %s' % (response,)
