# Copyright 2014 Google Inc. All rights reserved.
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

"""Custom exceptions for gcloud.storage package.

See: https://cloud.google.com/storage/docs/json_api/v1/status-codes
"""

import copy
import json
import six

_HTTP_CODE_TO_EXCEPTION = {}  # populated at end of module


class GCloudError(Exception):
    """Base error class for gcloud errors (abstract).

    Each subclass represents a single type of HTTP error response.
    """
    code = None
    """HTTP status code.  Concrete subclasses *must* define.

    See: http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
    """

    def __init__(self, message, errors=()):
        super(GCloudError, self).__init__()
        # suppress deprecation warning under 2.6.x
        self.message = message
        self._errors = errors

    def __str__(self):
        return '%d %s' % (self.code, self.message)

    @property
    def errors(self):
        """Detailed error information.

        :rtype: list(dict)
        :returns: a list of mappings describing each error.
        """
        return [copy.deepcopy(error) for error in self._errors]


class Redirection(GCloudError):
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


class ClientError(GCloudError):
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


class ServerError(GCloudError):
    """Base for 5xx responses:  (abstract)"""


class InternalServerError(ServerError):
    """Exception mapping a '500 Internal Server Error' response."""
    code = 500


class NotImplemented(ServerError):
    """Exception mapping a '501 Not Implemented' response."""
    code = 501


class ServiceUnavailable(ServerError):
    """Exception mapping a '503 Service Unavailable' response."""
    code = 503


def make_exception(response, content, error_info=None, use_json=True):
    """Factory:  create exception based on HTTP response code.

    :type response: :class:`httplib2.Response` or other HTTP response object
    :param response: A response object that defines a status code as the
                     status attribute.

    :type content: string or dictionary
    :param content: The body of the HTTP error response.

    :type error_info: string
    :param error_info: Optional string giving extra information about the
                       failed request.

    :type use_json: boolean
    :param use_json: Flag indicating if ``content`` is expected to be JSON.

    :rtype: instance of :class:`GCloudError`, or a concrete subclass.
    :returns: Exception specific to the error response.
    """
    if isinstance(content, six.binary_type):
        content = content.decode('utf-8')

    if isinstance(content, six.string_types):
        if use_json:
            payload = json.loads(content)
        else:
            payload = {'error': {'message': content}}
    else:
        payload = content

    message = payload.get('error', {}).get('message', '')
    errors = payload.get('error', {}).get('errors', ())

    if error_info is not None:
        message += ' (%s)' % (error_info,)

    try:
        klass = _HTTP_CODE_TO_EXCEPTION[response.status]
    except KeyError:
        error = GCloudError(message, errors)
        error.code = response.status
    else:
        error = klass(message, errors)
    return error


def _walk_subclasses(klass):
    """Recursively walk subclass tree."""
    for sub in klass.__subclasses__():
        yield sub
        for subsub in _walk_subclasses(sub):
            yield subsub


# Build the code->exception class mapping.
for eklass in _walk_subclasses(GCloudError):
    code = getattr(eklass, 'code', None)
    if code is not None:
        _HTTP_CODE_TO_EXCEPTION[code] = eklass
