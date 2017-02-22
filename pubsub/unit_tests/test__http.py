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


class _Base(unittest.TestCase):
    PROJECT = 'PROJECT'
    LIST_TOPICS_PATH = 'projects/%s/topics' % (PROJECT,)
    LIST_SUBSCRIPTIONS_PATH = 'projects/%s/subscriptions' % (PROJECT,)
    TOPIC_NAME = 'topic_name'
    TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
    LIST_TOPIC_SUBSCRIPTIONS_PATH = '%s/subscriptions' % (TOPIC_PATH,)
    SUB_NAME = 'subscription_name'
    SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)


class TestConnection(_Base):

    @staticmethod
    def _get_target_class():
        from google.cloud.pubsub._http import Connection

        return Connection

    def test_default_url(self):
        conn = self._make_one(object())
        klass = self._get_target_class()
        self.assertEqual(conn.api_base_url, klass.API_BASE_URL)

    def test_custom_url_from_env(self):
        from google.cloud.environment_vars import PUBSUB_EMULATOR

        HOST = 'localhost:8187'
        fake_environ = {PUBSUB_EMULATOR: HOST}

        with mock.patch('os.environ', new=fake_environ):
            conn = self._make_one(object())

        klass = self._get_target_class()
        self.assertNotEqual(conn.api_base_url, klass.API_BASE_URL)
        self.assertEqual(conn.api_base_url, 'http://' + HOST)

    def test_build_api_url_no_extra_query_params(self):
        conn = self._make_one(object())
        URI = '/'.join([
            conn.API_BASE_URL,
            conn.API_VERSION,
            'foo',
        ])
        self.assertEqual(conn.build_api_url('/foo'), URI)

    def test_build_api_url_w_extra_query_params(self):
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit

        conn = self._make_one(object())
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
        conn = self._make_one(object())
        conn.api_base_url = base_url1
        URI = '/'.join([
            base_url2,
            conn.API_VERSION,
            'foo',
        ])
        self.assertEqual(conn.build_api_url('/foo', api_base_url=base_url2),
                         URI)

    def test_extra_headers(self):
        from google.cloud import _http as base_http
        from google.cloud.pubsub import _http as MUT

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


class Test_PublisherAPI(_Base):

    @staticmethod
    def _get_target_class():
        from google.cloud.pubsub._http import _PublisherAPI

        return _PublisherAPI

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        connection = _Connection()
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)
        self.assertIs(api._client, client)
        self.assertEqual(api.api_request, connection.api_request)

    def test_list_topics_no_paging(self):
        from google.cloud.pubsub.topic import Topic

        returned = {'topics': [{'name': self.TOPIC_PATH}]}
        connection = _Connection(returned)
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        iterator = api.list_topics(self.PROJECT)
        topics = list(iterator)
        next_token = iterator.next_page_token

        self.assertEqual(len(topics), 1)
        topic = topics[0]
        self.assertIsInstance(topic, Topic)
        self.assertEqual(topic.name, self.TOPIC_NAME)
        self.assertEqual(topic.full_name, self.TOPIC_PATH)
        self.assertIsNone(next_token)

        self.assertEqual(connection._called_with['method'], 'GET')
        path = '/%s' % (self.LIST_TOPICS_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['query_params'], {})

    def test_list_topics_with_paging(self):
        import six
        from google.cloud.pubsub.topic import Topic

        TOKEN1 = 'TOKEN1'
        TOKEN2 = 'TOKEN2'
        SIZE = 1
        RETURNED = {
            'topics': [{'name': self.TOPIC_PATH}],
            'nextPageToken': 'TOKEN2',
        }
        connection = _Connection(RETURNED)
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        iterator = api.list_topics(
            self.PROJECT, page_token=TOKEN1, page_size=SIZE)
        page = six.next(iterator.pages)
        topics = list(page)
        next_token = iterator.next_page_token

        self.assertEqual(len(topics), 1)
        topic = topics[0]
        self.assertIsInstance(topic, Topic)
        self.assertEqual(topic.name, self.TOPIC_NAME)
        self.assertEqual(topic.full_name, self.TOPIC_PATH)
        self.assertEqual(next_token, TOKEN2)

        self.assertEqual(connection._called_with['method'], 'GET')
        path = '/%s' % (self.LIST_TOPICS_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['query_params'],
                         {'pageToken': TOKEN1, 'pageSize': SIZE})

    def test_list_topics_missing_key(self):
        returned = {}
        connection = _Connection(returned)
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        iterator = api.list_topics(self.PROJECT)
        topics = list(iterator)
        next_token = iterator.next_page_token

        self.assertEqual(len(topics), 0)
        self.assertIsNone(next_token)

        self.assertEqual(connection._called_with['method'], 'GET')
        path = '/%s' % (self.LIST_TOPICS_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['query_params'], {})

    def test_topic_create(self):
        RETURNED = {'name': self.TOPIC_PATH}
        connection = _Connection(RETURNED)
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        resource = api.topic_create(self.TOPIC_PATH)

        self.assertEqual(resource, RETURNED)
        self.assertEqual(connection._called_with['method'], 'PUT')
        path = '/%s' % (self.TOPIC_PATH,)
        self.assertEqual(connection._called_with['path'], path)

    def test_topic_create_already_exists(self):
        from google.cloud.exceptions import Conflict

        connection = _Connection()
        connection._no_response_error = Conflict
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        with self.assertRaises(Conflict):
            api.topic_create(self.TOPIC_PATH)

        self.assertEqual(connection._called_with['method'], 'PUT')
        path = '/%s' % (self.TOPIC_PATH,)
        self.assertEqual(connection._called_with['path'], path)

    def test_topic_get_hit(self):
        RETURNED = {'name': self.TOPIC_PATH}
        connection = _Connection(RETURNED)
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        resource = api.topic_get(self.TOPIC_PATH)

        self.assertEqual(resource, RETURNED)
        self.assertEqual(connection._called_with['method'], 'GET')
        path = '/%s' % (self.TOPIC_PATH,)
        self.assertEqual(connection._called_with['path'], path)

    def test_topic_get_miss(self):
        from google.cloud.exceptions import NotFound

        connection = _Connection()
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        with self.assertRaises(NotFound):
            api.topic_get(self.TOPIC_PATH)

        self.assertEqual(connection._called_with['method'], 'GET')
        path = '/%s' % (self.TOPIC_PATH,)
        self.assertEqual(connection._called_with['path'], path)

    def test_topic_delete_hit(self):
        RETURNED = {}
        connection = _Connection(RETURNED)
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        api.topic_delete(self.TOPIC_PATH)

        self.assertEqual(connection._called_with['method'], 'DELETE')
        path = '/%s' % (self.TOPIC_PATH,)
        self.assertEqual(connection._called_with['path'], path)

    def test_topic_delete_miss(self):
        from google.cloud.exceptions import NotFound

        connection = _Connection()
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        with self.assertRaises(NotFound):
            api.topic_delete(self.TOPIC_PATH)

        self.assertEqual(connection._called_with['method'], 'DELETE')
        path = '/%s' % (self.TOPIC_PATH,)
        self.assertEqual(connection._called_with['path'], path)

    def test_topic_publish_hit(self):
        import base64

        PAYLOAD = b'This is the message text'
        B64_PAYLOAD = base64.b64encode(PAYLOAD).decode('ascii')
        MSGID = 'DEADBEEF'
        MESSAGE = {'data': PAYLOAD, 'attributes': {}}
        B64MSG = {'data': B64_PAYLOAD, 'attributes': {}}
        RETURNED = {'messageIds': [MSGID]}
        connection = _Connection(RETURNED)
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        resource = api.topic_publish(self.TOPIC_PATH, [MESSAGE])

        self.assertEqual(resource, [MSGID])
        self.assertEqual(connection._called_with['method'], 'POST')
        path = '/%s:publish' % (self.TOPIC_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['data'],
                         {'messages': [B64MSG]})
        msg_data = connection._called_with['data']['messages'][0]['data']
        self.assertEqual(msg_data, B64_PAYLOAD)

    def test_topic_publish_twice(self):
        import base64

        PAYLOAD = b'This is the message text'
        B64_PAYLOAD = base64.b64encode(PAYLOAD).decode('ascii')
        MESSAGE = {'data': PAYLOAD, 'attributes': {}}
        RETURNED = {'messageIds': []}
        connection = _Connection(RETURNED, RETURNED)
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        api.topic_publish(self.TOPIC_PATH, [MESSAGE])
        api.topic_publish(self.TOPIC_PATH, [MESSAGE])

        messages = connection._called_with['data']['messages']
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]['data'], B64_PAYLOAD)

    def test_topic_publish_miss(self):
        import base64
        from google.cloud.exceptions import NotFound

        PAYLOAD = b'This is the message text'
        B64_PAYLOAD = base64.b64encode(PAYLOAD).decode('ascii')
        MESSAGE = {'data': PAYLOAD, 'attributes': {}}
        B64MSG = {'data': B64_PAYLOAD, 'attributes': {}}
        connection = _Connection()
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        with self.assertRaises(NotFound):
            api.topic_publish(self.TOPIC_PATH, [MESSAGE])

        self.assertEqual(connection._called_with['method'], 'POST')
        path = '/%s:publish' % (self.TOPIC_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['data'],
                         {'messages': [B64MSG]})

    def test_topic_list_subscriptions_no_paging(self):
        from google.cloud.pubsub.topic import Topic
        from google.cloud.pubsub.subscription import Subscription

        local_sub_path = 'projects/%s/subscriptions/%s' % (
            self.PROJECT, self.SUB_NAME)
        RETURNED = {'subscriptions': [local_sub_path]}
        connection = _Connection(RETURNED)
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        topic = Topic(self.TOPIC_NAME, client)
        iterator = api.topic_list_subscriptions(topic)
        subscriptions = list(iterator)
        next_token = iterator.next_page_token

        self.assertIsNone(next_token)
        self.assertEqual(len(subscriptions), 1)
        subscription = subscriptions[0]
        self.assertIsInstance(subscription, Subscription)
        self.assertEqual(subscription.name, self.SUB_NAME)
        self.assertEqual(subscription.topic, topic)
        self.assertIs(subscription._client, client)

        self.assertEqual(connection._called_with['method'], 'GET')
        path = '/%s' % (self.LIST_TOPIC_SUBSCRIPTIONS_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['query_params'], {})

    def test_topic_list_subscriptions_with_paging(self):
        import six
        from google.cloud.pubsub.subscription import Subscription
        from google.cloud.pubsub.topic import Topic

        TOKEN1 = 'TOKEN1'
        TOKEN2 = 'TOKEN2'
        SIZE = 1
        local_sub_path = 'projects/%s/subscriptions/%s' % (
            self.PROJECT, self.SUB_NAME)
        RETURNED = {
            'subscriptions': [local_sub_path],
            'nextPageToken': TOKEN2,
        }
        connection = _Connection(RETURNED)
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        topic = Topic(self.TOPIC_NAME, client)
        iterator = api.topic_list_subscriptions(
            topic, page_token=TOKEN1, page_size=SIZE)
        page = six.next(iterator.pages)
        subscriptions = list(page)
        next_token = iterator.next_page_token

        self.assertEqual(next_token, TOKEN2)
        self.assertEqual(len(subscriptions), 1)
        subscription = subscriptions[0]
        self.assertIsInstance(subscription, Subscription)
        self.assertEqual(subscription.name, self.SUB_NAME)
        self.assertEqual(subscription.topic, topic)
        self.assertIs(subscription._client, client)

        self.assertEqual(connection._called_with['method'], 'GET')
        path = '/%s' % (self.LIST_TOPIC_SUBSCRIPTIONS_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['query_params'],
                         {'pageToken': TOKEN1, 'pageSize': SIZE})

    def test_topic_list_subscriptions_missing_key(self):
        from google.cloud.pubsub.topic import Topic

        connection = _Connection({})
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        topic = Topic(self.TOPIC_NAME, client)
        iterator = api.topic_list_subscriptions(topic)
        subscriptions = list(iterator)
        next_token = iterator.next_page_token

        self.assertEqual(len(subscriptions), 0)
        self.assertIsNone(next_token)

        self.assertEqual(connection._called_with['method'], 'GET')
        path = '/%s' % (self.LIST_TOPIC_SUBSCRIPTIONS_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['query_params'], {})

    def test_topic_list_subscriptions_miss(self):
        from google.cloud.exceptions import NotFound
        from google.cloud.pubsub.topic import Topic

        connection = _Connection()
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        with self.assertRaises(NotFound):
            topic = Topic(self.TOPIC_NAME, client)
            list(api.topic_list_subscriptions(topic))

        self.assertEqual(connection._called_with['method'], 'GET')
        path = '/%s' % (self.LIST_TOPIC_SUBSCRIPTIONS_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['query_params'], {})


class Test_SubscriberAPI(_Base):

    @staticmethod
    def _get_target_class():
        from google.cloud.pubsub._http import _SubscriberAPI

        return _SubscriberAPI

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        connection = _Connection()
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)
        self.assertIs(api._client, client)
        self.assertEqual(api.api_request, connection.api_request)

    def test_list_subscriptions_no_paging(self):
        from google.cloud.pubsub.client import Client
        from google.cloud.pubsub.subscription import Subscription
        from google.cloud.pubsub.topic import Topic

        SUB_INFO = {'name': self.SUB_PATH, 'topic': self.TOPIC_PATH}
        RETURNED = {'subscriptions': [SUB_INFO]}
        connection = _Connection(RETURNED)
        creds = _make_credentials()
        client = Client(project=self.PROJECT, credentials=creds)
        client._connection = connection
        api = self._make_one(client)

        iterator = api.list_subscriptions(self.PROJECT)
        subscriptions = list(iterator)
        next_token = iterator.next_page_token

        # Check the token returned.
        self.assertIsNone(next_token)
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

        self.assertEqual(connection._called_with['method'], 'GET')
        path = '/%s' % (self.LIST_SUBSCRIPTIONS_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['query_params'], {})

    def test_list_subscriptions_with_paging(self):
        import six
        from google.cloud.pubsub.client import Client
        from google.cloud.pubsub.subscription import Subscription
        from google.cloud.pubsub.topic import Topic

        TOKEN1 = 'TOKEN1'
        TOKEN2 = 'TOKEN2'
        SIZE = 1
        SUB_INFO = {'name': self.SUB_PATH, 'topic': self.TOPIC_PATH}
        RETURNED = {
            'subscriptions': [SUB_INFO],
            'nextPageToken': 'TOKEN2',
        }
        connection = _Connection(RETURNED)
        creds = _make_credentials()
        client = Client(project=self.PROJECT, credentials=creds)
        client._connection = connection
        api = self._make_one(client)

        iterator = api.list_subscriptions(
            self.PROJECT, page_token=TOKEN1, page_size=SIZE)
        page = six.next(iterator.pages)
        subscriptions = list(page)
        next_token = iterator.next_page_token

        # Check the token returned.
        self.assertEqual(next_token, TOKEN2)
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

        self.assertEqual(connection._called_with['method'], 'GET')
        path = '/%s' % (self.LIST_SUBSCRIPTIONS_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['query_params'],
                         {'pageToken': TOKEN1, 'pageSize': SIZE})

    def test_list_subscriptions_missing_key(self):
        RETURNED = {}
        connection = _Connection(RETURNED)
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        iterator = api.list_subscriptions(self.PROJECT)
        subscriptions = list(iterator)
        next_token = iterator.next_page_token

        self.assertEqual(len(subscriptions), 0)
        self.assertIsNone(next_token)

        self.assertEqual(connection._called_with['method'], 'GET')
        path = '/%s' % (self.LIST_SUBSCRIPTIONS_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['query_params'], {})

    def test_subscription_create_defaults(self):
        RESOURCE = {'topic': self.TOPIC_PATH}
        RETURNED = RESOURCE.copy()
        RETURNED['name'] = self.SUB_PATH
        connection = _Connection(RETURNED)
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        resource = api.subscription_create(self.SUB_PATH, self.TOPIC_PATH)

        self.assertEqual(resource, RETURNED)
        self.assertEqual(connection._called_with['method'], 'PUT')
        path = '/%s' % (self.SUB_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['data'], RESOURCE)

    def test_subscription_create_explicit(self):
        ACK_DEADLINE = 90
        PUSH_ENDPOINT = 'https://api.example.com/push'
        RESOURCE = {
            'topic': self.TOPIC_PATH,
            'ackDeadlineSeconds': ACK_DEADLINE,
            'pushConfig': {
                'pushEndpoint': PUSH_ENDPOINT,
            },
        }
        RETURNED = RESOURCE.copy()
        RETURNED['name'] = self.SUB_PATH
        connection = _Connection(RETURNED)
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        resource = api.subscription_create(
            self.SUB_PATH, self.TOPIC_PATH,
            ack_deadline=ACK_DEADLINE, push_endpoint=PUSH_ENDPOINT)

        self.assertEqual(resource, RETURNED)
        self.assertEqual(connection._called_with['method'], 'PUT')
        path = '/%s' % (self.SUB_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['data'], RESOURCE)

    def test_subscription_get(self):
        ACK_DEADLINE = 90
        PUSH_ENDPOINT = 'https://api.example.com/push'
        RETURNED = {
            'topic': self.TOPIC_PATH,
            'name': self.SUB_PATH,
            'ackDeadlineSeconds': ACK_DEADLINE,
            'pushConfig': {'pushEndpoint': PUSH_ENDPOINT},
        }
        connection = _Connection(RETURNED)
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        resource = api.subscription_get(self.SUB_PATH)

        self.assertEqual(resource, RETURNED)
        self.assertEqual(connection._called_with['method'], 'GET')
        path = '/%s' % (self.SUB_PATH,)
        self.assertEqual(connection._called_with['path'], path)

    def test_subscription_delete(self):
        RETURNED = {}
        connection = _Connection(RETURNED)
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        api.subscription_delete(self.SUB_PATH)

        self.assertEqual(connection._called_with['method'], 'DELETE')
        path = '/%s' % (self.SUB_PATH,)
        self.assertEqual(connection._called_with['path'], path)

    def test_subscription_modify_push_config(self):
        PUSH_ENDPOINT = 'https://api.example.com/push'
        BODY = {
            'pushConfig': {'pushEndpoint': PUSH_ENDPOINT},
        }
        RETURNED = {}
        connection = _Connection(RETURNED)
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        api.subscription_modify_push_config(self.SUB_PATH, PUSH_ENDPOINT)

        self.assertEqual(connection._called_with['method'], 'POST')
        path = '/%s:modifyPushConfig' % (self.SUB_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['data'], BODY)

    def test_subscription_pull_defaults(self):
        import base64

        PAYLOAD = b'This is the message text'
        B64 = base64.b64encode(PAYLOAD).decode('ascii')
        ACK_ID = 'DEADBEEF'
        MSG_ID = 'BEADCAFE'
        MESSAGE = {'messageId': MSG_ID, 'data': B64, 'attributes': {'a': 'b'}}
        RETURNED = {
            'receivedMessages': [{'ackId': ACK_ID, 'message': MESSAGE}],
        }
        connection = _Connection(RETURNED)
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)
        BODY = {
            'returnImmediately': False,
            'maxMessages': 1,
        }

        received = api.subscription_pull(self.SUB_PATH)

        self.assertEqual(received, RETURNED['receivedMessages'])
        self.assertEqual(received[0]['message']['data'], PAYLOAD)
        self.assertEqual(connection._called_with['method'], 'POST')
        path = '/%s:pull' % (self.SUB_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['data'], BODY)

    def test_subscription_pull_explicit(self):
        import base64

        PAYLOAD = b'This is the message text'
        B64 = base64.b64encode(PAYLOAD).decode('ascii')
        ACK_ID = 'DEADBEEF'
        MSG_ID = 'BEADCAFE'
        MESSAGE = {'messageId': MSG_ID, 'data': B64, 'attributes': {'a': 'b'}}
        RETURNED = {
            'receivedMessages': [{'ackId': ACK_ID, 'message': MESSAGE}],
        }
        connection = _Connection(RETURNED)
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)
        MAX_MESSAGES = 10
        BODY = {
            'returnImmediately': True,
            'maxMessages': MAX_MESSAGES,
        }

        received = api.subscription_pull(
            self.SUB_PATH, return_immediately=True, max_messages=MAX_MESSAGES)

        self.assertEqual(received, RETURNED['receivedMessages'])
        self.assertEqual(connection._called_with['method'], 'POST')
        path = '/%s:pull' % (self.SUB_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['data'], BODY)

    def test_subscription_acknowledge(self):
        ACK_ID1 = 'DEADBEEF'
        ACK_ID2 = 'BEADCAFE'
        BODY = {
            'ackIds': [ACK_ID1, ACK_ID2],
        }
        RETURNED = {}
        connection = _Connection(RETURNED)
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        api.subscription_acknowledge(self.SUB_PATH, [ACK_ID1, ACK_ID2])

        self.assertEqual(connection._called_with['method'], 'POST')
        path = '/%s:acknowledge' % (self.SUB_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['data'], BODY)

    def test_subscription_modify_ack_deadline(self):
        ACK_ID1 = 'DEADBEEF'
        ACK_ID2 = 'BEADCAFE'
        NEW_DEADLINE = 90
        BODY = {
            'ackIds': [ACK_ID1, ACK_ID2],
            'ackDeadlineSeconds': NEW_DEADLINE,
        }
        RETURNED = {}
        connection = _Connection(RETURNED)
        client = _Client(connection, self.PROJECT)
        api = self._make_one(client)

        api.subscription_modify_ack_deadline(
            self.SUB_PATH, [ACK_ID1, ACK_ID2], NEW_DEADLINE)

        self.assertEqual(connection._called_with['method'], 'POST')
        path = '/%s:modifyAckDeadline' % (self.SUB_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['data'], BODY)


class Test_IAMPolicyAPI(_Base):

    @staticmethod
    def _get_target_class():
        from google.cloud.pubsub._http import _IAMPolicyAPI

        return _IAMPolicyAPI

    def test_ctor(self):
        connection = _Connection()
        client = _Client(connection, None)
        api = self._make_one(client)
        self.assertEqual(api.api_request, connection.api_request)

    def test_get_iam_policy(self):
        from google.cloud.pubsub.iam import OWNER_ROLE
        from google.cloud.pubsub.iam import EDITOR_ROLE
        from google.cloud.pubsub.iam import VIEWER_ROLE

        OWNER1 = 'user:phred@example.com'
        OWNER2 = 'group:cloud-logs@google.com'
        EDITOR1 = 'domain:google.com'
        EDITOR2 = 'user:phred@example.com'
        VIEWER1 = 'serviceAccount:1234-abcdef@service.example.com'
        VIEWER2 = 'user:phred@example.com'
        RETURNED = {
            'etag': 'DEADBEEF',
            'version': 17,
            'bindings': [
                {'role': OWNER_ROLE, 'members': [OWNER1, OWNER2]},
                {'role': EDITOR_ROLE, 'members': [EDITOR1, EDITOR2]},
                {'role': VIEWER_ROLE, 'members': [VIEWER1, VIEWER2]},
            ],
        }
        connection = _Connection(RETURNED)
        client = _Client(connection, None)
        api = self._make_one(client)

        policy = api.get_iam_policy(self.TOPIC_PATH)

        self.assertEqual(policy, RETURNED)
        self.assertEqual(connection._called_with['method'], 'GET')
        path = '/%s:getIamPolicy' % (self.TOPIC_PATH,)
        self.assertEqual(connection._called_with['path'], path)

    def test_set_iam_policy(self):
        from google.cloud.pubsub.iam import OWNER_ROLE
        from google.cloud.pubsub.iam import EDITOR_ROLE
        from google.cloud.pubsub.iam import VIEWER_ROLE

        OWNER1 = 'user:phred@example.com'
        OWNER2 = 'group:cloud-logs@google.com'
        EDITOR1 = 'domain:google.com'
        EDITOR2 = 'user:phred@example.com'
        VIEWER1 = 'serviceAccount:1234-abcdef@service.example.com'
        VIEWER2 = 'user:phred@example.com'
        POLICY = {
            'etag': 'DEADBEEF',
            'version': 17,
            'bindings': [
                {'role': OWNER_ROLE, 'members': [OWNER1, OWNER2]},
                {'role': EDITOR_ROLE, 'members': [EDITOR1, EDITOR2]},
                {'role': VIEWER_ROLE, 'members': [VIEWER1, VIEWER2]},
            ],
        }
        RETURNED = POLICY.copy()
        connection = _Connection(RETURNED)
        client = _Client(connection, None)
        api = self._make_one(client)

        policy = api.set_iam_policy(self.TOPIC_PATH, POLICY)

        self.assertEqual(policy, RETURNED)
        self.assertEqual(connection._called_with['method'], 'POST')
        path = '/%s:setIamPolicy' % (self.TOPIC_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['data'],
                         {'policy': POLICY})

    def test_test_iam_permissions(self):
        from google.cloud.pubsub.iam import OWNER_ROLE
        from google.cloud.pubsub.iam import EDITOR_ROLE
        from google.cloud.pubsub.iam import VIEWER_ROLE

        ALL_ROLES = [OWNER_ROLE, EDITOR_ROLE, VIEWER_ROLE]
        ALLOWED = ALL_ROLES[1:]
        RETURNED = {'permissions': ALLOWED}
        connection = _Connection(RETURNED)
        client = _Client(connection, None)
        api = self._make_one(client)

        allowed = api.test_iam_permissions(self.TOPIC_PATH, ALL_ROLES)

        self.assertEqual(allowed, ALLOWED)
        self.assertEqual(connection._called_with['method'], 'POST')
        path = '/%s:testIamPermissions' % (self.TOPIC_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['data'],
                         {'permissions': ALL_ROLES})

    def test_test_iam_permissions_missing_key(self):
        from google.cloud.pubsub.iam import OWNER_ROLE
        from google.cloud.pubsub.iam import EDITOR_ROLE
        from google.cloud.pubsub.iam import VIEWER_ROLE

        ALL_ROLES = [OWNER_ROLE, EDITOR_ROLE, VIEWER_ROLE]
        RETURNED = {}
        connection = _Connection(RETURNED)
        client = _Client(connection, None)
        api = self._make_one(client)

        allowed = api.test_iam_permissions(self.TOPIC_PATH, ALL_ROLES)

        self.assertEqual(allowed, [])
        self.assertEqual(connection._called_with['method'], 'POST')
        path = '/%s:testIamPermissions' % (self.TOPIC_PATH,)
        self.assertEqual(connection._called_with['path'], path)
        self.assertEqual(connection._called_with['data'],
                         {'permissions': ALL_ROLES})


class Test__transform_messages_base64_empty(unittest.TestCase):
    def _call_fut(self, messages, transform, key=None):
        from google.cloud.pubsub._http import _transform_messages_base64

        return _transform_messages_base64(messages, transform, key)

    def test__transform_messages_base64_empty_message(self):
        from base64 import b64decode

        DATA = [{'message': {}}]
        self._call_fut(DATA, b64decode, 'message')
        self.assertEqual(DATA, [{'message': {}}])

    def test__transform_messages_base64_empty_data(self):
        from base64 import b64decode

        DATA = [{'message': {'data': b''}}]
        self._call_fut(DATA, b64decode, 'message')
        self.assertEqual(DATA, [{'message': {'data': b''}}])

    def test__transform_messages_base64_pull(self):
        from base64 import b64encode

        DATA = [{'message': {'data': b'testing 1 2 3'}}]
        self._call_fut(DATA, b64encode, 'message')
        self.assertEqual(DATA[0]['message']['data'],
                         b64encode(b'testing 1 2 3'))

    def test__transform_messages_base64_publish(self):
        from base64 import b64encode

        DATA = [{'data': b'testing 1 2 3'}]
        self._call_fut(DATA, b64encode)
        self.assertEqual(DATA[0]['data'], b64encode(b'testing 1 2 3'))


class _Connection(object):

    _called_with = None
    _no_response_error = None

    def __init__(self, *responses):
        self._responses = responses

    def api_request(self, **kw):
        from google.cloud.exceptions import NotFound

        self._called_with = kw
        try:
            response, self._responses = self._responses[0], self._responses[1:]
        except IndexError:
            err_class = self._no_response_error or NotFound
            raise err_class('miss')
        return response


class _Client(object):

    def __init__(self, connection, project):
        self._connection = connection
        self.project = project
