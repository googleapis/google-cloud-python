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


class TestConnection(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.shiny.connection import Connection
        return Connection

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_build_api_url(self):
        connection = self._make_one()
        rel_path = 'foo'
        expected = '/'.join([
            connection.API_BASE_URL,
            connection.API_VERSION,
            rel_path,
        ])
        self.assertEqual(connection.build_api_url(rel_path), expected)

    def test_build_api_url_w_extra_query_params(self):
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit

        connection = self._make_one()
        rel_path = 'foo'
        query_param = 'bar'
        query_value = 'baz'
        built_url = connection.build_api_url(
            rel_path, {query_param: query_value})
        scheme, netloc, full_path, qs, _ = urlsplit(built_url)

        # Check base URL.
        expected_base = '{}://{}'.format(scheme, netloc)
        self.assertEqual(expected_base, connection.API_BASE_URL)
        # Check URL path.
        expected_path = '/{}/{}'.format(connection.API_VERSION, rel_path)
        self.assertEqual(full_path, expected_path)
        # Check query string.
        self.assertEqual(parse_qsl(qs), [('bar', 'baz')])
