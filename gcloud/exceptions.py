# TODO: Make these super useful.


class gcloudError(Exception):
  pass


class ConnectionError(gcloudError):

  def __init__(self, response, content):
    message = str(response) + content
    super(ConnectionError, self).__init__(message)


class NotFoundError(gcloudError):

  def __init__(self, response, content):
    self.message = 'GET %s returned a 404.' % (response.url)
