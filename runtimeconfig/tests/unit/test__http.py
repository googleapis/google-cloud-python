# Copyright 2016 Google LLC
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
        from google.cloud.runtimeconfig._http import Connection

        return Connection

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_default_url(self):
        client = object()
        conn = self._make_one(client)
        self.assertIs(conn._client, client)

    def test_build_api_url_w_custom_endpoint(self):
        custom_endpoint = "https://foo-runtimeconfig.googleapis.com"
        conn = self._make_one(object(), api_endpoint=custom_endpoint)
        URI = "/".join([custom_endpoint, conn.API_VERSION, "foo"])
        self.assertEqual(conn.build_api_url("/foo"), URI)

    def test_extra_headers(self):
        import requests
        from google.cloud import _http as base_http

        http = mock.create_autospec(requests.Session, instance=True)
        response = requests.Response()
        response.status_code = 200
        data = b"brent-spiner"
        response._content = data
        http.request.return_value = response
        client = mock.Mock(_http=http, spec=["_http"])

        conn = self._make_one(client)
        req_data = "req-data-boring"
        result = conn.api_request("GET", "/rainbow", data=req_data, expect_json=False)
        self.assertEqual(result, data)

        expected_headers = {
            "Accept-Encoding": "gzip",
            base_http.CLIENT_INFO_HEADER: conn.user_agent,
            "User-Agent": conn.user_agent,
        }
        expected_uri = conn.build_api_url("/rainbow")
        http.request.assert_called_once_with(
            data=req_data, headers=expected_headers, method="GET", url=expected_uri
        )
