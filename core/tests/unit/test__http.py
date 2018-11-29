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

import json
import unittest

import mock
import requests
from six.moves import http_client


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
        client = mock.Mock(spec=["_credentials"])
        conn = self._make_one(client)
        self.assertIs(conn.credentials, client._credentials)

    def test_http_property(self):
        client = mock.Mock(spec=["_http"])
        conn = self._make_one(client)
        self.assertIs(conn.http, client._http)

    def test_user_agent_format(self):
        from pkg_resources import get_distribution

        expected_ua = "gcloud-python/{0}".format(
            get_distribution("google-cloud-core").version
        )
        conn = self._make_one(object())
        self.assertEqual(conn.USER_AGENT, expected_ua)


def make_response(status=http_client.OK, content=b"", headers={}):
    response = requests.Response()
    response.status_code = status
    response._content = content
    response.headers = headers
    response.request = requests.Request()
    return response


def make_requests_session(responses):
    session = mock.create_autospec(requests.Session, instance=True)
    session.request.side_effect = responses
    return session


class TestJSONConnection(unittest.TestCase):
    JSON_HEADERS = {"content-type": "application/json"}
    EMPTY_JSON_RESPONSE = make_response(content=b"{}", headers=JSON_HEADERS)

    @staticmethod
    def _get_target_class():
        from google.cloud._http import JSONConnection

        return JSONConnection

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _make_mock_one(self, *args, **kw):
        class MockConnection(self._get_target_class()):
            API_URL_TEMPLATE = "{api_base_url}/mock/{api_version}{path}"
            API_BASE_URL = "http://mock"
            API_VERSION = "vMOCK"

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
        URI = "/".join([conn.API_BASE_URL, "mock", conn.API_VERSION, "foo"])
        self.assertEqual(conn.build_api_url("/foo"), URI)

    def test_build_api_url_w_extra_query_params(self):
        from six.moves.urllib.parse import parse_qs
        from six.moves.urllib.parse import urlsplit

        client = object()
        conn = self._make_mock_one(client)
        uri = conn.build_api_url("/foo", {"bar": "baz", "qux": ["quux", "corge"]})

        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual("%s://%s" % (scheme, netloc), conn.API_BASE_URL)
        # Intended to emulate mock_template
        PATH = "/".join(["", "mock", conn.API_VERSION, "foo"])
        self.assertEqual(path, PATH)
        parms = dict(parse_qs(qs))
        self.assertEqual(parms["bar"], ["baz"])
        self.assertEqual(parms["qux"], ["quux", "corge"])

    def test__make_request_no_data_no_content_type_no_headers(self):
        http = make_requests_session([make_response()])
        client = mock.Mock(_http=http, spec=["_http"])
        conn = self._make_one(client)
        url = "http://example.com/test"

        response = conn._make_request("GET", url)

        self.assertEqual(response.status_code, http_client.OK)
        self.assertEqual(response.content, b"")

        expected_headers = {"Accept-Encoding": "gzip", "User-Agent": conn.USER_AGENT}
        http.request.assert_called_once_with(
            method="GET", url=url, headers=expected_headers, data=None
        )

    def test__make_request_w_data_no_extra_headers(self):
        http = make_requests_session([make_response()])
        client = mock.Mock(_http=http, spec=["_http"])
        conn = self._make_one(client)
        url = "http://example.com/test"
        data = b"data"

        conn._make_request("GET", url, data, "application/json")

        expected_headers = {
            "Accept-Encoding": "gzip",
            "Content-Type": "application/json",
            "User-Agent": conn.USER_AGENT,
        }
        http.request.assert_called_once_with(
            method="GET", url=url, headers=expected_headers, data=data
        )

    def test__make_request_w_extra_headers(self):
        http = make_requests_session([make_response()])
        client = mock.Mock(_http=http, spec=["_http"])
        conn = self._make_one(client)

        url = "http://example.com/test"
        conn._make_request("GET", url, headers={"X-Foo": "foo"})

        expected_headers = {
            "Accept-Encoding": "gzip",
            "X-Foo": "foo",
            "User-Agent": conn.USER_AGENT,
        }
        http.request.assert_called_once_with(
            method="GET", url=url, headers=expected_headers, data=None
        )

    def test_api_request_defaults(self):
        http = make_requests_session(
            [make_response(content=b"{}", headers=self.JSON_HEADERS)]
        )
        client = mock.Mock(_http=http, spec=["_http"])
        conn = self._make_mock_one(client)
        path = "/path/required"

        self.assertEqual(conn.api_request("GET", path), {})

        expected_headers = {"Accept-Encoding": "gzip", "User-Agent": conn.USER_AGENT}
        expected_url = "{base}/mock/{version}{path}".format(
            base=conn.API_BASE_URL, version=conn.API_VERSION, path=path
        )
        http.request.assert_called_once_with(
            method="GET", url=expected_url, headers=expected_headers, data=None
        )

    def test_api_request_w_non_json_response(self):
        http = make_requests_session([make_response(content=b"content")])
        client = mock.Mock(_http=http, spec=["_http"])
        conn = self._make_mock_one(client)

        with self.assertRaises(ValueError):
            conn.api_request("GET", "/")

    def test_api_request_wo_json_expected(self):
        http = make_requests_session([make_response(content=b"content")])
        client = mock.Mock(_http=http, spec=["_http"])
        conn = self._make_mock_one(client)

        result = conn.api_request("GET", "/", expect_json=False)

        self.assertEqual(result, b"content")

    def test_api_request_w_query_params(self):
        from six.moves.urllib.parse import parse_qs
        from six.moves.urllib.parse import urlsplit

        http = make_requests_session([self.EMPTY_JSON_RESPONSE])
        client = mock.Mock(_http=http, spec=["_http"])
        conn = self._make_mock_one(client)

        result = conn.api_request("GET", "/", {"foo": "bar", "baz": ["qux", "quux"]})

        self.assertEqual(result, {})

        expected_headers = {"Accept-Encoding": "gzip", "User-Agent": conn.USER_AGENT}
        http.request.assert_called_once_with(
            method="GET", url=mock.ANY, headers=expected_headers, data=None
        )

        url = http.request.call_args[1]["url"]
        scheme, netloc, path, qs, _ = urlsplit(url)
        self.assertEqual("%s://%s" % (scheme, netloc), conn.API_BASE_URL)
        # Intended to emulate self.mock_template
        PATH = "/".join(["", "mock", conn.API_VERSION, ""])
        self.assertEqual(path, PATH)
        parms = dict(parse_qs(qs))
        self.assertEqual(parms["foo"], ["bar"])
        self.assertEqual(parms["baz"], ["qux", "quux"])

    def test_api_request_w_headers(self):
        http = make_requests_session([self.EMPTY_JSON_RESPONSE])
        client = mock.Mock(_http=http, spec=["_http"])
        conn = self._make_mock_one(client)

        result = conn.api_request("GET", "/", headers={"X-Foo": "bar"})
        self.assertEqual(result, {})

        expected_headers = {
            "Accept-Encoding": "gzip",
            "User-Agent": conn.USER_AGENT,
            "X-Foo": "bar",
        }
        http.request.assert_called_once_with(
            method="GET", url=mock.ANY, headers=expected_headers, data=None
        )

    def test_api_request_w_extra_headers(self):
        http = make_requests_session([self.EMPTY_JSON_RESPONSE])
        client = mock.Mock(_http=http, spec=["_http"])
        conn = self._make_mock_one(client)
        conn._EXTRA_HEADERS = {
            "X-Baz": "dax-quux",
            "X-Foo": "not-bar",  # Collision with ``headers``.
        }

        result = conn.api_request("GET", "/", headers={"X-Foo": "bar"})

        self.assertEqual(result, {})

        expected_headers = {
            "Accept-Encoding": "gzip",
            "User-Agent": conn.USER_AGENT,
            "X-Foo": "not-bar",  # The one passed-in is overridden.
            "X-Baz": "dax-quux",
        }
        http.request.assert_called_once_with(
            method="GET", url=mock.ANY, headers=expected_headers, data=None
        )

    def test_api_request_w_data(self):
        http = make_requests_session([self.EMPTY_JSON_RESPONSE])
        client = mock.Mock(_http=http, spec=["_http"])
        conn = self._make_mock_one(client)

        data = {"foo": "bar"}
        self.assertEqual(conn.api_request("POST", "/", data=data), {})

        expected_data = json.dumps(data)

        expected_headers = {
            "Accept-Encoding": "gzip",
            "Content-Type": "application/json",
            "User-Agent": conn.USER_AGENT,
        }

        http.request.assert_called_once_with(
            method="POST", url=mock.ANY, headers=expected_headers, data=expected_data
        )

    def test_api_request_w_404(self):
        from google.cloud import exceptions

        http = make_requests_session([make_response(http_client.NOT_FOUND)])
        client = mock.Mock(_http=http, spec=["_http"])
        conn = self._make_mock_one(client)

        with self.assertRaises(exceptions.NotFound):
            conn.api_request("GET", "/")

    def test_api_request_w_500(self):
        from google.cloud import exceptions

        http = make_requests_session([make_response(http_client.INTERNAL_SERVER_ERROR)])
        client = mock.Mock(_http=http, spec=["_http"])
        conn = self._make_mock_one(client)

        with self.assertRaises(exceptions.InternalServerError):
            conn.api_request("GET", "/")
