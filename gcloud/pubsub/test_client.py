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


class TestClient(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.pubsub.client import Client
        return Client

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_implicit(self):
        from gcloud._testing import _monkey_defaults as _monkey_base_defaults
        from gcloud.pubsub._testing import _monkey_defaults
        PROJECT = 'PROJECT'
        connection = _Connection()
        with _monkey_base_defaults(project=PROJECT):
            with _monkey_defaults(connection=connection):
                client = self._makeOne()
        self.assertTrue(client.connection is connection)
        self.assertEqual(client.project, PROJECT)

    def test_ctor_explicit(self):
        PROJECT = 'PROJECT'
        connection = _Connection()
        client = self._makeOne(connection, PROJECT)
        self.assertTrue(client.connection is connection)
        self.assertEqual(client.project, PROJECT)

    def test_topic(self):
        from gcloud.pubsub.client import _Topic
        from gcloud.pubsub.topic import Topic
        PROJECT = 'PROJECT'
        TOPIC_NAME = 'topic_name'
        connection = _Connection()
        client = self._makeOne(connection, PROJECT)
        topic = client.topic(TOPIC_NAME)
        self.assertTrue(isinstance(topic, _Topic))
        self.assertTrue(isinstance(topic._wrapped, Topic))
        self.assertTrue(topic._client is client)
        self.assertEqual(topic.name, TOPIC_NAME)
        self.assertEqual(topic.full_name,
                         'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME))

    def test_list_topics_defaults(self):
        from gcloud.pubsub.client import _Topic
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        returned = {'topics': [{'name': TOPIC_PATH}]}
        connection = _Connection(returned)
        client = self._makeOne(connection, PROJECT)
        topics, next_page_token = client.list_topics()
        self.assertEqual(len(topics), 1)
        self.assertTrue(isinstance(topics[0], _Topic))
        self.assertEqual(topics[0].name, TOPIC_NAME)
        self.assertEqual(next_page_token, None)
        self.assertEqual(len(connection._requested), 1)
        req = connection._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/topics' % PROJECT)
        self.assertEqual(req['query_params'], {})

    def test_list_topics_explicit(self):
        from gcloud.pubsub.client import _Topic
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        TOKEN1 = 'TOKEN1'
        TOKEN2 = 'TOKEN2'
        SIZE = 1
        returned = {'topics': [{'name': TOPIC_PATH}],
                    'nextPageToken': TOKEN2}
        connection = _Connection(returned)
        client = self._makeOne(connection, PROJECT)
        topics, next_page_token = client.list_topics(SIZE, TOKEN1)
        self.assertEqual(len(topics), 1)
        self.assertTrue(isinstance(topics[0], _Topic))
        self.assertTrue(topics[0]._client is client)
        self.assertEqual(topics[0].name, TOPIC_NAME)
        self.assertEqual(next_page_token, TOKEN2)
        self.assertEqual(len(connection._requested), 1)
        req = connection._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/topics' % PROJECT)
        self.assertEqual(req['query_params'],
                         {'pageSize': SIZE, 'pageToken': TOKEN1})

    def test_list_subscriptions_defaults(self):
        from gcloud.pubsub.client import _Subscription
        from gcloud.pubsub.client import _Topic
        PROJECT = 'PROJECT'
        SUB_NAME = 'subscription_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        TOPIC_NAME = 'topic_name'
        TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        SUB_INFO = [{'name': SUB_PATH, 'topic': TOPIC_PATH}]
        returned = {'subscriptions': SUB_INFO}
        connection = _Connection(returned)
        client = self._makeOne(connection, PROJECT)
        subscriptions, next_page_token = client.list_subscriptions()
        self.assertEqual(len(subscriptions), 1)
        self.assertTrue(isinstance(subscriptions[0], _Subscription))
        self.assertTrue(subscriptions[0]._client is client)
        self.assertEqual(subscriptions[0].name, SUB_NAME)
        self.assertTrue(isinstance(subscriptions[0].topic, _Topic))
        self.assertTrue(subscriptions[0].topic._client is client)
        self.assertEqual(subscriptions[0].topic.name, TOPIC_NAME)
        self.assertEqual(next_page_token, None)
        self.assertEqual(len(connection._requested), 1)
        req = connection._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/subscriptions' % PROJECT)
        self.assertEqual(req['query_params'], {})

    def test_list_subscriptions_w_paging(self):
        from gcloud.pubsub.client import _Subscription
        from gcloud.pubsub.client import _Topic
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
        connection = _Connection(returned)
        client = self._makeOne(connection, PROJECT)
        subscriptions, next_page_token = client.list_subscriptions(
            SIZE, TOKEN1)
        self.assertEqual(len(subscriptions), 1)
        self.assertTrue(isinstance(subscriptions[0], _Subscription))
        self.assertEqual(subscriptions[0].name, SUB_NAME)
        self.assertTrue(isinstance(subscriptions[0].topic, _Topic))
        self.assertTrue(subscriptions[0].topic._client is client)
        self.assertEqual(subscriptions[0].topic.name, TOPIC_NAME)
        self.assertEqual(subscriptions[0].ack_deadline, ACK_DEADLINE)
        self.assertEqual(subscriptions[0].push_endpoint, PUSH_ENDPOINT)
        self.assertEqual(next_page_token, TOKEN2)
        self.assertEqual(len(connection._requested), 1)
        req = connection._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/subscriptions' % PROJECT)
        self.assertEqual(req['query_params'],
                         {'pageSize': SIZE, 'pageToken': TOKEN1})


class Test_Topic(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.pubsub.client import _Topic
        return _Topic

    def _makeOne(self, wrapped, client):
        return self._getTargetClass()(wrapped, client)

    def test_ctor_and_properties(self):
        TOPIC_NAME = 'TOPIC'
        TOPIC_FULL_NAME = 'projects/PROJECT/topics/%s' % TOPIC_NAME
        TOPIC_PATH = '/%s' % TOPIC_FULL_NAME
        client = _Dummy()
        wrapped = _Dummy(name=TOPIC_NAME,
                         full_name=TOPIC_FULL_NAME,
                         path=TOPIC_PATH)
        topic = self._makeOne(wrapped, client)
        self.assertTrue(topic._wrapped is wrapped)
        self.assertTrue(topic._client is client)
        self.assertEqual(topic.name, TOPIC_NAME)
        self.assertEqual(topic.full_name, TOPIC_FULL_NAME)
        self.assertEqual(topic.path, TOPIC_PATH)

    def test_subscription(self):
        from gcloud.pubsub.client import _Subscription
        from gcloud.pubsub.client import _Topic
        from gcloud.pubsub.subscription import Subscription
        TOPIC_NAME = 'topic_name'
        SUB_NAME = 'sub_name'
        client = _Dummy()
        wrapped = _Dummy(name=TOPIC_NAME)
        topic = self._makeOne(wrapped, client)
        subscription = topic.subscription(SUB_NAME)
        self.assertTrue(isinstance(subscription, _Subscription))
        self.assertTrue(isinstance(subscription._wrapped, Subscription))
        self.assertTrue(subscription._client is client)
        self.assertTrue(isinstance(subscription.topic, _Topic))
        self.assertEqual(subscription.name, SUB_NAME)


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response


class _Dummy(object):

    def __init__(self, **kw):
        self.__dict__.update(kw)
