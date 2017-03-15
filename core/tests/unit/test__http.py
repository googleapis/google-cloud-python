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

import unittest

import mock


class TestConnection(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud._http import Connection

        return Connection

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor(self):
        client = object()
        conn = self._make_one(client)
        self.assertIs(conn._client, client)

    def test_credentials_property(self):
        client = mock.Mock(spec=['_credentials'])
        conn = self._make_one(client)
        self.assertIs(conn.credentials, client._credentials)

    def test_http_property(self):
        client = mock.Mock(spec=['_http'])
        conn = self._make_one(client)
        self.assertIs(conn.http, client._http)

    def test_user_agent_format(self):
        from pkg_resources import get_distribution

        expected_ua = 'gcloud-python/{0}'.format(
            get_distribution('google-cloud-core').version)
        conn = self._make_one(object())
        self.assertEqual(conn.USER_AGENT, expected_ua)


class TestJSONConnection(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud._http import JSONConnection

        return JSONConnection

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _make_mock_one(self, *args, **kw):
        class MockConnection(self._get_target_class()):
            API_URL_TEMPLATE = '{api_base_url}/mock/{api_version}{path}'
            API_BASE_URL = 'http://mock'
            API_VERSION = 'vMOCK'
        return MockConnection(*args, **kw)

    def test_class_defaults(self):
        klass = self._get_target_class()
        self.assertIsNone(klass.API_URL_TEMPLATE)
        self.assertIsNone(klass.API_BASE_URL)
        self.assertIsNone(klass.API_VERSION)

    def test_constructor(self):
        client = object()
        conn = self._make_one(client)
        self.assertIs(conn._client, client)

    def test_build_api_url_no_extra_query_params(self):
        client = object()
        conn = self._make_mock_one(client)
        # Intended to emulate self.mock_template
        URI = '/'.join([
            conn.API_BASE_URL,
            'mock',
            conn.API_VERSION,
            'foo',
        ])
        self.assertEqual(conn.build_api_url('/foo'), URI)

    def test_build_api_url_w_extra_query_params(self):
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit

        client = object()
        conn = self._make_mock_one(client)
        uri = conn.build_api_url('/foo', {'bar': 'baz'})

        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual('%s://%s' % (scheme, netloc), conn.API_BASE_URL)
        # Intended to emulate mock_template
        PATH = '/'.join([
            '',
            'mock',
            conn.API_VERSION,
            'foo',
        ])
        self.assertEqual(path, PATH)
        parms = dict(parse_qsl(qs))
        self.assertEqual(parms['bar'], 'baz')

    def test__make_request_no_data_no_content_type_no_headers(self):
        http = _Http(
            {'status': '200', 'content-type': 'text/plain'},
            b'',
        )
        client = mock.Mock(_http=http, spec=['_http'])
        conn = self._make_one(client)
        URI = 'http://example.com/test'
        headers, content = conn._make_request('GET', URI)
        self.assertEqual(headers['status'], '200')
        self.assertEqual(headers['content-type'], 'text/plain')
        self.assertEqual(content, b'')
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertIsNone(http._called_with['body'])
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': '0',
            'User-Agent': conn.USER_AGENT,
        }
        self.assertEqual(http._called_with['headers'], expected_headers)

    def test__make_request_w_data_no_extra_headers(self):
        http = _Http(
            {'status': '200', 'content-type': 'text/plain'},
            b'',
        )
        client = mock.Mock(_http=http, spec=['_http'])
        conn = self._make_one(client)
        URI = 'http://example.com/test'
        conn._make_request('GET', URI, {}, 'application/json')
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertEqual(http._called_with['body'], {})
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': '0',
            'Content-Type': 'application/json',
            'User-Agent': conn.USER_AGENT,
        }
        self.assertEqual(http._called_with['headers'], expected_headers)

    def test__make_request_w_extra_headers(self):
        http = _Http(
            {'status': '200', 'content-type': 'text/plain'},
            b'',
        )
        client = mock.Mock(_http=http, spec=['_http'])
        conn = self._make_one(client)
        URI = 'http://example.com/test'
        conn._make_request('GET', URI, headers={'X-Foo': 'foo'})
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertIsNone(http._called_with['body'])
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': '0',
            'X-Foo': 'foo',
            'User-Agent': conn.USER_AGENT,
        }
        self.assertEqual(http._called_with['headers'], expected_headers)

    def test_api_request_defaults(self):
        http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            b'{}',
        )
        client = mock.Mock(_http=http, spec=['_http'])
        conn = self._make_mock_one(client)
        PATH = '/path/required'
        # Intended to emulate self.mock_template
        URI = '/'.join([
            conn.API_BASE_URL,
            'mock',
            '%s%s' % (conn.API_VERSION, PATH),
        ])
        self.assertEqual(conn.api_request('GET', PATH), {})
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertIsNone(http._called_with['body'])
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': '0',
            'User-Agent': conn.USER_AGENT,
        }
        self.assertEqual(http._called_with['headers'], expected_headers)

    def test_api_request_w_non_json_response(self):
        http = _Http(
            {'status': '200', 'content-type': 'text/plain'},
            b'CONTENT',
        )
        client = mock.Mock(_http=http, spec=['_http'])
        conn = self._make_mock_one(client)

        self.assertRaises(TypeError, conn.api_request, 'GET', '/')

    def test_api_request_wo_json_expected(self):
        http = _Http(
            {'status': '200', 'content-type': 'text/plain'},
            b'CONTENT',
        )
        client = mock.Mock(_http=http, spec=['_http'])
        conn = self._make_mock_one(client)
        self.assertEqual(conn.api_request('GET', '/', expect_json=False),
                         b'CONTENT')

    def test_api_request_w_query_params(self):
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit

        http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            b'{}',
        )
        client = mock.Mock(_http=http, spec=['_http'])
        conn = self._make_mock_one(client)
        self.assertEqual(conn.api_request('GET', '/', {'foo': 'bar'}), {})
        self.assertEqual(http._called_with['method'], 'GET')
        uri = http._called_with['uri']
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual('%s://%s' % (scheme, netloc), conn.API_BASE_URL)
        # Intended to emulate self.mock_template
        PATH = '/'.join([
            '',
            'mock',
            conn.API_VERSION,
            '',
        ])
        self.assertEqual(path, PATH)
        parms = dict(parse_qsl(qs))
        self.assertEqual(parms['foo'], 'bar')
        self.assertIsNone(http._called_with['body'])
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': '0',
            'User-Agent': conn.USER_AGENT,
        }
        self.assertEqual(http._called_with['headers'], expected_headers)

    def test_api_request_w_headers(self):
        from six.moves.urllib.parse import urlsplit

        http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            b'{}',
        )
        client = mock.Mock(_http=http, spec=['_http'])
        conn = self._make_mock_one(client)
        self.assertEqual(
            conn.api_request('GET', '/', headers={'X-Foo': 'bar'}), {})
        self.assertEqual(http._called_with['method'], 'GET')
        uri = http._called_with['uri']
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual('%s://%s' % (scheme, netloc), conn.API_BASE_URL)
        # Intended to emulate self.mock_template
        PATH = '/'.join([
            '',
            'mock',
            conn.API_VERSION,
            '',
        ])
        self.assertEqual(path, PATH)
        self.assertEqual(qs, '')
        self.assertIsNone(http._called_with['body'])
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': '0',
            'User-Agent': conn.USER_AGENT,
            'X-Foo': 'bar',
        }
        self.assertEqual(http._called_with['headers'], expected_headers)

    def test_api_request_w_extra_headers(self):
        from six.moves.urllib.parse import urlsplit

        http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            b'{}',
        )
        client = mock.Mock(_http=http, spec=['_http'])
        conn = self._make_mock_one(client)
        conn._EXTRA_HEADERS = {
            'X-Baz': 'dax-quux',
            'X-Foo': 'not-bar',  # Collision with ``headers``.
        }
        self.assertEqual(
            conn.api_request('GET', '/', headers={'X-Foo': 'bar'}), {})
        self.assertEqual(http._called_with['method'], 'GET')
        uri = http._called_with['uri']
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual('%s://%s' % (scheme, netloc), conn.API_BASE_URL)
        # Intended to emulate self.mock_template
        PATH = '/'.join([
            '',
            'mock',
            conn.API_VERSION,
            '',
        ])
        self.assertEqual(path, PATH)
        self.assertEqual(qs, '')
        self.assertIsNone(http._called_with['body'])
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': '0',
            'User-Agent': conn.USER_AGENT,
            'X-Foo': 'not-bar',  # The one passed-in is overridden.
            'X-Baz': 'dax-quux',
        }
        self.assertEqual(http._called_with['headers'], expected_headers)

    def test_api_request_w_data(self):
        import json

        DATA = {'foo': 'bar'}
        DATAJ = json.dumps(DATA)
        http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            b'{}',
        )
        client = mock.Mock(_http=http, spec=['_http'])
        conn = self._make_mock_one(client)
        # Intended to emulate self.mock_template
        URI = '/'.join([
            conn.API_BASE_URL,
            'mock',
            conn.API_VERSION,
            '',
        ])
        self.assertEqual(conn.api_request('POST', '/', data=DATA), {})
        self.assertEqual(http._called_with['method'], 'POST')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertEqual(http._called_with['body'], DATAJ)
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': str(len(DATAJ)),
            'Content-Type': 'application/json',
            'User-Agent': conn.USER_AGENT,
        }
        self.assertEqual(http._called_with['headers'], expected_headers)

    def test_api_request_w_404(self):
        from google.cloud.exceptions import NotFound

        http = _Http(
            {'status': '404', 'content-type': 'text/plain'},
            b'{}'
        )
        client = mock.Mock(_http=http, spec=['_http'])
        conn = self._make_mock_one(client)
        self.assertRaises(NotFound, conn.api_request, 'GET', '/')

    def test_api_request_w_500(self):
        from google.cloud.exceptions import InternalServerError

        http = _Http(
            {'status': '500', 'content-type': 'text/plain'},
            b'{}',
        )
        client = mock.Mock(_http=http, spec=['_http'])
        conn = self._make_mock_one(client)
        self.assertRaises(InternalServerError, conn.api_request, 'GET', '/')

    def test_api_request_non_binary_response(self):
        http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            u'{}',
        )
        client = mock.Mock(_http=http, spec=['_http'])
        conn = self._make_mock_one(client)

        result = conn.api_request('GET', '/')
        # Intended to emulate self.mock_template
        URI = '/'.join([
            conn.API_BASE_URL,
            'mock',
            conn.API_VERSION,
            '',
        ])
        self.assertEqual(result, {})
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertIsNone(http._called_with['body'])
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': '0',
            'User-Agent': conn.USER_AGENT,
        }
        self.assertEqual(http._called_with['headers'], expected_headers)


class _Http(object):

    _called_with = None

    def __init__(self, headers, content):
        from httplib2 import Response

        self._response = Response(headers)
        self._content = content

    def request(self, **kw):
        self._called_with = kw
        return self._response, self._content
