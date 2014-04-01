from gcloud.exceptions import gcloudError

# TODO: Make these super useful.


class DNSError(gcloudError):
  pass


class ConnectionError(DNSError):

  def __init__(self, response, content):
    message = str(response) + content
    super(ConnectionError, self).__init__(message)


class NotFoundError(DNSError):

  def __init__(self, response, content):
    self.message = 'GET %s returned a 404.' % (response.url)
