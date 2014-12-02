#!/usr/bin/env python
"""Base class for api services."""

import contextlib
import datetime
import httplib
import logging
import pprint
import types
import urllib
import urlparse


from protorpc import message_types
from protorpc import messages

from apitools.base.py import credentials_lib
from apitools.base.py import encoding
from apitools.base.py import exceptions
from apitools.base.py import http_wrapper
from apitools.base.py import util

__all__ = [
    'ApiMethodInfo',
    'ApiUploadInfo',
    'BaseApiClient',
    'BaseApiService',
    'NormalizeApiEndpoint',
]

# TODO(craigcitro): Remove this once we quiet the spurious logging in
# oauth2client (or drop oauth2client).
logging.getLogger('oauth2client.util').setLevel(logging.ERROR)

_MAX_URL_LENGTH = 2048


class ApiUploadInfo(messages.Message):
  """Media upload information for a method.

  Fields:
    accept: (repeated) MIME Media Ranges for acceptable media uploads
        to this method.
    max_size: (integer) Maximum size of a media upload, such as 3MB
        or 1TB (converted to an integer).
    resumable_path: Path to use for resumable uploads.
    resumable_multipart: (boolean) Whether or not the resumable endpoint
        supports multipart uploads.
    simple_path: Path to use for simple uploads.
    simple_multipart: (boolean) Whether or not the simple endpoint
        supports multipart uploads.
  """
  accept = messages.StringField(1, repeated=True)
  max_size = messages.IntegerField(2)
  resumable_path = messages.StringField(3)
  resumable_multipart = messages.BooleanField(4)
  simple_path = messages.StringField(5)
  simple_multipart = messages.BooleanField(6)


class ApiMethodInfo(messages.Message):
  """Configuration info for an API method.

  All fields are strings unless noted otherwise.

  Fields:
    relative_path: Relative path for this method.
    method_id: ID for this method.
    http_method: HTTP verb to use for this method.
    path_params: (repeated) path parameters for this method.
    query_params: (repeated) query parameters for this method.
    ordered_params: (repeated) ordered list of parameters for
        this method.
    description: description of this method.
    request_type_name: name of the request type.
    response_type_name: name of the response type.
    request_field: if not null, the field to pass as the body
        of this POST request. may also be the REQUEST_IS_BODY
        value below to indicate the whole message is the body.
    upload_config: (ApiUploadInfo) Information about the upload
        configuration supported by this method.
    supports_download: (boolean) If True, this method supports
        downloading the request via the `alt=media` query
        parameter.
  """

  relative_path = messages.StringField(1)
  method_id = messages.StringField(2)
  http_method = messages.StringField(3)
  path_params = messages.StringField(4, repeated=True)
  query_params = messages.StringField(5, repeated=True)
  ordered_params = messages.StringField(6, repeated=True)
  description = messages.StringField(7)
  request_type_name = messages.StringField(8)
  response_type_name = messages.StringField(9)
  request_field = messages.StringField(10, default='')
  upload_config = messages.MessageField(ApiUploadInfo, 11)
  supports_download = messages.BooleanField(12, default=False)
REQUEST_IS_BODY = '<request>'


def _LoadClass(name, messages_module):
  if name.startswith('message_types.'):
    _, _, classname = name.partition('.')
    return getattr(message_types, classname)
  elif '.' not in name:
    return getattr(messages_module, name)
  else:
    raise exceptions.GeneratedClientError('Unknown class %s' % name)


def _RequireClassAttrs(obj, attrs):
  for attr in attrs:
    attr_name = attr.upper()
    if not hasattr(obj, '%s' % attr_name) or not getattr(obj, attr_name):
      msg = 'No %s specified for object of class %s.' % (
          attr_name, type(obj).__name__)
      raise exceptions.GeneratedClientError(msg)


def NormalizeApiEndpoint(api_endpoint):
  if not api_endpoint.endswith('/'):
    api_endpoint += '/'
  return api_endpoint


class _UrlBuilder(object):
  """Convenient container for url data."""

  def __init__(self, base_url, relative_path=None, query_params=None):
    components = urlparse.urlsplit(urlparse.urljoin(
        base_url, relative_path or ''))
    if components.fragment:
      raise exceptions.ConfigurationValueError(
          'Unexpected url fragment: %s' % components.fragment)
    self.query_params = urlparse.parse_qs(components.query or '')
    if query_params is not None:
      self.query_params.update(query_params)
    self.__scheme = components.scheme
    self.__netloc = components.netloc
    self.relative_path = components.path or ''

  @classmethod
  def FromUrl(cls, url):
    urlparts = urlparse.urlsplit(url)
    query_params = urlparse.parse_qs(urlparts.query)
    base_url = urlparse.urlunsplit((
        urlparts.scheme, urlparts.netloc, '', None, None))
    relative_path = urlparts.path or ''
    return cls(base_url, relative_path=relative_path, query_params=query_params)

  @property
  def base_url(self):
    return urlparse.urlunsplit((self.__scheme, self.__netloc, '', '', ''))

  @base_url.setter
  def base_url(self, value):
    components = urlparse.urlsplit(value)
    if components.path or components.query or components.fragment:
      raise exceptions.ConfigurationValueError('Invalid base url: %s' % value)
    self.__scheme = components.scheme
    self.__netloc = components.netloc

  @property
  def query(self):
    # TODO(craigcitro): In the case that some of the query params are
    # non-ASCII, we may silently fail to encode correctly. We should
    # figure out who is responsible for owning the object -> str
    # conversion.
    return urllib.urlencode(self.query_params, doseq=True)

  @property
  def url(self):
    if '{' in self.relative_path or '}' in self.relative_path:
      raise exceptions.ConfigurationValueError(
          'Cannot create url with relative path %s' % self.relative_path)
    return urlparse.urlunsplit((
        self.__scheme, self.__netloc, self.relative_path, self.query, ''))


class BaseApiClient(object):
  """Base class for client libraries."""
  MESSAGES_MODULE = None

  _API_KEY = ''
  _CLIENT_ID = ''
  _CLIENT_SECRET = ''
  _PACKAGE = ''
  _SCOPES = []
  _USER_AGENT = ''

  def __init__(self, url, credentials=None, get_credentials=True, http=None,
               model=None, log_request=False, log_response=False, num_retries=5,
               credentials_args=None, default_global_params=None,
               additional_http_headers=None):
    _RequireClassAttrs(self, ('_package', '_scopes', 'messages_module'))
    if default_global_params is not None:
      util.Typecheck(default_global_params, self.params_type)
    self.__default_global_params = default_global_params
    self.log_request = log_request
    self.log_response = log_response
    self.__num_retries = 5
    # We let the @property machinery below do our validation.
    self.num_retries = num_retries
    self._credentials = credentials
    if get_credentials and not credentials:
      credentials_args = credentials_args or {}
      self._SetCredentials(**credentials_args)
    self._url = NormalizeApiEndpoint(url)
    self._http = http or http_wrapper.GetHttp()
    # Note that "no credentials" is totally possible.
    if self._credentials is not None:
      self._http = self._credentials.authorize(self._http)
    # TODO(craigcitro): Remove this field when we switch to proto2.
    self.__include_fields = None

    self.additional_http_headers = additional_http_headers or {}

    # TODO(craigcitro): Finish deprecating these fields.
    _ = model

    self.__response_type_model = 'proto'

  def _SetCredentials(self, **kwds):
    """Fetch credentials, and set them for this client.

    Note that we can't simply return credentials, since creating them
    may involve side-effecting self.

    Args:
      **kwds: Additional keyword arguments are passed on to GetCredentials.

    Returns:
      None. Sets self._credentials.
    """
    args = {
        'api_key': self._API_KEY,
        'client': self,
        'client_id': self._CLIENT_ID,
        'client_secret': self._CLIENT_SECRET,
        'package_name': self._PACKAGE,
        'scopes': self._SCOPES,
        'user_agent': self._USER_AGENT,
    }
    args.update(kwds)
    # TODO(craigcitro): It's a bit dangerous to pass this
    # still-half-initialized self into this method, but we might need
    # to set attributes on it associated with our credentials.
    # Consider another way around this (maybe a callback?) and whether
    # or not it's worth it.
    self._credentials = credentials_lib.GetCredentials(**args)

  @classmethod
  def ClientInfo(cls):
    return {
        'client_id': cls._CLIENT_ID,
        'client_secret': cls._CLIENT_SECRET,
        'scope': ' '.join(sorted(util.NormalizeScopes(cls._SCOPES))),
        'user_agent': cls._USER_AGENT,
    }

  @property
  def base_model_class(self):
    return None

  @property
  def http(self):
    return self._http

  @property
  def url(self):
    return self._url

  @classmethod
  def GetScopes(cls):
    return cls._SCOPES

  @property
  def params_type(self):
    return _LoadClass('StandardQueryParameters', self.MESSAGES_MODULE)

  @property
  def user_agent(self):
    return self._USER_AGENT

  @property
  def _default_global_params(self):
    if self.__default_global_params is None:
      self.__default_global_params = self.params_type()
    return self.__default_global_params

  def AddGlobalParam(self, name, value):
    params = self._default_global_params
    setattr(params, name, value)

  @property
  def global_params(self):
    return encoding.CopyProtoMessage(self._default_global_params)

  @contextlib.contextmanager
  def IncludeFields(self, include_fields):
    self.__include_fields = include_fields
    yield
    self.__include_fields = None

  @property
  def response_type_model(self):
    return self.__response_type_model

  @contextlib.contextmanager
  def JsonResponseModel(self):
    """In this context, return raw JSON instead of proto."""
    old_model = self.response_type_model
    self.__response_type_model = 'json'
    yield
    self.__response_type_model = old_model

  @property
  def num_retries(self):
    return self.__num_retries

  @num_retries.setter
  def num_retries(self, value):
    util.Typecheck(value, (int, long))
    if value < 0:
      raise exceptions.InvalidDataError(
          'Cannot have negative value for num_retries')
    self.__num_retries = value

  @contextlib.contextmanager
  def WithRetries(self, num_retries):
    old_num_retries = self.num_retries
    self.num_retries = num_retries
    yield
    self.num_retries = old_num_retries

  def ProcessRequest(self, method_config, request):
    """Hook for pre-processing of requests."""
    if self.log_request:
      logging.info(
          'Calling method %s with %s: %s', method_config.method_id,
          method_config.request_type_name, request)
    return request

  def ProcessHttpRequest(self, http_request):
    """Hook for pre-processing of http requests."""
    http_request.headers.update(self.additional_http_headers)
    if self.log_request:
      logging.info('Making http %s to %s',
                   http_request.http_method, http_request.url)
      logging.info('Headers: %s', pprint.pformat(http_request.headers))
      if http_request.body:
        # TODO(craigcitro): Make this safe to print in the case of
        # non-printable body characters.
        logging.info('Body:\n%s', http_request.body)
      else:
        logging.info('Body: (none)')
    return http_request

  def ProcessResponse(self, method_config, response):
    if self.log_response:
      logging.info('Response of type %s: %s',
                   method_config.response_type_name, response)
    return response

  # TODO(craigcitro): Decide where these two functions should live.
  def SerializeMessage(self, message):
    return encoding.MessageToJson(message, include_fields=self.__include_fields)

  def DeserializeMessage(self, response_type, data):
    """Deserialize the given data as method_config.response_type."""
    try:
      message = encoding.JsonToMessage(response_type, data)
    except (exceptions.InvalidDataFromServerError,
            messages.ValidationError) as e:
      raise exceptions.InvalidDataFromServerError(
          'Error decoding response "%s" as type %s: %s' % (
              data, response_type.__name__, e))
    return message

  def FinalizeTransferUrl(self, url):
    """Modify the url for a given transfer, based on auth and version."""
    url_builder = _UrlBuilder.FromUrl(url)
    if self.global_params.key:
      url_builder.query_params['key'] = self.global_params.key
    return url_builder.url


class BaseApiService(object):
  """Base class for generated API services."""

  def __init__(self, client):
    self.__client = client
    self._method_configs = {}
    self._upload_configs = {}

  @property
  def _client(self):
    return self.__client

  @property
  def client(self):
    return self.__client

  def GetMethodConfig(self, method):
    return self._method_configs[method]

  def GetUploadConfig(self, method):
    return self._upload_configs.get(method)

  def GetRequestType(self, method):
    method_config = self.GetMethodConfig(method)
    return getattr(self.client.MESSAGES_MODULE,
                   method_config.request_type_name)

  def GetResponseType(self, method):
    method_config = self.GetMethodConfig(method)
    return getattr(self.client.MESSAGES_MODULE,
                   method_config.response_type_name)

  def __CombineGlobalParams(self, global_params, default_params):
    util.Typecheck(global_params, (types.NoneType, self.__client.params_type))
    result = self.__client.params_type()
    global_params = global_params or self.__client.params_type()
    for field in result.all_fields():
      value = (global_params.get_assigned_value(field.name) or
               default_params.get_assigned_value(field.name))
      if value not in (None, [], ()):
        setattr(result, field.name, value)
    return result

  def __ConstructQueryParams(self, query_params, request, global_params):
    """Construct a dictionary of query parameters for this request."""
    global_params = self.__CombineGlobalParams(
        global_params, self.__client.global_params)
    query_info = dict((field.name, getattr(global_params, field.name))
                      for field in self.__client.params_type.all_fields())
    query_info.update(
        (param, getattr(request, param, None)) for param in query_params)
    query_info = dict((k, v) for k, v in query_info.iteritems()
                      if v is not None)
    for k, v in query_info.iteritems():
      if isinstance(v, unicode):
        query_info[k] = v.encode('utf8')
      elif isinstance(v, str):
        query_info[k] = v.decode('utf8')
      elif isinstance(v, datetime.datetime):
        query_info[k] = v.isoformat()
    return query_info

  def __ConstructRelativePath(self, method_config, request, relative_path=None):
    """Determine the relative path for request."""
    params = dict([(param, getattr(request, param, None))
                   for param in method_config.path_params])
    return util.ExpandRelativePath(method_config, params,
                                   relative_path=relative_path)

  def __FinalizeRequest(self, http_request, url_builder):
    """Make any final general adjustments to the request."""
    if (http_request.http_method == 'GET' and
        len(http_request.url) > _MAX_URL_LENGTH):
      http_request.http_method = 'POST'
      http_request.headers['x-http-method-override'] = 'GET'
      http_request.headers['content-type'] = 'application/x-www-form-urlencoded'
      http_request.body = url_builder.query
      url_builder.query_params = {}
    http_request.url = url_builder.url

  def __ProcessHttpResponse(self, method_config, http_response):
    """Process the given http response."""
    if http_response.status_code not in (httplib.OK, httplib.NO_CONTENT):
      raise exceptions.HttpError.FromResponse(http_response)
    if http_response.status_code == httplib.NO_CONTENT:
      # TODO(craigcitro): Find out why _replace doesn't seem to work here.
      http_response = http_wrapper.Response(
          info=http_response.info, content='{}',
          request_url=http_response.request_url)
    if self.__client.response_type_model == 'json':
      return http_response.content
    else:
      response_type = _LoadClass(
          method_config.response_type_name, self.__client.MESSAGES_MODULE)
      return self.__client.DeserializeMessage(
          response_type, http_response.content)

  def __SetBaseHeaders(self, http_request, client):
    """Fill in the basic headers on http_request."""
    # TODO(craigcitro): Make the default a little better here, and
    # include the apitools version.
    user_agent = client.user_agent or 'apitools-client/1.0'
    http_request.headers['user-agent'] = user_agent
    http_request.headers['accept'] = 'application/json'
    http_request.headers['accept-encoding'] = 'gzip, deflate'

  def __SetBody(self, http_request, method_config, request, upload):
    """Fill in the body on http_request."""
    if not method_config.request_field:
      return

    request_type = _LoadClass(
        method_config.request_type_name, self.__client.MESSAGES_MODULE)
    if method_config.request_field == REQUEST_IS_BODY:
      body_value = request
      body_type = request_type
    else:
      body_value = getattr(request, method_config.request_field)
      body_field = request_type.field_by_name(method_config.request_field)
      util.Typecheck(body_field, messages.MessageField)
      body_type = body_field.type

    if upload and not body_value:
      # We're going to fill in the body later.
      return
    util.Typecheck(body_value, body_type)
    http_request.headers['content-type'] = 'application/json'
    http_request.body = self.__client.SerializeMessage(body_value)

  def PrepareHttpRequest(self, method_config, request, global_params=None,
                         upload=None, upload_config=None, download=None):
    """Prepares an HTTP request to be sent."""
    request_type = _LoadClass(
        method_config.request_type_name, self.__client.MESSAGES_MODULE)
    util.Typecheck(request, request_type)
    request = self.__client.ProcessRequest(method_config, request)

    http_request = http_wrapper.Request(http_method=method_config.http_method)
    self.__SetBaseHeaders(http_request, self.__client)
    self.__SetBody(http_request, method_config, request, upload)

    url_builder = _UrlBuilder(
        self.__client.url, relative_path=method_config.relative_path)
    url_builder.query_params = self.__ConstructQueryParams(
        method_config.query_params, request, global_params)

    # It's important that upload and download go before we fill in the
    # relative path, so that they can replace it.
    if upload is not None:
      upload.ConfigureRequest(upload_config, http_request, url_builder)
    if download is not None:
      download.ConfigureRequest(http_request, url_builder)

    url_builder.relative_path = self.__ConstructRelativePath(
        method_config, request, relative_path=url_builder.relative_path)
    self.__FinalizeRequest(http_request, url_builder)

    return self.__client.ProcessHttpRequest(http_request)

  def _RunMethod(self, method_config, request, global_params=None,
                 upload=None, upload_config=None, download=None):
    """Call this method with request."""
    if upload is not None and download is not None:
      # TODO(craigcitro): This just involves refactoring the logic
      # below into callbacks that we can pass around; in particular,
      # the order should be that the upload gets the initial request,
      # and then passes its reply to a download if one exists, and
      # then that goes to ProcessResponse and is returned.
      raise exceptions.NotYetImplementedError(
          'Cannot yet use both upload and download at once')

    http_request = self.PrepareHttpRequest(
        method_config, request, global_params, upload, upload_config, download)

    # TODO(craigcitro): Make num_retries customizable on Transfer
    # objects, and pass in self.__client.num_retries when initializing
    # an upload or download.
    if download is not None:
      download.InitializeDownload(http_request, client=self.client)
      return

    http_response = None
    if upload is not None:
      http_response = upload.InitializeUpload(http_request, client=self.client)
    if http_response is None:
      http_response = http_wrapper.MakeRequest(
          self.__client.http, http_request, retries=self.__client.num_retries)

    return self.ProcessHttpResponse(method_config, http_response)

  def ProcessHttpResponse(self, method_config, http_response):
    """Convert an HTTP response to the expected message type."""
    return self.__client.ProcessResponse(
        method_config,
        self.__ProcessHttpResponse(method_config, http_response))
