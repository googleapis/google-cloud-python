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

    def test_list_topics_no_paging(self):
        from gcloud.pubsub.topic import Topic
        PROJECT = 'PROJECT'
        CREDS = _Credentials()

        CLIENT_OBJ = self._makeOne(project=PROJECT, credentials=CREDS)

        TOPIC_NAME = 'topic_name'
        TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)

        RETURNED = {'topics': [{'name': TOPIC_PATH}]}
        # Replace the connection on the client with one of our own.
        CLIENT_OBJ.connection = _Connection(RETURNED)

        # Execute request.
        topics, next_page_token = CLIENT_OBJ.list_topics()
        # Test values are correct.
        self.assertEqual(len(topics), 1)
        self.assertTrue(isinstance(topics[0], Topic))
        self.assertEqual(topics[0].name, TOPIC_NAME)
        self.assertEqual(next_page_token, None)
        self.assertEqual(len(CLIENT_OBJ.connection._requested), 1)
        req = CLIENT_OBJ.connection._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/topics' % PROJECT)
        self.assertEqual(req['query_params'], {})

    def test_list_topics_with_paging(self):
        from gcloud.pubsub.topic import Topic
        PROJECT = 'PROJECT'
        CREDS = _Credentials()

        CLIENT_OBJ = self._makeOne(project=PROJECT, credentials=CREDS)

        TOPIC_NAME = 'topic_name'
        TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        TOKEN1 = 'TOKEN1'
        TOKEN2 = 'TOKEN2'
        SIZE = 1
        RETURNED = {'topics': [{'name': TOPIC_PATH}],
                    'nextPageToken': TOKEN2}
        # Replace the connection on the client with one of our own.
        CLIENT_OBJ.connection = _Connection(RETURNED)

        # Execute request.
        topics, next_page_token = CLIENT_OBJ.list_topics(SIZE, TOKEN1)
        # Test values are correct.
        self.assertEqual(len(topics), 1)
        self.assertTrue(isinstance(topics[0], Topic))
        self.assertEqual(topics[0].name, TOPIC_NAME)
        self.assertEqual(next_page_token, TOKEN2)
        self.assertEqual(len(CLIENT_OBJ.connection._requested), 1)
        req = CLIENT_OBJ.connection._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/topics' % PROJECT)
        self.assertEqual(req['query_params'],
                         {'pageSize': SIZE, 'pageToken': TOKEN1})

    def test_list_subscriptions_no_paging(self):
        from gcloud.pubsub.subscription import Subscription
        PROJECT = 'PROJECT'
        CREDS = _Credentials()

        CLIENT_OBJ = self._makeOne(project=PROJECT, credentials=CREDS)

        SUB_NAME = 'subscription_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        TOPIC_NAME = 'topic_name'
        TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        SUB_INFO = [{'name': SUB_PATH, 'topic': TOPIC_PATH}]
        RETURNED = {'subscriptions': SUB_INFO}
        # Replace the connection on the client with one of our own.
        CLIENT_OBJ.connection = _Connection(RETURNED)

        # Execute request.
        subscriptions, next_page_token = CLIENT_OBJ.list_subscriptions()
        # Test values are correct.
        self.assertEqual(len(subscriptions), 1)
        self.assertTrue(isinstance(subscriptions[0], Subscription))
        self.assertEqual(subscriptions[0].name, SUB_NAME)
        self.assertEqual(subscriptions[0].topic.name, TOPIC_NAME)
        self.assertEqual(next_page_token, None)
        self.assertEqual(len(CLIENT_OBJ.connection._requested), 1)
        req = CLIENT_OBJ.connection._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/subscriptions' % PROJECT)
        self.assertEqual(req['query_params'], {})

    def test_list_subscriptions_with_paging(self):
        from gcloud.pubsub.subscription import Subscription
        PROJECT = 'PROJECT'
        CREDS = _Credentials()

        CLIENT_OBJ = self._makeOne(project=PROJECT, credentials=CREDS)

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
        RETURNED = {'subscriptions': SUB_INFO, 'nextPageToken': TOKEN2}
        # Replace the connection on the client with one of our own.
        CLIENT_OBJ.connection = _Connection(RETURNED)

        # Execute request.
        subscriptions, next_page_token = CLIENT_OBJ.list_subscriptions(
            SIZE, TOKEN1)
        # Test values are correct.
        self.assertEqual(len(subscriptions), 1)
        self.assertTrue(isinstance(subscriptions[0], Subscription))
        self.assertEqual(subscriptions[0].name, SUB_NAME)
        self.assertEqual(subscriptions[0].topic.name, TOPIC_NAME)
        self.assertEqual(subscriptions[0].ack_deadline, ACK_DEADLINE)
        self.assertEqual(subscriptions[0].push_endpoint, PUSH_ENDPOINT)
        self.assertEqual(next_page_token, TOKEN2)
        self.assertEqual(len(CLIENT_OBJ.connection._requested), 1)
        req = CLIENT_OBJ.connection._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/projects/%s/subscriptions' % PROJECT)
        self.assertEqual(req['query_params'],
                         {'pageSize': SIZE, 'pageToken': TOKEN1})

    def test_list_subscriptions_with_topic_name(self):
        from gcloud.pubsub.subscription import Subscription
        PROJECT = 'PROJECT'
        CREDS = _Credentials()

        CLIENT_OBJ = self._makeOne(project=PROJECT, credentials=CREDS)

        SUB_NAME_1 = 'subscription_1'
        SUB_PATH_1 = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME_1)
        SUB_NAME_2 = 'subscription_2'
        SUB_PATH_2 = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME_2)
        TOPIC_NAME = 'topic_name'
        TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        SUB_INFO = [{'name': SUB_PATH_1, 'topic': TOPIC_PATH},
                    {'name': SUB_PATH_2, 'topic': TOPIC_PATH}]
        TOKEN = 'TOKEN'
        RETURNED = {'subscriptions': SUB_INFO, 'nextPageToken': TOKEN}
        # Replace the connection on the client with one of our own.
        CLIENT_OBJ.connection = _Connection(RETURNED)

        # Execute request.
        subscriptions, next_page_token = CLIENT_OBJ.list_subscriptions(
            topic_name=TOPIC_NAME)
        # Test values are correct.
        self.assertEqual(len(subscriptions), 2)
        self.assertTrue(isinstance(subscriptions[0], Subscription))
        self.assertEqual(subscriptions[0].name, SUB_NAME_1)
        self.assertEqual(subscriptions[0].topic.name, TOPIC_NAME)
        self.assertTrue(isinstance(subscriptions[1], Subscription))
        self.assertEqual(subscriptions[1].name, SUB_NAME_2)
        self.assertEqual(subscriptions[1].topic.name, TOPIC_NAME)
        self.assertTrue(subscriptions[1].topic is subscriptions[0].topic)
        self.assertEqual(next_page_token, TOKEN)
        self.assertEqual(len(CLIENT_OBJ.connection._requested), 1)
        req = CLIENT_OBJ.connection._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'],
                         '/projects/%s/topics/%s/subscriptions'
                         % (PROJECT, TOPIC_NAME))
        self.assertEqual(req['query_params'], {})

    def test_topic(self):
        PROJECT = 'PROJECT'
        TOPIC_NAME = 'TOPIC_NAME'
        CREDS = _Credentials()

        client_obj = self._makeOne(project=PROJECT, credentials=CREDS)
        new_topic = client_obj.topic(TOPIC_NAME)
        self.assertEqual(new_topic.name, TOPIC_NAME)
        self.assertTrue(new_topic._client is client_obj)
        self.assertEqual(new_topic.project, PROJECT)
        self.assertEqual(new_topic.full_name,
                         'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME))
        self.assertFalse(new_topic.timestamp_messages)


class _Credentials(object):

    _scopes = None

    @staticmethod
    def create_scoped_required():
        return True

    def create_scoped(self, scope):
        self._scopes = scope
        return self


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response
