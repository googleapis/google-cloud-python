# Copyright 2015 Google Inc. All rights reserved.
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


class TestConnection(unittest2.TestCase):
    PROJECT = 'PROJECT'
    LIST_TOPICS_PATH = 'projects/%s/topics' % (PROJECT,)
    TOPIC_NAME = 'topic_name'
    TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)

    def _getTargetClass(self):
        from gcloud.pubsub.connection import Connection
        return Connection

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_default_url(self):
        conn = self._makeOne()
        klass = self._getTargetClass()
        self.assertEqual(conn.api_base_url, klass.API_BASE_URL)

    def test_custom_url_from_env(self):
        import os
        from gcloud._testing import _Monkey
        from gcloud.environment_vars import PUBSUB_EMULATOR

        HOST = 'localhost:8187'
        fake_environ = {PUBSUB_EMULATOR: HOST}

        with _Monkey(os, getenv=fake_environ.get):
            conn = self._makeOne()

        klass = self._getTargetClass()
        self.assertNotEqual(conn.api_base_url, klass.API_BASE_URL)
        self.assertEqual(conn.api_base_url, 'http://' + HOST)

    def test_custom_url_from_constructor(self):
        HOST = object()
        conn = self._makeOne(api_base_url=HOST)

        klass = self._getTargetClass()
        self.assertNotEqual(conn.api_base_url, klass.API_BASE_URL)
        self.assertEqual(conn.api_base_url, HOST)

    def test_custom_url_constructor_and_env(self):
        import os
        from gcloud._testing import _Monkey
        from gcloud.environment_vars import PUBSUB_EMULATOR

        HOST1 = object()
        HOST2 = object()
        fake_environ = {PUBSUB_EMULATOR: HOST1}

        with _Monkey(os, getenv=fake_environ.get):
            conn = self._makeOne(api_base_url=HOST2)

        klass = self._getTargetClass()
        self.assertNotEqual(conn.api_base_url, klass.API_BASE_URL)
        self.assertNotEqual(conn.api_base_url, HOST1)
        self.assertEqual(conn.api_base_url, HOST2)

    def test_build_api_url_no_extra_query_params(self):
        conn = self._makeOne()
        URI = '/'.join([
            conn.API_BASE_URL,
            conn.API_VERSION,
            'foo',
        ])
        self.assertEqual(conn.build_api_url('/foo'), URI)

    def test_build_api_url_w_extra_query_params(self):
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit
        conn = self._makeOne()
        uri = conn.build_api_url('/foo', {'bar': 'baz'})
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual('%s://%s' % (scheme, netloc), conn.API_BASE_URL)
        self.assertEqual(path,
                         '/'.join(['', conn.API_VERSION, 'foo']))
        parms = dict(parse_qsl(qs))
        self.assertEqual(parms['bar'], 'baz')

    def test_build_api_url_w_base_url_override(self):
        base_url1 = 'api-base-url1'
        base_url2 = 'api-base-url2'
        conn = self._makeOne(api_base_url=base_url1)
        URI = '/'.join([
            base_url2,
            conn.API_VERSION,
            'foo',
        ])
        self.assertEqual(conn.build_api_url('/foo', api_base_url=base_url2),
                         URI)

    def _verify_uri(self, uri, expected_path, **expected_qs):
        from six.moves.urllib import parse
        klass = self._getTargetClass()
        scheme, netloc, path, query, _ = parse.urlsplit(uri)
        self.assertEqual('%s://%s' % (scheme, netloc), klass.API_BASE_URL)
        self.assertEqual(path, '/%s/%s' % (klass.API_VERSION, expected_path))
        qs = dict(parse.parse_qsl(query))
        self.assertEqual(qs, expected_qs)

    def test_list_topics_no_paging(self):
        import json
        RETURNED = {'topics': [{'name': self.TOPIC_PATH}]}
        HEADERS = {
            'status': '200',
            'content-type': 'application/json',
        }
        http = _Http(HEADERS, json.dumps(RETURNED))
        conn = self._makeOne(http=http)

        topics, next_token = conn.list_topics(self.PROJECT)

        self.assertEqual(len(topics), 1)
        topic = topics[0]
        self.assertTrue(isinstance(topic, dict))
        self.assertEqual(topic['name'], self.TOPIC_PATH)
        self.assertEqual(next_token, None)

        self.assertEqual(http._called_with['method'], 'GET')
        self._verify_uri(http._called_with['uri'], self.LIST_TOPICS_PATH)
        self.assertEqual(http._called_with['body'], None)

    def test_list_topics_with_paging(self):
        import json
        TOKEN1 = 'TOKEN1'
        TOKEN2 = 'TOKEN2'
        SIZE = 1
        RETURNED = {
            'topics': [{'name': self.TOPIC_PATH}],
            'nextPageToken': 'TOKEN2',
        }
        HEADERS = {
            'status': '200',
            'content-type': 'application/json',
        }
        http = _Http(HEADERS, json.dumps(RETURNED))
        conn = self._makeOne(http=http)

        topics, next_token = conn.list_topics(
            self.PROJECT, page_token=TOKEN1, page_size=SIZE)

        self.assertEqual(len(topics), 1)
        topic = topics[0]
        self.assertTrue(isinstance(topic, dict))
        self.assertEqual(topic['name'], self.TOPIC_PATH)
        self.assertEqual(next_token, TOKEN2)

        self.assertEqual(http._called_with['method'], 'GET')
        self._verify_uri(http._called_with['uri'], self.LIST_TOPICS_PATH,
                         pageToken=TOKEN1, pageSize=str(SIZE))
        self.assertEqual(http._called_with['body'], None)

    def test_list_topics_missing_key(self):
        import json
        RETURNED = {}
        HEADERS = {
            'status': '200',
            'content-type': 'application/json',
        }
        http = _Http(HEADERS, json.dumps(RETURNED))
        conn = self._makeOne(http=http)

        topics, next_token = conn.list_topics(self.PROJECT)

        self.assertEqual(len(topics), 0)
        self.assertEqual(next_token, None)

        self.assertEqual(http._called_with['method'], 'GET')
        self._verify_uri(http._called_with['uri'], self.LIST_TOPICS_PATH)
        self.assertEqual(http._called_with['body'], None)


class _Http(object):

    _called_with = None

    def __init__(self, headers, content):
        from httplib2 import Response
        self._response = Response(headers)
        self._content = content

    def request(self, **kw):
        self._called_with = kw
        return self._response, self._content
