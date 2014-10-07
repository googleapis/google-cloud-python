class StorageError(Exception):
    pass


class ConnectionError(StorageError):

    def __init__(self, response, content):
        message = str(response) + content
        super(ConnectionError, self).__init__(message)
        # suppress deprecation warning under 2.6.x
        self.message = message


class NotFoundError(ConnectionError):

    def __init__(self, response, content):
        self.message = 'Request returned a 404. Headers: %s' % (response)


class StorageDataError(StorageError):
    pass
