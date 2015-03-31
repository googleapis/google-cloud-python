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
        from gcloud.pubsub.topic import Topic
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        returned = {'topics': [{'name': TOPIC_PATH}]}
        conn = _Connection(returned)
        topics, next_page_token = self._callFUT(project=PROJECT,
                                                connection=conn)
        self.assertEqual(len(topics), 1)
        self.assertTrue(isinstance(topics[0], Topic))
        self.assertEqual(topics[0].name, TOPIC_NAME)
        self.assertEqual(next_page_token, None)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/topics' % PROJECT)
        self.assertEqual(req['query_params'], {})

    def test_w_implicit_connection_and_project_wo_paging(self):
        from gcloud._testing import _monkey_defaults as _monkey_base_defaults
        from gcloud.pubsub._testing import _monkey_defaults
        from gcloud.pubsub.topic import Topic
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        TOKEN = 'TOKEN'
        returned = {'topics': [{'name': TOPIC_PATH}],
                    'nextPageToken': TOKEN}
        conn = _Connection(returned)
        with _monkey_base_defaults(project=PROJECT):
            with _monkey_defaults(connection=conn):
                topics, next_page_token = self._callFUT()
        self.assertEqual(len(topics), 1)
        self.assertTrue(isinstance(topics[0], Topic))
        self.assertEqual(topics[0].name, TOPIC_NAME)
        self.assertEqual(next_page_token, TOKEN)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/topics' % PROJECT)
        self.assertEqual(req['query_params'], {})

    def test_w_explicit_connection_and_project_w_paging(self):
        from gcloud.pubsub.topic import Topic
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        TOKEN1 = 'TOKEN1'
        TOKEN2 = 'TOKEN2'
        SIZE = 1
        returned = {'topics': [{'name': TOPIC_PATH}],
                    'nextPageToken': TOKEN2}
        conn = _Connection(returned)
        topics, next_page_token = self._callFUT(SIZE, TOKEN1, PROJECT, conn)
        self.assertEqual(len(topics), 1)
        self.assertTrue(isinstance(topics[0], Topic))
        self.assertEqual(topics[0].name, TOPIC_NAME)
        self.assertEqual(next_page_token, TOKEN2)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/topics' % PROJECT)
        self.assertEqual(req['query_params'],
                         {'pageSize': SIZE, 'pageToken': TOKEN1})


class Test_list_subscriptions(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud.pubsub.api import list_subscriptions
        return list_subscriptions(*args, **kw)

    def test_w_implicit_connection_wo_paging(self):
        from gcloud._testing import _monkey_defaults as _monkey_base_defaults
        from gcloud.pubsub._testing import _monkey_defaults
        from gcloud.pubsub.subscription import Subscription
        PROJECT = 'PROJECT'
        SUB_NAME = 'subscription_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        TOPIC_NAME = 'topic_name'
        TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        SUB_INFO = [{'name': SUB_PATH, 'topic': TOPIC_PATH}]
        returned = {'subscriptions': SUB_INFO}
        conn = _Connection(returned)
        with _monkey_base_defaults(project=PROJECT):
            with _monkey_defaults(connection=conn):
                subscriptions, next_page_token = self._callFUT()
        self.assertEqual(len(subscriptions), 1)
        self.assertTrue(isinstance(subscriptions[0], Subscription))
        self.assertEqual(subscriptions[0].name, SUB_NAME)
        self.assertEqual(subscriptions[0].topic.name, TOPIC_NAME)
        self.assertEqual(next_page_token, None)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/subscriptions' % PROJECT)
        self.assertEqual(req['query_params'], {})

    def test_w_explicit_connection_and_project_w_paging(self):
        from gcloud.pubsub.subscription import Subscription
        PROJECT = 'PROJECT'
        SUB_NAME = 'subscription_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        TOPIC_NAME = 'topic_name'
        TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        ACK_DEADLINE = 42
        PUSH_ENDPOINT = 'https://push.example.com/endpoint'
        TOKEN1 = 'TOKEN1'
        TOKEN2 = 'TOKEN2'
        SIZE = 1
        SUB_INFO = [{'name': SUB_PATH,
                     'topic': TOPIC_PATH,
                     'ackDeadlineSeconds': ACK_DEADLINE,
                     'pushConfig': {'pushEndpoint': PUSH_ENDPOINT}}]
        returned = {'subscriptions': SUB_INFO, 'nextPageToken': TOKEN2}
        conn = _Connection(returned)
        subscriptions, next_page_token = self._callFUT(SIZE, TOKEN1,
                                                       project=PROJECT,
                                                       connection=conn)
        self.assertEqual(len(subscriptions), 1)
        self.assertTrue(isinstance(subscriptions[0], Subscription))
        self.assertEqual(subscriptions[0].name, SUB_NAME)
        self.assertEqual(subscriptions[0].topic.name, TOPIC_NAME)
        self.assertEqual(subscriptions[0].ack_deadline, ACK_DEADLINE)
        self.assertEqual(subscriptions[0].push_endpoint, PUSH_ENDPOINT)
        self.assertEqual(next_page_token, TOKEN2)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/subscriptions' % PROJECT)
        self.assertEqual(req['query_params'],
                         {'pageSize': SIZE, 'pageToken': TOKEN1})

    def test_w_topic_name(self):
        from gcloud.pubsub.subscription import Subscription
        PROJECT = 'PROJECT'
        SUB_NAME_1 = 'subscription_1'
        SUB_PATH_1 = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME_1)
        SUB_NAME_2 = 'subscription_2'
        SUB_PATH_2 = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME_2)
        TOPIC_NAME = 'topic_name'
        TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        SUB_INFO = [{'name': SUB_PATH_1, 'topic': TOPIC_PATH},
                    {'name': SUB_PATH_2, 'topic': TOPIC_PATH}]
        TOKEN = 'TOKEN'
        returned = {'subscriptions': SUB_INFO, 'nextPageToken': TOKEN}
        conn = _Connection(returned)
        subscriptions, next_page_token = self._callFUT(topic_name=TOPIC_NAME,
                                                       project=PROJECT,
                                                       connection=conn)
        self.assertEqual(len(subscriptions), 2)
        self.assertTrue(isinstance(subscriptions[0], Subscription))
        self.assertEqual(subscriptions[0].name, SUB_NAME_1)
        self.assertEqual(subscriptions[0].topic.name, TOPIC_NAME)
        self.assertTrue(isinstance(subscriptions[1], Subscription))
        self.assertEqual(subscriptions[1].name, SUB_NAME_2)
        self.assertEqual(subscriptions[1].topic.name, TOPIC_NAME)
        self.assertTrue(subscriptions[1].topic is subscriptions[0].topic)
        self.assertEqual(next_page_token, TOKEN)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'],
                         '/projects/%s/topics/%s/subscriptions'
                         % (PROJECT, TOPIC_NAME))
        self.assertEqual(req['query_params'], {})


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response
