# Copyright 2015 Google Inc.
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


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


class TestClient(unittest.TestCase):
    PROJECT = 'PROJECT'
    TOPIC_NAME = 'topic_name'
    TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
    SUB_NAME = 'subscription_name'
    SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)

    @staticmethod
    def _get_target_class():
        from google.cloud.pubsub.client import Client

        return Client

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_publisher_api_wo_gax(self):
        from google.cloud.pubsub._http import _PublisherAPI

        creds = _make_credentials()

        client = self._make_one(
            project=self.PROJECT, credentials=creds,
            use_gax=False)

        conn = client._connection = _Connection()
        api = client.publisher_api

        self.assertIsInstance(api, _PublisherAPI)
        self.assertEqual(api.api_request, conn.api_request)
        # API instance is cached
        again = client.publisher_api
        self.assertIs(again, api)

    def test_no_gax_ctor(self):
        from google.cloud.pubsub._http import _PublisherAPI

        creds = _make_credentials()
        with mock.patch('google.cloud.pubsub.client._USE_GAX',
                        new=True):
            client = self._make_one(project=self.PROJECT, credentials=creds,
                                    use_gax=False)

        self.assertFalse(client._use_gax)
        api = client.publisher_api
        self.assertIsInstance(api, _PublisherAPI)

    def _publisher_api_w_gax_helper(self, emulator=False):
        from google.cloud.pubsub import _http

        wrapped = object()
        _called_with = []

        def _generated_api(*args, **kw):
            _called_with.append((args, kw))
            return wrapped

        class _GaxPublisherAPI(object):

            def __init__(self, _wrapped, client):
                self._wrapped = _wrapped
                self._client = client

        creds = _make_credentials()
        client = self._make_one(
            project=self.PROJECT, credentials=creds,
            use_gax=True)
        client._connection.in_emulator = emulator

        patch = mock.patch.multiple(
            'google.cloud.pubsub.client',
            make_gax_publisher_api=_generated_api,
            GAXPublisherAPI=_GaxPublisherAPI)
        with patch:
            api = client.publisher_api

        self.assertIsInstance(api, _GaxPublisherAPI)
        self.assertIs(api._wrapped, wrapped)
        self.assertIs(api._client, client)
        # API instance is cached
        again = client.publisher_api
        self.assertIs(again, api)
        if emulator:
            kwargs = {'host': _http.Connection.API_BASE_URL}
        else:
            kwargs = {'credentials': creds}
        self.assertEqual(_called_with, [((), kwargs)])

    def test_publisher_api_w_gax(self):
        self._publisher_api_w_gax_helper()

    def test_publisher_api_w_gax_and_emulator(self):
        self._publisher_api_w_gax_helper(emulator=True)

    def test_subscriber_api_wo_gax(self):
        from google.cloud.pubsub._http import _SubscriberAPI

        creds = _make_credentials()
        client = self._make_one(
            project=self.PROJECT, credentials=creds,
            use_gax=False)

        conn = client._connection = _Connection()
        api = client.subscriber_api

        self.assertIsInstance(api, _SubscriberAPI)
        self.assertEqual(api.api_request, conn.api_request)
        # API instance is cached
        again = client.subscriber_api
        self.assertIs(again, api)

    def _subscriber_api_w_gax_helper(self, emulator=False):
        from google.cloud.pubsub import _http

        wrapped = object()
        _called_with = []

        def _generated_api(*args, **kw):
            _called_with.append((args, kw))
            return wrapped

        class _GaxSubscriberAPI(object):

            def __init__(self, _wrapped, client):
                self._wrapped = _wrapped
                self._client = client

        creds = _make_credentials()
        client = self._make_one(
            project=self.PROJECT, credentials=creds,
            use_gax=True)
        client._connection.in_emulator = emulator

        patch = mock.patch.multiple(
            'google.cloud.pubsub.client',
            make_gax_subscriber_api=_generated_api,
            GAXSubscriberAPI=_GaxSubscriberAPI)
        with patch:
            api = client.subscriber_api

        self.assertIsInstance(api, _GaxSubscriberAPI)
        self.assertIs(api._wrapped, wrapped)
        self.assertIs(api._client, client)
        # API instance is cached
        again = client.subscriber_api
        self.assertIs(again, api)
        if emulator:
            kwargs = {'host': _http.Connection.API_BASE_URL}
        else:
            kwargs = {'credentials': creds}
        self.assertEqual(_called_with, [((), kwargs)])

    def test_subscriber_api_w_gax(self):
        self._subscriber_api_w_gax_helper()

    def test_subscriber_api_w_gax_and_emulator(self):
        self._subscriber_api_w_gax_helper(emulator=True)

    def test_iam_policy_api(self):
        from google.cloud.pubsub._http import _IAMPolicyAPI

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        conn = client._connection = _Connection()

        api = client.iam_policy_api
        self.assertIsInstance(api, _IAMPolicyAPI)
        self.assertEqual(api.api_request, conn.api_request)
        # API instance is cached
        again = client.iam_policy_api
        self.assertIs(again, api)

    def test_list_topics_no_paging(self):
        from google.cloud.pubsub.topic import Topic

        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        client._connection = object()
        api = _FauxPublisherAPI(items=[Topic(self.TOPIC_NAME, client)])
        client._publisher_api = api

        iterator = client.list_topics()
        topics = list(iterator)
        next_page_token = iterator.next_page_token

        self.assertEqual(len(topics), 1)
        self.assertIsInstance(topics[0], Topic)
        self.assertEqual(topics[0].name, self.TOPIC_NAME)
        self.assertIsNone(next_page_token)

        self.assertEqual(api._listed_topics, (self.PROJECT, None, None))

    def test_list_topics_with_paging(self):
        from google.cloud.pubsub.topic import Topic

        TOKEN1 = 'TOKEN1'
        TOKEN2 = 'TOKEN2'
        SIZE = 1
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        client._connection = object()
        api = _FauxPublisherAPI([Topic(self.TOPIC_NAME, client)], TOKEN2)
        client._publisher_api = api

        iterator = client.list_topics(SIZE, TOKEN1)
        topics = list(iterator)
        next_page_token = iterator.next_page_token

        self.assertEqual(len(topics), 1)
        self.assertIsInstance(topics[0], Topic)
        self.assertEqual(topics[0].name, self.TOPIC_NAME)
        self.assertEqual(next_page_token, TOKEN2)

        self.assertEqual(api._listed_topics, (self.PROJECT, 1, TOKEN1))

    def test_list_topics_missing_key(self):
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds)
        client._connection = object()
        api = _FauxPublisherAPI()
        client._publisher_api = api

        iterator = client.list_topics()
        topics = list(iterator)
        next_page_token = iterator.next_page_token

        self.assertEqual(len(topics), 0)
        self.assertIsNone(next_page_token)

        self.assertEqual(api._listed_topics, (self.PROJECT, None, None))

    def test_list_subscriptions_no_paging(self):
        from google.cloud.pubsub.subscription import Subscription
        from google.cloud.pubsub.topic import Topic

        SUB_INFO = {'name': self.SUB_PATH, 'topic': self.TOPIC_PATH}
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                use_gax=False)
        returned = {'subscriptions': [SUB_INFO]}
        client._connection = _Connection(returned)

        iterator = client.list_subscriptions()
        subscriptions = list(iterator)
        next_page_token = iterator.next_page_token

        # Check the token returned.
        self.assertIsNone(next_page_token)
        # Check the subscription object returned.
        self.assertEqual(len(subscriptions), 1)
        subscription = subscriptions[0]
        self.assertIsInstance(subscription, Subscription)
        self.assertEqual(subscription.name, self.SUB_NAME)
        self.assertIsInstance(subscription.topic, Topic)
        self.assertEqual(subscription.topic.name, self.TOPIC_NAME)
        self.assertIs(subscription._client, client)
        self.assertEqual(subscription._project, self.PROJECT)
        self.assertIsNone(subscription.ack_deadline)
        self.assertIsNone(subscription.push_endpoint)

        called_with = client._connection._called_with
        expected_path = '/projects/%s/subscriptions' % (self.PROJECT,)
        self.assertEqual(called_with, {
            'method': 'GET',
            'path': expected_path,
            'query_params': {},
        })

    def test_list_subscriptions_with_paging(self):
        import six
        from google.cloud.pubsub.subscription import Subscription
        from google.cloud.pubsub.topic import Topic

        SUB_INFO = {'name': self.SUB_PATH, 'topic': self.TOPIC_PATH}
        creds = _make_credentials()
        client = self._make_one(project=self.PROJECT, credentials=creds,
                                use_gax=False)

        # Set up the mock response.
        ACK_DEADLINE = 42
        PUSH_ENDPOINT = 'https://push.example.com/endpoint'
        SUB_INFO = {'name': self.SUB_PATH,
                    'topic': self.TOPIC_PATH,
                    'ackDeadlineSeconds': ACK_DEADLINE,
                    'pushConfig': {'pushEndpoint': PUSH_ENDPOINT}}
        TOKEN1 = 'TOKEN1'
        TOKEN2 = 'TOKEN2'
        SIZE = 1
        returned = {
            'subscriptions': [SUB_INFO],
            'nextPageToken': TOKEN2,
        }
        client._connection = _Connection(returned)

        iterator = client.list_subscriptions(
            SIZE, TOKEN1)
        page = six.next(iterator.pages)
        subscriptions = list(page)
        next_page_token = iterator.next_page_token

        # Check the token returned.
        self.assertEqual(next_page_token, TOKEN2)
        # Check the subscription object returned.
        self.assertEqual(len(subscriptions), 1)
        subscription = subscriptions[0]
        self.assertIsInstance(subscription, Subscription)
        self.assertEqual(subscription.name, self.SUB_NAME)
        self.assertIsInstance(subscription.topic, Topic)
        self.assertEqual(subscription.topic.name, self.TOPIC_NAME)
        self.assertIs(subscription._client, client)
        self.assertEqual(subscription._project, self.PROJECT)
        self.assertEqual(subscription.ack_deadline, ACK_DEADLINE)
        self.assertEqual(subscription.push_endpoint, PUSH_ENDPOINT)

        called_with = client._connection._called_with
        expected_path = '/projects/%s/subscriptions' % (self.PROJECT,)
        self.assertEqual(called_with, {
            'method': 'GET',
            'path': expected_path,
            'query_params': {
                'pageSize': SIZE,
                'pageToken': TOKEN1,
            },
        })

    def test_list_subscriptions_w_missing_key(self):
        PROJECT = 'PROJECT'
        creds = _make_credentials()

        client = self._make_one(project=PROJECT, credentials=creds)
        client._connection = object()
        api = client._subscriber_api = _FauxSubscriberAPI()
        api._list_subscriptions_response = (), None

        subscriptions, next_page_token = client.list_subscriptions()

        self.assertEqual(len(subscriptions), 0)
        self.assertIsNone(next_page_token)

        self.assertEqual(api._listed_subscriptions,
                         (self.PROJECT, None, None))

    def test_topic(self):
        PROJECT = 'PROJECT'
        TOPIC_NAME = 'TOPIC_NAME'
        creds = _make_credentials()

        client_obj = self._make_one(project=PROJECT, credentials=creds)
        new_topic = client_obj.topic(TOPIC_NAME)
        self.assertEqual(new_topic.name, TOPIC_NAME)
        self.assertIs(new_topic._client, client_obj)
        self.assertEqual(new_topic.project, PROJECT)
        self.assertEqual(new_topic.full_name,
                         'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME))
        self.assertFalse(new_topic.timestamp_messages)


class _Iterator(object):

    def __init__(self, items, token):
        self._items = items or ()
        self.next_page_token = token

    def __iter__(self):
        return iter(self._items)


class _FauxPublisherAPI(object):

    def __init__(self, items=None, token=None):
        self._items = items
        self._token = token

    def list_topics(self, project, page_size, page_token):
        self._listed_topics = (project, page_size, page_token)
        return _Iterator(self._items, self._token)


class _FauxSubscriberAPI(object):

    def list_subscriptions(self, project, page_size, page_token):
        self._listed_subscriptions = (project, page_size, page_token)
        return self._list_subscriptions_response


class _Connection(object):

    _called_with = None

    def __init__(self, *responses):
        self._responses = responses

    def api_request(self, **kw):
        self._called_with = kw
        response, self._responses = self._responses[0], self._responses[1:]
        return response
