# TODO: Make these super useful.


class ComputeError(Exception):
  pass


class ConnectionError(ComputeError):

  def __init__(self, response, content):
    message = str(response) + content
    super(ConnectionError, self).__init__(message)


class NotFoundError(ConnectionError):

  def __init__(self, response, content):
    self.message = 'GET %s returned a 404.' % (response.url)
