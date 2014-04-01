# TODO: Make these super useful.


class Error(Exception):
  pass


class ConnectionError(Error):

  def __init__(self, response, content):
    message = str(response) + content
    super(ConnectionError, self).__init__(message)


class NotFoundError(Error):

  def __init__(self, response, content):
    self.message = 'GET %s returned a 404.' % (response.url)
