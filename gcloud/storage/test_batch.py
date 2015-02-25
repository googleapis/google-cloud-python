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

import unittest2


class TestMIMEApplicationHTTP(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.batch import MIMEApplicationHTTP
        return MIMEApplicationHTTP

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_body_None(self):
        METHOD = 'DELETE'
        PATH = '/path/to/api'
        LINES = [
            "DELETE /path/to/api HTTP/1.1",
            "",
            ]
        mah = self._makeOne(METHOD, PATH, {}, None)
        self.assertEqual(mah.get_content_type(), 'application/http')
        self.assertEqual(mah.get_payload().splitlines(), LINES)

    def test_ctor_body_str(self):
        METHOD = 'GET'
        PATH = '/path/to/api'
        BODY = 'ABC'
        HEADERS = {'Content-Length': len(BODY), 'Content-Type': 'text/plain'}
        LINES = [
            "GET /path/to/api HTTP/1.1",
            "Content-Length: 3",
            "Content-Type: text/plain",
            "",
            "ABC",
            ]
        mah = self._makeOne(METHOD, PATH, HEADERS, BODY)
        self.assertEqual(mah.get_payload().splitlines(), LINES)

    def test_ctor_body_dict(self):
        METHOD = 'GET'
        PATH = '/path/to/api'
        BODY = {'foo': 'bar'}
        HEADERS = {}
        LINES = [
            'GET /path/to/api HTTP/1.1',
            'Content-Length: 14',
            'Content-Type: application/json',
            '',
            '{"foo": "bar"}',
            ]
        mah = self._makeOne(METHOD, PATH, HEADERS, BODY)
        self.assertEqual(mah.get_payload().splitlines(), LINES)


class TestBatch(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.batch import Batch
        return Batch

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_w_explicit_connection(self):
        http = _HTTP()
        connection = _Connection(http=http)
        batch = self._makeOne(connection)
        self.assertTrue(batch._connection is connection)
        self.assertEqual(batch.project, connection.project)
        self.assertEqual(len(batch._requests), 0)
        self.assertEqual(len(batch._responses), 0)

    def test__make_request_GET_forwarded_to_connection(self):
        URL = 'http://example.com/api'
        expected = _Response()
        http = _HTTP((expected, ''))
        connection = _Connection(http=http)
        batch = self._makeOne(connection)
        response, content = batch._make_request('GET', URL)
        self.assertTrue(response is expected)
        self.assertEqual(content, '')
        EXPECTED_HEADERS = [
            ('Accept-Encoding', 'gzip'),
            ('Content-Length', 0),
        ]
        self.assertEqual(len(http._requests), 1)
        self.assertEqual(http._requests[0][0], 'GET')
        self.assertEqual(http._requests[0][1], URL)
        headers = http._requests[0][2]
        for key, value in EXPECTED_HEADERS:
            self.assertEqual(headers[key], value)
        self.assertEqual(http._requests[0][3], None)
        self.assertEqual(batch._requests, [])

    def test__make_request_POST_normal(self):
        URL = 'http://example.com/api'
        http = _HTTP()  # no requests expected
        connection = _Connection(http=http)
        batch = self._makeOne(connection)
        response, content = batch._make_request('POST', URL, data={'foo': 1})
        self.assertEqual(response.status, 204)
        self.assertEqual(content, '')
        self.assertEqual(http._requests, [])
        EXPECTED_HEADERS = [
            ('Accept-Encoding', 'gzip'),
            ('Content-Length', 10),
        ]
        self.assertEqual(len(batch._requests), 1)
        self.assertEqual(batch._requests[0][0], 'POST')
        self.assertEqual(batch._requests[0][1], URL)
        headers = batch._requests[0][2]
        for key, value in EXPECTED_HEADERS:
            self.assertEqual(headers[key], value)
        self.assertEqual(batch._requests[0][3], {'foo': 1})

    def test__make_request_PATCH_normal(self):
        URL = 'http://example.com/api'
        http = _HTTP()  # no requests expected
        connection = _Connection(http=http)
        batch = self._makeOne(connection)
        response, content = batch._make_request('PATCH', URL, data={'foo': 1})
        self.assertEqual(response.status, 204)
        self.assertEqual(content, '')
        self.assertEqual(http._requests, [])
        EXPECTED_HEADERS = [
            ('Accept-Encoding', 'gzip'),
            ('Content-Length', 10),
        ]
        self.assertEqual(len(batch._requests), 1)
        self.assertEqual(batch._requests[0][0], 'PATCH')
        self.assertEqual(batch._requests[0][1], URL)
        headers = batch._requests[0][2]
        for key, value in EXPECTED_HEADERS:
            self.assertEqual(headers[key], value)
        self.assertEqual(batch._requests[0][3], {'foo': 1})

    def test__make_request_DELETE_normal(self):
        URL = 'http://example.com/api'
        http = _HTTP()  # no requests expected
        connection = _Connection(http=http)
        batch = self._makeOne(connection)
        response, content = batch._make_request('DELETE', URL)
        self.assertEqual(response.status, 204)
        self.assertEqual(content, '')
        self.assertEqual(http._requests, [])
        EXPECTED_HEADERS = [
            ('Accept-Encoding', 'gzip'),
            ('Content-Length', 0),
        ]
        self.assertEqual(len(batch._requests), 1)
        self.assertEqual(batch._requests[0][0], 'DELETE')
        self.assertEqual(batch._requests[0][1], URL)
        headers = batch._requests[0][2]
        for key, value in EXPECTED_HEADERS:
            self.assertEqual(headers[key], value)
        self.assertEqual(batch._requests[0][3], None)

    def test__make_request_POST_too_many_requests(self):
        URL = 'http://example.com/api'
        http = _HTTP()  # no requests expected
        connection = _Connection(http=http)
        batch = self._makeOne(connection)
        batch._MAX_BATCH_SIZE = 1
        batch._requests.append(('POST', URL, {}, {'bar': 2}))
        self.assertRaises(ValueError,
                          batch._make_request, 'POST', URL, data={'foo': 1})
        self.assertTrue(connection.http is http)

    def test_finish_empty(self):
        http = _HTTP()  # no requests expected
        connection = _Connection(http=http)
        batch = self._makeOne(connection)
        self.assertRaises(ValueError, batch.finish)
        self.assertTrue(connection.http is http)

    def _check_subrequest_no_payload(self, chunk, method, url):
        lines = chunk.splitlines()
        # blank + 2 headers + blank + request + blank + blank
        self.assertEqual(len(lines), 7)
        self.assertEqual(lines[0], '')
        self.assertEqual(lines[1], 'Content-Type: application/http')
        self.assertEqual(lines[2], 'MIME-Version: 1.0')
        self.assertEqual(lines[3], '')
        self.assertEqual(lines[4], '%s %s HTTP/1.1' % (method, url))
        self.assertEqual(lines[5], '')
        self.assertEqual(lines[6], '')

    def _check_subrequest_payload(self, chunk, method, url, payload):
        import json
        lines = chunk.splitlines()
        # blank + 2 headers + blank + request + 2 headers + blank + body
        payload_str = json.dumps(payload)
        self.assertEqual(len(lines), 9)
        self.assertEqual(lines[0], '')
        self.assertEqual(lines[1], 'Content-Type: application/http')
        self.assertEqual(lines[2], 'MIME-Version: 1.0')
        self.assertEqual(lines[3], '')
        self.assertEqual(lines[4], '%s %s HTTP/1.1' % (method, url))
        self.assertEqual(lines[5], 'Content-Length: %d' % len(payload_str))
        self.assertEqual(lines[6], 'Content-Type: application/json')
        self.assertEqual(lines[7], '')
        self.assertEqual(json.loads(lines[8]), payload)

    def test_finish_nonempty(self):
        URL = 'http://api.example.com/other_api'
        expected = _Response()
        expected['Content-Type'] = 'multipart/mixed; boundary="DEADBEEF="'
        http = _HTTP((expected, _THREE_PART_MIME_RESPONSE))
        connection = _Connection(http=http)
        batch = self._makeOne(connection)
        batch._requests.append(('POST', URL, {}, {'foo': 1, 'bar': 2}))
        batch._requests.append(('PATCH', URL, {}, {'bar': 3}))
        batch._requests.append(('DELETE', URL, {}, None))
        result = batch.finish()
        self.assertEqual(len(result), len(batch._requests))
        self.assertEqual(result[0][0], '200')
        self.assertEqual(result[0][1], 'OK')
        self.assertEqual(result[0][2], {'foo': 1, 'bar': 2})
        self.assertEqual(result[1][0], '200')
        self.assertEqual(result[1][1], 'OK')
        self.assertEqual(result[1][2], {'foo': 1, 'bar': 3})
        self.assertEqual(result[2][0], '204')
        self.assertEqual(result[2][1], 'No Content')
        self.assertEqual(result[2][2], '')
        self.assertEqual(len(http._requests), 1)
        method, uri, headers, body = http._requests[0]
        self.assertEqual(method, 'POST')
        self.assertEqual(uri, 'http://api.example.com/batch')
        self.assertEqual(len(headers), 2)
        ctype, boundary = [x.strip()
                           for x in headers['Content-Type'].split(';')]
        self.assertEqual(ctype, 'multipart/mixed')
        self.assertTrue(boundary.startswith('boundary="=='))
        self.assertTrue(boundary.endswith('=="'))
        self.assertEqual(headers['MIME-Version'], '1.0')

        divider = '--' + boundary[len('boundary="'):-1]
        chunks = body.split(divider)[1:-1]  # discard prolog / epilog
        self.assertEqual(len(chunks), 3)

        self._check_subrequest_payload(chunks[0], 'POST', URL,
                                       {'foo': 1, 'bar': 2})

        self._check_subrequest_payload(chunks[1], 'PATCH', URL, {'bar': 3})

        self._check_subrequest_no_payload(chunks[2], 'DELETE', URL)

    def test_finish_nonempty_non_multipart_response(self):
        URL = 'http://api.example.com/other_api'
        expected = _Response()
        expected['Content-Type'] = 'text/plain'
        http = _HTTP((expected, 'NOT A MIME_RESPONSE'))
        connection = _Connection(http=http)
        batch = self._makeOne(connection)
        batch._requests.append(('POST', URL, {}, {'foo': 1, 'bar': 2}))
        batch._requests.append(('PATCH', URL, {}, {'bar': 3}))
        batch._requests.append(('DELETE', URL, {}, None))
        self.assertRaises(ValueError, batch.finish)

    def test_as_context_mgr_wo_error(self):
        from gcloud.storage.batch import _BATCHES
        URL = 'http://example.com/api'
        expected = _Response()
        expected['Content-Type'] = 'multipart/mixed; boundary="DEADBEEF="'
        http = _HTTP((expected, _THREE_PART_MIME_RESPONSE))
        connection = _Connection(http=http)

        self.assertEqual(list(_BATCHES), [])

        with self._makeOne(connection) as batch:
            self.assertEqual(list(_BATCHES), [batch])
            batch._make_request('POST', URL, {'foo': 1, 'bar': 2})
            batch._make_request('PATCH', URL, {'bar': 3})
            batch._make_request('DELETE', URL)

        self.assertEqual(list(_BATCHES), [])
        self.assertEqual(len(batch._requests), 3)
        self.assertEqual(batch._requests[0][0], 'POST')
        self.assertEqual(batch._requests[1][0], 'PATCH')
        self.assertEqual(batch._requests[2][0], 'DELETE')
        self.assertEqual(len(batch._responses), 3)
        self.assertEqual(
            batch._responses[0],
            ('200', 'OK', {'foo': 1, 'bar': 2}))
        self.assertEqual(
            batch._responses[1],
            ('200', 'OK', {'foo': 1, 'bar': 3}))
        self.assertEqual(
            batch._responses[2],
            ('204', 'No Content', ''))

    def test_as_context_mgr_w_error(self):
        from gcloud.storage.batch import _BATCHES
        URL = 'http://example.com/api'
        http = _HTTP()
        connection = _Connection(http=http)

        self.assertEqual(list(_BATCHES), [])

        try:
            with self._makeOne(connection) as batch:
                self.assertEqual(list(_BATCHES), [batch])
                batch._make_request('POST', URL, {'foo': 1, 'bar': 2})
                batch._make_request('PATCH', URL, {'bar': 3})
                batch._make_request('DELETE', URL)
                raise ValueError()
        except ValueError:
            pass

        self.assertEqual(list(_BATCHES), [])
        self.assertEqual(len(http._requests), 0)
        self.assertEqual(len(batch._requests), 3)
        self.assertEqual(len(batch._responses), 0)


_THREE_PART_MIME_RESPONSE = """\
--DEADBEEF=
Content-Type: application/http
Content-ID: <response-8a09ca85-8d1d-4f45-9eb0-da8e8b07ec83+1>

HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Content-Length: 20

{"foo": 1, "bar": 2}

--DEADBEEF=
Content-Type: application/http
Content-ID: <response-8a09ca85-8d1d-4f45-9eb0-da8e8b07ec83+2>

HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Content-Length: 20

{"foo": 1, "bar": 3}

--DEADBEEF=
Content-Type: application/http
Content-ID: <response-8a09ca85-8d1d-4f45-9eb0-da8e8b07ec83+3>

HTTP/1.1 204 No Content
Content-Length: 0

--DEADBEEF=--
"""


class _Connection(object):

    project = 'TESTING'

    def __init__(self, **kw):
        self.__dict__.update(kw)

    def build_api_url(self, path, **_):  # pragma: NO COVER
        return 'http://api.example.com%s' % path

    def _make_request(self, method, url, data=None, content_type=None,
                      headers=None):
        if content_type is not None:  # pragma: NO COVER
            headers['Content-Type'] = content_type

        return self.http.request(method, uri=url, headers=headers, body=data)

    def api_request(self, method, path, query_params=None,
                    data=None, content_type=None,
                    api_base_url=None, api_version=None,
                    expect_json=True):  # pragma: NO COVER
        pass

    def get_all_buckets(self):  # pragma: NO COVER
        pass

    def get_bucket(self, name):  # pragma: NO COVER
        pass

    def create_bucket(self, name):  # pragma: NO COVER
        pass

    def delete_bucket(self, name):  # pragma: NO COVER
        pass


class _Response(dict):

    def __init__(self, status=200, **kw):
        self.status = status
        super(_Response, self).__init__(**kw)


class _HTTP(object):

    def __init__(self, *responses):
        self._requests = []
        self._responses = list(responses)

    def request(self, method, uri, headers, body):
        self._requests.append((method, uri, headers, body))
        response, self._responses = self._responses[0], self._responses[1:]
        return response
