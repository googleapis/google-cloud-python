# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

from google.cloud.streaming.exceptions import BadStatusCodeError
from google.cloud.streaming.exceptions import RequestError
from google.cloud.streaming.exceptions import RetryAfterError
from google.cloud.streaming.util import calculate_wait_for_retry


_REDIRECTIONS = 5
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

    :type level: int
    :param level: the debuglevel for logging.

    :type http: :class:`httplib2.Http`
    :param http:
        (Optional) the instance on whose connections to set the debuglevel.
    """
    if http_request.loggable_body is None:
        yield
        return
    old_level = httplib2.debuglevel
    http_levels = {}
    httplib2.debuglevel = level
    if http is not None and getattr(http, 'connections', None) is not None:
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

    :type headers: mapping
    :param headers: (Optional) headers to be sent with the request

    :type body: str
    :param body: body to be sent with the request
    """
    def __init__(self, url='', http_method='GET', headers=None, body=''):
        self.url = url
        self.http_method = http_method
        self.headers = headers or {}
        self._body = None
        self._loggable_body = None
        self.body = body

    @property
    def loggable_body(self):
        """Request body for logging purposes

        :rtype: str
        :returns: The body to be logged.
        """
        return self._loggable_body

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
        self._loggable_body = value

    @property
    def body(self):
        """Request body

        :rtype: str
        :returns: The body of the request.
        """
        return self._body

    @body.setter
    def body(self, value):
        """Update the request body

        Handles logging and length measurement.

        :type value: str
        :param value: updated body
        """
        self._body = value
        if value is not None:
            # Avoid calling len() which cannot exceed 4GiB in 32-bit python.
            body_length = getattr(
                self._body, 'length', None) or len(self._body)
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

    :rtype: int
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

        :rtype: int or long
        :returns: The length of the response.
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

        :rtype: int
        :returns: The response status code.
        """
        return int(self.info['status'])

    @property
    def retry_after(self):
        """Retry interval (if set).

        :rtype: int
        :returns: interval in seconds
        """
        if 'retry-after' in self.info:
            return int(self.info['retry-after'])

    @property
    def is_redirect(self):
        """Does this response contain a redirect

        :rtype: bool
        :returns: True if the status code indicates a redirect and the
                  'location' header is present.
        """
        return (self.status_code in _REDIRECT_STATUS_CODES and
                'location' in self.info)


def _check_response(response):
    """Validate a response

    :type response: :class:`Response`
    :param response: the response to validate

    :raises: :exc:`google.cloud.streaming.exceptions.RequestError` if response
             is None, :exc:`~.exceptions.BadStatusCodeError` if response status
             code indicates an error, or :exc:`~.exceptions.RetryAfterError`
             if response indicates a retry interval.
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


def _make_api_request_no_retry(http, http_request, redirections=_REDIRECTIONS):
    """Send an HTTP request via the given http instance.

    This wrapper exists to handle translation between the plain httplib2
    request/response types and the Request and Response types above.

    :type http: :class:`httplib2.Http`
    :param http: an instance which impelements the `Http` API.

    :type http_request: :class:`Request`
    :param http_request: the request to send.

    :type redirections: int
    :param redirections: Number of redirects to follow.

    :rtype: :class:`Response`
    :returns: an object representing the server's response

    :raises: :exc:`google.cloud.streaming.exceptions.RequestError` if no
             response could be parsed.
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
    _check_response(response)
    return response


def make_api_request(http, http_request, retries=7,
                     redirections=_REDIRECTIONS):
    """Send an HTTP request via the given http, performing error/retry handling.

    :type http: :class:`httplib2.Http`
    :param http: an instance which implements the `Http` API.

    :type http_request: :class:`Request`
    :param http_request: the request to send.

    :type retries: int
    :param retries: Number of retries to attempt on retryable
                    responses (such as 429 or 5XX).

    :type redirections: int
    :param redirections: Number of redirects to follow.

    :rtype: :class:`Response`
    :returns: an object representing the server's response.

    :raises: :exc:`google.cloud.streaming.exceptions.RequestError` if no
             response could be parsed.
    """
    retry = 0
    while True:
        try:
            return _make_api_request_no_retry(http, http_request,
                                              redirections=redirections)
        except _RETRYABLE_EXCEPTIONS as exc:
            retry += 1
            if retry >= retries:
                raise
            retry_after = getattr(exc, 'retry_after', None)
            if retry_after is None:
                retry_after = calculate_wait_for_retry(retry)

            _reset_http_connections(http)
            logging.debug('Retrying request to url %s after exception %s',
                          http_request.url, type(exc).__name__)
            time.sleep(retry_after)
