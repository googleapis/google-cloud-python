# Copyright 2014 Google Inc.
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

"""Custom exceptions for :mod:`google.cloud` package.

See https://cloud.google.com/storage/docs/json_api/v1/status-codes
"""

# Avoid the grpc and google.cloud.grpc collision.
from __future__ import absolute_import

import copy

import six

from google.cloud._helpers import _to_bytes

try:
    from grpc._channel import _Rendezvous
except ImportError:  # pragma: NO COVER
    _Rendezvous = None

_HTTP_CODE_TO_EXCEPTION = {}  # populated at end of module


# pylint: disable=invalid-name
GrpcRendezvous = _Rendezvous
"""Exception class raised by gRPC stable."""
# pylint: enable=invalid-name


class GoogleCloudError(Exception):
    """Base error class for Google Cloud errors (abstract).

    Each subclass represents a single type of HTTP error response.
    """
    code = None
    """HTTP status code.  Concrete subclasses *must* define.

    See http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
    """

    def __init__(self, message, errors=()):
        super(GoogleCloudError, self).__init__(message)
        self.message = message
        self._errors = errors

    def __str__(self):
        result = u'%d %s' % (self.code, self.message)
        if six.PY2:
            result = _to_bytes(result, 'utf-8')
        return result

    @property
    def errors(self):
        """Detailed error information.

        :rtype: list(dict)
        :returns: a list of mappings describing each error.
        """
        return [copy.deepcopy(error) for error in self._errors]


class Redirection(GoogleCloudError):
    """Base for 3xx responses

    This class is abstract.
    """


class MovedPermanently(Redirection):
    """Exception mapping a '301 Moved Permanently' response."""
    code = 301


class NotModified(Redirection):
    """Exception mapping a '304 Not Modified' response."""
    code = 304


class TemporaryRedirect(Redirection):
    """Exception mapping a '307 Temporary Redirect' response."""
    code = 307


class ResumeIncomplete(Redirection):
    """Exception mapping a '308 Resume Incomplete' response."""
    code = 308


class ClientError(GoogleCloudError):
    """Base for 4xx responses

    This class is abstract
    """


class BadRequest(ClientError):
    """Exception mapping a '400 Bad Request' response."""
    code = 400


class Unauthorized(ClientError):
    """Exception mapping a '401 Unauthorized' response."""
    code = 401


class Forbidden(ClientError):
    """Exception mapping a '403 Forbidden' response."""
    code = 403


class NotFound(ClientError):
    """Exception mapping a '404 Not Found' response."""
    code = 404


class MethodNotAllowed(ClientError):
    """Exception mapping a '405 Method Not Allowed' response."""
    code = 405


class Conflict(ClientError):
    """Exception mapping a '409 Conflict' response."""
    code = 409


class LengthRequired(ClientError):
    """Exception mapping a '411 Length Required' response."""
    code = 411


class PreconditionFailed(ClientError):
    """Exception mapping a '412 Precondition Failed' response."""
    code = 412


class RequestRangeNotSatisfiable(ClientError):
    """Exception mapping a '416 Request Range Not Satisfiable' response."""
    code = 416


class TooManyRequests(ClientError):
    """Exception mapping a '429 Too Many Requests' response."""
    code = 429


class ServerError(GoogleCloudError):
    """Base for 5xx responses:  (abstract)"""


class InternalServerError(ServerError):
    """Exception mapping a '500 Internal Server Error' response."""
    code = 500


class MethodNotImplemented(ServerError):
    """Exception mapping a '501 Not Implemented' response."""
    code = 501


class BadGateway(ServerError):
    """Exception mapping a '502 Bad Gateway' response."""
    code = 502


class ServiceUnavailable(ServerError):
    """Exception mapping a '503 Service Unavailable' response."""
    code = 503


class GatewayTimeout(ServerError):
    """Exception mapping a `504 Gateway Timeout'` response."""
    code = 504


def from_http_status(status_code, message, errors=()):
    """Create a :class:`GoogleCloudError` from an HTTP status code.

    Args:
        status_code (int): The HTTP status code.
        message (str): The exception message.
        errors (Sequence[Any]): A list of additional error information.

    Returns:
        GoogleCloudError: An instance of the appropriate subclass of
            :class:`GoogleCloudError`.
    """
    error_class = _HTTP_CODE_TO_EXCEPTION.get(status_code, GoogleCloudError)
    error = error_class(message, errors)

    if error.code is None:
        error.code = status_code

    return error


def from_http_response(response):
    """Create a :class:`GoogleCloudError` from a :class:`requests.Response`.

    Args:
        response (requests.Response): The HTTP response.

    Returns:
        GoogleCloudError: An instance of the appropriate subclass of
            :class:`GoogleCloudError`, with the message and errors populated
            from the response.
    """
    try:
        payload = response.json()
    except ValueError:
        payload = {'error': {'message': response.text or 'unknown error'}}

    error_message = payload.get('error', {}).get('message', 'unknown error')
    errors = payload.get('error', {}).get('errors', ())

    message = '{method} {url}: {error}'.format(
        method=response.request.method,
        url=response.request.url,
        error=error_message)

    exception = from_http_status(
        response.status_code, message, errors=errors)
    exception.response = response
    return exception


def _walk_subclasses(klass):
    """Recursively walk subclass tree."""
    for sub in klass.__subclasses__():
        yield sub
        for subsub in _walk_subclasses(sub):
            yield subsub


# Build the code->exception class mapping.
for _eklass in _walk_subclasses(GoogleCloudError):
    code = getattr(_eklass, 'code', None)
    if code is not None:
        _HTTP_CODE_TO_EXCEPTION[code] = _eklass
