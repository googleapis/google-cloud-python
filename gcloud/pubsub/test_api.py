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


class Test_list_topics(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud.pubsub.api import list_topics
        return list_topics(*args, **kw)

    def test_w_explicit_connection_no_paging(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        TOKEN = 'TOKEN'
        returned = {'topics': [{'name': TOPIC_NAME}],
                    'nextPageToken': TOKEN}
        conn = _Connection(returned)
        response = self._callFUT(PROJECT, conn)
        topics = response['topics']
        self.assertEqual(len(topics), 1)
        self.assertEqual(topics[0], {'name': TOPIC_NAME})
        self.assertEqual(response['nextPageToken'], TOKEN)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/topics' % PROJECT)
        self.assertEqual(req.get('query_params'), None)

    def test_w_explicit_connection_w_paging(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        TOKEN1 = 'TOKEN1'
        TOKEN2 = 'TOKEN2'
        SIZE = 1
        returned = {'topics': [{'name': TOPIC_NAME}],
                    'nextPageToken': TOKEN2}
        conn = _Connection(returned)
        response = self._callFUT(PROJECT, conn, SIZE, TOKEN1)
        topics = response['topics']
        self.assertEqual(len(topics), 1)
        self.assertEqual(topics[0], {'name': TOPIC_NAME})
        self.assertEqual(response['nextPageToken'], TOKEN2)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/topics' % PROJECT)
        self.assertEqual(req['query_params'],
                         {'pageSize': SIZE, 'pageToken': TOKEN1})


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response
