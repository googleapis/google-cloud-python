# Copyright 2014 Google LLC
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
"""Batch updates / deletes of storage buckets / blobs.

See https://cloud.google.com/storage/docs/json_api/v1/how-tos/batch
"""
from email.encoders import encode_noop
from email.generator import Generator
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.parser import Parser
import io
import json

import requests
import six

from google.cloud import _helpers
from google.cloud import exceptions
from google.cloud.storage._http import Connection


class MIMEApplicationHTTP(MIMEApplication):
    """MIME type for ``application/http``.

    Constructs payload from headers and body

    :type method: str
    :param method: HTTP method

    :type uri: str
    :param uri: URI for HTTP request

    :type headers:  dict
    :param headers: HTTP headers

    :type body: str
    :param body: (Optional) HTTP payload

    """

    def __init__(self, method, uri, headers, body):
        if isinstance(body, dict):
            body = json.dumps(body)
            headers["Content-Type"] = "application/json"
            headers["Content-Length"] = len(body)
        if body is None:
            body = ""
        lines = ["%s %s HTTP/1.1" % (method, uri)]
        lines.extend(
            ["%s: %s" % (key, value) for key, value in sorted(headers.items())]
        )
        lines.append("")
        lines.append(body)
        payload = "\r\n".join(lines)
        if six.PY2:
            # email.message.Message is an old-style class, so we
            # cannot use 'super()'.
            MIMEApplication.__init__(self, payload, "http", encode_noop)
        else:  # pragma: NO COVER  Python3
            super_init = super(MIMEApplicationHTTP, self).__init__
            super_init(payload, "http", encode_noop)


class _FutureDict(object):
    """Class to hold a future value for a deferred request.

    Used by for requests that get sent in a :class:`Batch`.
    """

    @staticmethod
    def get(key, default=None):
        """Stand-in for dict.get.

        :type key: object
        :param key: Hashable dictionary key.

        :type default: object
        :param default: Fallback value to dict.get.

        :raises: :class:`KeyError` always since the future is intended to fail
                 as a dictionary.
        """
        raise KeyError("Cannot get(%r, default=%r) on a future" % (key, default))

    def __getitem__(self, key):
        """Stand-in for dict[key].

        :type key: object
        :param key: Hashable dictionary key.

        :raises: :class:`KeyError` always since the future is intended to fail
                 as a dictionary.
        """
        raise KeyError("Cannot get item %r from a future" % (key,))

    def __setitem__(self, key, value):
        """Stand-in for dict[key] = value.

        :type key: object
        :param key: Hashable dictionary key.

        :type value: object
        :param value: Dictionary value.

        :raises: :class:`KeyError` always since the future is intended to fail
                 as a dictionary.
        """
        raise KeyError("Cannot set %r -> %r on a future" % (key, value))


class _FutureResponse(requests.Response):
    """Reponse that returns a placeholder dictionary for a batched requests."""

    def __init__(self, future_dict):
        super(_FutureResponse, self).__init__()
        self._future_dict = future_dict
        self.status_code = 204

    def json(self):
        return self._future_dict

    @property
    def content(self):
        return self._future_dict


class Batch(Connection):
    """Proxy an underlying connection, batching up change operations.

    :type client: :class:`google.cloud.storage.client.Client`
    :param client: The client to use for making connections.
    """

    _MAX_BATCH_SIZE = 1000

    def __init__(self, client):
        super(Batch, self).__init__(client)
        self._requests = []
        self._target_objects = []

    def _do_request(self, method, url, headers, data, target_object, timeout=None):
        """Override Connection:  defer actual HTTP request.

        Only allow up to ``_MAX_BATCH_SIZE`` requests to be deferred.

        :type method: str
        :param method: The HTTP method to use in the request.

        :type url: str
        :param url: The URL to send the request to.

        :type headers: dict
        :param headers: A dictionary of HTTP headers to send with the request.

        :type data: str
        :param data: The data to send as the body of the request.

        :type target_object: object
        :param target_object:
            (Optional) This allows us to enable custom behavior in our batch
            connection. Here we defer an HTTP request and complete
            initialization of the object at a later time.

        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response. By default, the method waits indefinitely.
            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :rtype: tuple of ``response`` (a dictionary of sorts)
                and ``content`` (a string).
        :returns: The HTTP response object and the content of the response.
        """
        if len(self._requests) >= self._MAX_BATCH_SIZE:
            raise ValueError(
                "Too many deferred requests (max %d)" % self._MAX_BATCH_SIZE
            )
        self._requests.append((method, url, headers, data, timeout))
        result = _FutureDict()
        self._target_objects.append(target_object)
        if target_object is not None:
            target_object._properties = result
        return _FutureResponse(result)

    def _prepare_batch_request(self):
        """Prepares headers and body for a batch request.

        :rtype: tuple (dict, str)
        :returns: The pair of headers and body of the batch request to be sent.
        :raises: :class:`ValueError` if no requests have been deferred.
        """
        if len(self._requests) == 0:
            raise ValueError("No deferred requests")

        multi = MIMEMultipart()

        # Use timeout of last request, default to None (indefinite)
        timeout = None
        for method, uri, headers, body, _timeout in self._requests:
            subrequest = MIMEApplicationHTTP(method, uri, headers, body)
            multi.attach(subrequest)
            timeout = _timeout

        # The `email` package expects to deal with "native" strings
        if six.PY3:  # pragma: NO COVER  Python3
            buf = io.StringIO()
        else:
            buf = io.BytesIO()
        generator = Generator(buf, False, 0)
        generator.flatten(multi)
        payload = buf.getvalue()

        # Strip off redundant header text
        _, body = payload.split("\n\n", 1)
        return dict(multi._headers), body, timeout

    def _finish_futures(self, responses):
        """Apply all the batch responses to the futures created.

        :type responses: list of (headers, payload) tuples.
        :param responses: List of headers and payloads from each response in
                          the batch.

        :raises: :class:`ValueError` if no requests have been deferred.
        """
        # If a bad status occurs, we track it, but don't raise an exception
        # until all futures have been populated.
        exception_args = None

        if len(self._target_objects) != len(responses):  # pragma: NO COVER
            raise ValueError("Expected a response for every request.")

        for target_object, subresponse in zip(self._target_objects, responses):
            if not 200 <= subresponse.status_code < 300:
                exception_args = exception_args or subresponse
            elif target_object is not None:
                try:
                    target_object._properties = subresponse.json()
                except ValueError:
                    target_object._properties = subresponse.content

        if exception_args is not None:
            raise exceptions.from_http_response(exception_args)

    def finish(self):
        """Submit a single `multipart/mixed` request with deferred requests.

        :rtype: list of tuples
        :returns: one ``(headers, payload)`` tuple per deferred request.
        """
        headers, body, timeout = self._prepare_batch_request()

        url = "%s/batch/storage/v1" % self.API_BASE_URL

        # Use the private ``_base_connection`` rather than the property
        # ``_connection``, since the property may be this
        # current batch.
        response = self._client._base_connection._make_request(
            "POST", url, data=body, headers=headers, timeout=timeout
        )
        responses = list(_unpack_batch_response(response))
        self._finish_futures(responses)
        return responses

    def current(self):
        """Return the topmost batch, or None."""
        return self._client.current_batch

    def __enter__(self):
        self._client._push_batch(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                self.finish()
        finally:
            self._client._pop_batch()


def _generate_faux_mime_message(parser, response):
    """Convert response, content -> (multipart) email.message.

    Helper for _unpack_batch_response.
    """
    # We coerce to bytes to get consistent concat across
    # Py2 and Py3. Percent formatting is insufficient since
    # it includes the b in Py3.
    content_type = _helpers._to_bytes(response.headers.get("content-type", ""))

    faux_message = b"".join(
        [b"Content-Type: ", content_type, b"\nMIME-Version: 1.0\n\n", response.content]
    )

    if six.PY2:
        return parser.parsestr(faux_message)
    else:  # pragma: NO COVER  Python3
        return parser.parsestr(faux_message.decode("utf-8"))


def _unpack_batch_response(response):
    """Convert requests.Response -> [(headers, payload)].

    Creates a generator of tuples of emulating the responses to
    :meth:`requests.Session.request`.

    :type response: :class:`requests.Response`
    :param response: HTTP response / headers from a request.
    """
    parser = Parser()
    message = _generate_faux_mime_message(parser, response)

    if not isinstance(message._payload, list):  # pragma: NO COVER
        raise ValueError("Bad response:  not multi-part")

    for subrequest in message._payload:
        status_line, rest = subrequest._payload.split("\n", 1)
        _, status, _ = status_line.split(" ", 2)
        sub_message = parser.parsestr(rest)
        payload = sub_message._payload
        msg_headers = dict(sub_message._headers)
        content_id = msg_headers.get("Content-ID")

        subresponse = requests.Response()
        subresponse.request = requests.Request(
            method="BATCH", url="contentid://{}".format(content_id)
        ).prepare()
        subresponse.status_code = int(status)
        subresponse.headers.update(msg_headers)
        subresponse._content = payload.encode("utf-8")

        yield subresponse
