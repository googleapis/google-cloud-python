"""HTTP wrapper for apitools.

This library wraps the underlying http library we use, which is
currently :mod:`httplib2`.
"""

import collections
import contextlib
import logging
import socket
import time

import httplib2
import six
from six.moves import http_client
from six.moves.urllib import parse

from gcloud.streaming.exceptions import BadStatusCodeError
from gcloud.streaming.exceptions import RequestError
from gcloud.streaming.exceptions import RetryAfterError
from gcloud.streaming.util import calculate_wait_for_retry


# 308 and 429 don't have names in httplib.
RESUME_INCOMPLETE = 308
TOO_MANY_REQUESTS = 429


_REDIRECT_STATUS_CODES = (
    http_client.MOVED_PERMANENTLY,
    http_client.FOUND,
    http_client.SEE_OTHER,
    http_client.TEMPORARY_REDIRECT,
    RESUME_INCOMPLETE,
)


_RETRYABLE_EXCEPTIONS = (
    http_client.BadStatusLine,
    http_client.IncompleteRead,
    http_client.ResponseNotReady,
    socket.error,
    httplib2.ServerNotFoundError,
    ValueError,
    RequestError,
    BadStatusCodeError,
    RetryAfterError,
)


class _ExceptionRetryArgs(
        collections.namedtuple(
            '_ExceptionRetryArgs',
            ['http', 'http_request', 'exc', 'num_retries', 'max_retry_wait'])):
    """Bundle of information for retriable exceptions.

    :type http: :class:`httplib2.Http` (or conforming alternative)
    :param http: instance used to perform requests.

    :type http_request: :class:`Request`
    :param http_request: the request whose response was a retriable error

    :type exc: :class:`Exception` subclass
    :param exc: the exception being raised.

    :type num_retries: integer
    :param num_retries: Number of retries consumed; used for exponential
                        backoff.
    """


@contextlib.contextmanager
def _httplib2_debug_level(http_request, level, http=None):
    """Temporarily change the value of httplib2.debuglevel, if necessary.

    If http_request has a `loggable_body` distinct from `body`, then we
    need to prevent httplib2 from logging the full body. This sets
    httplib2.debuglevel for the duration of the `with` block; however,
    that alone won't change the value of existing HTTP connections. If
    an httplib2.Http object is provided, we'll also change the level on
    any cached connections attached to it.

    :type http_request: :class:`Request`
    :param http_request: the request to be logged.

    :type level: integer
    :param level: the debuglevel for logging.

    :type http: :class:`httplib2.Http`, or ``None``
    :param http: the instance on whose connections to set the debuglevel.
    """
    if http_request.loggable_body is None:
        yield
        return
    old_level = httplib2.debuglevel
    http_levels = {}
    httplib2.debuglevel = level
    if http is not None:
        for connection_key, connection in http.connections.items():
            # httplib2 stores two kinds of values in this dict, connection
            # classes and instances. Since the connection types are all
            # old-style classes, we can't easily distinguish by connection
            # type -- so instead we use the key pattern.
            if ':' not in connection_key:
                continue
            http_levels[connection_key] = connection.debuglevel
            connection.set_debuglevel(level)
    yield
    httplib2.debuglevel = old_level
    if http is not None:
        for connection_key, old_level in http_levels.items():
            http.connections[connection_key].set_debuglevel(old_level)


class Request(object):
    """Encapsulates the data for an HTTP request.

    :type url: str
    :param url: the URL for the request

    :type http_method: str
    :param http_method: the HTTP method to use for the request

    :type headers: mapping or None
    :param headers: headers to be sent with the request

    :type body: str
    :param body: body to be sent with the request
    """
    def __init__(self, url='', http_method='GET', headers=None, body=''):
        self.url = url
        self.http_method = http_method
        self.headers = headers or {}
        self.__body = None
        self.__loggable_body = None
        self.body = body

    @property
    def loggable_body(self):
        """Request body for logging purposes

        :rtype: str
        """
        return self.__loggable_body

    @loggable_body.setter
    def loggable_body(self, value):
        """Update request body for logging purposes

        :type value: str
        :param value: updated body

        :raises: :exc:`RequestError` if the request does not have a body.
        """
        if self.body is None:
            raise RequestError(
                'Cannot set loggable body on request with no body')
        self.__loggable_body = value

    @property
    def body(self):
        """Request body

        :rtype: str
        """
        return self.__body

    @body.setter
    def body(self, value):
        """Update the request body

        Handles logging and length measurement.

        :type value: str
        :param value: updated body
        """
        self.__body = value
        if value is not None:
            # Avoid calling len() which cannot exceed 4GiB in 32-bit python.
            body_length = getattr(
                self.__body, 'length', None) or len(self.__body)
            self.headers['content-length'] = str(body_length)
        else:
            self.headers.pop('content-length', None)
        # This line ensures we don't try to print large requests.
        if not isinstance(value, (type(None), six.string_types)):
            self.loggable_body = '<media body>'


def _process_content_range(content_range):
    """Convert a 'Content-Range' header into a length for the response.

    Helper for :meth:`Response.length`.

    :type content_range: str
    :param content_range: the header value being parsed.

    :rtype: integer
    :returns: the length of the response chunk.
    """
    _, _, range_spec = content_range.partition(' ')
    byte_range, _, _ = range_spec.partition('/')
    start, _, end = byte_range.partition('-')
    return int(end) - int(start) + 1


# Note: currently the order of fields here is important, since we want
# to be able to pass in the result from httplib2.request.
_ResponseTuple = collections.namedtuple(
    'HttpResponse', ['info', 'content', 'request_url'])


class Response(_ResponseTuple):
    """Encapsulates data for an HTTP response.
    """
    __slots__ = ()

    def __len__(self):
        return self.length

    @property
    def length(self):
        """Length of this response.

        Exposed as an attribute since using ``len()`` directly can fail
        for responses larger than ``sys.maxint``.

        :rtype: integer or long
        """
        if 'content-encoding' in self.info and 'content-range' in self.info:
            # httplib2 rewrites content-length in the case of a compressed
            # transfer; we can't trust the content-length header in that
            # case, but we *can* trust content-range, if it's present.
            return _process_content_range(self.info['content-range'])
        elif 'content-length' in self.info:
            return int(self.info.get('content-length'))
        elif 'content-range' in self.info:
            return _process_content_range(self.info['content-range'])
        return len(self.content)

    @property
    def status_code(self):
        """HTTP status code

        :rtype: integer
        """
        return int(self.info['status'])

    @property
    def retry_after(self):
        """Retry interval (if set).

        :rtype: integer
        :returns: interval in seconds
        """
        if 'retry-after' in self.info:
            return int(self.info['retry-after'])

    @property
    def is_redirect(self):
        """Does this response contain a redirect

        :rtype: boolean
        :returns: True if the status code indicates a redirect and the
                  'location' header is present.
        """
        return (self.status_code in _REDIRECT_STATUS_CODES and
                'location' in self.info)


def _check_response(response):
    """Validate a response

    :type response: :class:`Response`
    :param response: the response to validate

    :raises: :exc:`gcloud.streaming.exceptions.RequestError` if response is
             None, :exc:`gcloud.streaming.exceptions.BadStatusCodeError` if
             response status code indicates an error, or
             :exc:`gcloud.streaming.exceptions.RetryAfterError` if response
             indicates a retry interval.
    """
    if response is None:
        # Caller shouldn't call us if the response is None, but handle anyway.
        raise RequestError(
            'Request did not return a response.')
    elif (response.status_code >= 500 or
          response.status_code == TOO_MANY_REQUESTS):
        raise BadStatusCodeError.from_response(response)
    elif response.retry_after:
        raise RetryAfterError.from_response(response)


def _reset_http_connections(http):
    """Rebuild all http connections in the httplib2.Http instance.

    httplib2 overloads the map in http.connections to contain two different
    types of values:
    { scheme string:  connection class } and
    { scheme + authority string : actual http connection }
    Here we remove all of the entries for actual connections so that on the
    next request httplib2 will rebuild them from the connection types.

    :type http: :class:`httplib2.Http`
    :param http: the instance whose connections are to be rebuilt
    """
    if getattr(http, 'connections', None):
        for conn_key in list(http.connections.keys()):
            if ':' in conn_key:
                del http.connections[conn_key]


def _make_api_request_no_retry(http, http_request, redirections=5,
                               check_response_func=_check_response):
    """Send an HTTP request via the given http instance.

    This wrapper exists to handle translation between the plain httplib2
    request/response types and the Request and Response types above.

    :type http: :class:`httplib2.Http`
    :param http: an instance which impelements the `Http` API.

    :type http_request: :class:`Request`
    :param http_request: the request to send.

    :type redirections: integer
    :param redirections: Number of redirects to follow.

    :type check_response_func: function taking (response, content, url).
    :param check_response_func: Function to validate the HTTP response.

    :rtype: :class:`Response`
    :returns: an object representing the server's response

    :raises: :exc:`gcloud.streaming.exceptions.RequestError` if no response
             could be parsed.
    """
    connection_type = None
    # Handle overrides for connection types.  This is used if the caller
    # wants control over the underlying connection for managing callbacks
    # or hash digestion.
    if getattr(http, 'connections', None):
        url_scheme = parse.urlsplit(http_request.url).scheme
        if url_scheme and url_scheme in http.connections:
            connection_type = http.connections[url_scheme]

    # Custom printing only at debuglevel 4
    new_debuglevel = 4 if httplib2.debuglevel == 4 else 0
    with _httplib2_debug_level(http_request, new_debuglevel, http=http):
        info, content = http.request(
            str(http_request.url), method=str(http_request.http_method),
            body=http_request.body, headers=http_request.headers,
            redirections=redirections, connection_type=connection_type)

    if info is None:
        raise RequestError()

    response = Response(info, content, http_request.url)
    check_response_func(response)
    return response


def make_api_request(http, http_request,
                     retries=7,
                     max_retry_wait=60,
                     redirections=5,
                     check_response_func=_check_response,
                     wo_retry_func=_make_api_request_no_retry):
    """Send an HTTP request via the given http, performing error/retry handling.

    :type http: :class:`httplib2.Http`
    :param http: an instance which impelements the `Http` API.

    :type http_request: :class:`Request`
    :param http_request: the request to send.

    :type retries: integer
    :param retries: Number of retries to attempt on retryable
                    responses (such as 429 or 5XX).

    :type max_retry_wait: integer
    :param max_retry_wait: Maximum number of seconds to wait when retrying.

    :type redirections: integer
    :param redirections: Number of redirects to follow.

    :type check_response_func: function taking (response, content, url).
    :param check_response_func: Function to validate the HTTP response.

    :type wo_retry_func: function taking
                         (http, request, redirections, check_response_func)
    :param wo_retry_func: Function to make HTTP request without retries.

    :rtype: :class:`Response`
    :returns: an object representing the server's response

    :raises: :exc:`gcloud.streaming.exceptions.RequestError` if no response
             could be parsed.
    """
    retry = 0
    while True:
        try:
            return wo_retry_func(
                http, http_request, redirections=redirections,
                check_response_func=check_response_func)
        except _RETRYABLE_EXCEPTIONS as exc:
            retry += 1
            if retry >= retries:
                raise
            retry_after = getattr(exc, 'retry_after', None)
            if retry_after is None:
                retry_after = calculate_wait_for_retry(retry, max_retry_wait)

            _reset_http_connections(http)
            logging.debug('Retrying request to url %s after exception %s',
                          http_request.url, type(exc).__name__)
            time.sleep(retry_after)


_HTTP_FACTORIES = []


def _register_http_factory(factory):
    """Register a custom HTTP factory.

    :type factory: callable taking keyword arguments, returning an Http
                   instance (or an instance implementing the same API);
    :param factory: the new factory (it may return ``None`` to defer to
                    a later factory or the default).
    """
    _HTTP_FACTORIES.append(factory)


def get_http(**kwds):
    """Construct an Http instance.

    :type kwds: dict
    :param kwds:  keyword arguments to pass to factories.

    :rtype: :class:`httplib2.Http` (or a workalike)
    """
    for factory in _HTTP_FACTORIES:
        http = factory(**kwds)
        if http is not None:
            return http
    return httplib2.Http(**kwds)
