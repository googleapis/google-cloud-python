import httplib2
import json
import urllib

from gcloud import exceptions


class Connection(object):
  """A generic connection to Google Cloud Platform.

  Subclasses should understand
  only the basic types
  in method arguments,
  however they should be capable
  of returning advanced types.
  """

  API_BASE_URL = 'https://www.googleapis.com'
  """The base of the API call URL."""

  _EMPTY = object()
  """A pointer to represent an empty value for default arguments."""

  def __init__(self, credentials=None):
    """
    :type credentials: :class:`gcloud.credentials.Credentials`
    :param credentials: The OAuth2 Credentials to use for this connection.
    """

    self._credentials = credentials

  @property
  def credentials(self):
    return self._credentials

  @property
  def http(self):
    """A getter for the HTTP transport used in talking to the API.

    :rtype: :class:`httplib2.Http`
    :returns: A Http object used to transport data.
    """
    if not hasattr(self, '_http'):
      self._http = httplib2.Http()
      if self._credentials:
        self._http = self._credentials.authorize(self._http)
    return self._http


class JsonConnection(Connection):

  API_BASE_URL = 'https://www.googleapis.com'
  """The base of the API call URL."""

  _EMPTY = object()
  """A pointer to represent an empty value for default arguments."""

  def __init__(self, project=None, *args, **kwargs):

    super(JsonConnection, self).__init__(*args, **kwargs)

    self.project = project

  def build_api_url(self, path, query_params=None, api_base_url=None,
                    api_version=None):

    url = self.API_URL_TEMPLATE.format(
        api_base_url=(api_base_url or self.API_BASE_URL),
        api_version=(api_version or self.API_VERSION),
        path=path)

    query_params = query_params or {}
    query_params.update({'project': self.project})
    url += '?' + urllib.urlencode(query_params)

    return url

  def make_request(self, method, url, data=None, content_type=None,
                   headers=None):

    headers = headers or {}
    headers['Accept-Encoding'] = 'gzip'

    if data:
      content_length = len(str(data))
    else:
      content_length = 0

    headers['Content-Length'] = content_length

    if content_type:
      headers['Content-Type'] = content_type

    return self.http.request(uri=url, method=method, headers=headers,
                             body=data)

  def api_request(self, method, path=None, query_params=None,
                  data=None, content_type=None,
                  api_base_url=None, api_version=None,
                  expect_json=True):

    url = self.build_api_url(path=path, query_params=query_params,
                             api_base_url=api_base_url,
                             api_version=api_version)

    # Making the executive decision that any dictionary
    # data will be sent properly as JSON.
    if data and isinstance(data, dict):
      data = json.dumps(data)
      content_type = 'application/json'

    response, content = self.make_request(
        method=method, url=url, data=data, content_type=content_type)

    # TODO: Add better error handling.
    if response.status == 404:
      raise exceptions.NotFoundError(response, content)
    elif not 200 <= response.status < 300:
      raise exceptions.ConnectionError(response, content)

    if content and expect_json:
      # TODO: Better checking on this header for JSON.
      content_type = response.get('content-type', '')
      if not content_type.startswith('application/json'):
        raise TypeError('Expected JSON, got %s' % content_type)
      return json.loads(content)

    return content
