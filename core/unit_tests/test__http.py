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


class TestConnection(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud._http import Connection

        return Connection

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_defaults(self):
        conn = self._make_one()
        self.assertIsNone(conn.credentials)

    def test_ctor_explicit(self):
        credentials = _Credentials()
        self.assertEqual(credentials._create_scoped_calls, 0)
        conn = self._make_one(credentials)
        self.assertEqual(credentials._create_scoped_calls, 1)
        self.assertIs(conn.credentials, credentials)
        self.assertIsNone(conn._http)

    def test_ctor_explicit_http(self):
        http = object()
        conn = self._make_one(http=http)
        self.assertIsNone(conn.credentials)
        self.assertIs(conn.http, http)

    def test_ctor_credentials_wo_create_scoped(self):
        credentials = object()
        conn = self._make_one(credentials)
        self.assertIs(conn.credentials, credentials)
        self.assertIsNone(conn._http)

    def test_http_w_existing(self):
        conn = self._make_one()
        conn._http = http = object()
        self.assertIs(conn.http, http)

    def test_http_wo_creds(self):
        import httplib2
        conn = self._make_one()
        self.assertIsInstance(conn.http, httplib2.Http)

    def test_http_w_creds(self):
        import httplib2

        authorized = object()
        credentials = _Credentials(authorized)
        conn = self._make_one(credentials)
        self.assertIs(conn.http, authorized)
        self.assertIsInstance(credentials._called_with, httplib2.Http)

    def test_user_agent_format(self):
        from pkg_resources import get_distribution
        expected_ua = 'gcloud-python/{0}'.format(
            get_distribution('google-cloud-core').version)
        conn = self._make_one()
        self.assertEqual(conn.USER_AGENT, expected_ua)

    def test__create_scoped_credentials_with_scoped_credentials(self):
        klass = self._get_target_class()
        scoped_creds = object()
        scope = 'google-specific-scope'
        credentials = _Credentials(scoped=scoped_creds)

        result = klass._create_scoped_credentials(credentials, scope)
        self.assertIs(result, scoped_creds)
        self.assertEqual(credentials._create_scoped_calls, 1)
        self.assertEqual(credentials._scopes, [scope])

    def test__create_scoped_credentials_without_scope_required(self):
        klass = self._get_target_class()
        credentials = _Credentials()

        result = klass._create_scoped_credentials(credentials, None)
        self.assertIs(result, credentials)
        self.assertEqual(credentials._create_scoped_calls, 1)
        self.assertEqual(credentials._scopes, [])

    def test__create_scoped_credentials_non_scoped_credentials(self):
        klass = self._get_target_class()
        credentials = object()
        result = klass._create_scoped_credentials(credentials, None)
        self.assertIs(result, credentials)

    def test__create_scoped_credentials_no_credentials(self):
        klass = self._get_target_class()
        result = klass._create_scoped_credentials(None, None)
        self.assertIsNone(result)


class TestJSONConnection(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud._http import JSONConnection

        return JSONConnection

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _makeMockOne(self, *args, **kw):
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

    def test_ctor_defaults(self):
        conn = self._make_one()
        self.assertIsNone(conn.credentials)

    def test_ctor_explicit(self):
        credentials = _Credentials()
        conn = self._make_one(credentials)
        self.assertIs(conn.credentials, credentials)

    def test_http_w_existing(self):
        conn = self._make_one()
        conn._http = http = object()
        self.assertIs(conn.http, http)

    def test_http_wo_creds(self):
        import httplib2
        conn = self._make_one()
        self.assertIsInstance(conn.http, httplib2.Http)

    def test_http_w_creds(self):
        import httplib2

        authorized = object()
        credentials = _Credentials(authorized)
        conn = self._make_one(credentials)
        self.assertIs(conn.http, authorized)
        self.assertIsInstance(credentials._called_with, httplib2.Http)

    def test_build_api_url_no_extra_query_params(self):
        conn = self._makeMockOne()
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
        conn = self._makeMockOne()
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
        conn = self._make_one()
        URI = 'http://example.com/test'
        http = conn._http = _Http(
            {'status': '200', 'content-type': 'text/plain'},
            b'',
        )
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
        conn = self._make_one()
        URI = 'http://example.com/test'
        http = conn._http = _Http(
            {'status': '200', 'content-type': 'text/plain'},
            b'',
        )
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
        conn = self._make_one()
        URI = 'http://example.com/test'
        http = conn._http = _Http(
            {'status': '200', 'content-type': 'text/plain'},
            b'',
        )
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
        PATH = '/path/required'
        conn = self._makeMockOne()
        # Intended to emulate self.mock_template
        URI = '/'.join([
            conn.API_BASE_URL,
            'mock',
            '%s%s' % (conn.API_VERSION, PATH),
        ])
        http = conn._http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            b'{}',
        )
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
        conn = self._makeMockOne()
        conn._http = _Http(
            {'status': '200', 'content-type': 'text/plain'},
            b'CONTENT',
        )

        self.assertRaises(TypeError, conn.api_request, 'GET', '/')

    def test_api_request_wo_json_expected(self):
        conn = self._makeMockOne()
        conn._http = _Http(
            {'status': '200', 'content-type': 'text/plain'},
            b'CONTENT',
        )
        self.assertEqual(conn.api_request('GET', '/', expect_json=False),
                         b'CONTENT')

    def test_api_request_w_query_params(self):
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit
        conn = self._makeMockOne()
        http = conn._http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            b'{}',
        )
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
        conn = self._makeMockOne()
        http = conn._http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            b'{}',
        )
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

    def test_api_request_w_data(self):
        import json
        DATA = {'foo': 'bar'}
        DATAJ = json.dumps(DATA)
        conn = self._makeMockOne()
        # Intended to emulate self.mock_template
        URI = '/'.join([
            conn.API_BASE_URL,
            'mock',
            conn.API_VERSION,
            '',
        ])
        http = conn._http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            b'{}',
        )
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
        conn = self._makeMockOne()
        conn._http = _Http(
            {'status': '404', 'content-type': 'text/plain'},
            b'{}'
        )
        self.assertRaises(NotFound, conn.api_request, 'GET', '/')

    def test_api_request_w_500(self):
        from google.cloud.exceptions import InternalServerError
        conn = self._makeMockOne()
        conn._http = _Http(
            {'status': '500', 'content-type': 'text/plain'},
            b'{}',
        )
        self.assertRaises(InternalServerError, conn.api_request, 'GET', '/')

    def test_api_request_non_binary_response(self):
        conn = self._makeMockOne()
        http = conn._http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            u'{}',
        )
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


class _Credentials(object):

    def __init__(self, authorized=None, scoped=None):
        self._authorized = authorized
        self._scoped = scoped
        self._scoped_required = scoped is not None
        self._create_scoped_calls = 0
        self._scopes = []

    def authorize(self, http):
        self._called_with = http
        return self._authorized

    def create_scoped_required(self):
        self._create_scoped_calls += 1
        return self._scoped_required

    def create_scoped(self, scope):
        self._scopes.append(scope)
        return self._scoped
