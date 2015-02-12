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
"""Batch updates / deletes of storage buckets / blobs.

See: https://cloud.google.com/storage/docs/json_api/v1/how-tos/batch
"""
from email.encoders import encode_noop
from email.generator import Generator
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.parser import Parser
import io
import json
import sys

import six

from gcloud._localstack import _LocalStack


_BATCHES = _LocalStack()

_PROXIED_ATTRS = [
    '_make_request',
    'api_request',
    'build_api_url',
    'get_all_buckets',
    'get_bucket',
    'create_bucket',
    'delete_bucket',
]


class MIMEApplicationHTTP(MIMEApplication):
    """MIME type for ``application/http``.

    Constructs payload from headers and body

    :type headers:  dict
    :param headers: HTTP headers

    :type body: text or None
    :param body: HTTP payload
    """
    def __init__(self, method, uri, headers, body):
        if isinstance(body, dict):
            body = json.dumps(body)
            headers['Content-Type'] = 'application/json'
            headers['Content-Length'] = len(body)
        if body is None:
            body = ''
        lines = ['%s %s HTTP/1.1' % (method, uri)]
        lines.extend(['%s: %s' % (key, value)
                      for key, value in sorted(headers.items())])
        lines.append('')
        lines.append(body)
        payload = '\r\n'.join(lines)
        if sys.version_info[0] < 3:  # pragma: NO COVER  Python2
            MIMEApplication.__init__(self, payload, 'http', encode_noop)
        else:                        # pragma: NO COVER  Python3
            super_init = super(MIMEApplicationHTTP, self).__init__
            super_init(payload, 'http', encode_noop)


class Batch(object):
    """Proxy an underlying connection, batching up change operations.

    :type connection: :class:`gcloud.storage.connection.Connection`
    :param connection: the connection for which the batch proxies.
    """
    def __init__(self, connection):
        self._connection = connection
        self._http = _FauxHTTP(connection)
        self._requests = self._responses = ()
        for attr in _PROXIED_ATTRS:
            setattr(self, attr, getattr(connection, attr))

    def finish(self):
        """Submit a single `multipart/mixed` request w/ deferred requests.

        :rtype: list of tuples
        :returns: one ``(status, reason, payload)`` tuple per deferred request.
        :raises: ValueError if no requests have been deferred.
        """
        deferred = self._requests = self._http.finalize()

        if len(deferred) == 0:
            raise ValueError("No deferred requests")

        multi = MIMEMultipart()

        for method, uri, headers, body in deferred:
            subrequest = MIMEApplicationHTTP(method, uri, headers, body)
            multi.attach(subrequest)

        # The `email` package expects to deal with "native" strings
        if six.PY3:             # pragma: NO COVER  Python3
            buf = io.StringIO()
        else:                   # pragma: NO COVER  Python2
            buf = io.BytesIO()
        generator = Generator(buf, False, 0)
        generator.flatten(multi)
        payload = buf.getvalue()

        # Strip off redundant header text
        _, body = payload.split('\n\n', 1)
        headers = dict(multi._headers)

        url = self._connection.build_api_url('/batch')

        _req = self._connection._make_request
        response, content = _req('POST', url, data=body, headers=headers)
        self._responses = list(_unpack_batch_response(response, content))
        return self._responses

    def __enter__(self):
        _BATCHES.push(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                self.finish()
            else:
                self._http.reset()
        finally:
            _BATCHES.pop()


def _unpack_batch_response(response, content):
    """Convert response, content -> [(status, reason, payload)]."""
    parser = Parser()
    faux_message = ('Content-Type: %s\nMIME-Version: 1.0\n\n%s' %
                    (response['Content-Type'], content))

    message = parser.parsestr(faux_message)

    if not isinstance(message._payload, list):
        raise ValueError('Bad response:  not multi-part')

    for subrequest in message._payload:
        status_line, rest = subrequest._payload.split('\n', 1)
        _, status, reason = status_line.split(' ', 2)
        message = parser.parsestr(rest)
        payload = message._payload
        ctype = message['Content-Type']
        if ctype and ctype.startswith('application/json'):
            payload = json.loads(payload)
        yield status, reason, payload


class NoContent(object):
    """Emulate an HTTP '204 No Content' response."""
    status = 204


class _FauxHTTP(object):
    """Emulate ``connection.http``, but store requests.

    Only allow up to ``_MAX_BATCH_SIZE`` requests to be bathed.
    """
    _MAX_BATCH_SIZE = 1000

    def __init__(self, connection):
        self._connection = connection
        self._requests = []
        self._orig_http, connection.http = connection.http, self

    def request(self, method, uri, headers, body):
        """Emulate / proxy underlying HTTP request.

        - Pass 'GET' requests through.

        - Defer others for later processing
        """
        if method == 'GET':
            _req = self._orig_http.request
            return _req(method=method, uri=uri, headers=headers, body=body)

        if len(self._requests) >= self._MAX_BATCH_SIZE:
            self.reset()
            raise ValueError("Too many deferred requests (max %d)" %
                             self._MAX_BATCH_SIZE)

        self._requests.append((method, uri, headers, body))
        return NoContent(), ''

    def reset(self):
        """Restore the connection's ``http``."""
        self._connection.http = self._orig_http

    def finalize(self):
        """Return the deferred requests.

        First restores the connection's ``http`` via ``reset()``.
        """
        self.reset()
        return self._requests
