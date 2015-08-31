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

    def test_ctor(self):
        http = _HTTP()
        connection = _Connection(http=http)
        client = _Client(connection)
        batch = self._makeOne(client)
        self.assertTrue(batch._client is client)
        self.assertEqual(len(batch._requests), 0)
        self.assertEqual(len(batch._target_objects), 0)

    def test_current(self):
        from gcloud.storage.client import Client
        project = 'PROJECT'
        credentials = _Credentials()
        client = Client(project=project, credentials=credentials)
        batch1 = self._makeOne(client)
        self.assertTrue(batch1.current() is None)

        client._push_batch(batch1)
        self.assertTrue(batch1.current() is batch1)

        batch2 = self._makeOne(client)
        client._push_batch(batch2)
        self.assertTrue(batch1.current() is batch2)

    def test__make_request_GET_normal(self):
        from gcloud.storage.batch import _FutureDict
        URL = 'http://example.com/api'
        expected = _Response()
        http = _HTTP((expected, ''))
        connection = _Connection(http=http)
        batch = self._makeOne(connection)
        target = _MockObject()
        response, content = batch._make_request('GET', URL,
                                                target_object=target)
        self.assertEqual(response.status, 204)
        self.assertTrue(isinstance(content, _FutureDict))
        self.assertTrue(target._properties is content)
        self.assertEqual(http._requests, [])
        EXPECTED_HEADERS = [
            ('Accept-Encoding', 'gzip'),
            ('Content-Length', 0),
        ]
        solo_request, = batch._requests
        self.assertEqual(solo_request[0], 'GET')
        self.assertEqual(solo_request[1], URL)
        headers = solo_request[2]
        for key, value in EXPECTED_HEADERS:
            self.assertEqual(headers[key], value)
        self.assertEqual(solo_request[3], None)

    def test__make_request_POST_normal(self):
        from gcloud.storage.batch import _FutureDict
        URL = 'http://example.com/api'
        http = _HTTP()  # no requests expected
        connection = _Connection(http=http)
        batch = self._makeOne(connection)
        target = _MockObject()
        response, content = batch._make_request('POST', URL, data={'foo': 1},
                                                target_object=target)
        self.assertEqual(response.status, 204)
        self.assertTrue(isinstance(content, _FutureDict))
        self.assertTrue(target._properties is content)
        self.assertEqual(http._requests, [])
        EXPECTED_HEADERS = [
            ('Accept-Encoding', 'gzip'),
            ('Content-Length', 10),
        ]
        solo_request, = batch._requests
        self.assertEqual(solo_request[0], 'POST')
        self.assertEqual(solo_request[1], URL)
        headers = solo_request[2]
        for key, value in EXPECTED_HEADERS:
            self.assertEqual(headers[key], value)
        self.assertEqual(solo_request[3], {'foo': 1})

    def test__make_request_PATCH_normal(self):
        from gcloud.storage.batch import _FutureDict
        URL = 'http://example.com/api'
        http = _HTTP()  # no requests expected
        connection = _Connection(http=http)
        batch = self._makeOne(connection)
        target = _MockObject()
        response, content = batch._make_request('PATCH', URL, data={'foo': 1},
                                                target_object=target)
        self.assertEqual(response.status, 204)
        self.assertTrue(isinstance(content, _FutureDict))
        self.assertTrue(target._properties is content)
        self.assertEqual(http._requests, [])
        EXPECTED_HEADERS = [
            ('Accept-Encoding', 'gzip'),
            ('Content-Length', 10),
        ]
        solo_request, = batch._requests
        self.assertEqual(solo_request[0], 'PATCH')
        self.assertEqual(solo_request[1], URL)
        headers = solo_request[2]
        for key, value in EXPECTED_HEADERS:
            self.assertEqual(headers[key], value)
        self.assertEqual(solo_request[3], {'foo': 1})

    def test__make_request_DELETE_normal(self):
        from gcloud.storage.batch import _FutureDict
        URL = 'http://example.com/api'
        http = _HTTP()  # no requests expected
        connection = _Connection(http=http)
        batch = self._makeOne(connection)
        target = _MockObject()
        response, content = batch._make_request('DELETE', URL,
                                                target_object=target)
        self.assertEqual(response.status, 204)
        self.assertTrue(isinstance(content, _FutureDict))
        self.assertTrue(target._properties is content)
        self.assertEqual(http._requests, [])
        EXPECTED_HEADERS = [
            ('Accept-Encoding', 'gzip'),
            ('Content-Length', 0),
        ]
        solo_request, = batch._requests
        self.assertEqual(solo_request[0], 'DELETE')
        self.assertEqual(solo_request[1], URL)
        headers = solo_request[2]
        for key, value in EXPECTED_HEADERS:
            self.assertEqual(headers[key], value)
        self.assertEqual(solo_request[3], None)

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
        self.assertEqual(lines[0], '')
        self.assertEqual(lines[1], 'Content-Type: application/http')
        self.assertEqual(lines[2], 'MIME-Version: 1.0')
        self.assertEqual(lines[3], '')
        self.assertEqual(lines[4], '%s %s HTTP/1.1' % (method, url))
        if method == 'GET':
            self.assertEqual(len(lines), 7)
            self.assertEqual(lines[5], '')
            self.assertEqual(lines[6], '')
        else:
            self.assertEqual(len(lines), 9)
            self.assertEqual(lines[5], 'Content-Length: %d' % len(payload_str))
            self.assertEqual(lines[6], 'Content-Type: application/json')
            self.assertEqual(lines[7], '')
            self.assertEqual(json.loads(lines[8]), payload)

    def test_finish_nonempty(self):
        import httplib2
        URL = 'http://api.example.com/other_api'
        expected = _Response()
        expected['content-type'] = 'multipart/mixed; boundary="DEADBEEF="'
        http = _HTTP((expected, _THREE_PART_MIME_RESPONSE))
        connection = _Connection(http=http)
        client = _Client(connection)
        batch = self._makeOne(client)
        batch.API_BASE_URL = 'http://api.example.com'
        batch._do_request('POST', URL, {}, {'foo': 1, 'bar': 2}, None)
        batch._do_request('PATCH', URL, {}, {'bar': 3}, None)
        batch._do_request('DELETE', URL, {}, None, None)
        result = batch.finish()
        self.assertEqual(len(result), len(batch._requests))
        response0 = httplib2.Response({
            'content-length': '20',
            'content-type': 'application/json; charset=UTF-8',
            'status': '200',
        })
        self.assertEqual(result[0], (response0, {'foo': 1, 'bar': 2}))
        response1 = response0
        self.assertEqual(result[1], (response1, {u'foo': 1, u'bar': 3}))
        response2 = httplib2.Response({
            'content-length': '0',
            'status': '204',
        })
        self.assertEqual(result[2], (response2, ''))
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

    def test_finish_responses_mismatch(self):
        URL = 'http://api.example.com/other_api'
        expected = _Response()
        expected['content-type'] = 'multipart/mixed; boundary="DEADBEEF="'
        http = _HTTP((expected, _TWO_PART_MIME_RESPONSE_WITH_FAIL))
        connection = _Connection(http=http)
        client = _Client(connection)
        batch = self._makeOne(client)
        batch.API_BASE_URL = 'http://api.example.com'
        batch._requests.append(('GET', URL, {}, None))
        self.assertRaises(ValueError, batch.finish)

    def test_finish_nonempty_with_status_failure(self):
        from gcloud.exceptions import NotFound
        URL = 'http://api.example.com/other_api'
        expected = _Response()
        expected['content-type'] = 'multipart/mixed; boundary="DEADBEEF="'
        http = _HTTP((expected, _TWO_PART_MIME_RESPONSE_WITH_FAIL))
        connection = _Connection(http=http)
        client = _Client(connection)
        batch = self._makeOne(client)
        batch.API_BASE_URL = 'http://api.example.com'
        target1 = _MockObject()
        target2 = _MockObject()
        batch._do_request('GET', URL, {}, None, target1)
        batch._do_request('GET', URL, {}, None, target2)
        # Make sure futures are not populated.
        self.assertEqual([future for future in batch._target_objects],
                         [target1, target2])
        target2_future_before = target2._properties
        self.assertRaises(NotFound, batch.finish)
        self.assertEqual(target1._properties,
                         {'foo': 1, 'bar': 2})
        self.assertTrue(target2._properties is target2_future_before)

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
        self.assertEqual(len(chunks), 2)

        self._check_subrequest_payload(chunks[0], 'GET', URL, {})
        self._check_subrequest_payload(chunks[1], 'GET', URL, {})

    def test_finish_nonempty_non_multipart_response(self):
        URL = 'http://api.example.com/other_api'
        expected = _Response()
        expected['content-type'] = 'text/plain'
        http = _HTTP((expected, 'NOT A MIME_RESPONSE'))
        connection = _Connection(http=http)
        client = _Client(connection)
        batch = self._makeOne(client)
        batch._requests.append(('POST', URL, {}, {'foo': 1, 'bar': 2}))
        batch._requests.append(('PATCH', URL, {}, {'bar': 3}))
        batch._requests.append(('DELETE', URL, {}, None))
        self.assertRaises(ValueError, batch.finish)

    def test_as_context_mgr_wo_error(self):
        from gcloud.storage.client import Client
        URL = 'http://example.com/api'
        expected = _Response()
        expected['content-type'] = 'multipart/mixed; boundary="DEADBEEF="'
        http = _HTTP((expected, _THREE_PART_MIME_RESPONSE))
        project = 'PROJECT'
        credentials = _Credentials()
        client = Client(project=project, credentials=credentials)
        client._connection._http = http

        self.assertEqual(list(client._batch_stack), [])

        target1 = _MockObject()
        target2 = _MockObject()
        target3 = _MockObject()
        with self._makeOne(client) as batch:
            self.assertEqual(list(client._batch_stack), [batch])
            batch._make_request('POST', URL, {'foo': 1, 'bar': 2},
                                target_object=target1)
            batch._make_request('PATCH', URL, {'bar': 3},
                                target_object=target2)
            batch._make_request('DELETE', URL, target_object=target3)

        self.assertEqual(list(client._batch_stack), [])
        self.assertEqual(len(batch._requests), 3)
        self.assertEqual(batch._requests[0][0], 'POST')
        self.assertEqual(batch._requests[1][0], 'PATCH')
        self.assertEqual(batch._requests[2][0], 'DELETE')
        self.assertEqual(batch._target_objects, [target1, target2, target3])
        self.assertEqual(target1._properties,
                         {'foo': 1, 'bar': 2})
        self.assertEqual(target2._properties,
                         {'foo': 1, 'bar': 3})
        self.assertEqual(target3._properties, '')

    def test_as_context_mgr_w_error(self):
        from gcloud.storage.batch import _FutureDict
        from gcloud.storage.client import Client
        URL = 'http://example.com/api'
        http = _HTTP()
        connection = _Connection(http=http)
        project = 'PROJECT'
        credentials = _Credentials()
        client = Client(project=project, credentials=credentials)
        client._connection = connection

        self.assertEqual(list(client._batch_stack), [])

        target1 = _MockObject()
        target2 = _MockObject()
        target3 = _MockObject()
        try:
            with self._makeOne(client) as batch:
                self.assertEqual(list(client._batch_stack), [batch])
                batch._make_request('POST', URL, {'foo': 1, 'bar': 2},
                                    target_object=target1)
                batch._make_request('PATCH', URL, {'bar': 3},
                                    target_object=target2)
                batch._make_request('DELETE', URL, target_object=target3)
                raise ValueError()
        except ValueError:
            pass

        self.assertEqual(list(client._batch_stack), [])
        self.assertEqual(len(http._requests), 0)
        self.assertEqual(len(batch._requests), 3)
        self.assertEqual(batch._target_objects, [target1, target2, target3])
        # Since the context manager fails, finish will not get called and
        # the _properties will still be futures.
        self.assertTrue(isinstance(target1._properties, _FutureDict))
        self.assertTrue(isinstance(target2._properties, _FutureDict))
        self.assertTrue(isinstance(target3._properties, _FutureDict))


class Test__unpack_batch_response(unittest2.TestCase):

    def _callFUT(self, response, content):
        from gcloud.storage.batch import _unpack_batch_response
        return _unpack_batch_response(response, content)

    def _unpack_helper(self, response, content):
        import httplib2
        result = list(self._callFUT(response, content))
        self.assertEqual(len(result), 3)
        response0 = httplib2.Response({
            'content-length': '20',
            'content-type': 'application/json; charset=UTF-8',
            'status': '200',
        })
        self.assertEqual(result[0], (response0, {u'bar': 2, u'foo': 1}))
        response1 = response0
        self.assertEqual(result[1], (response1, {u'foo': 1, u'bar': 3}))
        response2 = httplib2.Response({
            'content-length': '0',
            'status': '204',
        })
        self.assertEqual(result[2], (response2, ''))

    def test_bytes(self):
        RESPONSE = {'content-type': b'multipart/mixed; boundary="DEADBEEF="'}
        CONTENT = _THREE_PART_MIME_RESPONSE
        self._unpack_helper(RESPONSE, CONTENT)

    def test_unicode(self):
        RESPONSE = {'content-type': u'multipart/mixed; boundary="DEADBEEF="'}
        CONTENT = _THREE_PART_MIME_RESPONSE.decode('utf-8')
        self._unpack_helper(RESPONSE, CONTENT)


_TWO_PART_MIME_RESPONSE_WITH_FAIL = b"""\
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

HTTP/1.1 404 Not Found
Content-Type: application/json; charset=UTF-8
Content-Length: 35

{"error": {"message": "Not Found"}}

--DEADBEEF=--
"""

_THREE_PART_MIME_RESPONSE = b"""\
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


class Test__FutureDict(unittest2.TestCase):

    def _makeOne(self, *args, **kw):
        from gcloud.storage.batch import _FutureDict
        return _FutureDict(*args, **kw)

    def test_get(self):
        future = self._makeOne()
        self.assertRaises(KeyError, future.get, None)

    def test___getitem__(self):
        future = self._makeOne()
        value = orig_value = object()
        with self.assertRaises(KeyError):
            value = future[None]
        self.assertTrue(value is orig_value)

    def test___setitem__(self):
        future = self._makeOne()
        with self.assertRaises(KeyError):
            future[None] = None


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

        return self.http.request(uri=url, method=method,
                                 headers=headers, body=data)

    def api_request(self, method, path, query_params=None,
                    data=None, content_type=None,
                    api_base_url=None, api_version=None,
                    expect_json=True):  # pragma: NO COVER
        pass


class _Response(dict):

    def __init__(self, status=200, **kw):
        self.status = status
        super(_Response, self).__init__(**kw)


class _HTTP(object):

    def __init__(self, *responses):
        self._requests = []
        self._responses = list(responses)

    def request(self, uri, method, headers, body):
        self._requests.append((method, uri, headers, body))
        response, self._responses = self._responses[0], self._responses[1:]
        return response


class _MockObject(object):
    pass


class _Client(object):

    def __init__(self, connection):
        self._connection = connection


class _Credentials(object):

    _scopes = None

    @staticmethod
    def create_scoped_required():
        return True

    def create_scoped(self, scope):
        self._scopes = scope
        return self
