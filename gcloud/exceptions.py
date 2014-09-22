# TODO: Make these super useful.
import ast

class Error(Exception):
  """General Gcloud error."""
  def __init__(self, message, *args):
      super(GcloudClientError, self).__init__(message, *args)
      self.message = message

  def __repr__(self):
      return 'GcloudClientError: %s' % self.message

  def __str__(self):
      return 'GcloudClientError: %s' % self.message


class ConnectionError(Exception):
  """General error handler for HTTP errors for gclouds sub-modules."""
  def __init__(self, response, content, *args):
    super(ConnectionError, self).__init__(response, content, *args)
    evaluated_content = ast.literal_eval(content)
    self.headers = response
    self.status = response.status
    self.date = response['date']
    self.expires = response['expires']
    self.errors = evaluated_content["error"]["errors"]
    self.message = evaluated_content["error"]["message"]


  def __repr__(self):
    return '%s: Status: %s Message: %s' % (self.__class__.__name__,
                                           self.status, self.message)

  def __str__(self):
    return '%s: Status: %s Message: %s' % (self.__class__.__name__,
                                           self.status, self.message)
