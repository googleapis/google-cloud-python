# Copyright 2016 Google Inc.
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
        from google.cloud.monitoring._http import Connection

        return Connection

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor(self):
        client = object()
        connection = self._make_one(client)
        self.assertIs(connection._client, client)

    def test_extra_headers(self):
        from google.cloud import _http as base_http
        from google.cloud.monitoring import _http as MUT

        http = mock.Mock(spec=['request'])
        response = mock.Mock(status=200, spec=['status'])
        data = b'brent-spiner'
        http.request.return_value = response, data
        client = mock.Mock(_http=http, spec=['_http'])

        conn = self._make_one(client)
        req_data = 'req-data-boring'
        result = conn.api_request(
            'GET', '/rainbow', data=req_data, expect_json=False)
        self.assertEqual(result, data)

        expected_headers = {
            'Content-Length': str(len(req_data)),
            'Accept-Encoding': 'gzip',
            base_http.CLIENT_INFO_HEADER: MUT._CLIENT_INFO,
            'User-Agent': conn.USER_AGENT,
        }
        expected_uri = conn.build_api_url('/rainbow')
        http.request.assert_called_once_with(
            body=req_data,
            headers=expected_headers,
            method='GET',
            uri=expected_uri,
        )
